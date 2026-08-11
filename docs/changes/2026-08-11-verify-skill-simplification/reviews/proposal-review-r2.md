# Proposal Review R2: Verify Skill Simplification

Review ID: proposal-review-r2
Stage: proposal-review
Round: r2
Reviewer: user-supplied independent proposal-review
Target: docs/proposals/2026-08-11-verify-skill-simplification.md
Reviewed artifact: `docs/proposals/2026-08-11-verify-skill-simplification.md` at commit `77038be4`
Status: changes-requested
Review date: 2026-08-11
Recording status: recorded

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: VFSIM-PR1, VFSIM-PR2, VFSIM-PR3
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-08-11-verify-skill-simplification/reviews/proposal-review-r2.md
- Review log: docs/changes/2026-08-11-verify-skill-simplification/review-log.md
- Review resolution: docs/changes/2026-08-11-verify-skill-simplification/review-resolution.md
- Open blockers: requested outcomes, execution authority, and evidence-rule ownership require proposal revision
- Immediate next stage: proposal revision

## Material Findings

### Finding VFSIM-PR1

Finding ID: VFSIM-PR1
Severity: major
Location: Recommended Direction, Closed invocation profiles
Evidence: `branch_readiness_context` combines governed final verify with user requests for branch, workflow-closeout, or release-sensitive readiness without a closed outcome vocabulary or exact repository, branch or commit, and change or evidence-root resolution. A direct request can therefore be mistaken for governed final verification, and ambiguous targets have no deterministic stop result.
Required outcome: Define closed requested outcomes, treat release sensitivity as evidence applicability rather than a readiness claim, resolve exactly one branch or commit and change or evidence root for branch readiness, and require valid governed final-verify state for workflow final verification.
Safe resolution path: Use `scoped-verification`, `branch-readiness`, and `workflow-final-verification`; add exact target-resolution and ambiguity stops; allow direct branch readiness but reserve workflow final verification for governed state.
needs-decision rationale: none; the reviewer supplied a deterministic recommended resolution.

### Finding VFSIM-PR2

Finding ID: VFSIM-PR2
Severity: major
Location: Recommended Direction, Closed invocation profiles; Conditional branch-readiness reference ownership
Evidence: Direct branch-readiness assessment and governed final verification load the same `VP1` package, while only governed final verification may perform formal verify-owned recording and handoff behavior. The proposal does not independently classify execution authority, so Phase C, recording, lifecycle progression, and `pr` behavior could be applied to the wrong invocation.
Required outcome: Keep loaded-package profiles separate from a closed execution-authority axis, preserve verify, workflow, and pr write boundaries, and explicitly distinguish isolated completion from governed-final completion.
Safe resolution path: Add `isolated` and `governed-final` execution modes; state that resources determine available procedure while execution mode determines permitted branches and writes; prohibit isolated lifecycle advancement and PR invocation.
needs-decision rationale: none; the reviewer supplied a deterministic recommended resolution.

### Finding VFSIM-PR3

Finding ID: VFSIM-PR3
Severity: major
Location: Universal SKILL.md ownership; Conditional branch-readiness reference ownership
Evidence: The reference is assigned targeted proof, CI evidence, generated-output drift, manual proof, and release-sensitive evidence semantics even though scoped requests may assess any one of those evidence classes without performing final readiness. `VP0` would therefore lack procedure needed for valid scoped verification.
Required outcome: Keep universal evidence-type interpretation inline and limit the conditional reference to final evidence applicability, completeness, aggregation, closeout, and readiness calculation.
Safe resolution path: Keep actual-run, freshness, status, CI truthfulness, generated-output currency, manual-proof validity, ambiguity, escalation, and external-action boundaries inline; move only change-wide evidence composition and final blocker aggregation behind the branch-readiness trigger.
needs-decision rationale: none; the reviewer supplied a deterministic recommended resolution.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Scoped verification currently loads final-closeout procedure it often cannot use. |
| User value | pass | A shorter direct profile is valuable without weakening readiness proof. |
| Option diversity | pass | The alternatives are materially different. |
| Decision rationale | pass | One final-readiness reference remains the right package direction. |
| Scope control | pass | The proposal stays bounded to verify and its package surfaces. |
| Architecture awareness | pass | `architecture-not-required` remains plausible after bounded assessment. |
| Testability | block | Requested outcomes and target identity are not deterministic enough for fixtures. |
| Risk honesty | concern | Direct versus governed write authority and scoped evidence semantics need closure. |
| Rollout realism | pass | Missing-resource and package rollout behavior are sound. |
| Readiness for spec | block | VFSIM-PR1 through VFSIM-PR3 require proposal-level resolution. |

## Scope Preservation Review

- Scope-preservation result: pass. The selected package design and initial user goals remain visible.
- Scope-budget result: pass. The findings clarify existing core work rather than expanding the proposal into another skill or runtime.
- Vision-fit result: pass. The direction remains consistent with the current vision.

## Recommended Proposal Edits

- Recommended edits: add the three-value requested-outcome contract and target-resolution rules; add an independent two-value execution-mode contract and authority matrix; move universal evidence interpretation inline while limiting the reference to final applicability and aggregation.

## Recommendation

- Recommendation: changes requested. Revise the proposal to resolve VFSIM-PR1 through VFSIM-PR3, then perform an independent proposal-review rerun. No automatic downstream handoff follows this review.
