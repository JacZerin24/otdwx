"""Evidence-led OTDwx visuals: real archive imagery and real geographic vectors.

This renderer never fetches, paints, or invents radar returns, tornado tracks,
storm footprints, geographic boundaries, or photographs. It consumes private,
individually reviewed source files and records their origins in the SVG.
"""
from __future__ import annotations

import base64
from datetime import date
from hashlib import sha256
from html import escape
import json
import math
from pathlib import Path
import re
from urllib.parse import urlparse


CANVAS_W, CANVAS_H = 1600, 900
TYPES = {"archive_panel", "geo_track"}
ARCHIVE_KINDS = {
    "survey_map": "NWS DAMAGE SURVEY", "radar_reflectivity": "RADAR / REFLECTIVITY",
    "radar_velocity": "RADAR / VELOCITY", "snowfall_analysis": "OBSERVED SNOWFALL",
    "satellite": "SATELLITE ARCHIVE", "flood_extent": "FLOOD EXTENT / GIS",
    "documentary_photo": "DOCUMENTARY PHOTOGRAPH",
}
PALETTES = {
    "winter": ("#071f31","#d9f5fe","#60cbe7"),
    "tornado": ("#201c1a","#fff0e1","#e99653"),
    "severe_storm": ("#101b2c","#f2f6fa","#fdb96e"),
    "tropical": ("#062d35","#e8fafa","#55c5c3"),
    "flood": ("#102923","#e8f6ef","#78ccac"),
    "wildfire_weather": ("#281f1a","#fff4e5","#eea85d"),
    "unusual": ("#202136","#f2eaff","#c3a5fa"),
}


def _esc(value):
    return escape(str(value), quote=True)


def _text(x, y, value, size=26, color="#ffffff", weight=400, serif=False):
    font = "Georgia,Times New Roman,serif" if serif else "Arial,Helvetica,sans-serif"
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{font}" '
            f'font-size="{size}" font-weight="{weight}">{_esc(value)}</text>')


def _wrap(value, max_chars, max_lines):
    lines, current = [], ""
    for word in str(value).split():
        next_line = (current + " " + word).strip()
        if len(next_line) > max_chars and current:
            lines.append(current)
            current = word
        else:
            current = next_line
    if current: lines.append(current)
    if len(lines) > max_lines:
        raise ValueError("Evidence panel text too long; shorten title/deck")
    return lines


def _https(value):
    return isinstance(value,str) and urlparse(value).scheme == "https" and bool(urlparse(value).netloc)


def _private_path(root, filename, suffixes):
    if root is None:
        raise ValueError("Evidence visual needs --asset-root")
    if not isinstance(filename,str):
        raise ValueError("Source asset filename required")
    relative = Path(filename)
    if (relative.is_absolute() or
        any(p in ("..", ".") for p in relative.parts) or
        "\\" in filename or relative.suffix.lower() not in suffixes):
        raise ValueError("Unsafe evidence asset path/type")
    root = Path(root).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("Evidence asset escapes private source folder")
    if not path.is_file() or path.stat().st_size > 20_000_000:
        raise ValueError("Evidence source absent or above 20MB")
    return path


def validate_evidence(item):
    errors=[]
    spec=item.get("graphic_spec")
    if not isinstance(spec,dict):
        return ["evidence graphic_spec must be an object"]
    typ=item.get("type")
    if typ not in TYPES:
        return ["unsupported evidence visual type"]
    if not str(spec.get("title", "")).strip():
        errors.append("evidence graphic title required")
    if not _https(spec.get("data_source_url")):
        errors.append("evidence original data_source_url must be HTTPS")
    if not _https(spec.get("rights_basis_url")):
        errors.append("source-specific rights_basis_url must be HTTPS")
    if spec.get("rights_status") not in (
        "public_domain", "government_reusable", "cc_by",
        "licensed", "permission_granted", "original_work"
    ):
        errors.append("source rights must be individually cleared")
    if not spec.get("rights_reviewed_by") or not spec.get("rights_reviewed_on"):
        errors.append("source rights reviewer and date required")
    try: date.fromisoformat(spec["rights_reviewed_on"])
    except (KeyError,TypeError,ValueError):errors.append("rights_reviewed_on must be ISO date")
    if spec.get("credit_checked") is not True:
        errors.append("explicit credit_checked required")
    if spec.get("rights_status")=="cc_by" and not _https(spec.get("license_url")):
        errors.append("CC BY requires individual license URL")
    if spec.get("rights_status") in ("licensed","permission_granted") and not spec.get("license_scope"):
        errors.append("license_scope required")
    if typ=="archive_panel":
        if spec.get("asset_kind") not in ARCHIVE_KINDS:
            errors.append("archive_panel needs defined actual evidence kind")
        if not spec.get("asset_file"):
            errors.append("archive_panel needs local evidence asset_file")
        if spec.get("asset_kind","").startswith("radar"):
            if not spec.get("radar_site") or not spec.get("radar_product"):
                errors.append("radar evidence needs radar_site and radar_product")
            if not spec.get("observed_at_utc"):
                errors.append("radar evidence needs observed_at_utc")
        if not spec.get("observed_at_utc") and not spec.get("valid_period"):
            errors.append("actual observation timestamp or period required")
        if not spec.get("source_creator") or not spec.get("source_credit"):
            errors.append("specific asset source creator and credit required")
    if typ=="geo_track":
        if not spec.get("geometry_file"):
            errors.append("track source GeoJSON file required")
        if spec.get("track_quality") not in (
            "surveyed", "best_track", "endpoint_summary", "approximate"
        ):
            errors.append("explicit track_quality required")
        if not spec.get("geometry_role"):
            errors.append("geometry_role required (track, best-track, etc)")
    for field,max_chars,max_lines in (("title",33,3),("deck",46,4)):
        try:_wrap(spec.get(field,""),max_chars,max_lines)
        except ValueError as e:errors.append(str(e))
    return errors


