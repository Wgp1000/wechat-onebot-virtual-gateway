"""Fail-closed admission gate for one verified private text message."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AdmissionEvidence:
    registered_private: bool
    list_stable: bool
    unpinned_unfolded: bool
    header_matches: bool
    pane_unoccluded: bool
    copied_text: str


def admit_private_message(evidence: AdmissionEvidence) -> bool:
    return all((
        evidence.registered_private,
        evidence.list_stable,
        evidence.unpinned_unfolded,
        evidence.header_matches,
        evidence.pane_unoccluded,
        bool(evidence.copied_text.strip()),
    ))
