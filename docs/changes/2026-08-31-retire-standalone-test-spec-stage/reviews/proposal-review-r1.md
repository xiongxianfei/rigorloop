# Proposal Review R1: Retire the Standalone Test-Spec Stage

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex proposal-review with fresh-assumption reset
Target: `docs/proposals/2026-08-31-retire-standalone-test-spec-stage.md`
Reviewed artifact path: docs/proposals/2026-08-31-retire-standalone-test-spec-stage.md
Reviewed artifact identity: sha256:ecb6d3be476a2d3b0fe4790142121fe8cfa4af58d3afb9597182a2a80952148c
Review date: 2026-08-31
Recording mode: formal-lifecycle
Automation mode: manual
Assembly: PRR1G-recorded-context-gated
Status: changes-requested
Material findings: RTS-PR1

## Result

- Skill: proposal-review
- Review status: changes-requested
- Vision alignment: aligned
- Material findings: RTS-PR1
- Open blockers: the proposal's vision-conflict disclosure and requested action are stale after the authorized vision revision
- Proposal readiness: revision required before Design
- Immediate next stage: proposal revision
- Automatic downstream handoff: none; workflow owns routing
- Claim limitations: this review does not approve Design, Delivery, implementation, verification, branch, or PR readiness

## Review Dimensions

- Review dimensions: Challenge pass; Goals pass; Scope pass; Governing principle pass; Direction pass; Feasibility pass; Material impact concern; Vision alignment pass; Downstream authority pass; Requested decision concern.

The retirement direction remains valuable, bounded, and feasible. It preserves pre-implementation verification responsibility, keeps engineering-led milestone decomposition, identifies compatibility and predecessor constraints, and leaves detailed schema, migration, reference, and proof mechanics downstream. Current `VISION.md` now expresses the same artifact-independent traceability model, so the proposal no longer needs a vision exception or future vision-revision decision.

## Scope Preservation Review

- Scope-preservation result: pass. Every initial goal remains visible, the broad implementation surface is classified, and historical compatibility plus in-flight handling remain explicit.

## Recommended Proposal Edits

- Recommended edits: change the vision discussion from a current conflict and requested future revision to completed upstream alignment; remove decision item 11 as an outstanding action while retaining the requirement that implementation remain consistent with the revised vision.

## Recommendation

- Recommendation: changes-requested. Correct the stale vision state without changing the retirement direction, then perform same-stage proposal rereview.

## Specialized-gate group

- Active gate predicates: scope_budget_context
- Gate outcomes: pass; core work, same-slice dependencies, downstream Design decisions, separate implementation slices, and exclusions remain distinguishable
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: docs/changes/2026-08-31-retire-standalone-test-spec-stage/reviews/proposal-review-r1.md
- Finding-record paths: this record and docs/changes/2026-08-31-retire-standalone-test-spec-stage/review-resolution.md#rts-pr1

## Formal-settlement group

- Review ID: proposal-review-r1
- Review record: docs/changes/2026-08-31-retire-standalone-test-spec-stage/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-08-31-retire-standalone-test-spec-stage/review-log.md
- Review resolution: docs/changes/2026-08-31-retire-standalone-test-spec-stage/review-resolution.md
- Proposal settlement: changes requested; exact CLI settlement pending
- Governed change identity: 2026-08-31-retire-standalone-test-spec-stage
- Formal next-stage eligibility: proposal revision only

## Finding RTS-PR1

Finding ID: RTS-PR1

Severity: material

Location: `Impact and major trade-offs`; `Decision requested` item 11 and closing authority paragraph

Evidence: `VISION.md` at `sha256:d3e6268fce3aec69785fdfd75551694b08e391a8be30ad39751aa3d64aa5d39f` already replaces the standalone test-plan/test-spec chain with testable requirements, architecture, verification-aware planning, concrete proof, and evidence. The proposal still says the current vision mandates a separate artifact and asks the implementing change to revise it.

Required outcome: make the proposal accurately describe vision alignment and avoid requesting an action that has already completed.

Safe resolution path: state that the upstream vision revision is complete, preserve its traceability commitments as a constraint, remove the outstanding vision-revision decision item, record the revised proposal identity, and rerun Proposal Review.

needs-decision rationale: none; the owner explicitly authorized and completed the vision revision.
