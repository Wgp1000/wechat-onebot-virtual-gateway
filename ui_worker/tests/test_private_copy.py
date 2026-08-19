import unittest
from unittest.mock import MagicMock

from ui_worker.private_copy import extract_verified_private_text


class PrivateCopyTests(unittest.TestCase):
    def test_returns_text_only_when_menu_and_clipboard_are_verified(self):
        runner = MagicMock()
        runner.open_menu.return_value = "Copy\nForward\nDelete"
        runner.copy_text.return_value = "private test"
        self.assertEqual(extract_verified_private_text(runner, (600, 500)), "private test")
        runner.dismiss_menu.assert_called_once()

    def test_rejects_menu_without_copy_and_does_not_read_clipboard(self):
        runner = MagicMock()
        runner.open_menu.return_value = "Forward\nDelete"
        self.assertIsNone(extract_verified_private_text(runner, (600, 500)))
        runner.copy_text.assert_not_called()
        runner.dismiss_menu.assert_called_once()


if __name__ == "__main__":
    unittest.main()
