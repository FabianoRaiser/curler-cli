"""End-to-end integration tests with a local HTTP server."""

import shutil
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from curler.fetcher import fetch
from curler.renderer import format_body

LOCAL_PAGE = b"""\
<!DOCTYPE html>
<html>
<head><title>Integration Test</title></head>
<body>
  <h1>Local Server</h1>
  <p>End-to-end fetch and parse.</p>
  <ul>
    <li><a href="/docs">Docs</a></li>
  </ul>
</body>
</html>
"""


class _FixtureHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(LOCAL_PAGE)

    def log_message(self, format: str, *args: object) -> None:
        return


class LocalHttpIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if shutil.which("curl") is None:
            raise unittest.SkipTest("curl is required for integration tests")
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), _FixtureHandler)
        cls.base_url = f"http://127.0.0.1:{cls.server.server_address[1]}/"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()

    def test_fetch_and_parse_local_page(self) -> None:
        result = fetch(self.base_url)
        output = format_body(result, color=False)

        self.assertEqual(result.url, self.base_url)
        self.assertIn("Integration Test", output)
        self.assertIn("# Local Server", output)
        self.assertIn("End-to-end fetch and parse.", output)
        self.assertIn("- Docs [1]", output)
        self.assertIn("(1 link)", output)

    def test_raw_mode_returns_html_from_local_server(self) -> None:
        result = fetch(self.base_url)
        raw_body = format_body(result, raw=True)

        self.assertIn("Integration Test", raw_body)
        self.assertIn("<h1>Local Server</h1>", raw_body)


if __name__ == "__main__":
    unittest.main()
