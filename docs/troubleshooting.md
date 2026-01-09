# Troubleshooting

This page documents common issues resolved during repository hardening.

## Audit fails with "Provide either url or html"

The `/audit` endpoint requires either a `url` or `html` field. Provide one of
these fields in your JSON payload.

## Database file is missing

`SQLiteAuditStore` will create the database file if the directory exists. Ensure
`DATAGUARDIAN_DATA_DIR` points to a valid directory, or keep the default `data/`.

## Network access is blocked

If outbound network access is restricted, use the `html` payload approach and
avoid URL fetching. The tests and verification script rely on HTML fixtures
specifically to avoid external dependencies.

## AWS DynamoDB errors

The AWS path is optional. If you set `DATAGUARDIAN_USE_DYNAMODB=true` without
valid AWS credentials, the Lambda wrapper will fail with a `boto3` error. Use
`DATAGUARDIAN_USE_DYNAMODB=false` for local execution.

## Port already in use

If `./scripts/run.sh` fails because port `8000` is in use, either stop the
existing process or set `UVICORN_PORT` in your shell and run the command
manually:

```
python -m uvicorn dataguardian.api:create_app --factory --host 0.0.0.0 --port 8080
```
