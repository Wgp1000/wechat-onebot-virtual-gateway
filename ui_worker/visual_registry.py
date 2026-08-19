"""Operator-approved visual identity bindings for private conversations."""
from __future__ import annotations

import json
import os
from pathlib import Path


class VisualPrivateRegistry:
    def __init__(self, path: Path) -> None:
        self.path = path

    def _load(self) -> dict[str, dict[str, str]]:
        return json.loads(self.path.read_text()) if self.path.exists() else {}

    def lookup(self, fingerprint: str) -> dict[str, str] | None:
        return self._load().get(fingerprint)

    def bind(self, user_id: str, fingerprint: str, search_key: str) -> None:
        data = self._load()
        data[fingerprint] = {"user_id": str(user_id), "search_key": search_key}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        os.replace(temporary, self.path)
