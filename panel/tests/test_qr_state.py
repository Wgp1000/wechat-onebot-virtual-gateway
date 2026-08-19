import json
import unittest
from unittest.mock import patch

from panel.qr_state import LoginPanelState, login_state_from_x11


class LoginPanelStateTests(unittest.TestCase):
    def test_login_window_becomes_scannable_state(self):
        x11 = {
            "client_state": "awaiting_login",
            "windows": ['0x1200006 "Weixin": ("wechat" "wechat")  292x396+0+0  +494+202'],
        }

        state = login_state_from_x11(x11)

        self.assertEqual(state.mode, "awaiting_login")
        self.assertEqual(state.window_box, (494, 202, 292, 396))

    def test_missing_login_window_has_no_capture_box(self):
        state = login_state_from_x11({"client_state": "not_detected", "windows": []})
        self.assertEqual(state.mode, "not_detected")
        self.assertIsNone(state.window_box)


if __name__ == "__main__":
    unittest.main()
