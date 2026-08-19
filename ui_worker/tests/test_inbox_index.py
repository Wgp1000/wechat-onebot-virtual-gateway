import tempfile
import unittest
from pathlib import Path

from ui_worker.inbox_index import ConversationEntry, InboxIndex, InboxSafetyError


class InboxIndexTests(unittest.TestCase):
    def test_refuses_auto_mode_when_any_conversation_is_pinned(self):
        entries = [ConversationEntry("Alice", "alice", pinned=True)]
        with self.assertRaises(InboxSafetyError):
            InboxIndex.from_scan(entries)

    def test_refuses_auto_mode_when_a_group_is_collapsed(self):
        entries = [ConversationEntry("Team", "team", collapsed=True)]
        with self.assertRaises(InboxSafetyError):
            InboxIndex.from_scan(entries)

    def test_persists_directory_and_returns_first_unpinned_entry(self):
        entries = [ConversationEntry("Alice", "alice"), ConversationEntry("Bob", "bob")]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "inbox.json"
            index = InboxIndex.from_scan(entries)
            index.save(path)
            loaded = InboxIndex.load(path)
        self.assertEqual(loaded.first_active().search_key, "alice")


if __name__ == "__main__":
    unittest.main()
