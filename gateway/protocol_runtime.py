"""Protocol configuration change detection for live gateway updates."""
from __future__ import annotations

from gateway.protocol_config import ProtocolConfig


def config_changed(current: ProtocolConfig, updated: ProtocolConfig) -> bool:
    return current != updated
