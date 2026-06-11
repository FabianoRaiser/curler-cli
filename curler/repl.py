"""Interactive Manuscript shell."""

from __future__ import annotations

from collections.abc import Callable
import sys
from typing import TextIO

from .fetcher import FetchError, FetchResult, fetch
from .formatter import format_html
from .url import UrlError, normalize_url


HELP_TEXT = """Commands:
  <url>    Fetch a URL and print raw HTML
  headers  Show headers from the last response
  raw      Reprint the last raw HTML response
  pretty   Reprint the last response with readable HTML indentation
  help     Show this help
  quit     Exit Curler
  exit     Exit Curler
"""


InputFunc = Callable[[str], str]
FetchFunc = Callable[[str], FetchResult]


def run_repl(
    *,
    input_func: InputFunc = input,
    output: TextIO = sys.stdout,
    error: TextIO = sys.stderr,
    fetch_func: FetchFunc = fetch,
) -> int:
    """Run the Curler Manuscript REPL."""
    last_response: FetchResult | None = None
    print("Curler Manuscript. Type help for commands.", file=output)

    while True:
        try:
            command = input_func("curler> ").strip()
        except EOFError:
            print(file=output)
            return 0
        except KeyboardInterrupt:
            print(file=output)
            return 130

        if not command:
            continue
        if command in {"quit", "exit"}:
            return 0
        if command == "help":
            print(HELP_TEXT, end="", file=output)
            continue
        if command == "headers":
            if last_response is None:
                print("No response yet.", file=error)
            else:
                print(last_response.headers, end="", file=output)
            continue
        if command == "raw":
            if last_response is None:
                print("No response yet.", file=error)
            else:
                print(last_response.body, end="", file=output)
            continue
        if command == "pretty":
            if last_response is None:
                print("No response yet.", file=error)
            else:
                print(format_html(last_response.body), end="", file=output)
            continue

        try:
            url = normalize_url(command)
            last_response = fetch_func(url)
        except (UrlError, FetchError) as exc:
            print(f"curler: {exc}", file=error)
            continue

        print(last_response.body, end="", file=output)
