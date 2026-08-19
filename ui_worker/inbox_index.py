"""Persisted, safe inbox ordering model for deterministic WeChat polling."""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path


class InboxSafetyError(ValueError):
    pass


@dataclass(frozen=True)
class ConversationEntry:
    display_name: str
    search_key: str
    pinned: bool = False
    collapsed: bool = False


@dataclass
class InboxIndex:
    entries: list[ConversationEntry]

    @classmethod
    def from_scan(cls, entries: list[ConversationEntry]) -> "InboxIndex":
        if any(entry.pinned for entry in entries):
            raise InboxSafetyError("pinned conversations disable ordered inbox mode")
        if any(entry.collapsed for entry in entries):
            raise InboxSafetyError("collapsed conversations disable ordered inbox mode")
        if not entries:
            raise InboxSafetyError("conversation directory is empty")
        return cls(entries)

    def first_active(self) -> ConversationEntry:
        return self.entries[0]

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps([asdict(entry) for entry in self.entries], ensure_ascii=False, indent=2))
        os.replace(temporary, path)

    @classmethod
    def load(cls, path: Path) -> "InboxIndex":
        entries = [ConversationEntry(**row) for row in json.loads(path.read_text())]
        return cls.from_scan(entries)
