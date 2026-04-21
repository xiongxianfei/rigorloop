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

artifact_lifecycle_label=""
artifact_lifecycle_cmd=()

determine_artifact_lifecycle_command() {
  if [[ -n "${ARTIFACT_LIFECYCLE_MODE:-}" ]]; then
    case "${ARTIFACT_LIFECYCLE_MODE}" in
      pr-ci)
        if [[ -z "${ARTIFACT_LIFECYCLE_BASE:-}" || -z "${ARTIFACT_LIFECYCLE_HEAD:-}" ]]; then
          echo "ARTIFACT_LIFECYCLE_MODE=pr-ci requires ARTIFACT_LIFECYCLE_BASE and ARTIFACT_LIFECYCLE_HEAD." >&2
          return 1
        fi
        artifact_lifecycle_label="Validate artifact lifecycle (pr-ci)"
        artifact_lifecycle_cmd=(
          python scripts/validate-artifact-lifecycle.py
          --mode pr-ci
          --base "$ARTIFACT_LIFECYCLE_BASE"
          --head "$ARTIFACT_LIFECYCLE_HEAD"
        )
        ;;
      push-main-ci)
        if [[ -z "${ARTIFACT_LIFECYCLE_BEFORE:-}" || -z "${ARTIFACT_LIFECYCLE_AFTER:-}" ]]; then
          echo "ARTIFACT_LIFECYCLE_MODE=push-main-ci requires ARTIFACT_LIFECYCLE_BEFORE and ARTIFACT_LIFECYCLE_AFTER." >&2
          return 1
        fi
        artifact_lifecycle_label="Validate artifact lifecycle (push-main-ci)"
        artifact_lifecycle_cmd=(
          python scripts/validate-artifact-lifecycle.py
          --mode push-main-ci
          --before "$ARTIFACT_LIFECYCLE_BEFORE"
          --after "$ARTIFACT_LIFECYCLE_AFTER"
        )
        ;;
      local)
        artifact_lifecycle_label="Validate artifact lifecycle (local)"
        artifact_lifecycle_cmd=(
          python scripts/validate-artifact-lifecycle.py
          --mode local
        )
        ;;
      *)
        echo "Unsupported ARTIFACT_LIFECYCLE_MODE: ${ARTIFACT_LIFECYCLE_MODE}" >&2
        return 1
        ;;
    esac

    if [[ -n "${ARTIFACT_LIFECYCLE_PR_BODY_FILE:-}" ]]; then
      artifact_lifecycle_cmd+=(--pr-body-file "$ARTIFACT_LIFECYCLE_PR_BODY_FILE")
    fi
    return 0
  fi

  local -a tracked_diff_paths=()
  mapfile -t tracked_diff_paths < <(git diff --name-only --diff-filter=ACMRT HEAD -- .)
  if [[ ${#tracked_diff_paths[@]} -gt 0 ]]; then
    artifact_lifecycle_label="Validate artifact lifecycle (explicit-paths from tracked diff)"
    artifact_lifecycle_cmd=(
      python scripts/validate-artifact-lifecycle.py
      --mode explicit-paths
    )
    for path in "${tracked_diff_paths[@]}"; do
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

run_check "Run artifact lifecycle validator fixtures" \
  python scripts/test-artifact-lifecycle-validator.py

determine_artifact_lifecycle_command
run_check "$artifact_lifecycle_label" \
  "${artifact_lifecycle_cmd[@]}"

echo "CI checks passed."
