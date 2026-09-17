#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

DEFAULT_TIMEOUT_SECONDS=300

ci_original_args=("$@")
mode=""
base=""
head=""
release_version=""
broad_smoke=0
skip_diff_scoped=0
jobs=""
jobs_explicit=0
timeout_seconds="$DEFAULT_TIMEOUT_SECONDS"
fail_fast=0
verbose=0
durations=""
paths=()

usage() {
  cat <<'EOF'
Usage:
  bash scripts/ci.sh --mode local [--path <path>...]
  bash scripts/ci.sh --mode explicit --path <path>... [--broad-smoke]
  bash scripts/ci.sh --mode pr --base <sha> --head <sha>
  bash scripts/ci.sh --mode main --base <sha> --head <sha>
  bash scripts/ci.sh --mode release --release-version <version>
  bash scripts/ci.sh --mode broad-smoke [--skip-diff-scoped]

Execution options:
  --jobs <positive-integer>       Limit the shared validation worker budget.
  --timeout <positive-seconds>    Per-check timeout, default 300 seconds.
  --fail-fast                     Stop launching queued checks after a failure.
  --verbose                       Print successful check output when supported.
  --durations <nonnegative-int>    Show slowest dispatched workers; 0 shows all.
  --skip-diff-scoped              In broad-smoke mode, skip dirty-worktree review roots and use push-range lifecycle scope.

PR mode runs change-selected checks; main retains the full direct product gates.
When no --mode is supplied, ci.sh defaults to --mode broad-smoke for legacy compatibility.
When --jobs is omitted, ci.sh uses max(1, min(4, available CPU count minus one)) for selected checks.
Assessed independent work uses this budget in every execution mode.
EOF
}

fail_invalid_positive_integer() {
  local flag="$1"
  local value="$2"
  if [[ -z "$value" ]]; then
    echo "Invalid $flag: expected a positive integer, got empty value." >&2
  else
    echo "Invalid $flag: expected a positive integer, got '$value'." >&2
  fi
  exit 4
}

validate_positive_integer() {
  local flag="$1"
  local value="$2"
  if [[ ! "$value" =~ ^[1-9][0-9]*$ ]]; then
    fail_invalid_positive_integer "$flag" "$value"
  fi
}

require_option_value() {
  local flag="$1"
  local count="$2"
  if [[ "$count" -lt 2 ]]; then
    fail_invalid_positive_integer "$flag" ""
  fi
}

available_cpu_count() {
  local cpu_count=""
  if [[ -n "${RIGORLOOP_CI_CPU_COUNT_FIXTURE:-}" ]]; then
    cpu_count="$RIGORLOOP_CI_CPU_COUNT_FIXTURE"
  fi
  if [[ ! "$cpu_count" =~ ^[1-9][0-9]*$ ]] && command -v getconf >/dev/null 2>&1; then
    cpu_count="$(getconf _NPROCESSORS_ONLN 2>/dev/null || true)"
  fi
  if [[ ! "$cpu_count" =~ ^[1-9][0-9]*$ ]] && command -v nproc >/dev/null 2>&1; then
    cpu_count="$(nproc 2>/dev/null || true)"
  fi
  if [[ ! "$cpu_count" =~ ^[1-9][0-9]*$ ]]; then
    cpu_count=1
  fi
  echo "$cpu_count"
}

default_jobs() {
  local cpu_count
  cpu_count="$(available_cpu_count)"
  if [[ "$cpu_count" -gt 1 ]]; then
    echo $((cpu_count > 5 ? 4 : cpu_count - 1))
  else
    echo 1
  fi
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --mode)
        mode="${2:-}"
        shift 2
        ;;
      --path)
        paths+=("${2:-}")
        shift 2
        ;;
      --base)
        base="${2:-}"
        shift 2
        ;;
      --head)
        head="${2:-}"
        shift 2
        ;;
      --release-version)
        release_version="${2:-}"
        shift 2
        ;;
      --broad-smoke)
        broad_smoke=1
        shift
        ;;
      --jobs)
        require_option_value "$1" "$#"
        jobs="${2:-}"
        jobs_explicit=1
        validate_positive_integer "$1" "$jobs"
        shift 2
        ;;
      --timeout)
        require_option_value "$1" "$#"
        timeout_seconds="${2:-}"
        validate_positive_integer "$1" "$timeout_seconds"
        shift 2
        ;;
      --durations)
        if [[ "$#" -lt 2 || ! "${2:-}" =~ ^[0-9]+$ ]]; then
          echo "Invalid --durations: expected a nonnegative decimal integer." >&2
          exit 4
        fi
        durations="$2"
        shift 2
        ;;
      --fail-fast)
        fail_fast=1
        shift
        ;;
      --verbose)
        verbose=1
        shift
        ;;
      --skip-diff-scoped)
        skip_diff_scoped=1
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "Unknown ci.sh argument: $1" >&2
        usage >&2
        exit 4
        ;;
    esac
  done
}

parse_args "$@"

if [[ -n "${RIGORLOOP_BROAD_SMOKE_CLASSIFICATION+x}" ]]; then
  echo "RIGORLOOP_BROAD_SMOKE_CLASSIFICATION is retired; current catalog owns constraints." >&2
  exit 4
fi


if [[ -z "$jobs" ]]; then
  jobs="$(default_jobs)"
fi

# A nested wrapper may use only its parent's explicit allocation.
if [[ -n "${RIGORLOOP_VALIDATION_WORKERS:-}" ]]; then
  validate_positive_integer "parent worker allocation" "$RIGORLOOP_VALIDATION_WORKERS"
  if [[ "$jobs" -gt "$RIGORLOOP_VALIDATION_WORKERS" ]]; then
    jobs="$RIGORLOOP_VALIDATION_WORKERS"
  fi
fi

if [[ -z "$mode" ]]; then
  echo "No --mode supplied; defaulting to --mode broad-smoke for legacy compatibility."
  mode="broad-smoke"
fi

if ! command -v python >/dev/null 2>&1; then
  echo "python command not found; install Python or provide a python shim before running CI." >&2
  exit 1
fi

# The existing executor owns reporting before selection or release preparation.
python - "$mode" "$jobs" "$timeout_seconds" "$fail_fast" "$verbose" "$base" "$head" "$skip_diff_scoped" "$release_version" "$broad_smoke" "$durations" "${#paths[@]}" "${paths[@]}" "${ci_original_args[@]}" <<'PYCI'
import sys
from pathlib import Path
sys.path.insert(0, str(Path("scripts").resolve()))
from lib.validation.validation_execution import ci_main
try:
    ci_main(sys.argv[1:])
except (ValueError, OSError, TypeError, KeyError) as exc:
    print(f"Invalid validation execution: {exc}", file=sys.stderr)
    raise SystemExit(4)
PYCI
