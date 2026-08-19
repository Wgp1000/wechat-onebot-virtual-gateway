"""Safe geometry gates for selecting left-aligned incoming message bubbles."""
from __future__ import annotations


def incoming_bubble_point(left: int, top: int, width: int, height: int, split_x: int) -> tuple[int, int] | None:
    if width <= 0 or height <= 0 or left < 0 or left + width >= split_x:
        return None
    return (left + width // 2, top + height // 2)
