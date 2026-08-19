"""Automatic mapping for an inbound message in the active WeChat conversation."""
from __future__ import annotations

from ui_worker.contact_identity import stable_user_id
from ui_worker.contact_map import ContactMapStore


def register_active_contact(contacts: ContactMapStore) -> int:
    user_id = stable_user_id("@active")
    contacts.set(str(user_id), "@active")
    return user_id
