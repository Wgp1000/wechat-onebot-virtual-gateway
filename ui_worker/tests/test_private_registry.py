import unittest

from ui_worker.private_registry import PrivateConversation, approved_private_candidates


class PrivateRegistryTests(unittest.TestCase):
    def test_returns_only_registered_private_rows_with_exact_titles(self):
        registry = [
            PrivateConversation("100", "Alice", "Alice"),
            PrivateConversation("200", "Team Group", "Team Group", kind="group"),
        ]
        rows = [{"title": "Alice", "row": 0}, {"title": "Team Group", "row": 1}]
        candidates = approved_private_candidates(registry, rows)
        self.assertEqual([(c.conversation_id, c.row) for c in candidates], [("100", 0)])

    def test_duplicate_display_titles_are_quarantined(self):
        registry = [PrivateConversation("100", "Alex", "alex-1"), PrivateConversation("101", "Alex", "alex-2")]
        self.assertEqual(approved_private_candidates(registry, [{"title": "Alex", "row": 0}]), [])


if __name__ == "__main__":
    unittest.main()
