"""Find only approved private conversations from visual row evidence."""
from __future__ import annotations

from ui_worker.row_match import match_registered_row


def discover_registered_rows(registry: dict[str, dict[str, str]], rows: list[dict[str, object]]) -> list[dict[str, object]]:
    matches = []
    for row in rows:
        match = match_registered_row(registry, str(row["fingerprint"]), int(str(row["row"])))
        if match is not None:
            matches.append(match)
    return matches
