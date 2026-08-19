"""Translate read-only X11 window discovery into panel login state."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LoginPanelState:
    mode: str
    window_box: tuple[int, int, int, int] | None


_LOGIN_WINDOW = re.compile(r'"Weixin".*?\s(\d+)x(\d+)\+\d+\+\d+\s+\+(\d+)\+(\d+)$')


def login_state_from_x11(payload: dict[str, Any]) -> LoginPanelState:
    mode = str(payload.get("client_state", "unknown"))
    if mode != "awaiting_login":
        return LoginPanelState(mode=mode, window_box=None)
    for line in payload.get("windows", []):
        match = _LOGIN_WINDOW.search(str(line))
        if match:
            width, height, x, y = (int(part) for part in match.groups())
            return LoginPanelState(mode=mode, window_box=(x, y, width, height))
    return LoginPanelState(mode=mode, window_box=None)
