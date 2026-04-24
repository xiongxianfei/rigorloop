#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PLACEHOLDER_MARKERS=(
  "Replace this script with repository-specific release"" checks"
  "TO""DO: release checks"
  "placeholder release"" check"
)

usage() {
  echo "usage: bash scripts/release-verify.sh <release-tag>" >&2
  echo "or set GITHUB_REF_NAME when running from GitHub Actions." >&2
}

release_version="${1:-${GITHUB_REF_NAME:-}}"
if [[ -z "$release_version" ]]; then
  usage
  exit 1
fi

case "$release_version" in
  v0.1.0-rc.1|v0.1.0)
    ;;
  *)
    echo "Unsupported release target: ${release_version}" >&2
    exit 1
    ;;
esac

adapter_version="${release_version#v}"
SEEN_COMMANDS=()
SEEN_LABELS=()
REQUIRED_CHECK_COMMANDS=(
  "python scripts/validate-skills.py"
  "python scripts/test-skill-validator.py"
  "python scripts/build-skills.py --check"
  "python scripts/test-adapter-distribution.py"
  "python scripts/build-adapters.py --version ${adapter_version} --check"
  "python scripts/validate-adapters.py --version ${adapter_version}"
  "python scripts/validate-release.py --version ${release_version}"
)

verify_release_script_contract() {
  local marker=""
  for marker in "${PLACEHOLDER_MARKERS[@]}"; do
    if grep -Fq "$marker" scripts/release-verify.sh; then
      echo "release gate failure: placeholder release-check text remains: ${marker}" >&2
      return 1
    fi
  done

}

run_check() {
  local label="$1"
  shift
  local command_text=""
  printf -v command_text '%s ' "$@"
  command_text="${command_text% }"
  SEEN_LABELS+=("$label")
  SEEN_COMMANDS+=("$command_text")

  echo "==> ${label}"
  echo "+ ${command_text}"
  if [[ "${RELEASE_VERIFY_DRY_RUN:-}" != "1" ]]; then
    "$@"
  fi
  echo
}

verify_required_invocations() {
  local required=""
  local seen=""
  local found=""
  for required in "${REQUIRED_CHECK_COMMANDS[@]}"; do
    found="false"
    for seen in "${SEEN_COMMANDS[@]}"; do
      if [[ "$seen" == "$required" ]]; then
        found="true"
        break
      fi
    done
    if [[ "$found" != "true" ]]; then
      echo "release gate failure: required release check was not invoked: ${required}" >&2
      return 1
    fi
  done

  found="false"
  for seen in "${SEEN_LABELS[@]}"; do
    if [[ "${seen,,}" == *security* ]]; then
      found="true"
      break
    fi
  done
  if [[ "$found" != "true" ]]; then
    echo "release gate failure: required security check category was not invoked" >&2
    return 1
  fi
}

echo "Release verification for ${release_version}"
echo "Adapter manifest version: ${adapter_version}"
echo

verify_release_script_contract

run_check "Validate canonical skills" \
  python scripts/validate-skills.py

run_check "Run skill regression validation" \
  python scripts/test-skill-validator.py

run_check "Check generated Codex skill drift" \
  python scripts/build-skills.py --check

run_check "Run adapter distribution regression tests" \
  python scripts/test-adapter-distribution.py

run_check "Check generated adapter drift" \
  python scripts/build-adapters.py --version "$adapter_version" --check

run_check "Validate generated adapters and security" \
  python scripts/validate-adapters.py --version "$adapter_version"

run_check "Validate release metadata, smoke rules, notes, and security" \
  python scripts/validate-release.py --version "$release_version"

verify_required_invocations

echo "Release verification passed for ${release_version}."