def _geometry_points(data):
    if data.get("type") == "FeatureCollection":
        fs=data.get("features",[])
    elif data.get("type") == "Feature":
        fs=[data]
    else:
        raise ValueError("GeoJSON Feature or FeatureCollection required")
    if not 1 <= len(fs) <= 100:
        raise ValueError("Geometry must have 1–100 features")
    tracks=[]
    for f in fs:
        g=f.get("geometry") or {}
        typ=g.get("type")
        co=g.get("coordinates",[])
        lines=([co] if typ=="LineString" else co) if typ in ("LineString","MultiLineString") else []
        if not lines: raise ValueError("All source track geometries must be lines")
        for seq in lines:
            if not 2 <= len(seq) <= 3000:
                raise ValueError("Track feature needs 2–3000 real coordinates")
            pts=[]
            for point in seq:
                if len(point)<2:raise ValueError("Malformed lon/lat point")
                lon,lat=float(point[0]),float(point[1])
                if not math.isfinite(lon) or not math.isfinite(lat) or abs(lon)>180 or abs(lat)>90:
                    raise ValueError("Invalid lon/lat coordinate")
                pts.append((lon,lat))
            tracks.append(pts)
    return tracks


def _header(item, palette, evidence_label):
    bg,white,accent=palette
    event_day=date.fromisoformat(item["event_date"]).strftime("%b %-d, %Y")
    parts=[
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 1600 900" role="img">',
        f'<title>{_esc(item["graphic_spec"]["title"])}</title>',
        f'<desc>{_esc(item["alt"])}</desc>',
        f'<rect width="1600" height="900" fill="{bg}"/>',
        f'<rect x="52" y="39" width="10" height="38" fill="{accent}"/>',
        _text(80,70,"OTDwx",37,white,700,True),
        _text(320,66,"THE WEATHER RECORD  /  "+evidence_label,17,accent,700),
        _text(1300,68,event_day,23,white),
        f'<line x1="52" y1="98" x2="1548" y2="98" stroke="{accent}" stroke-opacity=".4" />']
    return parts


def _credit(parts, spec, palette):
    bg,white,accent=palette
    parts += [
        '<line x1="52" y1="836" x2="1548" y2="836" stroke="#ffffff" stroke-opacity=".22"/>',
        _text(54,872,"ORIGINAL ARCHIVE • NOT SIMULATED",17,accent,700),
        _text(602,871,"SOURCE: "+str(spec.get("source_credit",spec.get("data_publisher","ORIGINAL DATA ARCHIVE")))[:70],
              17,white)
    ]


