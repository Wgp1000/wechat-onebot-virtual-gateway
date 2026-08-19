import tempfile
import unittest
from pathlib import Path

from gateway.app import GatewayService
from ui_worker.contact_map import ContactMapStore


class FriendListActionTests(unittest.IsolatedAsyncioTestCase):
    async def test_get_friend_list_returns_configured_mapping(self):
        with tempfile.TemporaryDirectory() as directory:
            contacts = Path(directory) / "contacts.json"
            ContactMapStore(contacts).set("42", "Test Contact")
            gateway = GatewayService(Path(directory) / "gateway.sqlite3", contacts_path=contacts)
            try:
                response = await gateway.handle_action("get_friend_list", {})
            finally:
                await gateway.close()

        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["data"], [{"user_id": 42, "nickname": "Test Contact"}])


if __name__ == "__main__":
    unittest.main()
