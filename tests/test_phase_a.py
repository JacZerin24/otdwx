"""Phase A guardrails: research leads never become approved events accidentally."""
import copy
from datetime import date
import unittest

from otdwx.phase_a import (
    anniversary_days, source_is_url, validate_calendar, summarize, suggest
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

    def test_links_are_https(self):
        self.assertFalse(source_is_url(""))
        self.assertFalse(source_is_url("http://example.org"))
        self.assertTrue(source_is_url("https://www.weather.gov/pah/"))

if __name__ == "__main__":
    unittest.main()
