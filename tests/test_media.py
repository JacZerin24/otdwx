"""Rights and private-media integration tests. All imagery is synthetic."""
from __future__ import annotations

import base64
import copy
import json
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree

from otdwx.media import validate_media, render_photo_card, export_media
from otdwx.production import validate_package, generate


def sample():
    return {
        "event_id": "synthetic-1900-01-01", "event_date": "1900-01-01",
        "post_date": "2027-01-01",
        "caption": "#OTDwx: January 1, 1900:\n\nOnly a test fixture.\n\nSource: Example Archive",
        "source_name": "Example Archive", "source_url": "https://example.org/source",
        "weather_category": "winter", "type": "bar_comparison",
        "graphic_spec": {"title": "Synthetic test", "rows": [
            {"label": "1900", "value": 4}, {"label": "1899", "value": 2}],
            "unit": "in", "footnote": "Fake test measurements"},
        "evidence": [{"fact": "SYNTHETIC", "section": "Test only"}],
        "alt": "Synthetic test chart with fake values, not historical weather.",
        "editor_approval": "pending",
    }


def cleared_photo():
    return {
        "kind": "photo", "file": "photo/example.png",
        "source_url": "https://example.org/fixture-photo",
        "rights_basis_url": "https://example.org/rights",
        "creator": "Synthetic Test Generator", "credit": "Synthetic Test Generator",
        "caption": "Generated test pattern, not a real weather image.",
        "alt_text": "Synthetic one-pixel fixture for exercising image packaging tests.",
        "event_relation": "related_context",
        "context_disclosure": "NOT A HISTORICAL EVENT IMAGE",
        "rights_status": "original_work", "rights_reviewed_by": "Test Fixture",
        "rights_reviewed_on": "2026-11-21",
        "commercial_use_allowed": True, "modifications_allowed": True,
        "credit_placement_confirmed": True,
    }


def write_test_pixel(root: Path):
    img = root / "photo" / "example.png"
    img.parent.mkdir(parents=True, exist_ok=True)
    img.write_bytes(base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9c9YLXQAAAAASUVORK5CYII="))
    return img


class MediaTests(unittest.TestCase):
    def test_original_package_stays_compatible(self):
        p = sample()
        self.assertEqual([], validate_media(p))
        self.assertEqual([], validate_package(p))
        with tempfile.TemporaryDirectory() as d:
            rows = generate([p], Path(d))
            self.assertEqual("graphic_only", rows[0]["media_mode"])
            self.assertEqual(1, len(list(Path(d).glob("*.svg"))))
            self.assertEqual(2, len(list(Path(d).glob("*.txt"))))

    def test_unknown_license_blocks_photo_output(self):
        p = sample()
        p["media_mode"] = "graphic_plus_photo"
        photo = cleared_photo()
        photo["rights_status"] = "unknown"
        p["photo"] = photo
        self.assertTrue(any("rights_status" in x for x in validate_media(p)))
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                generate([p], Path(d), asset_root=Path(d))

    def test_no_rights_inferred_from_noaa_source(self):
        p = sample()
        p["media_mode"] = "graphic_plus_photo"
        photo = cleared_photo()
        photo["source_url"] = "https://www.weather.gov/some-case"
        del photo["rights_basis_url"]
        p["photo"] = photo
        self.assertTrue(any("rights_basis_url" in x for x in validate_media(p)))

    def test_safe_local_file_and_actual_composite_render(self):
        p = sample()
        p["media_mode"] = "graphic_plus_photo"
        p["photo_layout"] = "editorial_split"
        p["photo"] = cleared_photo()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "private"
            image = write_test_pixel(root)
            svg = render_photo_card(p, image)
            ElementTree.fromstring(svg)
            self.assertIn("data:image/png;base64,", svg)
            self.assertIn("CONTEXT PHOTO", svg)
            rows = generate([p], Path(d) / "exports", asset_root=root)
            slug = p["post_date"] + "_" + p["event_id"]
            self.assertEqual("graphic_plus_photo", rows[0]["media_mode"])
            self.assertTrue((Path(d) / "exports" / (slug + ".documentary.svg")).exists())
            self.assertTrue((Path(d) / "exports" / (slug + ".asset-1.png")).exists())
            manifest = json.loads((Path(d) / "exports" / (slug + ".media.json")).read_text())
            self.assertFalse(manifest["publishing_enabled"])
            self.assertEqual("pending", manifest["approval"])

    def test_photo_must_have_explicit_modification_permission_for_composite(self):
        p = sample()
        p.update(media_mode="graphic_plus_photo", photo=cleared_photo(),
                 photo_layout="editorial_split")
        p["photo"]["modifications_allowed"] = False
        self.assertTrue(any("layout not licensed" in x for x in validate_media(p)))
        p["photo_layout"] = "none"
        self.assertEqual([], validate_media(p))

    def test_traversal_and_symlink_paths_rejected(self):
        p = sample()
        p.update(media_mode="graphic_plus_photo", photo=cleared_photo())
        p["photo"]["file"] = "../../home/secrets.png"
        self.assertTrue(any("local relative" in x for x in validate_media(p)))

    def test_cc_by_requires_license_link_and_change_disclosure(self):
        p = sample()
        p.update(media_mode="graphic_plus_photo", photo=cleared_photo(),
                 photo_layout="editorial_split")
        p["photo"]["rights_status"] = "cc_by"
        self.assertTrue(any("license URL" in x for x in validate_media(p)))
        p["photo"]["license_url"] = "https://creativecommons.org/licenses/by/4.0/"
        self.assertTrue(any("disclose changes" in x for x in validate_media(p)))
        p["photo"]["changes_disclosed"] = True
        self.assertEqual([], validate_media(p))

    def test_map_requires_asset_and_rights(self):
        p = sample()
        p["media_mode"] = "graphic_plus_map"
        self.assertTrue(validate_media(p))
        asset = cleared_photo()
        asset.update(kind="map",file="maps/map.png")
        p["supporting_media"] = [asset]
        self.assertEqual([], validate_media(p))

    def test_animated_loop_cannot_be_mixed_into_carousel(self):
        p = sample()
        p["media_mode"] = "carousel"
        a = cleared_photo()
        a.update(kind="radar_loop",file="loops/radar.gif")
        p["supporting_media"] = [a]
        self.assertTrue(any("separate X" in x for x in validate_media(p)))
        p["media_mode"] = "animated_package"
        self.assertEqual([], validate_media(p))
        p["photo"] = cleared_photo()
        self.assertTrue(validate_media(p))

    def test_asset_root_is_required_for_real_media(self):
        p = sample()
        p.update(media_mode="graphic_plus_photo",photo=cleared_photo())
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError, "asset-root"):
                generate([p], Path(d))


if __name__ == "__main__":
    unittest.main()
