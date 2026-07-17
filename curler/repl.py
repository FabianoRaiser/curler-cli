"""Interactive Paperback shell."""

from __future__ import annotations

import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import TextIO

from .fetcher import FetchError, FetchResult, fetch
from .formatter import format_html
from .history import History, HistoryEntry
from .parser import parse_html
from .renderer import format_body
from .url import UrlError, normalize_url

HELP_TEXT = """Commands:
  <url>             Fetch a URL and print a readable page
  go <n>            Follow link number N from the current page
  links             List links on the current page
  back              Go back in history
  forward           Go forward in history
  headers           Show headers from the current page
  raw               Reprint the raw HTML of the current page
  pretty            Reprint the current page with readable HTML indentation
  cookies           Show cookies in the session jar
  clear-cookies     Clear the session cookie jar
  help              Show this help
  quit              Exit Curler
  exit              Exit Curler
"""


InputFunc = Callable[[str], str]
FetchFunc = Callable[[str], FetchResult]


PAGE_NOT_LOADED = "No page loaded."


def _session_jar(cookie_jar: str | None) -> tuple[str, bool]:
    """Return (path, owned). owned=True means we created a temp file."""
    if cookie_jar is not None:
        return cookie_jar, False
    tmp = tempfile.NamedTemporaryFile(
        prefix="curler-cookies-",
        suffix=".txt",
        delete=False,
    )
    tmp.close()
    return tmp.name, True


def _cleanup_jar(jar_path: str, owned: bool) -> None:
    if owned:
        Path(jar_path).unlink(missing_ok=True)


def _require_page(history: History, error: TextIO) -> HistoryEntry | None:
    entry = history.current
    if entry is None:
        print(PAGE_NOT_LOADED, file=error)
    return entry


def _cmd_help(*, output: TextIO) -> None:
    print(HELP_TEXT, end="", file=output)


def _cmd_headers(history: History, output: TextIO, error: TextIO) -> None:
    entry = _require_page(history, error)
    if entry is not None:
        print(entry.headers, end="", file=output)


def _cmd_raw(history: History, output: TextIO, error: TextIO) -> None:
    entry = _require_page(history, error)
    if entry is not None:
        print(entry.body, end="", file=output)


def _cmd_pretty(history: History, output: TextIO, error: TextIO) -> None:
    entry = _require_page(history, error)
    if entry is not None:
        print(format_html(entry.body), end="", file=output)


def _cmd_links(current_page, output: TextIO, error: TextIO) -> None:
    page = current_page()
    if page is None:
        print(PAGE_NOT_LOADED, file=error)
        return
    if not page.links:
        print("No links found.", file=output)
        return
    for link in page.links:
        print(f"  [{link.number}] {link.text} ({link.href})", file=output)


def _cmd_go(command, current_page, do_fetch, push_result, error: TextIO) -> None:
    page = current_page()
    if page is None:
        print(PAGE_NOT_LOADED, file=error)
        return
    try:
        number = int(command.split(maxsplit=1)[1])
    except (IndexError, ValueError):
        print("Usage: go <n>", file=error)
        return
    link = next((item for item in page.links if item.number == number), None)
    if link is None:
        print(f"Link {number} not found.", file=error)
        return
    try:
        result = do_fetch(link.href)
    except (UrlError, FetchError) as exc:
        print(f"curler: {exc}", file=error)
        return
    push_result(result)


def _cmd_back(history: History, show_parsed, error: TextIO) -> None:
    if not history.can_go_back():
        print("No previous page.", file=error)
        return
    history.back()
    show_parsed()


def _cmd_forward(history: History, show_parsed, error: TextIO) -> None:
    if not history.can_go_forward():
        print("No next page.", file=error)
        return
    history.forward()
    show_parsed()


def _cmd_fetch_url(
    command: str,
    *,
    do_fetch: FetchFunc,
    push_result: Callable[[FetchResult], None],
    error: TextIO,
) -> None:
    try:
        url = normalize_url(command)
        result = do_fetch(url)
    except (UrlError, FetchError) as exc:
        print(f"curler: {exc}", file=error)
        return
    push_result(result)


def _cmd_cookies(jar_path: str, output: TextIO) -> None:
    path = Path(jar_path)
    if not path.exists() or path.stat().st_size == 0:
        print("No cookies.", file=output)
        return
    print(path.read_text(), end="", file=output)


def _cmd_clear_cookies(jar_path: str, output: TextIO) -> None:
    Path(jar_path).write_text("")
    print("Cookies cleared.", file=output)


def run_repl(
    *,
    input_func: InputFunc = input,
    output: TextIO = sys.stdout,
    error: TextIO = sys.stderr,
    fetch_func: FetchFunc | None = None,
    cookie_jar: str | None = None,
) -> int:
    """Run the Curler Paperback REPL."""
    history = History()
    jar_path, jar_owned = _session_jar(cookie_jar)
    do_fetch = fetch_func or (
        lambda url: fetch(url, cookie=jar_path, cookie_jar=jar_path)
    )
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
        print(format_body(result, show_links_hint=True, output=output), end="", file=output)

    def push_result(result: FetchResult) -> None:
        history.push(
            HistoryEntry(url=result.url, headers=result.headers, body=result.body)
        )
        show_parsed()


    simple = {
        "help": lambda: _cmd_help(output=output),
        "headers": lambda: _cmd_headers(history, output, error),
        "raw": lambda: _cmd_raw(history, output, error),
        "pretty": lambda: _cmd_pretty(history, output, error),
        "links": lambda: _cmd_links(current_page, output, error),
        "back": lambda: _cmd_back(history, show_parsed, error),
        "forward": lambda: _cmd_forward(history, show_parsed, error),
        "cookies": lambda: _cmd_cookies(jar_path, output),
        "clear-cookies": lambda: _cmd_clear_cookies(jar_path, output),
    }

    try:
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
            if command in simple:
                simple[command]()
                continue
            if command.startswith("go "):
                _cmd_go(command, current_page, do_fetch, push_result, error)
                continue
            _cmd_fetch_url(command, do_fetch=do_fetch, push_result=push_result, error=error)
    finally:
        _cleanup_jar(jar_path, jar_owned)
