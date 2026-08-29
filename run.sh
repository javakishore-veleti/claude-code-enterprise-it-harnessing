#!/usr/bin/env bash
# Run a Python file with this project's uv virtualenv.
# Creates .venv and installs dependencies if they are missing.
#
# Usage:
#   ./run.sh s01_perception_action_loop.py
#   ./run.sh ./s01_perception_action_loop.py --help
#   ./run.sh /absolute/path/to/script.py [args...]

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

usage() {
  echo "Usage: $(basename "$0") <python-file> [args...]" >&2
  echo "  python-file  Path to a .py file (relative to repo root or absolute)" >&2
  exit 1
}

[[ $# -ge 1 ]] || usage

PYFILE="$1"
shift

if [[ ! -f "$PYFILE" ]]; then
  echo "error: Python file not found: $PYFILE" >&2
  exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "error: uv is not installed or not on PATH." >&2
  echo "Install: https://docs.astral.sh/uv/getting-started/installation/" >&2
  exit 1
fi

VENV="$ROOT/.venv"

if [[ ! -x "$VENV/bin/python" ]]; then
  echo "Virtual environment not found; creating $VENV"
  uv venv "$VENV"
fi

uv sync

# Use the venv interpreter by path. `exec python` fails when `python` is not
# on PATH (common on macOS; interactive shells often only alias python=python3).
if [[ ! -x "$VENV/bin/python" ]]; then
  echo "error: $VENV/bin/python is missing after uv sync" >&2
  exit 1
fi

exec "$VENV/bin/python" "$PYFILE" "$@"
