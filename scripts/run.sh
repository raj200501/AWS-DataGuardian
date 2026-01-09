#!/usr/bin/env bash
set -euo pipefail

export DATAGUARDIAN_DATA_DIR=${DATAGUARDIAN_DATA_DIR:-data}
export DATAGUARDIAN_SQLITE_PATH=${DATAGUARDIAN_SQLITE_PATH:-$DATAGUARDIAN_DATA_DIR/audit_results.db}

python -m dataguardian.api
