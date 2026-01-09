import logging
import os

from dataguardian.config import Settings, ensure_data_dir
from dataguardian.storage import SQLiteAuditStore


USE_DYNAMODB = os.getenv("DATAGUARDIAN_USE_DYNAMODB", "false").lower() == "true"


def save_audit_result(table_name, url, audit_result):
    if USE_DYNAMODB:
        import boto3

        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(table_name)
        response = table.put_item(
            Item={
                "url": url,
                "trackers": audit_result["trackers"],
                "cookies": audit_result["cookies"],
                "third_party_domains": audit_result.get("third_party_domains", 0),
                "risk_score": audit_result.get("risk_score", 0),
            }
        )
        logging.info("Stored audit result for %s: %s", url, response)
        return

    settings = Settings.load()
    ensure_data_dir(settings)
    store = SQLiteAuditStore(settings.sqlite_path)
    store.initialize()

    from dataguardian.models import AuditResult
    from datetime import datetime, timezone

    result = AuditResult(
        url=url,
        scanned_at=datetime.now(timezone.utc),
        trackers=audit_result["trackers"],
        cookies=audit_result["cookies"],
        third_party_domains=audit_result.get("third_party_domains", 0),
        risk_score=audit_result.get("risk_score", 0),
        findings=[],
    )
    store.save(result)
    logging.info("Stored audit result for %s in SQLite", url)
