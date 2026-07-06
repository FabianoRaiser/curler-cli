import unittest

from curler.fetcher import FetchResult
from curler.parser import ParsedLink, ParsedPage
from curler.renderer import SPA_WARNING, format_body, render_page


class RenderPageTest(unittest.TestCase):
    def test_renders_title_text_and_links(self):
        page = ParsedPage(
            title="Example",
            text="Hello\nWorld",
            links=(
                ParsedLink(number=1, text="Docs", href="https://example.com/docs"),
                ParsedLink(number=2, text="Blog", href="https://example.com/blog"),
            ),
        )

        output = render_page(page)

        self.assertIn("Example", output)
        self.assertIn("Hello\nWorld", output)
        self.assertIn("[1] Docs (https://example.com/docs)", output)
        self.assertIn("[2] Blog (https://example.com/blog)", output)

    def test_includes_spa_warning(self):
        page = ParsedPage(title="App", text="", links=(), spa_warning=True)

        output = render_page(page)

        self.assertIn(SPA_WARNING, output)

    def test_format_body_parsed(self):
        result = FetchResult(
            url="https://example.com",
            headers="",
            body="<html><body>Hello</body></html>",
        )

        self.assertEqual(format_body(result), "Hello\n")

    def test_format_body_raw(self):
        html = "<html><body>Hello</body></html>"
        result = FetchResult(url="https://example.com", headers="", body=html)

        self.assertEqual(format_body(result, raw=True), html)

    def test_empty_page_returns_empty_string(self):
        page = ParsedPage(title="", text="", links=())

        self.assertEqual(render_page(page), "")


if __name__ == "__main__":
    unittest.main()
