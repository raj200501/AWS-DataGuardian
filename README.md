# DataGuardian

**DataGuardian** is a privacy-audit toolkit that inspects HTML for tracking
scripts, analytics beacons, and third-party resources. The project ships with a
local API/CLI for deterministic audits and includes optional AWS Lambda wiring
for serverless deployment.

> ✅ This repository has been validated in local mode. The commands below were
> executed successfully in CI and are deterministic.

## Features

- Deterministic privacy audits using a local HTTP service
- CLI for auditing HTML files and listing recent results
- SQLite-based storage for reproducible local runs
- Optional AWS Lambda wrapper that can write to DynamoDB when enabled
- Comprehensive unit + integration tests (stdlib-only)

## Repository layout

```
.
├── dataguardian/            # Local API, audit engine, and storage
├── serverless_functions/    # AWS Lambda wrapper and helpers
├── scripts/                 # run/verify scripts used in CI
├── tests/                   # unit + integration tests and fixtures
├── docs/                    # architecture + API references
└── data/                    # local SQLite database (generated)
```

## Installation

The local runtime uses **only Python's standard library**. If you already have
Python 3.11+ available, there are no additional dependencies to install.

Optional: create a virtual environment for isolation:

```bash
python -m venv .venv
source .venv/bin/activate
```

Optionally copy the sample environment file:

```bash
cp .env.example .env
```

## Verified Quickstart (local API)

Start the API:

```bash
./scripts/run.sh
```

In another terminal, run an audit using a deterministic fixture:

```bash
curl -X POST http://localhost:8000/audit \
  -H 'Content-Type: application/json' \
  -d '{
    "html": "<html><script src=\"https://www.google-analytics.com/analytics.js\"></script></html>",
    "source_label": "quickstart"
  }'
```

Expected response (truncated):

```json
{
  "message": "Audit completed",
  "result": {
    "trackers": 1,
    "cookies": 0,
    "third_party_domains": 1,
    "risk_score": 15
  }
}
```

## CLI Usage

Audit a local HTML file:

```bash
python -m dataguardian.cli audit --html-file tests/fixtures/sample_page.html
```

List recent audits:

```bash
python -m dataguardian.cli list
```

## Verified Verification

Run the deterministic verification suite (unit tests + smoke test):

```bash
./scripts/verify.sh
```

The verification script performs:

1. Unit test execution via `unittest`
2. A smoke test that starts the API and exercises `/healthz` and `/audit`

## AWS Lambda (optional)

The AWS Lambda wrapper in `serverless_functions/main.py` uses the same audit
engine. By default it stores results in local SQLite. To enable DynamoDB
integration, set:

```bash
export DATAGUARDIAN_USE_DYNAMODB=true
```

If you want to deploy to AWS, install the AWS SDK dependency and use the
existing scripts:

```bash
pip install boto3

cd serverless_functions
./build_lambda.sh

cd ../deployment
./deploy_infrastructure.sh
```

> Note: AWS deployment is not exercised in CI and requires valid AWS
> credentials in your environment.

## Documentation

- [Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [Local Development](docs/local_dev.md)
- [Runbook](docs/runbook.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Audit Signature Catalog](docs/audit_signatures.md)
- [Sample Reports](docs/sample_reports.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE)
file for details.
