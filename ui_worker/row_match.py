"""Map a calibrated visual conversation row to an approved private identity."""
from __future__ import annotations


def match_registered_row(registry: dict[str, dict[str, str]], fingerprint: str, row: int) -> dict[str, object] | None:
    entry = registry.get(fingerprint)
    if entry is None:
        return None
    return {**entry, "row": row}
