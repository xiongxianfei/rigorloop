# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Target: docs/proposals/2026-05-25-installed-skill-artifact-placement-contract.md
Reviewed artifact: docs/proposals/2026-05-25-installed-skill-artifact-placement-contract.md
Review date: 2026-05-25
Reviewer: Codex proposal-review
Recording status: recorded
Status: approved

## Result

- Skill: proposal-review
- Review status: approved
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-25-installed-skill-artifact-placement-contract/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-log.md
- Review resolution: not-required
- Open blockers: none
- Immediate next stage: spec

## Outcome

- Review status: approved with observations
- Material findings: none
- Blocking findings: none

## Scope checked

- Problem framing and adopter value.
- Placement-in-skills options and early-lifecycle recording locality options.
- Plan-surface disambiguation.
- Skill/workflow-guide drift-check binding.
- Testability, rollout, rollback, and first-slice scope.

## Review Dimensions

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | The split-contract diagram directly identifies the gap between installed skills and repo-local workflow guidance. |
| User value | pass | The proposal serves skill-only adopters at the point where the confusion appeared. |
| Option diversity | pass | Six options cover placement surface and early-lifecycle locality. |
| Decision rationale | pass | Option 3 plus Option 6 is defended and acknowledges the dual-surface maintenance cost. |
| Scope control | pass | The first slice is limited to proposal-review, spec-review, plan-surface disambiguation, workflow sync, validation, and adapter validation. |
| Architecture awareness | pass | Skills own placement, workflow docs own project-local maps, specs/schemas own exact shape, and validators prevent drift. |
| Testability | pass | SAP checks include deterministic strings, synchronization checks, and cold-read proofs. |
| Risk honesty | pass | Skill verbosity, drift, casual-review ceremony, customization, and validator overfitting risks are named. |
| Rollout realism | pass | The rollout starts with review skills, synchronizes workflow guidance, validates adapters, and runs cold-read proof. |
| Readiness for spec | pass | Open questions are specific enough for the spec to answer. |

## Scope Preservation Review

- Scope-preservation result: pass. The proposal classifies the initial adopter-confusion signal, placement-in-skills direction, early lifecycle locality, plan-surface ambiguity, workflow-guide synchronization, drift validation, and project-local customization preservation.

## Observations

### OBS-1 - Change-pack-first needs creation ownership pinned in the spec

Type: observation
Severity: low-medium
Location: Recommended Direction; Open Questions 1 and 2
Evidence: Option 6 resolves where early findings go, but the proposal leaves who creates the pack and whether change-pack-first applies to all reviews or only material-finding reviews as open questions.
Suggested spec treatment: Promote "proposal creates the change pack when authoring a workflow-managed proposal" to a spec rule. Review skills should create or block when a formal review is requested and no pack exists, as a safety fallback rather than the primary path.

### OBS-2 - Workflow-guide precedence should be per artifact, not by mere presence

Type: observation
Severity: low
Location: Recommended Direction; Open Question 3
Evidence: The proposal says to use the project workflow guide when present, then use the portable default when no project-local map exists. A present but partial workflow guide should not suppress portable defaults for artifacts it does not specify.
Suggested spec treatment: State that `docs/workflows.md` takes precedence for artifacts it specifies. For artifacts it does not specify, the portable default applies. Block only when explicit paths, active metadata, governing constraints, the workflow guide, and the portable default fail to resolve placement.

## Answers for Spec Authoring

| Question | Proposal-review answer |
|---|---|
| Who creates the first formal lifecycle artifact? | `proposal` creates the change pack when authoring a workflow-managed proposal. Review skills create or block only as fallback. |
| Change-pack-first for all formal reviews or only material-finding reviews? | All formal lifecycle reviews. Clean reviews still need durable receipts. |
| Should `docs/workflows.md` remain above portable defaults? | Yes, for artifacts it specifies. Portable defaults fill gaps in a partial workflow guide. |
| Where should the drift check live? | `validate-skills.py` should own the first deterministic skill/workflow placement drift check. |
| First slice: all review skills or proposal-review plus spec-review? | Start with `proposal-review` and `spec-review`, plus plan-surface disambiguation, then generalize after proof. |

## Recommended Proposal Edits

- Recommended edits: none required before spec. The observations should be resolved in the placement-contract spec.

## Recommendation

- Recommendation: approved with observations. Advance to the installed-skill artifact placement contract spec when the user requests downstream work. The spec should promote proposal-authored change-pack creation to a rule, make change-pack-first unconditional for formal lifecycle reviews, define workflow-guide precedence per artifact, put the first drift check in `validate-skills.py`, and scope the first implementation slice to proposal-review, spec-review, and plan-surface disambiguation.

## No-finding statement

Clean formal review completed with no material findings.
