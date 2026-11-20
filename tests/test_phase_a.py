"""Phase A guardrails: research leads never become approved events accidentally."""
import copy
from datetime import date
import unittest

from otdwx.phase_a import (
    anniversary_days, source_is_url, validate_calendar, validate_claim_checks, summarize, suggest
)


class PhaseAEditorialTests(unittest.TestCase):
    def fixture(self):
        rows = []
        catalog = {}
        for i, day in enumerate(anniversary_days()):
            historic = f"2024-{day}"
            ids = [f"lead-{i}-primary", f"lead-{i}-alt-1", f"lead-{i}-alt-2"]
            for ident in ids:
                catalog[ident] = {
                    "event_id": ident,
                    "event_date": historic,
                    "weather_type": "winter",
                    "region": "Midwest",
                    "country": "USA",
                    "title": f"Case {ident}",
                    "summary": "Snow observations and a documented mesoscale pattern" * 3,
                    "source_id": "ncei-storm-events",
                    "source_url": "https://example.org/archive",
                    "base_score": 40
                }
            rows.append({
                "calendar_date": day,
                "primary_event_id": ids[0],
                "first_alternate_event_id": ids[1],
                "second_alternate_event_id": ids[2],
                "historical_event_date": historic,
                "historical_year": 2024,
                "weather_category": "winter",
                "editorial_tier": "Tier 3 — Niche",
                "primary_storytelling_angle": "An original observed snow-gradient explanation",
                "alternate_storytelling_angle": "Context in the local climate record",
                "primary_source_url": "https://example.org/archive",
                "secondary_source_url": "",
                "source_verification_status": "single_source_record_needs_corroboration",
                "human_approval_status": "not_approved",
                "human_fact_check_status": "pending",
                "image_rights_status": "not_reviewed",
                "graphic_type": "Observational chart",
                "graphic_data_source": "https://example.org/archive",
                "country": "USA",
                "region": "Midwest",
                "geography_key": "Iowa",
                "primary_source_family": "ncei-storm-events",
                "historical_era": "2000–2025"
            })
        return {"days": rows}, catalog

    def test_all_366_days_and_leap_day(self):
        days = anniversary_days()
        self.assertEqual(len(days), 366)
        self.assertEqual(len(set(days)), 366)
        self.assertIn("02-29", days)

    def test_366_fixture_valid_research_only(self):
        cal, cat = self.fixture()
        self.assertEqual(validate_calendar(cal, cat), [])
        audit = summarize(cal["days"])
        self.assertEqual(audit["calendar_rows"], 366)
        self.assertEqual(audit["fully_fact_checked"], 0)
        self.assertEqual(audit["human_approved"], 0)

    def test_same_alternate_and_primary_disallowed(self):
        cal, cat = self.fixture()
        cal["days"][58]["first_alternate_event_id"] = cal["days"][58]["primary_event_id"]
        self.assertTrue(any("same ID" in e for e in validate_calendar(cal, cat)))

    def test_event_anniversary_mismatch_rejected(self):
        cal, cat = self.fixture()
        cal["days"][59]["historical_event_date"] = "2024-03-01"
        self.assertTrue(any("primary date not anniversary" in e
                            for e in validate_calendar(cal, cat)))

    def test_approval_guardrails(self):
        cal, cat = self.fixture()
        cal["days"][60]["human_approval_status"] = "approved"
        self.assertTrue(any("approval requires" in e
                            for e in validate_calendar(cal, cat)))
        cal["days"][60]["human_fact_check_status"] = "completed"
        cal["days"][60]["image_rights_status"] = "verified_public_domain"
        self.assertEqual(validate_calendar(cal, cat), [])

    def test_core_corroboration_requires_link(self):
        cal, cat = self.fixture()
        cal["days"][60]["source_verification_status"] = "core_date_location_corroborated"
        self.assertTrue(any("corroborated label lacks secondary URL" in e
                            for e in validate_calendar(cal, cat)))

    def test_nhc_track_never_receives_confirmation_from_score(self):
        cal, cat = self.fixture()
        lead = cat["lead-50-alt-1"]
        lead["country"] = "Unconfirmed"
        lead["source_id"] = "nhc-hurdat-atlantic"
        lead["base_score"] = 100
        result = suggest("02-20", cat, cal["days"])
        match = next(x for x in result if x["event_id"] == lead["event_id"])
        self.assertTrue(match["requires_editor_review"])
        self.assertFalse(match["current_primary"])
        self.assertTrue(match["research_signal_not_verification"] < 100)

    def test_dual_alternates_need_two_explicit_evidence_records(self):
        cal, cat = self.fixture()
        row = cal["days"][60]
        row["alternates_verification_status"] = "two_alternates_core_corroborated"
        self.assertTrue(any("two matching evidence records" in e
                            for e in validate_calendar(cal, cat)))
        row["alternate_corroboration"] = [
            {"event_id": row[k],
             "event_date": row["historical_event_date"],
             "source_url": "https://example.org/source",
             "secondary_source_url": "https://example.com/review",
             "verified_core_fact": "Occurrence and date corroborated",
             "source_independence_assessment": "original source reused",
             "review_scope": "core event/date/location only",
             "publication_approval_status": "not_approved"}
            for k in ("first_alternate_event_id", "second_alternate_event_id")
        ]
        self.assertEqual(validate_calendar(cal, cat), [])
        self.assertEqual(summarize(cal["days"])["dates_with_two_corroborated_alternates"], 1)
        row["alternate_corroboration"][0]["secondary_source_url"] = ""
        self.assertTrue(any("lacks trustworthy core-only evidence" in e
                            for e in validate_calendar(cal, cat)))


    def test_adjacent_same_historical_storm_blocked(self):
        cal, cat = self.fixture()
        first, second = cal["days"][40:42]
        first["title"] = "The Great Blizzard of 1888"
        second["title"] = "The Great Blizzard of 1888 begins across New York"
        self.assertTrue(any("likely repeated same historical event" in e
                            for e in validate_calendar(cal, cat)))
        self.assertEqual(len(summarize(cal["days"])["adjacent_repeated_event_warnings"]), 1)
        second["title"] = "Thunderstorm winds strike the Gulf Coast"
        self.assertEqual(validate_calendar(cal, cat), [])


    def test_claim_ledger_requires_same_current_event_and_clear_unverified_guidance(self):
        cal, _ = self.fixture()
        row = cal["days"][62]
        good = {
            "claim_id": "test-001",
            "date": row["calendar_date"],
            "primary_event_id": row["primary_event_id"],
            "claim": "An observed weather event happened",
            "evidence": "Archived dated observation",
            "status": "source_cross_checked",
            "url": "https://example.com/source",
            "full_human_fact_check_status": "pending",
            "publication_approval": "not_approved",
            "media_rights": "not_reviewed",
            "use": "Research only"
        }
        ledger = {"metadata": {"claim_ledger_entries": 1},
                  "claim_checks": [good]}
        self.assertEqual(validate_claim_checks(ledger, cal["days"]), [])
        bad = copy.deepcopy(ledger)
        bad["claim_checks"][0]["primary_event_id"] = "replaced-event"
        self.assertTrue(any("stale or wrong primary" in e
                            for e in validate_claim_checks(bad, cal["days"])))
        bad = copy.deepcopy(ledger)
        bad["claim_checks"][0]["status"] = "unsupported_do_not_use"
        self.assertTrue(any("do-not-publish" in e
                            for e in validate_claim_checks(bad, cal["days"])))
        bad["claim_checks"][0]["use"] = "Exclude from published posts"
        self.assertEqual(validate_claim_checks(bad, cal["days"]), [])
        bad["claim_checks"][0]["publication_approval"] = "approved"
        self.assertTrue(any("approval lacks" in e
                            for e in validate_claim_checks(bad, cal["days"])))

    def test_claim_ledger_discovers_recent_research_passes(self):
        from otdwx.phase_a import CLAIM_LEDGERS
        included = {p.name for p in CLAIM_LEDGERS}
        for number in range(10, 20):
            self.assertIn(f"phase_a_pass{number}_research.json", included)

    def test_links_are_https(self):
        self.assertFalse(source_is_url(""))
        self.assertFalse(source_is_url("http://example.org"))
        self.assertTrue(source_is_url("https://www.weather.gov/pah/"))

if __name__ == "__main__":
    unittest.main()
