"""Deterministic OCR/geometry parser for calibrated WeChat conversation rows."""
from __future__ import annotations

import csv
from dataclasses import dataclass


@dataclass(frozen=True)
class ScannedRow:
    title: str
    preview: str
    timestamp: str
    row: int


def parse_list_tsv(tsv: str, row_height: int) -> list[ScannedRow]:
    buckets: dict[int, list[dict[str, str]]] = {}
    for word in csv.DictReader(tsv.splitlines(), delimiter="\t"):
        text = word.get("text", "").strip()
        try:
            confidence = float(word.get("conf", "-1"))
            left = int(word.get("left", "0"))
            top = int(word.get("top", "0"))
        except ValueError:
            continue
        if not text or confidence < 40:
            continue
        buckets.setdefault(top // row_height, []).append({"text": text, "left": str(left), "top": str(top), "line": word.get("line_num", "0")})
    rows = []
    for row, words in sorted(buckets.items()):
        non_time = [item for item in words if int(item["left"]) < 150]
        line_ids = sorted({int(item["line"]) for item in non_time})
        title_line = line_ids[0] if line_ids else -1
        title = " ".join(item["text"] for item in sorted((item for item in non_time if int(item["line"]) == title_line), key=lambda item: int(item["left"])))
        preview = " ".join(item["text"] for item in sorted((item for item in non_time if int(item["line"]) != title_line), key=lambda item: (int(item["line"]), int(item["left"]))))
        timestamp = " ".join(item["text"] for item in sorted((item for item in words if int(item["left"]) >= 150), key=lambda item: int(item["left"])))
        if title:
            rows.append(ScannedRow(title, preview, timestamp, row))
    return rows
