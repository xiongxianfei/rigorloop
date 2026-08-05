# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Codex proposal-review skill
Target: docs/proposals/2026-07-29-progressive-boundary-first-skill-guidance.md
Status: changes-requested
Original review source: User-invoked `$proposal-review` on 2026-07-29.
Material findings: PBS-PR1
Scope-preservation result: pass
Immediate next stage: proposal revision
Automatic downstream handoff: none

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: `PBS-PR1`
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/review-log.md
- Review resolution: docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/review-resolution.md#proposal-review-r1
- Open blockers: `PBS-PR1`
- Immediate next stage: proposal revision

## Material Findings

## Finding PBS-PR1

Finding ID: PBS-PR1
Severity: major
Location: `Next Artifacts`, especially steps 1-3; `AC-PBS-013` through `AC-PBS-017`
Evidence: The proposal correctly treats the embedded-status correction as an implementation of the approved stage-owned lifecycle contract, but step 2 removes published skill paths from artifact-lifecycle selection before step 3 amends and reviews the skill, validation, and workflow contracts. Selector behavior is a contributor-visible workflow and validation contract. `CONSTITUTION.md` requires an approved spec before externally observable behavior changes, while the proposal delays `spec-review` until step 4 and limits its explicit implementation gate to boundary-guidance changes in step 9.
Required outcome: Separate the already-specified embedded-status bug fix from the new selector-policy change, and place every new selector or published-skill validation behavior behind approved contract and test-spec gates.
Safe resolution path: Let the stage-owned validator bug fix proceed only under the existing `SLA-R013`, `SLA-R014`, and `SLA-R070` contract; amend the relevant validation, skill, boundary, and workflow specs plus matching test specs; complete `spec-review`; then plan and implement skill-path selector removal together with the boundary-guidance changes. Make the final implementation gate apply to every new behavior in `AC-PBS-013` through `AC-PBS-017`.
needs-decision rationale: none; the proposal needs a sequencing correction, not a new product-direction choice.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The prompt-dependence, repeated-model cost, scenario over-generation, and validator-ownership problems are explicit. |
| User value | pass | Users can describe behavior normally while receiving concise boundary coverage and less irrelevant validation ceremony. |
| Option diversity | pass | The proposal compares do nothing, trigger-only, progressive references, independent models, derived packets, a runtime service, and checker deletion. |
| Decision rationale | pass | The compact-core and stage-owned consumption model follows portability, traceability, and context-cost criteria. |
| Scope control | concern | The scope budget separates the validator defect, but the downstream sequence does not preserve that boundary at the spec gate. |
| Architecture awareness | pass | Canonical ownership, projection, packaging, selector routing, compatibility, and rollback boundaries are visible. |
| Testability | pass | Acceptance criteria and fixtures cover prompt independence, over-generation, parity, selector retention, mixed changes, exact ownership, and fail-closed behavior. |
| Risk honesty | pass | Drift, omitted context, surprise activation, compatibility, false validation ownership, and ambiguous owner lookup are addressed. |
| Rollout realism | concern | Atomic boundary activation is credible, but selector removal is ordered before its contract review. |
| Readiness for spec | block | `PBS-PR1` must reorder and broaden the contract-first gate before downstream work can rely on the sequence. |

## Scope Preservation Review

- Scope-preservation result: pass.

Every initial user goal is classified with an allowed treatment.
The proposal preserves automatic boundary awareness, key-boundary coverage, scenario restraint, one shared model, stage-specific consumption, and removal of irrelevant lifecycle checking from published skill paths.
Deleting useful governed-artifact lifecycle validation is explicitly rejected with rationale.

## Recommended Proposal Edits

- Split `Next Artifacts` into the existing-contract validator bug fix and the new contract amendments.
- Move skill-path selector removal after the relevant spec and test-spec amendments have passed `spec-review`.
- Apply the implementation gate to validator-selector behavior as well as boundary-guidance behavior.
- State that the proposal remains isolated and not ready for specification until the reordered sequence passes proposal-review R2.

## Recommendation

- Recommendation: `changes-requested`. The strategic direction, vision fit, option quality, scope preservation, architecture awareness, and proof strategy are sound. Reorder the validator and selector work so only the already-approved stage-owned bug fix can precede new contract review, then run proposal-review R2. This direct review is isolated, edits no proposal content, and performs no automatic downstream handoff.