def render_archive(item, asset_root):
    errors=validate_evidence(item)
    if errors:raise ValueError("; ".join(errors))
    spec=item["graphic_spec"]
    asset=_private_path(asset_root,spec["asset_file"],{".png",".jpeg",".jpg"})
    data=asset.read_bytes()
    if asset.suffix.lower()==".png":
        if not data.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("Asset is not a genuine PNG")
        mime="image/png"
    else:
        if not data.startswith(b"\xff\xd8\xff"):
            raise ValueError("Asset is not a genuine JPEG")
        mime="image/jpeg"
    checksum=sha256(data).hexdigest()
    if spec.get("sha256") and spec["sha256"].lower()!=checksum:
        raise ValueError("Source checksum mismatch; possible wrong asset")
    category=item.get("weather_category","unusual")
    palette=PALETTES.get(category,PALETTES["unusual"])
    bg,white,accent=palette
    parts=_header(item,palette,ARCHIVE_KINDS[spec["asset_kind"]])
    parts += [
        '<rect x="52" y="128" width="1020" height="667" fill="#ffffff"/>',
        f'<image x="59" y="135" width="1006" height="653" href="data:{mime};base64,{base64.b64encode(data).decode("ascii")}" preserveAspectRatio="xMidYMid meet"/>',
        '<line x1="1110" y1="148" x2="1110" y2="787" stroke="'+accent+'" stroke-width="5" opacity=".75"/>'
    ]
    for i,line in enumerate(_wrap(spec["title"],21,3)):
        parts.append(_text(1140,228+i*64,line,42,white,700,True))
    start=488
    if spec.get("headline_stat"):
        parts.append(_text(1138,start,spec["headline_stat"],69,accent,700,True))
        start+=57
    for i,line in enumerate(_wrap(spec.get("deck",""),25,5)):
        parts.append(_text(1140,start+35*i,line,22,white))
    time_note=spec.get("observed_at_utc") or spec.get("valid_period")
    parts.append(_text(75,817,str(time_note)[:68],18,accent,700))
    _credit(parts,spec,palette)
    parts.append("</svg>")
    return "\n".join(parts)+"\n"


def render_geo_track(item, asset_root):
    errors=validate_evidence(item)
    if errors:raise ValueError("; ".join(errors))
    spec=item["graphic_spec"]
    fp=_private_path(asset_root,spec["geometry_file"],{".geojson",".json"})
    data=json.loads(fp.read_text(encoding="utf-8"))
    tracks=_geometry_points(data)
    # Approximate/equirectangular lon correction at reference latitude.
    # No claims about measured track widths, distances or wind swaths.
    pts=[p for t in tracks for p in t]
    west=min(p[0] for p in pts);east=max(p[0] for p in pts)
    south=min(p[1] for p in pts);north=max(p[1] for p in pts)
    lat0=(south+north)/2
    correction=max(.05,math.cos(math.radians(lat0)))
    dx=max(0.03,(east-west)*correction)
    dy=max(0.03,north-south)
    ratio=max(dx/900,dy/550)
    xmid=(east+west)/2;ymid=(south+north)/2
    def xy(p):
        return 560+(p[0]-xmid)*correction/ratio,464-(p[1]-ymid)/ratio
    palette=PALETTES.get(item.get("weather_category","tornado"),PALETTES["tornado"])
    bg,white,accent=palette
    parts=_header(item,palette,"GEOGRAPHIC TRACK / OBSERVED")
    parts += ['<rect x="52" y="128" width="1035" height="675" fill="#f1f3f1"/>']
    # Verified only: do not invent a coastline, county outline, street or map tile.
    for t in tracks:
        coords=" ".join(f"{xy(p)[0]:.1f},{xy(p)[1]:.1f}" for p in t)
        dash='stroke-dasharray="13 13"' if spec["track_quality"] in ("approximate","endpoint_summary") else ""
        parts.append(f'<polyline points="{coords}" stroke="#ad371f" stroke-width="12" '
                     f'fill="none" stroke-linecap="round" stroke-linejoin="round" {dash}/>')
        for idx,p in enumerate((t[0],t[-1])):
            x,y=xy(p)
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{accent}" stroke="#ffffff" stroke-width="4"/>')
    parts.append(_text(77,164,spec["track_quality"].replace("_"," ").upper()+" / SOURCE GEOMETRY",17,"#494f4e",700))
    parts.append(_text(80,776,"NO SYNTHETIC BASEMAP / NO INTERPOLATED WIDTH",15,"#556260"))
    parts.append('<line x1="1124" y1="160" x2="1124" y2="767" stroke="'+accent+'" stroke-width="5"/>')
    for i,line in enumerate(_wrap(spec["title"],21,3)):
        parts.append(_text(1160,232+i*64,line,42,white,700,True))
    if spec.get("headline_stat"):
        parts.append(_text(1160,494,spec["headline_stat"],68,accent,700,True))
    for i,line in enumerate(_wrap(spec.get("deck",""),25,4)):
        parts.append(_text(1160,559+i*36,line,22,white))
    _credit(parts,spec,palette)
    parts.append("</svg>")
    return "\n".join(parts)+"\n"


def render_evidence(item, asset_root):
    typ=item.get("type")
    if typ=="archive_panel":return render_archive(item,asset_root)
    if typ=="geo_track":return render_geo_track(item,asset_root)
    raise ValueError("unsupported authentic evidence graphic")
