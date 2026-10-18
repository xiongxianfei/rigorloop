#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ $# -ne 0 ]]; then
  echo 'usage: bash scripts/ci.sh (runs the complete essential suite; no mode/path options)' >&2
  exit 2
fi
node --test packages/rigorloop/test/*.test.js
python3 tests/engineering/packaging/test-adapter-distribution.py
python3 tests/engineering/packaging/test-npm-package-publication.py
python3 tests/skill/test-skill-validator.py
