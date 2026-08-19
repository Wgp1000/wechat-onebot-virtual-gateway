import json
import unittest
from unittest.mock import MagicMock

from ui_worker.http_api import handle_send_request


class WorkerHttpApiTests(unittest.TestCase):
    def test_send_request_calls_driver_with_mapped_contact(self):
        driver = MagicMock()
        driver.send_text.return_value = "wechat-outbound-1"
        contacts = MagicMock()
        contacts.get.return_value = "Adapter Test Contact"

        status, payload = handle_send_request({"user_id": "42", "text": "hello"}, driver, contacts)

        self.assertEqual(status, 200)
        self.assertEqual(payload["event_id"], "wechat-outbound-1")
        driver.send_text.assert_called_once_with("Adapter Test Contact", "hello")

    def test_unknown_contact_is_rejected_without_driver_call(self):
        driver = MagicMock()
        contacts = MagicMock()
        contacts.get.return_value = None

        status, payload = handle_send_request({"user_id": "42", "text": "hello"}, driver, contacts)

        self.assertEqual(status, 404)
        self.assertEqual(payload["error"], "contact mapping not found")
        driver.send_text.assert_not_called()


if __name__ == "__main__":
    unittest.main()
