import unittest

from ui_worker.copy_menu import copy_action_point_from_tsv


class CopyMenuTests(unittest.TestCase):
    def test_uses_center_of_verified_incoming_bubble(self):
        from ui_worker.copy_menu import copy_menu_point
        self.assertEqual(copy_menu_point((175, 359, 80, 18), origin=(430, 100)), (645, 468))

    def test_rejects_clipped_or_empty_bubble(self):
        from ui_worker.copy_menu import copy_menu_point
        self.assertIsNone(copy_menu_point((175, 0, 80, 18), origin=(430, 100)))
        self.assertIsNone(copy_menu_point((175, 359, 0, 18), origin=(430, 100)))

    def test_accepts_verified_copy_menu_item(self):
        from ui_worker.copy_menu import has_copy_action
        self.assertTrue(has_copy_action("Copy\nForward\nDelete"))
        self.assertTrue(has_copy_action("复制\n转发\n删除"))

    def test_rejects_card_menu_without_copy(self):
        from ui_worker.copy_menu import has_copy_action
        self.assertFalse(has_copy_action("Open with Default\nAdd to Favorite\nDelete"))

    def test_returns_root_point_for_copy_menu_word(self):
        tsv = """level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext
5\t1\t1\t1\t1\t1\t30\t20\t40\t16\t95\tCopy
"""
        self.assertEqual(copy_action_point_from_tsv(tsv, origin=(500, 480), scale=3), (516, 489))


if __name__ == "__main__":
    unittest.main()
