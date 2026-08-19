import unittest

from ui_worker.window_guard import chat_pane_unoccluded


class WindowGuardTests(unittest.TestCase):
    def test_allows_main_window_without_intersecting_auxiliary(self):
        main = (129, 30, 1021, 740)
        self.assertTrue(chat_pane_unoccluded(main, [], (430, 100, 700, 530)))

    def test_rejects_auxiliary_intersecting_chat_pane(self):
        main = (129, 30, 1021, 740)
        auxiliary = [(352, 185, 573, 427)]
        self.assertFalse(chat_pane_unoccluded(main, auxiliary, (430, 100, 700, 530)))


if __name__ == "__main__":
    unittest.main()
