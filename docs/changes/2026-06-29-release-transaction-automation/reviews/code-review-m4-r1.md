# Code Review M4 R1

Review ID: code-review-m4-r1
Stage: code-review
Round: M4 R1
Reviewer: Codex code-review skill
Target: M4 commit `b89ff336`
Reviewed artifact: M4 commit `b89ff336`
Reviewed milestone: M4. Release preflight command
Status: changes-requested
Review status: changes-requested
Review date: 2026-06-29
Recording status: recorded
Material findings: CR-RTA-M4-F1, CR-RTA-M4-F2
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m4-r1.md, docs/changes/2026-06-29-release-transaction-automation/review-log.md, docs/changes/2026-06-29-release-transaction-automation/review-resolution.md, docs/plans/2026-06-29-release-transaction-automation.md, docs/plan.md, docs/changes/2026-06-29-release-transaction-automation/change.yaml
- Open blockers: none
- Next stage: review-resolution M4
- Review status: changes-requested
- Material findings: CR-RTA-M4-F1, CR-RTA-M4-F2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m4-r1.md
- Review log: docs/changes/2026-06-29-release-transaction-automation/review-log.md
- Review resolution: docs/changes/2026-06-29-release-transaction-automation/review-resolution.md#code-review-m4-r1
- Reviewed milestone: M4. Release preflight command
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution needed, M5, M6
- Required review-resolution: yes
- Finding IDs: CR-RTA-M4-F1, CR-RTA-M4-F2
- Verify readiness: not-claimed

## Review Inputs

- Diff range: `HEAD^..HEAD` at `b89ff336`.
- Review surface: `scripts/release_transaction.py`, `scripts/release-preflight.py`, `scripts/test-release-transaction.py`, active plan M4 state, change metadata, and recorded validation evidence.
- Tracked governing branch state: approved proposal, approved spec, approved architecture/ADR, approved test spec, active plan, change metadata, closed M1, closed M2, closed M3, and M4 implementation are tracked at `b89ff336`.
- Governing spec: `specs/release-transaction-automation.md` requirements `R18`-`R27`; acceptance criteria `AC8`, `AC9`.
- Test spec: `specs/release-transaction-automation.test.md` `RTA-T011` through `RTA-T015`.
- Plan milestone: `docs/plans/2026-06-29-release-transaction-automation.md` M4.
- Validation evidence inspected: M4 plan validation notes for `python scripts/test-release-transaction.py`, `python scripts/release-preflight.py --help`, Python compilation, selector manual-routing result, change metadata validation, lifecycle explicit-path validation, review artifact validation, and whitespace validation.
- Validation spot checks run during review: `python scripts/test-release-transaction.py`, `python scripts/release-preflight.py --help`, `python -m py_compile scripts/release_transaction.py scripts/test-release-transaction.py scripts/prepare-release.py scripts/release-preflight.py`, `git diff --check --`, and a temporary CLI reproduction of changed unauthorized literal behavior without `--changed-file`.

## Diff Summary

M4 adds `scripts/release-preflight.py`, a shared `release_preflight` helper, and focused preflight tests. The helper checks routine profile loading, package/profile metadata agreement, bundled metadata pointer drift, generated pending evidence shape, literal-audit baseline diagnostics when given changed files, `release-output` cleanliness, local tag conflicts, reachable remote tag conflicts, and unreachable remote tag warnings. The tests cover a clean fixture, CLI success, missing profile, package mismatch, metadata pointer drift, invalid pending evidence, dirty `release-output`, changed unauthorized literal through the helper API, local tag conflict, unreachable remote tag warning, and reachable remote tag conflict.

## Findings

### CR-RTA-M4-F1: Default preflight CLI does not enforce newly changed unauthorized literals

Finding ID: CR-RTA-M4-F1
Severity: major
Status: open
Location: `scripts/release-preflight.py:22`
Evidence: The spec requires release preflight to fail for newly changed unauthorized current-version literals at `specs/release-transaction-automation.md:109`, and the preferred M4 command is `python scripts/release-preflight.py <tag>` at `specs/release-transaction-automation.md:101`. The CLI accepts `--changed-file` at `scripts/release-preflight.py:22` through `scripts/release-preflight.py:27`, but defaults it to an empty tuple and passes only that explicit argument set into `release_preflight` at `scripts/release-preflight.py:38` through `scripts/release-preflight.py:42`. The helper defaults `changed_files` to `()` at `scripts/release_transaction.py:294` through `scripts/release_transaction.py:300`, and literal-audit enforcement depends on that set at `scripts/release_transaction.py:318`. The only changed-unauthorized-literal test calls the helper with an explicit `changed_files=("scripts/new_release_state.py",)` at `scripts/test-release-transaction.py:660` through `scripts/test-release-transaction.py:664`; it does not prove the required CLI invocation catches the issue. During review, a prepared fixture with an unauthorized current literal in `release-literal-audit-baseline.yaml` returned exit code 0 from `python scripts/release-preflight.py v0.3.5 --root <fixture>` because no changed files were supplied.
Required outcome: The default M4 preflight command must detect newly changed unauthorized literals under the normal `python scripts/release-preflight.py <tag>` invocation, or the approved spec/test spec must be revised to make `--changed-file` mandatory and update the workflow command contract.
Safe resolution path: Derive changed files from git by default when `--changed-file` is not provided, preserve explicit `--changed-file` as an override for fixtures, and add a CLI-level regression proving a changed unauthorized literal fails without manually passing `--changed-file`. If a non-git fixture needs explicit changed files, keep that helper test as secondary proof.
needs-decision rationale: none

