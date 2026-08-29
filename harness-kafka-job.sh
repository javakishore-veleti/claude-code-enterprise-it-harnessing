#!/usr/bin/env bash
# Kafka / Event Bus jobs — 15 industry jobs. Does not replace ./harness-kafka.sh
# Usage: ./harness-kafka-job.sh                 # list jobs
#        ./harness-kafka-job.sh <job>
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$ROOT/enterprise_it_harnessing/_invoke.sh" kafka_harnessing/jobs "$@"
