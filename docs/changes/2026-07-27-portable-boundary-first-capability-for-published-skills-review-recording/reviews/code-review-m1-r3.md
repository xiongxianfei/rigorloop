# Code Review M1 R3

Review ID: code-review-m1-r3
Stage: code-review
Round: 3
Reviewer: Codex code-review skill
Target: M1 correction commit ffa692c0
Reviewed artifact: commit ffa692c0
Reviewed milestone: M1
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-28
Recording status: recorded
Recording blocker: none
Material findings: PBF-M1-CR4
Immediate next stage: blocked pending renewed correction authority
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: R3 invocation manifest, this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: PBF-M1-CR4 and exhausted two-cycle correction budget
- Next stage: blocked pending renewed correction authority
- Review status: changes-requested
- Material findings: PBF-M1-CR4
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/reviews/code-review-m1-r3.md`
- Review log: `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-log.md`
- Review resolution: `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-resolution.md#code-review-m1-r3`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4
- Required review-resolution: yes
- Finding IDs: PBF-M1-CR4
- Verify readiness: not-claimed

## Review inputs

- Diff surface: correction commit `ffa692c0`, reviewed blind-first before prior findings and validation summaries.
- Governing clauses: PBF-R046 through PBF-R050, test-spec T1, security/privacy verification, and M1 proof ownership.
- Tracked governing branch state: governing artifacts and R1/R2 correction evidence are tracked through `90dcb7fb`.
- Invocation evidence: `review-invocation-code-review-m1-r3.yaml`.

## Risk map

- Affected behavior: unexpected-consumer symlink classification and temporary fixture lifecycle.
- Highest-impact failures: following an outside link, accepting unsafe membership drift, rejecting legitimate non-symlink entries, or leaking test state.
- Changed boundaries: closed consumer enumeration, error aggregation, and test isolation.
- Expected evidence: both unsafe topology errors, no traversal, ordinary unexpected-file preservation, managed cleanup, and unchanged ten-consumer parity.
- Direct inspection: non-recursive enumeration branches, error ordering, fixture cleanup registration, and existing negative tests.
- Applicable risks: filesystem integrity, generated-output currency, regression safety, and test isolation.
- Non-applicable risks: external actions, credentials, and network access.

## Diff summary

R3 reviews the correction that rejects ungoverned skill-root and references-directory symlinks during non-recursive enumeration and gives every outside regression fixture registered cleanup.

## Prior-finding reconciliation

| Finding | R3 result | Evidence |
| --- | --- | --- |
| PBF-M1-CR1 | resolved | Source and expected destination components still fail before reads or writes. |
| PBF-M1-CR2 | resolved | Both unsafe ungoverned symlink placements now produce a stable unsuccessful result without traversal in check mode. |
| PBF-M1-CR3 | resolved | Managed outside directories leave the legacy sibling-directory count unchanged after the ten-test suite. |
| PBF-M1-CR4 | new-finding | Write-mode outside-mutation and combined-error behavior lack direct regression proof. |

## Findings

### PBF-M1-CR4 - Unexpected-consumer symlink proof omits write mode and combined errors

Finding ID: PBF-M1-CR4
Severity: major
Location: `scripts/test-boundary-first-reference.py:165`
Evidence: `test_unexpected_consumer_symlink_topologies_fail_closed` invokes only `mode="check"` and asserts only the symlink diagnostic. It does not prove that `mode="write"` leaves outside sentinel bytes unchanged, nor that an unsafe unexpected consumer is reported alongside another deterministic projection error. The isolated second reviewer independently identified both gaps. T1 requires exercise of check/write behavior and explicit failure for every membership or byte drift.
Required outcome: Both unsafe unexpected-consumer topologies must be exercised in check and write modes with immutable outside sentinels, and one direct case must prove the symlink error aggregates deterministically with another projection error.
Safe resolution path: Parameterize or extend the focused regression over `check` and `write`, assert outside bytes before and after each call, and combine one unsafe ungoverned consumer with a missing or stale governed projection while asserting both stable errors.
needs-decision rationale: none
auto_fix_class: mechanical
auto_fix_kind: test-coverage-expansion
affected_paths: scripts/test-boundary-first-reference.py
deterministic_authority: test-spec T1 and R3 second-review required outcome
required_validation: `python scripts/test-boundary-first-reference.py`; `python scripts/project-boundary-first-reference.py --check`

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | Production logic now preserves closed membership and avoids symlink traversal. |
| Test coverage | block | The new topology lacks write-mode non-mutation and combined-error proof. |
| Edge cases | concern | Both topology shapes are covered only in check mode. |
| Error handling | concern | Error aggregation is implemented but not directly proved for the new branch. |
| Architecture boundaries | pass | One source, ten consumers, raw bytes, and shared digest remain unchanged. |
| Compatibility | pass | Existing diagnostics and ordinary unexpected-projection behavior remain intact. |
| Security/privacy | concern | Check-mode containment is direct; write-mode outside non-mutation is inferred only from code shape. |
| Derived artifact currency | pass | Live parity remains ten consumers with the approved digest. |
| Unrelated changes | pass | The correction is limited to enumeration and fixture ownership. |
| Validation evidence | concern | Ten tests pass, but they do not execute the missing proof paths. |

## Second-review evidence

- Second reviewer: isolated `/root/m1_r3_second_review`
- Second-review result: changes-requested
- New finding: PBF-M1-CR4
- Confidence: high on the proof gap and high on implementation containment.
- Unreviewed surfaces: later milestones, Windows-native execution, permission races, write atomicity, and hard-link policy.

## Requirement-fidelity receipt

- Relevant spec clauses decomposed: yes
- Property matrix complete: yes for M1 correction scope
- Multi-surface contracts identified: yes
- Validator assertions checked against spec: yes
- Compressed requirement risk: direct proof omits write and combined-error properties
- Requirement-fidelity no-finding rationale: not applicable because PBF-M1-CR4 is material

## Automation boundary

The active implementation authorization grants two automatic correction cycles.
R1 and R2 consumed those cycles.
R3 therefore records PBF-M1-CR4 but does not enter another correction until the user renews correction authority.

## Milestone handoff

- Reviewed milestone: M1
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining in-scope implementation milestones: M1, M2, M3, M4
- Next stage: blocked pending renewed correction authority
- Final closeout readiness: not ready; PBF-M1-CR4 and downstream work remain open.
