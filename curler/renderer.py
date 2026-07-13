"""Terminal rendering for Curler Paperback."""

from __future__ import annotations

from typing import TextIO

from .fetcher import FetchResult
from .formatter import format_html
from .parser import ParsedPage, parse_html
from .style import Stylizer, style_text

SPA_WARNING = (
    "This page looks like a JavaScript SPA with little server-rendered content. "
    "Curler shows what the server sent — client-rendered pages are out of scope."
)


def link_count_footer(
    count: int,
    *,
    show_links_hint: bool,
    sty: Stylizer,
) -> str:
    """Format the footer showing how many links the page has."""
    if count <= 0:
        return ""
    label = "1 link" if count == 1 else f"{count} links"
    if show_links_hint:
        if not sty.enabled:
            return f"({label} — use links)"
        return (
            sty.dim("(")
            + sty.dim(f"{label} — use ")
            + sty.blue("links")
            + sty.dim(")")
        )

    plain = f"({label})"
    return sty.dim(plain) if sty.enabled else plain


def render_page(
    page: ParsedPage,
    *,
    show_links_hint: bool = False,
    stylizer: Stylizer | None = None,
) -> str:
    """Format a parsed page for terminal output."""
    sty = stylizer or Stylizer.auto()
    lines: list[str] = []

    if page.title:
        lines.extend([sty.heading(1, page.title), ""])

    if page.spa_warning:
        lines.extend([sty.yellow(SPA_WARNING), ""])

    if page.text:
        lines.extend([style_text(page.text, sty), ""])

    footer = link_count_footer(len(page.links), show_links_hint=show_links_hint, sty=sty)
    if footer:
        lines.append(footer)

    if not lines:
        return ""

    return "\n".join(lines).rstrip() + "\n"


def format_body(
    result: FetchResult,
    *,
    raw: bool = False,
    pretty: bool = False,
    show_links_hint: bool = False,
    color: bool | None = None,
    output: TextIO | None = None,
) -> str:
    """Choose parsed, raw, or pretty-printed output for a fetch result."""
    if pretty:
        return format_html(result.body)
    if raw:
        return result.body
    page = parse_html(result.body, base_url=result.url)
    sty = Stylizer.auto(stream=output, color=color)
    return render_page(page, show_links_hint=show_links_hint, stylizer=sty)
