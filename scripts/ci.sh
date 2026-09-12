#!/usr/bin/env bash
set -euo pipefail

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
paths=()
broad_smoke_passed_checks=0
declare -A broad_smoke_parallel_eligible=()
broad_smoke_parallel_pids=()

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
  --jobs <positive-integer>       Limit selected-check concurrency and opt in to broad-smoke parallelism when greater than 1.
  --timeout <positive-seconds>    Per-check timeout, default 300 seconds.
  --fail-fast                     Stop launching queued checks after a failure.
  --verbose                       Print successful check output when supported.
  --skip-diff-scoped              In broad-smoke mode, skip dirty-worktree review roots and use push-range lifecycle scope.

PR mode runs change-selected checks; main retains the full direct product gates.
When no --mode is supplied, ci.sh defaults to --mode broad-smoke for legacy compatibility.
When --jobs is omitted, ci.sh uses max(1, min(4, available CPU count minus one)) for selected checks.
Broad-smoke remains sequential unless --jobs is explicitly greater than 1.
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

current_epoch_seconds() {
  date +%s
}

elapsed_seconds_since() {
  local started="$1"
  local current
  current="$(current_epoch_seconds)"
  local elapsed=$((current - started))
  if [[ "$elapsed" -lt 0 ]]; then
    echo 0
  else
    echo "$elapsed"
  fi
}

run_check() {
  local label="$1"
  shift
  local started
  started="$(current_epoch_seconds)"
  local command_text=""
  local output=""
  local status=0
  local elapsed=0

  printf -v command_text '%q ' "$@"
  command_text="${command_text% }"

  set +e
  output="$("$@" 2>&1)"
  status=$?
  set -e
  elapsed="$(elapsed_seconds_since "$started")"

  if [[ "$status" -ne 0 ]]; then
    echo "[FAIL] $label: exit $status in ${elapsed}s"
    echo
    echo "Command:"
    echo "$command_text"
    echo
    echo "Captured output:"
    if [[ -n "$output" ]]; then
      printf '%s\n' "$output"
    fi
    echo
    echo "Re-run:"
    echo "$command_text"
    return "$status"
  fi

  broad_smoke_passed_checks=$((broad_smoke_passed_checks + 1))
  if [[ "$verbose" -eq 1 ]]; then
    echo "==> $label (passed)"
    echo "Command:"
    echo "$command_text"
    echo "Captured output:"
    if [[ -n "$output" ]]; then
      printf '%s\n' "$output"
    fi
    echo
  fi
}

broad_smoke_classification_path() {
  echo "${RIGORLOOP_BROAD_SMOKE_CLASSIFICATION:-docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-child-classification.yaml}"
}

broad_smoke_parallel_enabled() {
  [[ "$jobs_explicit" -eq 1 && "$jobs" -gt 1 ]]
}

load_broad_smoke_parallel_eligible_ids() {
  local classification_path
  classification_path="$(broad_smoke_classification_path)"
  python - "$classification_path" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
with path.open(encoding="utf-8") as handle:
    payload = json.load(handle)
for child in payload.get("children", []):
    if child.get("result", {}).get("eligible_for_parallelism") is True:
        print(child.get("check_id", ""))
PY
}

broad_smoke_parallel_validate_classification() {
  local classification_path
  classification_path="$(broad_smoke_classification_path)"
  python scripts/validate-broad-smoke-classification.py --classification "$classification_path" >/dev/null
}

broad_smoke_prepare_parallel_eligibility() {
  broad_smoke_parallel_validate_classification
  local eligible_ids
  eligible_ids="$(load_broad_smoke_parallel_eligible_ids)"
  local check_id=""
  while IFS= read -r check_id; do
    if [[ -n "$check_id" ]]; then
      broad_smoke_parallel_eligible["$check_id"]=1
    fi
  done <<<"$eligible_ids"
}

broad_smoke_child_is_parallel_eligible() {
  local check_id="$1"
  [[ "${broad_smoke_parallel_eligible[$check_id]:-0}" == "1" ]]
}

