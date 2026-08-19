import unittest

from ui_worker.row_identity import row_fingerprint


class RowIdentityTests(unittest.TestCase):
    def test_fingerprint_is_stable_for_same_row_visual_evidence(self):
        self.assertEqual(row_fingerprint(b"avatar", b"title", 0), row_fingerprint(b"avatar", b"title", 0))

    def test_fingerprint_survives_row_reordering(self):
        self.assertEqual(row_fingerprint(b"avatar", b"title", 0), row_fingerprint(b"avatar", b"title", 1))

    def test_fingerprint_changes_for_different_visual_evidence(self):
        self.assertNotEqual(row_fingerprint(b"avatar", b"title", 0), row_fingerprint(b"avatar2", b"title", 0))


if __name__ == "__main__":
    unittest.main()
