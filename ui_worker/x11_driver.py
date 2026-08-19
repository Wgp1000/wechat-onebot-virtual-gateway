"""Deterministic X11 actions for an already selected approved chat.

This module deliberately contains no visual model calls. It is a small state
machine building shell scripts around X11 geometry validated for this client
version. A production caller must whitelist the active conversation first.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChatGeometry:
    main_x: int = 129
    main_y: int = 30
    main_width: int = 1021
    main_height: int = 740

    @property
    def input_point(self) -> tuple[int, int]:
        return (self.main_x + 301, self.main_y + 645)

    @property
    def send_point(self) -> tuple[int, int]:
        return (self.main_x + 951, self.main_y + 706)


def current_chat_send_script(geometry: ChatGeometry) -> str:
    input_x, input_y = geometry.input_point
    send_x, send_y = geometry.send_point
    return (
        "xdotool mousemove {input_x} {input_y} click 1; "
        "xclip -selection clipboard; "
        "sleep 0.2; "
        "xdotool mousemove {send_x} {send_y} click 1"
    ).format(input_x=input_x, input_y=input_y, send_x=send_x, send_y=send_y)
