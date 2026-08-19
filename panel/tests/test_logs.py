import unittest

from panel.logs import sanitize_log_line


class PanelLogsTests(unittest.TestCase):
    def test_redacts_tokens_and_query_strings(self):
        line = "GET /wechat/secret-token/?token=another-secret HTTP/1.1"
        cleaned = sanitize_log_line(line)
        self.assertNotIn("secret-token", cleaned)
        self.assertNotIn("another-secret", cleaned)
        self.assertIn("[REDACTED]", cleaned)

    def test_keeps_non_sensitive_service_status(self):
        self.assertEqual(sanitize_log_line("OneBot reverse WebSocket listening"), "OneBot reverse WebSocket listening")


if __name__ == "__main__":
    unittest.main()
