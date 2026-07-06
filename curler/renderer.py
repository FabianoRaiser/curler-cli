"""Terminal rendering for Curler Paperback."""

from __future__ import annotations

from .fetcher import FetchResult
from .formatter import format_html
from .parser import ParsedPage, parse_html

SPA_WARNING = (
    "This page looks like a JavaScript SPA with little server-rendered content. "
    "Try Stagecraft or Blockbuster for full browser rendering."
)


def render_page(page: ParsedPage) -> str:
    """Format a parsed page for terminal output."""
    lines: list[str] = []

    if page.title:
        lines.extend([page.title, ""])

    if page.spa_warning:
        lines.extend([SPA_WARNING, ""])

    if page.text:
        lines.extend([page.text, ""])

    if page.links:
        lines.append("Links:")
        for link in page.links:
            lines.append(f"  [{link.number}] {link.text} ({link.href})")

    if not lines:
        return ""

    return "\n".join(lines).rstrip() + "\n"


def format_body(result: FetchResult, *, raw: bool = False, pretty: bool = False) -> str:
    """Choose parsed, raw, or pretty-printed output for a fetch result."""
    if pretty:
        return format_html(result.body)
    if raw:
        return result.body
    return render_page(parse_html(result.body, base_url=result.url))
