# Code Review M2 R1: Proposal Validation and Compatibility

Review ID: code-review-m2-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review context with fresh-assumption reset
Review date: 2026-08-30
Target: exact M2 implementation commit `a1b57bbf05e28f1e4362d49ffb520066a1aff479`; routing commit `436efa47` excluded
Reviewed milestone: M2
Reviewed artifact: commit `a1b57bbf05e28f1e4362d49ffb520066a1aff479`
Review status: changes-requested
Status: changes-requested
Material findings: SPC-M2-CR1, SPC-M2-CR2
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/reviews/code-review-m2-r1.md` and `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-log.md`
- Open blockers: current-versus-historical selection and governed path mismatch detection are incomplete
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SPC-M2-CR1, SPC-M2-CR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-log.md`
- Review resolution: required
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: SPC-M2-CR1, SPC-M2-CR2
- Verify readiness: not-claimed

## Actual-diff summary

M2 adds the simplified proposal section grammar, precise structural diagnostics, governed ownership without a reverse proposal pointer, a compatibility selector for legacy proposals, and a closed Proposal Review vision-alignment vocabulary. It also adds focused artifact-lifecycle and review-validator tests and milestone validation evidence. The implementation introduces no new CLI command, proposal field, document version, per-document hash, or compatibility document.

## Finding SPC-M2-CR1

Finding ID: SPC-M2-CR1
Severity: major
Location: `scripts/artifact_lifecycle_validation.py:1431`, with incomplete compatibility coverage at `scripts/test-artifact-lifecycle-validator.py:3698`
Evidence: `_proposal_requires_simplified_contract` selects the legacy contract for every governed proposal whose lifecycle state is `accepted`, `rejected`, `abandoned`, `superseded`, or `archived`; it receives no selected-path or changed-path fact. A changed accepted legacy proposal therefore returns `False` and remains on the legacy contract. The settled-history test removes the change-record pointer and validates only the proposal path, so it proves detached portable legacy readability rather than the required governed untouched-versus-changed distinction. Shape detection can also force historical legacy evidence through the new contract merely because it already contained one new section name.
Required outcome: Preserve only untouched settled historical evidence under its settled contract while changed, unsettled, and new current proposals use the simplified contract, with direct governed fixtures for each required temporal partition.
Safe resolution path: Use existing validation-scope facts to distinguish a selected changed/current proposal from untouched settled evidence; keep the selection bounded and add no hash, version, field, compatibility document, or CLI command. Add focused tests for untouched settled governed legacy, changed settled governed legacy, unsettled governed legacy, and historical legacy containing an otherwise valid extra heading.
needs-decision rationale: none

## Finding SPC-M2-CR2

Finding ID: SPC-M2-CR2
Severity: major
Location: `scripts/artifact_lifecycle_validation.py:2080`, with missing governed-path-mismatch coverage for SPC-T04
Evidence: a simplified proposal contains no reverse pointer, so when the selected `change.yaml` primary proposal entry points to another path, `owners` is empty and the selected proposal is treated as portable. A direct fixture containing the simplified proposal and mismatched selected change record returned no blocking findings. The existing mismatch tests rely on the legacy reverse pointer and do not exercise the new one-way ownership model.
Required outcome: A selected governed proposal and selected change record must block lifecycle reliance when the primary proposal entry does not identify that exact proposal path, while a genuinely portable proposal remains valid without `change.yaml`.
Safe resolution path: Correlate the selected current proposal with the selected governing change record at the validation-scope boundary and emit the existing normalized-owner/path diagnostic when they differ. Add focused matching, mismatched, and portable fixtures without restoring a reverse proposal pointer.
needs-decision rationale: none

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | SPC-R15 and SPC-R16 require changed current proposals to adopt the simplified contract; SPC-R7 requires exact governed ownership. Both boundaries have failing counterexamples. |
| Test coverage | concern | The two required negative partitions are absent: changed settled governed legacy and simplified governed path mismatch. |
| Edge cases | concern | Untouched-versus-changed temporal state and portable-versus-mismatched governed identity are not distinguished. |
| Error handling | concern | Both invalid states can complete validation without an actionable blocking diagnostic. |
| Architecture boundaries | concern | The one-way `change.yaml` ownership design is implemented for the matching case but lacks the corresponding mismatch enforcement path. |
| Compatibility | block | Terminal lifecycle state alone grants the historical exception, so changed settled evidence remains exempt and shape can reject legitimate settled history. |
| Security/privacy | pass | No credential, network, secret, authorization, or private-data behavior changed. |
| Derived artifact currency | pass for M2 scope | Published adapter parity remains explicitly assigned to M3; M2 does not hand-edit generated output. |
| Unrelated changes | pass | Commit `a1b57bbf` is limited to M2 validators, focused tests, and M2 evidence. Routing commit `436efa47` is excluded. |
| Validation evidence | concern | All named suites pass, but they do not contain the two contract-required negative cases demonstrated by this review. |

## Validation and direct proof

- `python scripts/test-artifact-lifecycle-validator.py`: passed, 153 tests.
- `python scripts/test-review-artifact-validator.py`: passed, 107 tests.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-08-30-simplify-rigorloop-proposal-contract.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md`: passed.
- `python scripts/validate-review-artifacts.py docs/changes/2026-08-30-simplify-rigorloop-proposal-contract`: passed before this record was added.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/change.yaml`: passed before this record was added.
- `python scripts/validate-boundary-first.py --check --path specs/simplified-proposal-contract.test.md`: passed.
- Direct changed-settled selector probe: returned `False`, selecting the legacy contract for changed content with accepted governed status.
- Direct simplified governed-path mismatch fixture: returned zero blocking findings.
- `git diff --check a1b57bbf^ a1b57bbf`: passed.

M2 requires review-resolution and an independent rereview after correction. This review does not approve M2, close the milestone, authorize M3, or claim final verification, branch readiness, or PR readiness.
