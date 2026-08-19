"""Local dashboard token comparison helper."""
from __future__ import annotations

import hmac
import os


def token_matches(provided: str | None) -> bool:
    configured = os.environ.get("DASHBOARD_TOKEN", "")
    return bool(configured) and isinstance(provided, str) and hmac.compare_digest(configured, provided)
