"""Command line interface for Curler Manuscript."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence, TextIO

from . import __version__
from .fetcher import FetchError, fetch
from .formatter import format_html
from .repl import run_repl
from .url import UrlError, normalize_url


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="curler",
        description="Curler Manuscript: fetch a URL with curl and print raw HTML.",
    )
    parser.add_argument("url", nargs="?", help="URL to fetch")
    parser.add_argument(
        "--headers",
        action="store_true",
        help="print response headers instead of the body",
    )
    parser.add_argument(
        "--include-headers",
        action="store_true",
        help="print response headers followed by the body",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="print the response body with readable HTML indentation",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"curler {__version__}",
    )
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    output: TextIO = sys.stdout,
    error: TextIO = sys.stderr,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.headers and args.include_headers:
        parser.error("--headers and --include-headers cannot be used together")
    if args.headers and args.pretty:
        parser.error("--headers and --pretty cannot be used together")

    if args.url is None:
        return run_repl(output=output, error=error)

    try:
        url = normalize_url(args.url)
        result = fetch(url)
    except (UrlError, FetchError) as exc:
        print(f"curler: {exc}", file=error)
        return 1

    body = format_html(result.body) if args.pretty else result.body

    if args.headers:
        print(result.headers, end="", file=output)
    elif args.include_headers:
        print(result.headers, end="", file=output)
        print(body, end="", file=output)
    else:
        print(body, end="", file=output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
