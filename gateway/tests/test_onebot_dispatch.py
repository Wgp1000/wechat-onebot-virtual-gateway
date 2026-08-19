import asyncio
import tempfile
import unittest
from pathlib import Path

from gateway.app import GatewayService
from ui_worker.adapter import Adapter, MemoryDesktopDriver
from ui_worker.state_client import ClientState


class OneBotDispatchTests(unittest.IsolatedAsyncioTestCase):
    async def test_send_private_msg_dispatches_to_ready_adapter(self):
        driver = MemoryDesktopDriver()
        adapter = Adapter(
            driver=driver,
            state=lambda: ClientState("logged_in_or_main_window", True),
        )
        with tempfile.TemporaryDirectory() as directory:
            gateway = GatewayService(Path(directory) / "gateway.sqlite3", adapter=adapter)
            try:
                response = await gateway.handle_action(
                    "send_private_msg",
                    {"user_id": 42, "message": "[OneBot Test] hello"},
                )
            finally:
                await gateway.close()

        self.assertEqual(response["status"], "ok")
        self.assertEqual(driver.sent, [("42", "[OneBot Test] hello")])

    async def test_unsupported_message_type_stays_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            gateway = GatewayService(Path(directory) / "gateway.sqlite3")
            try:
                response = await gateway.handle_action("send_group_msg", {"group_id": 42, "message": "no"})
            finally:
                await gateway.close()

        self.assertEqual(response["retcode"], 1404)


if __name__ == "__main__":
    unittest.main()
