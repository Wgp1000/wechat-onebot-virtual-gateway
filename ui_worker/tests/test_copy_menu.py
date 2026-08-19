import unittest

from ui_worker.copy_menu import has_copy_action


class CopyMenuTests(unittest.TestCase):
    def test_uses_center_of_verified_incoming_bubble(self):
        from ui_worker.copy_menu import copy_menu_point
        self.assertEqual(copy_menu_point((175, 359, 80, 18), origin=(430, 100)), (645, 468))

    def test_rejects_clipped_or_empty_bubble(self):
        from ui_worker.copy_menu import copy_menu_point
        self.assertIsNone(copy_menu_point((175, 0, 80, 18), origin=(430, 100)))
        self.assertIsNone(copy_menu_point((175, 359, 0, 18), origin=(430, 100)))

    def test_accepts_verified_copy_menu_item(self):
        self.assertTrue(has_copy_action("Copy\nForward\nDelete"))
        self.assertTrue(has_copy_action("复制\n转发\n删除"))

    def test_rejects_card_menu_without_copy(self):
        self.assertFalse(has_copy_action("Open with Default\nAdd to Favorite\nDelete"))


if __name__ == "__main__":
    unittest.main()
