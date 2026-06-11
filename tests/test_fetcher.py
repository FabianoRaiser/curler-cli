import unittest
from types import SimpleNamespace
from unittest.mock import patch

from curler.fetcher import FetchError, build_curl_command, fetch, split_headers_and_body


class FetcherTest(unittest.TestCase):
    def test_build_curl_command_follows_redirects_and_captures_headers(self):
        self.assertEqual(
            build_curl_command("https://example.com"),
            [
                "curl",
                "-L",
                "-sS",
                "-D",
                "-",
                "-o",
                "-",
                "https://example.com",
            ],
        )

    def test_split_headers_and_body_uses_last_header_block(self):
        output = (
            b"HTTP/1.1 301 Moved\r\nLocation: https://example.com/\r\n\r\n"
            b"HTTP/2 200\r\nContent-Type: text/html\r\n\r\n"
            b"<html>ok</html>"
        )

        headers, body = split_headers_and_body(output)

        self.assertEqual(headers, "HTTP/2 200\r\nContent-Type: text/html\r\n\r\n")
        self.assertEqual(body, "<html>ok</html>")

    def test_split_headers_and_body_replaces_invalid_utf8_body_bytes(self):
        output = b"HTTP/2 200\r\nContent-Type: text/html\r\n\r\n<html>caf\xe7</html>"

        headers, body = split_headers_and_body(output)

        self.assertEqual(headers, "HTTP/2 200\r\nContent-Type: text/html\r\n\r\n")
        self.assertEqual(body, "<html>caf�</html>")

    def test_fetch_runs_curl_and_returns_result(self):
        calls = []

        def fake_run(command, check, capture_output):
            calls.append(
                {
                    "command": command,
                    "check": check,
                    "capture_output": capture_output,
                }
            )
            return SimpleNamespace(
                returncode=0,
                stdout=b"HTTP/2 200\r\nContent-Type: text/html\r\n\r\n<body>Hello</body>",
                stderr=b"",
            )

        with patch("curler.fetcher.shutil.which", return_value="/usr/bin/curl"):
            with patch("curler.fetcher.subprocess.run", side_effect=fake_run):
                result = fetch("https://example.com")

        self.assertEqual(
            calls,
            [
                {
                    "command": build_curl_command("https://example.com"),
                    "check": False,
                    "capture_output": True,
                }
            ],
        )
        self.assertEqual(result.headers, "HTTP/2 200\r\nContent-Type: text/html\r\n\r\n")
        self.assertEqual(result.body, "<body>Hello</body>")

    def test_fetch_raises_when_curl_is_missing(self):
        with patch("curler.fetcher.shutil.which", return_value=None):
            with self.assertRaisesRegex(FetchError, "curl was not found"):
                fetch("https://example.com")

    def test_fetch_raises_when_curl_fails(self):
        completed = SimpleNamespace(returncode=6, stdout=b"", stderr=b"Could not resolve host")
        with patch("curler.fetcher.shutil.which", return_value="/usr/bin/curl"):
            with patch("curler.fetcher.subprocess.run", return_value=completed):
                with self.assertRaisesRegex(FetchError, "Could not resolve host"):
                    fetch("https://missing.example")


if __name__ == "__main__":
    unittest.main()
