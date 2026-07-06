"""Interactive Paperback shell."""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import TextIO

from .fetcher import FetchError, FetchResult, fetch
from .formatter import format_html
from .history import History, HistoryEntry
from .parser import parse_html
from .renderer import format_body
from .url import UrlError, normalize_url

HELP_TEXT = """Commands:
  <url>       Fetch a URL and print a readable page
  go <n>      Follow link number N from the current page
  links       List links on the current page
  back        Go back in history
  forward     Go forward in history
  headers     Show headers from the current page
  raw         Reprint the raw HTML of the current page
  pretty      Reprint the current page with readable HTML indentation
  help        Show this help
  quit        Exit Curler
  exit        Exit Curler
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
    """Run the Curler Paperback REPL."""
    history = History()
    print("Curler Paperback. Type help for commands.", file=output)

    def current_page():
        entry = history.current
        if entry is None:
            return None
        return parse_html(entry.body, base_url=entry.url)

    def show_parsed() -> None:
        entry = history.current
        if entry is None:
            return
        result = FetchResult(url=entry.url, headers=entry.headers, body=entry.body)
        print(format_body(result), end="", file=output)

    def push_result(result: FetchResult) -> None:
        history.push(
            HistoryEntry(url=result.url, headers=result.headers, body=result.body)
        )
        show_parsed()

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
            if history.current is None:
                print("No page loaded.", file=error)
            else:
                print(history.current.headers, end="", file=output)
            continue
        if command == "raw":
            if history.current is None:
                print("No page loaded.", file=error)
            else:
                print(history.current.body, end="", file=output)
            continue
        if command == "pretty":
            if history.current is None:
                print("No page loaded.", file=error)
            else:
                print(format_html(history.current.body), end="", file=output)
            continue
        if command == "links":
            page = current_page()
            if page is None:
                print("No page loaded.", file=error)
                continue
            if not page.links:
                print("No links found.", file=output)
                continue
            for link in page.links:
                print(f"  [{link.number}] {link.text} ({link.href})", file=output)
            continue
        if command == "back":
            if not history.can_go_back():
                print("No previous page.", file=error)
                continue
            history.back()
            show_parsed()
            continue
        if command == "forward":
            if not history.can_go_forward():
                print("No next page.", file=error)
                continue
            history.forward()
            show_parsed()
            continue
        if command.startswith("go "):
            page = current_page()
            if page is None:
                print("No page loaded.", file=error)
                continue
            try:
                number = int(command.split(maxsplit=1)[1])
            except (IndexError, ValueError):
                print("Usage: go <n>", file=error)
                continue
            link = next((item for item in page.links if item.number == number), None)
            if link is None:
                print(f"Link {number} not found.", file=error)
                continue
            try:
                result = fetch_func(link.href)
            except (UrlError, FetchError) as exc:
                print(f"curler: {exc}", file=error)
                continue
            push_result(result)
            continue

        try:
            url = normalize_url(command)
            result = fetch_func(url)
        except (UrlError, FetchError) as exc:
            print(f"curler: {exc}", file=error)
            continue

        push_result(result)
