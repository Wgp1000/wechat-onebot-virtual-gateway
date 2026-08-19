"""Conservative two-snapshot inbox candidate detection."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConversationRow:
    display_name: str
    search_key: str
    preview: str
    timestamp: str
    unread: bool = False
    pinned: bool = False
    collapsed: bool = False


@dataclass(frozen=True)
class InboxSnapshot:
    rows: list[ConversationRow]


def newly_active_conversations(before: InboxSnapshot, after: InboxSnapshot) -> list[ConversationRow]:
    previous = {row.search_key: row for row in before.rows}
    candidates = []
    for row in after.rows:
        old = previous.get(row.search_key)
        changed = old is None or (old.preview, old.timestamp) != (row.preview, row.timestamp)
        if changed and row.unread and not row.pinned and not row.collapsed:
            candidates.append(row)
    return candidates
