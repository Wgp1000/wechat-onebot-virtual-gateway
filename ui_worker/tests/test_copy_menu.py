import unittest

from ui_worker.copy_menu import copy_menu_point


class CopyMenuTests(unittest.TestCase):
    def test_uses_center_of_verified_incoming_bubble(self):
        self.assertEqual(copy_menu_point((175, 359, 80, 18), origin=(430, 100)), (645, 468))

    def test_rejects_clipped_or_empty_bubble(self):
        self.assertIsNone(copy_menu_point((175, 0, 80, 18), origin=(430, 100)))
        self.assertIsNone(copy_menu_point((175, 359, 0, 18), origin=(430, 100)))


if __name__ == "__main__":
    unittest.main()
