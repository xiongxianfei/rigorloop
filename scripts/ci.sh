#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mode=""
base=""
head=""
release_version=""
broad_smoke=0
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

When no --mode is supplied, ci.sh defaults to --mode broad-smoke for legacy compatibility.
EOF
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

  python - "$selector_output" "$selector_exit" <<'PY'
from __future__ import annotations

import json
import shlex
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path("scripts").resolve()))

from validation_selection import DEFAULT_ADAPTER_VERSION, catalog_command  # noqa: E402


def fail(message: str, code: int = 4) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


selector_output = Path(sys.argv[1])
selector_exit = int(sys.argv[2])
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
    print(f"==> Run selected check: {check_id}")
    if check.get("reason"):
        print(f"Reason: {check['reason']}")
    print("+ " + " ".join(shlex.quote(arg) for arg in args))

    if check_id == "broad_smoke.repo":
        args = ["bash", "scripts/ci.sh", "--mode", "broad-smoke"]

    if args[0] in {"python", "bash"} and len(args) > 1 and args[1].startswith("scripts/"):
        if not Path(args[1]).exists():
            fail(f"Selected check {check_id} command is unavailable: {args[1]}", code=127)

    try:
        completed = subprocess.run(args)
    except FileNotFoundError as exc:
        fail(f"Selected check {check_id} command is unavailable: {exc.filename}", code=127)
    if completed.returncode != 0:
        fail(f"Selected check {check_id} failed with exit code {completed.returncode}", code=completed.returncode)
    print()

print("Selected CI checks passed.")
PY
}

parse_args "$@"

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
