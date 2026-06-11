"""URL normalization for Curler."""

from __future__ import annotations

from urllib.parse import urlparse


class UrlError(ValueError):
    """Raised when user input cannot be used as a URL."""


def normalize_url(value: str) -> str:
    """Normalize a user-provided URL for curl."""
    candidate = value.strip()
    if not candidate:
        raise UrlError("URL cannot be empty.")

    if "://" not in candidate:
        candidate = f"https://{candidate}"

    parsed = urlparse(candidate)
    if parsed.scheme not in {"http", "https"}:
        raise UrlError("Only http:// and https:// URLs are supported.")
    if not parsed.netloc:
        raise UrlError("URL must include a host.")

    return candidate
