#!/usr/bin/env bash
# Redis enterprise harness — forwards to enterprise_it_harnessing/redis_harnessing/package.json
# Usage: ./harness-redis.sh            # list 25+ Redis commands
#        ./harness-redis.sh repl --interactive
#        ./harness-redis.sh info-shopify-idemp
#        ./harness-redis.sh info-shopify-idemp --interactive
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HARNESS_CLI="./harness-redis.sh"
exec "$ROOT/enterprise_it_harnessing/_invoke.sh" redis_harnessing "$@"
