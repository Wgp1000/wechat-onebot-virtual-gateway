"""Bridge normalized desktop adapter messages into the OneBot gateway."""
from __future__ import annotations

from gateway.app import GatewayService
from ui_worker.adapter import Adapter


async def publish_adapter_messages(adapter: Adapter, gateway: GatewayService) -> int:
    published = 0
    for message in adapter.poll_inbound():
        accepted = await gateway.accept_ui_event(
            {
                "event_id": message.event_id,
                "conversation_id": message.conversation_id,
                "sender_id": message.conversation_id,
                "sender_name": message.sender_name,
                "text": message.text,
            }
        )
        published += int(accepted)
    return published
