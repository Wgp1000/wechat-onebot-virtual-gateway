import tempfile
import unittest
from pathlib import Path

from gateway.protocol_config import ProtocolConfig, ProtocolStore


class ProtocolStoreTests(unittest.TestCase):
    def test_creates_safe_local_reverse_websocket_default(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ProtocolStore(Path(directory) / "protocol.json")
            config = store.load()

        self.assertTrue(config.reverse_ws.enabled)
        self.assertEqual(config.reverse_ws.bind_host, "0.0.0.0")
        self.assertEqual(config.reverse_ws.port, 16700)
        self.assertFalse(config.forward_ws.enabled)

    def test_saves_and_reloads_forward_websocket_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "protocol.json"
            store = ProtocolStore(path)
            config = store.load()
            updated = ProtocolConfig(
                reverse_ws=config.reverse_ws,
                forward_ws=config.forward_ws.with_enabled(True).with_url("ws://127.0.0.1:18080"),
            )
            store.save(updated)

            reloaded = store.load()

        self.assertTrue(reloaded.forward_ws.enabled)
        self.assertEqual(reloaded.forward_ws.url, "ws://127.0.0.1:18080")


if __name__ == "__main__":
    unittest.main()
