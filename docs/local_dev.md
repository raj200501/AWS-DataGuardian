# Local Development Guide

This guide documents how to run DataGuardian locally with deterministic
results. It mirrors the commands used in CI and in the verified quickstart.

## Prerequisites

- Python 3.11+
- `curl` (for the smoke test and manual validation)

## Setup

The local runtime uses only Python's standard library. A virtual environment is
optional but recommended for isolation:

```
python -m venv .venv
source .venv/bin/activate
```

## Run the API

```
./scripts/run.sh
```

The API will bind to `http://localhost:8000`.

## Run an audit via curl

```
curl -X POST http://localhost:8000/audit \
  -H 'Content-Type: application/json' \
  -d '{
    "html": "<html><script src=\"https://www.google-analytics.com/analytics.js\"></script></html>",
    "source_label": "manual"
  }'
```

## Use the CLI

```
python -m dataguardian.cli audit --html-file tests/fixtures/sample_page.html
python -m dataguardian.cli list
```

## Environment variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `DATAGUARDIAN_DATA_DIR` | `./data` | Directory for SQLite database |
| `DATAGUARDIAN_SQLITE_PATH` | `./data/audit_results.db` | SQLite database file |
| `DATAGUARDIAN_AUDIT_TIMEOUT` | `10` | HTTP request timeout in seconds |
| `DATAGUARDIAN_USER_AGENT` | `DataGuardian/1.0 (+local)` | User agent for URL fetching |
| `DATAGUARDIAN_LOG_LEVEL` | `INFO` | Logging verbosity |
| `DATAGUARDIAN_USE_DYNAMODB` | `false` | Use DynamoDB storage when `true` |

## Running tests

```
./scripts/verify.sh
```

## Notes on AWS usage

The AWS deployment scripts are intentionally not executed in local verification.
If you want to deploy to AWS, ensure you have valid AWS credentials configured
and install `boto3` before running the deployment scripts.
