# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: M2 R1
Reviewer: Codex code-review skill
Target: M2 commit `dcb40465`
Reviewed artifact: M2 commit `dcb40465`
Reviewed milestone: M2. Release-surface inventory and ownership classification
Status: changes-requested
Review status: changes-requested
Review date: 2026-06-29
Recording status: recorded
Material findings: CR-RTA-M2-F1, CR-RTA-M2-F2
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m2-r1.md, docs/changes/2026-06-29-release-transaction-automation/review-log.md, docs/changes/2026-06-29-release-transaction-automation/review-resolution.md, docs/plans/2026-06-29-release-transaction-automation.md, docs/plan.md, docs/changes/2026-06-29-release-transaction-automation/change.yaml
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CR-RTA-M2-F1, CR-RTA-M2-F2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m2-r1.md
- Review log: docs/changes/2026-06-29-release-transaction-automation/review-log.md
- Review resolution: docs/changes/2026-06-29-release-transaction-automation/review-resolution.md
- Reviewed milestone: M2. Release-surface inventory and ownership classification
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2 resolution needed, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: CR-RTA-M2-F1, CR-RTA-M2-F2
- Verify readiness: not-claimed

## Review Inputs

- Diff range: `HEAD^..HEAD` at `dcb40465`.
- Review surface: `scripts/release_transaction.py`, `scripts/test-release-transaction.py`, `tests/fixtures/release-transaction/surface-inventory/`, `tests/fixtures/release-transaction/literal-audit/`, change-local surface inventory and literal-audit baseline evidence, active plan M2 state, change metadata, and recorded validation evidence.
- Tracked governing branch state: approved proposal, approved spec, approved architecture/ADR, approved test spec, active plan, change metadata, approved M1, and M2 implementation are tracked at `dcb40465`.
- Governing spec: `specs/release-transaction-automation.md` requirements `R7`, `R10`, `R11`, `R14`, `R15`, `R22`-`R26`, `R43`, `R44`; acceptance criteria `AC5`-`AC7`, `AC18`.
- Test spec: `specs/release-transaction-automation.test.md` `RTA-T003`, `RTA-T004`, `RTA-T014`, `TRTA-LIT-001` through `TRTA-LIT-007`.
- Plan milestone: `docs/plans/2026-06-29-release-transaction-automation.md` M2.
- Validation evidence inspected: M2 plan validation notes for `python scripts/test-release-transaction.py`, selector regression, change metadata validation, lifecycle explicit-path validation, review artifact validation, guide validation, Python compilation, and whitespace validation.
- Validation spot check run during review: `python scripts/test-release-transaction.py`.

## Diff Summary

M2 adds release surface inventory and literal-audit baseline validation to `scripts/release_transaction.py`, fixture coverage in `scripts/test-release-transaction.py`, change-local evidence files for `release-surface-inventory.yaml` and `release-literal-audit-baseline.yaml`, and selector registration for those two change-local evidence artifacts. The implementation keeps enforcement preflight wiring deferred to later milestones.

## Findings

### CR-RTA-M2-F1: Literal-audit missing-classification proof is absent

Finding ID: CR-RTA-M2-F1
Severity: major
Location: `scripts/test-release-transaction.py:209`
Evidence: The approved test spec requires `TRTA-LIT-002 | Missing classification | fail` at `specs/release-transaction-automation.test.md:121`. M2 adds literal-audit tests for valid baseline drift, unknown classification, changed unauthorized literal, historical fixture without rationale, and generated-current without owner at `scripts/test-release-transaction.py:194` through `scripts/test-release-transaction.py:248`, but there is no fixture or assertion for a literal-audit entry that omits `classification`. The fixture directory likewise includes `invalid-unknown-classification.yaml` but no missing-classification fixture.
Required outcome: Add a direct literal-audit negative fixture and test proving an entry missing `classification` fails with a diagnostic naming `classification`.
Safe resolution path: Add `tests/fixtures/release-transaction/literal-audit/invalid-missing-classification.yaml`, add a focused assertion in `LiteralAuditBaselineTests`, rerun `python scripts/test-release-transaction.py`, and update M2 validation evidence. No spec or plan change is needed if the implementation follows the approved `TRTA-LIT-002` contract.
needs-decision rationale: none

