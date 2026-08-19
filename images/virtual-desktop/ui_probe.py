#!/usr/bin/env python3
"""Read the AT-SPI tree and publish a minimal, redacted WeChat UI state."""
from __future__ import annotations

import json
import time
from pathlib import Path

import pyatspi

OUTPUT = Path("/tmp/runtime-wechat/ui-status.json")


def walk(node, depth: int = 0) -> list[dict[str, str]]:
    if depth > 2:
        return []
    rows = []
    try:
        name = node.name or ""
        role = node.getRoleName() or ""
        if name or role:
            rows.append({"name": name[:120], "role": role[:60]})
        for index in range(node.childCount):
            rows.extend(walk(node.getChildAtIndex(index), depth + 1))
    except Exception:
        pass
    return rows


def main() -> None:
    desktop = pyatspi.Registry.getDesktop(0)
    apps = []
    all_apps = []
    for index in range(desktop.childCount):
        app = desktop.getChildAtIndex(index)
        name = (app.name or "").strip()
        node_summary = walk(app)
        all_apps.append({"name": name[:120], "role": (app.getRoleName() or "")[:60], "nodes": node_summary[:40]})
        joined = " ".join(item["name"] for item in node_summary).lower()
        if "wechat" in name.lower() or "weixin" in name.lower() or "微信" in name or "scan to log in" in joined:
            apps.append({"name": name, "nodes": node_summary})
    state = {
        "updated_at": int(time.time()),
        "wechat_window_detected": bool(apps),
        "apps": apps,
        "desktop_apps": all_apps,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
