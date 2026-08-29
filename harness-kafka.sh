#!/usr/bin/env bash
# Kafka enterprise harness — forwards to enterprise_it_harnessing/kafka_harnessing/package.json
# Usage: ./harness-kafka.sh            # list 25+ Kafka commands
#        ./harness-kafka.sh repl
#        ./harness-kafka.sh lag-shopify-orders
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$ROOT/enterprise_it_harnessing/_invoke.sh" kafka_harnessing "$@"
