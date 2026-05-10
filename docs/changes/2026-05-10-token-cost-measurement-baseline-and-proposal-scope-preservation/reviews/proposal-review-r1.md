# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Codex proposal-review
Target: docs/proposals/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md
Status: revise

## Review inputs

- Proposal: `docs/proposals/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md`
- Governance: `CONSTITUTION.md`, `AGENTS.md`, `VISION.md`
- Prior proposal: `docs/proposals/2026-05-09-skill-token-cost-optimization.md`
- Learn session: `docs/learn/sessions/2026-05-10-skill-token-measurement-scope-narrowing.md`

## Findings

### TCSP-PR1-F1 - Downstream artifact wording makes spec optional

Finding ID: TCSP-PR1-F1
Severity: material
Evidence: The proposal's rollout step 2 says "Write focused spec or implementation plan for measurement and proposal-scope preservation," and `Next artifacts` lists "focused spec or implementation plan." The proposal also changes contributor-visible skill behavior and proposal-review behavior, adds new measurement scripts, and introduces validation expectations for skill and adapter surfaces. `CONSTITUTION.md` says changes that affect externally observable behavior must have an approved spec before implementation, and specs must define non-goals and compatibility expectations for behavior-changing work.
Required outcome: The proposal must make focused spec authoring the required next artifact before execution planning or implementation relies on the proposal.
Safe resolution: Replace "focused spec or implementation plan" with "focused spec, then implementation plan if the accepted spec requires one" in `Rollout and rollback` and `Next artifacts`. Update `Readiness` to say ready for proposal revision, then proposal-review, then spec once the proposal is accepted.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | The proposal states both the missing measurement baseline and the process defect that let initial scope disappear. |
| User value | pass | The value is concrete: evidence-based token optimization and reviewable proposal narrowing. |
| Option diversity | pass | It compares measurement-only, proposal-skill-only, and combined workstreams. |
| Decision rationale | pass | The recommended combined option follows from the incident evidence and avoids reopening PR #39. |
| Scope control | pass | Non-goals rule out PR #39 reopening, hosted telemetry, hard token-budget gates, all-skill rewrites, and proposal-review authoring responsibility. |
| Architecture awareness | pass | The proposal identifies workflow, skill, script, generated-output, docs, and adapter surfaces while stating no runtime architecture impact. |
| Testability | pass | The measurement outputs, validator checks, generated-output drift checks, and adapter validation can be specified and verified. |
| Risk honesty | pass | Risks cover skill weight, review intrusiveness, approximate estimates, script maintenance, and over-preserving scope. |
| Rollout realism | concern | Rollout is realistic after TCSP-PR1-F1 removes the optional-spec path. |
| Readiness for spec | revise | Direction is strong, but the proposal needs the spec-stage correction before downstream spec authoring relies on it. |

## Scope preservation review

Pass. The proposal includes `Initial Intent Preservation`, and every initial goal in the triggering request is visibly classified as in scope, out of scope, or deferred follow-up. The proposal does not silently narrow the request.

## Vision fit review

Pass. The proposal includes `Vision fit` with the exact allowed value `fits the current vision`, and root `VISION.md` exists.

## Standing artifact gate review

Pass. `VISION.md` and `CONSTITUTION.md` exist, and this proposal does not bypass a bootstrap gate.

## Recommended next stage

Revise the proposal to resolve TCSP-PR1-F1, then rerun proposal-review. This review is isolated and does not automatically hand off to spec.
