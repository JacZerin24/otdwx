"""Private, rights-gated OTDwx documentary media packaging.

No archive downloading, rights inference, image synthesis, or automatic approval.
Graphic-only packages remain backward-compatible with the original generator.
"""
from __future__ import annotations

import base64
from datetime import date
from html import escape
import json
from pathlib import Path
import shutil
from urllib.parse import urlparse

from .themed_graphics import _theme

MEDIA_MODES = frozenset({
    "graphic_only", "graphic_plus_photo", "graphic_plus_map",
    "carousel", "animated_package",
})
RIGHTS_STATUSES = frozenset({
    "public_domain", "government_reusable", "cc_by",
    "licensed", "permission_granted", "original_work",
})
ASSET_KINDS = frozenset({
    "photo", "map", "radar_loop", "satellite_loop", "radar_still",
    "satellite_still", "newspaper", "other",
})
PHOTO_RELATIONS = frozenset({"during_event", "aftermath", "related_context"})
APPROVAL_STATES = frozenset({"pending", "approved", "changes_needed", "rejected"})
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | {".gif", ".webp", ".mp4"}


def _https(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def _safe_file(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    path = Path(value)
    return (not path.is_absolute() and not any(p in (".", "..") for p in path.parts)
            and "\\" not in value and path.suffix.lower() in ALLOWED_EXTENSIONS)


def _check_asset(asset: object, *, position: str, composite: bool) -> list[str]:
    problems = []
    if not isinstance(asset, dict):
        return [f"{position} must be an object"]
    kind = asset.get("kind")
    if kind not in ASSET_KINDS:
        problems.append(f"{position}: unsupported kind")
    if not _safe_file(asset.get("file")):
        problems.append(f"{position}: local relative image/media file required")
    suffix = Path(str(asset.get("file", ""))).suffix.lower()
    if kind == "photo" and suffix not in IMAGE_EXTENSIONS:
        problems.append(f"{position}: photo must be JPEG or PNG")
    if kind in ("radar_loop", "satellite_loop") and suffix not in (".gif", ".mp4"):
        problems.append(f"{position}: animated loop must be GIF or MP4")
    if kind in ("map", "radar_still", "satellite_still", "newspaper") and suffix not in IMAGE_EXTENSIONS | {".webp"}:
        problems.append(f"{position}: supporting still asset must be image")
    for field in ("source_url", "rights_basis_url"):
        if not _https(asset.get(field)):
            problems.append(f"{position}: {field} must be an HTTPS source")
    for field in ("credit", "caption", "creator", "rights_reviewed_by"):
        if not isinstance(asset.get(field), str) or not asset[field].strip():
            problems.append(f"{position}: {field} required")
    if not isinstance(asset.get("alt_text"), str) or len(asset["alt_text"].strip()) < 30:
        problems.append(f"{position}: descriptive alt_text (30+ chars) required")
    if kind == "photo" and asset.get("event_relation") not in PHOTO_RELATIONS:
        problems.append(f"{position}: photo event_relation required")
    if kind == "photo" and asset.get("event_relation") == "related_context":
        if not asset.get("context_disclosure"):
            problems.append(f"{position}: context image must disclose it is not event footage")
    status = asset.get("rights_status")
    if status not in RIGHTS_STATUSES:
        problems.append(f"{position}: rights_status not cleared")
    try:
        date.fromisoformat(asset["rights_reviewed_on"])
    except (KeyError, TypeError, ValueError):
        problems.append(f"{position}: rights_reviewed_on must be ISO YYYY-MM-DD")
    if asset.get("commercial_use_allowed") is not True:
        problems.append(f"{position}: commercial_use_allowed must be explicitly true")
    if asset.get("credit_placement_confirmed") is not True:
        problems.append(f"{position}: required attribution placement must be confirmed")
    if not isinstance(asset.get("modifications_allowed"), bool):
        problems.append(f"{position}: modifications_allowed must be explicitly set")
    if composite and asset.get("modifications_allowed") is not True:
        problems.append(f"{position}: modified photo layout not licensed")
    if status == "cc_by":
        if not _https(asset.get("license_url")):
            problems.append(f"{position}: CC BY requires actual license URL")
        if asset.get("changes_disclosed") is not True and composite:
            problems.append(f"{position}: CC BY composite must disclose changes")
    if status in ("licensed", "permission_granted") and not asset.get("license_scope"):
        problems.append(f"{position}: record explicit license/permission scope")
    return problems


def validate_media(item: dict) -> list[str]:
    """Enforce media provenance, file references and rights, never self-approve."""
    mode = item.get("media_mode", "graphic_only")
    if mode not in MEDIA_MODES:
        return ["unsupported media_mode"]
    if item.get("media_editor_approval", "pending") not in APPROVAL_STATES:
        return ["invalid media_editor_approval"]
    photo = item.get("photo")
    supporting = item.get("supporting_media", [])
    layout = item.get("photo_layout", "none")
    if layout not in ("none", "editorial_split"):
        return ["invalid photo_layout"]
    if not isinstance(supporting, list):
        return ["supporting_media must be a list"]
    if len(supporting) > 3:
        return ["maximum of three supporting assets per post"]
    if mode == "graphic_only":
        if photo or supporting or layout != "none":
            return ["graphic_only cannot include additional media"]
        return []
    errors = []
    if mode == "graphic_plus_photo" and not photo:
        errors.append("graphic_plus_photo requires a photo")
    if mode == "graphic_plus_map" and not any(
        isinstance(a, dict) and a.get("kind") == "map" for a in supporting
    ):
        errors.append("graphic_plus_map requires a source-backed map")
    if mode == "carousel" and not (photo or supporting):
        errors.append("carousel requires one or more support assets")
    if mode == "animated_package":
        loops = [a for a in supporting if isinstance(a, dict)
                 and a.get("kind") in ("radar_loop", "satellite_loop")]
        if len(loops) != 1 or len(supporting) != 1 or photo:
            errors.append("animated_package needs one loop only; no simultaneous photo")
        if layout != "none":
            errors.append("animated_package cannot use a photo layout")
    if layout != "none" and not photo:
        errors.append("photo_layout requires a cleared photo")
    if photo:
        if not isinstance(photo, dict) or photo.get("kind") != "photo":
            errors.append("photo.kind must be photo")
        errors += _check_asset(photo, position="photo", composite=layout != "none")
    for index, asset in enumerate(supporting):
        errors += _check_asset(asset, position=f"supporting_media[{index}]", composite=False)
    if photo and mode in ("graphic_plus_map", "animated_package"):
        errors.append(f"{mode} must not include photo (use carousel instead)")
    if mode == "carousel" and 1 + int(bool(photo)) + len(supporting) > 4:
        errors.append("standard carousel can have at most four still images")
    if mode == "carousel":
        if any(isinstance(a, dict) and a.get("kind") in ("radar_loop", "satellite_loop")
               for a in supporting):
            errors.append("animated loops must be a separate X post or reply")
        if any(isinstance(a, dict) and Path(str(a.get("file", ""))).suffix.lower()
               not in IMAGE_EXTENSIONS | {".webp"} for a in supporting):
            errors.append("carousel supports still images only")
    return errors


def _private_file(asset: dict, root: Path) -> Path:
    """Resolve only real private files under the explicit asset root; no URLs."""
    if not _safe_file(asset["file"]):
        raise ValueError("unsafe asset path")
    root = root.resolve()
    source = (root / asset["file"]).resolve()
    if not source.is_relative_to(root):
        raise ValueError("asset path escapes private root")
    if not source.is_file():
        raise FileNotFoundError(source)
    if source.stat().st_size > 20 * 1024 * 1024:
        raise ValueError("source asset exceeds 20 MB packaging limit")
    return source


def _svg_text(x, y, label, size, color, *, bold=False, serif=False) -> str:
    family = "Georgia,serif" if serif else "Arial,Helvetica,sans-serif"
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-weight="{"bold" if bold else "normal"}" '
            f'font-family="{family}">{escape(str(label))}</text>')


def _wrap_words(value: str, length: int, max_lines: int) -> list[str]:
    words = value.strip().split()
    lines = []
    active = ""
    for word in words:
        candidate = (active + " " + word).strip()
        if len(candidate) > length and active:
            lines.append(active)
            active = word
        else:
            active = candidate
    if active:
        lines.append(active)
    if len(lines) > max_lines:
        raise ValueError("Photo-card text too long for designed layout")
    return lines


def render_photo_card(item: dict, photo_path: Path) -> str:
    """Editable branded 16:9 SVG; embeds only locally supplied cleared pixels.

    The photo is shown whole using xMidYMid meet (no crop). Captions call out
    contextual photos rather than pretending they show the historical event.
    """
    errors = validate_media(item)
    if errors:
        raise ValueError("; ".join(errors))
    photo = item.get("photo")
    if not photo or item.get("photo_layout") != "editorial_split":
        raise ValueError("editorial_split cleared photo required")
    suffix = photo_path.suffix.lower()
    if suffix not in IMAGE_EXTENSIONS:
        raise ValueError("Only JPEG/PNG documentary photos can be composited")
    mime = "image/png" if suffix == ".png" else "image/jpeg"
    data = base64.b64encode(photo_path.read_bytes()).decode("ascii")
    theme = _theme(item)
    title = str(item["graphic_spec"].get("photo_title",
                item["graphic_spec"].get("title", "From the archive")))
    dek = str(item["graphic_spec"].get("photo_deck", photo["caption"]))
    title_lines = _wrap_words(title, 21, 3)
    dek_lines = _wrap_words(dek, 33, 4)
    header = date.fromisoformat(item["event_date"]).strftime("%B %d, %Y").replace(" 0", " ")
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900" role="img">',
         f'<title>{escape(title)}</title><desc>{escape(photo["alt_text"])}</desc>',
         f'<rect width="1600" height="900" fill="{theme.paper}"/>',
         f'<rect x="62" y="60" width="10" height="35" fill="{theme.accent}"/>',
         _svg_text(95, 88, "OTDwx", 37, theme.ink, bold=True, serif=True),
         _svg_text(1220, 87, header, 23, theme.muted),
         f'<line x1="62" y1="114" x2="1540" y2="114" stroke="{theme.rule}" stroke-width="2"/>',
         f'<rect x="62" y="151" width="920" height="624" fill="{theme.faint}"/>',
         f'<image x="62" y="151" width="920" height="624" preserveAspectRatio="xMidYMid meet" href="data:{mime};base64,{data}"/>',
         f'<line x1="1015" y1="182" x2="1015" y2="764" stroke="{theme.accent}" stroke-width="6"/>',
         _svg_text(1050, 210, "ARCHIVAL PHOTOGRAPH", 19, theme.accent, bold=True)]
    for i, row in enumerate(title_lines):
        p.append(_svg_text(1050, 298 + 68 * i, row, 40, theme.ink, bold=True, serif=True))
    for i, row in enumerate(dek_lines):
        p.append(_svg_text(1050, 535 + 38 * i, row, 24, theme.ink))
    rel = photo.get("event_relation")
    if rel == "related_context":
        p.append(_svg_text(1050, 717, "CONTEXT PHOTO — NOT EVENT FOOTAGE", 18, theme.accent, bold=True))
    else:
        p.append(_svg_text(1050, 717, "EVENT" if rel == "during_event" else "AFTERMATH", 18, theme.accent, bold=True))
    p += [f'<line x1="62" y1="804" x2="1540" y2="804" stroke="{theme.rule}" stroke-width="2"/>',
          _svg_text(63, 839, "PHOTO: " + photo["credit"][:90], 19, theme.ink),
          _svg_text(63, 871, "WEATHER DATA: " + item["source_name"], 17, theme.muted),
          "</svg>"]
    return "\n".join(p) + "\n"


