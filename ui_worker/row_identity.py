"""Visual evidence fingerprints for calibrated conversation-list rows."""
from __future__ import annotations

import hashlib


def row_fingerprint(avatar_crop: bytes, title_crop: bytes, row: int) -> str:
    digest = hashlib.blake2b(digest_size=32)
    digest.update(avatar_crop)
    digest.update(title_crop)
    return digest.hexdigest()
