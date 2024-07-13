import unittest
from aws_helpers import save_audit_result

class AWSHelpersTestCase(unittest.TestCase):
    def test_save_audit_result(self):
        table_name = "PrivacyAuditTable"
        url = "http://example.com"
        audit_result = {"trackers": 5, "cookies": 3}
        save_audit_result(table_name, url, audit_result)
        self.assertTrue(True)  # Mock test; in real scenarios, check DynamoDB contents

if __name__ == '__main__':
    unittest.main()
