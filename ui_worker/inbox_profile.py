"""Calibrated fixed-layout profile for the supported WeChat desktop build."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InboxProfile:
    row_start_y: int = 106
    row_height: int = 71
    title_x: int = 252
    title_y_offset: int = 10
    title_width: int = 113
    title_height: int = 21
    preview_x: int = 252
    preview_y_offset: int = 36
    preview_width: int = 113
    preview_height: int = 21
    unread_x: int = 234
    unread_y_offset: int = 3
    unread_width: int = 18
    unread_height: int = 17


@dataclass(frozen=True)
class RowRegions:
    title: tuple[int, int, int, int]
    preview: tuple[int, int, int, int]
    unread_badge: tuple[int, int, int, int]


def row_regions(profile: InboxProfile, row: int) -> RowRegions:
    y = profile.row_start_y + profile.row_height * row
    return RowRegions(
        title=(profile.title_x, y + profile.title_y_offset, profile.title_width, profile.title_height),
        preview=(profile.preview_x, y + profile.preview_y_offset, profile.preview_width, profile.preview_height),
        unread_badge=(profile.unread_x, y + profile.unread_y_offset, profile.unread_width, profile.unread_height),
    )
