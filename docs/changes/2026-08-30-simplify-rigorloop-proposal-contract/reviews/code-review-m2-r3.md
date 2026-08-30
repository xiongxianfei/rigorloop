# Code Review M2 R3: Compatibility Composition Rereview

Review ID: code-review-m2-r3
Stage: code-review
Round: r3
Reviewer: Codex independent code-review context with fresh-assumption reset
Review date: 2026-08-30
Target: aggregate M2 implementation commits `a1b57bbf05e28f1e4362d49ffb520066a1aff479`, `f3fd200c`, and `b98e9926`
Reviewed milestone: M2
Reviewed artifact: commits `a1b57bbf05e28f1e4362d49ffb520066a1aff479`, `f3fd200c`, and `b98e9926`
Review status: changes-requested
Status: changes-requested
Material findings: SPC-M2-CR5
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/reviews/code-review-m2-r3.md` and matching change-local review evidence and review projection
- Open blockers: a portable proposal is incorrectly coupled to an unrelated selected stage-owned change record
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SPC-M2-CR5
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/reviews/code-review-m2-r3.md`
- Review log: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-log.md`
- Review resolution: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: SPC-M2-CR5
- Verify readiness: not-claimed

## Actual-diff summary

The aggregate M2 implementation now preserves untouched settled legacy and simplified proposals, requires changed settled and unsettled legacy proposals to adopt the simplified contract, accepts portable and matching governed proposals, and rejects a different-ID selected governed mismatch. CR1 through CR4 remain resolved by `f3fd200c` and `b98e9926`. R3 found one adjacent composition false positive: one unrelated selected stage-owned record is treated as the governing proposal record even when it has no proposal entry.

## Finding SPC-M2-CR5

Finding ID: SPC-M2-CR5
Severity: major
Location: `scripts/artifact_lifecycle_validation.py:2093-2102`
Evidence: mismatch inference activates whenever exactly one stage-owned change record and a proposal are selected, even when that record has no proposal artifact entry. A valid portable simplified proposal selected alongside an unrelated spec-only stage-owned change record receives `selected change record does not identify this proposal as its primary proposal`.
Required outcome: Mismatch validation must apply only when the selected stage-owned change record declares a primary proposal entry. A proposal selected alongside a record with no proposal entry must remain portable.
Safe resolution path: Narrow the existing inference to the selected record's primary proposal entry and add a regression for a portable proposal selected with an unrelated stage-owned record that has no proposal entry. Preserve the current different-ID mismatch behavior when a proposal entry exists.
needs-decision rationale: none

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | SPC-R6 is violated by the unrelated-record false positive; SPC-R7 and SPC-R15-R16 pass their requested partitions. |
| Test coverage | concern | The 156-test suite covers CR1-CR4 but omits portable proposal plus unrelated selected change record. |
| Edge cases | concern | A selected record with no proposal entry changes a portable proposal's outcome. |
| Error handling | concern | The validator emits a governed mismatch error where no governed proposal relationship exists. |
| Architecture boundaries | concern | One-way ownership inference extends beyond records that declare proposal ownership. |
| Compatibility | pass | Untouched settled legacy and simplified, changed settled legacy, and unsettled legacy outcomes passed direct proof. |
| Security/privacy | pass | No credential, network, authorization, secret, or private-data behavior changed. |
| Derived artifact currency | pass for M2 scope | M3 remains responsible for supported published adapter parity. |
| Unrelated changes | pass | Aggregate implementation changes remain scoped to M2 validators, tests, and evidence. |
| Validation evidence | concern | Named suites and seven requested partitions pass, but the direct composition probe exposes the uncovered false positive. |

## Validation and direct proof

- `python scripts/test-artifact-lifecycle-validator.py`: passed, 156 tests.
- `python scripts/test-review-artifact-validator.py`: passed, 107 tests.
- Direct partitions passed: untouched settled legacy, untouched settled simplified, changed settled legacy, unsettled legacy, portable proposal, matching governed proposal, and different-ID selected mismatch.
- Current proposal explicit-path validation: passed.
- Review artifact structure validation: passed before this R3 record was added.
- Change metadata validation: passed before this R3 record was added.
- Boundary validation: passed.
- Aggregate implementation diff check: passed.
- Portable proposal plus unrelated spec-only stage-owned change record: incorrectly emitted the governed proposal mismatch diagnostic.

CR1 through CR4 remain resolved. CR5 requires owner disposition, bounded correction, and independent M2 rereview. This review does not close M2, authorize M3, or claim final verification, branch readiness, or PR readiness.
