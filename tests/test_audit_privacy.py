import unittest
from audit_privacy import perform_privacy_audit

class AuditPrivacyTestCase(unittest.TestCase):
    def test_perform_privacy_audit(self):
        url = "http://example.com"
        result = perform_privacy_audit(url)
        self.assertIn("trackers", result)
        self.assertIn("cookies", result)

if __name__ == '__main__':
    unittest.main()
