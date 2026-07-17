import unittest
from io import StringIO

from curler.fetcher import FetchResult
from curler.repl import run_repl

HOME_HTML = """\
<html><head><title>Home</title></head><body>
<p>Welcome</p>
<a href="https://example.com/about">About</a>
</body></html>
"""
ABOUT_HTML = """\
<html><head><title>About</title></head><body><p>About us</p></body></html>
"""


class ReplTest(unittest.TestCase):
    def test_repl_fetches_url_and_reprints_headers_and_raw(self):
        commands = iter(["example.com", "headers", "raw", "quit"])

        def fake_input(prompt):
            return next(commands)

        def fake_fetch(url):
            return FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body=HOME_HTML,
            )

        output = StringIO()
        error = StringIO()

        code = run_repl(
            input_func=fake_input, output=output, error=error, fetch_func=fake_fetch
        )

        self.assertEqual(code, 0)
        self.assertIn("Curler Paperback.", output.getvalue())
        self.assertIn("Home", output.getvalue())
        self.assertIn("Welcome", output.getvalue())
        self.assertIn("About [1]", output.getvalue())
        self.assertIn("(1 link — use links)", output.getvalue())
        self.assertIn("HTTP/2 200", output.getvalue())
        self.assertIn(HOME_HTML, output.getvalue())
        self.assertEqual(error.getvalue(), "")

    def test_repl_pretty_reprints_formatted_response(self):
        commands = iter(["example.com", "pretty", "quit"])

        def fake_input(prompt):
            return next(commands)

        def fake_fetch(url):
            return FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body="<html><body>Hello</body></html>",
            )

        output = StringIO()
        error = StringIO()

        code = run_repl(
            input_func=fake_input, output=output, error=error, fetch_func=fake_fetch
        )

        self.assertEqual(code, 0)
        self.assertIn(
            "<html>\n  <body>\n    Hello\n  </body>\n</html>\n",
            output.getvalue(),
        )
        self.assertEqual(error.getvalue(), "")

    def test_repl_reports_missing_previous_response(self):
        commands = iter(["headers", "raw", "exit"])

        def fake_input(prompt):
            return next(commands)

        output = StringIO()
        error = StringIO()

        code = run_repl(input_func=fake_input, output=output, error=error)

        self.assertEqual(code, 0)
        self.assertEqual(
            error.getvalue(),
            "No page loaded.\nNo page loaded.\n",
        )

    def test_repl_lists_links(self):
        commands = iter(["example.com", "links", "quit"])

        def fake_input(prompt):
            return next(commands)

        def fake_fetch(url):
            return FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body=HOME_HTML,
            )

        output = StringIO()
        error = StringIO()

        run_repl(input_func=fake_input, output=output, error=error, fetch_func=fake_fetch)

        self.assertIn("[1] About (https://example.com/about)", output.getvalue())
        self.assertEqual(error.getvalue(), "")

    def test_repl_follows_link_with_go(self):
        commands = iter(["example.com", "go 1", "quit"])

        def fake_input(prompt):
            return next(commands)

        def fake_fetch(url):
            if url == "https://example.com":
                return FetchResult(
                    url="https://example.com",
                    headers="HTTP/2 200\n\n",
                    body=HOME_HTML,
                )
            return FetchResult(
                url="https://example.com/about",
                headers="HTTP/2 200\n\n",
                body=ABOUT_HTML,
            )

        output = StringIO()
        error = StringIO()

        run_repl(input_func=fake_input, output=output, error=error, fetch_func=fake_fetch)

        self.assertIn("About us", output.getvalue())
        self.assertEqual(error.getvalue(), "")

    def test_repl_navigates_back_and_forward(self):
        commands = iter(["example.com", "go 1", "back", "forward", "quit"])

        def fake_input(prompt):
            return next(commands)

        def fake_fetch(url):
            if url == "https://example.com":
                return FetchResult(
                    url="https://example.com",
                    headers="HTTP/2 200\n\n",
                    body=HOME_HTML,
                )
            return FetchResult(
                url="https://example.com/about",
                headers="HTTP/2 200\n\n",
                body=ABOUT_HTML,
            )

        output = StringIO()
        error = StringIO()

        run_repl(input_func=fake_input, output=output, error=error, fetch_func=fake_fetch)

        self.assertGreaterEqual(output.getvalue().count("Welcome"), 2)
        self.assertGreaterEqual(output.getvalue().count("About us"), 2)
        self.assertEqual(error.getvalue(), "")

    def test_repl_back_at_start_reports_error(self):
        commands = iter(["example.com", "back", "quit"])

        def fake_input(prompt):
            return next(commands)

        def fake_fetch(url):
            return FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body=HOME_HTML,
            )

        output = StringIO()
        error = StringIO()

        run_repl(input_func=fake_input, output=output, error=error, fetch_func=fake_fetch)

        self.assertIn("No previous page.", error.getvalue())

    def test_repl_forward_at_end_reports_error(self):
        commands = iter(["example.com", "forward", "quit"])

        def fake_input(prompt):
            return next(commands)

        def fake_fetch(url):
            return FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body=HOME_HTML,
            )

        output = StringIO()
        error = StringIO()

        run_repl(input_func=fake_input, output=output, error=error, fetch_func=fake_fetch)

        self.assertIn("No next page.", error.getvalue())

    def test_repl_go_with_invalid_link_reports_error(self):
        commands = iter(["example.com", "go 99", "quit"])

        def fake_input(prompt):
            return next(commands)

        def fake_fetch(url):
            return FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body=HOME_HTML,
            )

        output = StringIO()
        error = StringIO()

        run_repl(input_func=fake_input, output=output, error=error, fetch_func=fake_fetch)

        self.assertIn("Link 99 not found.", error.getvalue())

    def test_repl_go_without_page_reports_error(self):
        commands = iter(["go 1", "quit"])

        def fake_input(prompt):
            return next(commands)

        output = StringIO()
        error = StringIO()

        run_repl(input_func=fake_input, output=output, error=error)

        self.assertIn("No page loaded.", error.getvalue())

    def test_repl_links_without_page_reports_error(self):
        commands = iter(["links", "quit"])

        def fake_input(prompt):
            return next(commands)

        output = StringIO()
        error = StringIO()

        run_repl(input_func=fake_input, output=output, error=error)

        self.assertIn("No page loaded.", error.getvalue())

    def test_repl_reports_no_links_on_empty_page(self):
        commands = iter(["example.com", "links", "quit"])

        def fake_input(prompt):
            return next(commands)

        def fake_fetch(url):
            return FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body="<html><body><p>No links here</p></body></html>",
            )

        output = StringIO()
        error = StringIO()

        run_repl(input_func=fake_input, output=output, error=error, fetch_func=fake_fetch)

        self.assertIn("No links found.", output.getvalue())
        self.assertEqual(error.getvalue(), "")

    def test_repl_cookies_and_clear_cookies(self):
        import tempfile
        from pathlib import Path

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
            tmp.write("# Netscape cookie file\nexample.com\tTRUE\t/\tFALSE\t0\tsession\tabc\n")
            jar = tmp.name

        commands = iter(["cookies", "clear-cookies", "cookies", "quit"])

        def fake_input(prompt):
            return next(commands)

        def fake_fetch(url):
            return FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body=HOME_HTML,
            )

        output = StringIO()
        try:
            code = run_repl(
                input_func=fake_input,
                output=output,
                error=StringIO(),
                fetch_func=fake_fetch,
                cookie_jar=jar,
            )
        finally:
            Path(jar).unlink(missing_ok=True)

        self.assertEqual(code, 0)
        text = output.getvalue()
        self.assertIn("session", text)
        self.assertIn("Cookies cleared.", text)
        self.assertIn("No cookies.", text)


    def test_repl_default_fetch_uses_cookie_jar(self):
        from unittest.mock import patch
        commands = iter(["example.com", "quit"])
        with patch("curler.repl.fetch") as mock_fetch:
            mock_fetch.return_value = FetchResult(
                url="https://example.com",
                headers="HTTP/2 200\n\n",
                body=HOME_HTML,
            )
            run_repl(
                input_func=lambda p: next(commands),
                output=StringIO(),
                error=StringIO(),
                cookie_jar="/tmp/curler-test-jar.txt",
            )
        mock_fetch.assert_called_once_with(
            "https://example.com",
            cookie="/tmp/curler-test-jar.txt",
            cookie_jar="/tmp/curler-test-jar.txt",
        )


if __name__ == "__main__":
    unittest.main()
