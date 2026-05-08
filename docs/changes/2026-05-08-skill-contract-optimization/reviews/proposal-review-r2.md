# Proposal Review R2

Review ID: proposal-review-r2
Stage: proposal-review
Round: 2
Reviewer: Contributor proposal-review
Target: docs/proposals/2026-05-08-skill-contract-optimization.md
Status: approve

## Review inputs

- Proposal: `docs/proposals/2026-05-08-skill-contract-optimization.md`
- Prior review record: `docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md`
- Prior review resolution: `docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md`

## Verdict

Ready with decisions added.

The proposal direction is sound: define a normative `specs/skill-contract.md`, normalize the highest-risk lifecycle skills first, then expand in phases.

## Decisions added

- Later-phase normalization order uses three follow-on waves: core lifecycle authoring and review skills; on-demand and standing or living-reference skills; newly adopted optional skills when they exist and own approved artifacts or gates.
- Shared blocks ready for v1 are `review-isolation-and-recording`, `evidence-collection-efficiency`, and `generated-output-handling`.
- Shared blocks deferred until stable are `vision-fit`, `plan-readiness-vs-completion`, `milestone-aware-review-handoff`, `first-pass-completeness`, and `material-finding-requirements` if still under active simplification.
- Shared-block delivery for v1 is copy into canonical skills with `scripts/test-skill-validator.py` drift checks; generation is deferred.
- Forbidden-overclaim validation stays positive-first, narrow, and incident-based.
- Minimum viable skill guidance is normative in `specs/skill-contract.md`, summarized in `docs/workflows.md` and `AGENTS.md`, and detailed in skill-creator guidance.

## Findings

No material findings.

## Checklist coverage

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | The proposal targets recurring skill overclaim and state-confusion issues. |
| User value | pass | Smaller, claim-safe skills support traceable agent behavior. |
| Option diversity | pass | The proposal compares no change, patch-only, phased contract, and central-router options. |
| Decision rationale | pass | The proposal now records rollout, shared-block, validator, and skill-creation decisions. |
| Scope control | pass | The first slice is limited to seven lifecycle skills. |
| Architecture awareness | pass | Normative ownership is assigned to `specs/skill-contract.md` with workflow-spec pointer scope. |
| Testability | pass | The proposal describes positive required wording, narrow forbidden phrases, shared-block drift, and generated-output checks. |
| Risk honesty | pass | Risks around over-normalization, shared-block rigidity, validator overfit, and generated drift are covered. |
| Rollout realism | pass | Rollout is phased and rollback is straightforward. |
| Readiness for spec | pass | Open questions are resolved enough for feature spec authoring. |

## Recommended next stage

Feature spec authoring for `specs/skill-contract.md`.
