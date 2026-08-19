"""Explicit supported-scope declaration for downstream OneBot clients."""
from __future__ import annotations


def onebot_capabilities() -> dict[str, bool]:
    return {
        "private_text_inbound": False,
        "private_text_inbound_experimental": True,
        "group_inbound": False,
        "native_mentions": False,
        "requires_unpinned_unfolded_inbox": True,
    }
