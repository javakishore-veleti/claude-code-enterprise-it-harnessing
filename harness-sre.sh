#!/usr/bin/env bash
# SRE enterprise harness — forwards to enterprise_it_harnessing/sre_harnessing/package.json
# Usage: ./harness-sre.sh              # list 25+ SRE commands
#        ./harness-sre.sh repl         # interactive SRE session
#        ./harness-sre.sh observe-fx-matching
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$ROOT/enterprise_it_harnessing/_invoke.sh" sre_harnessing "$@"