### CR-RTA-M2-F2: Surface ownership inventory omits prior profile snapshots and lacks unclassified-surface proof

Finding ID: CR-RTA-M2-F2
Severity: major
Location: `docs/changes/2026-06-29-release-transaction-automation/release-surface-inventory.yaml:39`
Evidence: The governing spec defines historical immutable surfaces as including prior profile snapshots at `specs/release-transaction-automation.md:27` and requires every routine release-prep surface to be classified at `specs/release-transaction-automation.md:79`. The approved M2 test case requires the surface inventory fixture to cover "profile snapshots" and expects unclassified surfaces to fail at `specs/release-transaction-automation.test.md:382` through `specs/release-transaction-automation.test.md:384`. The committed change-local inventory classifies prior release evidence and historical fixtures at `docs/changes/2026-06-29-release-transaction-automation/release-surface-inventory.yaml:39` through `docs/changes/2026-06-29-release-transaction-automation/release-surface-inventory.yaml:48`, but has no prior profile snapshot surface. The valid fixture similarly ends with prior release evidence and historical fixture entries at `tests/fixtures/release-transaction/surface-inventory/valid-inventory.yaml:39` through `tests/fixtures/release-transaction/surface-inventory/valid-inventory.yaml:48`, and the negative fixture set covers unknown classification and manual override without rationale but not an omitted `classification` field.
Required outcome: Add prior profile snapshots to the M2 surface inventory and valid fixture as a `historical-immutable` surface, and add a direct negative fixture/test proving an unclassified surface fails with an owner/classification diagnostic.
Safe resolution path: Add a `prior-profile-snapshots` or equivalent surface entry for `docs/releases/profiles/v*.yaml` in both the change-local inventory and surface-inventory fixture, add `invalid-missing-classification.yaml` under `tests/fixtures/release-transaction/surface-inventory/`, assert the missing classification diagnostic in `ReleaseSurfaceInventoryTests`, and rerun the M2 focused and lifecycle validation commands.
needs-decision rationale: none

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | block | CR-RTA-M2-F2 identifies an unclassified historical immutable surface from the spec glossary and `R7`. |
| Test coverage | block | CR-RTA-M2-F1 and CR-RTA-M2-F2 identify missing direct proof required by approved test-spec rows. |
| Edge cases | block | Missing classification paths are not directly proven for literal audit or surface inventory. |
| Error handling | concern | The helper appears capable of reporting missing fields generically, but M2 cannot close on inference where the test spec names direct proof. |
| Architecture boundaries | pass | M2 keeps inventory/audit helpers local to release transaction tooling and does not introduce release prep, preflight, closeout, publication, or full-gate changes. |
| Compatibility | pass | Existing release verification and publication boundaries remain unchanged. |
| Security/privacy | pass | No secrets, credentials, live npm/GitHub calls, or publication side effects appear in the reviewed code or fixtures. |
| Derived artifact currency | concern | The change-local inventory is missing prior profile snapshots, so the current ownership evidence is incomplete. |
| Unrelated changes | pass | Selector evidence registration and tests are scoped to the M2 change-local evidence classes. |
| Validation evidence | concern | Focused tests pass, but they do not include the required missing-classification and prior-profile-snapshot proof. |

## No-Finding Rationale

Not applicable. This review has two material findings.

## Residual Risks

The review did not attempt to fix or rerun the implementation after recording the findings. M3-M6 remain unreviewed and out of scope for this milestone-local review.

## Validation

- `python scripts/test-release-transaction.py` passed during review: 21 tests.

## Recommended Next Stage

Enter `review-resolution` for `CR-RTA-M2-F1` and `CR-RTA-M2-F2`, apply the targeted M2 fixture/test and inventory fixes, rerun M2 validation, return M2 to `review-requested`, and rerun `code-review M2`.
