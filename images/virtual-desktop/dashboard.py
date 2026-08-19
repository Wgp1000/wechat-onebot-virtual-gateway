#!/usr/bin/env python3
"""Minimal local-only status panel for the virtual desktop container."""

from __future__ import annotations

import html
import json
import os
import socket
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def port_open(port: int) -> bool:
    with socket.socket() as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def process_running(name: str) -> bool:
    for entry in os.scandir("/proc"):
        if not entry.name.isdigit():
            continue
        try:
            if open(f"/proc/{entry.name}/comm", encoding="utf-8").read().strip() == name:
                return True
        except (FileNotFoundError, PermissionError):
            continue
    return False


def status() -> dict[str, bool | str]:
    display = os.environ.get("DISPLAY", ":99")
    ui_detected = False
    try:
        ui_detected = bool(json.loads(open("/tmp/runtime-wechat/ui-status.json", encoding="utf-8").read()).get("wechat_window_detected"))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    x11_detected = False
    client_state = "unknown"
    try:
        x11_data = json.loads(open("/tmp/runtime-wechat/x11-status.json", encoding="utf-8").read())
        x11_detected = bool(x11_data.get("wechat_window_detected"))
        client_state = str(x11_data.get("client_state", "unknown"))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return {
        "x11_socket": os.path.exists(f"/tmp/.X11-unix/X{display.removeprefix(':')}") ,
        "xvfb": process_running("Xvfb"),
        "openbox": process_running("openbox"),
        "vnc": port_open(5900),
        "novnc": port_open(6080),
        "test_window": process_running("python3"),
        "wechat_client": process_running("wechat"),
        "wechat_ui_detected": ui_detected,
        "wechat_x11_window_detected": x11_detected,
        "wechat_client_state": client_state,
    }


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        states = status()
        if self.path == "/api/v1/state":
            body = json.dumps(states, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/healthz":
            good = all(states[key] for key in ("x11_socket", "xvfb", "vnc", "novnc"))
            body = ("ok" if good else "degraded").encode()
            self.send_response(200 if good else 503)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        rows = "".join(
            f"<tr><td>{html.escape(name)}</td><td class='{('ok' if value else 'bad')}'>{'ready' if value else 'not ready'}</td></tr>"
            for name, value in states.items()
        )
        page = f"""<!doctype html><meta charset='utf-8'><title>WeChat Virtual Gateway</title>
<style>body{{font-family:system-ui;background:#f6f8fa;color:#17212b;margin:0}}main{{max-width:760px;margin:48px auto;background:#fff;padding:28px;border:1px solid #d0d7de}}h1{{margin-top:0}}table{{border-collapse:collapse;width:100%}}td{{padding:10px;border-bottom:1px solid #d8dee4}}.ok{{color:#1a7f37}}.bad{{color:#cf222e}}a{{display:inline-block;background:#0969da;color:#fff;padding:10px 14px;text-decoration:none;border-radius:6px;margin-top:20px}}small{{color:#57606a}}</style>
<main><h1>WeChat Virtual Gateway</h1><p>Official WeChat client runs inside an isolated virtual desktop.</p><table>{rows}</table><a href='http://127.0.0.1:6080/vnc.html'>Open noVNC desktop</a><p><small>Local-only panel. Login and UI automation remain user-controlled while the gateway is under development.</small></p></main>"""
        body = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        return


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8088), Handler).serve_forever()
