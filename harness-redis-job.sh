#!/usr/bin/env bash
# Redis jobs — 15 industry jobs. Does not replace ./harness-redis.sh
# Usage: ./harness-redis-job.sh                 # list jobs
#        ./harness-redis-job.sh <job>
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HARNESS_CLI="./harness-redis-job.sh"
exec "$ROOT/enterprise_it_harnessing/_invoke.sh" redis_harnessing/jobs "$@"
