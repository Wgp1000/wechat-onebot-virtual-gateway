"""Local OCR message fingerprinting and exactly-once event suppression."""
from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path


def message_fingerprint(conversation_id: str, text: str) -> str:
    return hashlib.blake2b(f"{conversation_id}\0{text}".encode(), digest_size=16).hexdigest()


class InboundDeduper:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        with sqlite3.connect(path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS seen (fingerprint TEXT PRIMARY KEY)")

    def accept(self, fingerprint: str) -> bool:
        try:
            with sqlite3.connect(self.path) as db:
                db.execute("INSERT INTO seen (fingerprint) VALUES (?)", (fingerprint,))
            return True
        except sqlite3.IntegrityError:
            return False

    def close(self) -> None:
        return
