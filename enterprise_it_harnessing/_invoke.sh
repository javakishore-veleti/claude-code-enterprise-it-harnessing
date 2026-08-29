#!/usr/bin/env bash
# Dispatch to a profile package.json under enterprise_it_harnessing/.
# Usage: _invoke.sh <profile_dir> [npm-script] [args...]

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
PROFILE="${1:-}"
shift || true

if [[ -z "$PROFILE" ]]; then
  echo "Usage: $(basename "$0") <profile_dir> [script] [args...]" >&2
  echo "Profiles: sre_harnessing db_admin_harnessing kubernetes_harnessing redis_harnessing kafka_harnessing elk_harnessing" >&2
  exit 1
fi

PKG="$HERE/$PROFILE"
if [[ ! -f "$PKG/package.json" ]]; then
  echo "error: missing $PKG/package.json" >&2
  exit 1
fi

cd "$ROOT"

if [[ $# -eq 0 ]]; then
  echo "Enterprise harness: $PROFILE"
  echo "package.json: $PKG/package.json"
  echo
  npm --prefix "$PKG" run
  echo
  echo "Run a script:  $(basename "$0" .sh) <script> [--interactive]"
  echo "Example:       $0 repl"
  echo "Keep session:  $0 <playbook> --interactive"
  exit 0
fi

# -s hides npm's "> script-name" / "> ../../run.sh ..." banner.
exec npm --prefix "$PKG" run -s -- "$@"
