"""Draft assembly and conservative, URL-aware X character preflight."""
from __future__ import annotations

from datetime import date
import re

MAX_WEIGHTED_CHARS = 280
DRAFT_TARGET = 260
URL_WEIGHT = 23
URL_RE = re.compile(r"https?://[^\s]+", flags=re.IGNORECASE)


def _weight(char: str) -> int:
    """Weight based on twitter-text v3 ranges; conservative for emoji clusters."""
    code = ord(char)
    if (
        code <= 4351
        or 8192 <= code <= 8205
        or 8208 <= code <= 8223
        or 8242 <= code <= 8247
    ):
        return 1
    return 2


def weighted_length(text: str) -> int:
    """Estimate X weighted characters (URLs count as 23).

    Complex grapheme/emoji sequences can be over-counted. Verify in the X
    composer before posting. A conservative rejection may need human review.
    """
    total = 0
    cursor = 0
    for match in URL_RE.finditer(text):
        total += sum(_weight(c) for c in text[cursor:match.start()])
        url = match.group(0)
        trailing = len(url) - len(url.rstrip(".,!?;:"))
        total += URL_WEIGHT
        total += sum(_weight(c) for c in url[-trailing:]) if trailing else 0
        cursor = match.end()
    return total + sum(_weight(c) for c in text[cursor:])


def format_post(event_date: date, narrative: str, source_label: str,
                stats: list[tuple[str, str]] | None = None) -> str:
    """Create the house format without writing, inferring or changing any facts."""
    if not narrative.strip() or not source_label.strip():
        raise ValueError("Narrative and source_label are required.")
    if "\n" in source_label:
        raise ValueError("Source label must fit on one line.")
    intro = f"#OTDwx: {event_date.strftime('%B')} {event_date.day}, {event_date.year}:"
    blocks = [intro]
    if stats:
        stat_lines = []
        for label, value in stats:
            if not label.strip() or not value.strip() or "\n" in label + value:
                raise ValueError("Stats must be single-line, nonempty labels and values.")
            stat_lines.append(f"{label}: {value}")
        blocks.append("\n".join(stat_lines))
    blocks.append(narrative.strip())
    blocks.append(f"Source: {source_label.strip()}")
    return "\n\n".join(blocks)


def check_post(text: str) -> dict[str, object]:
    count = weighted_length(text)
    return {
        "weighted_chars_estimate": count,
        "remaining": MAX_WEIGHTED_CHARS - count,
        "under_hard_limit": count <= MAX_WEIGHTED_CHARS,
        "under_draft_target": count <= DRAFT_TARGET,
        "has_otdwx_header": text.lstrip().startswith("#OTDwx: "),
        "has_source_line": "\nSource: " in text or text.startswith("Source: "),
    }
