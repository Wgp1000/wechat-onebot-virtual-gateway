import tempfile
import unittest
from pathlib import Path

from gateway.contacts_api import friend_list
from ui_worker.contact_map import ContactMapStore


class ContactsApiTests(unittest.TestCase):
    def test_friend_list_exposes_persisted_contact_mappings(self):
        with tempfile.TemporaryDirectory() as directory:
            contacts = Path(directory) / "contacts.json"
            store = ContactMapStore(contacts)
            store.set("42", "Test Contact")
            self.assertEqual(friend_list(contacts), [{"user_id": 42, "nickname": "Test Contact"}])


if __name__ == "__main__":
    unittest.main()
