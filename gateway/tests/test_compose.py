import unittest
from pathlib import Path

import yaml


class ComposeGatewayTests(unittest.TestCase):
    def test_gateway_is_local_only_and_persists_its_database(self):
        compose = yaml.safe_load(Path("compose.yaml").read_text())
        gateway = compose["services"]["gateway"]

        self.assertIn("127.0.0.1:16700:16700", gateway["ports"])
        self.assertIn("./runtime/gateway:/data", gateway["volumes"])
        self.assertEqual(gateway["networks"], ["default", "internal"])


if __name__ == "__main__":
    unittest.main()
