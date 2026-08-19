import asyncio
import json
import tempfile
import unittest
from pathlib import Path

import websockets

from gateway.app import GatewayService
from ui_worker.adapter import Adapter, InboundText, MemoryDesktopDriver
from ui_worker.bridge import publish_adapter_messages
from ui_worker.state_client import ClientState


class AdapterGatewayBridgeTests(unittest.IsolatedAsyncioTestCase):
    async def test_publishes_normalized_adapter_text_to_onebot(self):
        with tempfile.TemporaryDirectory() as directory:
            gateway = GatewayService(Path(directory) / "gateway.sqlite3")
            adapter = Adapter(
                driver=MemoryDesktopDriver([InboundText("desktop-1", "alice", "Alice", "hello from adapter")]),
                state=lambda: ClientState("logged_in_or_main_window", True),
            )
            try:
                async with gateway.reverse_websocket_server(port=0) as server:
                    port = server.sockets[0].getsockname()[1]
                    async with websockets.connect(f"ws://127.0.0.1:{port}") as client:
                        await client.recv()  # lifecycle
                        published = await publish_adapter_messages(adapter, gateway)
                        event = json.loads(await asyncio.wait_for(client.recv(), timeout=1))
                        self.assertEqual(published, 1)
                        self.assertEqual(event["raw_message"], "hello from adapter")
            finally:
                await gateway.close()


if __name__ == "__main__":
    unittest.main()
