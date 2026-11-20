import tempfile
from pathlib import Path
from xml.etree import ElementTree
import unittest

from otdwx.production import render_svg, validate_package, generate


def fixture():
    return {
       "event_id":"synthetic-example-1900", "event_date":"1900-01-01",
       "post_date":"2027-01-01",
       "caption":"#OTDwx: January 1, 1900:\n\nExample only (not a real event).\n\nSource: Fictional Archive",
       "source_name":"Fictional Archive","source_url":"https://example.org/source",
       "type":"bar_comparison","alt":"Synthetic chart demonstration, not real weather history.",
       "evidence":[{"fact":"Synthetic fact for unit tests only.","section":"Fixture"}],
       "graphic_spec":{"title":"Fictional <record>","subtitle":"Synthetic / test",
                       "rows":[{"label":"A","value":8},{"label":"B","value":4}],
                       "unit":"in","footnote":"No real observations"},
       "editor_approval":"pending",
    }


class ProductionTests(unittest.TestCase):
    def test_valid_fixture(self):
        self.assertEqual(validate_package(fixture()),[])

    def test_svg_is_safe_xml_and_no_external_media(self):
        svg=render_svg(fixture())
        ElementTree.fromstring(svg)
        self.assertIn("Fictional &lt;record&gt;",svg)
        self.assertNotIn("<image",svg)

    def test_source_required(self):
        p=fixture();p["source_url"]="http://example.org"
        self.assertTrue(any("HTTPS" in e for e in validate_package(p)))

    def test_length_limit(self):
        p=fixture();p["caption"]=p["caption"].replace("Example only", "A"*350)
        self.assertTrue(any("280" in e for e in validate_package(p)))

    def test_historical_date_guard(self):
        p=fixture();p["event_date"]="1901-01-01"
        self.assertTrue(any("date header" in e for e in validate_package(p)))

    def test_export_with_private_fixture(self):
        with tempfile.TemporaryDirectory() as d:
            rows=generate([fixture()],Path(d))
            self.assertEqual(len(rows),1)
            self.assertEqual(len(list(Path(d).glob("*.svg"))),1)
            self.assertEqual(len(list(Path(d).glob("*.txt"))),2)
            self.assertTrue((Path(d)/"manifest.csv").exists())


if __name__=="__main__":
    unittest.main()
