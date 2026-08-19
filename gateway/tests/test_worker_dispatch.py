import asyncio
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from gateway.app import GatewayService


class WorkerDispatchTests(unittest.IsolatedAsyncioTestCase):
    async def test_send_private_uses_internal_worker_client(self):
        worker = MagicMock()
        worker.send_private.return_value = "wechat-outbound-9"
        with tempfile.TemporaryDirectory() as directory:
            gateway = GatewayService(Path(directory) / "gateway.sqlite3", worker_client=worker)
            try:
                response = await gateway.handle_action("send_private_msg", {"user_id": 42, "message": "hello"})
            finally:
                await gateway.close()

        self.assertEqual(response["status"], "ok")
        worker.send_private.assert_called_once_with("42", "hello")


if __name__ == "__main__":
    unittest.main()
