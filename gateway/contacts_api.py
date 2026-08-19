"""OneBot contact-directory projection from configured UI mappings."""
from __future__ import annotations

import json
from pathlib import Path


def friend_list(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    contacts = json.loads(path.read_text(encoding="utf-8"))
    return [
        {"user_id": int(user_id), "nickname": str(search_key)}
        for user_id, search_key in sorted(contacts.items(), key=lambda item: int(item[0]))
        if str(user_id).isdecimal()
    ]
