"""Approved private-conversation registry for fail-closed inbound scanning."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PrivateConversation:
    conversation_id: str
    display_name: str
    search_key: str
    kind: str = "private"


@dataclass(frozen=True)
class Candidate:
    conversation_id: str
    row: int


def approved_private_candidates(registry: list[PrivateConversation], rows: list[dict[str, object]]) -> list[Candidate]:
    title_counts: dict[str, int] = {}
    for entry in registry:
        if entry.kind == "private":
            title_counts[entry.display_name] = title_counts.get(entry.display_name, 0) + 1
    unique = {entry.display_name: entry for entry in registry if entry.kind == "private" and title_counts[entry.display_name] == 1}
    candidates = []
    for row in rows:
        title = str(row.get("title", ""))
        entry = unique.get(title)
        if entry is not None:
            candidates.append(Candidate(entry.conversation_id, int(str(row["row"]))))
    return candidates
