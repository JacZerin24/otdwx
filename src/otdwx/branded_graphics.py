"""OTDwx visual identity v2: evidence-first, newsroom-like, editable SVG graphics.

No network access and no fabricated satellite/radar/map layers. Public generators
must be given observed values and, for maps, documented coordinates.
"""
from __future__ import annotations

from datetime import date
from html import escape
import math
import re
import textwrap
from typing import Any

W, H = 1600, 900
PAPER = '#f4f1ea'
INK = '#1a2c34'
ACCENT = '#126987'
PALE = '#c5dbe1'
ORANGE = '#b35c39'
MUTED = '#60747b'
RULE = '#c8ccc7'
WHITE = '#ffffff'


def esc(text: Any) -> str:
    return escape(str(text), quote=True)


def text(x: float, y: float, value: Any, size=24, *, color=INK, weight='normal',
         family='sans', anchor='start', letter_spacing=0) -> str:
    font = 'Georgia,Times New Roman,serif' if family == 'serif' else 'Arial,Helvetica,sans-serif'
    return (f'<text x="{x:g}" y="{y:g}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}" font-family="{font}" text-anchor="{anchor}" '
            f'letter-spacing="{letter_spacing}">{esc(value)}</text>')


def line(x1, y1, x2, y2, *, stroke=RULE, width=2, dash='') -> str:
    extra = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{stroke}" stroke-width="{width}"{extra}/>'


def rect(x, y, width, height, *, fill, radius=0) -> str:
    return f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}" rx="{radius:g}" fill="{fill}"/>'


def grouped_lines(s: Any, max_chars: int, limit: int = 3) -> list[str]:
    if not str(s).strip():
        return []
    output=[]
    for para in str(s).split('\n'):
        output.extend(textwrap.wrap(para.strip(), width=max_chars, break_long_words=False,
                                    break_on_hyphens=False) or [''])
    if len(output)>limit:
        raise ValueError('Graphic copy too long; shorten or edit headline/annotation')
    return output


def stack(x, y, content, *, width, size=42, leading=1.15, limit=3,
          family='serif', weight='bold', color=INK) -> list[str]:
    return [text(x, y + i*size*leading, s, size, family=family, weight=weight,
                 color=color) for i,s in enumerate(grouped_lines(content,width,limit))]


def _base(item: dict, spec: dict, eyebrow: str) -> list[str]:
    event_date=date.fromisoformat(item['event_date'])
    display_date=f'{event_date:%B} {event_date.day}, {event_date.year}'
    title=str(spec.get('title','Weather history'))
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}" role="img">',
           f'<title>{esc(title)}</title>', f'<desc>{esc(item["alt"])}</desc>',
           rect(0,0,W,H,fill=PAPER), rect(70,57,9,35,fill=ACCENT),
           text(95,83,'OTDwx',38,weight='bold',family='serif'),
           text(280,82,'WEATHER HISTORY',17,weight='bold',color=MUTED,letter_spacing=3),
           text(1530,82,display_date,22,weight='bold',anchor='end'),
           line(70,116,1530,116,stroke=INK,width=2),
           text(72,158,eyebrow.upper(),18,color=ACCENT,weight='bold',letter_spacing=2),
           line(70,826,1530,826,stroke=INK,width=2),
           text(72,861,'OTDwx  /  WEATHER ARCHIVE',17,weight='bold',color=MUTED,letter_spacing=1),
           text(1530,861,'SOURCE: '+str(item['source_name']).upper(),17,
                color=MUTED,anchor='end')]
    return parts


def _bar_comparison(item: dict, spec: dict, parts: list[str]):
    rows=spec.get('rows',[])
    if len(rows)!=2 or any(not isinstance(r,dict) or not isinstance(r.get('value'),(int,float))
                           or not math.isfinite(r['value']) or r['value']<0 for r in rows):
        raise ValueError('bar_comparison requires two nonnegative finite observed values')
    parts+=stack(72,234,spec.get('title','Observed comparison'),width=47,size=65,limit=2)
    parts+=stack(73,340,spec.get('subtitle',''),width=86,size=25,limit=2,
                 family='sans',weight='normal',color=MUTED)
    parts.append(text(74,448,spec.get('comparison_label','OBSERVED VALUES'),18,
                      color=MUTED,weight='bold',letter_spacing=2))
    high=max(r['value'] for r in rows) or 1
    unit=str(spec.get('unit',''))
    for i,r in enumerate(rows):
        y=511+i*122
        parts.extend([text(74,y+24,r['label'],32,weight='bold'),
                      line(312,y+13,1150,y+13,stroke=RULE,width=19),
                      line(312,y+13,312+838*(r['value']/high),y+13,
                           stroke=ACCENT if i==0 else PALE,width=19),
                      text(1180,y+25,f'{r["value"]:g} {unit}'.strip(),44,
                           family='serif',weight='bold')])
    note=spec.get('footnote','')
    parts += [line(74,724,1530,724),*stack(75,763,note,width=120,size=24,
                                          limit=2,weight='normal',family='sans')]


