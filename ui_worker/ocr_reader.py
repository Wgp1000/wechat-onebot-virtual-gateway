"""Deterministic OCR extraction for the active approved conversation."""
from __future__ import annotations

import csv
import subprocess
from pathlib import Path


def extract_new_lines(text: str, outgoing_marker: str = "") -> list[str]:
    lines = [line.strip() for line in text.splitlines()]
    return [line for line in lines if line and (not outgoing_marker or outgoing_marker not in line)]


def extract_left_aligned_lines(tsv: str, split_x: int) -> list[str]:
    grouped: dict[tuple[str, str, str, str], list[tuple[int, str]]] = {}
    for row in csv.DictReader(tsv.splitlines(), delimiter="\t"):
        text = row.get("text", "").strip()
        try:
            confidence = float(row.get("conf", "-1"))
            left = int(row.get("left", "0"))
        except ValueError:
            continue
        if not text or confidence < 40:
            continue
        key = (row["block_num"], row["par_num"], row["line_num"], row["top"])
        grouped.setdefault(key, []).append((left, text))
    messages = []
    for words in grouped.values():
        words.sort()
        if words[0][0] < split_x:
            messages.append(" ".join(word for _, word in words))
    return messages


def read_active_conversation(display: str = ":99", workspace: Path = Path("/tmp/wechat-adapter")) -> list[str]:
    workspace.mkdir(parents=True, exist_ok=True)
    xwd = workspace / "inbound.xwd"
    png = workspace / "inbound.png"
    threshold = workspace / "inbound-threshold.png"
    subprocess.run(["sh", "-c", f"DISPLAY={display} xwd -root -silent > {xwd}"], check=True)
    # Message pane, excluding left navigation/search and bottom composer.
    subprocess.run(["convert", str(xwd), "-crop", "700x530+430+100", str(png)], check=True)
    subprocess.run(["convert", str(png), "-colorspace", "Gray", "-contrast-stretch", "1%x1%", "-threshold", "65%", str(threshold)], check=True)
    result = subprocess.run(["tesseract", str(threshold), "stdout", "-l", "chi_sim+eng", "--psm", "6", "tsv"], capture_output=True, text=True, check=True)
    return extract_left_aligned_lines(result.stdout, split_x=350)
