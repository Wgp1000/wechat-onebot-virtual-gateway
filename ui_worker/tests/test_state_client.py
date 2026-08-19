import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ui_worker.state_client import ClientState, fetch_client_state


class ClientStateTests(unittest.TestCase):
    def test_awaiting_login_state_is_not_ready_for_message_operations(self):
        payload = json.dumps({"wechat_client": True, "wechat_client_state": "awaiting_login"}).encode()
        with patch("ui_worker.state_client.urlopen") as request:
            request.return_value.__enter__.return_value.read.return_value = payload
            state = fetch_client_state("http://127.0.0.1:8088/api/v1/state")

        self.assertEqual(state.state, "awaiting_login")
        self.assertFalse(state.message_operations_ready)

    def test_main_window_state_is_ready_for_message_operations(self):
        payload = json.dumps({"wechat_client": True, "wechat_client_state": "logged_in_or_main_window"}).encode()
        with patch("ui_worker.state_client.urlopen") as request:
            request.return_value.__enter__.return_value.read.return_value = payload
            state = fetch_client_state("http://127.0.0.1:8088/api/v1/state")

        self.assertTrue(state.message_operations_ready)


if __name__ == "__main__":
    unittest.main()
