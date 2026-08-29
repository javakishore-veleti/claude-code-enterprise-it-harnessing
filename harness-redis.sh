#!/usr/bin/env bash
# Redis enterprise harness — forwards to enterprise_it_harnessing/redis_harnessing/package.json
# Usage: ./harness-redis.sh            # list 25+ Redis commands
#        ./harness-redis.sh repl
#        ./harness-redis.sh info-shopify-idemp
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$ROOT/enterprise_it_harnessing/_invoke.sh" redis_harnessing "$@"
