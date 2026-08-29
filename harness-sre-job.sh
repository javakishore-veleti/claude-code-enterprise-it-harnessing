#!/usr/bin/env bash
# SRE jobs — 15 industry jobs. Does not replace ./harness-sre.sh
# Usage: ./harness-sre-job.sh                 # list jobs
#        ./harness-sre-job.sh <job>
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$ROOT/enterprise_it_harnessing/_invoke.sh" sre_harnessing/jobs "$@"