def export_media(item: dict, output: Path, asset_root: Path | None, slug: str,
                 *, png_converter=None) -> dict:
    """Stage exact private media bytes, one credit ledger, optional photo SVG."""
    errors = validate_media(item)
    if errors:
        raise ValueError("; ".join(errors))
    mode = item.get("media_mode", "graphic_only")
    if mode == "graphic_only":
        return {"mode": mode, "assets": [], "approval": "pending"}
    if asset_root is None:
        raise ValueError("private --asset-root required for media packages")
    output.mkdir(parents=True, exist_ok=True)
    assets = ([item["photo"]] if item.get("photo") else []) + item.get("supporting_media", [])
    prepared = []
    for index, asset in enumerate(assets):
        src = _private_file(asset, asset_root)
        filename = f"{slug}.asset-{index+1}{src.suffix.lower()}"
        shutil.copy2(src, output / filename)
        prepared.append({"file": filename, "kind": asset["kind"], "credit": asset["credit"],
                         "creator": asset["creator"], "rights_status": asset["rights_status"],
                         "rights_basis_url": asset["rights_basis_url"],
                         "license_url": asset.get("license_url", ""),
                         "license_scope": asset.get("license_scope", ""),
                         "source_url": asset["source_url"], "alt_text": asset["alt_text"],
                         "caption": asset["caption"], "event_relation": asset.get("event_relation"),
                         "context_disclosure": asset.get("context_disclosure", ""),
                         "changes_disclosed": asset.get("changes_disclosed", False),
                         "rights_reviewed_by": asset["rights_reviewed_by"],
                         "rights_reviewed_on": asset["rights_reviewed_on"]})
    if item.get("photo_layout") == "editorial_split":
        photo_path = _private_file(item["photo"], asset_root)
        svg = render_photo_card(item, photo_path)
        filename = slug + ".documentary.svg"
        (output / filename).write_text(svg, encoding="utf-8")
        prepared.append({"file": filename, "kind": "photo_composite",
                         "credit": item["photo"]["credit"],
                         "alt_text": item["photo"]["alt_text"]})
        if png_converter is not None:
            png_name = slug + ".documentary.png"
            png_converter.svg2png(bytestring=svg.encode("utf-8"),
                                  write_to=str(output / png_name),
                                  output_width=1920, output_height=1080)
            prepared.append({"file": png_name, "kind": "photo_composite_png",
                             "credit": item["photo"]["credit"],
                             "alt_text": item["photo"]["alt_text"]})
    package = {"mode": mode, "assets": prepared, "approval": "pending",
               "human_editor_approval": item.get("media_editor_approval", "pending"),
               "publishing_enabled": False,
               "note": "Source licensing and image use must be rechecked by a human in X before posting."}
    (output / (slug + ".media.json")).write_text(json.dumps(package, indent=2)+"\n",
                                                    encoding="utf-8")
    credit_lines = []
    for asset in prepared:
        if not asset.get("source_url"):
            continue
        credit_lines += [
            "Asset: " + asset["file"],
            "Creator: " + asset["creator"],
            "Credit: " + asset["credit"],
            "Source: " + asset["source_url"],
            "Rights basis: " + asset["rights_basis_url"],
            "License URL: " + asset.get("license_url", ""),
            "License scope: " + asset.get("license_scope", ""),
            "Caption: " + asset["caption"],
            "Alt text: " + asset["alt_text"],
            "Event relation: " + str(asset.get("event_relation", "")),
            "Changes disclosed: " + str(asset.get("changes_disclosed", False)),
            "Verify the full attribution/change notices on X before publication.",
            "",
        ]
    (output / (slug + ".credits.txt")).write_text(
        "\n".join(credit_lines) + "\n", encoding="utf-8")
    return package
