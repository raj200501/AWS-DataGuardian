import unittest
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from dataguardian.models import AuditResult, TrackerFinding
from dataguardian.storage import SQLiteAuditStore


class StorageTestCase(unittest.TestCase):
    def test_sqlite_store_round_trip(self):
        with TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "audit.db"
            store = SQLiteAuditStore(db_path)
            store.initialize()

            result = AuditResult(
                url="fixture",
                scanned_at=datetime.now(timezone.utc),
                trackers=2,
                cookies=1,
                third_party_domains=1,
                risk_score=25,
                findings=[
                    TrackerFinding(tag="script", attribute="src", value="https://example.com", reason="Test"),
                ],
            )

            record_id = store.save(result)
            records = store.list_recent(limit=5)

            self.assertEqual(record_id, records[0].id)
            self.assertEqual(records[0].url, "fixture")
            self.assertEqual(records[0].trackers, 2)

            loaded = store.get(record_id)
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.id, record_id)
            self.assertEqual(loaded.risk_score, 25)


if __name__ == "__main__":
    unittest.main()
