#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

run_check() {
  local label="$1"
  shift

  echo "==> $label"
  printf '+'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  echo
}

if ! command -v python >/dev/null 2>&1; then
  echo "python command not found; install Python or provide a python shim before running CI." >&2
  exit 1
fi

run_check "Validate canonical skills" \
  python scripts/validate-skills.py

run_check "Run skill validator fixtures" \
  python scripts/test-skill-validator.py

run_check "Check generated skill drift" \
  python scripts/build-skills.py --check

echo "CI checks passed."
