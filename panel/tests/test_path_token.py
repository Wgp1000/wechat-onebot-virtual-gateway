import os
import unittest
from unittest.mock import patch

from panel.web import token_from_path


class PanelPathTokenTests(unittest.TestCase):
    def test_reads_token_from_first_path_segment(self):
        self.assertEqual(token_from_path("/secret/"), "secret")
        self.assertEqual(token_from_path("/secret/qr.png"), "secret")

    def test_empty_path_has_no_token(self):
        self.assertIsNone(token_from_path("/"))


if __name__ == "__main__":
    unittest.main()
