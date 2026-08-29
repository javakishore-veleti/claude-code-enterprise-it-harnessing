#!/usr/bin/env bash
# DB jobs — 15 industry jobs. Does not replace ./harness-db.sh
# Usage: ./harness-db-job.sh                 # list jobs
#        ./harness-db-job.sh <job>
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HARNESS_CLI="./harness-db-job.sh"
exec "$ROOT/enterprise_it_harnessing/_invoke.sh" db_admin_harnessing/jobs "$@"
