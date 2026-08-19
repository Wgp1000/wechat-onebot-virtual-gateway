"""Validation for text copied from a selected incoming message bubble."""
from __future__ import annotations


def normalize_copied_message(value: str) -> str | None:
    text = " ".join(value.split())
    if not text or text.lower() in {"copy", "复制"}:
        return None
    return text
