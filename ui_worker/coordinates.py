"""Coordinate transforms between calibrated WeChat crop and root X11 space."""
from __future__ import annotations


def crop_point_to_root(point: tuple[int, int], main_origin: tuple[int, int], crop_origin: tuple[int, int]) -> tuple[int, int]:
    x, y = point
    crop_x, crop_y = crop_origin
    return (crop_x + x, crop_y + y)
