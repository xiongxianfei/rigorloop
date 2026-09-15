#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

usage() {
  echo "usage: bash scripts/release-verify.sh <release-tag>" >&2
  echo "or set GITHUB_REF_NAME when running from GitHub Actions." >&2
}

release_version="${1:-${GITHUB_REF_NAME:-}}"
if [[ -z "$release_version" ]]; then
  usage
  exit 1
fi

# The prepared path verifies immutable archives and the already-packed tarball.
# It cannot rebuild approved bytes or treat a dry run as a verified candidate.
if [[ "${2:-}" == "--prepared-candidate" ]]; then
  if [[ "$#" != 3 || "${RELEASE_VERIFY_DRY_RUN:-}" == "1" ]]; then
    echo "prepared candidate verification requires actual checks and an output directory" >&2
    exit 1
  fi
  exec python scripts/validate-release.py --version "$release_version" --prepared-candidate "$3"
fi

release_tag_commit="${RELEASE_TAG_COMMIT:-}"
if [[ "${GITHUB_ACTIONS:-}" == "true" && "${GITHUB_REF_TYPE:-}" == "tag" && -z "$release_tag_commit" ]]; then
  echo "release gate failure: trusted workflow requires RELEASE_TAG_COMMIT" >&2
  exit 1
fi
if [[ -n "$release_tag_commit" ]]; then
  if [[ ! "$release_tag_commit" =~ ^[0-9a-f]{40}$ ]]; then
    echo "release gate failure: RELEASE_TAG_COMMIT must be a full 40-character Git SHA" >&2
    exit 1
  fi
  if [[ "${GITHUB_ACTIONS:-}" == "true" && "${GITHUB_REF_TYPE:-}" == "tag" ]]; then
    python - "$release_version" "${GITHUB_REF_NAME:-}" "$release_tag_commit" <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, str(Path("scripts").resolve()))
from lib.release.release_transaction import validate_trusted_release_tag_identity

errors = validate_trusted_release_tag_identity(sys.argv[1], sys.argv[2], sys.argv[3])
if errors:
    for error in errors:
        print(f"release gate failure: {error}", file=sys.stderr)
    raise SystemExit(1)
PY
  else
    checked_commit="$(git rev-parse HEAD)"
    if [[ "$release_tag_commit" != "$checked_commit" ]]; then
      echo "release gate failure: RELEASE_TAG_COMMIT does not match checked HEAD" >&2
      exit 1
    fi
  fi
fi

if [[ "$#" -gt 1 ]]; then
  usage
  exit 1
fi
if [[ "${RELEASE_VERIFY_DRY_RUN:-}" == "1" ]]; then
  echo "release gate failure: current qualification requires actual checks; historical recipe dry runs are unsupported" >&2
  exit 1
fi
args=(--version "$release_version")
if [[ -n "${RELEASE_TAG_COMMIT:-}" ]]; then
  args+=(--release-commit "$RELEASE_TAG_COMMIT")
fi
if [[ -n "${RELEASE_OUTPUT_DIR:-}" ]]; then
  args+=(--release-output-dir "$RELEASE_OUTPUT_DIR")
fi
exec python scripts/validate-release.py "${args[@]}"
