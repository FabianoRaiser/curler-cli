"""ANSI styling helpers for Curler Paperback."""

from __future__ import annotations

import os
import re
import sys
from typing import TextIO

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
BRIGHT_CYAN = "\033[96m"

HEADING_CODES = {
    1: (BOLD, BRIGHT_CYAN),
    2: (BOLD, CYAN),
    3: (BOLD, CYAN),
    4: (BOLD, YELLOW),
    5: (BOLD, YELLOW),
    6: (BOLD, YELLOW),
}

LINK_REF_RE = re.compile(r"(.+?) \[(\d+)\]")
MARKUP_PATTERNS = (
    (re.compile(r"\*\*(.+?)\*\*"), "bold"),
    (re.compile(r"\*(.+?)\*"), "italic"),
    (re.compile(r"`(.+?)`"), "code"),
)


class Stylizer:
    """Apply ANSI styles when enabled."""

    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled

    @classmethod
    def auto(cls, *, stream: TextIO | None = None, color: bool | None = None) -> Stylizer:
        if color is False:
            return cls(False)
        if color is True:
            return cls(True)
        if os.environ.get("NO_COLOR"):
            return cls(False)
        if stream is not None and hasattr(stream, "isatty") and not stream.isatty():
            return cls(False)
        if stream is None and hasattr(sys.stdout, "isatty") and not sys.stdout.isatty():
            return cls(False)
        return cls(True)

    def wrap(self, text: str, *codes: str) -> str:
        if not self.enabled or not text:
            return text
        return "".join(codes) + text + RESET

    def bold(self, text: str) -> str:
        return self.wrap(text, BOLD)

    def dim(self, text: str) -> str:
        return self.wrap(text, DIM)

    def italic(self, text: str) -> str:
        return self.wrap(text, ITALIC)

    def blue(self, text: str, *, underline: bool = False) -> str:
        codes = (BLUE, UNDERLINE) if underline else (BLUE,)
        return self.wrap(text, *codes)

    def yellow(self, text: str) -> str:
        return self.wrap(text, YELLOW)

    def magenta(self, text: str) -> str:
        return self.wrap(text, MAGENTA)

    def heading(self, level: int, text: str) -> str:
        if not self.enabled:
            return text
        codes = HEADING_CODES.get(min(max(level, 1), 6), (BOLD, CYAN))
        return self.wrap(text, *codes)


def strip_markup(text: str) -> str:
    """Remove temporary inline markup markers."""
    for pattern, _kind in MARKUP_PATTERNS:
        text = pattern.sub(r"\1", text)
    return text


def style_inline_markup(text: str, sty: Stylizer) -> str:
    """Style or strip bold, italic, and code markers."""
    if not sty.enabled:
        return strip_markup(text)

    for pattern, kind in MARKUP_PATTERNS:
        while True:
            match = pattern.search(text)
            if match is None:
                break
            inner = style_inline_markup(match.group(1), sty)
            if kind == "bold":
                styled = sty.bold(inner)
            elif kind == "italic":
                styled = sty.italic(inner)
            else:
                styled = sty.magenta(inner)
            text = text[: match.start()] + styled + text[match.end() :]
    return text


def style_link_refs(text: str, sty: Stylizer) -> str:
    """Color link text and [n] references."""
    if not sty.enabled:
        return text

    parts: list[str] = []
    last = 0
    for match in LINK_REF_RE.finditer(text):
        parts.append(style_inline_markup(text[last : match.start()], sty))
        link_text = match.group(1)
        number = match.group(2)
        parts.append(sty.blue(link_text, underline=True))
        parts.append(sty.blue(f" [{number}]"))
        last = match.end()
    parts.append(style_inline_markup(text[last:], sty))
    return "".join(parts)


def style_line(line: str, sty: Stylizer) -> str:
    """Apply line-level styling for headings, blockquotes, and links."""
    if not sty.enabled:
        return strip_markup(line)

    if line.startswith("> "):
        return sty.dim(style_link_refs(line, sty))

    heading_match = re.match(r"^(#{1,6}) (.*)$", line)
    if heading_match:
        level = len(heading_match.group(1))
        prefix = heading_match.group(1)
        content = style_link_refs(heading_match.group(2), sty)
        return sty.heading(level, f"{prefix} {content}")

    return style_link_refs(line, sty)


def style_text(text: str, sty: Stylizer) -> str:
    """Style a multi-line parsed page body."""
    if not text:
        return text
    if not sty.enabled:
        return strip_markup(text)
    return "\n".join(style_line(line, sty) for line in text.splitlines())
