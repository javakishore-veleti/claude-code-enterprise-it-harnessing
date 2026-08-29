#!/usr/bin/env bash
# SRE enterprise harness — forwards to enterprise_it_harnessing/sre_harnessing/package.json
# Usage: ./harness-sre.sh              # list 25+ SRE commands
#        ./harness-sre.sh repl --interactive
#        ./harness-sre.sh observe-fx-matching
#        ./harness-sre.sh observe-fx-matching --interactive
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HARNESS_CLI="./harness-sre.sh"
exec "$ROOT/enterprise_it_harnessing/_invoke.sh" sre_harnessing "$@"
