import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ui_worker.linux_runner import LinuxWeChatRunner


class LinuxRunnerCopyTests(unittest.TestCase):
    def test_copy_bubble_returns_clipboard_only_after_copy_menu_is_found(self):
        runner = LinuxWeChatRunner(workdir=Path("/tmp/test-runner-copy"))
        with patch.object(runner, "_run"), patch("subprocess.run") as run:
            run.side_effect = [
                type("R", (), {"stdout": ""})(),
                type("R", (), {"stdout": "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n5\t1\t1\t1\t1\t1\t30\t20\t40\t16\t95\tCopy\n"})(),
                type("R", (), {"stdout": "hello"})(),
            ]
            self.assertEqual(runner.copy_bubble_text((571, 570), menu_origin=(500, 480)), "hello")

    def test_copy_bubble_returns_none_when_copy_action_is_absent(self):
        runner = LinuxWeChatRunner(workdir=Path("/tmp/test-runner-copy"))
        with patch.object(runner, "_run"), patch("subprocess.run") as run:
            run.return_value = type("R", (), {"stdout": "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n"})()
            self.assertIsNone(runner.copy_bubble_text((571, 570), menu_origin=(500, 480)))


if __name__ == "__main__":
    unittest.main()
