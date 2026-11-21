"""Source-checked single-post packaging and original vector graphics.

This module deliberately has NO X API integration. Never commit unpublished
package JSON to a public repository: use a local private file instead.
"""
from __future__ import annotations

import argparse
import csv
from datetime import date
from html import escape as xml_escape
import json
from pathlib import Path
from urllib.parse import urlparse

from .editorial import weighted_length
from .branded_graphics import render_visual, validate_visual

MAX_CHARS = 280
VISUAL_TYPES = {
    "bar_comparison", "big_number", "contrast",
    "morning_timeline", "warning_timeline", "conceptual_schematic",
    "track_map", "point_map",
}
BG = "#0c1825"
FG = "#f3f4f1"
MUTED = "#b2c5d1"
CYAN = "#4fd4d4"
ORANGE = "#ffa260"
ICE = "#a9d7ff"
LINE = "#355166"
DARK = "#14273a"


def safe(value: object) -> str:
    return xml_escape(str(value), quote=True)


def svg_text(x: int, y: int, label: object, size: int = 20,
             color: str = FG, weight: str = "normal",
             anchor: str = "start") -> str:
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" '
            f'font-family="Arial,Helvetica,sans-serif">{safe(label)}</text>')


def rect(x: int, y: int, w: float, h: float, color: str) -> str:
    return f'<rect x="{x}" y="{y}" width="{w:.2f}" height="{h:.2f}" fill="{color}"/>'


def line(x1: int, y1: int, x2: int, y2: int,
         color: str = LINE, width: int = 4) -> str:
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{width}"/>')


def circle(x: int, y: int, r: int, color: str) -> str:
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'


def validate_package(item: dict) -> list[str]:
    """Check publication safety properties, not semantic truth of source claims."""
    issues = []
    required = ("event_id","event_date","post_date","caption","source_name",
                "source_url","evidence","alt","type","graphic_spec")
    for key in required:
        if not item.get(key):
            issues.append(f"missing {key}")
    if issues:
        return issues
    try:
        event_day = date.fromisoformat(item["event_date"])
        date.fromisoformat(item["post_date"])
        header = f"#OTDwx: {event_day.strftime('%B')} {event_day.day}, {event_day.year}:"
        if not item["caption"].startswith(header + "\n"):
            issues.append("tweet date header differs from actual historical event date")
    except (ValueError, TypeError):
        issues.append("event_date and post_date must be ISO calendar dates")
    if item["caption"].count("#OTDwx") != 1:
        issues.append("the post should use exactly one #OTDwx tag")
    if not item["caption"].endswith("Source: " + item["source_name"]):
        issues.append("post must end with the verified source label")
    count = weighted_length(item["caption"])
    if count > MAX_CHARS:
        issues.append(f"over 280-character X limit ({count})")
    parsed = urlparse(item["source_url"])
    if parsed.scheme != "https" or not parsed.netloc:
        issues.append("source must have an HTTPS URL")
    if not isinstance(item["evidence"],list) or not item["evidence"]:
        issues.append("source-linked fact-check notes are required")
    else:
        for note in item["evidence"]:
            if not isinstance(note,dict) or not note.get("fact") or not note.get("section"):
                issues.append("each evidence note needs fact and section")
    if item["type"] not in VISUAL_TYPES:
        issues.append("unknown graphic layout")
    if not isinstance(item["graphic_spec"],dict):
        issues.append("graphic_spec must be a dict")
    elif item["type"] in {"track_map", "point_map"} or item["graphic_spec"].get("style") != "legacy":
        issues.extend(validate_visual(item))
    if len(item["alt"].strip()) < 30:
        issues.append("meaningful image alt text is required")
    if item.get("editor_approval") not in (None,"pending","changes_needed","approved"):
        issues.append("unrecognized editor approval state")
    return issues