### CR-RTA-M4-F2: Named preflight negative fixtures are incomplete

Finding ID: CR-RTA-M4-F2
Severity: major
Status: open
Location: `scripts/test-release-transaction.py:591`
Evidence: The M4 plan requires fixtures for "missing profile, malformed profile, version mismatch, stale metadata pointer, unauthorized changed literal, invalid pending evidence shape, local tag conflict, reachable remote tag conflict, unreachable remote diagnostic, and dirty release-output fixtures" at `docs/plans/2026-06-29-release-transaction-automation.md:186` through `docs/plans/2026-06-29-release-transaction-automation.md:188`. The approved test spec also names malformed profile, incomplete profile, and missing local input in `RTA-T012` at `specs/release-transaction-automation.test.md:458` through `specs/release-transaction-automation.test.md:464`. M4 tests include missing profile at `scripts/test-release-transaction.py:591`, package mismatch at `scripts/test-release-transaction.py:597`, stale metadata pointer at `scripts/test-release-transaction.py:606`, invalid pending evidence at `scripts/test-release-transaction.py:615`, dirty `release-output` at `scripts/test-release-transaction.py:626`, and tag cases at `scripts/test-release-transaction.py:668` through `scripts/test-release-transaction.py:715`, but there is no direct preflight test for malformed profile, incomplete profile, or missing required local input. Code shape is not enough proof for named M4 edge cases under this repository's direct-proof rule.
Required outcome: Add direct M4 preflight tests for malformed profile, incomplete profile, and missing required local input diagnostics, or revise the approved plan/test spec before claiming M4 closeout.
Safe resolution path: Add focused temporary-repository preflight tests that corrupt the active profile YAML, remove a required top-level profile field or use an existing invalid profile fixture, and remove a required local input such as `packages/rigorloop/package.json` or `packages/rigorloop/dist/metadata/releases.json`. Assert each failure diagnostic names the profile path/field or missing local input path. Rerun `python scripts/test-release-transaction.py` and lifecycle validation.
needs-decision rationale: none

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | block | CR-RTA-M4-F1 shows the default preflight command does not satisfy `R22`; CR-RTA-M4-F2 identifies missing direct proof for named `R21` fixture cases. |
| Test coverage | block | Several preflight tests exist, but malformed profile, incomplete profile, missing local input, and default CLI changed-literal enforcement are not directly proven. |
| Edge cases | block | The changed unauthorized literal case passes through the helper only when the caller supplies `changed_files`; the documented CLI path can pass. Named malformed/incomplete/missing-input fixtures are absent. |
| Error handling | concern | Existing diagnostics are actionable for covered cases, but the default changed-file discovery path is missing. |
| Architecture boundaries | pass | M4 remains in release transaction tooling and does not invoke full release verification, adapter generation, publication closeout, or public smoke. |
| Compatibility | concern | Adding an optional `--changed-file` is fine for fixtures, but relying on it changes the preferred command contract unless the default command can derive changed files. |
| Security/privacy | pass | No secrets, credentials, registry reads, publication actions, or public smoke are introduced. Remote checks use `git ls-remote` against configured `origin` only. |
| Derived artifact currency | pass | No generated release artifacts are updated by preflight; the clean fixture test asserts file contents are unchanged. |
| Unrelated changes | pass | The reviewed diff is scoped to M4 preflight tooling, focused tests, and lifecycle metadata. |
| Validation evidence | concern | Focused tests pass, but they do not exercise all named M4 failure fixtures or the default CLI path for changed unauthorized literals. |

## No-Finding Rationale

Not applicable. This review has two material findings.

## Residual Risks

The review did not attempt to fix or rerun the implementation after recording the findings. M5-M6 remain unimplemented and unreviewed. Selector manual-routing for release transaction scripts remains known validation infrastructure debt and is not the blocker in this M4 review.

## Validation

- `python scripts/test-release-transaction.py` passed during review: 45 tests.
- `python scripts/release-preflight.py --help` passed.
- `python -m py_compile scripts/release_transaction.py scripts/test-release-transaction.py scripts/prepare-release.py scripts/release-preflight.py` passed.
- `git diff --check --` passed.
- Temporary CLI reproduction: unauthorized changed literal baseline passed with exit code 0 under `python scripts/release-preflight.py v0.3.5 --root <fixture>` when no `--changed-file` argument was supplied, confirming CR-RTA-M4-F1.

## Recommended Next Stage

Enter `review-resolution` for `CR-RTA-M4-F1` and `CR-RTA-M4-F2`, apply targeted M4 CLI/default changed-file discovery and missing fixture proof fixes, rerun M4 validation, return M4 to `review-requested`, and rerun `code-review M4`.
