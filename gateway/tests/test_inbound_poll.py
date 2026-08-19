import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from gateway.app import GatewayService


class InboundPollTests(unittest.IsolatedAsyncioTestCase):
    async def test_polls_worker_and_publishes_onebot_message(self):
        worker = MagicMock()
        worker.poll_inbound.return_value = [{"event_id": "evt-1", "conversation_id": "42", "sender_name": "Test", "text": "hello"}]
        with tempfile.TemporaryDirectory() as directory:
            gateway = GatewayService(Path(directory) / "gateway.sqlite3", worker_client=worker)
            events = []
            async def collect(event): events.append(event)
            gateway._publish = collect
            try:
                count = await gateway.poll_worker_once()
            finally:
                await gateway.close()

        self.assertEqual(count, 1)
        self.assertEqual(events[0]["post_type"], "message")
        self.assertEqual(events[0]["raw_message"], "hello")


if __name__ == "__main__":
    unittest.main()
