"""Guard unreliable inbound publishing until message identity is deterministic."""
from __future__ import annotations

import os


def inbound_publishing_enabled() -> bool:
    return os.environ.get("UI_WORKER_INBOUND_ENABLED", "false").lower() == "true"
