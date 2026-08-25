# Proposal Review R1: Workflow-Routed Upstream Corrections

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewed artifact: docs/proposals/2026-08-25-workflow-routed-upstream-corrections.md
Target: docs/proposals/2026-08-25-workflow-routed-upstream-corrections.md
Reviewed artifact identity: sha256:3c14ab7974a87a7c6ba534119b2ffe83c7b1c0ffc35c8c0441e9a053e3c1fed1
Review date: 2026-08-25
Reviewer: Codex proposal-review with fresh-assumption reset
Recording mode: formal-lifecycle
Automation mode: manual
Assembly: PRR1G-recorded-context-gated
Status: changes-requested
Recording status: recorded
Material findings: WRUC-PR1

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: WRUC-PR1
- Open blockers: the scope budget makes duplicate-registration withdrawal optional even though the proposal promises to unblock the observed duplicate
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none; workflow owns routing
- Claim limitations: this review does not approve a specification, architecture, implementation, verification, branch, or PR

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The proposal separates correct fail-closed rejection from the absence of a supported corrective transition. |
| User value | pass | It restores resumable upstream correction without returning lifecycle mechanics to skills. |
| Option diversity | pass | Direct mutation, blocker bypass, and operation-oriented routing are materially different choices. |
| Decision rationale | pass | The recommended authority split follows the existing Git-first CLI boundary. |
| Vision fit | pass | The change improves repository-contained traceability and does not introduce autonomous orchestration. |
| Scope control | block | The proposal promises recovery for the current duplicate registration while classifying withdrawal only as a first-slice candidate. |
| Architecture awareness | pass | The public schema, transaction, discovery, authority, and compatibility impacts are explicit. |
| Testability | pass | Route, replay, collision, withdrawal, recovery, and diagnostic outcomes are observable. |
| Risk honesty | pass | The main authority and recovery risks have concrete mitigations. |
| Rollout realism | concern | Rollout is workable once the withdrawal commitment is unambiguous. |
| Readiness for spec | block | Specification cannot know whether duplicate-withdrawal behavior is mandatory. |

## Scope Preservation Review

- Scope-preservation result: changes requested. The user's request to address the current duplicate architecture registration is listed as in scope, but its only recovery operation is not committed to the same slice.

## Recommended Proposal Edits

- Change duplicate-registration withdrawal from `first-slice candidate` to `same-slice dependency`.
- State that collision prevention and withdrawal ship together, while repair of the observability branch remains a separate consuming change.

## Recommendation

- Recommendation: revise the scope budget and rollout commitment, then rerun proposal review on the exact revised identity.

## Specialized-gate group

- Active gate predicates: scope_budget_context
- Gate outcomes: changes requested because one core promised outcome has an optional treatment
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: docs/changes/2026-08-25-workflow-routed-upstream-corrections/reviews/proposal-review-r1.md
- Finding-record paths: this record and review-resolution.md#WRUC-PR1

## Formal-settlement group

- Review ID: proposal-review-r1
- Review record: docs/changes/2026-08-25-workflow-routed-upstream-corrections/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-08-25-workflow-routed-upstream-corrections/review-log.md
- Review resolution: docs/changes/2026-08-25-workflow-routed-upstream-corrections/review-resolution.md
- Proposal settlement: changes requested; exact settlement pending CLI recording
- Governed change identity: 2026-08-25-workflow-routed-upstream-corrections, artifact proposal
- Formal next-stage eligibility: proposal revision only

## Finding WRUC-PR1

Finding ID: WRUC-PR1
Severity: material
Location: Scope budget, Narrow duplicate-registration withdrawal
Evidence: The goals, recommended direction, initial-intent table, and rollout promise a supported repair for the active duplicate registration, but the scope budget classifies that repair only as a `first-slice candidate`.
Required outcome: Make guarded withdrawal a committed same-slice dependency or explicitly defer the current duplicate blocker and narrow the proposal's promises consistently.
Safe resolution path: Select the same-slice treatment, align rollout language, preserve observability-branch consumption as a separate implementation slice, and rerun proposal review.
needs-decision rationale: none; the user already requested that the current blocker be addressed.