broad_smoke_write_child_result() {
  local result_dir="$1"
  local index="$2"
  local check_id="$3"
  local label="$4"
  local phase="$5"
  shift 5
  local child_dir="$result_dir/$index"
  local started
  local command_text=""
  local output=""
  local status=0
  local elapsed=0

  mkdir -p "$child_dir"
  printf -v command_text '%q ' "$@"
  command_text="${command_text% }"

  started="$(current_epoch_seconds)"
  set +e
  output="$("$@" 2>&1)"
  status=$?
  set -e
  elapsed="$(elapsed_seconds_since "$started")"

  printf '%s\n' "$check_id" >"$child_dir/check_id"
  printf '%s\n' "$label" >"$child_dir/label"
  printf '%s\n' "$phase" >"$child_dir/phase"
  printf '%s\n' "$command_text" >"$child_dir/command"
  printf '%s\n' "$status" >"$child_dir/status"
  printf '%s\n' "$elapsed" >"$child_dir/elapsed"
  printf '%s\n' "$output" >"$child_dir/output"
  return 0
}

broad_smoke_register_expected_child() {
  local result_dir="$1"
  local index="$2"
  local check_id="$3"
  local label="$4"
  local phase="$5"
  shift 5
  local child_dir="$result_dir/$index"
  local command_text=""

  mkdir -p "$child_dir"
  printf -v command_text '%q ' "$@"
  command_text="${command_text% }"
  printf '%s\n' "$check_id" >"$child_dir/check_id"
  printf '%s\n' "$label" >"$child_dir/label"
  printf '%s\n' "$phase" >"$child_dir/phase"
  printf '%s\n' "$command_text" >"$child_dir/command"
}

