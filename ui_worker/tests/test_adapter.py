import unittest

from ui_worker.adapter import Adapter, InboundText, MemoryDesktopDriver
from ui_worker.state_client import ClientState


class AdapterTests(unittest.TestCase):
    def test_send_is_rejected_until_client_reaches_main_window(self):
        driver = MemoryDesktopDriver()
        adapter = Adapter(driver=driver, state=lambda: ClientState("awaiting_login", False))

        with self.assertRaisesRegex(RuntimeError, "not ready"):
            adapter.send_private_text("alice", "hello")
        self.assertEqual(driver.sent, [])

    def test_send_reaches_driver_after_main_window_is_ready(self):
        driver = MemoryDesktopDriver()
        adapter = Adapter(driver=driver, state=lambda: ClientState("logged_in_or_main_window", True))

        key = adapter.send_private_text("alice", "hello")

        self.assertEqual(key, "outbound-1")
        self.assertEqual(driver.sent, [("alice", "hello")])

    def test_normalizes_inbound_text_for_gateway(self):
        driver = MemoryDesktopDriver(inbound=[InboundText("raw-1", "alice", "Alice", "hi")])
        adapter = Adapter(driver=driver, state=lambda: ClientState("logged_in_or_main_window", True))

        messages = list(adapter.poll_inbound())

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].event_id, "raw-1")
        self.assertEqual(messages[0].sender_name, "Alice")
        self.assertEqual(messages[0].text, "hi")


if __name__ == "__main__":
    unittest.main()
