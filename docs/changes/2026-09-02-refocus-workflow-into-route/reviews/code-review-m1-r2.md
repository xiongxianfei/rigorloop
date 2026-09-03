# Code Review M1 R2: Workflow Context Corrections

Review ID: code-review-m1-r2
Stage: code-review
Round: r2
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: correction commit a8ec338c; workflow return commit da8a5a81 contains routing state only
Reviewed artifact: M1 correction 47a87bb8..a8ec338c
Reviewed milestone: M1
Review date: 2026-09-02
Status: changes-requested
Review status: changes-requested
Material findings: RFR-M1-CR4, RFR-M1-CR5
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-09-02-refocus-workflow-into-route/reviews/code-review-m1-r2.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/review-log.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/review-resolution.md`
- Open blockers: RFR-M1-CR2, RFR-M1-CR3, RFR-M1-CR4, RFR-M1-CR5
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: RFR-M1-CR4, RFR-M1-CR5
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-09-02-refocus-workflow-into-route/reviews/code-review-m1-r2.md`
- Review log: `docs/changes/2026-09-02-refocus-workflow-into-route/review-log.md`
- Review resolution: `docs/changes/2026-09-02-refocus-workflow-into-route/review-resolution.md`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3
- Required review-resolution: yes
- Finding IDs: RFR-M1-CR4, RFR-M1-CR5
- Verify readiness: not-claimed

## Scope and authority

R2 independently inspected the complete correction against Design Review `design-review-r1`, Delivery Review `delivery-review-r1`, M1 TG-01 through TG-05, and the three R1 findings. The review checked the implementation diff, public rendering, exact selection, tests, schema, documentation, and recorded validation. The implementation remained untouched during review.

## R1 finding reconciliation

| Finding | R2 classification | Evidence |
| --- | --- | --- |
| RFR-M1-CR1 | resolved | Four stage-specific review-record kinds now preserve proposal-review, design-review, delivery-review, and code-review ownership; wrong-owner overrides fail directly. |
| RFR-M1-CR2 | failed-remediation | JSON projections are capped and unsafe current-stage values fail closed, but human candidate output omits the available truncation facts. |
| RFR-M1-CR3 | failed-remediation | Exact selection is isolated in code and broader byte-identity tests exist, but no test reaches `RL_CONTEXT_READ_FAILED` or proves interruption leaves the governed/config tree unchanged. |

## Findings

## Finding RFR-M1-CR4

Finding ID: RFR-M1-CR4
Severity: major
Location: `packages/rigorloop/dist/lib/workflow-context.js:271-283`; `packages/rigorloop/test/workflow-context.test.js:148-169`
Evidence: Project JSON records `candidate_total_count` and `candidates_truncated`, but `workflowContextHuman` prints only the first 32 candidates and `Selection: ambiguous`. A user cannot tell that candidates were omitted, even though the README says count and truncation fields show when exact selection is required. This leaves the human side of RT-R35 and the RFR-M1-CR2 actionable-output outcome incomplete.
Required outcome: Human project output must state the total candidate count, whether the list is truncated, and that exact `--change` selection is required when truncation occurs.
Safe resolution path: Render the existing count/truncation fields in the shared human formatter and add a public human regression with more than 32 active candidates; do not add a new result model or byte-budget framework.
needs-decision rationale: none; the existing JSON model already contains the required facts.

## Finding RFR-M1-CR5

Finding ID: RFR-M1-CR5
Severity: major
Location: `packages/rigorloop/dist/lib/workflow-context.js:386-395`; `packages/rigorloop/test/workflow-context.test.js:207-251`
Evidence: The production wrapper normalizes thrown reads as `RL_CONTEXT_READ_FAILED`, but the added filesystem test takes the ordinary non-file configuration branch and expects `RL_CONTEXT_PATH_UNSAFE`; it never exercises the catch boundary. The retry test covers success, ambiguity, configuration rejection, and mutation but not process interruption. The malformed-unrelated test proves successful exact selection, while the implementation diff supplies the isolation mechanism. TG-05 and RFR-M1-CR3 explicitly require direct failure and interruption proof over the complete governed/config surface.
Required outcome: Direct tests must exercise unexpected read normalization and an interrupted public invocation, and must prove the complete governed/config tree remains byte-identical in both cases.
Safe resolution path: Add one narrow deterministic read-fault seam at the workflow-context boundary and one public child-process interruption test, each test-only controlled and without a general filesystem abstraction; retain the complete-tree snapshot helper.
needs-decision rationale: none; this is proof already allocated to M1.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | Structural output is bounded, but human truncation disclosure remains incomplete. |
| Test coverage | block | Unexpected-read and interruption paths lack direct TG-05 proof. |
| Edge cases | concern | Truncated human output does not disclose omitted candidates. |
| Error handling | concern | The normalized catch exists but is unexercised. |
| Architecture boundaries | pass | Review ownership is no longer collapsed and CLI remains structural. |
| Compatibility | pass | Exact requested-change selection no longer parses unrelated records. |
| Security/privacy | pass | Unsafe current-stage and path values are not emitted. |
| Derived artifact currency | pass | M1 schema and package documentation match the correction; adapters remain M3. |
| Unrelated changes | pass | The correction stays within M1 and accepted findings. |
| Validation evidence | concern | All named commands pass, but they do not cover the two required outcomes above. |

## Validation inspected

- Plan-selected Node suite: 174 passed.
- Full package suite: 358 passed, 2 skipped.
- Change-metadata validator: 107 passed.
- Schema parse, direct CLI invocation, and `git diff --check`: passed.

## Handoff

M1 remains open. Workflow should route RFR-M1-CR2 through RFR-M1-CR5 to the M1 implementer for the two narrow corrections, then request Code Review M1 R3. M2 and M3 remain planned; final readiness is not claimed.
