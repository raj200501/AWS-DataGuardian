# Operations Runbook

This runbook captures step-by-step operational guidance for running DataGuardian
in local mode.

## Purpose

- Provide a deterministic path to run the service.
- Explain expected outputs.
- Document troubleshooting steps for common failure modes.

## Pre-flight checklist

1. Confirm Python 3.11+ is installed:
   ```bash
   python --version
   ```
2. Ensure write access to the data directory:
   ```bash
   mkdir -p data && touch data/.probe
   ```
3. Confirm the test fixtures are available:
   ```bash
   ls tests/fixtures
   ```

## Start the service

```
./scripts/run.sh
```

You should see output similar to:

```
INFO:root:Starting DataGuardian API on 0.0.0.0:8000
```

## Validate health

```
curl http://localhost:8000/healthz
```

Expected output:

```
{"status": "ok"}
```

## Run a sample audit

```
curl -X POST http://localhost:8000/audit \
  -H 'Content-Type: application/json' \
  -d '{
    "html": "<html><script src=\"https://www.google-analytics.com/analytics.js\"></script></html>",
    "source_label": "runbook"
  }'
```

Expected output:

```
{"message": "Audit completed", "result": {"trackers": 1}}
```

## Inspect stored audits

```
python -m dataguardian.cli list
```

Expected output (example):

```
#1 runbook | trackers=1 cookies=0 risk=15
```

## Operational checks

| Check | Command | Pass Criteria |
| --- | --- | --- |
| API running | `curl http://localhost:8000/healthz` | Returns `{"status":"ok"}` |
| Audit works | `curl -X POST ... /audit` | Returns `"Audit completed"` |
| Storage works | `python -m dataguardian.cli list` | Output includes audits |

## Data retention guidance

- The default database path is `data/audit_results.db`.
- Delete or rotate this file according to your data retention policy.
- For sensitive environments, encrypt storage at rest or use a dedicated
  database with access controls.

## Logging

- Local logs are written to stdout.
- Use `DATAGUARDIAN_LOG_LEVEL=DEBUG` for verbose logging.

## Incident response

If you identify unexpected trackers:

1. Capture the URL and timestamp.
2. Store the audit JSON output.
3. Validate against your privacy policy.
4. Remediate unauthorized scripts.
5. Re-run the audit to confirm changes.

## Maintenance tasks

- Update the signature catalog quarterly.
- Review `docs/audit_signatures.md` for new vendors.
- Ensure the verification script remains green.

## Contact

For maintainers, document escalation paths internally.
