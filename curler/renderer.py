"""Terminal rendering for Curler Paperback."""

from __future__ import annotations

from .parser import ParsedPage

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
