# Proposal Review R1: Proposal-Review Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex independent product, engineering, and delivery reviewer
Target: docs/proposals/2026-08-11-proposal-review-skill-simplification.md
Reviewed artifact: `docs/proposals/2026-08-11-proposal-review-skill-simplification.md` at commit `57e2c85d`
Status: changes-requested
Review date: 2026-08-11
Recording status: recorded

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PRSIM-PR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-08-11-proposal-review-skill-simplification/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-08-11-proposal-review-skill-simplification/review-log.md
- Review resolution: docs/changes/2026-08-11-proposal-review-skill-simplification/review-resolution.md
- Open blockers: specialized proposal-gate activation is not deterministic enough for specification or static fixtures
- Immediate next stage: proposal revision

## Review Inputs

- Tracked proposal: `docs/proposals/2026-08-11-proposal-review-skill-simplification.md` at commit `57e2c85d`.
- User intent: optimize `proposal-review`, preserve concise source-line readability, create a new branch, author a proposal, and perform formal proposal review.
- Standing authority: `CONSTITUTION.md`, `VISION.md`, `AGENTS.md`, `docs/workflows.md`, `specs/skill-contract.md`, and `specs/installed-skill-artifact-placement-contract.md`.
- Current package and architecture context: the complete canonical `skills/proposal-review/` package and `docs/architecture/system/architecture.md`.
- Related evidence: completed review-skill simplification artifacts used only as comparative evidence, not as authority for this package.

## Material Findings

### Finding PRSIM-PR1

Finding ID: PRSIM-PR1
Severity: major
Location: Recommended Direction, Conditional proposal-gates reference
Evidence: The proposal calls `vision_exception_context`, `standing_artifact_context`, and `scope_budget_context` closed predicates but does not define the evidence that makes them true. It is therefore unclear whether the conditional reference loads when a proposal declares an exception, when the reviewer discovers an undeclared conflict, whenever `VISION.md` or `CONSTITUTION.md` is consulted, whenever a standing artifact is missing, or for any proposal with several deliverables. The specification and static scenarios would have to invent these boundaries, and a false negative could omit required gate procedure.
Required outcome: Define each specialized-gate predicate from observable proposal and repository evidence, define whether reviewer-discovered conditions activate it, close overlapping combinations, and specify ambiguity and late-discovery behavior before the proposal is considered ready for specification.
Safe resolution path: Make `vision_exception_context` true when the proposal declares an exception or review evidence identifies a conflict or unsupported exception; make `standing_artifact_context` true only for bootstrap, adoption, governance, or source-of-truth direction whose required standing artifact is absent, being created, or being materially changed; make `scope_budget_context` true when the proposal contains multiple separable workstreams, broad cross-component rollout, or explicit follow-up allocation requiring closed treatment. Load the reference when any predicate is true, permit combined predicates in one invocation, load it late when review evidence first triggers a predicate, and stop on unresolved trigger ambiguity before acceptance.
needs-decision rationale: none; the existing skill contract provides enough evidence to adopt the bounded trigger definitions without expanding scope.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The proposal distinguishes common-path loading and duplicate ownership from review rigor. |
| User value | pass | A shorter advisory review path would make a frequently used decision gate easier to apply. |
| Option diversity | pass | No change, inline-only, one-reference, two-reference, fragmented, and runtime alternatives are materially different. |
| Decision rationale | pass | Two references correspond to durable-recording and specialized-gate boundaries without creating a generic review framework. |
| Scope control | pass | Other skills, runtime infrastructure, target-agent execution, and permanent simplicity validation remain excluded. |
| Vision fit | pass | The direction improves usability while retaining auditable evidence and explicit ownership. |
| Initial-goal preservation | pass | Optimization, branch creation, proposal authoring, and formal review remain visible and in scope. |
| Architecture awareness | pass | The design reuses the existing packaged-skill model and gives this change ownership of any required bounded architecture update. |
| Testability | block | Static fixtures cannot deterministically select the conditional gate reference until the three predicates are defined. |
| Risk honesty | concern | The proposal recognizes hidden universal rules as a risk but does not yet close the trigger false-negative path. |
| Rollout realism | pass | Atomic canonical rollout, parity proof, failure behavior, and rollback are proportionate. |
| Readiness for spec | block | PRSIM-PR1 requires proposal-level closure. |

## Scope Preservation Review

- Scope-preservation result: pass. Every initial user goal remains classified and the selected package stays bounded to `proposal-review` and directly coupled surfaces.
- Scope-budget result: pass with revision. The implementation scope is proportionate, but the runtime meaning of `scope_budget_context` must be distinguished from the proposal's own change scope.
- Vision-fit result: pass. The proposal fits the current vision and does not request an exception.

## Recommended Proposal Edits

- Recommended edits: add a specialized-gate trigger table with observable required evidence, positive and forbidden cases, combined-context behavior, late-discovery loading, and an ambiguity stop. Update the resource assembly and static-scenario sections to use those definitions.
- Retain the two-reference recommendation, the universal-inline ownership list, the separate execution-authority rule, the existing assets, the preservation ledgers, and the deterministic testing boundary.

## Recommendation

- Recommendation: changes requested. Resolve `PRSIM-PR1`, validate the revised proposal and lifecycle metadata, and rerun independent `proposal-review` against a frozen revision.
- No automatic downstream handoff follows this review. The specification is not ready until the predicate model is closed.
