import unittest
from gateway.app import GatewayService
from gateway.forward_ws import ForwardWebSocketRuntime
from gateway.protocol_config import ForwardWebSocket
from pathlib import Path
import tempfile


class ForwardReloadTests(unittest.IsolatedAsyncioTestCase):
    async def test_replaces_forward_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            old = ForwardWebSocketRuntime(ForwardWebSocket(False, ""))
            gateway = GatewayService(Path(directory) / "db.sqlite3", forward_runtime=old)
            try:
                await gateway.reload_forward_ws(ForwardWebSocket(True, "ws://127.0.0.1:18080"))
                self.assertTrue(gateway._forward_runtime.config.enabled)
                self.assertEqual(gateway._forward_runtime.config.url, "ws://127.0.0.1:18080")
            finally:
                await gateway.close()


if __name__ == "__main__":
    unittest.main()
