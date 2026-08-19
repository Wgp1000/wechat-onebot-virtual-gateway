import json
import unittest
from unittest.mock import patch

from gateway.ui_worker_client import UiWorkerClient


class UiWorkerClientTests(unittest.TestCase):
    def test_send_private_posts_user_and_text(self):
        client = UiWorkerClient("http://ui-worker:9121")
        response = type("Response", (), {"read": lambda self: b'{\"event_id\":\"wechat-outbound-1\"}', "__enter__": lambda self: self, "__exit__": lambda *args: None})()
        with patch("gateway.ui_worker_client.urlopen", return_value=response) as request:
            event_id = client.send_private("42", "hello")

        self.assertEqual(event_id, "wechat-outbound-1")
        body = request.call_args.args[0].data.decode()
        self.assertEqual(json.loads(body), {"user_id": "42", "text": "hello"})


if __name__ == "__main__":
    unittest.main()
