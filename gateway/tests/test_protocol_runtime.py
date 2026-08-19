import tempfile
import unittest
from pathlib import Path

from gateway.protocol_runtime import config_changed
from gateway.protocol_config import ProtocolConfig, ReverseWebSocket, ForwardWebSocket


class ProtocolRuntimeTests(unittest.TestCase):
    def test_detects_forward_ws_change(self):
        current = ProtocolConfig(ReverseWebSocket(), ForwardWebSocket(False, ""))
        updated = ProtocolConfig(ReverseWebSocket(), ForwardWebSocket(True, "ws://127.0.0.1:18080"))
        self.assertTrue(config_changed(current, updated))

    def test_identical_config_does_not_require_reload(self):
        config = ProtocolConfig(ReverseWebSocket(), ForwardWebSocket(False, ""))
        self.assertFalse(config_changed(config, config))


if __name__ == "__main__":
    unittest.main()
