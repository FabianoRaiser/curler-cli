import unittest

from curler.style import (
    RESET,
    Stylizer,
    strip_markup,
    style_line,
    style_link_refs,
    style_text,
)


class StylizerTest(unittest.TestCase):
    def test_disabled_returns_plain_text(self):
        sty = Stylizer(False)

        self.assertEqual(sty.blue("link"), "link")
        self.assertEqual(sty.bold("bold"), "bold")
        self.assertEqual(sty.heading(1, "# Title"), "# Title")

    def test_enabled_wraps_with_codes(self):
        sty = Stylizer(True)

        self.assertTrue(sty.blue("link").startswith("\033[34m"))
        self.assertTrue(sty.blue("link").endswith(RESET))

    def test_auto_respects_explicit_color_flag(self):
        self.assertFalse(Stylizer.auto(color=False).enabled)
        self.assertTrue(Stylizer.auto(color=True).enabled)


class StyleTextTest(unittest.TestCase):
    def test_styles_headings_and_links(self):
        sty = Stylizer(True)
        text = "# Home\nRead Docs [1]"

        output = style_text(text, sty)

        self.assertIn("\033[1m", output)
        self.assertIn("\033[34m", output)
        self.assertIn("[1]", output)

    def test_disabled_strips_markup(self):
        sty = Stylizer(False)
        text = "Use **curl** and `python`"

        self.assertEqual(style_text(text, sty), "Use curl and python")

    def test_styles_inline_markup(self):
        sty = Stylizer(True)

        output = style_link_refs("Try **curl**", sty)

        self.assertIn("\033[1m", output)
        self.assertNotIn("**", output)

    def test_styles_blockquote(self):
        sty = Stylizer(True)

        output = style_line("> quoted text", sty)

        self.assertIn("\033[2m", output)
        self.assertIn("quoted text", output)

    def test_strip_markup(self):
        self.assertEqual(strip_markup("**bold** and `code`"), "bold and code")


if __name__ == "__main__":
    unittest.main()
