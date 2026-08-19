import os
import unittest
from unittest.mock import patch

from panel.web import authorized


class PanelAuthTests(unittest.TestCase):
    def test_correct_query_token_authorizes(self):
        with patch.dict(os.environ, {"PANEL_TOKEN": "token"}):
            self.assertTrue(authorized("token"))

    def test_missing_or_wrong_token_is_denied(self):
        with patch.dict(os.environ, {"PANEL_TOKEN": "token"}):
            self.assertFalse(authorized(None))
            self.assertFalse(authorized("wrong"))


if __name__ == "__main__":
    unittest.main()
