import unittest
from pathlib import Path

from dataguardian.audit import AuditEngine


class AuditEngineTestCase(unittest.TestCase):
    def test_audit_engine_detects_trackers(self):
        html = Path("tests/fixtures/sample_page.html").read_text(encoding="utf-8")
        engine = AuditEngine()
        result = engine.audit(html=html, source_label="https://fixture.local")

        self.assertGreaterEqual(result.trackers, 3)
        self.assertGreaterEqual(result.third_party_domains, 2)
        self.assertGreater(result.risk_score, 0)
        self.assertTrue(
            any("Analytics" in finding.reason or "Keyword" in finding.reason for finding in result.findings)
        )

    def test_audit_engine_no_trackers(self):
        html = Path("tests/fixtures/sample_page_clean.html").read_text(encoding="utf-8")
        engine = AuditEngine()
        result = engine.audit(html=html, source_label="https://fixture.local")

        self.assertEqual(result.trackers, 0)
        self.assertEqual(result.third_party_domains, 0)
        self.assertEqual(result.risk_score, 0)


if __name__ == "__main__":
    unittest.main()