def render_svg(item: dict) -> str:
    """Render source-linked facts with vector shapes, never fabricated radar or maps."""
    errors = validate_package(item)
    if errors:
        raise ValueError("; ".join(errors))
    if item["type"] in {"track_map", "point_map"} or item["graphic_spec"].get("style") != "legacy":
        return render_visual(item)
    spec = item["graphic_spec"]
    typ = item["type"]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" '
        'width="1200" height="675" role="img">',
        f'<title>{safe(spec.get("title","OTDwx weather history"))}</title>',
        f'<desc>{safe(item["alt"])}</desc>',
        rect(0,0,1200,675,BG),rect(55,59,6,44,CYAN),
        svg_text(82,92,"OTDwx",26,FG,"bold"),
        svg_text(1130,91,item["event_date"].replace("-"," / "),15,MUTED,anchor="end"),
        svg_text(65,156,str(spec.get("title",item["event_id"])).upper(),30,FG,"bold"),
        svg_text(65,198,spec.get("subtitle","WEATHER HISTORY"),17,MUTED)
    ]
    if typ == "bar_comparison":
        rows = spec.get("rows",[])
        if len(rows) != 2 or any(float(r.get("value",0))<0 for r in rows):
            raise ValueError("bar_comparison needs two nonnegative numbers")
        maximum = max(1,1.06*max(float(r["value"]) for r in rows))
        unit = spec.get("unit","")
        for n,row in enumerate(rows):
            y=300+133*n
            value=float(row["value"])
            parts.extend([
                svg_text(80,y+20,row["label"],26,FG,"bold"),
                rect(235,y-20,630,53,LINE),
                rect(235,y-20,630*value/maximum,53,CYAN if n==0 else ICE),
                svg_text(915,y+19,f'{value:g} {unit}',31,FG,"bold")
            ])
        parts.append(svg_text(75,575,spec.get("footnote",""),18,MUTED))
    elif typ == "big_number":
        parts.extend([
            svg_text(76,431,spec.get("hero",""),164,CYAN,"bold"),
            svg_text(377,335,spec.get("hero_label",""),26,FG,"bold"),
        ])
        for i,s in enumerate(spec.get("detail_lines",[])[:3]):
            parts.append(svg_text(379,390+i*51,s,20,ICE if i==0 else MUTED))
    elif typ == "contrast":
        left=spec.get("left",{});right=spec.get("right",{})
        for i,s in enumerate((left,right)):
            x=74+560*i
            parts.extend([
                rect(x,230,510,330,"#19394e" if i==0 else "#283e4a"),
                svg_text(x+35,285,s.get("name",""),22,FG,"bold"),
                svg_text(x+35,421,s.get("value",""),83,ICE if i==0 else ORANGE,"bold"),
                svg_text(x+35,485,s.get("note",""),18,FG)
            ])
        parts.append(svg_text(600,588,spec.get("footnote",""),17,MUTED,anchor="middle"))
    elif typ in ("morning_timeline","warning_timeline"):
        is_warning=typ=="warning_timeline"
        parts.extend([
            svg_text(76,318,spec.get("hero",""),80 if is_warning else 135,CYAN,"bold"),
            svg_text(78,364,spec.get("hero_label",""),21,MUTED),
            line(125,451,1075,451,ICE,6),
            circle(125,451,11,CYAN),circle(1075,451,11,ORANGE),
            svg_text(125,423,spec.get("start",""),22,FG,anchor="middle"),
            svg_text(1075,423,spec.get("end",""),22,FG,anchor="middle")
        ])
        for i,s in enumerate(spec.get("detail_lines",[])[:3]):
            parts.append(svg_text(600,515+i*29,s,18,MUTED,anchor="middle"))
    else:
        parts.extend([
            rect(75,242,1050,320,"#142c3a"),
            rect(75,242,1050,72,"#567b84"),
            svg_text(600,286,spec.get("upper","INVERSION LAYER"),23,FG,"bold",anchor="middle"),
            rect(75,314,1050,236,"#334a57"),
            svg_text(600,376,spec.get("middle",""),20,FG,anchor="middle")
        ])
        for col in range(12):
            for row in range(3):
                parts.append(circle(153+80*col,414+29*row,4,ORANGE))
        parts.extend([
            svg_text(600,537,spec.get("lower",""),19,FG,anchor="middle"),
            svg_text(600,587,spec.get("footnote","CONCEPTUAL SCHEMATIC — NOT OBSERVED DATA"),14,MUTED,anchor="middle")
        ])
    parts.extend([
        line(60,609,1140,609,LINE,2),
        svg_text(64,642,"OTDwx  •  ORIGINAL VECTOR ILLUSTRATION",14,MUTED),
        svg_text(1135,642,"DATA: " + item["source_name"].upper(),14,MUTED,anchor="end"),
        '</svg>'
    ])
    return "\n".join(parts) + "\n"


def generate(packages: list[dict],output: Path,make_png: bool = False) -> list[dict]:
    """Write review-only post text, original SVGs, alt text and a manifest."""
    all_issues = []
    seen=set()
    for item in packages:
        errors=validate_package(item)
        if item.get("event_id") in seen:errors.append("duplicate event_id")
        seen.add(item.get("event_id"))
        if errors:all_issues.append(str(item.get("event_id","UNKNOWN")) + ": " + "; ".join(errors))
    if all_issues:
        raise ValueError("\n".join(all_issues))
    converter=None
    if make_png:
        try: import cairosvg as converter
        except ImportError as exc:
            raise RuntimeError("PNG export needs optional dependency: pip install cairosvg") from exc
    output.mkdir(parents=True,exist_ok=True)
    rows=[]
    for item in packages:
        slug=item["post_date"]+"_"+item["event_id"]
        svg=render_svg(item)
        (output/(slug+".svg")).write_text(svg,encoding="utf-8")
        (output/(slug+".txt")).write_text(item["caption"]+"\n",encoding="utf-8")
        (output/(slug+".alt.txt")).write_text(item["alt"]+"\n",encoding="utf-8")
        if converter is not None:
            converter.svg2png(bytestring=svg.encode("utf-8"),
                              write_to=str(output/(slug+".png")),
                              output_width=1920,output_height=1080)
        rows.append({"planned_date":item["post_date"],"event_id":item["event_id"],
                     "source_url":item["source_url"],
                     "weighted_characters":weighted_length(item["caption"]),
                     "editor_approval":item.get("editor_approval","pending"),
                     "asset":slug+".svg"})
    with (output/"manifest.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys() if rows else
                              ["planned_date","event_id","source_url","weighted_characters","editor_approval","asset"])
        writer.writeheader();writer.writerows(rows)
    return rows


def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,required=True,
                        help="private post-package JSON (outside the public repository)")
    parser.add_argument("--output",type=Path,default=Path("exports/post-studio"))
    parser.add_argument("--png",action="store_true",help="also render PNG with optional CairoSVG")
    args=parser.parse_args(argv)
    payload=json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(payload,list):
        parser.error("input JSON must be an array of post packages")
    rows=generate(payload,args.output,args.png)
    print(f"Created {len(rows)} editor-review-only original graphics and text packages in {args.output}")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
