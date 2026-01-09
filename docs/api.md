# DataGuardian API Reference

This API reference covers the local HTTP service used for deterministic
verification.

## Base URL

```
http://localhost:8000
```

## Health Check

**GET** `/healthz`

### Response

```
{
  "status": "ok"
}
```

## Run an Audit

**POST** `/audit`

### Request body

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `url` | string | optional | URL to fetch and analyze |
| `html` | string | optional | HTML payload to analyze |
| `source_label` | string | optional | Label to appear in audit output |

At least one of `url` or `html` is required.

### Example (HTML payload)

```
curl -X POST http://localhost:8000/audit \
  -H 'Content-Type: application/json' \
  -d '{
    "html": "<html><script src=\"https://www.google-analytics.com/analytics.js\"></script></html>",
    "source_label": "manual"
  }'
```

### Example response

```
{
  "message": "Audit completed",
  "result": {
    "url": "manual",
    "scanned_at": "2024-10-10T12:00:00Z",
    "trackers": 1,
    "cookies": 0,
    "third_party_domains": 1,
    "risk_score": 15,
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

### Error responses

| Status | Meaning | Example |
| --- | --- | --- |
| 400 | Invalid request | `{"detail": "Provide either url or html for auditing"}` |
| 500 | Internal error | `{"detail": "Audit failed"}` |

## Audit record storage

Records are written to the local SQLite database defined by
`DATAGUARDIAN_SQLITE_PATH`. The API does not currently expose a query endpoint
for historical data; use the CLI `list` command instead.

## CLI usage

While not part of the HTTP API, the CLI complements the API by producing and
listing audit results from the same storage:

```
python -m dataguardian.cli audit --html-file tests/fixtures/sample_page.html
python -m dataguardian.cli list
```
