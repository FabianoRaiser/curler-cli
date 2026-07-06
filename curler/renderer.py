"""Terminal rendering for Curler Paperback."""

from __future__ import annotations

from .fetcher import FetchResult
from .formatter import format_html
from .parser import ParsedPage, parse_html

SPA_WARNING = (
    "This page looks like a JavaScript SPA with little server-rendered content. "
    "Try Stagecraft or Blockbuster for full browser rendering."
)


def link_count_footer(count: int, *, show_links_hint: bool) -> str:
    """Format the footer showing how many links the page has."""
    if count <= 0:
        return ""
    label = "1 link" if count == 1 else f"{count} links"
    if show_links_hint:
        return f"({label} — use links)"
    return f"({label})"


def render_page(page: ParsedPage, *, show_links_hint: bool = False) -> str:
    """Format a parsed page for terminal output."""
    lines: list[str] = []

    if page.title:
        lines.extend([page.title, ""])

    if page.spa_warning:
        lines.extend([SPA_WARNING, ""])

    if page.text:
        lines.extend([page.text, ""])

    footer = link_count_footer(len(page.links), show_links_hint=show_links_hint)
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
) -> str:
    """Choose parsed, raw, or pretty-printed output for a fetch result."""
    if pretty:
        return format_html(result.body)
    if raw:
        return result.body
    page = parse_html(result.body, base_url=result.url)
    return render_page(page, show_links_hint=show_links_hint)
