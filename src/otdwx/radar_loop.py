"""Assemble time-ordered, *real* archived-radar frames into an OTDwx GIF.

This module does not download or invent radar. Input PNGs must be genuine,
licensed/pre-cleared archive scan renders with a documented product/site/time.
Requires optional Pillow: pip install Pillow.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.parse import urlparse


def validate_manifest(manifest: dict) -> list[str]:
    problems=[]
    if not isinstance(manifest,dict):return ['manifest must be an object']
    for key in ('title','source_name','source_url','radar_site','product','frames'):
        if not manifest.get(key):problems.append('missing '+key)
    if problems:return problems
    url=urlparse(manifest['source_url'])
    if url.scheme!='https' or not url.netloc:problems.append('HTTPS source URL required')
    frames=manifest['frames']
    if not isinstance(frames,list) or not 2<=len(frames)<=80:
        return problems+['radar GIF needs 2–80 genuine historical frames']
    timestamps=[]
    for index,f in enumerate(frames):
        try:
            stamp=datetime.fromisoformat(f['timestamp_utc'].replace('Z','+00:00'))
            if stamp.utcoffset() is None or stamp.utcoffset().total_seconds()!=0:
                raise ValueError('frame time must be UTC')
            path=Path(f['file'])
            if path.suffix.lower() not in ('.png','.webp'):
                raise ValueError('frame must be PNG or WEBP')
            timestamps.append(stamp)
        except (KeyError,TypeError,ValueError) as exc:
            problems.append(f'frame {index}: {exc}')
    if timestamps and timestamps!=sorted(set(timestamps)):
        problems.append('frame UTC timestamps must be strictly increasing')
    if not manifest.get('media_rights_reviewed',False):
        problems.append('explicit media_rights_reviewed flag required')
    if not manifest.get('data_provenance_reviewed',False):
        problems.append('explicit data_provenance_reviewed flag required')
    return problems


def render_gif(manifest: dict, output: str|Path, *, root: str|Path='.', frame_ms=350):
    """Branded 16:9 GIF from prepared archived radar frames; no data decoding."""
    errors=validate_manifest(manifest)
    if errors:raise ValueError('; '.join(errors))
    if not 120<=frame_ms<=2000:raise ValueError('frame_ms must be 120–2000')
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except ImportError as exc:
        raise RuntimeError('Pillow is required: pip install Pillow') from exc
    canvas=(1600,900)
    def font(size,bold=False):
        paths=['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'] if bold else ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
        paths+=['/Library/Fonts/Arial.ttf','C:/Windows/Fonts/arial.ttf']
        for candidate in paths:
            if Path(candidate).exists():return ImageFont.truetype(candidate,size)
        return ImageFont.load_default()
    small=font(22);medium=font(30,True);strong=font(48,True)
    out=[]
    root=Path(root).resolve()
    for f in manifest['frames']:
        p=(root/f['file']).resolve()
        if not p.is_relative_to(root):raise ValueError('radar frame escapes the private input directory')
        if not p.exists():raise FileNotFoundError(str(p))
        with Image.open(p) as im:
            raw=im.convert('RGB')
            fitted=ImageOps.contain(raw,(1480,645),Image.Resampling.LANCZOS)
        page=Image.new('RGB',canvas,'#f4f1ea');draw=ImageDraw.Draw(page)
        draw.rectangle((70,44,80,95),fill='#126987')
        draw.text((100,43),'OTDwx',font=strong,fill='#1a2c34')
        draw.text((350,65),'RADAR ARCHIVE   /   OBSERVED FRAMES',font=small,fill='#60747b')
        draw.line((70,130,1530,130),fill='#1a2c34',width=3)
        draw.text((72,150),manifest['title'][:75],font=medium,fill='#1a2c34')
        x=60+(1480-fitted.width)//2; y=212+(645-fitted.height)//2
        page.paste(fitted,(x,y))
        draw.line((70,865,1530,865),fill='#1a2c34',width=3)
        stamp=datetime.fromisoformat(f['timestamp_utc'].replace('Z','+00:00'))
        draw.text((72,872),stamp.strftime('%Y-%m-%d  %H:%M UTC'),font=small,fill='#126987')
        right=f"{manifest['radar_site']} / {manifest['product']}  •  {manifest['source_name']}"
        length=draw.textbbox((0,0),right,font=small)[2]
        draw.text((1530-length,872),right,font=small,fill='#60747b')
        out.append(page)
    output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    out[0].save(output,save_all=True,append_images=out[1:],duration=frame_ms,
                loop=0,optimize=False,disposal=2)
    return output


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--frame-ms',type=int,default=350)
    args=parser.parse_args(argv)
    data=json.loads(args.manifest.read_text(encoding='utf-8'))
    out=render_gif(data,args.output,root=args.manifest.parent,frame_ms=args.frame_ms)
    print('Wrote',out,'— human editorial approval remains pending')
    return 0


if __name__=='__main__':raise SystemExit(main())
