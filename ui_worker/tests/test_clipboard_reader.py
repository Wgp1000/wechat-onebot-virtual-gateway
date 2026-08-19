import unittest

from ui_worker.clipboard_reader import normalize_copied_message


class ClipboardReaderTests(unittest.TestCase):
    def test_keeps_single_line_message(self):
        self.assertEqual(normalize_copied_message("  hello world \n"), "hello world")

    def test_rejects_empty_or_ui_noise(self):
        self.assertIsNone(normalize_copied_message("   \n\t"))
        self.assertIsNone(normalize_copied_message("Copy"))


if __name__ == "__main__":
    unittest.main()
