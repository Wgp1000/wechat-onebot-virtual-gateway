"""Internal UI-worker HTTP contract."""
from __future__ import annotations

from typing import Any


def handle_send_request(payload: dict[str, Any], driver: Any, contacts: Any) -> tuple[int, dict[str, Any]]:
    user_id = str(payload.get("user_id", ""))
    text = str(payload.get("text", ""))
    if not user_id or not text:
        return 400, {"error": "user_id and text are required"}
    search_key = contacts.get(user_id)
    if not search_key:
        return 404, {"error": "contact mapping not found"}
    try:
        event_id = driver.send_text(search_key, text)
    except (RuntimeError, ValueError) as exc:
        return 409, {"error": str(exc)}
    return 200, {"event_id": event_id, "user_id": user_id}
