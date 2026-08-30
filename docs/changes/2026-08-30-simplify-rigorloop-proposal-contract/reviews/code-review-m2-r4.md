# Code Review M2 R4: Mixed Proposal Composition Rereview

Review ID: code-review-m2-r4
Stage: code-review
Round: r4
Reviewer: Codex independent code-review context with fresh-assumption reset
Review date: 2026-08-30
Target: aggregate M2 implementation commits `a1b57bbf05e28f1e4362d49ffb520066a1aff479`, `f3fd200c`, `b98e9926`, and `f395ab51`
Reviewed milestone: M2
Reviewed artifact: commits `a1b57bbf05e28f1e4362d49ffb520066a1aff479`, `f3fd200c`, `b98e9926`, and `f395ab51`
Review status: changes-requested
Status: changes-requested
Material findings: SPC-M2-CR6
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/reviews/code-review-m2-r4.md` and matching change-local review evidence and review projection
- Open blockers: a portable proposal is incorrectly coupled to a correctly governed proposal selected in the same validation scope
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SPC-M2-CR6
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/reviews/code-review-m2-r4.md`
- Review log: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-log.md`
- Review resolution: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: SPC-M2-CR6
- Verify readiness: not-claimed

## Actual-diff summary

The aggregate M2 implementation preserves untouched settled legacy and simplified proposals, requires changed settled and unsettled legacy proposals to adopt the simplified contract, accepts portable and matching governed proposals in isolation, rejects a different-ID selected governed mismatch, and preserves portable composition with an unrelated non-proposal change record. CR1 through CR5 remain resolved. R4 found one remaining scope-composition false positive: a portable proposal is treated as governed when another proposal and its matching primary-proposal record are selected in the same validation scope.

## Finding SPC-M2-CR6

Finding ID: SPC-M2-CR6
Severity: major
Location: `scripts/artifact_lifecycle_validation.py:2101-2115`
Evidence: the mismatch condition applies the presence of exactly one selected primary-proposal change record to every changed proposal. A scope containing one valid portable proposal plus one correctly governed proposal and its matching `change.yaml` therefore emits `selected change record does not identify this proposal as its primary proposal` against the portable proposal. The R4 regression added for CR5 covers only an unrelated non-proposal record and does not exercise this ordinary mixed-proposal composition.
Required outcome: Portable and governed proposals must compose in one validation scope while the existing unambiguous one-proposal/one-primary-record mismatch case continues to fail.
Safe resolution path: Bound mismatch inference to an unambiguous one-proposal/one-primary-record selection, or otherwise correlate selected proposals and primary-proposal records without filenames, hashes, versions, reverse pointers, repository-wide inventory, or a new CLI mechanism. Add a regression containing a portable proposal alongside a correctly governed proposal and its matching record.
needs-decision rationale: none

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | The mixed scope violates SPC-R6 portable validity; the isolated SPC-R7 and SPC-R15-R16 partitions pass. |
| Test coverage | concern | The 157-test suite covers CR1-CR5 but omits portable and governed proposals selected together. |
| Edge cases | concern | One matching governed pair changes an independent portable proposal's outcome. |
| Error handling | concern | The validator emits a governed mismatch diagnostic for a proposal that has no governed relationship. |
| Architecture boundaries | concern | Scope-wide primary-proposal-record presence is treated as ownership of every selected proposal. |
| Compatibility | pass | Untouched settled legacy and simplified, changed settled legacy, and unsettled legacy outcomes passed direct proof. |
| Security/privacy | pass | No credential, network, authorization, secret, or private-data behavior changed. |
| Derived artifact currency | pass for M2 scope | M3 remains responsible for supported published adapter parity. |
| Unrelated changes | pass | Aggregate implementation changes remain scoped to M2 validators, tests, and evidence. |
| Validation evidence | concern | Full required suites pass, but the direct mixed-proposal composition probe exposes the uncovered false positive. |

## Validation and direct proof

- `python scripts/test-artifact-lifecycle-validator.py`: passed, 157 tests.
- `python scripts/test-review-artifact-validator.py`: passed, 107 tests.
- Focused compatibility matrix: passed, 9 tests covering simplified shape, malformed structure, governed ownership, unsettled and settled legacy, settled simplified, selected mismatch, and CR5 composition.
- Current proposal explicit-path validation: passed.
- Review artifact structure validation: passed before this R4 record was added.
- Change metadata validation: passed before this R4 record was added.
- Boundary validation: passed.
- Aggregate implementation diff check: passed.
- Portable proposal plus a matching governed proposal/change-record pair: incorrectly emitted one governed proposal mismatch diagnostic against the portable proposal.

CR1 through CR5 remain resolved. CR6 requires owner disposition, bounded correction, and independent M2 rereview. This review does not close M2, authorize M3, or claim final verification, branch readiness, or PR readiness.
