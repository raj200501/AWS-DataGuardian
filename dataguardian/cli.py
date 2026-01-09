"""Command-line interface for DataGuardian."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dataguardian.audit import AuditEngine
from dataguardian.config import Settings, ensure_data_dir
from dataguardian.storage import SQLiteAuditStore


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run DataGuardian privacy audits.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="Run an audit against a URL or HTML file.")
    audit_parser.add_argument("--url", help="URL to fetch and audit.")
    audit_parser.add_argument("--html-file", type=Path, help="Path to a local HTML file to audit.")
    audit_parser.add_argument("--label", help="Optional label for local HTML audits.")

    list_parser = subparsers.add_parser("list", help="List recent audits from storage.")
    list_parser.add_argument("--limit", type=int, default=5, help="Number of records to display.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    settings = Settings.load()
    ensure_data_dir(settings)
    store = SQLiteAuditStore(settings.sqlite_path)
    store.initialize()
    engine = AuditEngine(
        timeout_seconds=settings.audit_timeout_seconds,
        user_agent=settings.user_agent,
    )

    if args.command == "audit":
        if args.url and args.html_file:
            print("Provide either --url or --html-file, not both.", file=sys.stderr)
            return 2
        if not args.url and not args.html_file:
            print("Provide one of --url or --html-file.", file=sys.stderr)
            return 2

        html = None
        label = None
        if args.html_file:
            html = args.html_file.read_text(encoding="utf-8")
            label = args.label or args.html_file.name

        result = engine.audit(url=args.url, html=html, source_label=label)
        audit_id = store.save(result)
        payload = result.to_dict()
        payload["id"] = audit_id
        print(json.dumps(payload, indent=2, default=str))
        return 0

    if args.command == "list":
        records = store.list_recent(limit=args.limit)
        for record in records:
            print(
                f"#{record.id} {record.url} | trackers={record.trackers} cookies={record.cookies} risk={record.risk_score}"
            )
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
