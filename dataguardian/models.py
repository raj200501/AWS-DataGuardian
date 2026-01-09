"""Data models for DataGuardian (stdlib-only)."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class TrackerFinding:
    tag: str
    attribute: str
    value: str
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class AuditResult:
    url: str
    scanned_at: datetime
    trackers: int
    cookies: int
    third_party_domains: int
    risk_score: int
    findings: List[TrackerFinding]

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "scanned_at": self.scanned_at.isoformat(),
            "trackers": self.trackers,
            "cookies": self.cookies,
            "third_party_domains": self.third_party_domains,
            "risk_score": self.risk_score,
            "findings": [finding.to_dict() for finding in self.findings],
        }


@dataclass(frozen=True)
class StoredAudit:
    id: int
    url: str
    scanned_at: datetime
    trackers: int
    cookies: int
    third_party_domains: int
    risk_score: int
    findings_json: str
