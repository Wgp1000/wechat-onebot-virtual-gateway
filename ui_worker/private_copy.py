"""Fail-closed extraction of one approved private text bubble via Copy."""
from __future__ import annotations

from typing import Protocol

from ui_worker.clipboard_reader import normalize_copied_message
from ui_worker.copy_menu import has_copy_action


class PrivateCopyRunner(Protocol):
    def open_menu(self, point: tuple[int, int]) -> str: ...
    def copy_text(self) -> str: ...
    def dismiss_menu(self) -> None: ...


def extract_verified_private_text(runner: PrivateCopyRunner, point: tuple[int, int]) -> str | None:
    try:
        menu = runner.open_menu(point)
        if not has_copy_action(menu):
            return None
        return normalize_copied_message(runner.copy_text())
    finally:
        runner.dismiss_menu()
