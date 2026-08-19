"""Production X11 runner for the verified WeChat desktop geometry."""
from __future__ import annotations

import subprocess
import time
from pathlib import Path


class LinuxWeChatRunner:
    def __init__(self, display: str = ":99", window=(129, 30, 1021, 740)) -> None:
        self.display = display
        self.x, self.y, self.width, self.height = window
        self.workdir = Path("/tmp/wechat-adapter")
        self.workdir.mkdir(parents=True, exist_ok=True)

    def _run(self, command: str) -> None:
        subprocess.run(["sh", "-c", command], check=True)

    def open_search(self) -> None:
        self._run(f"DISPLAY={self.display} xdotool mousemove {self.x + 155} {self.y + 44} click 1")
        time.sleep(0.2)

    def type_search(self, text: str) -> None:
        # Clipboard avoids keyboard-layout and non-ASCII key-event problems.
        encoded = text.replace("'", "'\\''")
        self._run(f"printf '%s' '{encoded}' | xclip -selection clipboard; DISPLAY={self.display} xdotool key ctrl+a ctrl+v")
        time.sleep(0.8)

    def capture_ocr(self) -> str:
        self._run(f"DISPLAY={self.display} xwd -root -silent > {self.workdir / 'screen.xwd'}")
        subprocess.run([
            "convert", str(self.workdir / "screen.xwd"), "-crop", f"410x180+{self.x + 60}+{self.y + 60}",
            str(self.workdir / "search.png"),
        ], check=True)
        result = subprocess.run(["tesseract", str(self.workdir / "search.png"), "stdout", "-l", "chi_sim+eng"], capture_output=True, text=True, check=True)
        return result.stdout.strip()

    def click_search_result(self, search_key: str) -> None:
        self._run(f"DISPLAY={self.display} xdotool mousemove {self.x + 155} {self.y + 110} click 1")
        time.sleep(0.7)

    def paste_and_send(self, text: str) -> None:
        encoded = text.replace("'", "'\\''")
        self._run(f"printf '%s' '{encoded}' | xclip -selection clipboard; DISPLAY={self.display} xdotool mousemove {self.x + 301} {self.y + 645} click 1; xdotool key ctrl+v")
        time.sleep(0.3)
        self._run(f"DISPLAY={self.display} xdotool mousemove {self.x + 951} {self.y + 706} click 1")
