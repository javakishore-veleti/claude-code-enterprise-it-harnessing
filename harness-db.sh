#!/usr/bin/env bash
# DBA enterprise harness — forwards to enterprise_it_harnessing/db_admin_harnessing/package.json
# Usage: ./harness-db.sh               # list 25+ DBA commands
#        ./harness-db.sh repl
#        ./harness-db.sh describe-fx-trades
#        ./harness-db.sh describe-fx-trades --interactive
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$ROOT/enterprise_it_harnessing/_invoke.sh" db_admin_harnessing "$@"
