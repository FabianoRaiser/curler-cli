"""Readable HTML formatting for Manuscript."""

from __future__ import annotations

from html import escape
from html.parser import HTMLParser
import textwrap


VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


class PrettyHTMLFormatter(HTMLParser):
    """Format HTML with indentation and readable line breaks."""

    def __init__(self, *, indent_width: int = 2, width: int = 100) -> None:
        super().__init__(convert_charrefs=False)
        self.indent_width = indent_width
        self.width = width
        self.level = 0
        self.lines: list[str] = []

    def format(self, html: str) -> str:
        self.feed(html)
        self.close()
        return "\n".join(line for line in self.lines if line.strip()) + "\n"

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._emit(self.get_starttag_text() or self._render_start_tag(tag, attrs))
        if tag.lower() not in VOID_ELEMENTS:
            self.level += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._emit(
            self.get_starttag_text() or f"{self._render_start_tag(tag, attrs)[:-1]} />"
        )

    def handle_endtag(self, tag: str) -> None:
        self.level = max(0, self.level - 1)
        self._emit(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if not text:
            return

        available_width = max(20, self.width - (self.level * self.indent_width))
        for line in textwrap.wrap(text, width=available_width, break_long_words=False):
            self._emit(line)

    def handle_entityref(self, name: str) -> None:
        self._emit(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self._emit(f"&#{name};")

    def handle_comment(self, data: str) -> None:
        self._emit(f"<!--{data}-->")

    def handle_decl(self, decl: str) -> None:
        self._emit(f"<!{decl}>")

    def handle_pi(self, data: str) -> None:
        self._emit(f"<?{data}>")

    def unknown_decl(self, data: str) -> None:
        self._emit(f"<![{data}]>")

    def _emit(self, value: str) -> None:
        self.lines.append(f"{self._indent()}{value}")

    def _indent(self) -> str:
        return " " * (self.level * self.indent_width)

    def _render_start_tag(self, tag: str, attrs: list[tuple[str, str | None]]) -> str:
        if not attrs:
            return f"<{tag}>"

        rendered_attrs = []
        for name, value in attrs:
            if value is None:
                rendered_attrs.append(name)
            else:
                rendered_attrs.append(f'{name}="{escape(value, quote=True)}"')
        return f"<{tag} {' '.join(rendered_attrs)}>"


def format_html(html: str, *, indent_width: int = 2, width: int = 100) -> str:
    """Return a readable representation of raw HTML."""
    if not html:
        return ""
    return PrettyHTMLFormatter(indent_width=indent_width, width=width).format(html)
