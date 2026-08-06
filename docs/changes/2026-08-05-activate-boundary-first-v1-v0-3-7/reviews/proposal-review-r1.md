# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: independent Codex proposal-review peer
Target: docs/proposals/2026-08-05-activate-boundary-first-v1-v0-3-7.md
Status: changes-requested
Material findings: BFA-PR1-001
Scope-preservation result: pass
Immediate next stage: proposal revision
Automatic downstream handoff: workflow-owned after recording

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: BFA-PR1-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/review-log.md`
- Review resolution: `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/review-resolution.md`
- Open blockers: BFA-PR1-001
- Immediate next stage: proposal revision

## Material Findings

## Finding BFA-PR1-001

Finding ID: BFA-PR1-001
Severity: major
Location: Recommended direction; testing and verification strategy; rollout and rollback
Evidence: The proposal requires verified PR readiness before tag creation, but `scripts/boundary_first_validation.py` rejects an active manifest unless the activating tag already exists and resolves to the exact first-parent pending-to-active transition commit. A pending PR cannot prove the proposed active release state, while an active PR cannot pass the current strict tag-bound validator before publication.
Required outcome: Define separate candidate and tag-context validation phases with exact evidence, transition identity, publication stop, and rollback behavior.
Safe resolution path: Amend the proposal to include a narrow pre-tag candidate-validation mode that validates the proposed active tree and expected release identity without accepting it as published; keep the existing strict tag-existence, predecessor, and tag-to-transition proof in the release-owned tag context. Route the normative behavior through the new spec and architecture assessment.
needs-decision rationale: none; this is a required feasibility correction and the smallest safe direction preserves the selected stable-release objective.

## Review Dimensions

- Problem clarity: pass
- User value: pass
- Option diversity: pass
- Decision rationale: pass
- Scope control: concern; the proposal incorrectly classifies all release-tooling changes as out of scope despite the required candidate-validation bridge.
- Architecture awareness: concern; the pre-tag and tag-context authority boundary is missing.
- Testability: block; the stated pre-tag PR gate cannot pass the current strict validator.
- Risk honesty: concern; partial release sequencing is named, but the validator/tag circularity is not.
- Rollout realism: block; no feasible reviewed transition from pending PR to immutable tagged activation is defined.
- Readiness for spec: block until BFA-PR1-001 is resolved and rereviewed.

## Scope Preservation Review

- Scope-preservation result: pass. The user's activation and publication objective remains in scope, the concise-solution constraint is explicit, and publication is separated only because it is an external-action boundary.

## Recommended Proposal Edits

- Recommended edits: Add the smallest candidate-validation bridge to goals, non-goals, recommended direction, architecture impact, testing, rollout, risks, scope budget, decision log, and next-artifact scope. State that candidate success is not active-release proof and that tag-context validation remains strict and publication-blocking.

## Recommendation

- Recommendation: changes-requested. Record BFA-PR1-001, revise the proposal without changing the selected `v0.3.7` direction, then run proposal-review R2 before specification.
