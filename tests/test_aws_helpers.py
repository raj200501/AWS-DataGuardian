import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from serverless_functions.aws_helpers import save_audit_result
from dataguardian.storage import SQLiteAuditStore


class AWSHelpersTestCase(unittest.TestCase):
    def test_save_audit_result_local(self):
        with TemporaryDirectory() as tmp:
            os.environ["DATAGUARDIAN_USE_DYNAMODB"] = "false"
            os.environ["DATAGUARDIAN_DATA_DIR"] = tmp
            os.environ["DATAGUARDIAN_SQLITE_PATH"] = str(Path(tmp) / "audit.db")

            save_audit_result(
                "PrivacyAuditTable",
                "http://example.com",
                {"trackers": 2, "cookies": 1, "third_party_domains": 1, "risk_score": 25},
            )

            store = SQLiteAuditStore(Path(tmp) / "audit.db")
            store.initialize()
            records = store.list_recent(limit=1)
            self.assertEqual(records[0].url, "http://example.com")


if __name__ == "__main__":
    unittest.main()
