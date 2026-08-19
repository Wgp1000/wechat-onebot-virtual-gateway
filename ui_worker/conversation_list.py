"""Parse deterministic OCR output from WeChat conversation-list region."""
from __future__ import annotations


def parse_conversation_candidates(text: str) -> list[str]:
    ignored = {"搜索", "+", "Recent News"}
    candidates = []
    for line in (part.strip() for part in text.splitlines()):
        if not line or line in ignored or line.startswith("[") or len(line) > 48:
            continue
        candidates.append(line)
    return candidates
