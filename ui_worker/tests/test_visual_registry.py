import tempfile
import unittest
from pathlib import Path

from ui_worker.visual_registry import VisualPrivateRegistry


class VisualRegistryTests(unittest.TestCase):
    def test_binds_onebot_user_to_stable_row_fingerprint(self):
        with tempfile.TemporaryDirectory() as directory:
            registry = VisualPrivateRegistry(Path(directory) / "private-rows.json")
            registry.bind("195", "fingerprint", "approved-search-key")
            self.assertEqual(registry.lookup("fingerprint"), {"user_id": "195", "search_key": "approved-search-key"})

    def test_persists_visual_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "private-rows.json"
            VisualPrivateRegistry(path).bind("195", "fingerprint", "approved-search-key")
            self.assertEqual(VisualPrivateRegistry(path).lookup("fingerprint")["user_id"], "195")


if __name__ == "__main__":
    unittest.main()
