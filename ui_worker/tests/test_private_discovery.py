import unittest

from ui_worker.private_discovery import discover_registered_rows


class PrivateDiscoveryTests(unittest.TestCase):
    def test_discovers_only_registered_visual_row(self):
        registry = {"known": {"user_id": "195", "search_key": "alice"}}
        rows = [{"row": 0, "fingerprint": "known"}, {"row": 1, "fingerprint": "unknown"}]
        self.assertEqual(discover_registered_rows(registry, rows), [{"user_id": "195", "search_key": "alice", "row": 0}])


if __name__ == "__main__":
    unittest.main()
