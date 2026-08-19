import unittest
from unittest.mock import MagicMock

from ui_worker.wechat_x11_driver import WeChatX11Driver


class WeChatX11DriverTests(unittest.TestCase):
    def test_send_requires_mapped_search_key_and_verifies_search_before_sending(self):
        runner = MagicMock()
        runner.capture_ocr.return_value = "Adapter Test Contact"
        driver = WeChatX11Driver(runner=runner)

        event_id = driver.send_text("Adapter Test Contact", "hello")

        self.assertEqual(event_id, "wechat-outbound-1")
        calls = "\n".join(str(call) for call in runner.method_calls)
        self.assertIn("open_search", calls)
        self.assertIn("Adapter Test Contact", calls)
        self.assertIn("click_search_result", calls)
        self.assertIn("paste_and_send", calls)

    def test_send_refuses_when_ocr_does_not_match_contact(self):
        runner = MagicMock()
        runner.capture_ocr.return_value = "Different contact"
        driver = WeChatX11Driver(runner=runner)

        with self.assertRaisesRegex(RuntimeError, "search verification failed"):
            driver.send_text("Adapter Test Contact", "hello")
        runner.paste_and_send.assert_not_called()


if __name__ == "__main__":
    unittest.main()
