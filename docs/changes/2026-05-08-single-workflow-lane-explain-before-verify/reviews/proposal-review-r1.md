# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Contributor proposal-review
Target: docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md
Status: revise

## Review inputs

- Proposal: `docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md`
- Governance: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`
- Related proposals: `docs/proposals/2026-05-01-workflow-refactor.md`, `docs/proposals/2026-05-08-skill-contract-optimization.md`

## Reconstruction note

This detailed record was reconstructed after proposal edits began. The source review feedback was provided by the user in chat with finding IDs SWF1 through SWF8, severity labels, evidence, required outcomes, and safe resolutions.

## Findings

### SWF1 - Proportional evidence needs a minimum observable contract

Finding ID: SWF1
Severity: major
Evidence: The proposal says RigorLoop will use one standard workflow with proportional evidence and that tiny low-risk changes remain practical without a separate fast lane.
Required outcome: Define the minimum evidence for a tiny low-risk change under the standard workflow.
Safe resolution: Add a `Proportional evidence` section with the minimum evidence floor and state that proportional evidence is not a separate lane.

### SWF2 - Explain-change must not claim final verification before verify

Finding ID: SWF2
Severity: major
Evidence: The proposal moves `explain-change` before `verify`, while keeping validation execution and branch-ready proof under `verify`.
Required outcome: Add a clear claim boundary between `explain-change` and `verify`.
Safe resolution: Add an `Explain-change before verify` section that says pre-verify explanation may summarize available evidence and gaps but must not claim final verify, branch-ready, PR-ready, or CI-final status.

### SWF3 - Public skill portability needs an exact allow/block policy

Finding ID: SWF3
Severity: major
Evidence: The proposal says shipped skills should not contain RigorLoop-repository-specific paths, local examples, selector commands, generated mirror details, or adapter build internals.
Required outcome: Define an allowlist and blocklist for public skill text.
Safe resolution: Add a `Public skill surface boundary` section listing portable project surfaces, blocked RigorLoop repository-internal surfaces, and allowed internal maintenance locations.

### SWF4 - docs/workflows.md generation responsibility needs a required output shape

Finding ID: SWF4
Severity: major
Evidence: The proposal says the `workflow` skill should create or refresh `docs/workflows.md` by instruction and should not author the canonical workflow spec by default.
Required outcome: Add a required guide structure.
Safe resolution: Add a `Workflow guide responsibility` section naming required guide content and stating that `docs/workflows.md` is a readable guide, not a competing workflow spec.

### SWF5 - Static validation must cover the exact retired and required wording

Finding ID: SWF5
Severity: major
Evidence: The proposal calls for validation coverage that prevents old ordering, fast-lane resurfacing, and public-skill leakage.
Required outcome: Add exact validation targets.
Safe resolution: Add phrase-based static validation expectations for retired terms, old ordering, public skill internal-path leakage, and required replacement phrases.

### SWF6 - Active-plan transition rule needs a durable surface

Finding ID: SWF6
Severity: concern
Evidence: The proposal says active plans use the current standard workflow at the next handoff and affected plans should add a short workflow transition note only when the transition affects them.
Required outcome: Define the transition-note surface.
Safe resolution: Record the transition note in the active plan's current handoff, readiness, or progress section with the current order, preliminary prior verification status, and final verify dependency on current explain-change.

### SWF7 - ci-maintenance placement should clarify trigger timing

Finding ID: SWF7
Severity: concern
Evidence: The proposal says `ci-maintenance` runs before `explain-change` when triggered so the explanation covers the final changed surfaces.
Required outcome: Restate the boundary so `ci-maintenance` does not become a general validation-running stage.
Safe resolution: Clarify that `ci-maintenance` is triggered only for hosted workflow automation, validation automation, or related platform configuration changes, while validation execution and branch-ready proof remain under `verify`.

### SWF8 - Public-skill check must distinguish canonical public skills from internal docs

Finding ID: SWF8
Severity: concern
Evidence: The proposal says public skill wording should avoid maintainer-only details, but those details may remain in repository governance, contributor docs, specs, tests, plans, maintainer surfaces, or non-published internal skills.
Required outcome: Define which surfaces the public-skill portability check applies to.
Safe resolution: Scope portability checks to canonical skill files shipped to users, generated public skill copies, and public adapter skill copies; exclude internal specs, plans, tests, generator scripts, maintainer docs, and repository-only contributor docs.

## Checklist coverage

| Dimension | Result | Notes |
|---|---|---|
| Problem framing | pass | The proposal ties the lane model, final-stage order, and public-skill boundary to real workflow defects. |
| Direction quality | pass | The recommended direction uses one workflow, proportional evidence, and `explain-change -> verify -> pr`. |
| Evidence contract | revise | SWF1 requires a minimum proportional evidence floor. |
| Stage ownership | revise | SWF2 and SWF7 require clearer ownership boundaries. |
| Public surface boundary | revise | SWF3 and SWF8 require exact allow/block scope. |
| Guide responsibility | revise | SWF4 requires the `docs/workflows.md` guide shape. |
| Validation specificity | revise | SWF5 requires phrase-based static validation targets. |
| Transition handling | concern | SWF6 requires a durable active-plan note surface. |

## Recommended next stage

Revise the proposal to resolve SWF1 through SWF8, then rerun proposal-review before downstream spec authoring relies on the proposal.
