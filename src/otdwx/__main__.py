"""Command-line checks; deliberately no publishing commands."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .editorial import check_post
from .validation import validate_events, validate_log, diversity_warnings

ROOT = Path(__file__).resolve().parents[2]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(prog="otdwx", description="OTDwx Phase 1 editorial tools")
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("validate-data", help="Check canonical event data and publishing log")
    post = commands.add_parser("post-check", help="Check one draft text file against 280 characters")
    post.add_argument("--file", required=True, type=Path)
    diversity = commands.add_parser("diversity-check", help="Warn about repeats for one saved event")
    diversity.add_argument("--event-id", required=True)
    args = parser.parse_args()
    if args.action == "validate-data":
        events = load_json(ROOT / "data/events.json")
        history = load_json(ROOT / "data/publishing_log.json")
        issues = validate_events(events) + validate_log(history)
        if issues:
            for issue in issues:
                print(f"ERROR {issue}")
            return 1
        print(f"OK: {len(events)} curated events; {len(history)} published posts")
        return 0
    if args.action == "post-check":
        txt = args.file.read_text(encoding="utf-8").rstrip("\n")
        outcome = check_post(txt)
        print(json.dumps(outcome, indent=2))
        return 0 if outcome["under_hard_limit"] and outcome["has_otdwx_header"] and outcome["has_source_line"] else 1
    if args.action == "diversity-check":
        events = load_json(ROOT / "data/events.json")
        history = load_json(ROOT / "data/publishing_log.json")
        match = next((e for e in events if e.get("event_id") == args.event_id), None)
        if match is None:
            print(f"ERROR: no such event_id: {args.event_id}")
            return 1
        candidate = {**match, "featured_source_id": match["sources"][0]["source_id"]}
        warnings = diversity_warnings(candidate, history)
        print("\n".join(warnings) if warnings else "No repetition warnings from recorded posts")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
