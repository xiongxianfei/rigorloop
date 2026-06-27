#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

DEFAULT_TIMEOUT_SECONDS=300

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

When no --mode is supplied, ci.sh defaults to --mode broad-smoke for legacy compatibility.
When --jobs is omitted, ci.sh uses available CPU count minus one with a floor of one for selected checks.
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
    echo $((cpu_count - 1))
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
  local root="docs/changes/${change_id}"
  local existing=""
  for existing in "${review_artifact_cmd[@]:2}"; do
    if [[ "$existing" == "$root" ]]; then
      return 0
    fi
  done
  review_artifact_cmd+=("$root")
}

determine_review_artifact_command() {
  review_artifact_label="Validate review artifacts (changed roots)"
  review_artifact_cmd=(python scripts/validate-review-artifacts.py)

  local -a changed_paths=()
  if [[ -n "${REVIEW_ARTIFACT_ROOTS:-}" ]]; then
    local root=""
    for root in ${REVIEW_ARTIFACT_ROOTS}; do
      review_artifact_cmd+=("$root")
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

    broad_smoke_schedule_child "$broad_smoke_result_dir" 3 "broad_smoke.skills.generation_regression" "Run local skill mirror generation fixtures" \
      python scripts/test-build-skills.py

    broad_smoke_schedule_child "$broad_smoke_result_dir" 4 "broad_smoke.skills.drift" "Validate generated skill mirror output" \
      python scripts/build-skills.py --check

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

  run_check "Run local skill mirror generation fixtures" \
    python scripts/test-build-skills.py

  run_check "Validate generated skill mirror output" \
    python scripts/build-skills.py --check

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

  python - "$selector_output" "$selector_exit" "$timeout_seconds" "$verbose" "$jobs" "$fail_fast" <<'PY'
from __future__ import annotations

from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
import json
import os
import shlex
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path("scripts").resolve()))

from validation_selection import DEFAULT_ADAPTER_VERSION, catalog_command, is_parallel_safe_check  # noqa: E402


def fail(message: str, code: int = 4) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


@dataclass
class CheckPlan:
    check_id: str
    command: str
    args: list[str]
    reason: str | None
    phase: str
    parallel_safe: bool


@dataclass
class CheckResult:
    plan: CheckPlan
    status: str
    exit_reason: str
    elapsed_seconds: float
    stdout_bytes: bytes
    stderr_bytes: bytes
    exit_code: int
    stdout_text: str = ""
    stderr_text: str = ""
    stdout_decode_error: bool = False
    stderr_decode_error: bool = False


def command_display(args: list[str]) -> str:
    return " ".join(shlex.quote(arg) for arg in args)


def unavailable_script_path(args: list[str]) -> str | None:
    if not args:
        return "empty command"
    if args[0] in {"python", "bash"} and len(args) > 1 and args[1].startswith("scripts/"):
        if not Path(args[1]).exists():
            return args[1]
    return None


def signal_label(signal_number: int) -> str:
    try:
        return signal.Signals(signal_number).name
    except ValueError:
        return f"signal {signal_number}"


def decode_stream(data: bytes) -> tuple[str, bool]:
    try:
        return data.decode("utf-8"), False
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace"), True


def prepare_output(result: CheckResult) -> None:
    result.stdout_text, result.stdout_decode_error = decode_stream(result.stdout_bytes)
    result.stderr_text, result.stderr_decode_error = decode_stream(result.stderr_bytes)
    notes = []
    if result.stdout_decode_error:
        notes.append("stdout decode error")
    if result.stderr_decode_error:
        notes.append("stderr decode error")
    if notes:
        result.exit_reason = result.exit_reason + "; " + "; ".join(notes)


def not_started_result(plan: CheckPlan) -> CheckResult:
    return CheckResult(
        plan=plan,
        status="not started",
        exit_reason="fail-fast cancelled remaining queue",
        elapsed_seconds=0.0,
        stdout_bytes=b"",
        stderr_bytes=b"",
        exit_code=125,
    )


