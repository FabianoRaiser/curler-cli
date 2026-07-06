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


if __name__ == "__main__":
    unittest.main()
