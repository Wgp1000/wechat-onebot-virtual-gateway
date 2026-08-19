"""Safe point selection for a contextual Copy action on an incoming bubble."""
from __future__ import annotations


def has_copy_action(menu_text: str) -> bool:
    tokens = {token.strip().lower() for token in menu_text.splitlines()}
    return "copy" in tokens or "复制" in tokens


def copy_menu_point(bounds: tuple[int, int, int, int], origin: tuple[int, int]) -> tuple[int, int] | None:
    left, top, width, height = bounds
    ox, oy = origin
    if width <= 0 or height <= 0 or top <= 0:
        return None
    return (ox + left + width // 2, oy + top + height // 2)
