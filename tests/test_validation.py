import unittest

from otdwx.validation import validate_events, validate_log, diversity_warnings


class ValidationTests(unittest.TestCase):
    def test_empty_canonical_data_is_valid(self):
        self.assertEqual(validate_events([]), [])
        self.assertEqual(validate_log([]), [])

    def test_unverified_approval_is_rejected(self):
        event = {
            "event_id": "example-1900", "event_date": "1900-01-01",
            "title": "Illustrative event only", "summary": "Illustrative description only.",
            "weather_type": "tornado", "location": "Example", "region": "Example",
            "country": "USA", "sources": [{"source_id":"archive","publisher":"Archive","url":"https://example.org"}],
            "status": "approved",
            "media": [{"uri": "image","rights_status": "unverified"}]
        }
        issues = validate_events([event])
        self.assertTrue(any("fact_checked_by" in issue for issue in issues))
        self.assertTrue(any("media rights" in issue for issue in issues))

    def test_diversity_warning_is_advisory(self):
        recent = [
            {"event_id":"old1","region":"AL","weather_type":"tornado","featured_source_id":"nws"},
            {"event_id":"old2","region":"AL","weather_type":"tornado","featured_source_id":"nws"},
        ]
        new = {"event_id":"old1","region":"AL","weather_type":"tornado","featured_source_id":"nws"}
        warnings = diversity_warnings(new, recent)
        self.assertEqual(len(warnings), 4)


if __name__ == "__main__":
    unittest.main()
