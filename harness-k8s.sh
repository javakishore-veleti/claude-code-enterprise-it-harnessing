#!/usr/bin/env bash
# Kubernetes enterprise harness — forwards to enterprise_it_harnessing/kubernetes_harnessing/package.json
# Usage: ./harness-k8s.sh              # list 25+ K8s commands
#        ./harness-k8s.sh repl
#        ./harness-k8s.sh pods-forex-markets
#        ./harness-k8s.sh pods-forex-markets --interactive
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$ROOT/enterprise_it_harnessing/_invoke.sh" kubernetes_harnessing "$@"
