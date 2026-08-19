"""Internal client for the deterministic virtual-desktop UI worker."""
from __future__ import annotations

import json
from urllib.request import Request, urlopen


class UiWorkerClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def poll_inbound(self) -> list[dict[str, str]]:
        with urlopen(f"{self.base_url}/v1/poll-inbound", timeout=20) as response:
            return list(json.loads(response.read().decode()).get("messages", []))

    def send_private(self, user_id: str, text: str) -> str:
        payload = json.dumps({"user_id": user_id, "text": text}).encode()
        request = Request(
            f"{self.base_url}/v1/send-private",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=10) as response:
            body = json.loads(response.read().decode())
        return str(body["event_id"])
