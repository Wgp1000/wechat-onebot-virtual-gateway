import unittest

from ui_worker.message_select import incoming_bubble_point


class MessageSelectTests(unittest.TestCase):
    def test_returns_point_only_for_left_message_bounds(self):
        self.assertEqual(incoming_bubble_point(left=35, top=80, width=160, height=30, split_x=350), (115, 95))

    def test_rejects_right_side_bounds(self):
        self.assertIsNone(incoming_bubble_point(left=470, top=80, width=160, height=30, split_x=350))


if __name__ == "__main__":
    unittest.main()
