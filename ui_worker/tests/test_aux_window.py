import unittest

from ui_worker.aux_window import classify_auxiliary_window


class AuxiliaryWindowTests(unittest.TestCase):
    def test_known_wechat_utility_overlay_is_blocking_but_safe_to_minimize(self):
        result = classify_auxiliary_window(title="wechat", window_type="utility", size=(333, 388), relation="wechat-main")
        self.assertEqual(result, "known_utility_overlay")

    def test_black_empty_weixin_window_is_safe_to_minimize_after_capture(self):
        result = classify_auxiliary_window("Weixin", "normal", (573, 427), "unknown", capture_is_blank=True)
        self.assertEqual(result, "blank_safe_overlay")

    def test_unknown_or_sensitive_overlay_requires_user(self):
        self.assertEqual(classify_auxiliary_window("Confirm", "dialog", (400, 300), "wechat-main"), "sensitive_blocking")
        self.assertEqual(classify_auxiliary_window("Weixin", "normal", (573, 427), "unknown"), "unknown_blocking")


if __name__ == "__main__":
    unittest.main()
