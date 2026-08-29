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
  echo "Jobs:     sre_harnessing/jobs db_admin_harnessing/jobs kubernetes_harnessing/jobs redis_harnessing/jobs kafka_harnessing/jobs elk_harnessing/jobs" >&2
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
  echo "Example:       $0 repl --interactive"
  echo "Keep session:  $0 <playbook> --interactive"
  echo "Apply a skill: $0 skills <name>   or   $0 apply <name>"
  exit 0
fi

# ./harness-sre.sh skills <name>  and  ./harness-sre.sh apply <name>
# print that runbook. Extra flags (--interactive, --debug) still forward.
if [[ "${1:-}" == "apply" || ( "${1:-}" == "skills" && $# -ge 2 && "${2:-}" != --* ) ]]; then
  shift
  SKILL="${1:-}"
  if [[ -z "$SKILL" || "$SKILL" == --* ]]; then
    echo "Usage: apply <skill-name> [--interactive]" >&2
    exit 1
  fi
  shift
  exec npm --prefix "$PKG" run -s -- load-skill -- --skill "$SKILL" "$@"
fi

# -s hides npm's "> script-name" / "> ../../run.sh ..." banner.
exec npm --prefix "$PKG" run -s -- "$@"
