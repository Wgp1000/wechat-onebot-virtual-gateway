"""User-facing capability status for the conservative inbound roadmap."""
from __future__ import annotations


def private_inbound_status() -> dict[str, object]:
    return {
        "mode": "experimental_private_only",
        "enabled": False,
        "requires_unpinned_unfolded_inbox": True,
        "group_inbound": False,
        "mentions": False,
    }
