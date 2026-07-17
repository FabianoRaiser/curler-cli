import unittest
from io import StringIO
from unittest.mock import patch

import curler.cli
from curler.fetcher import FetchResult

SIMPLE_HTML = "<html><body>Hello</body></html>"
NESTED_HTML = "<html><body>Hello</body></html>"


class CliTest(unittest.TestCase):
    def test_direct_mode_prints_parsed_body(self):
        with patch(
            "curler.cli.fetch",
            return_value=FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body=SIMPLE_HTML,
            ),
        ):
            output = StringIO()
            code = curler.cli.main(["example.com"], output=output, error=StringIO())

        self.assertEqual(code, 0)
        self.assertEqual(output.getvalue(), "Hello\n")

    def test_raw_mode_prints_html_body(self):
        with patch(
            "curler.cli.fetch",
            return_value=FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body=SIMPLE_HTML,
            ),
        ):
            output = StringIO()
            code = curler.cli.main(
                ["--raw", "example.com"], output=output, error=StringIO()
            )

        self.assertEqual(code, 0)
        self.assertEqual(output.getvalue(), SIMPLE_HTML)

    def test_headers_mode_prints_headers(self):
        with patch(
            "curler.cli.fetch",
            return_value=FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body=SIMPLE_HTML,
            ),
        ):
            output = StringIO()
            code = curler.cli.main(
                ["--headers", "example.com"], output=output, error=StringIO()
            )

        self.assertEqual(code, 0)
        self.assertEqual(output.getvalue(), "HTTP/2 200\n\n")

    def test_include_headers_mode_prints_headers_and_body(self):
        with patch(
            "curler.cli.fetch",
            return_value=FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body=SIMPLE_HTML,
            ),
        ):
            output = StringIO()
            code = curler.cli.main(
                ["--include-headers", "example.com"], output=output, error=StringIO()
            )

        self.assertEqual(code, 0)
        self.assertEqual(output.getvalue(), "HTTP/2 200\n\nHello\n")

    def test_pretty_mode_prints_formatted_body(self):
        with patch(
            "curler.cli.fetch",
            return_value=FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body=NESTED_HTML,
            ),
        ):
            output = StringIO()
            code = curler.cli.main(
                ["--pretty", "example.com"], output=output, error=StringIO()
            )

        self.assertEqual(code, 0)
        self.assertEqual(
            output.getvalue(),
            "<html>\n  <body>\n    Hello\n  </body>\n</html>\n",
        )

    def test_no_color_disables_ansi_in_parsed_output(self):
        with patch(
            "curler.cli.fetch",
            return_value=FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body='<html><body><a href="/x">Link</a></body></html>',
            ),
        ):
            output = StringIO()
            code = curler.cli.main(
                ["--no-color", "example.com"], output=output, error=StringIO()
            )

        self.assertEqual(code, 0)
        self.assertNotIn("\033[", output.getvalue())
        self.assertIn("Link [1]", output.getvalue())

    def test_direct_mode_reports_invalid_url(self):
        error = StringIO()

        code = curler.cli.main(["ftp://example.com"], output=StringIO(), error=error)

        self.assertEqual(code, 1)
        self.assertIn("Only http:// and https:// URLs are supported.", error.getvalue())

    def test_header_flag_is_passed_to_fetch(self):
        with patch(
            "curler.cli.fetch",
            return_value=FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body=SIMPLE_HTML,
            ),
        ) as mock_fetch:
            output = StringIO()
            code = curler.cli.main(
                ["-H", "Accept: application/json", "example.com"],
                output=output,
                error=StringIO(),
            )

        self.assertEqual(code, 0)
        mock_fetch.assert_called_once_with(
            "https://example.com",
            headers=["Accept: application/json"],
            cookie=None,
            cookie_jar=None,
        )
    
    def test_multiple_header_flags_are_passed_to_fetch(self):
        with patch(
            "curler.cli.fetch",
            return_value=FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body=SIMPLE_HTML,
            ),
        ) as mock_fetch:
            output = StringIO()
            code = curler.cli.main(
                [
                    "-H", "Accept: application/json", 
                    "-H", "X-Debug: 1", 
                    "example.com"
                ],
                output=output,
                error=StringIO(),
            )

        self.assertEqual(code, 0)
        mock_fetch.assert_called_once_with(
            "https://example.com",
            headers=["Accept: application/json", "X-Debug: 1"],
            cookie=None,
            cookie_jar=None,
        )

    def test_cookie_flags_are_passed_to_fetch(self):
        with patch(
            "curler.cli.fetch",
            return_value=FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body=SIMPLE_HTML,
            ),
        ) as mock_fetch:
            code = curler.cli.main(
                [
                    "--cookie", "jar.txt",
                    "--cookie-jar", "jar.txt",
                    "example.com"
                ],
                output=StringIO(),
                error=StringIO(),
            )

        self.assertEqual(code, 0)
        mock_fetch.assert_called_once_with(
            "https://example.com",
            headers=None,
            cookie="jar.txt",
            cookie_jar="jar.txt",
        )


    def test_jar_flag_sets_cookie_and_cookie_jar(self):
        with patch("curler.cli.fetch", return_value=FetchResult(
            url="https://example.com",
            headers="HTTP/2 200\n\n",
            body=SIMPLE_HTML,
        )) as mock_fetch:
            code = curler.cli.main(
                ["--jar", "jar.txt", "example.com"],
                output=StringIO(),
                error=StringIO(),
            )

        self.assertEqual(code, 0)
        mock_fetch.assert_called_once_with(
            "https://example.com",
            headers=None,
            cookie="jar.txt",
            cookie_jar="jar.txt",
        )

    def test_jar_conflicts_with_cookie_flags(self):
        with self.assertRaises(SystemExit):
            curler.cli.main(
                ["--jar", "a.txt", "--cookie", "b.txt", "example.com"],
                output=StringIO(),
                error=StringIO(),
            )


if __name__ == "__main__":
    unittest.main()
