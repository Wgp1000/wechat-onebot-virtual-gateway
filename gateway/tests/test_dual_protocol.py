import asyncio
import json
import tempfile
import unittest
from pathlib import Path

import websockets

from gateway.app import GatewayService
from gateway.forward_ws import ForwardWebSocketRuntime
from gateway.protocol_config import ForwardWebSocket


class DualProtocolTests(unittest.IsolatedAsyncioTestCase):
    async def test_gateway_publishes_one_event_to_reverse_and_forward_ws(self):
        forward_events: list[dict] = []

        async def forward_handler(ws):
            forward_events.append(json.loads(await ws.recv()))

        async with websockets.serve(forward_handler, "127.0.0.1", 0) as forward_server:
            forward_port = forward_server.sockets[0].getsockname()[1]
            with tempfile.TemporaryDirectory() as directory:
                runtime = ForwardWebSocketRuntime(ForwardWebSocket(True, f"ws://127.0.0.1:{forward_port}"))
                gateway = GatewayService(Path(directory) / "gateway.sqlite3", forward_runtime=runtime)
                try:
                    async with gateway.reverse_websocket_server(port=0) as reverse_server:
                        reverse_port = reverse_server.sockets[0].getsockname()[1]
                        async with websockets.connect(f"ws://127.0.0.1:{reverse_port}") as reverse_client:
                            await reverse_client.recv()
                            await gateway.publish({"post_type": "meta_event", "meta_event_type": "heartbeat"})
                            reverse_event = json.loads(await asyncio.wait_for(reverse_client.recv(), timeout=1))
                            await asyncio.sleep(0.1)
                finally:
                    await gateway.close()

        self.assertEqual(reverse_event["meta_event_type"], "heartbeat")
        self.assertEqual(forward_events[0]["meta_event_type"], "heartbeat")


if __name__ == "__main__":
    unittest.main()
