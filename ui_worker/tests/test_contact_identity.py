import unittest

from ui_worker.contact_identity import stable_user_id, normalize_contact_key


class ContactIdentityTests(unittest.TestCase):
    def test_contact_key_normalizes_ocr_whitespace(self):
        self.assertEqual(normalize_contact_key("  Test   Contact \n"), "Test Contact")

    def test_same_contact_has_stable_onebot_id(self):
        self.assertEqual(stable_user_id("Test Contact"), stable_user_id("Test Contact"))

    def test_different_contacts_have_different_ids(self):
        self.assertNotEqual(stable_user_id("Alice"), stable_user_id("Bob"))


if __name__ == "__main__":
    unittest.main()
