import unittest

from ui_worker.conversation_list import parse_conversation_candidates


class ConversationListTests(unittest.TestCase):
    def test_filters_ui_noise_and_keeps_text_candidates(self):
        text = "搜索\nTest Contact\n[Adapter Test] inbound\n+\n"
        self.assertEqual(parse_conversation_candidates(text), ["Test Contact"])


if __name__ == "__main__":
    unittest.main()
