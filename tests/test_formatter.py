import unittest

from curler.formatter import format_html


class FormatterTest(unittest.TestCase):
    def test_formats_nested_html_with_line_breaks(self):
        html = "<!doctype html><html><body><h1>Hello</h1><p>World</p><br></body></html>"

        self.assertEqual(
            format_html(html),
            "<!doctype html>\n"
            "<html>\n"
            "  <body>\n"
            "    <h1>\n"
            "      Hello\n"
            "    </h1>\n"
            "    <p>\n"
            "      World\n"
            "    </p>\n"
            "    <br>\n"
            "  </body>\n"
            "</html>\n",
        )

    def test_wraps_long_text(self):
        html = "<p>one two three four five six</p>"

        self.assertEqual(
            format_html(html, width=14),
            "<p>\n"
            "  one two three four\n"
            "  five six\n"
            "</p>\n",
        )


if __name__ == "__main__":
    unittest.main()
