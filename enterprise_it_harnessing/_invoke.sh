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

_cli_for_profile() {
  case "$1" in
    sre_harnessing) echo "./harness-sre.sh" ;;
    sre_harnessing/jobs) echo "./harness-sre-job.sh" ;;
    db_admin_harnessing) echo "./harness-db.sh" ;;
    db_admin_harnessing/jobs) echo "./harness-db-job.sh" ;;
    kubernetes_harnessing) echo "./harness-k8s.sh" ;;
    kubernetes_harnessing/jobs) echo "./harness-k8s-job.sh" ;;
    redis_harnessing) echo "./harness-redis.sh" ;;
    redis_harnessing/jobs) echo "./harness-redis-job.sh" ;;
    kafka_harnessing) echo "./harness-kafka.sh" ;;
    kafka_harnessing/jobs) echo "./harness-kafka-job.sh" ;;
    elk_harnessing) echo "./harness-elk.sh" ;;
    elk_harnessing/jobs) echo "./harness-elk-job.sh" ;;
    *) echo "./$(basename "$0")" ;;
  esac
}

CLI="${HARNESS_CLI:-$(_cli_for_profile "$PROFILE")}"

if [[ $# -eq 0 ]]; then
  echo "$CLI"
  python3 - "$PKG/package.json" <<'PY'
import json
import sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text())
for name in data.get("scripts", {}):
    print(f"  {name}")
PY
  echo
  echo "Run:  $CLI <name>"
  if [[ "$PROFILE" != */jobs ]]; then
    echo "Keep: $CLI <name> --interactive"
    echo "Skill: $CLI apply <name>"
  fi
  exit 0
fi

# ./harness-sre.sh skills <name>  and  ./harness-sre.sh apply <name>
# print that runbook. Extra flags (--interactive, --debug) still forward.
if [[ "${1:-}" == "apply" || ( "${1:-}" == "skills" && $# -ge 2 && "${2:-}" != --* ) ]]; then
  shift
  SKILL="${1:-}"
  if [[ -z "$SKILL" || "$SKILL" == --* ]]; then
    echo "Usage: $CLI apply <skill-name> [--interactive]" >&2
    exit 1
  fi
  shift
  exec npm --prefix "$PKG" run -s -- load-skill -- --skill "$SKILL" "$@"
fi

# -s hides npm's "> script-name" / "> ../../run.sh ..." banner.
exec npm --prefix "$PKG" run -s -- "$@"
