import unittest

from panel.x11_state import classify_client_state


class X11StateTests(unittest.TestCase):
    def test_small_original_login_window_is_awaiting_login(self):
        windows = ['0x1 "Weixin": ("wechat" "wechat")  292x396+0+0  +494+202']
        self.assertEqual(classify_client_state(windows), "awaiting_login")

    def test_large_weixin_main_window_is_logged_in(self):
        windows = [
            '0x1 "Weixin": ("wechat" "wechat")  573x427+0+0  +352+185',
            '0x2 "Weixin": ("wechat" "wechat")  1021x740+0+0  +129+30',
        ]
        self.assertEqual(classify_client_state(windows), "logged_in_or_main_window")


if __name__ == "__main__":
    unittest.main()