def _big_number(item: dict, spec: dict, parts: list[str]):
    parts+=stack(72,238,spec.get('title',''),width=45,size=65,limit=2)
    parts.append(text(74,550,spec.get('hero',''),205,family='serif',weight='bold',color=ACCENT))
    parts+=stack(755,474,spec.get('hero_label',''),width=28,size=43,limit=2)
    for i,d in enumerate(spec.get('detail_lines',[])[:3]):
        parts.append(text(758,565+i*48,d,26,color=MUTED))


def _contrast(item: dict, spec: dict, parts: list[str]):
    parts+=stack(72,238,spec.get('title',''),width=46,size=61,limit=2)
    for i,key in enumerate(('left','right')):
        x=72+i*750; r=spec.get(key,{})
        parts.extend([line(x,376,x+674,376,stroke=ACCENT if i==0 else ORANGE,width=5),
                     text(x,424,r.get('name',''),27,weight='bold'),
                     text(x,575,r.get('value',''),105,family='serif',weight='bold'),
                     *stack(x,631,r.get('note',''),width=40,size=24,limit=2)])
    parts+=stack(72,761,spec.get('footnote',''),width=110,size=20,
                 limit=2,family='sans',weight='normal',color=MUTED)


def _timeline(item: dict, spec: dict, parts: list[str]):
    parts+=stack(72,240,spec.get('title',''),width=50,size=58,limit=2)
    parts.append(text(74,438,spec.get('hero',''),100,family='serif',weight='bold',color=ACCENT))
    parts+=stack(625,410,spec.get('hero_label',''),width=43,size=28,limit=2)
    parts+= [line(140,569,1430,569,stroke=PALE,width=7),
             f'<circle cx="140" cy="569" r="13" fill="{ACCENT}"/>',
             f'<circle cx="1430" cy="569" r="13" fill="{ORANGE}"/>',
             text(140,529,spec.get('start',''),24,weight='bold'),
             text(1430,529,spec.get('end',''),24,weight='bold',anchor='end')]
    for i,s in enumerate(spec.get('detail_lines',[])[:3]):
        parts.append(text(74,650+i*43,s,22,color=MUTED))


def _schematic(item: dict, spec: dict, parts: list[str]):
    parts+=stack(72,238,spec.get('title',''),width=47,size=60,limit=2)
    parts += [rect(74,365,1452,125,fill=PALE),
              text(800,429,spec.get('upper','INVERSION'),32,weight='bold',anchor='middle'),
              line(74,490,1526,490,stroke=ACCENT,width=5),
              rect(74,500,1452,192,fill='#e4e1da'),
              text(800,579,spec.get('middle','TRAPPED POLLUTANTS'),34,
                   weight='bold',anchor='middle'),
              text(800,638,spec.get('lower',''),22,anchor='middle'),
              text(78,752,spec.get('footnote','CONCEPTUAL DIAGRAM, NOT AN OBSERVATION'),
                   20,color=MUTED)]


def _xy(lon: float,lat: float,bounds: list[float]) -> tuple[float,float]:
    west,south,east,north=bounds
    # Simple longitude/latitude viewport, not a measured-distance projection.
    return 170+1260*(lon-west)/(east-west), 720-450*(lat-south)/(north-south)


def _coords(point: Any) -> tuple[float,float]:
    if not isinstance(point,(list,tuple)) or len(point)!=2:
        raise ValueError('Map coordinates must be [longitude, latitude]')
    lon,lat=map(float,point)
    if not all(math.isfinite(v) for v in (lon,lat)) or not (-180<=lon<=180 and -90<=lat<=90):
        raise ValueError('Map coordinates outside geographic limits')
    return lon,lat


