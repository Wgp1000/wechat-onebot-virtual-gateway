"""Minimal OneBot V11 forward WebSocket event publisher."""
from __future__ import annotations

import json

import websockets
from websockets.asyncio.client import ClientConnection

from gateway.protocol_config import ForwardWebSocket


class ForwardWebSocketRuntime:
    def __init__(self, config: ForwardWebSocket) -> None:
        self.config = config
        self._connection: ClientConnection | None = None

    async def publish(self, event: dict[str, object]) -> bool:
        if not self.config.enabled or not self.config.url:
            return False
        try:
            if self._connection is None:
                self._connection = await websockets.connect(self.config.url)
            await self._connection.send(json.dumps(event, ensure_ascii=False))
            return True
        except Exception:
            await self.close()
            return False

    async def close(self) -> None:
        if self._connection is not None:
            await self._connection.close()
            self._connection = None
