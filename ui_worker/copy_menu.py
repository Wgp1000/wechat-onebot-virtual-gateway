"""Safe point selection for a contextual Copy action on an incoming bubble."""
from __future__ import annotations

import csv


def copy_action_point_from_tsv(tsv: str, origin: tuple[int, int], scale: int) -> tuple[int, int] | None:
    ox, oy = origin
    for row in csv.DictReader(tsv.splitlines(), delimiter="\t"):
        if row.get("text", "").strip().lower() not in {"copy", "复制"}:
            continue
        try:
            if float(row.get("conf", "-1")) < 60:
                continue
            left = int(row["left"])
            top = int(row["top"])
            width = int(row["width"])
            height = int(row["height"])
        except ValueError:
            continue
        return (ox + (left + width // 2) // scale, oy + (top + height // 2) // scale)
    return None


def has_copy_action(menu_text: str) -> bool:
    tokens = {token.strip().lower() for token in menu_text.splitlines()}
    return "copy" in tokens or "复制" in tokens


def copy_menu_point(bounds: tuple[int, int, int, int], origin: tuple[int, int]) -> tuple[int, int] | None:
    left, top, width, height = bounds
    ox, oy = origin
    if width <= 0 or height <= 0 or top <= 0:
        return None
    return (ox + left + width // 2, oy + top + height // 2)
