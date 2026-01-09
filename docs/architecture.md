# DataGuardian Architecture

This document describes how DataGuardian works in **local mode**, which is the
validated configuration used in CI and in the quickstart. The AWS components are
still present as optional deployment targets, but the local runtime is the
source of truth for deterministic verification.

## High-level flow

1. A client submits HTML content or a URL to the `/audit` endpoint.
2. The `AuditEngine` fetches (if needed) and analyzes the HTML.
3. Findings are translated into a normalized `AuditResult` structure.
4. Results are stored in a local SQLite database.
5. The response includes an audit summary with a risk score and findings.

## Components

| Component | Path | Responsibility |
| --- | --- | --- |
| HTTP server | `dataguardian/api.py` | HTTP endpoints and orchestration |
| Audit engine | `dataguardian/audit.py` | HTML analysis and risk scoring |
| Storage | `dataguardian/storage.py` | SQLite persistence |
| CLI | `dataguardian/cli.py` | Scriptable audits and listing |
| Lambda wrapper | `serverless_functions/main.py` | AWS Lambda entrypoint |

## Audit engine

The audit engine evaluates HTML content for evidence of tracking scripts,
beacons, and analytics vendors. It maintains a configurable list of tracker
signatures and keyword matches that represent likely analytics scripts.

### Tracker signatures

The following signatures are intentionally deterministic and are scoped to
commonly used trackers:

- Google Analytics
- Google Tag Manager
- DoubleClick
- Meta Pixel (Facebook)
- Segment
- Hotjar
- Microsoft Clarity
- Mixpanel
- Snap Pixel
- TikTok Pixel

### Keyword matches

When an attribute contains an ambiguous tracker-like keyword, the engine assigns
an entry with a `Keyword match:` reason. These matches are meant to be visible
in output so that a user can manually review the findings.

### Risk scoring

Risk scores are calculated with the formula:

```
score = trackers * 10 + cookies * 2 + third_party_domains * 5
```

The score is capped at 100. The scaling is intentionally simple and can be
refined, but the current implementation provides consistent expectations for
verification and test coverage.

## Storage layer

Audit results are persisted to an SQLite database. This is deterministic,
requires no external service, and is suitable for local development and CI.

### Schema

The schema is created automatically:

```
CREATE TABLE audits (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  url TEXT NOT NULL,
  scanned_at TEXT NOT NULL,
  trackers INTEGER NOT NULL,
  cookies INTEGER NOT NULL,
  third_party_domains INTEGER NOT NULL,
  risk_score INTEGER NOT NULL,
  findings_json TEXT NOT NULL
)
```

### Storage decisions

- **SQLite** is used for deterministic local testing.
- **DynamoDB** is optional via `DATAGUARDIAN_USE_DYNAMODB=true` and is not used
  in CI.
- The storage layer returns normalized `StoredAudit` objects for CLI use.

## Local execution layout

The standard directory layout is:

```
.
├── dataguardian/
├── serverless_functions/
├── scripts/
├── tests/
├── data/
└── docs/
```

The `data/` directory is created automatically when running audits.

## API endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/healthz` | Service health check |
| POST | `/audit` | Run privacy audit |

### Example payload

```
{
  "html": "<html>...</html>",
  "source_label": "local-fixture"
}
```

### Example response

```
{
  "message": "Audit completed",
  "result": {
    "url": "local-fixture",
    "scanned_at": "2024-10-10T12:00:00Z",
    "trackers": 3,
    "cookies": 0,
    "third_party_domains": 2,
    "risk_score": 40,
    "findings": [
      {
        "tag": "script",
        "attribute": "src",
        "value": "https://www.google-analytics.com/analytics.js",
        "reason": "Google Analytics"
      }
    ]
  }
}
```

## AWS Lambda compatibility

The Lambda wrapper (`serverless_functions/main.py`) calls the same audit engine
and writes to storage. The function checks the environment variable
`DATAGUARDIAN_USE_DYNAMODB` to determine whether to call DynamoDB or local
SQLite. This ensures local verification remains deterministic while preserving
an AWS-compatible entrypoint.

## Data flow in local mode

1. API receives `/audit` request.
2. `AuditEngine.audit` returns `AuditResult`.
3. `SQLiteAuditStore.save` writes the record.
4. Response is returned with audit metadata.

## Observability

Logging is configured via standard Python logging with `logger.py` for the
serverless entrypoint and environment-driven log levels for the API.

## Security considerations

- The audit engine never executes JavaScript.
- Only HTML attributes are parsed and matched.
- Data is stored locally unless explicitly configured otherwise.

## Extensibility notes

Potential future enhancements:

- Add URL allow/deny lists.
- Extend signature catalog with policy metadata.
- Provide export to JSON/CSV in CLI.
- Add optional consent signal analysis.
