from dataguardian.audit import AuditEngine


def perform_privacy_audit(url: str):
    """Backwards-compatible wrapper used by the Lambda handler."""

    engine = AuditEngine()
    result = engine.audit(url=url)
    return {
        "trackers": result.trackers,
        "cookies": result.cookies,
        "third_party_domains": result.third_party_domains,
        "risk_score": result.risk_score,
    }
