import unittest
from io import StringIO

from curler.fetcher import FetchResult
from curler.repl import run_repl


class ReplTest(unittest.TestCase):
    def test_repl_fetches_url_and_reprints_headers_and_raw(self):
        commands = iter(["example.com", "headers", "raw", "quit"])

        def fake_input(prompt):
            return next(commands)

        def fake_fetch(url):
            return FetchResult(url=url, headers="HTTP/2 200\n\n", body="<html>Hello</html>")

        output = StringIO()
        error = StringIO()

        code = run_repl(input_func=fake_input, output=output, error=error, fetch_func=fake_fetch)

        self.assertEqual(code, 0)
        self.assertEqual(
            output.getvalue(),
            "Curler Manuscript. Type help for commands.\n"
            "<html>Hello</html>"
            "HTTP/2 200\n\n"
            "<html>Hello</html>",
        )
        self.assertEqual(error.getvalue(), "")


    def test_repl_pretty_reprints_formatted_response(self):
        commands = iter(["example.com", "pretty", "quit"])

        def fake_input(prompt):
            return next(commands)

        def fake_fetch(url):
            return FetchResult(url=url, headers="HTTP/2 200\n\n", body="<html><body>Hello</body></html>")

        output = StringIO()
        error = StringIO()

        code = run_repl(input_func=fake_input, output=output, error=error, fetch_func=fake_fetch)

        self.assertEqual(code, 0)
        self.assertEqual(
            output.getvalue(),
            "Curler Manuscript. Type help for commands.\n"
            "<html><body>Hello</body></html>"
            "<html>\n"
            "  <body>\n"
            "    Hello\n"
            "  </body>\n"
            "</html>\n",
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
        self.assertEqual(error.getvalue(), "No response yet.\nNo response yet.\n")


if __name__ == "__main__":
    unittest.main()
