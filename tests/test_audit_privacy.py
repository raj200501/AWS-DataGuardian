import unittest
from unittest.mock import patch

from serverless_functions import audit_privacy


class AuditPrivacyTestCase(unittest.TestCase):
    def test_perform_privacy_audit(self):
        with patch("dataguardian.audit.AuditEngine.audit") as fake_audit:
            fake_audit.return_value = type(
                "Result",
                (),
                {"trackers": 2, "cookies": 1, "third_party_domains": 1, "risk_score": 25},
            )()
            result = audit_privacy.perform_privacy_audit("http://example.com")
            self.assertEqual(result["trackers"], 2)
            self.assertEqual(result["cookies"], 1)


if __name__ == "__main__":
    unittest.main()
