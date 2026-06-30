# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: M1 R1
Reviewer: Codex code-review skill
Target: M1 commit `c03698ed`
Reviewed artifact: M1 commit `c03698ed`
Reviewed milestone: M1. Release profile schema and loader
Status: changes-requested
Review status: changes-requested
Review date: 2026-06-29
Recording status: recorded
Material findings: CR-RTA-M1-F1
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m1-r1.md, docs/changes/2026-06-29-release-transaction-automation/review-log.md, docs/changes/2026-06-29-release-transaction-automation/review-resolution.md, docs/plans/2026-06-29-release-transaction-automation.md, docs/plan.md, docs/changes/2026-06-29-release-transaction-automation/change.yaml
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CR-RTA-M1-F1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m1-r1.md
- Review log: docs/changes/2026-06-29-release-transaction-automation/review-log.md
- Review resolution: docs/changes/2026-06-29-release-transaction-automation/review-resolution.md
- Reviewed milestone: M1. Release profile schema and loader
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1 resolution needed, M2, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: CR-RTA-M1-F1
- Verify readiness: not-claimed

## Review Inputs

- Diff range: `HEAD^..HEAD` at `c03698ed`.
- Review surface: `scripts/release_transaction.py`, `scripts/test-release-transaction.py`, `tests/fixtures/release-transaction/profiles/`, active plan M1 state, change metadata, and recorded validation evidence.
- Tracked governing branch state: approved proposal, approved spec, approved architecture/ADR, approved test spec, active plan, change metadata, test-spec-review-r3, and M1 implementation are tracked at `c03698ed`.
- Governing spec: `specs/release-transaction-automation.md` requirements `R1`-`R6`, acceptance criteria `AC1`, `AC19`.
- Test spec: `specs/release-transaction-automation.test.md` `RTA-T001`, `RTA-T002`, fixture inventory, and command matrix entry for `python scripts/test-release-transaction.py`.
- Plan milestone: `docs/plans/2026-06-29-release-transaction-automation.md` M1.
- Architecture / ADR: `docs/architecture/system/architecture.md`, `docs/adr/ADR-20260629-release-transaction-profile.md`.
- Validation evidence inspected: M1 plan validation notes for `python scripts/test-release-transaction.py`, `python scripts/validate-release.py --help`, selector manual routing, change metadata validation, artifact lifecycle validation, `git diff --check`, and Python compilation.

## Diff Summary

M1 adds a Python release profile helper in `scripts/release_transaction.py`, focused profile tests in `scripts/test-release-transaction.py`, valid and invalid profile fixtures under `tests/fixtures/release-transaction/profiles/`, and lifecycle artifacts for the approved release transaction automation change. The helper resolves profiles from `docs/releases/profiles/<tag>.yaml`, parses the first-slice profile YAML shape, validates required release profile fields, fails closed on unknown release kind and target values, and distinguishes routine from special release profiles.

## Findings

### CR-RTA-M1-F1: M1 tests do not directly prove all required missing-profile-field failures

Finding ID: CR-RTA-M1-F1
Severity: major
Location: `scripts/test-release-transaction.py:80`
Evidence: `specs/release-transaction-automation.test.md:353` requires negative fixtures for missing release tag, package version, npm package, targets, adapter expectations, publication requirements, evidence requirements, and validation requirements. The committed M1 test suite has only one missing-field negative case, `test_missing_targets_fail_with_named_field`, at `scripts/test-release-transaction.py:80`. The fixture directory contains no missing `release_tag`, missing `package_version`, missing `npm_package`, missing `adapter_artifacts`, missing `publication`, missing `evidence`, missing `validation`, or missing-profile path fixture. The active M1 plan also names missing profile as an M1 test case at `docs/plans/2026-06-29-release-transaction-automation.md:99`.
Required outcome: M1 must add direct tests and fixtures for the required missing profile and missing required profile-field failures, or revise the approved test spec and plan before claiming M1 review closeout.
Safe resolution path: Add focused negative fixtures and assertions in `scripts/test-release-transaction.py` for missing profile, missing `release_tag`, missing `package_version`, missing `npm_package`, missing `adapter_artifacts`, missing `publication`, missing `evidence`, and missing `validation`; rerun `python scripts/test-release-transaction.py`, `python scripts/validate-change-metadata.py docs/changes/2026-06-29-release-transaction-automation/change.yaml`, lifecycle explicit-path validation, and whitespace validation. No owner decision is needed if the implementation follows the existing test spec.
needs-decision rationale: none

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | concern | The profile helper implements the M1 fields and source path, but M1 cannot close cleanly while proof for required missing-field failures is incomplete. |
| Test coverage | block | CR-RTA-M1-F1 identifies missing direct proof required by `RTA-T001` and the M1 plan. |
| Edge cases | block | Named missing-profile and missing required-field paths do not have complete direct test proof. |
| Error handling | concern | Code appears to handle many missing fields, but review cannot accept inference as direct proof for named edge cases. |
| Architecture boundaries | pass | M1 keeps release-profile parsing in a shared script helper and does not weaken `release-verify.sh` or publication checks. |
| Compatibility | pass | Existing `validate-release.py --help` remains unchanged and available; generated-surface integration is deferred by plan. |
| Security/privacy | pass | No secrets, credentials, external network calls, or publication side effects appear in the reviewed code or fixtures. |
| Derived artifact currency | pass | M1 introduces fixtures and a helper only; no generated release surfaces are claimed current. |
| Unrelated changes | pass | Implementation changes match the approved release transaction automation artifact stack and M1 helper/test scope. |
| Validation evidence | concern | Executed validation is relevant, but the focused test suite omits required negative cases. |

## No-Finding Rationale

Not applicable. This review has one material finding.

## Residual Risks

The review did not attempt to fix or rerun the implementation after the finding. M2-M6 remain unreviewed and out of scope for this milestone-local review.

## Recommended Next Stage

Enter `review-resolution` for `CR-RTA-M1-F1`, apply the targeted M1 test/fixture coverage fix, rerun M1 validation, return M1 to `review-requested`, and rerun `code-review M1`.
