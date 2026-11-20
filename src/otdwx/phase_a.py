"""Phase A editorial library inspection. Research candidates are never approvals.

Run:
    python -m otdwx.phase_a --audit
    python -m otdwx.phase_a --suggest 02-29

This module does not mutate the hand-curated calendar or source catalog.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date, timedelta
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
CALENDAR = ROOT / "data/phase_a_calendar.json"
CATALOG = ROOT / "data/discovery_candidates.json"
CURATED = ROOT / "data/curated_candidates.json"
ANCHORS = ROOT / "data/phase_a_sourced_anchors.json"
PUBLICATION = ROOT / "data/publishing_log.json"
CLAIM_LEDGERS = [ROOT / "data/phase_a_pass10_research.json",
                 ROOT / "data/phase_a_pass11_research.json"]
ALLOWED = {"tornado", "severe_storm", "tropical", "flood", "winter",
           "temperature", "drought", "wildfire_weather", "unusual", "other"}
GRADES = {"Tier 1 — Flagship", "Tier 2 — Strong", "Tier 3 — Niche"}
CORE = "core_date_location_corroborated"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def anniversary_days() -> list[str]:
    return [(date(2024, 1, 1) + timedelta(days=n)).strftime("%m-%d")
            for n in range(366)]


def source_is_url(value: str) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def candidates(root: Path = ROOT) -> dict[str, dict]:
    discovery = read(root / "data/discovery_candidates.json")["candidates"]
    curated = read(root / "data/curated_candidates.json")
    anchors = read(root / "data/phase_a_sourced_anchors.json")
    return {x["event_id"]: x for x in [*discovery, *curated, *anchors]}


def adjacent_repeated_event_warnings(rows: list[dict]) -> list[str]:
    """Flag likely duplicate stories on neighboring anniversaries, not shared hazards.

    This narrow headline heuristic intentionally avoids using source URL alone:
    NCEI year-level CSV URLs can legitimately cover many unrelated events.
    """
    common = {"the", "a", "an", "of", "as", "in", "on", "into", "to", "near",
              "over", "across", "from", "through", "and", "after", "before",
              "during", "begins", "brings", "strikes", "reaches", "with",
              "while", "its", "at", "for", "recorded", "historic"}

    def words(title):
        return {w for w in re.findall(r"[a-z0-9]+", str(title).lower())
                if len(w) > 2 and w not in common}

    warnings = []
    for previous, current in zip(rows, rows[1:]):
        if previous.get("historical_year") != current.get("historical_year"):
            continue
        left = words(previous.get("title", ""))
        right = words(current.get("title", ""))
        shared = len(left & right)
        if shared >= 3 and shared / max(1, min(len(left), len(right))) >= 0.8:
            warnings.append(
                f"{previous.get('calendar_date')} and {current.get('calendar_date')}: "
                "likely repeated same historical event on adjacent days")
    return warnings


def validate_claim_checks(ledger: dict, calendar_rows: list[dict]) -> list[str]:
    """Check claim-ledger structure and event linkage, NOT truth of its source claims."""
    problems: list[str] = []
    checks = ledger.get("claim_checks", [])
    if not isinstance(checks, list):
        return ["claim_checks must be a list"]
    expected_count = ledger.get("metadata", {}).get("claim_ledger_entries")
    if expected_count != len(checks):
        problems.append("claim-ledger metadata count mismatch")
    current_by_date = {row.get("calendar_date"): row for row in calendar_rows}
    seen = set()
    for item in checks:
        if not isinstance(item, dict):
            problems.append("claim check must be an object")
            continue
        cid = item.get("claim_id", "")
        if not cid or cid in seen:
            problems.append(f"claim ID missing or duplicated: {cid}")
        seen.add(cid)
        date_str = item.get("date", "")
        current = current_by_date.get(date_str)
        if current is None:
            problems.append(f"{cid}: claim has unrecognized anniversary")
            continue
        if item.get("primary_event_id") != current.get("primary_event_id"):
            problems.append(f"{cid}: claim references stale or wrong primary event ID")
        if not item.get("claim") or not item.get("evidence") or not item.get("status"):
            problems.append(f"{cid}: missing substantive claim or evidence")
        if not source_is_url(item.get("url", "")):
            problems.append(f"{cid}: claim source must be an HTTPS URL")
        status = item.get("status", "")
        if (status.endswith("do_not_use") or status == "conflicting_source_counts") and (
                "exclude" not in item.get("use", "").lower()
                and "do not" not in item.get("use", "").lower()):
            problems.append(f"{cid}: unresolved assertion lacks explicit do-not-publish guidance")
        if item.get("publication_approval") == "approved":
            if (current.get("human_approval_status") != "approved"
                    or item.get("full_human_fact_check_status") != "completed"
                    or item.get("media_rights") not in
                    {"verified_public_domain", "licensed", "permission_granted"}):
                problems.append(f"{cid}: claim approval lacks full editorial and rights gate")
    return problems


def validate_calendar(calendar: dict, catalog: dict[str, dict],
                      publishing_log: list[dict] | None = None) -> list[str]:
    """Return structural and status-integrity errors, not editorial opinions."""
    problems: list[str] = []
    rows = calendar.get("days")
    if not isinstance(rows, list):
        return ["calendar.days must be an array"]
    valid_days = anniversary_days()
    if len(rows) != len(valid_days):
        problems.append("expected 366 calendar rows")
    existing: set[str] = set()
    primaries: set[str] = set()
    published_ids = {x.get("event_id") for x in (publishing_log or [])}
    for index, row in enumerate(rows):
        day = row.get("calendar_date", "")
        if day != (valid_days[index] if index < 366 else ""):
            problems.append(f"row {index + 1}: dates must be in leap-year order")
        if day in existing:
            problems.append(f"{day}: duplicate anniversary")
        existing.add(day)
        primary = row.get("primary_event_id", "")
        alternates = [row.get("first_alternate_event_id", ""),
                      row.get("second_alternate_event_id", "")]
        if not primary or any(not x for x in alternates):
            problems.append(f"{day}: missing primary or alternate ID")
        if len(set([primary, *alternates])) != 3:
            problems.append(f"{day}: same ID used more than once")
        if primary in primaries:
            problems.append(f"{day}: duplicate primary ID used on another date")
        primaries.add(primary)
        for eid in [primary, *alternates]:
            if eid not in catalog:
                problems.append(f"{day}: ID missing from catalog: {eid}")
            elif catalog[eid].get("event_date", "")[5:] != day:
                problems.append(f"{day}: event date mismatch: {eid}")
        historical_date = row.get("historical_event_date", "")
        try:
            parsed = date.fromisoformat(historical_date)
            if parsed.strftime("%m-%d") != day:
                problems.append(f"{day}: primary date not anniversary")
            if row.get("historical_year") != parsed.year:
                problems.append(f"{day}: year and historic date disagree")
        except (ValueError, TypeError):
            problems.append(f"{day}: invalid historical_event_date")
        if row.get("weather_category") not in ALLOWED:
            problems.append(f"{day}: unknown hazard")
        if row.get("editorial_tier") not in GRADES:
            problems.append(f"{day}: missing/invalid tier")
        if not source_is_url(row.get("primary_source_url", "")):
            problems.append(f"{day}: missing primary HTTPS source")
        if not row.get("graphic_type") or not source_is_url(
                row.get("graphic_data_source", "")):
            problems.append(f"{day}: missing proposed graphic/data source")
        if not row.get("primary_storytelling_angle") or not row.get("alternate_storytelling_angle"):
            problems.append(f"{day}: editorial angles missing")
        status = row.get("source_verification_status", "")
        if not status:
            problems.append(f"{day}: absent independent source review status")
        if status == CORE and not source_is_url(row.get("secondary_source_url", "")):
            problems.append(f"{day}: corroborated label lacks secondary URL")
        if row.get("human_approval_status") == "approved" and (
                row.get("human_fact_check_status") != "completed"
                or row.get("image_rights_status") not in
                {"verified_public_domain", "licensed", "permission_granted"}):
            problems.append(f"{day}: approval requires completed fact check and image rights")
        if row.get("alternates_verification_status") == "two_alternates_core_corroborated":
            evidence = row.get("alternate_corroboration", [])
            if (not isinstance(evidence, list) or len(evidence) != 2
                    or {item.get("event_id") for item in evidence
                        if isinstance(item, dict)} != set(alternates)):
                problems.append(f"{day}: two corroborated alternates require two matching evidence records")
            else:
                for item in evidence:
                    if (item.get("event_date", "")[5:] != day
                            or item.get("review_scope") != "core event/date/location only"
                            or not source_is_url(item.get("source_url", ""))
                            or not source_is_url(item.get("secondary_source_url", ""))
                            or not item.get("verified_core_fact")
                            or not item.get("source_independence_assessment")
                            or item.get("publication_approval_status") != "not_approved"):
                        problems.append(f"{day}: alternate {item.get('event_id')} lacks trustworthy core-only evidence")
        if primary in published_ids and row.get("human_approval_status") == "not_approved":
            # Only an indicator: publishing history takes precedence over a research calendar.
            # A manual status sync must not silently rewrite the historical publishing log.
            pass
    if set(valid_days) != existing:
        problems.append("missing or unrecognized anniversary days")
    problems.extend(adjacent_repeated_event_warnings(rows))
    return problems


def summarize(rows: list[dict]) -> dict:
    def distribution(name: str) -> dict:
        return dict(Counter(x.get(name, "unknown") for x in rows).most_common())

    def count(condition) -> int:
        return sum(1 for x in rows if condition(x))

    def adjacent(key: str) -> int:
        return sum(rows[i][key] == rows[i - 1][key]
                   for i in range(1, len(rows)))

    problems = [x["calendar_date"] for x in rows
                if x.get("editorial_tier") == "Tier 3 — Niche"
                and x.get("source_verification_status") != CORE]
    return {
        "calendar_rows": len(rows),
        "distinct_primary_event_ids": len({x.get("primary_event_id") for x in rows}),
        "dates_with_two_corroborated_alternates": count(
            lambda x: x.get("alternates_verification_status") == "two_alternates_core_corroborated"),
        "days_with_two_alternate_leads": count(
            lambda x: bool(x.get("first_alternate_event_id")
                           and x.get("second_alternate_event_id"))),
        "core_date_location_corroborated": count(
            lambda x: x.get("source_verification_status") == CORE),
        "secondary_links_present": count(
            lambda x: source_is_url(x.get("secondary_source_url", ""))),
        "fully_fact_checked": count(
            lambda x: x.get("human_fact_check_status") == "completed"),
        "human_approved": count(
            lambda x: x.get("human_approval_status") == "approved"),
        "assigned_graphic_concepts": count(lambda x: bool(x.get("graphic_type"))),
        "asset_rights_cleared": count(
            lambda x: x.get("image_rights_status") in
            {"verified_public_domain", "licensed", "permission_granted"}),
        "international_primary_days": count(lambda x: x.get("country") != "USA"),
        "pre_1950_primary_days": count(lambda x: int(x.get("historical_year") or 9999) < 1950),
        "hazard_categories": distribution("weather_category"),
        "geographic_regions": distribution("region"),
        "source_families": distribution("primary_source_family"),
        "historical_eras": distribution("historical_era"),
        "editorial_tiers": distribution("editorial_tier"),
        "consecutive_same_hazard": adjacent("weather_category"),
        "consecutive_same_region": adjacent("region"),
        "consecutive_same_geography": adjacent("geography_key"),
        "consecutive_same_source_family": adjacent("primary_source_family"),
        "weak_tier3_dates": problems,
        "adjacent_repeated_event_warnings": adjacent_repeated_event_warnings(rows),
        "days_lacking_second_source": [
            x["calendar_date"] for x in rows
            if not source_is_url(x.get("secondary_source_url", ""))
        ],
    }


def suggest(date_mmdd: str, catalog: dict[str, dict],
            calendar_rows: list[dict], limit: int = 8) -> list[dict]:
    if date_mmdd not in anniversary_days():
        raise ValueError("Enter a valid MM-DD calendar anniversary, including 02-29")
    current = next(x for x in calendar_rows if x["calendar_date"] == date_mmdd)
    recent_index = anniversary_days().index(date_mmdd)
    previous = calendar_rows[recent_index - 1] if recent_index else calendar_rows[-1]
    possibilities = []
    for x in catalog.values():
        if x.get("event_date", "")[5:] != date_mmdd:
            continue
        narrative = str(x.get("summary") or "")
        source_family = x.get("source_id", "")
        # This is a RESEARCH triage signal, not an editorial or fact-check grade.
        score = float(x.get("base_score", 0)) + min(len(narrative), 250) / 35
        if len(narrative) < 65:
            score -= 28
        if x.get("country") == "Unconfirmed":
            score -= 35
        if source_family.startswith("nhc-hurdat-"):
            score -= 16  # Offshore track points aren't necessarily human-impact events.
        if x.get("weather_type") == previous.get("weather_category"):
            score -= 12
        if x.get("region") == previous.get("region"):
            score -= 8
        if source_family == previous.get("primary_source_family"):
            score -= 12
        if source_family == "phasea-authoritative-anchor":
            score += 20
        possibilities.append({
            "event_id": x["event_id"],
            "date": x["event_date"],
            "title": x.get("title"),
            "weather_type": x.get("weather_type"),
            "country": x.get("country"),
            "source_url": x.get("source_url"),
            "research_signal_not_verification": round(score, 2),
            "narrative_available": bool(narrative),
            "current_primary": x["event_id"] == current["primary_event_id"],
            "requires_editor_review": True
        })
    return sorted(possibilities,
                  key=lambda x: (-x["research_signal_not_verification"], x["event_id"]))[:limit]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--audit", action="store_true", help="Check 366 days and print an evidence-status audit")
    mode.add_argument("--suggest", metavar="MM-DD", help="Show research leads, not automatic choices")
    args = parser.parse_args(argv)
    calendar = read(CALENDAR)
    inventory = candidates()
    problems = validate_calendar(calendar, inventory, read(PUBLICATION))
    ledgers = [read(path) for path in CLAIM_LEDGERS if path.exists()]
    for ledger in ledgers:
        problems.extend(validate_claim_checks(ledger, calendar["days"]))
    all_claim_ids = [claim["claim_id"] for ledger in ledgers
                     for claim in ledger.get("claim_checks", []) if isinstance(claim, dict)]
    if len(all_claim_ids) != len(set(all_claim_ids)):
        problems.append("duplicate claim IDs across research passes")
    if args.audit:
        report = summarize(calendar["days"])
        if ledgers:
            report["claim_ledger_checks"] = sum(len(ledger.get("claim_checks", []))
                                                for ledger in ledgers)
        print(json.dumps({"structural_validation": {
            "valid": not problems, "problems": problems}, "metrics": report}, indent=2))
        return 0 if not problems else 1
    if problems:
        print(json.dumps({"errors": problems}, indent=2))
        return 1
    try:
        leads = suggest(args.suggest, inventory, calendar["days"])
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps({"anniversary": args.suggest,
                      "notice": "Research leads only; never automatically approved",
                      "leads": leads}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
