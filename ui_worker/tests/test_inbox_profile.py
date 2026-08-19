import unittest

from ui_worker.inbox_profile import InboxProfile, row_regions


class InboxProfileTests(unittest.TestCase):
    def test_fixed_profile_returns_title_preview_and_badge_regions(self):
        profile = InboxProfile()
        regions = row_regions(profile, 0)
        self.assertEqual(regions.title, (252, 116, 113, 21))
        self.assertEqual(regions.preview, (252, 142, 113, 21))
        self.assertEqual(regions.unread_badge, (234, 109, 18, 17))

    def test_next_row_advances_by_calibrated_height(self):
        profile = InboxProfile()
        self.assertEqual(row_regions(profile, 1).title[1], 187)


if __name__ == "__main__":
    unittest.main()
