"""HTML parsing for Curler Paperback."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

SPA_ROOT_IDS = frozenset({"root", "app", "__next"})
SKIP_LINK_SCHEMES = frozenset({"javascript", "mailto", "tel", "data"})


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
    text = _extract_text(soup)
    links = _extract_links(soup, base_url=base_url)
    spa_warning = _looks_like_empty_spa(soup, text)
    return ParsedPage(title=title, text=text, links=links, spa_warning=spa_warning)


def _extract_title(soup: BeautifulSoup) -> str:
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return ""


def _extract_text(soup: BeautifulSoup) -> str:
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    body = soup.body or soup
    chunks = [line.strip() for line in body.get_text("\n", strip=True).splitlines()]
    return "\n".join(line for line in chunks if line)


def _extract_links(soup: BeautifulSoup, *, base_url: str) -> tuple[ParsedLink, ...]:
    links: list[ParsedLink] = []
    seen: set[str] = set()

    for anchor in soup.find_all("a", href=True):
        href = anchor.get("href", "").strip()
        if not href or href.startswith("#"):
            continue

        parsed = urlparse(href)
        if parsed.scheme and parsed.scheme.lower() in SKIP_LINK_SCHEMES:
            continue

        absolute_href = urljoin(base_url, href)
        if absolute_href in seen:
            continue
        seen.add(absolute_href)

        text = anchor.get_text(" ", strip=True) or absolute_href
        links.append(ParsedLink(number=len(links) + 1, text=text, href=absolute_href))

    return tuple(links)


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
