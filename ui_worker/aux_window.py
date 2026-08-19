"""Conservative classification of auxiliary WeChat windows."""
from __future__ import annotations


def classify_auxiliary_window(title: str, window_type: str, size: tuple[int, int], relation: str, capture_is_blank: bool = False) -> str:
    normalized = title.strip().lower()
    if normalized == "wechat" and window_type == "utility" and relation == "wechat-main":
        return "known_utility_overlay"
    if normalized == "weixin" and window_type == "normal" and relation == "unknown" and capture_is_blank:
        return "blank_safe_overlay"
    if window_type in {"dialog", "modal"} or normalized in {"confirm", "login", "permission", "payment", "qr"}:
        return "sensitive_blocking"
    return "unknown_blocking"
