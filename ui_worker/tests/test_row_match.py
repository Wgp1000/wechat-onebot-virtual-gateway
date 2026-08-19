import unittest

from ui_worker.row_match import match_registered_row


class RowMatchTests(unittest.TestCase):
    def test_matches_same_visual_row_after_position_change(self):
        registered = {"fingerprint": {"user_id": "195", "search_key": "alice"}}
        self.assertEqual(match_registered_row(registered, "fingerprint", row=0), {"user_id": "195", "search_key": "alice", "row": 0})

    def test_rejects_unknown_visual_row(self):
        self.assertIsNone(match_registered_row({}, "unknown", row=0))


if __name__ == "__main__":
    unittest.main()
