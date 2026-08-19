#!/usr/bin/env python3
"""Fallback X11 window discovery for clients that expose no AT-SPI tree."""
from __future__ import annotations

import json
import os
import re
import subprocess
import time
from pathlib import Path

OUTPUT = Path("/tmp/runtime-wechat/x11-status.json")


def main() -> None:
    result = subprocess.run(
        ["xwininfo", "-display", os.environ.get("DISPLAY", ":99"), "-root", "-tree"],
        capture_output=True,
        text=True,
        check=False,
    )
    lines = [line.strip() for line in result.stdout.splitlines() if '"' in line]
    windows = lines[:100]
    combined = " ".join(windows).lower()
    weixin_login = [line for line in windows if '"Weixin"' in line]
    sizes = []
    for line in weixin_login:
        match = re.search(r'"Weixin".*?\s(\d+)x(\d+)\+', line)
        if match:
            sizes.append((int(match.group(1)), int(match.group(2))))
    if not sizes:
        client_state = "not_detected"
    elif any(width >= 500 or height >= 500 for width, height in sizes):
        client_state = "logged_in_or_main_window"
    else:
        client_state = "awaiting_login"
    state = {
        "updated_at": int(time.time()),
        "x11_available": result.returncode == 0,
        "wechat_window_detected": client_state != "not_detected",
        "client_state": client_state,
        "windows": windows,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
