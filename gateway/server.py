#!/usr/bin/env python3
"""Run the local-only OneBot V11 reverse WebSocket gateway."""
from __future__ import annotations

import asyncio
import os
from pathlib import Path

from gateway.app import GatewayService
from gateway.forward_ws import ForwardWebSocketRuntime
from gateway.protocol_config import ForwardWebSocket, ProtocolConfig, ProtocolStore, ReverseWebSocket
from gateway.ui_worker_client import UiWorkerClient


def create_service(database: Path, config_path: Path, worker_url: str = "", contacts_path: Path | None = None) -> tuple[GatewayService, ProtocolConfig]:
    config = ProtocolStore(config_path).load()
    forward = ForwardWebSocketRuntime(config.forward_ws)
    worker = UiWorkerClient(worker_url) if worker_url else None
    return GatewayService(database, forward_runtime=forward, worker_client=worker, contacts_path=contacts_path), config


async def _poll_forever(service: GatewayService, store: ProtocolStore, initial: ProtocolConfig) -> None:
    current = initial
    while True:
        try:
            await service.poll_worker_once()
            updated = store.load()
            if updated.forward_ws != current.forward_ws:
                await service.reload_forward_ws(updated.forward_ws)
                print("Forward WebSocket configuration reloaded", flush=True)
            current = updated
        except Exception as exc:
            print(f"Gateway background poll failed: {exc}", flush=True)
        await asyncio.sleep(1)


async def main() -> None:
    database = Path(os.environ.get("GATEWAY_DATABASE", "/data/gateway.sqlite3"))
    config_path = Path(os.environ.get("GATEWAY_PROTOCOL_CONFIG", "/data/protocol.json"))
    if not config_path.exists():
        fallback = ProtocolConfig(
            reverse_ws=ReverseWebSocket(
                enabled=True,
                bind_host=os.environ.get("GATEWAY_HOST", "0.0.0.0"),
                port=int(os.environ.get("GATEWAY_PORT", "16700")),
            ),
            forward_ws=ForwardWebSocket(),
        )
        ProtocolStore(config_path).save(fallback)
    contacts_path = Path(os.environ.get("CONTACTS_PATH", "/data/contacts.json"))
    service, config = create_service(database, config_path, os.environ.get("UI_WORKER_URL", ""), contacts_path)
    if not config.reverse_ws.enabled:
        raise SystemExit("reverse WebSocket is disabled; no listener configured")
    store = ProtocolStore(config_path)
    poller = asyncio.create_task(_poll_forever(service, store, config))
    try:
        async with service.reverse_websocket_server(host=config.reverse_ws.bind_host, port=config.reverse_ws.port):
            print(f"OneBot reverse WebSocket listening on {config.reverse_ws.bind_host}:{config.reverse_ws.port}", flush=True)
            await asyncio.Future()
    finally:
        poller.cancel()
        await service.close()


if __name__ == "__main__":
    asyncio.run(main())
