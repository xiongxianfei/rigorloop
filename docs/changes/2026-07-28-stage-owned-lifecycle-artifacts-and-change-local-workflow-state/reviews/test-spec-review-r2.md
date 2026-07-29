# Test Spec Review R2

Review ID: test-spec-review-r2
Stage: test-spec-review
Round: 2
Reviewer: Codex test-spec-review skill
Target: specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.test.md
Status: changes-requested
Review status: changes-requested
Original review source: User-requested test-spec refinement followed by
`$test-spec-review` on 2026-07-29.
Material findings: SLA-TSR4
Immediate next stage: test-spec revision
Implementation handoff: not-allowed
Automatic downstream handoff: none

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: SLA-TSR4
- Recording status: recorded
- Recording blocker: none
- Review record:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/test-spec-review-r2.md`
- Review log:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-log.md`
- Review resolution:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-resolution.md#test-spec-review-r2`
- Open blockers: SLA-TSR4
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: align the remaining test-local milestone labels and rerun
  test-spec-review

## Prior-finding assessment

`SLA-TSR1` is resolved by the progressive activation table, M1/M2
published-guidance tests T23/T24, M3 state activation, T22 placement,
preimplementation/M4 compatibility split, and M6/M7 external-boundary split.

`SLA-TSR2` is resolved.
MP1 and MP2 now name stable IDs, automation rationale, exact gates, reviewer
role, environment, perspectives, steps, evidence, pass/fail conditions, and
escalation.
They are agent-performed pre-PR semantic reviews; human PR review remains the
final external approval after submission.

`SLA-TSR3` is resolved by CP-001 through CP-032.
Every dependent notice cites exactly one stable projection row, and every row
names the source, whole-subject replacement rule, retained disposition, and
replacement tests.

## Findings

## Finding SLA-TSR4

Finding ID: SLA-TSR4
Severity: major
Location: T5, T6, and T19 `Required by milestone` and evidence fields
Evidence: The revised milestone proof map and progressive activation table
correctly defer state-backed author/review settlement to M3.
T5 and T6 still say `Required by milestone: M1` and name M1 evidence, while
T19 still says `M1 and M2` and names M1/M2 evidence.
All three depend on CMD4/CMD6, whose first required milestone is M3.
The published-skill portions are already proved separately by T23 at M1 and
T24 at M2.
Required outcome: Every test-local required milestone and evidence artifact
must agree with the milestone proof map and command ledger.
Safe resolution path: Move T5, T6, and T19 test-local requirement and evidence
labels to M3.
Keep T23/T24 as the earlier published-guidance proof and preserve the
progressive activation table.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| Governing-contract alignment | pass | The proof map preserves published-skill ownership, change-local state, conservative replay, and the external-action boundary. |
| Requirement, example, and edge coverage | pass | The approved requirements, criteria, examples, negative cases, eight boundaries, and seven interactions remain mapped. |
| Proof-level adequacy | pass | Deterministic structure, agent semantic judgment, and post-PR human review have distinct authority. |
| Milestone mapping | block | Three test-local labels still contradict the corrected M3 activation. |
| Command validity | pass | All twelve registered entrypoint files resolve and command ownership is explicit; proof commands were not executed. |
| Manual-proof boundary | pass | MP1/MP2 are exact, bounded agent procedures where scripts cannot establish meaning or path completeness. |
| Compatibility and traceability | pass | CP-001 through CP-032 provide exact, one-to-one prospective dispositions. |
| Implementation handoff | block | M1 cannot begin while test-local timing contradicts the milestone table. |

## Review boundary

Boundary-first structural validation passed for the feature/test-spec pair.
The 32 projection IDs and 32 dependent notices are unique and one-to-one.
No proof command, fixture suite, network action, secret access, external
action, or implementation validation was executed during review.

## Recommendation

Changes requested.

Correct the three test-local M3 labels and rerun `test-spec-review`.
This formal review is isolated and does not authorize implementation or
advance workflow routing.
