import os
import unittest
from unittest.mock import patch

from dashboard_auth import token_matches


class DashboardAuthTests(unittest.TestCase):
    def test_rejects_request_without_token(self):
        with patch.dict(os.environ, {"DASHBOARD_TOKEN": "secret"}):
            self.assertFalse(token_matches(None))

    def test_accepts_exact_configured_token(self):
        with patch.dict(os.environ, {"DASHBOARD_TOKEN": "secret"}):
            self.assertTrue(token_matches("secret"))

    def test_rejects_wrong_token(self):
        with patch.dict(os.environ, {"DASHBOARD_TOKEN": "secret"}):
            self.assertFalse(token_matches("different"))


if __name__ == "__main__":
    unittest.main()
