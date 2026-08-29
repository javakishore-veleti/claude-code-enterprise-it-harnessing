#!/usr/bin/env bash
# ELK / Search jobs — 15 industry jobs. Does not replace ./harness-elk.sh
# Usage: ./harness-elk-job.sh                 # list jobs
#        ./harness-elk-job.sh <job>
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HARNESS_CLI="./harness-elk-job.sh"
exec "$ROOT/enterprise_it_harnessing/_invoke.sh" elk_harnessing/jobs "$@"