def _map(item: dict, spec: dict, parts: list[str], *, typ: str):
    bounds=spec.get('bounds')
    if not isinstance(bounds,list) or len(bounds)!=4:
        raise ValueError('Maps require documented bounds [W,S,E,N]')
    west,south=_coords(bounds[:2]);east,north=_coords(bounds[2:])
    if east<=west or north<=south or east-west>100 or north-south>70:
        raise ValueError('Map bounds invalid or too broad for regional graphic')
    parts+=stack(72,231,spec.get('title',''),width=55,size=53,limit=2)
    parts.append(rect(125,254,1346,510,fill='#e5edf0'))
    for i in range(1,5):
        x=125+i*1346/5;y=254+i*510/5
        parts.extend([line(x,254,x,764,stroke='#cad9dd',width=2),
                      line(125,y,1471,y,stroke='#cad9dd',width=2)])
    def place(pt):
        lon,lat=_coords(pt)
        if not (west<=lon<=east and south<=lat<=north):
            raise ValueError('Map feature coordinate outside bounds')
        # same projection everywhere inside view
        return 125+1346*(lon-west)/(east-west), 764-510*(lat-south)/(north-south)
    for feature in spec.get('geography',[]):
        if feature.get('type') not in ('LineString','Polygon'):
            raise ValueError('Geography overlays accept only source-backed LineString/Polygon')
        seq=feature['coordinates'] if feature['type']=='LineString' else feature['coordinates'][0]
        if len(seq)<2 or len(seq)>10000:
            raise ValueError('Geography feature must contain 2..10000 points')
        points=' '.join(f'{x:.1f},{y:.1f}' for x,y in map(place,seq))
        parts.append(f'<polyline points="{points}" fill="none" stroke="#95aeb8" stroke-width="2"/>')
    if typ=='track_map':
        pts=spec.get('track',[])
        if len(pts)<2 or len(pts)>1000:
            raise ValueError('track_map requires two or more source-backed points')
        quality=spec.get('track_quality')
        if quality not in ('surveyed','best_track','approximate'):
            raise ValueError('track_map requires a surveyed, best_track, or approximate quality label')
        points=[place(p) for p in pts]
        coords=' '.join(f'{x:.1f},{y:.1f}' for x,y in points)
        parts.append(f'<polyline points="{coords}" fill="none" stroke="{ORANGE}" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>')
        for x,y in [points[0],points[-1]]:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" stroke="{WHITE}" stroke-width="3" fill="{ACCENT}"/>')
        parts.append(text(145,795,{'surveyed':'SURVEYED TRACK','best_track':'BEST TRACK','approximate':'APPROXIMATE PATH'}[quality],19,weight='bold',color=ORANGE))
    else:
        pts=spec.get('points',[])
        if not pts:
            raise ValueError('point_map requires at least one source-backed observation')
        if len(pts)>40:
            raise ValueError('point_map max 40 labeled observations')
        for p in pts:
            x,y=place(p['coordinates']); label=str(p['label'])
            if len(label)>30:raise ValueError('Point label too long')
            parts.extend([f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{ACCENT}" stroke="{WHITE}" stroke-width="3"/>',
                          text(x+15,y-12,label,20,weight='bold')])
    parts.append(text(1440,797,spec.get('map_note','LON/LAT GRID • SCHEMATIC BASE'),19,
                      anchor='end',color=MUTED))


def validate_visual(item: dict) -> list[str]:
    typ=item.get('type'); spec=item.get('graphic_spec',{})
    if typ not in {'bar_comparison','big_number','contrast','morning_timeline',
                   'warning_timeline','conceptual_schematic','track_map','point_map'}:
        return ['unsupported branded graphic type']
    if not isinstance(spec,dict):return ['graphic_spec must be an object']
    if typ in ('track_map','point_map'):
        if not spec.get('geography_source_url') and spec.get('geography'):
            return ['map boundary source URL required for supplied geography']
        if not spec.get('data_source_url'):
            return ['map observed track/point data source URL required']
    try:
        render_visual(item,validate=False)
    except (ValueError,KeyError,TypeError,OverflowError) as exc:
        return [str(exc)]
    return []


def render_visual(item: dict, *, validate=True) -> str:
    typ=item['type'];spec=item['graphic_spec']
    if validate:
        issues=validate_visual(item)
        if issues:raise ValueError('; '.join(issues))
    parts=_base(item,spec,{'bar_comparison':'THE RECORD','big_number':'THE NUMBER',
                'contrast':'SIDE BY SIDE','morning_timeline':'CHRONOLOGY',
                'warning_timeline':'WARNING TIMELINE','conceptual_schematic':'THE SETUP',
                'track_map':'THE PATH','point_map':'THE OBSERVATIONS'}[typ])
    if typ=='bar_comparison':_bar_comparison(item,spec,parts)
    elif typ=='big_number':_big_number(item,spec,parts)
    elif typ=='contrast':_contrast(item,spec,parts)
    elif typ in ('morning_timeline','warning_timeline'):_timeline(item,spec,parts)
    elif typ=='conceptual_schematic':_schematic(item,spec,parts)
    else:_map(item,spec,parts,typ=typ)
    parts.append('</svg>')
    return '\n'.join(parts)+'\n'
