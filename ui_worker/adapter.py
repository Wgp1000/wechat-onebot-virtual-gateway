"""Login-gated transport adapter contract for the virtual desktop client."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Protocol

from ui_worker.state_client import ClientState


@dataclass(frozen=True)
class InboundText:
    event_id: str
    conversation_id: str
    sender_name: str
    text: str


class DesktopDriver(Protocol):
    def send_text(self, conversation_id: str, text: str) -> str: ...

    def poll_text(self) -> Iterable[InboundText]: ...


class MemoryDesktopDriver:
    """Test driver; never interacts with a real chat client."""

    def __init__(self, inbound: Iterable[InboundText] = ()) -> None:
        self.inbound = list(inbound)
        self.sent: list[tuple[str, str]] = []

    def send_text(self, conversation_id: str, text: str) -> str:
        self.sent.append((conversation_id, text))
        return f"outbound-{len(self.sent)}"

    def poll_text(self) -> Iterable[InboundText]:
        messages, self.inbound = self.inbound, []
        return messages


class Adapter:
    def __init__(self, *, driver: DesktopDriver, state: Callable[[], ClientState]) -> None:
        self._driver = driver
        self._state = state

    def _require_ready(self) -> None:
        if not self._state().message_operations_ready:
            raise RuntimeError("desktop client is not ready for message operations")

    def send_private_text(self, conversation_id: str, text: str) -> str:
        self._require_ready()
        if not conversation_id or not text:
            raise ValueError("conversation_id and text are required")
        return self._driver.send_text(conversation_id, text)

    def poll_inbound(self) -> Iterable[InboundText]:
        self._require_ready()
        return self._driver.poll_text()
