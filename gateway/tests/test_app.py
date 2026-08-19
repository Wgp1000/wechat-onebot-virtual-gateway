import asyncio
import json
import tempfile
import unittest
from pathlib import Path

import websockets

from gateway.app import GatewayService


class GatewayServiceTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.service = GatewayService(Path(self.temp_dir.name) / "gateway.sqlite3")

    async def asyncTearDown(self):
        await self.service.close()
        self.temp_dir.cleanup()

    async def test_mock_ui_event_reaches_onebot_reverse_websocket(self):
        async with self.service.reverse_websocket_server(port=0) as server:
            port = server.sockets[0].getsockname()[1]
            async with websockets.connect(f"ws://127.0.0.1:{port}") as client:
                lifecycle = json.loads(await asyncio.wait_for(client.recv(), timeout=1))
                self.assertEqual(lifecycle["meta_event_type"], "lifecycle")

                accepted = await self.service.accept_ui_event(
                    {
                        "event_id": "ui-demo-001",
                        "conversation_id": "alice",
                        "sender_id": "alice",
                        "sender_name": "Alice",
                        "text": "hello from mock ui",
                    }
                )
                self.assertTrue(accepted)

                event = json.loads(await asyncio.wait_for(client.recv(), timeout=1))
                self.assertEqual(event["post_type"], "message")
                self.assertEqual(event["message_type"], "private")
                self.assertEqual(event["raw_message"], "hello from mock ui")

    async def test_pause_rejects_ui_events_without_losing_gateway_health(self):
        await self.service.pause()
        accepted = await self.service.accept_ui_event(
            {
                "event_id": "ui-paused-001",
                "conversation_id": "alice",
                "sender_id": "alice",
                "sender_name": "Alice",
                "text": "must not publish",
            }
        )
        self.assertFalse(accepted)
        self.assertEqual(await self.service.status(), {"paused": True, "ui_events": 0})


if __name__ == "__main__":
    unittest.main()
