#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

DEFAULT_TIMEOUT_SECONDS=60

mode=""
base=""
head=""
release_version=""
broad_smoke=0
jobs=""
timeout_seconds="$DEFAULT_TIMEOUT_SECONDS"
fail_fast=0
verbose=0
paths=()

usage() {
  cat <<'EOF'
Usage:
  bash scripts/ci.sh --mode local [--path <path>...]
  bash scripts/ci.sh --mode explicit --path <path>... [--broad-smoke]
  bash scripts/ci.sh --mode pr --base <sha> --head <sha>
  bash scripts/ci.sh --mode main --base <sha> --head <sha>
  bash scripts/ci.sh --mode release --release-version <version>
  bash scripts/ci.sh --mode broad-smoke

Execution options:
  --jobs <positive-integer>       Limit selected-check concurrency.
  --timeout <positive-seconds>    Per-check timeout, default 60 seconds.
  --fail-fast                     Stop launching queued checks after a failure.
  --verbose                       Print successful check output when supported.

When no --mode is supplied, ci.sh defaults to --mode broad-smoke for legacy compatibility.
When --jobs is omitted, ci.sh uses available CPU count minus one with a floor of one.
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
  if command -v getconf >/dev/null 2>&1; then
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

  run_check "Validate canonical skills" \
    python scripts/validate-skills.py

  run_check "Run skill validator fixtures" \
    python scripts/test-skill-validator.py

  run_check "Check generated skill drift" \
    python scripts/build-skills.py --check

  run_check "Run adapter distribution fixtures" \
    python scripts/test-adapter-distribution.py

  run_check "Check generated adapter drift" \
    python scripts/build-adapters.py --version 0.1.1 --check

  run_check "Validate generated adapters" \
    python scripts/validate-adapters.py --version 0.1.1

  run_check "Run change metadata validator fixtures" \
    python scripts/test-change-metadata-validator.py

  run_check "Run artifact lifecycle validator fixtures" \
    python scripts/test-artifact-lifecycle-validator.py

  run_check "Run review artifact validator fixtures" \
    python scripts/test-review-artifact-validator.py

  if determine_review_artifact_command; then
    run_check "$review_artifact_label" \
      "${review_artifact_cmd[@]}"
  else
    echo "No changed review artifact roots to validate."
    echo
  fi

  determine_artifact_lifecycle_command
  run_check "$artifact_lifecycle_label" \
    "${artifact_lifecycle_cmd[@]}"

  echo "CI broad smoke checks passed."
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

  python - "$selector_output" "$selector_exit" "$timeout_seconds" "$verbose" <<'PY'
from __future__ import annotations

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

from validation_selection import DEFAULT_ADAPTER_VERSION, catalog_command  # noqa: E402


def fail(message: str, code: int = 4) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


@dataclass
class CheckPlan:
    check_id: str
    command: str
    args: list[str]
    reason: str | None


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


def print_summary(results: list[CheckResult]) -> None:
    print("Selected CI check summary:")
    print("check ID | status | exit reason | elapsed")
    for result in results:
        print(
            f"{result.plan.check_id} | {result.status} | {result.exit_reason} | "
            f"{result.elapsed_seconds:.2f}s"
        )


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
    if check_id == "broad_smoke.repo":
        args = ["bash", "scripts/ci.sh", "--mode", "broad-smoke"]
    reason = check.get("reason")
    plans.append(CheckPlan(check_id=check_id, command=expected_command, args=args, reason=reason if isinstance(reason, str) else None))

for plan in plans:
    print(f"==> Run selected check: {plan.check_id}")
    if plan.reason:
        print(f"Reason: {plan.reason}")
    print("+ " + command_display(plan.args))

results = []
for plan in plans:
    # broad_smoke.repo delegates to the non-recursive broad-smoke path. Do
    # not add a selected-check outer timeout around that wrapper delegation.
    check_timeout = None if plan.check_id == "broad_smoke.repo" else timeout_seconds
    results.append(run_one_check(plan, timeout_seconds=check_timeout))
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
