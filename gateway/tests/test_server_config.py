import tempfile
import unittest
from pathlib import Path

from gateway.protocol_config import ForwardWebSocket, ProtocolConfig, ProtocolStore, ReverseWebSocket
from gateway.server import create_service


class GatewayServerConfigTests(unittest.TestCase):
    def test_create_service_uses_persisted_protocol_config(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "protocol.json"
            ProtocolStore(path).save(
                ProtocolConfig(
                    reverse_ws=ReverseWebSocket(enabled=True, bind_host="127.0.0.1", port=17600),
                    forward_ws=ForwardWebSocket(enabled=True, url="ws://127.0.0.1:17601"),
                )
            )
            service, config = create_service(Path(directory) / "gateway.sqlite3", path)

        self.assertEqual(config.reverse_ws.port, 17600)
        self.assertTrue(service._forward_runtime.config.enabled)
        self.assertEqual(service._forward_runtime.config.url, "ws://127.0.0.1:17601")


if __name__ == "__main__":
    unittest.main()
