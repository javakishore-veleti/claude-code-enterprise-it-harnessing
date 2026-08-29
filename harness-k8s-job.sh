#!/usr/bin/env bash
# Kubernetes jobs — 15 industry jobs. Does not replace ./harness-k8s.sh
# Usage: ./harness-k8s-job.sh                 # list jobs
#        ./harness-k8s-job.sh <job>
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HARNESS_CLI="./harness-k8s-job.sh"
exec "$ROOT/enterprise_it_harnessing/_invoke.sh" kubernetes_harnessing/jobs "$@"
