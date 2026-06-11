"""curl subprocess integration."""

from __future__ import annotations

from dataclasses import dataclass
import shutil
import subprocess


class FetchError(RuntimeError):
    """Raised when curl cannot complete a request."""


@dataclass(frozen=True)
class FetchResult:
    url: str
    headers: str
    body: str


def build_curl_command(url: str) -> list[str]:
    """Build the curl command used by Manuscript."""
    return [
        "curl",
        "-L",
        "-sS",
        "-D",
        "-",
        "-o",
        "-",
        url,
    ]


def decode_headers(value: bytes) -> str:
    """Decode HTTP headers without losing byte values."""
    return value.decode("iso-8859-1", errors="replace")


def decode_body(value: bytes) -> str:
    """Decode response bodies for terminal output without crashing."""
    return value.decode("utf-8", errors="replace")


def split_headers_and_body(output: bytes) -> tuple[str, str]:
    """Split curl's combined stdout into final response headers and body."""
    marker = b"\r\n\r\n" if b"\r\n\r\n" in output else b"\n\n"
    if marker not in output:
        return "", decode_body(output)

    headers_blob, body = output.rsplit(marker, 1)
    final_headers = headers_blob.split(marker)[-1]
    return decode_headers(final_headers + marker), decode_body(body)


def fetch(url: str) -> FetchResult:
    """Fetch a URL with curl, returning headers and raw body."""
    if shutil.which("curl") is None:
        raise FetchError("curl was not found. Install curl and try again.")

    command = build_curl_command(url)
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

    headers, body = split_headers_and_body(completed.stdout)
    return FetchResult(url=url, headers=headers, body=body)
