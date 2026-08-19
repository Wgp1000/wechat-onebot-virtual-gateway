import tempfile
import unittest
from pathlib import Path

from panel.config_api import apply_contact_mapping, apply_protocol_config


class PanelConfigApiTests(unittest.TestCase):
    def test_contact_mapping_is_saved(self):
        with tempfile.TemporaryDirectory() as directory:
            contacts = Path(directory) / "contacts.json"
            apply_contact_mapping(contacts, {"user_id": "42", "search_key": "Adapter Test Contact"})
            self.assertIn('"42": "Adapter Test Contact"', contacts.read_text())

    def test_protocol_config_rejects_public_reverse_bind(self):
        with tempfile.TemporaryDirectory() as directory:
            protocol = Path(directory) / "protocol.json"
            with self.assertRaisesRegex(ValueError, "bind_host"):
                apply_protocol_config(protocol, {"reverse_ws": {"bind_host": "192.168.1.10", "port": 16700}})


if __name__ == "__main__":
    unittest.main()
