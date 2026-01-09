"""SQLite storage for audit results."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import List

from dataguardian.models import AuditResult, StoredAudit


class SQLiteAuditStore:
    """Store audit results in a local SQLite database."""

    def __init__(self, db_path: Path):
        self.db_path = db_path

    def initialize(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS audits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    scanned_at TEXT NOT NULL,
                    trackers INTEGER NOT NULL,
                    cookies INTEGER NOT NULL,
                    third_party_domains INTEGER NOT NULL,
                    risk_score INTEGER NOT NULL,
                    findings_json TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def save(self, result: AuditResult) -> int:
        findings_json = json.dumps([finding.to_dict() for finding in result.findings])
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO audits (url, scanned_at, trackers, cookies, third_party_domains, risk_score, findings_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    result.url,
                    result.scanned_at.isoformat(),
                    result.trackers,
                    result.cookies,
                    result.third_party_domains,
                    result.risk_score,
                    findings_json,
                ),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def list_recent(self, limit: int = 10) -> List[StoredAudit]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, url, scanned_at, trackers, cookies, third_party_domains, risk_score, findings_json
                FROM audits
                ORDER BY scanned_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return [self._row_to_record(row) for row in rows]

    def get(self, audit_id: int) -> StoredAudit | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT id, url, scanned_at, trackers, cookies, third_party_domains, risk_score, findings_json
                FROM audits
                WHERE id = ?
                """,
                (audit_id,),
            ).fetchone()
        if not row:
            return None
        return self._row_to_record(row)

    @contextmanager
    def _connect(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _row_to_record(self, row: sqlite3.Row) -> StoredAudit:
        return StoredAudit(
            id=row[0],
            url=row[1],
            scanned_at=datetime.fromisoformat(row[2]),
            trackers=row[3],
            cookies=row[4],
            third_party_domains=row[5],
            risk_score=row[6],
            findings_json=row[7],
        )
