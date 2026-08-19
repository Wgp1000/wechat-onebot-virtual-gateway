import os
import unittest
from unittest.mock import patch

from ui_worker.inbound_policy import inbound_publishing_enabled


class InboundPolicyTests(unittest.TestCase):
    def test_is_disabled_by_default_until_reliable_conversation_identity_exists(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(inbound_publishing_enabled())

    def test_can_be_explicitly_enabled_for_validated_runtime(self):
        with patch.dict(os.environ, {"UI_WORKER_INBOUND_ENABLED": "true"}, clear=True):
            self.assertTrue(inbound_publishing_enabled())


if __name__ == "__main__":
    unittest.main()
