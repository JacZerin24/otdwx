"""Offline tests for real-evidence visual pipeline (assets are SYNTHETIC)."""
from __future__ import annotations

import base64
from pathlib import Path
import json
import tempfile
from xml.etree import ElementTree
import unittest

from otdwx.evidence_visuals import render_evidence, validate_evidence
from otdwx.production import validate_package, generate


PNG_PIXEL = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9c9YLXQAAAAASUVORK5CYII="
)


def fixture(typ="archive_panel"):
    return {
        "event_id": "test-only-1969-11-14", "event_date": "1969-11-14",
        "post_date": "2027-11-14",
        "caption": "#OTDwx: November 14, 1969:\n\nSYNTHETIC TEST ONLY.\n\nSource: Example Archive",
        "source_name": "Example Archive", "source_url": "https://example.org/test",
        "alt": "Synthetic placeholder fixture for source evidence image, not genuine historical media.",
        "type": typ, "weather_category": "unusual",
        "evidence": [{"fact": "test-only", "section": "test fixture"}],
        "editor_approval": "pending",
        "graphic_spec": {
            "title": "Synthetic evidence test",
            "deck": "Not a meteorological observation.",
            "headline_stat": "TEST",
            "data_source_url": "https://example.org/real-source-in-production",
            "rights_basis_url": "https://example.org/rights-in-production",
            "rights_status": "original_work",
            "rights_reviewed_by": "Test Fixture",
            "rights_reviewed_on": "2026-11-21",
            "credit_checked": True,
            "source_creator": "Test Fixture", "source_credit": "Test Fixture",
            "asset_kind": "survey_map", "asset_file": "demo.png",
            "valid_period": "SYNTHETIC NOT OBSERVED"
        }
    }


class EvidencePipelineTests(unittest.TestCase):
    def test_doc_archive_embeds_actual_private_png_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "demo.png").write_bytes(PNG_PIXEL)
            pkg = fixture()
            self.assertEqual([], validate_evidence(pkg))
            self.assertEqual([], validate_package(pkg))
            svg = render_evidence(pkg, root)
            self.assertIn("data:image/png;base64", svg)
            self.assertNotIn("FAKE RADAR", svg)
            ElementTree.fromstring(svg)
            rows=generate([pkg],root/"exports",asset_root=root)
            self.assertEqual(1,len(rows))
            self.assertTrue(next((root/"exports").glob("*.svg")).exists())

    def test_uncleared_rights_rejected(self):
        item = fixture()
        item["graphic_spec"]["rights_status"]="researching"
        self.assertTrue(any("rights" in e for e in validate_evidence(item)))
        self.assertTrue(validate_package(item))

    def test_missing_time_or_site_rejected_for_radar(self):
        pkg = fixture()
        pkg["graphic_spec"]["asset_kind"]="radar_reflectivity"
        pkg["graphic_spec"].pop("valid_period",None)
        self.assertTrue(validate_package(pkg))
        pkg["graphic_spec"].update(
            radar_site="KLTX",radar_product="0.5 deg base reflectivity",
            observed_at_utc="2006-11-16T11:37:00Z")
        self.assertEqual([],validate_package(pkg))

    def test_broken_image_bytes_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/"demo.png").write_text("not image bytes")
            with self.assertRaisesRegex(ValueError,"genuine PNG"):
                render_evidence(fixture(),Path(d))

    def test_checksum_guard_prevents_wrong_radar_still(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/"demo.png").write_bytes(PNG_PIXEL)
            pkg=fixture()
            pkg["graphic_spec"]["sha256"]="0"*64
            with self.assertRaisesRegex(ValueError,"checksum mismatch"):
                render_evidence(pkg,Path(d))

    def test_prevent_escape_from_private_source_root(self):
        pkg = fixture()
        pkg["graphic_spec"]["asset_file"]="../secret.png"
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,"Unsafe evidence"):
                render_evidence(pkg,Path(d))

    def test_geojson_source_track_requires_valid_lonlat(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            geometry={
                "type":"FeatureCollection",
                "features":[{"type":"Feature","properties":{"source":"synthetic"},
                             "geometry":{"type":"LineString","coordinates":[[-78.24,34.34],[-78.21,34.36]]}}]
            }
            (root/"shape.geojson").write_text(json.dumps(geometry))
            pkg=fixture("geo_track")
            pkg["graphic_spec"]={
                "title":"Synthetic track only","deck":"Two artificial endpoints; not surveyed",
                "geometry_file":"shape.geojson",
                "geometry_role":"straight summary line",
                "track_quality":"endpoint_summary",
                "data_source_url":"https://example.org/test-only",
                "rights_basis_url":"https://example.org/test-only-rights",
                "rights_status":"original_work","rights_reviewed_by":"Fixture",
                "rights_reviewed_on":"2026-11-21","credit_checked":True,
                "source_credit":"Example Archive",
            }
            self.assertEqual([],validate_package(pkg))
            svg=render_evidence(pkg,root)
            self.assertIn('stroke-dasharray="13 13"',svg)
            ElementTree.fromstring(svg)
            geometry["features"][0]["geometry"]["coordinates"][0]=[-300,34.34]
            (root/"shape.geojson").write_text(json.dumps(geometry))
            with self.assertRaisesRegex(ValueError,"Invalid lon/lat"):
                render_evidence(pkg,root)

    def test_no_data_file_is_not_silently_replaced_with_illustration(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,"absent"):
                generate([fixture()],Path(d)/"exports",asset_root=Path(d))

if __name__=="__main__":
    unittest.main()
