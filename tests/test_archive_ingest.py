"""Archive link discovery is pure HTML parsing; no web requests in CI."""
import unittest

from otdwx.archive_ingest import EvidenceLinkParser


class ArchiveIngestTests(unittest.TestCase):
    def test_extracts_relative_source_image_and_link(self):
        parser=EvidenceLinkParser("https://www.weather.gov/ilm/2006-Nov-16tornado")
        parser.feed('''<img src="/images/ilm/historic/radar.gif" alt="Reflectivity loop">
        <a href="/images/ilm/tornado_path.png" title="Survey track">map</a>
        <img src="/images/ilm/historic/radar.gif" alt="same loop">''')
        urls=[r["asset_url"] for r in parser.items]
        self.assertIn("https://www.weather.gov/images/ilm/historic/radar.gif",urls)
        self.assertIn("https://www.weather.gov/images/ilm/tornado_path.png",urls)
        self.assertEqual(3,len(urls))

    def test_ignores_nonarchive_and_script_links(self):
        p=EvidenceLinkParser("https://www.weather.gov/test")
        p.feed('<script src="/a.js"></script><a href="javascript:alert(1)">hi</a><img src="/map.png">')
        self.assertEqual(["https://www.weather.gov/map.png"],
                         [x["asset_url"] for x in p.items])


if __name__=="__main__":
    unittest.main()
