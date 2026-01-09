#!/usr/bin/env bash
set -euo pipefail

python -m unittest discover -s tests -p "test_*.py"

TEMP_DIR=$(mktemp -d)
export DATAGUARDIAN_DATA_DIR="$TEMP_DIR"
export DATAGUARDIAN_SQLITE_PATH="$TEMP_DIR/audit_results.db"

python -m dataguardian.api &
SERVER_PID=$!

cleanup() {
  kill "$SERVER_PID" >/dev/null 2>&1 || true
  rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

for i in {1..20}; do
  if curl -s http://127.0.0.1:8000/healthz >/dev/null; then
    break
  fi
  sleep 0.2
done

HTML_PAYLOAD=$(python - <<'PY'
from pathlib import Path
html = (Path('tests') / 'fixtures' / 'sample_page.html').read_text(encoding='utf-8')
print(html.replace('"', '\\"').replace('\n', '\\n'))
PY
)

RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/audit \
  -H 'Content-Type: application/json' \
  -d "{\"html\": \"$HTML_PAYLOAD\", \"source_label\": \"verify-fixture\"}")

python - <<PY
import json
payload = json.loads('''$RESPONSE''')
assert payload['message'] == 'Audit completed'
assert payload['result']['trackers'] >= 3
assert payload['result']['risk_score'] > 0
print('Smoke test passed')
PY
