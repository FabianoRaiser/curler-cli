"""Command line interface for Curler Paperback."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from typing import TextIO

from . import __version__
from .fetcher import FetchError, fetch
from .renderer import format_body
from .repl import run_repl
from .url import UrlError, normalize_url


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="curler",
        description="Curler Paperback: fetch a URL with curl and print a readable page.",
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
        "--raw",
        action="store_true",
        help="print the raw HTML body instead of a parsed readable page",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="print the response body with readable HTML indentation",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="disable ANSI colors in parsed output",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"curler {__version__}",
    )
    parser.add_argument(
        "-H",
        "--header",
        action="append",
        metavar="HEADER",
        help="add a request header (Name: value); repeatable "
             "Not to be confused with --headers (print response headers)",
    )
    parser.add_argument(
        "-b",
        "--cookie",
        metavar="DATA|FILE",
        help="send cookies from string (NAME=VALUE) or file (curl -b)",
    )
    parser.add_argument(
        "-c",
        "--cookie-jar",
        metavar="FILE",
        help="write cookies to file after the request (curl -c)",
    )
    parser.add_argument(
        "--jar",
        metavar="FILE",
        help="read and write cookies using the same file (-b and -c)",
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

        if args.jar and (args.cookie is not None or args.cookie_jar is not None):
            parser.error("--jar cannot be used with --cookie or --cookie-jar")

        cookie = args.cookie
        cookie_jar = args.cookie_jar
        if args.jar is not None:
            cookie = args.jar
            cookie_jar = args.jar

        result = fetch(
            url, 
            headers=args.header,
            cookie=cookie,
            cookie_jar=cookie_jar,
        )
    except (UrlError, FetchError) as exc:
        print(f"curler: {exc}", file=error)
        return 1

    body = format_body(
        result,
        raw=args.raw,
        pretty=args.pretty,
        color=False if args.no_color else None,
        output=output,
    )

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
