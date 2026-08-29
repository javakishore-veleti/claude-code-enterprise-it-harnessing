#!/usr/bin/env bash
# Kafka enterprise harness — forwards to enterprise_it_harnessing/kafka_harnessing/package.json
# Usage: ./harness-kafka.sh            # list 25+ Kafka commands
#        ./harness-kafka.sh repl --interactive
#        ./harness-kafka.sh lag-shopify-orders
#        ./harness-kafka.sh lag-shopify-orders --interactive
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HARNESS_CLI="./harness-kafka.sh"
exec "$ROOT/enterprise_it_harnessing/_invoke.sh" kafka_harnessing "$@"
