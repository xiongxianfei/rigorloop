# Review Resolution: Assets-First Progressive Disclosure Pilot for Published Skills

## Scope

This record tracks material finding closeout for formal reviews of the assets-first progressive disclosure pilot for published skills.

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: plan-review-r1
Review closeout: plan-review-r2
Review closeout: code-review-m1-r1

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `spec-review-r1`, `plan-review-r1`, `plan-review-r2`, `code-review-m1-r1`
- Findings resolved: 6
- Unresolved findings: 0
- Final result: `APD-PR1`, `APD-PR2`, `APD-PR3`, and `APD-PR4` are accepted and resolved for proposal-revision purposes. `APD-PLR1` is accepted and resolved for plan-revision purposes. `APD-CR1` is accepted and resolved for M1 review-resolution purposes.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| APD-PR1 | accepted | resolved | Added the spec-slice dependency and renamed the implementation slice to the asset pilot implementation slice. |
| APD-PR2 | accepted | resolved | Added the handoff asset boundary and acceptance criteria preserving handoff consistency rules in `SKILL.md`. |
| APD-PR3 | accepted | resolved | Added the output skeleton boundary for `assets/plan-skeleton.md` as a reviewed equivalent template with compact `SKILL.md` summary. |
| APD-PR4 | accepted | resolved | Added deterministic static validation boundaries and routed qualitative checks to bounded heuristics, fixtures, or code review. |
| APD-PLR1 | accepted | resolved | Revised the plan so test-spec authoring stays in the `test-spec` stage and M1 implements the approved test-spec amendment. |
| APD-CR1 | accepted | resolved | Added direct plan-asset fixture proof for a missing resource-map entry. |

## Common Resolution Metadata

- Owner: proposal author
- Owning stage: proposal
- Validation target: targeted readback of the revised proposal and review closeout artifacts.
- Validation evidence: Targeted readback confirmed the revised proposal records the accepted boundaries. Artifact lifecycle, review artifact, change metadata, and whitespace validation were run after recording.

## Finding Details

### proposal-review-r1

Finding closeout for `proposal-review-r1`.

### proposal-review-r2

No material findings. Clean formal review approved the revised proposal for proposal-stage purposes. Immediate next stage is proposal status normalization to `accepted`, then spec amendment. No disposition entries required.

### spec-review-r1

No material findings. Clean formal review approved the draft `specs/skill-contract.md` amendment for spec-stage purposes. Immediate next stage is `plan`. Eventual test-spec readiness is `ready`. No disposition entries required.

### plan-review-r1

Finding closeout for `plan-review-r1` is closed for plan-revision purposes. Immediate next stage remains follow-up plan-review.

### plan-review-r2

No material findings. Clean formal review approved the revised plan for plan-stage purposes. Immediate next stage is `test-spec`. No disposition entries required.

### code-review-m1-r1

Finding closeout for `code-review-m1-r1` is closed for M1 review-resolution purposes. Immediate next stage is M1 code-review rerun.

### APD-PR1 - Proposal needs explicit dependency on existing skill-contract slice

Finding ID: APD-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Add `Spec-slice dependency`, state this is a follow-on asset pilot unless `specs/skill-contract.md` is explicitly amended and approved, and rename first-slice wording to `asset pilot implementation slice`.
Rationale: The proposal must not accidentally overlap or reopen existing published-skill design first-slice work.
Validation target: Confirm the proposal records the spec-slice dependency and uses asset-pilot terminology for the implementation slice.
Validation evidence: Targeted readback confirmed `Spec-slice dependency` and `Asset pilot implementation slice` are present in the revised proposal.

### APD-PR2 - Handoff summary asset is lifecycle-sensitive

Finding ID: APD-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Add `Handoff asset boundary`, forbid lifecycle status values, transition rules, claim ownership, readiness semantics, and validation requirements in `assets/current-handoff-summary.md`, and add acceptance criteria for the boundary.
Rationale: Current handoff state is lifecycle-sensitive and must not become hidden workflow rule text inside an asset template.
Validation target: Confirm the proposal keeps handoff semantics and consistency rules in `SKILL.md` or governing workflow/spec artifacts.
Validation evidence: Targeted readback confirmed the revised proposal states `current-handoff-summary.md` may contain only section headings, field labels, and placeholders, and that `SKILL.md` retains handoff consistency responsibility.

### APD-PR3 - Output skeleton source boundary is unclear

Finding ID: APD-PR3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Add `Output skeleton boundary`, allowing `assets/plan-skeleton.md` to serve as the reviewed equivalent full output template only when `SKILL.md` keeps a compact output expectation summary and Resource map entry.
Rationale: The proposal needs one clear full-plan template source while preserving visible output expectations in `SKILL.md`.
Validation target: Confirm the proposal forbids duplicating the full section layout in both `SKILL.md` and the asset.
Validation evidence: Targeted readback confirmed the output skeleton boundary states the full section layout must not be duplicated in both places.

### APD-PR4 - Asset validation checks need deterministic oracle boundaries

Finding ID: APD-PR4
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Add `Asset validation oracle boundary`, list allowed static checks, reject broad semantic scoring for asset prose, and require behavior parity to be fixture-based or review-recorded.
Rationale: Asset validation must be implementable and reviewable without unbounded semantic scoring.
Validation target: Confirm the proposal separates deterministic static checks from bounded heuristics, fixture evidence, and code-review judgment.
Validation evidence: Targeted readback confirmed the revised testing strategy includes deterministic static checks and limits qualitative checks to bounded heuristics, fixtures, or code review.

### APD-PLR1 - Test-spec authoring is mixed into implementation milestone

Finding ID: APD-PLR1
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Revise the plan to keep `test-spec` authoring after plan-review and before implementation, remove `specs/skill-contract.test.md` from M1 implementation-owned file scope, and make M1 implement tests and fixtures from the approved test-spec amendment.
Rationale: The lifecycle order is `plan -> plan-review -> test-spec -> implement`; authoring the test spec inside M1 would blur the stage boundary and weaken test-driven sequencing.
Validation target: Confirm the revised plan separates the test-spec stage from M1 implementation and keeps the immediate next stage as `test-spec` after a clean plan-review.
Validation evidence: Plan revision added `Pre-implementation prerequisites`, removed `specs/skill-contract.test.md` from M1 implementation-owned files, replaced test-spec authoring with implementation of approved test-spec-defined tests, and kept current handoff at follow-up plan-review before `test-spec`.

### APD-CR1 - Missing direct fixture proof for plan asset resource-map omissions

Finding ID: APD-CR1
Disposition: accepted
Status: resolved
Owner: implementation
Owning stage: review-resolution
Chosen action: Added `tests/fixtures/skills/published-design/plan-assets-missing-resource-map-entry/` with the approved four `plan` assets while omitting `assets/decision-log-row.md` from `SKILL.md`'s `Resource map`, and added `test_published_design_plan_asset_resource_map_requires_every_asset`.
Rationale: T34 and the M1 plan require direct fixture proof for missing resource-map entries in the assets-first plan pilot, and the reviewed implementation does not add that plan-asset-specific omission fixture.
Validation target: Add direct plan-asset missing resource-map-entry fixture/test coverage and rerun the M1 validation commands.
Validation evidence: `python scripts/test-skill-validator.py` passed with 128 tests, including the new plan-asset missing resource-map-entry test. `python scripts/validate-skills.py` passed after the fixture addition.