def run_one_check(plan: CheckPlan, *, timeout_seconds: int | None) -> CheckResult:
    unavailable = unavailable_script_path(plan.args)
    if unavailable is not None:
        return CheckResult(
            plan=plan,
            status="unavailable",
            exit_reason=f"command unavailable: {unavailable}",
            elapsed_seconds=0.0,
            stdout_bytes=b"",
            stderr_bytes=b"",
            exit_code=127,
        )

    start = time.monotonic()
    try:
        process = subprocess.Popen(
            plan.args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
    except FileNotFoundError as exc:
        return CheckResult(
            plan=plan,
            status="unavailable",
            exit_reason=f"command unavailable: {exc.filename}",
            elapsed_seconds=0.0,
            stdout_bytes=b"",
            stderr_bytes=b"",
            exit_code=127,
        )

    try:
        stdout_bytes, stderr_bytes = process.communicate(timeout=timeout_seconds)
        elapsed = time.monotonic() - start
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        except OSError:
            process.kill()
        stdout_bytes, stderr_bytes = process.communicate()
        elapsed = time.monotonic() - start
        return CheckResult(
            plan=plan,
            status="timed out",
            exit_reason=f"timeout after {timeout_seconds}s",
            elapsed_seconds=elapsed,
            stdout_bytes=stdout_bytes,
            stderr_bytes=stderr_bytes,
            exit_code=124,
        )

    return_code = process.returncode
    if return_code == 0:
        return CheckResult(
            plan=plan,
            status="passed",
            exit_reason="ok",
            elapsed_seconds=elapsed,
            stdout_bytes=stdout_bytes,
            stderr_bytes=stderr_bytes,
            exit_code=0,
        )
    if return_code < 0:
        signal_number = -return_code
        return CheckResult(
            plan=plan,
            status="killed",
            exit_reason=f"signal {signal_label(signal_number)} ({signal_number})",
            elapsed_seconds=elapsed,
            stdout_bytes=stdout_bytes,
            stderr_bytes=stderr_bytes,
            exit_code=128 + signal_number,
        )
    return CheckResult(
        plan=plan,
        status="exited",
        exit_reason=f"exit code {return_code}",
        elapsed_seconds=elapsed,
        stdout_bytes=stdout_bytes,
        stderr_bytes=stderr_bytes,
        exit_code=return_code,
    )


def check_timeout_for(plan: CheckPlan, timeout_seconds: int) -> int | None:
    # broad_smoke.repo delegates to the non-recursive broad-smoke path. Do
    # not add a selected-check outer timeout around that wrapper delegation.
    if plan.check_id == "broad_smoke.repo":
        return None
    return timeout_seconds


def run_planned_check(plan: CheckPlan, *, timeout_seconds: int) -> CheckResult:
    return run_one_check(plan, timeout_seconds=check_timeout_for(plan, timeout_seconds))


def runner_error_result(plan: CheckPlan, exc: BaseException) -> CheckResult:
    return CheckResult(
        plan=plan,
        status="exited",
        exit_reason=f"runner error: {exc}",
        elapsed_seconds=0.0,
        stdout_bytes=b"",
        stderr_bytes=b"",
        exit_code=4,
    )


def run_parallel_safe_chunk(
    chunk: list[CheckPlan],
    *,
    jobs: int,
    timeout_seconds: int,
    fail_fast: bool,
) -> list[CheckResult]:
    results: list[CheckResult | None] = [None] * len(chunk)
    next_to_start = 0
    stop_launching = False
    max_workers = min(jobs, len(chunk))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        running: dict[Future[CheckResult], int] = {}

        def launch_next() -> None:
            nonlocal next_to_start
            future = executor.submit(
                run_planned_check,
                chunk[next_to_start],
                timeout_seconds=timeout_seconds,
            )
            running[future] = next_to_start
            next_to_start += 1

        while next_to_start < len(chunk) and len(running) < max_workers:
            launch_next()

        while running:
            done, _ = wait(running, return_when=FIRST_COMPLETED)
            for future in done:
                result_index = running.pop(future)
                try:
                    result = future.result()
                except BaseException as exc:  # pragma: no cover - defensive runner boundary
                    result = runner_error_result(chunk[result_index], exc)
                results[result_index] = result
                if fail_fast and result.status != "passed":
                    stop_launching = True
            while (
                not stop_launching
                and next_to_start < len(chunk)
                and len(running) < max_workers
            ):
                launch_next()

    if stop_launching:
        while next_to_start < len(chunk):
            results[next_to_start] = not_started_result(chunk[next_to_start])
            next_to_start += 1

    return [result for result in results if result is not None]


def run_scheduled_checks(
    plans: list[CheckPlan],
    *,
    jobs: int,
    timeout_seconds: int,
    fail_fast: bool,
) -> list[CheckResult]:
    results: list[CheckResult] = []
    index = 0
    stop_launching = False

    while index < len(plans):
        if stop_launching:
            results.extend(not_started_result(plan) for plan in plans[index:])
            break

        plan = plans[index]
        if plan.parallel_safe and jobs > 1:
            chunk: list[CheckPlan] = []
            while index < len(plans) and plans[index].parallel_safe:
                chunk.append(plans[index])
                index += 1
            chunk_results = run_parallel_safe_chunk(
                chunk,
                jobs=jobs,
                timeout_seconds=timeout_seconds,
                fail_fast=fail_fast,
            )
            results.extend(chunk_results)
            if fail_fast and any(result.status != "passed" for result in chunk_results):
                stop_launching = True
            continue

        result = run_planned_check(plan, timeout_seconds=timeout_seconds)
        results.append(result)
        index += 1
        if fail_fast and result.status != "passed":
            stop_launching = True

    return results


def print_summary(results: list[CheckResult]) -> None:
    print("Selected CI check summary:")
    print("check ID | status | exit reason | elapsed")
    for result in results:
        print(
            f"{result.plan.check_id} | {result.status} | {result.exit_reason} | "
            f"{result.elapsed_seconds:.2f}s"
        )
    print("Selected CI check phases:")
    print("check ID | phase")
    for result in results:
        print(f"{result.plan.check_id} | {result.plan.phase}")
    phase_totals: dict[str, float] = {}
    for result in results:
        phase_totals[result.plan.phase] = phase_totals.get(result.plan.phase, 0.0) + result.elapsed_seconds
    if phase_totals:
        print("Selected CI phase timing summary:")
        for phase in sorted(phase_totals):
            print(f"{phase} | {phase_totals[phase]:.2f}s")


def print_stream(label: str, text: str, *, decode_error: bool) -> None:
    if decode_error:
        print(f"--- {label} (decode error; replacement text) ---")
    else:
        print(f"--- {label} ---")
    if text:
        print(text, end="" if text.endswith("\n") else "\n")
    else:
        print("(empty)")


def print_result_output(results: list[CheckResult], *, verbose: bool) -> None:
    printable = [result for result in results if verbose or result.status != "passed"]
    if not printable:
        return
    if verbose:
        print("Selected check output:")
    else:
        print("Failed selected check output:")
    for result in printable:
        print(f"==> {result.plan.check_id} ({result.status})")
        print("Command: " + command_display(result.plan.args))
        if result.stdout_bytes:
            print_stream("stdout", result.stdout_text, decode_error=result.stdout_decode_error)
        if result.stderr_bytes:
            print_stream("stderr", result.stderr_text, decode_error=result.stderr_decode_error)
        if not result.stdout_bytes and not result.stderr_bytes:
            print("(no captured output)")


selector_output = Path(sys.argv[1])
selector_exit = int(sys.argv[2])
timeout_seconds = int(sys.argv[3])
verbose = bool(int(sys.argv[4]))
jobs = int(sys.argv[5])
fail_fast = bool(int(sys.argv[6]))
try:
    payload = json.loads(selector_output.read_text(encoding="utf-8"))
except json.JSONDecodeError as exc:
    fail(f"Malformed selector JSON: {exc}")

required_fields = {
    "mode",
    "status",
    "changed_paths",
    "classified_paths",
    "unclassified_paths",
    "selected_checks",
    "affected_roots",
    "broad_smoke_required",
    "blocking_results",
    "preflight_results",
    "rationale",
}
missing = sorted(required_fields - set(payload))
if missing:
    fail(f"Selector JSON missing required fields: {', '.join(missing)}")

mode = payload["mode"]
status = payload["status"]
print(f"Selector mode: {mode}")
print(f"Selector status: {status}")
if payload.get("changed_paths"):
    print("Changed paths: " + ", ".join(payload["changed_paths"]))
if payload.get("affected_roots"):
    print("Affected roots: " + ", ".join(payload["affected_roots"]))
if payload.get("broad_smoke_required"):
    print("Broad smoke required: true")
    for source in payload.get("broad_smoke", {}).get("sources", []):
        print(f"Broad smoke source: {source}")
if payload.get("preflight_results"):
    print("Preflight results:")
    for result in payload["preflight_results"]:
        line = f"- {result.get('check')}: {result.get('result')}"
        if result.get("path"):
            line += f" ({result.get('path')})"
        if result.get("corrective_action"):
            line += f"; action: {result.get('corrective_action')}"
        print(line)

if status == "blocked":
    for result in payload["blocking_results"]:
        print(f"Blocking result: {result}", file=sys.stderr)
    raise SystemExit(2)
if status == "fallback":
    print("Selector status: fallback; fallback execution is not supported in v1.", file=sys.stderr)
    raise SystemExit(3)
if status == "error":
    for result in payload["blocking_results"]:
        print(f"Selector error: {result}", file=sys.stderr)
    raise SystemExit(4)
if status != "ok":
    fail(f"Unsupported selector status: {status}")
if selector_exit != 0:
    fail(f"Selector exited {selector_exit} while reporting status ok")

selected_checks = payload["selected_checks"]
if not selected_checks:
    print("No selected checks to run.")
    raise SystemExit(0)

plans: list[CheckPlan] = []
for check in selected_checks:
    check_id = check.get("id")
    if not isinstance(check_id, str):
        fail(f"Selected check missing string id: {check}")
    paths = tuple(check.get("paths", []))
    affected_roots = tuple(check.get("affected_roots", []))
    versions = tuple(check.get("versions", []))
    try:
        expected_command = catalog_command(
            check_id,
            paths=paths,
            affected_roots=affected_roots,
            versions=versions,
            adapter_version=DEFAULT_ADAPTER_VERSION,
        )
    except ValueError as exc:
        fail(f"Selected check {check_id} cannot be converted to a trusted command: {exc}")

    command = check.get("command")
    if command != expected_command:
        fail(
            f"Selected check {check_id} command does not match catalog: "
            f"expected {expected_command!r}, got {command!r}"
        )

    args = shlex.split(expected_command)
    reason = check.get("reason")
    phase = check.get("phase", "focused")
    if phase not in {"preflight", "focused", "boundary"}:
        fail(f"Selected check {check_id} has unsupported phase: {phase!r}")
    plans.append(
        CheckPlan(
            check_id=check_id,
            command=expected_command,
            args=args,
            reason=reason if isinstance(reason, str) else None,
            phase=phase,
            parallel_safe=is_parallel_safe_check(check_id),
        )
    )

for plan in plans:
    print(f"==> Run selected check: {plan.check_id}")
    print(f"Phase: {plan.phase}")
    if plan.reason:
        print(f"Reason: {plan.reason}")
    print("+ " + command_display(plan.args))

results = run_scheduled_checks(
    plans,
    jobs=jobs,
    timeout_seconds=timeout_seconds,
    fail_fast=fail_fast,
)
for result in results:
    prepare_output(result)

print_summary(results)
print_result_output(results, verbose=verbose)

failed_results = [result for result in results if result.status != "passed"]
if failed_results:
    for result in failed_results:
        print(f"Selected check {result.plan.check_id} failed: {result.exit_reason}", file=sys.stderr)
    raise SystemExit(failed_results[0].exit_code)

print("Selected CI checks passed.")
PY
}

parse_args "$@"

if [[ -z "$jobs" ]]; then
  jobs="$(default_jobs)"
fi

if [[ -z "$mode" ]]; then
  echo "No --mode supplied; defaulting to --mode broad-smoke for legacy compatibility."
  mode="broad-smoke"
fi

if ! command -v python >/dev/null 2>&1; then
  echo "python command not found; install Python or provide a python shim before running CI." >&2
  exit 1
fi

case "$mode" in
  local|explicit|pr|main|release)
    run_selected_mode
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
