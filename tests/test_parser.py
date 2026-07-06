import unittest

from curler.parser import parse_html
from tests.fixtures.html_samples import (
    BLOG_HTML,
    DUPLICATE_LINKS_HTML,
    HEADINGS_HTML,
    INLINE_MARKUP_HTML,
    LIST_WITH_LINK_HTML,
    LISTS_HTML,
    NESTED_LIST_HTML,
    SPA_HTML,
    WIKI_HTML,
)


class ParseHtmlTest(unittest.TestCase):
    def test_extracts_title_and_text_from_blog(self):
        page = parse_html(BLOG_HTML, base_url="https://blog.example.com/post")

        self.assertEqual(page.title, "My Blog Post")
        self.assertIn("# Hello World", page.text)
        self.assertIn("First paragraph.", page.text)
        self.assertIn("Second paragraph.", page.text)
        self.assertNotIn("console.log", page.text)
        self.assertFalse(page.spa_warning)

    def test_resolves_relative_links(self):
        page = parse_html(BLOG_HTML, base_url="https://blog.example.com/post")

        self.assertEqual(len(page.links), 2)
        self.assertEqual(page.links[0].number, 1)
        self.assertEqual(page.links[0].text, "About us")
        self.assertEqual(page.links[0].href, "https://blog.example.com/about")
        self.assertEqual(page.links[1].href, "https://example.com/contact")
        self.assertIn("About us [1]", page.text)
        self.assertIn("Contact [2]", page.text)

    def test_wiki_like_page_skips_fragment_and_js_links(self):
        page = parse_html(WIKI_HTML, base_url="https://en.wikipedia.org/wiki/Python")

        self.assertIn("# Python", page.text)
        self.assertIn("Python is a programming language.", page.text)
        self.assertIn("Guido van Rossum [1]", page.text)
        self.assertEqual(len(page.links), 1)
        self.assertEqual(
            page.links[0].href,
            "https://en.wikipedia.org/wiki/Guido_van_Rossum",
        )

    def test_renders_heading_levels(self):
        page = parse_html(HEADINGS_HTML, base_url="https://example.com/docs")

        self.assertIn("# Getting Started", page.text)
        self.assertIn("## Installation", page.text)
        self.assertIn("### Requirements", page.text)
        self.assertIn("Need Python 3.10+.", page.text)

    def test_renders_unordered_and_ordered_lists(self):
        page = parse_html(LISTS_HTML, base_url="https://example.com/")

        self.assertIn("- Gmail", page.text)
        self.assertIn("- Imagens", page.text)
        self.assertIn("1. Passo 1", page.text)
        self.assertIn("2. Passo 2", page.text)

    def test_renders_nested_unordered_lists(self):
        page = parse_html(NESTED_LIST_HTML, base_url="https://example.com/")

        self.assertIn("- One", page.text)
        self.assertIn("- Two", page.text)
        self.assertIn("  - Two A", page.text)

    def test_renders_links_inside_list_items(self):
        page = parse_html(LIST_WITH_LINK_HTML, base_url="https://example.com/")

        self.assertIn("- Docs [1]", page.text)
        self.assertEqual(page.links[0].href, "https://example.com/docs")

    def test_renders_inline_markup_markers(self):
        page = parse_html(INLINE_MARKUP_HTML, base_url="https://example.com/")

        self.assertIn("**curl**", page.text)
        self.assertIn("`python`", page.text)
        self.assertIn("> A note.", page.text)

    def test_detects_empty_spa_root(self):
        page = parse_html(SPA_HTML, base_url="https://app.example.com/")

        self.assertEqual(page.title, "React App")
        self.assertTrue(page.spa_warning)
        self.assertEqual(page.text, "")

    def test_deduplicates_identical_hrefs(self):
        page = parse_html(
            DUPLICATE_LINKS_HTML,
            base_url="https://example.com/",
        )

        self.assertEqual(len(page.links), 1)
        self.assertIn("Page [1]", page.text)
        self.assertEqual(page.links[0].href, "https://example.com/page")

    def test_empty_html_returns_empty_page(self):
        page = parse_html("", base_url="https://example.com")

        self.assertEqual(page.title, "")
        self.assertEqual(page.text, "")
        self.assertEqual(page.links, ())
        self.assertFalse(page.spa_warning)


if __name__ == "__main__":
    unittest.main()
