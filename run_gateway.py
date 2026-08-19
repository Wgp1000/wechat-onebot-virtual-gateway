#!/usr/bin/env python3
"""Run the OneBot V11 gateway with a mock UI event source."""

from __future__ import annotations

import asyncio
from pathlib import Path

from gateway.app import GatewayService


async def main() -> None:
    gateway = GatewayService(Path("runtime/gateway.sqlite3"))
    async with gateway.reverse_websocket_server(host="127.0.0.1", port=16700):
        print("OneBot reverse WebSocket: ws://127.0.0.1:16700")
        print("Mock UI event API is represented by gateway.accept_ui_event().")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
