"""Sanitization helpers for the panel's read-only runtime log view."""
from __future__ import annotations

import re

_PATH_TOKEN = re.compile(r"/wechat/[^/\s?]+")
_QUERY_TOKEN = re.compile(r"([?&]token=)[^&\s]+", re.IGNORECASE)


def sanitize_log_line(line: str) -> str:
    line = _PATH_TOKEN.sub("/wechat/[REDACTED]", line)
    return _QUERY_TOKEN.sub(r"\1[REDACTED]", line)
