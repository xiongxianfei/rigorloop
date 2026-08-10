# CI Clean-Runner Retirement-Ledger Fix

## Result

- Skill: bugfix, followed by CI-maintenance review
- Status: implemented; hosted rerun pending
- Affected PR: https://github.com/xiongxianfei/rigorloop/pull/131
- Failed run: https://github.com/xiongxianfei/rigorloop/actions/runs/31384291330
- Failed check: `Governance: retirement ledger`

## Expected and actual behavior

Expected: the direct PR graph runs on the clean GitHub Python 3.11 runner using
only repository-declared or standard-library dependencies.

Actual: `scripts/retirement_ledger.py` imported `yaml`, but the repository had
no Python dependency declaration or installation step. The hosted job stopped
with `ModuleNotFoundError: No module named 'yaml'`. Local verification had
passed because the workstation happened to provide PyYAML.

## Root cause and correction

Root-cause class: environment-integration regression introduced by M1 and first
exposed when M6 made the retirement-ledger regression a direct hosted check.

The first candidate fix declared and installed PyYAML. It was rejected before
commit because adding a network package installation would violate the approved
network-independent acceptance boundary and expand the dependency surface.

The final correction:

- converts the change-local ledger from YAML to JSON;
- replaces `yaml.safe_load` with standard-library `json.load`;
- rejects duplicate JSON object keys instead of silently overwriting them;
- adds a regression that imports and loads the ledger under `python -S`, where
  third-party site packages are unavailable; and
- updates the stable plan, test-spec command, explanation, and M1 evidence path
  from `retirement-ledger.yaml` to `retirement-ledger.json`.

The GitHub workflow remains least privilege, contains no dependency-install or
network step, and still invokes the same 26 direct checks.

## Validation before hosted rerun

- Red proof: `python scripts/test-retirement-ledger.py` failed because the new
  dependency-free ledger path did not exist.
- `python scripts/test-retirement-ledger.py` — pass; 15 tests, including
  third-party-site-package exclusion.
- `python scripts/test-select-validation.py` — pass; 152 tests in 60.26 seconds.
- `RIGORLOOP_CI_DIRECT_DRY_RUN=1 bash scripts/ci.sh --mode pr --base origin/main --head HEAD`
  — pass; the same 26 direct commands selected.
- `bash -n scripts/ci.sh` — pass.
- `git diff --check` — pass.

## CI-maintenance assessment

- Workflow file: `.github/workflows/ci.yml`
- Status: reviewed; no workflow mutation required
- Permissions: `contents: read`
- Secrets, write permissions, cache, dependency installation, target runtimes,
  publication, and deployment: absent
- Hosted outcome: pending after the correction is pushed
