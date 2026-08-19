"""Persistent, conservative OneBot protocol configuration."""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReverseWebSocket:
    enabled: bool = True
    bind_host: str = "0.0.0.0"
    port: int = 16700


@dataclass(frozen=True)
class ForwardWebSocket:
    enabled: bool = False
    url: str = ""

    def with_enabled(self, value: bool) -> "ForwardWebSocket":
        return ForwardWebSocket(enabled=value, url=self.url)

    def with_url(self, value: str) -> "ForwardWebSocket":
        return ForwardWebSocket(enabled=self.enabled, url=value)


@dataclass(frozen=True)
class ProtocolConfig:
    reverse_ws: ReverseWebSocket
    forward_ws: ForwardWebSocket

    @staticmethod
    def defaults() -> "ProtocolConfig":
        return ProtocolConfig(reverse_ws=ReverseWebSocket(), forward_ws=ForwardWebSocket())


class ProtocolStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> ProtocolConfig:
        if not self.path.exists():
            return ProtocolConfig.defaults()
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return ProtocolConfig(
            reverse_ws=ReverseWebSocket(**raw.get("reverse_ws", {})),
            forward_ws=ForwardWebSocket(**raw.get("forward_ws", {})),
        )

    def save(self, config: ProtocolConfig) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(".tmp")
        temp.write_text(json.dumps(asdict(config), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temp, self.path)
