"""Classify WeChat client state from read-only X11 window metadata."""
from __future__ import annotations

import re
from collections.abc import Iterable

_SIZE = re.compile(r'"Weixin".*?\s(\d+)x(\d+)\+')


def classify_client_state(windows: Iterable[str]) -> str:
    sizes: list[tuple[int, int]] = []
    for line in windows:
        match = _SIZE.search(line)
        if match:
            sizes.append((int(match.group(1)), int(match.group(2))))
    if not sizes:
        return "not_detected"
    if any(width >= 500 or height >= 500 for width, height in sizes):
        return "logged_in_or_main_window"
    return "awaiting_login"
