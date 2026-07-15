"""curl subprocess integration."""

from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass


class FetchError(RuntimeError):
    """Raised when curl cannot complete a request."""


@dataclass(frozen=True)
class FetchResult:
    url: str
    headers: str
    body: str


CHARSET_ALIASES = {
    "utf8": "utf-8",
    "latin1": "latin-1",
    "iso-8859-1": "latin-1",
    "iso8859-1": "latin-1",
    "windows-1252": "cp1252",
}


def build_curl_command(url: str, headers: list[str] | None = None) -> list[str]:
    """Build the curl command used by Manuscript."""
    command = ["curl", "-L", "-sS", "-D", "-", "-o", "-"]
    for header in headers or []:
        command.extend(["-H", header])
    command.append(url)
    return command


def normalize_charset(name: str) -> str:
    """Normalize a charset label from HTTP or HTML metadata."""
    cleaned = name.strip().strip("\"'").lower()
    return CHARSET_ALIASES.get(cleaned, cleaned)


def charset_from_content_type(headers: str) -> str | None:
    """Read charset from the final Content-Type header block."""
    for line in headers.splitlines():
        if line.lower().startswith("content-type:"):
            match = re.search(r"charset\s*=\s*([^\s;]+)", line, re.IGNORECASE)
            if match:
                return normalize_charset(match.group(1))
    return None


def charset_from_html_meta(body: bytes) -> str | None:
    """Sniff charset from HTML meta tags in the first few kilobytes."""
    head = body[:4096].decode("ascii", errors="ignore")
    match = re.search(
        r'<meta[^>]+charset\s*=\s*["\']?([^"\'>\s;]+)',
        head,
        re.IGNORECASE,
    )
    if match:
        return normalize_charset(match.group(1))

    match = re.search(
        r'<meta[^>]+content\s*=\s*["\'][^"\']*charset=([^"\'>\s;]+)',
        head,
        re.IGNORECASE,
    )
    if match:
        return normalize_charset(match.group(1))
    return None


def detect_body_charset(headers: str, body: bytes) -> str:
    """Pick the most likely body encoding for terminal output."""
    return charset_from_content_type(headers) or charset_from_html_meta(body) or "utf-8"


def decode_headers(value: bytes) -> str:
    """Decode HTTP headers without losing byte values."""
    return value.decode("iso-8859-1", errors="replace")


def decode_body(value: bytes, *, charset: str | None = None) -> str:
    """Decode response bodies for terminal output without crashing."""
    encoding = normalize_charset(charset) if charset else "utf-8"
    try:
        return value.decode(encoding)
    except LookupError:
        return value.decode("utf-8", errors="replace")
    except UnicodeDecodeError:
        if encoding == "utf-8":
            return value.decode("latin-1")
        return value.decode(encoding, errors="replace")


def split_headers_and_body(output: bytes) -> tuple[str, str]:
    """Split curl's combined stdout into final response headers and body."""
    marker = b"\r\n\r\n" if b"\r\n\r\n" in output else b"\n\n"
    if marker not in output:
        return "", decode_body(output)

    headers_blob, body = output.rsplit(marker, 1)
    final_headers = headers_blob.split(marker)[-1]
    headers = decode_headers(final_headers + marker)
    charset = detect_body_charset(headers, body)
    return headers, decode_body(body, charset=charset)


def fetch(url: str, headers: list[str] | None = None) -> FetchResult:
    """Fetch a URL with curl, returning headers and raw body."""
    if shutil.which("curl") is None:
        raise FetchError("curl was not found. Install curl and try again.")

    command = build_curl_command(url, headers=headers)
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
        )
    except OSError as exc:
        raise FetchError(f"Could not run curl: {exc}") from exc

    if completed.returncode != 0:
        message = decode_body(completed.stderr).strip() or "curl request failed."
        raise FetchError(message)

    response_headers, body = split_headers_and_body(completed.stdout)
    return FetchResult(url=url, headers=response_headers, body=body)
