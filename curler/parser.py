"""HTML parsing for Curler Paperback."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup, NavigableString, Tag

SPA_ROOT_IDS = frozenset({"root", "app", "__next"})
SKIP_LINK_SCHEMES = frozenset({"javascript", "mailto", "tel", "data"})
BLOCK_TAGS = frozenset(
    {
        "article",
        "aside",
        "blockquote",
        "div",
        "footer",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "header",
        "li",
        "main",
        "nav",
        "ol",
        "p",
        "section",
        "tr",
        "ul",
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

    def render(node: Tag | NavigableString, parent: Tag | None = None) -> str:
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
    lines = [line.strip() for line in raw_text.splitlines()]
    text = "\n".join(line for line in lines if line)
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
