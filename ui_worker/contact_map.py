"""Persistent deterministic OneBot user ID to WeChat search-key mappings."""
from __future__ import annotations

import json
import os
from pathlib import Path


class ContactMapStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def _load(self) -> dict[str, str]:
        if not self.path.exists():
            return {}
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return {str(key): str(value) for key, value in data.items()}

    def get(self, onebot_user_id: str) -> str | None:
        return self._load().get(str(onebot_user_id))

    def set(self, onebot_user_id: str, wechat_search_key: str) -> None:
        if not onebot_user_id or not wechat_search_key:
            raise ValueError("onebot_user_id and wechat_search_key are required")
        data = self._load()
        data[str(onebot_user_id)] = wechat_search_key
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(".tmp")
        temp.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temp, self.path)
