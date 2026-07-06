"""HTML parsing for Curler Paperback."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup, NavigableString, Tag

SPA_ROOT_IDS = frozenset({"root", "app", "__next"})
SKIP_LINK_SCHEMES = frozenset({"javascript", "mailto", "tel", "data"})
HEADING_PREFIX = {
    "h1": "# ",
    "h2": "## ",
    "h3": "### ",
    "h4": "#### ",
    "h5": "##### ",
    "h6": "###### ",
}
BLOCK_TAGS = frozenset(
    {
        "article",
        "aside",
        "div",
        "footer",
        "header",
        "main",
        "nav",
        "p",
        "section",
        "tr",
    }
)


@dataclass(frozen=True)
class ParsedLink:
    number: int
    text: str
    href: str


@dataclass(frozen=True)
class ParsedPage:
    title: str
    text: str
    links: tuple[ParsedLink, ...]
    spa_warning: bool = False


def parse_html(html: str, *, base_url: str) -> ParsedPage:
    """Parse HTML into a readable page structure."""
    soup = BeautifulSoup(html or "", "lxml")
    title = _extract_title(soup)
    text, links = _extract_text_with_links(soup, base_url=base_url)
    spa_warning = _looks_like_empty_spa(soup, text)
    return ParsedPage(title=title, text=text, links=links, spa_warning=spa_warning)


def _extract_title(soup: BeautifulSoup) -> str:
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return ""


def _resolve_link_href(anchor: Tag, *, base_url: str) -> str | None:
    href = anchor.get("href", "").strip()
    if not href or href.startswith("#"):
        return None

    parsed = urlparse(href)
    if parsed.scheme and parsed.scheme.lower() in SKIP_LINK_SCHEMES:
        return None

    return urljoin(base_url, href)


def _ordered_list_item_number(item: Tag) -> int:
    number = 1
    for sibling in item.previous_siblings:
        if isinstance(sibling, Tag) and sibling.name == "li":
            number += 1
    return number


def _extract_text_with_links(
    soup: BeautifulSoup, *, base_url: str
) -> tuple[str, tuple[ParsedLink, ...]]:
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    links: list[ParsedLink] = []
    href_to_number: dict[str, int] = {}

    def register_link(href: str, text: str) -> int:
        if href in href_to_number:
            return href_to_number[href]
        number = len(links) + 1
        href_to_number[href] = number
        links.append(ParsedLink(number=number, text=text, href=href))
        return number

    def render(
        node: Tag | NavigableString,
        parent: Tag | None = None,
        *,
        list_depth: int = 0,
    ) -> str:
        if isinstance(node, NavigableString):
            return str(node)

        if node.name in {"script", "style", "noscript"}:
            return ""

        if node.name == "a":
            href = _resolve_link_href(node, base_url=base_url)
            if href is not None:
                text = node.get_text(" ", strip=True) or href
                number = register_link(href, text)
                rendered = f"{text} [{number}]"
                if parent is not None and parent.name == "body":
                    return rendered + "\n"
                return rendered

        if node.name == "br":
            return "\n"

        if node.name in ("strong", "b"):
            inner = "".join(render(child, node) for child in node.children)
            return f"**{inner}**"

        if node.name in ("em", "i"):
            inner = "".join(render(child, node) for child in node.children)
            return f"*{inner}*"

        if node.name == "code":
            inner = "".join(render(child, node) for child in node.children)
            return f"`{inner}`"

        if node.name == "blockquote":
            inner = "".join(render(child, node) for child in node.children).strip()
            if not inner:
                return ""
            return "\n".join(f"> {part}" for part in inner.splitlines()) + "\n"

        if node.name in HEADING_PREFIX:
            rendered_children = "".join(render(child, node) for child in node.children).strip()
            if rendered_children:
                return HEADING_PREFIX[node.name] + rendered_children + "\n"
            return ""

        if node.name in {"ul", "ol"}:
            return "".join(
                render(child, node, list_depth=list_depth) for child in node.children
            )

        if node.name == "li" and parent is not None and parent.name in {"ul", "ol"}:
            line_parts: list[str] = []
            nested_parts: list[str] = []
            for child in node.children:
                if isinstance(child, Tag) and child.name in {"ul", "ol"}:
                    nested_parts.append(
                        render(child, node, list_depth=list_depth + 1)
                    )
                else:
                    line_parts.append(render(child, node, list_depth=list_depth))

            line_text = "".join(line_parts).strip()
            indent = "  " * list_depth
            if parent.name == "ul":
                marker = "- "
            else:
                marker = f"{_ordered_list_item_number(node)}. "

            rendered = ""
            if line_text:
                rendered = f"{indent}{marker}{line_text}\n"
            rendered += "".join(nested_parts)
            return rendered

        rendered_children = "".join(render(child, node) for child in node.children)

        if node.name in BLOCK_TAGS:
            rendered_children = rendered_children.strip()
            if rendered_children:
                return rendered_children + "\n"
            return ""

        if node.name == "body":
            return rendered_children

        return rendered_children

    root = soup.body or soup
    raw_text = render(root)
    lines = [line.rstrip() for line in raw_text.splitlines()]
    text = "\n".join(line for line in lines if line.strip())
    return text, tuple(links)


def _looks_like_empty_spa(soup: BeautifulSoup, text: str) -> bool:
    if len(text) > 80:
        return False

    for root_id in SPA_ROOT_IDS:
        root = soup.find(id=root_id)
        if root is None:
            continue
        if not root.get_text(strip=True):
            return True

    return False
