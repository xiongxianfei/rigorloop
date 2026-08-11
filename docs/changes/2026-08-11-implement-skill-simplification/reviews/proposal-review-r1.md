# Proposal Review R1: Implement Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex proposal-review skill
Target: docs/proposals/2026-08-11-implement-skill-simplification.md
Reviewed artifact: `docs/proposals/2026-08-11-implement-skill-simplification.md`
Status: changes-requested
Review date: 2026-08-11
Recording status: recorded

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: IMPSIM-PR1, IMPSIM-PR2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-08-11-implement-skill-simplification/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-08-11-implement-skill-simplification/review-log.md
- Review resolution: docs/changes/2026-08-11-implement-skill-simplification/review-resolution.md
- Open blockers: the optimized invocation profile and conditional-resource ownership model are not yet closed
- Immediate next stage: proposal revision

## Material Findings

### Finding IMPSIM-PR1

Finding ID: IMPSIM-PR1
Severity: major
Location: Goals; Options Considered O3; Recommended Direction; Testing and Verification Strategy
Evidence: The proposal treats `SKILL.md` reduction as the common-path result, but a normal planned workflow-managed implementation would load `SKILL.md` plus `workflow-managed-implementation.md`. The proposed measurements report `SKILL.md`, the reference, and the total package, but do not report loaded context by invocation profile. A 30–45 percent main-file reduction could therefore coincide with no reduction—or an increase—for the planned-milestone journey that is central to this stage.
Required outcome: Define the invocation profiles being optimized and require separate loaded-context accounting for isolated implementation, planned workflow-managed milestone execution, and armed review-fix execution. Identify which profiles must materially improve and prevent a file-only reduction from being reported as user-journey simplification.
Safe resolution path: Add a profile table to the proposal, measure the exact mapped resources loaded by each profile before and after, retain total-package accounting, and keep percentage values non-normative. The proposal author should make planned workflow-managed execution an explicit optimization target or explain why it is intentionally excluded.
needs-decision rationale: The proposal-owning stage must decide whether planned workflow-managed execution is a primary success profile; no downstream stage should infer that product choice from a `SKILL.md` percentage.

### Finding IMPSIM-PR2

Finding ID: IMPSIM-PR2
Severity: major
Location: Scope Budget; Options Considered O3 and O4; Recommended Direction; Expected Behavior Changes
Evidence: The single proposed `workflow-managed-implementation.md` reference loads for every planned workflow-managed milestone, yet it owns both ordinary planned-milestone procedure and automation-only adversarial-review packet, forbidden-context, auto-fix, and Phase C rules. This makes all planned milestones load automation procedure even when no automated review or correction loop is armed, weakening the progressive-disclosure rationale and obscuring two distinct authority boundaries.
Required outcome: Select a package ownership model that separates ordinary planned-milestone procedure from armed automation-only review and correction procedure, or provide evidence that every planned workflow-managed milestone requires the automation content. Exact load triggers and universal inline policy must be decided at proposal level.
Safe resolution path: Prefer two bounded references—one for planned milestone execution and one for armed automated review/correction—plus the single output asset. Keep purpose, authority, test-first behavior, first-pass completeness, validation, scope, stops, claims, direct handoff, and both resource triggers inline. Update O3/O4 comparison, package shape, risks, scenarios, and metrics accordingly.
needs-decision rationale: The proposal-owning stage must choose one-reference versus two-reference ownership. Proposal-review recommends two because the current single-reference design couples distinct invocation and authority profiles.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The proposal identifies concrete repetition, conditional procedure, and usability cost without reducing the problem to a token target. |
| User value | pass | Direct and isolated implementation clarity is explicit and aligned with the preceding successful optimization. |
| Option diversity | pass | O0 through O4 present materially different costs and benefits. |
| Decision rationale | concern | O3 is plausible, but the comparison does not evaluate loaded context for planned versus armed profiles. |
| Scope control | pass | Other skills, workflow order, runtime testing, and permanent simplicity gates are excluded clearly. |
| Architecture awareness | concern | Package ownership is discussed, but one reference currently combines two distinct conditional authorities. |
| Testability | concern | Structural, package, scenario, and semantic proof is strong; profile-specific loaded-context success is missing. |
| Risk honesty | pass | Semantic loss, trigger errors, literal compatibility, package growth, fragmentation, and validator overreach are named. |
| Rollout realism | pass | Atomic package rollout and rollback are bounded and compatible with existing generation. |
| Readiness for spec | concern | IMPSIM-PR1 and IMPSIM-PR2 require proposal-level decisions before a specification can encode exact triggers and success evidence. |

## Scope Preservation Review

- Scope-preservation result: pass. Every initial user goal is classified, the request is not silently narrowed, and other-skill optimization is explicitly routed to separate proposals.
- Scope-budget result: pass. Core package work, same-slice proof and architecture assessment, separate proposals, and out-of-scope validator work are classified with allowed treatment values.
- Vision-fit result: pass. `fits the current vision` is valid and supported by the repository's reviewability, traceability, and usable-artifact commitments.

## Recommended Proposal Edits

- Recommended edits: define isolated, planned, and armed invocation profiles; report before/after loaded context for each; make planned execution an explicit success target; replace the single conditional procedure reference with separate planned-milestone and automation-only references unless contrary evidence is recorded; update package shape, option rationale, scenarios, risks, and decision log.

## Recommendation

- Recommendation: revise the proposal to close IMPSIM-PR1 and IMPSIM-PR2, then run proposal-review R2. Do not proceed to specification until the invocation-profile success model and conditional-reference ownership are settled. No automatic downstream handoff follows this review.
