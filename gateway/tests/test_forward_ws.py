import asyncio
import json
import unittest

import websockets

from gateway.forward_ws import ForwardWebSocketRuntime
from gateway.protocol_config import ForwardWebSocket


class ForwardWebSocketRuntimeTests(unittest.IsolatedAsyncioTestCase):
    async def test_enabled_runtime_connects_and_receives_lifecycle(self):
        received: list[dict] = []

        async def handler(ws):
            received.append(json.loads(await ws.recv()))

        async with websockets.serve(handler, "127.0.0.1", 0) as server:
            port = server.sockets[0].getsockname()[1]
            runtime = ForwardWebSocketRuntime(ForwardWebSocket(enabled=True, url=f"ws://127.0.0.1:{port}"))
            await runtime.publish({"post_type": "meta_event", "meta_event_type": "lifecycle"})
            await asyncio.sleep(0.1)
            await runtime.close()

        self.assertEqual(received[0]["meta_event_type"], "lifecycle")

    async def test_disabled_runtime_does_not_connect(self):
        runtime = ForwardWebSocketRuntime(ForwardWebSocket(enabled=False, url="ws://127.0.0.1:1"))
        delivered = await runtime.publish({"post_type": "meta_event"})
        await runtime.close()
        self.assertFalse(delivered)


if __name__ == "__main__":
    unittest.main()
