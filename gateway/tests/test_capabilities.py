import unittest

from gateway.capabilities import onebot_capabilities


class CapabilityTests(unittest.TestCase):
    def test_declares_private_text_inbound_as_experimental_not_enabled(self):
        capabilities = onebot_capabilities()
        self.assertFalse(capabilities["private_text_inbound"])
        self.assertTrue(capabilities["private_text_inbound_experimental"])
        self.assertFalse(capabilities["group_inbound"])
        self.assertFalse(capabilities["native_mentions"])
        self.assertTrue(capabilities["requires_unpinned_unfolded_inbox"])


if __name__ == "__main__":
    unittest.main()
