import tempfile
import unittest
from pathlib import Path

from ui_worker.contact_map import ContactMapStore


class ContactMapStoreTests(unittest.TestCase):
    def test_persists_onebot_id_to_wechat_search_key(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ContactMapStore(Path(directory) / "contacts.json")
            store.set("42", "Adapter Test Contact")
            self.assertEqual(store.get("42"), "Adapter Test Contact")

    def test_unknown_onebot_id_returns_none(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertIsNone(ContactMapStore(Path(directory) / "contacts.json").get("999"))


if __name__ == "__main__":
    unittest.main()