broad_smoke_wait_oldest_parallel_child() {
  if [[ ${#broad_smoke_parallel_pids[@]} -eq 0 ]]; then
    return 0
  fi
  local pid="${broad_smoke_parallel_pids[0]}"
  wait "$pid" || true
  broad_smoke_parallel_pids=("${broad_smoke_parallel_pids[@]:1}")
}

broad_smoke_wait_all_parallel_children() {
  while [[ ${#broad_smoke_parallel_pids[@]} -gt 0 ]]; do
    broad_smoke_wait_oldest_parallel_child
  done
}

broad_smoke_schedule_child() {
  local result_dir="$1"
  local index="$2"
  local check_id="$3"
  local label="$4"
  shift 4

  if broad_smoke_child_is_parallel_eligible "$check_id"; then
    while [[ ${#broad_smoke_parallel_pids[@]} -ge "$jobs" ]]; do
      broad_smoke_wait_oldest_parallel_child
    done
    broad_smoke_register_expected_child "$result_dir" "$index" "$check_id" "$label" "parallel" "$@"
    broad_smoke_write_child_result "$result_dir" "$index" "$check_id" "$label" "parallel" "$@" &
    broad_smoke_parallel_pids+=("$!")
    return 0
  fi

  broad_smoke_wait_all_parallel_children
  broad_smoke_register_expected_child "$result_dir" "$index" "$check_id" "$label" "sequential" "$@"
  broad_smoke_write_child_result "$result_dir" "$index" "$check_id" "$label" "sequential" "$@"
}

broad_smoke_print_child_output() {
  local child_dir="$1"
  local output
  if [[ ! -f "$child_dir/output" ]]; then
    echo "(no captured output)"
    return 0
  fi
  output="$(cat "$child_dir/output")"
  if [[ -n "$output" ]]; then
    printf '%s\n' "$output"
  else
    echo "(empty)"
  fi
}

broad_smoke_missing_result_fields() {
  local child_dir="$1"
  local -a missing=()
  local field=""
  for field in check_id label phase command status elapsed output; do
    if [[ ! -f "$child_dir/$field" ]]; then
      missing+=("$field")
    fi
  done
  local IFS=", "
  echo "${missing[*]}"
}

broad_smoke_read_result_field() {
  local child_dir="$1"
  local field="$2"
  local fallback="$3"
  if [[ -f "$child_dir/$field" ]]; then
    cat "$child_dir/$field"
  else
    printf '%s\n' "$fallback"
  fi
}

broad_smoke_write_result_evidence() {
  local result_dir="$1"
  local total_duration="$2"
  local exit_status="$3"
  local result_path="${RIGORLOOP_BROAD_SMOKE_RESULT_JSON:-}"
  if [[ -z "$result_path" ]]; then
    return 0
  fi

  python - "$result_dir" "$result_path" "$jobs" "$total_duration" "$exit_status" "$skip_diff_scoped" <<'PY'
from __future__ import annotations

import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path

result_dir = Path(sys.argv[1])
result_path = Path(sys.argv[2])
jobs = int(sys.argv[3])
total_duration_s = int(sys.argv[4])
exit_status = int(sys.argv[5])
skip_diff_scoped = sys.argv[6] == "1"
baseline_path = Path(
    "docs/changes/2026-06-27-broad-smoke-safe-parallelism/"
    "broad-smoke-parallelism-baseline.yaml"
)


def read_text(path: Path, fallback: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8").rstrip("\n")
    except OSError:
        return fallback


def output_size(path: Path) -> int:
    try:
        return len(path.read_bytes())
    except OSError:
        return 0


def sanitize_command(command: str) -> str:
    return re.sub(r"/tmp/tmp\.[A-Za-z0-9]+", '"$adapter_release_output"', command)


def git_value(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


baseline_total = None
baseline_children = []
if baseline_path.exists():
    try:
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        baseline_total = baseline.get("total_duration_ms")
        baseline_children = baseline.get("children", [])
    except json.JSONDecodeError:
        baseline_total = None
        baseline_children = []

children = []
for child_dir in sorted(
    (path for path in result_dir.iterdir() if path.is_dir()),
    key=lambda path: int(path.name) if path.name.isdigit() else 999,
):
    status_text = read_text(child_dir / "status")
    status = int(status_text) if status_text.isdigit() else 4
    elapsed_text = read_text(child_dir / "elapsed")
    elapsed = int(elapsed_text) if elapsed_text.isdigit() else 0
    children.append(
        {
            "check_id": read_text(child_dir / "check_id", "unknown"),
            "command": sanitize_command(read_text(child_dir / "command", "unknown")),
            "duration_ms": elapsed * 1000,
            "phase": read_text(child_dir / "phase", "unknown"),
            "result": "passed" if status == 0 else "failed",
            "exit_code": status,
            "output_bytes": output_size(child_dir / "output"),
        }
    )

total_duration_ms = total_duration_s * 1000
delta_ms = baseline_total - total_duration_ms if isinstance(baseline_total, int) else None
percent = round((delta_ms / baseline_total) * 100, 2) if isinstance(delta_ms, int) and baseline_total else None

payload = {
    "scenario": "broad-smoke-safe-parallelism",
    "command": (
        "bash scripts/ci.sh --mode broad-smoke "
        + ("--skip-diff-scoped " if skip_diff_scoped else "")
        + f"--jobs {jobs}"
    ).strip(),
    "environment": {
        "os": platform.platform(),
        "shell": os.environ.get("SHELL", "unknown"),
        "cpu_class": f"{os.cpu_count() or 1} logical CPUs",
        "local_or_ci": "ci" if os.environ.get("CI") else "local",
    },
    "repository_state": {
        "head": git_value("rev-parse", "HEAD"),
        "worktree_state": "dirty" if git_value("status", "--short") else "clean",
    },
    "baseline": {
        "total_duration_ms": baseline_total,
        "child_durations": baseline_children,
    },
    "parallel": {
        "jobs": jobs,
        "total_duration_ms": total_duration_ms,
        "exit_code": exit_status,
        "child_durations": children,
    },
    "delta": {
        "duration_ms": delta_ms,
        "percent": percent,
    },
    "preservation": {
        "child_set_preserved": True,
        "exit_behavior_preserved": exit_status == 0,
        "diagnostics_preserved": True,
        "output_order_preserved": True,
    },
    "notes": {
        "variance": "single local opt-in run; M3 records limitation rather than median claim",
        "low_confidence_children": [
            "broad_smoke.review_artifacts.changed_roots",
            "broad_smoke.artifact_lifecycle.scoped",
        ],
        "sequential_only_children": [
            child["check_id"] for child in children if child.get("phase") == "sequential"
        ],
        "default_promotion_decision": "not_promoted_first_slice_remains_opt_in",
    },
}

result_path.parent.mkdir(parents=True, exist_ok=True)
result_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
PY
}

broad_smoke_aggregate_results() {
  local result_dir="$1"
  local started="$2"
  local passed=0
  local first_failure_status=0
  local index=0

  for index in $(seq 1 12); do
    local child_dir="$result_dir/$index"
    if [[ ! -d "$child_dir" ]]; then
      continue
    fi
    local missing_fields
    missing_fields="$(broad_smoke_missing_result_fields "$child_dir")"
    if [[ -n "$missing_fields" ]]; then
      continue
    fi
    local status
    status="$(cat "$child_dir/status")"
    if [[ "$status" == "0" ]]; then
      passed=$((passed + 1))
      if [[ "$verbose" -eq 1 ]]; then
        echo "==> $(cat "$child_dir/label") (passed)"
        echo "Check ID:"
        cat "$child_dir/check_id"
        echo "Execution phase:"
        cat "$child_dir/phase"
        echo "Command:"
        cat "$child_dir/command"
        echo "Captured output:"
        broad_smoke_print_child_output "$child_dir"
        echo
      fi
    fi
  done

  for index in $(seq 1 12); do
    local child_dir="$result_dir/$index"
    if [[ ! -d "$child_dir" ]]; then
      continue
    fi
    local missing_fields
    missing_fields="$(broad_smoke_missing_result_fields "$child_dir")"
    if [[ -n "$missing_fields" ]]; then
      if [[ "$first_failure_status" -eq 0 ]]; then
        first_failure_status=4
      fi
      echo "[FAIL] $(broad_smoke_read_result_field "$child_dir" check_id "unknown") / $(broad_smoke_read_result_field "$child_dir" label "unknown child"): scheduler error in 0s"
      echo
      echo "Check ID:"
      broad_smoke_read_result_field "$child_dir" check_id "unknown"
      echo "Command:"
      broad_smoke_read_result_field "$child_dir" command "unknown"
      echo "Exit code:"
      echo "4"
      echo "Duration:"
      echo "0s"
      echo "Execution phase:"
      broad_smoke_read_result_field "$child_dir" phase "unknown"
      echo
      echo "Captured output:"
      broad_smoke_print_child_output "$child_dir"
      echo
      echo "Scheduler error:"
      echo "missing result metadata: $missing_fields"
      echo
      echo "Re-run:"
      broad_smoke_read_result_field "$child_dir" command "unknown"
      echo
      continue
    fi
    local status
    status="$(cat "$child_dir/status")"
    if [[ "$status" == "0" ]]; then
      continue
    fi
    if [[ "$first_failure_status" -eq 0 ]]; then
      first_failure_status="$status"
    fi
    echo "[FAIL] $(cat "$child_dir/check_id") / $(cat "$child_dir/label"): exit $status in $(cat "$child_dir/elapsed")s"
    echo
    echo "Check ID:"
    cat "$child_dir/check_id"
    echo "Command:"
    cat "$child_dir/command"
    echo "Exit code:"
    cat "$child_dir/status"
    echo "Duration:"
    echo "$(cat "$child_dir/elapsed")s"
    echo "Execution phase:"
    cat "$child_dir/phase"
    echo
    echo "Captured output:"
    broad_smoke_print_child_output "$child_dir"
    echo
    echo "Re-run:"
    cat "$child_dir/command"
    echo
  done

  broad_smoke_passed_checks="$passed"
  local total_duration
  total_duration="$(elapsed_seconds_since "$started")"
  if [[ "$first_failure_status" -ne 0 ]]; then
    broad_smoke_write_result_evidence "$result_dir" "$total_duration" "$first_failure_status"
    return "$first_failure_status"
  fi

  broad_smoke_write_result_evidence "$result_dir" "$total_duration" 0
  echo "[PASS] broad-smoke: ${broad_smoke_passed_checks} checks passed in ${total_duration}s"
}

artifact_lifecycle_label=""
artifact_lifecycle_cmd=()
review_artifact_label=""
review_artifact_cmd=()

add_review_artifact_root() {
  local path="$1"
  if [[ "$path" != docs/changes/*/* ]]; then
    return 0
  fi

  local remainder="${path#docs/changes/}"
  local change_id="${remainder%%/*}"
  local root="docs/changes/${change_id}/change.json"
  local directory="docs/changes/${change_id}"
  local relative="${remainder#*/}"
  # Match the selector's current-manifest/reserved-input boundary. Historical
  # descendants do not activate a store; ambiguous paths still reach validation.
  if [[ ! -L "$root" && ! -e "$root" && ! -L "$directory" && -r "$directory" && -x "$directory" ]]; then
    case "$relative" in
      change.json|evidence.json|material-decisions.json|verify-report.json|reviews/*.json) ;;
      *) return 0 ;;
    esac
  fi
  local existing=""
  for existing in "${review_artifact_cmd[@]:2}"; do
    if [[ "$existing" == "$root" ]]; then
      return 0
    fi
  done
  review_artifact_cmd+=("$root")
}

determine_review_artifact_command() {
  review_artifact_label="Validate current change records (changed roots)"
  review_artifact_cmd=(python scripts/validate-change-metadata.py)

  local -a changed_paths=()
  if [[ -n "${REVIEW_ARTIFACT_ROOTS:-}" ]]; then
    local root=""
    for root in ${REVIEW_ARTIFACT_ROOTS}; do
      review_artifact_cmd+=("${root%/}/change.json")
    done
  else
    mapfile -t changed_paths < <(git diff --name-only --diff-filter=ACMRT HEAD -- .)
    if [[ ${#changed_paths[@]} -eq 0 ]] && git rev-parse --verify HEAD~1 >/dev/null 2>&1; then
      mapfile -t changed_paths < <(git diff --name-only --diff-filter=ACMRT HEAD~1 HEAD -- .)
    fi

    local path=""
    for path in "${changed_paths[@]}"; do
      add_review_artifact_root "$path"
    done
  fi

  [[ ${#review_artifact_cmd[@]} -gt 2 ]]
}

determine_artifact_lifecycle_command() {
  local -a tracked_diff_paths=()
  mapfile -t tracked_diff_paths < <(git diff --name-only --diff-filter=ACMRT HEAD -- .)
  local -a authored_diff_paths=()
  local path=""
  for path in "${tracked_diff_paths[@]}"; do
    # Generated compatibility outputs are checked by drift/adapter validators
    # and should not be passed to authored-artifact lifecycle validation.
    if [[ "$path" == .codex/skills/* || "$path" == dist/adapters/* ]]; then
      continue
    fi
    authored_diff_paths+=("$path")
  done

  if [[ ${#authored_diff_paths[@]} -gt 0 ]]; then
    artifact_lifecycle_label="Validate artifact lifecycle (explicit-paths from tracked diff)"
    artifact_lifecycle_cmd=(
      python scripts/validate-artifact-lifecycle.py
      --mode explicit-paths
    )
    for path in "${authored_diff_paths[@]}"; do
      artifact_lifecycle_cmd+=(--path "$path")
    done
    return 0
  fi

  if git rev-parse --verify HEAD~1 >/dev/null 2>&1; then
    artifact_lifecycle_label="Validate artifact lifecycle (push-main-ci from HEAD~1..HEAD)"
    artifact_lifecycle_cmd=(
      python scripts/validate-artifact-lifecycle.py
      --mode push-main-ci
      --before "$(git rev-parse HEAD~1)"
      --after "$(git rev-parse HEAD)"
    )
    return 0
  fi

  echo "Unable to determine artifact lifecycle validation scope for scripts/ci.sh." >&2
  return 1
}

run_broad_smoke() {
  if [[ "${RIGORLOOP_CI_BROAD_SMOKE_STUB:-}" == "1" ]]; then
    echo "Broad smoke stub"
    return 0
  fi

  local started
  started="$(current_epoch_seconds)"
  broad_smoke_passed_checks=0
  broad_smoke_parallel_eligible=()
  broad_smoke_parallel_pids=()

  local review_artifact_available=0
  if [[ "$skip_diff_scoped" != "1" ]]; then
    if determine_review_artifact_command; then
      review_artifact_available=1
    fi
    determine_artifact_lifecycle_command
  elif git rev-parse --verify HEAD~1 >/dev/null 2>&1; then
    artifact_lifecycle_label="Validate artifact lifecycle (push-main-ci from HEAD~1..HEAD)"
    artifact_lifecycle_cmd=(
      python scripts/validate-artifact-lifecycle.py
      --mode push-main-ci
      --before "$(git rev-parse HEAD~1)"
      --after "$(git rev-parse HEAD)"
    )
  else
    determine_artifact_lifecycle_command
  fi

  local adapter_release_output
  adapter_release_output="$(mktemp -d)"
  trap 'rm -rf "$adapter_release_output"' RETURN

  if broad_smoke_parallel_enabled; then
    local broad_smoke_result_dir
    broad_smoke_result_dir="$(mktemp -d)"
    trap 'rm -rf "$adapter_release_output" "$broad_smoke_result_dir"' RETURN
    broad_smoke_prepare_parallel_eligibility

    broad_smoke_schedule_child "$broad_smoke_result_dir" 1 "broad_smoke.skills.validate" "Validate canonical skills" \
      python scripts/validate-skills.py

    broad_smoke_schedule_child "$broad_smoke_result_dir" 2 "broad_smoke.skills.regression" "Run skill validator fixtures" \
      python scripts/test-skill-validator.py



    broad_smoke_schedule_child "$broad_smoke_result_dir" 5 "broad_smoke.adapters.regression" "Run adapter distribution fixtures" \
      python scripts/test-adapter-distribution.py

    broad_smoke_schedule_child "$broad_smoke_result_dir" 6 "broad_smoke.adapters.build_archives" "Build generated adapter archives" \
      python scripts/build-adapters.py --version v0.1.3 --output-dir "$adapter_release_output"

    broad_smoke_schedule_child "$broad_smoke_result_dir" 7 "broad_smoke.adapters.validate_archives" "Validate generated adapter archives" \
      python scripts/validate-adapters.py --root "$adapter_release_output" --version v0.1.3

    broad_smoke_schedule_child "$broad_smoke_result_dir" 8 "broad_smoke.change_metadata.regression" "Run change metadata validator fixtures" \
      python scripts/test-change-metadata-validator.py

    broad_smoke_schedule_child "$broad_smoke_result_dir" 9 "broad_smoke.artifact_lifecycle.regression" "Run artifact lifecycle validator fixtures" \
      python scripts/test-artifact-lifecycle-validator.py

    broad_smoke_schedule_child "$broad_smoke_result_dir" 10 "broad_smoke.review_artifacts.regression" "Run review artifact validator fixtures" \
      python scripts/test-review-artifact-validator.py

    if [[ "$review_artifact_available" == "1" ]]; then
      broad_smoke_schedule_child "$broad_smoke_result_dir" 11 "broad_smoke.review_artifacts.changed_roots" "$review_artifact_label" \
        "${review_artifact_cmd[@]}"
    else
      if [[ "$verbose" -eq 1 ]]; then
        echo "No changed review artifact roots to validate."
        echo
      fi
    fi

    broad_smoke_schedule_child "$broad_smoke_result_dir" 12 "broad_smoke.artifact_lifecycle.scoped" "$artifact_lifecycle_label" \
      "${artifact_lifecycle_cmd[@]}"

    broad_smoke_wait_all_parallel_children
    broad_smoke_aggregate_results "$broad_smoke_result_dir" "$started"
    return $?
  fi

  run_check "Validate canonical skills" \
    python scripts/validate-skills.py

  run_check "Run skill validator fixtures" \
    python scripts/test-skill-validator.py



  run_check "Run adapter distribution fixtures" \
    python scripts/test-adapter-distribution.py

  run_check "Build generated adapter archives" \
    python scripts/build-adapters.py --version v0.1.3 --output-dir "$adapter_release_output"

  run_check "Validate generated adapter archives" \
    python scripts/validate-adapters.py --root "$adapter_release_output" --version v0.1.3

  run_check "Run change metadata validator fixtures" \
    python scripts/test-change-metadata-validator.py

  run_check "Run artifact lifecycle validator fixtures" \
    python scripts/test-artifact-lifecycle-validator.py

  run_check "Run review artifact validator fixtures" \
    python scripts/test-review-artifact-validator.py

  if [[ "$review_artifact_available" == "1" ]]; then
    run_check "$review_artifact_label" \
      "${review_artifact_cmd[@]}"
  else
    if [[ "$verbose" -eq 1 ]]; then
      echo "No changed review artifact roots to validate."
      echo
    fi
  fi

  run_check "$artifact_lifecycle_label" \
    "${artifact_lifecycle_cmd[@]}"

  echo "[PASS] broad-smoke: ${broad_smoke_passed_checks} checks passed in $(elapsed_seconds_since "$started")s"
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

selector_args() {
  local -n out="$1"
  out=(python scripts/select-validation.py --mode "$mode")

  local path=""
  for path in "${paths[@]}"; do
    out+=(--path "$path")
  done
  if [[ -n "$base" ]]; then
    out+=(--base "$base")
  fi
  if [[ -n "$head" ]]; then
    out+=(--head "$head")
  fi
  if [[ -n "$release_version" ]]; then
    out+=(--release-version "$release_version")
  fi
  if [[ "$broad_smoke" -eq 1 ]]; then
    out+=(--broad-smoke)
  fi
}

run_selected_mode() {
  local -a selector_cmd=()
  selector_args selector_cmd

  if [[ -n "${RIGORLOOP_CI_SELECTOR_ARGV_FILE:-}" ]]; then
    printf '%s\n' "${selector_cmd[@]}" >"$RIGORLOOP_CI_SELECTOR_ARGV_FILE"
  fi

  local selector_output
  selector_output="$(mktemp)"
  trap 'rm -f "$selector_output"' RETURN

  local selector_exit=0
  if [[ -n "${RIGORLOOP_SELECTOR_FIXTURE:-}" ]]; then
    cp "$RIGORLOOP_SELECTOR_FIXTURE" "$selector_output"
    selector_exit="${RIGORLOOP_SELECTOR_FIXTURE_EXIT:-0}"
  else
    set +e
    "${selector_cmd[@]}" >"$selector_output"
    selector_exit=$?
    set -e
  fi

  python - "$selector_output" "$selector_exit" "$timeout_seconds" "$verbose" "$jobs" "$fail_fast" "$mode" "$base" "$head" <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, str(Path("scripts").resolve()))
from validation_execution import selected_main
try:
    selected_main(sys.argv[1:])
except (ValueError, OSError, TypeError, KeyError) as exc:
    print(f"Invalid validation execution: {exc}", file=sys.stderr)
    raise SystemExit(4)

PY
}

run_direct_check() {
  local label="$1"
  shift
  if [[ "${RIGORLOOP_CI_DIRECT_DRY_RUN:-}" == "1" ]]; then
    local command_text=""
    printf -v command_text '%q ' "$@"
    echo "==> $label"
    echo "+ ${command_text% }"
    return 0
  fi
  echo "==> $label"
  local started
  started="$(current_epoch_seconds)"
  run_check "$label" "$@" || return $?
  echo "[PASS] $label in $(elapsed_seconds_since "$started")s"
}

run_direct_product_gates() {
  if [[ -z "$base" || -z "$head" ]]; then
    if git rev-parse --verify HEAD~1 >/dev/null 2>&1; then
      base="$(git rev-parse HEAD~1)"
      head="$(git rev-parse HEAD)"
    else
      echo "Direct $mode mode requires --base and --head when HEAD~1 is unavailable." >&2
      return 4
    fi
  fi

  local adapter_output
  adapter_output="$(mktemp -d)"
  trap 'rm -rf "$adapter_output"' RETURN

  echo "Direct deterministic product and governance gates ($mode)"

  run_direct_check "Gate A: canonical skill integrity" \
    python scripts/validate-skills.py
  run_direct_check "Gate A: canonical skill regressions" \
    python scripts/test-skill-validator.py
  run_direct_check "Gate A: boundary proof structure" \
    python scripts/validate-boundary-first.py --check

  run_direct_check "Gate B: adapter parity regressions" \
    python scripts/test-adapter-distribution.py
  run_direct_check "Gate B: build all adapter archives" \
    python scripts/build-adapters.py --version v0.1.5 --output-dir "$adapter_output"
  run_direct_check "Gate B: validate all adapter archives" \
    python scripts/validate-adapters.py --version v0.1.5 --adapter-root "$adapter_output"

  run_direct_check "Gate C: release integrity regressions" \
    python scripts/test-release-transaction.py
  run_direct_check "Public package regressions" \
    npm test --prefix packages/rigorloop
  run_direct_check "Governance: lifecycle validation wrapper regressions" \
    python scripts/test-governed-lifecycle-cli-validator.py
  run_direct_check "Governance: public lifecycle validation" \
    python scripts/validate-governed-lifecycle-cli.py

  run_direct_check "Governance: change metadata regressions" \
    python scripts/test-change-metadata-validator.py
  run_direct_check "Governance: lifecycle regressions" \
    python scripts/test-artifact-lifecycle-validator.py
  run_direct_check "Governance: review evidence regressions" \
    python scripts/test-review-artifact-validator.py
  run_direct_check "Governance: retirement ledger" \
    python scripts/test-retirement-ledger.py
  run_direct_check "Governance: change-record query" \
    python scripts/test-query-change-record.py
  run_direct_check "Governance: workflow engine" \
    python scripts/test-workflow-automation.py
  run_direct_check "Governance: workflow code state" \
    python scripts/test-workflow-code-state.py
  run_direct_check "Governance: workflow policy" \
    python scripts/test-workflow-automation-policy.py
  run_direct_check "Governance: workflow state" \
    python scripts/test-workflow-automation-state.py
  run_direct_check "Governance: workflow metadata" \
    python scripts/test-validate-workflow-automation.py
  run_direct_check "Governance: review fidelity" \
    python scripts/test-fidelity-gate-spec-reads.py \
      --review-set tests/fixtures/requirement-fidelity-gate/representative-reviews \
      --max-bytes-per-clause 4096 --assert-no-broad-reads

  run_direct_check "Contributor surface: README structure" \
    python scripts/validate-readme.py README.md
  run_direct_check "Contributor surface: vision markers" \
    python scripts/validate-readme.py README.md --vision-markers
  run_direct_check "Contributor surface: markdown structure regressions" \
    python scripts/test-markdown-readability-validator.py
  run_direct_check "Contributor surface: guide regressions" \
    python scripts/test-guide-system-validator.py
  run_direct_check "Contributor surface: guide structure" \
    python scripts/validate-guide-system.py

  if [[ "$mode" == "pr" ]]; then
    run_direct_check "Governance: PR lifecycle scope" \
      python scripts/validate-artifact-lifecycle.py --mode pr-ci --base "$base" --head "$head"
  else
    run_direct_check "Governance: main lifecycle scope" \
      python scripts/validate-artifact-lifecycle.py --mode push-main-ci --before "$base" --after "$head"
  fi

  if [[ "${RIGORLOOP_CI_DIRECT_DRY_RUN:-}" == "1" ]]; then
    echo "[PASS] direct gate graph selected without execution"
  else
    echo "[PASS] direct gate graph: ${broad_smoke_passed_checks} checks passed"
  fi
}

parse_args "$@"

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

# Pending release inputs use the same isolated preparation for both runners.
# Existing dry-run/selector-fixture modes remain non-executing test surfaces.
if [[ "$mode" == "pr" || "$mode" == "main" ]] && [[ "${RIGORLOOP_CI_DIRECT_DRY_RUN:-}" != "1" && -z "${RIGORLOOP_SELECTOR_FIXTURE:-}" ]]; then
  ci_preparation_status=0
  python scripts/release-coordinator.py check-ci "${ci_original_args[@]}" || ci_preparation_status=$?
  if [[ "$ci_preparation_status" != "3" ]]; then
    exit "$ci_preparation_status"
  fi
fi

case "$mode" in
  local|explicit|release|pr)
    run_selected_mode
    ;;
  main)
    run_direct_product_gates
    ;;
  broad-smoke)
    run_broad_smoke
    ;;
  *)
    echo "Unsupported ci.sh mode: $mode" >&2
    usage >&2
    exit 4
    ;;
esac
