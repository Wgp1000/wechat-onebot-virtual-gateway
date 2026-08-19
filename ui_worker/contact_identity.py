"""Stable local OneBot identity for OCR-discovered WeChat contacts."""
from __future__ import annotations

import hashlib


def normalize_contact_key(value: str) -> str:
    return " ".join(value.split())


def stable_user_id(contact_key: str) -> int:
    digest = hashlib.blake2b(normalize_contact_key(contact_key).encode(), digest_size=8).digest()
    return int.from_bytes(digest, "big") & 0x7FFF_FFFF
