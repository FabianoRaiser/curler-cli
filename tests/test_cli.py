import unittest
from io import StringIO
from unittest.mock import patch

import curler.cli
from curler.fetcher import FetchResult


class CliTest(unittest.TestCase):
    def test_direct_mode_prints_body(self):
        with patch(
            "curler.cli.fetch",
            return_value=FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body="<html>Hello</html>",
            ),
        ):
            output = StringIO()
            code = curler.cli.main(["example.com"], output=output, error=StringIO())

        self.assertEqual(code, 0)
        self.assertEqual(output.getvalue(), "<html>Hello</html>")

    def test_headers_mode_prints_headers(self):
        with patch(
            "curler.cli.fetch",
            return_value=FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body="<html>Hello</html>",
            ),
        ):
            output = StringIO()
            code = curler.cli.main(["--headers", "example.com"], output=output, error=StringIO())

        self.assertEqual(code, 0)
        self.assertEqual(output.getvalue(), "HTTP/2 200\n\n")

    def test_include_headers_mode_prints_headers_and_body(self):
        with patch(
            "curler.cli.fetch",
            return_value=FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body="<html>Hello</html>",
            ),
        ):
            output = StringIO()
            code = curler.cli.main(["--include-headers", "example.com"], output=output, error=StringIO())

        self.assertEqual(code, 0)
        self.assertEqual(output.getvalue(), "HTTP/2 200\n\n<html>Hello</html>")


    def test_pretty_mode_prints_formatted_body(self):
        with patch(
            "curler.cli.fetch",
            return_value=FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body="<html><body>Hello</body></html>",
            ),
        ):
            output = StringIO()
            code = curler.cli.main(["--pretty", "example.com"], output=output, error=StringIO())

        self.assertEqual(code, 0)
        self.assertEqual(
            output.getvalue(),
            "<html>\n"
            "  <body>\n"
            "    Hello\n"
            "  </body>\n"
            "</html>\n",
        )

    def test_direct_mode_reports_invalid_url(self):
        error = StringIO()

        code = curler.cli.main(["ftp://example.com"], output=StringIO(), error=error)

        self.assertEqual(code, 1)
        self.assertIn("Only http:// and https:// URLs are supported.", error.getvalue())


if __name__ == "__main__":
    unittest.main()
