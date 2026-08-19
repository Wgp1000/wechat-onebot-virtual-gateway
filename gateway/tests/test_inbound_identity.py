import tempfile
import unittest
from pathlib import Path

from gateway.app import GatewayService


class InboundIdentityTests(unittest.IsolatedAsyncioTestCase):
    async def test_numeric_worker_conversation_id_becomes_onebot_user_id(self):
        with tempfile.TemporaryDirectory() as directory:
            gateway = GatewayService(Path(directory) / "gateway.sqlite3")
            events = []
            async def collect(event): events.append(event)
            gateway._publish = collect
            try:
                await gateway.accept_ui_event({"event_id": "id-1", "conversation_id": "12345", "sender_id": "12345", "sender_name": "active", "text": "hello"})
            finally:
                await gateway.close()

        self.assertEqual(events[0]["user_id"], 12345)


if __name__ == "__main__":
    unittest.main()
