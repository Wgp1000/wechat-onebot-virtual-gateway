import unittest

from ui_worker.wechat_x11_driver import WeChatX11Driver


class ActiveConversationTests(unittest.TestCase):
    def test_active_mapping_skips_search_and_sends_in_current_chat(self):
        class Runner:
            def __init__(self): self.sent = []
            def open_search(self): raise AssertionError("must not search active chat")
            def type_search(self, text): raise AssertionError("must not search active chat")
            def capture_ocr(self): return ""
            def click_search_result(self, key): raise AssertionError("must not click result")
            def paste_and_send(self, text): self.sent.append(text)
        runner = Runner()
        driver = WeChatX11Driver(runner=runner)

        event_id = driver.send_text("@active", "reply")

        self.assertEqual(event_id, "wechat-outbound-1")
        self.assertEqual(runner.sent, ["reply"])


if __name__ == "__main__":
    unittest.main()
