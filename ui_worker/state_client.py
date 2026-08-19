"""Read the local virtual-desktop client state before message operations."""
from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.request import urlopen


@dataclass(frozen=True)
class ClientState:
    state: str
    message_operations_ready: bool


def fetch_client_state(url: str) -> ClientState:
    with urlopen(url, timeout=3) as response:
        payload = json.loads(response.read().decode("utf-8"))
    state = str(payload.get("wechat_client_state", "unknown"))
    return ClientState(
        state=state,
        message_operations_ready=bool(payload.get("wechat_client")) and state == "logged_in_or_main_window",
    )
