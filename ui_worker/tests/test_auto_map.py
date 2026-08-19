import unittest
from unittest.mock import MagicMock

from ui_worker.auto_map import register_active_contact


class AutoMapTests(unittest.TestCase):
    def test_registers_active_conversation_with_stable_onebot_id(self):
        contacts = MagicMock()
        user_id = register_active_contact(contacts)

        self.assertIsInstance(user_id, int)
        contacts.set.assert_called_once_with(str(user_id), "@active")


if __name__ == "__main__":
    unittest.main()
