"""Fail-closed window overlap checks for private-message extraction."""
from __future__ import annotations


def _intersects(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


def chat_pane_unoccluded(main_window: tuple[int, int, int, int], auxiliaries: list[tuple[int, int, int, int]], pane: tuple[int, int, int, int]) -> bool:
    mx, my, _, _ = main_window
    px, py, pw, ph = pane
    absolute_pane = (mx + px, my + py, pw, ph)
    return not any(_intersects(absolute_pane, auxiliary) for auxiliary in auxiliaries)
