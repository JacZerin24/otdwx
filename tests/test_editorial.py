import unittest
from datetime import date

from otdwx.editorial import check_post, format_post, weighted_length


class EditorialTests(unittest.TestCase):
    def test_format_matches_house_style(self):
        post = format_post(
            date(1998, 4, 8), "A concise, researched event description.",
            "Verified Archive", [("Injuries", "verified count")]
        )
        self.assertTrue(post.startswith("#OTDwx: April 8, 1998:\n\nInjuries:"))
        self.assertTrue(post.endswith("\n\nSource: Verified Archive"))
        self.assertLessEqual(weighted_length(post), 280)

    def test_ascii_280_exact(self):
        text = "a" * 280
        self.assertEqual(weighted_length(text), 280)
        self.assertTrue(check_post(text)["under_hard_limit"])
        self.assertFalse(check_post(text + "a")["under_hard_limit"])

    def test_link_is_23_weighted_chars(self):
        self.assertEqual(weighted_length("View https://example.com/long/path"), 5 + 23)
        self.assertEqual(weighted_length("https://example.com."), 24)

    def test_post_preflight(self):
        text = "#OTDwx: May 1, 1900:\n\nA verified, short fact.\n\nSource: Historical Archive"
        result = check_post(text)
        self.assertTrue(result["under_hard_limit"])
        self.assertTrue(result["has_otdwx_header"])
        self.assertTrue(result["has_source_line"])

    def test_unicode_does_not_undercount(self):
        self.assertEqual(weighted_length("🌪"), 2)
        self.assertEqual(weighted_length("A🌪"), 3)


if __name__ == "__main__":
    unittest.main()
