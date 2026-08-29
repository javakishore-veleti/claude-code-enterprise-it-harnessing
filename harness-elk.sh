#!/usr/bin/env bash
# ELK + Grafana enterprise harness — forwards to enterprise_it_harnessing/elk_harnessing/package.json
# Usage: ./harness-elk.sh              # list 25+ ELK/Grafana commands
#        ./harness-elk.sh repl --interactive
#        ./harness-elk.sh search-shopify-webhooks
#        ./harness-elk.sh search-shopify-webhooks --interactive
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HARNESS_CLI="./harness-elk.sh"
exec "$ROOT/enterprise_it_harnessing/_invoke.sh" elk_harnessing "$@"
