import tempfile
import unittest
from pathlib import Path

from ui_worker.inbound import InboundDeduper, message_fingerprint


class InboundDeduperTests(unittest.TestCase):
    def test_same_message_is_accepted_once(self):
        with tempfile.TemporaryDirectory() as directory:
            deduper = InboundDeduper(Path(directory) / "inbound.sqlite3")
            key = message_fingerprint("42", "hello")
            self.assertTrue(deduper.accept(key))
            self.assertFalse(deduper.accept(key))
            deduper.close()

    def test_different_texts_have_different_fingerprints(self):
        self.assertNotEqual(message_fingerprint("42", "one"), message_fingerprint("42", "two"))


if __name__ == "__main__":
    unittest.main()
