import unittest

from ui_worker.inbox_diff import InboxSnapshot, ConversationRow, newly_active_conversations


class InboxDiffTests(unittest.TestCase):
    def test_returns_only_changed_unpinned_unfolded_rows(self):
        before = InboxSnapshot([
            ConversationRow("Alice", "alice", "old", "09:00"),
            ConversationRow("Team", "team", "unchanged", "09:01"),
        ])
        after = InboxSnapshot([
            ConversationRow("Alice", "alice", "new preview", "09:02", unread=True),
            ConversationRow("Team", "team", "unchanged", "09:01"),
        ])
        self.assertEqual([row.search_key for row in newly_active_conversations(before, after)], ["alice"])

    def test_rejects_pinned_or_collapsed_changed_rows(self):
        before = InboxSnapshot([])
        after = InboxSnapshot([
            ConversationRow("Pinned", "pinned", "new", "09:03", unread=True, pinned=True),
            ConversationRow("Folded", "folded", "new", "09:03", unread=True, collapsed=True),
        ])
        self.assertEqual(newly_active_conversations(before, after), [])

    def test_does_not_treat_reordering_without_new_evidence_as_message(self):
        before = InboxSnapshot([ConversationRow("A", "a", "same", "09:00"), ConversationRow("B", "b", "same", "09:00")])
        after = InboxSnapshot([ConversationRow("B", "b", "same", "09:00"), ConversationRow("A", "a", "same", "09:00")])
        self.assertEqual(newly_active_conversations(before, after), [])


if __name__ == "__main__":
    unittest.main()
