# Code Review M2 R2: Compatibility Correction Rereview

Review ID: code-review-m2-r2
Stage: code-review
Round: r2
Reviewer: Codex independent code-review context with fresh-assumption reset
Review date: 2026-08-30
Target: combined M2 implementation commits `a1b57bbf05e28f1e4362d49ffb520066a1aff479` and `f3fd200c`
Reviewed milestone: M2
Reviewed artifact: commits `a1b57bbf05e28f1e4362d49ffb520066a1aff479` and `f3fd200c`
Review status: changes-requested
Status: changes-requested
Material findings: SPC-M2-CR3, SPC-M2-CR4
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/reviews/code-review-m2-r2.md` and matching change-local review evidence and review projection
- Open blockers: settled simplified proposals are reinterpreted as legacy; governed mismatch detection depends on filename equality
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SPC-M2-CR3, SPC-M2-CR4
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/reviews/code-review-m2-r2.md`
- Review log: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-log.md`
- Review resolution: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: SPC-M2-CR3, SPC-M2-CR4
- Verify readiness: not-claimed

## Actual-diff summary

The correction adds selected-path awareness for changed settled legacy proposals and a same-named proposal/change-record mismatch check. The two R1 counterexamples now have passing regressions, and CR1 and CR2 remain resolved by commit `f3fd200c`. R2 found two adjacent boundary partitions that the correction does not handle: unchanged settled simplified proposals and selected mismatched proposal/change-record pairs whose valid identities differ.

## Finding SPC-M2-CR3

Finding ID: SPC-M2-CR3
Severity: major
Location: `scripts/artifact_lifecycle_validation.py:1438-1444`
Evidence: terminal governed status is checked before proposal shape. An accepted simplified proposal reached only through its unchanged `change.yaml` therefore returns `current_path == false`, selects the legacy contract, and fails with missing `Problem`, `Non-goals`, and `Recommended direction` sections. The 155-test suite has no accepted simplified governed proposal validated through only its change record.
Required outcome: Unchanged settled legacy and unchanged settled simplified proposals must each remain readable under their actual contract, while changed settled legacy work adopts the current contract.
Safe resolution path: Recognize a complete simplified proposal shape before applying the terminal legacy exception, while retaining current-path enforcement for malformed or changed proposals. Add a direct accepted simplified governed fixture selected through only its change record.
needs-decision rationale: none

## Finding SPC-M2-CR4

Finding ID: SPC-M2-CR4
Severity: major
Location: `scripts/artifact_lifecycle_validation.py:2092-2097`
Evidence: mismatch detection requires `change-record directory name == proposal filename stem`, a constraint absent from the approved contract. A selected simplified proposal and selected stage-owned `change.yaml` with different valid identities and a mismatched primary proposal path returned zero blocking findings. The added regression covers only the same-named case.
Required outcome: Selected proposal/change-record correlation must use explicit validation scope and the primary proposal entry rather than filename equality, while genuinely portable proposals remain valid when no governing record is selected.
Safe resolution path: Correlate an unambiguous selected proposal/change-record pair directly and add a different-change-ID mismatch regression. Preserve portable behavior when the selected scope contains no governing change record for the proposal.
needs-decision rationale: none

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | SPC-R7 and SPC-R15-R16 remain incomplete for the two uncovered state and identity partitions. |
| Test coverage | concern | The focused tests prove the original counterexamples but omit accepted simplified non-current selection and different-identity mismatch. |
| Edge cases | concern | Terminal simplified state and non-equal valid proposal/change identities change the validator outcome. |
| Error handling | concern | The first valid state emits legacy-section errors; the second invalid state emits no blocking diagnostic. |
| Architecture boundaries | concern | One-way lifecycle ownership is still inferred from filename equality rather than exact selected ownership evidence. |
| Compatibility | block | A settled simplified artifact is not readable through its governing change record. |
| Security/privacy | pass | No credential, network, authorization, secret, or private-data behavior changed. |
| Derived artifact currency | pass for M2 scope | M3 still owns supported published adapter parity. |
| Unrelated changes | pass | The correction commit is limited to the validator, focused tests, and M2 evidence. |
| Validation evidence | concern | Named suites pass, but direct probes demonstrate two required uncovered outcomes. |

## Validation and direct proof

- `python scripts/test-artifact-lifecycle-validator.py`: passed, 155 tests.
- `python scripts/test-review-artifact-validator.py`: passed, 107 tests.
- Current proposal explicit-path validation: passed.
- Review artifact structure validation: passed before this R2 record was added.
- Boundary validation: passed.
- Combined implementation diff check: passed.
- Accepted simplified governed proposal selected through only `change.yaml`: failed with legacy `Problem`, `Non-goals`, and `Recommended direction` diagnostics.
- Different-identity selected proposal/change-record mismatch: returned zero blocking findings.
- Change metadata validation before R2 recording exposed stale R1 `unresolved_items`; this R2 recording reconciles the matching review summary and current review projection.

CR1 and CR2 remain resolved by `f3fd200c`. CR3 and CR4 require owner disposition, bounded correction, and independent M2 rereview. This review does not close M2, authorize M3, or claim final verification, branch readiness, or PR readiness.
