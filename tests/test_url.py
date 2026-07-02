import unittest

from curler.url import UrlError, normalize_url


class NormalizeUrlTest(unittest.TestCase):
    def test_adds_https_when_scheme_is_missing(self):
        self.assertEqual(normalize_url("example.com"), "https://example.com")

    def test_preserves_http_and_https_urls(self):
        self.assertEqual(normalize_url("http://example.com"), "http://example.com")
        self.assertEqual(
            normalize_url("https://example.com/docs"), "https://example.com/docs"
        )

    def test_rejects_invalid_urls(self):
        for value in ["", "   ", "ftp://example.com", "https:///missing-host"]:
            with self.subTest(value=value):
                with self.assertRaises(UrlError):
                    normalize_url(value)


if __name__ == "__main__":
    unittest.main()
