import unittest

from ui_worker.private_admission import AdmissionEvidence, admit_private_message


class PrivateAdmissionTests(unittest.TestCase):
    def test_admits_only_complete_verified_private_evidence(self):
        evidence = AdmissionEvidence(
            registered_private=True,
            list_stable=True,
            unpinned_unfolded=True,
            header_matches=True,
            pane_unoccluded=True,
            copied_text="hello",
        )
        self.assertTrue(admit_private_message(evidence))

    def test_rejects_if_any_identity_or_copy_evidence_is_missing(self):
        evidence = AdmissionEvidence(True, True, True, True, True, "")
        self.assertFalse(admit_private_message(evidence))
        self.assertFalse(admit_private_message(AdmissionEvidence(False, True, True, True, True, "hello")))


if __name__ == "__main__":
    unittest.main()
