import unittest

from curler.fetcher import FetchResult
from curler.parser import ParsedLink, ParsedPage
from curler.renderer import SPA_WARNING, format_body, render_page
from curler.style import RESET, Stylizer


class RenderPageTest(unittest.TestCase):
    def test_renders_title_text_and_inline_link_count(self):
        page = ParsedPage(
            title="Example",
            text="Read Docs [1] and Blog [2] for more.",
            links=(
                ParsedLink(number=1, text="Docs", href="https://example.com/docs"),
                ParsedLink(number=2, text="Blog", href="https://example.com/blog"),
            ),
        )

        output = render_page(page, stylizer=Stylizer(False))

        self.assertIn("Example", output)
        self.assertIn("Read Docs [1] and Blog [2] for more.", output)
        self.assertIn("(2 links)", output)
        self.assertNotIn("Links:", output)
        self.assertNotIn("https://example.com/docs", output)

    def test_repl_footer_includes_links_hint(self):
        page = ParsedPage(
            title="Example",
            text="About us [1]",
            links=(ParsedLink(number=1, text="About us", href="https://example.com/about"),),
        )

        output = render_page(page, show_links_hint=True, stylizer=Stylizer(False))

        self.assertIn("(1 link — use links)", output)

    def test_applies_ansi_colors_when_enabled(self):
        page = ParsedPage(
            title="Example",
            text="# Section\nDocs [1]",
            links=(ParsedLink(number=1, text="Docs", href="https://example.com/docs"),),
        )

        output = render_page(page, show_links_hint=True, stylizer=Stylizer(True))

        self.assertIn("\033[34m", output)
        self.assertIn("\033[1m", output)
        self.assertTrue(output.count(RESET) >= 3)

    def test_includes_spa_warning(self):
        page = ParsedPage(title="App", text="", links=(), spa_warning=True)

        output = render_page(page, stylizer=Stylizer(False))

        self.assertIn(SPA_WARNING, output)

    def test_spa_warning_is_yellow_when_colored(self):
        page = ParsedPage(title="App", text="", links=(), spa_warning=True)

        output = render_page(page, stylizer=Stylizer(True))

        self.assertIn("\033[33m", output)
        self.assertIn(SPA_WARNING, output)

    def test_format_body_parsed(self):
        result = FetchResult(
            url="https://example.com",
            headers="",
            body="<html><body>Hello</body></html>",
        )

        self.assertEqual(format_body(result, color=False), "Hello\n")

    def test_format_body_with_links_shows_count(self):
        result = FetchResult(
            url="https://example.com",
            headers="",
            body='<html><body><a href="/about">About</a></body></html>',
        )

        output = format_body(result, color=False)

        self.assertIn("About [1]", output)
        self.assertIn("(1 link)", output)
        self.assertNotIn("use links", output)

    def test_format_body_raw(self):
        html = "<html><body>Hello</body></html>"
        result = FetchResult(url="https://example.com", headers="", body=html)

        self.assertEqual(format_body(result, raw=True), html)

    def test_empty_page_returns_empty_string(self):
        page = ParsedPage(title="", text="", links=())

        self.assertEqual(render_page(page, stylizer=Stylizer(False)), "")


if __name__ == "__main__":
    unittest.main()
