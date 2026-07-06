"""Navigation history for Curler Paperback."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HistoryEntry:
    url: str
    headers: str
    body: str


class History:
    """Back/forward stacks for visited pages."""

    def __init__(self) -> None:
        self._entries: list[HistoryEntry] = []
        self._index = -1

    @property
    def current(self) -> HistoryEntry | None:
        if self._index < 0:
            return None
        return self._entries[self._index]

    def push(self, entry: HistoryEntry) -> None:
        """Record a new page, discarding any forward history."""
        self._entries = self._entries[: self._index + 1]
        self._entries.append(entry)
        self._index = len(self._entries) - 1

    def can_go_back(self) -> bool:
        return self._index > 0

    def can_go_forward(self) -> bool:
        return 0 <= self._index < len(self._entries) - 1

    def back(self) -> HistoryEntry | None:
        if not self.can_go_back():
            return self.current
        self._index -= 1
        return self.current

    def forward(self) -> HistoryEntry | None:
        if not self.can_go_forward():
            return self.current
        self._index += 1
        return self.current
