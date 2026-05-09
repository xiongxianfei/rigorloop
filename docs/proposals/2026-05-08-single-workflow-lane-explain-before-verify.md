# Single Workflow Lane, Explain-Change Before Verify, and Public Skill Surface Boundary

## Status

- accepted

## Problem

RigorLoop's public workflow guidance exposes three related problems.

First, the fast-lane and full-lifecycle split makes routing more complex than the current workflow needs. The repository already has one category-based workflow model with conditional stages, but contributor-facing surfaces still describe a separate fast lane with separate evidence rules.

Second, final `verify` can block on a missing or stale `docs/changes/<change-id>/explain-change.md` artifact even though the documented per-change sequence places `explain-change` after `verify`. That creates a circular dependency: verification expects the durable explanation to exist before the stage that creates it has run.

Third, shipped skill text is a public interface for other projects, but some public skill wording still names RigorLoop repository internals such as local spec paths, generated mirrors, adapter directories, selector commands, validator names, and maintainer-only generation mechanics. That makes the skills less portable for projects that adopt the workflow without having this repository's internal layout.

## Goals

- Present RigorLoop as one recommended standard workflow with conditional, on-demand, and periodic stages.
- Remove fast lane and all replacement size or risk lanes from public workflow guidance.
- Define manual individual skill invocation as isolated by default and not equivalent to full workflow completion.
- Move `explain-change` before final `verify`, so `verify` validates the final change-local pack rather than blocking on a downstream artifact.
- Keep `ci-maintenance` before `explain-change` when CI infrastructure changes are triggered, so the explanation covers the final diff.
- Make shipped skills project-portable by blocking RigorLoop-repository-specific paths, local examples, selector commands, generated mirror details, and adapter build internals from published skill text.
- Clarify that the `workflow` skill routes work and creates or refreshes `docs/workflows.md` by instruction; it does not author the canonical workflow spec by default and this change does not add a workflow-guide generator script.
- Add validation coverage that prevents old ordering, fast-lane resurfacing, and public-skill leakage of maintainer-only repository mechanics.

## Non-goals

- Do not weaken requirements for behavior, workflow, schema, generated-output, compatibility, security-sensitive, release, or public contributor expectation changes.
- Do not classify public workflow routes by tiny, low-risk, high-risk, fast-lane, full-lane, small-change, or mini-spec labels.
- Do not remove `spec`, `code-review`, `verify`, `explain-change`, or `pr` as workflow stages.
- Do not move authoritative workflow policy out of approved specs into `docs/workflows.md` or skill prose.
- Do not redesign the full skill contract beyond the public-surface boundary needed for this change.
- Do not change adapter package formats except as generated output from canonical skill edits.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.
- Do not make `learn` a default per-change stage.

## Vision fit

fits the current vision

This proposal supports RigorLoop's commitment to traceable, reviewable AI-assisted delivery. A single workflow with clearer stage order makes the loop easier to inspect, while project-portable skill wording helps other repositories adopt the workflow without inheriting RigorLoop's maintainer-only implementation details.

## Context

`CONSTITUTION.md` says RigorLoop optimizes for reviewability, traceability, trustworthy automation, and design-implementation consistency. It also says workflow stage order and public contributor expectations are compatibility-sensitive changes, and that workflow or governance changes update affected operating and governance guidance.

The accepted workflow refactor proposal, `docs/proposals/2026-05-01-workflow-refactor.md`, introduced category-based workflow guidance and kept `specs/rigorloop-workflow.md` as the canonical workflow definition. That proposal still preserved a fast-lane and full-lifecycle model and documented the per-change sequence as `verify -> ci-maintenance when triggered -> explain-change -> pr`.

The accepted skill contract optimization proposal, `docs/proposals/2026-05-08-skill-contract-optimization.md`, established that skills should be smaller, locally owned, and claim-safe. It also reinforced that shipped skill text is user-facing and should not expose maintainer-only details.

Current surfaces still show the old model. `docs/workflows.md`, `AGENTS.md`, `README.md`, `skills/workflow/SKILL.md`, `skills/verify/SKILL.md`, `skills/explain-change/SKILL.md`, `specs/rigorloop-workflow.md`, and `specs/workflow-stage-autoprogression.md` all contain workflow-order, lane, or handoff wording affected by this proposal. `docs/project-map.md` is absent, so this proposal does not rely on project-map claims.

## Options considered

### Option 1: Keep the current fast-lane and full-lifecycle model

This avoids immediate workflow churn and preserves existing trivial-change guidance. It also keeps the current contradiction between `verify` and `explain-change`, leaves routing complexity in public guidance, and continues to expose maintainers' internal repository mechanics in shipped skills.

### Option 2: Only move `explain-change` before `verify`

This fixes the circular dependency with the smallest conceptual change. It does not address the separate lane model, and it leaves public skill portability as a separate source of confusion.

### Option 3: Remove fast lane as a named lane but keep current `verify -> explain-change` order

This simplifies routing while preserving the existing late-stage order. It leaves `verify` responsible for validating an artifact that may not exist yet, so the most concrete workflow bug remains.

### Option 4: Split the work into three independent proposals

Separate proposals for fast-lane removal, stage-order repair, and public-skill boundary would lower the scope of each review. It would also force three tightly coupled changes to coordinate across the same specs, docs, skills, generated outputs, and validation tests.

### Option 5: One focused workflow-optimization proposal

This handles the three related issues together because they affect the same public workflow surfaces. The risk is a broader first implementation, but the scope stays documentation, spec, skill, generated-output, and static-validation alignment rather than runtime behavior.

## Recommended direction

Choose Option 5.

Adopt one recommended standard RigorLoop workflow:

```text
proposal, when direction is not already settled
-> proposal-review, when triggered
-> spec, when behavior or workflow contract changes
-> spec-review, when triggered
-> architecture, when triggered
-> architecture-review, when triggered
-> plan, when needed
-> plan-review, when triggered
-> test-spec, when proof design is needed
-> implement
-> code-review
-> review-resolution, when triggered
-> ci-maintenance, when triggered
-> explain-change
-> verify
-> pr
```

For milestone-based plans, keep the implementation review loop scoped to each in-scope implementation milestone:

```text
implement M<n>
-> code-review M<n>
-> review-resolution M<n>, when triggered
-> close M<n>
-> implement next milestone
```

After all in-scope implementation milestones are closed and required review-resolution is closed, the final closeout sequence becomes:

```text
ci-maintenance, when triggered
-> explain-change
-> verify
-> pr
```

This keeps validation execution owned by `verify`, but moves CI infrastructure maintenance before explanation when that maintenance changes the final diff. It also lets `explain-change` own the durable rationale while `verify` owns branch-ready proof that the final artifact pack, including durable change reasoning, is complete and current.

### Manual skill invocation

RigorLoop should use one recommended standard workflow for complete AI-assisted delivery.

Users may manually invoke an individual skill, such as `implement`, `code-review`, `verify`, `explain-change`, or `pr`, for a focused task. That invocation is isolated by default.

Manual skill output may be useful, but it does not imply that upstream or downstream workflow stages have been completed. Workflow completion claims require evidence from the relevant standard workflow stages.

### Explain-change before verify

`explain-change` should create or update durable rationale before final `verify`.

Before final `verify`, `explain-change` may summarize:

- implementation scope;
- review outcomes;
- validation commands already run;
- known validation gaps;
- expected final verification checks.

It should not claim final `verify`, `branch-ready`, PR-ready, or CI-final status. `verify` should validate that `explain-change.md` exists, is current, and matches the final changed surfaces.

The stage ownership split should remain:

| Stage | Owns |
| --- | --- |
| `explain-change` | Durable rationale and diff explanation. |
| `verify` | Final validation evidence and `branch-ready` proof. |
| `pr` | PR body and PR-opening readiness. |

### CI-maintenance boundary

`ci-maintenance` should be triggered only when hosted workflow automation, validation automation, or related platform configuration must be created or changed.

It is not the stage that runs validation. Validation execution and branch-ready proof remain owned by `verify`.

### Public skill surface boundary

Public skill wording should use project-portable terms such as "project workflow guide", "local workflow contract", "project validation command", "generated skill output", and "adapter output if this project uses adapters". Published skills should not include local RigorLoop repository examples. RigorLoop-specific internals such as `specs/rigorloop-workflow.md`, `specs/skill-contract.md`, `.codex/skills/`, `dist/adapters/`, `scripts/select-validation.py`, `scripts/build-adapters.py`, `templates/shared/`, selector path constraints, drift-check mechanics, and shared-block implementation details should appear only in RigorLoop repository governance, contributor docs, specs, tests, plans, maintainer surfaces, or non-published internal skills.

Published skill text may reference portable project surfaces such as:

- `AGENTS.md`;
- `docs/workflows.md`;
- `VISION.md`;
- `docs/changes/<change-id>/`;
- `docs/plans/<plan>.md`;
- local workflow contract, if the adopting project has one;
- project validation command, when supplied by the adopting project.

Published skill text should not reference RigorLoop repository-internal surfaces such as:

- `specs/rigorloop-workflow.md`;
- `specs/skill-contract.md`;
- `.codex/skills/`;
- `dist/adapters/`;
- `scripts/select-validation.py`;
- `scripts/build-adapters.py`;
- `templates/shared/`;
- RigorLoop-local examples;
- selector path constraints;
- drift-check mechanics;
- shared-block implementation mechanics.

Internal details may remain in RigorLoop repository specs, tests, plans, maintainer docs, generator code, and repository-only contributor docs.

Public skill portability checks should apply to canonical skill files that are shipped to users, generated public skill copies, and public adapter skill copies. They should not apply to internal specs, plans, tests, generator scripts, maintainer docs, or repository-only contributor docs.

### Workflow guide responsibility

The `workflow` skill should route work, audit current workflow state, create or refresh `docs/workflows.md` when requested or when adopting RigorLoop into a repository, and recommend the next valid skill or stop condition. It should not invent new workflow policy, author the canonical workflow spec by default, edit every stage skill as part of ordinary routing, or claim review, verification, or PR readiness without owning evidence. No separate `docs/workflows.md` generator script should be introduced in this change.

When the `workflow` skill creates or refreshes `docs/workflows.md`, the guide should include:

- source-of-truth note;
- one standard workflow;
- manual skill invocation and isolation behavior;
- stage obligation meanings;
- ordered workflow sequence;
- milestone-based implementation and review loop;
- `review-resolution` trigger;
- `ci-maintenance` boundary;
- `explain-change -> verify -> pr` final order;
- verify and PR ownership;
- learn trigger summary;
- skill index.

`docs/workflows.md` is a readable guide. It is not a competing workflow spec.

### Active plan transition note

Active plans should use the current standard workflow at the next handoff. If the transition affects a plan, record the transition note in the active plan's current handoff, readiness, or progress section.

The note should say:

- current final order is `explain-change -> verify -> pr`;
- prior verification evidence before `explain-change` is preliminary;
- final `verify` runs after `explain-change.md` exists and is current.

## Expected behavior changes

- Contributors see one recommended standard workflow instead of choosing between named fast-lane, full-lifecycle, small-change, low-risk, or high-risk lanes.
- Users may invoke individual skills manually, but manual skill output remains isolated and does not claim workflow completion.
- `explain-change` creates or updates the durable rationale before final `verify`.
- `verify` treats a missing or stale required `explain-change.md` as a blocker and routes back to `explain-change` rather than trying to create the explanation itself.
- `ci-maintenance` runs before `explain-change` when triggered, so the explanation describes the final changed surfaces.
- `verify` remains the owner of `branch-ready`; `pr` remains the owner of `pr-body-ready` and `pr-open-ready`.
- Published portability checks block RigorLoop-repository-specific paths, local examples, selector commands, generated mirror details, and adapter build internals in shipped skill text.
- `docs/workflows.md` becomes the readable project workflow guide and summary, not a competing workflow spec.
- Active plans that are affected by the transition use the new order from the next handoff and record only a short current-state transition note.

## Architecture impact

This is a workflow-governance and distribution-surface change, not a product runtime architecture change.

Expected touched surfaces include:

- `CONSTITUTION.md` for removing fast-lane governance and updating final-stage ordering.
- `AGENTS.md`, `README.md`, and `docs/workflows.md` for contributor-facing workflow summaries.
- `specs/rigorloop-workflow.md` and `specs/rigorloop-workflow.test.md` for canonical stage order, stage obligations, examples, and acceptance criteria.
- `specs/workflow-stage-autoprogression.md` and `specs/workflow-stage-autoprogression.test.md` for downstream continuation after review-resolution, ci-maintenance, explain-change, verify, and pr.
- `skills/workflow/SKILL.md`, `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, `skills/explain-change/SKILL.md`, `skills/verify/SKILL.md`, `skills/pr/SKILL.md`, and any review-resolution guidance embedded in existing skills.
- Generated local Codex skill output and public adapter packages after canonical skill changes.
- Static validators and tests that scan workflow order, public skill wording, generated-output drift, and adapter distribution consistency.
- Active execution plans only when their current handoff is affected by the transition to `explain-change -> verify -> pr`.

## Testing and verification strategy

Update the workflow spec tests to cover the single standard workflow sequence, manual skill invocation isolation, milestone-aware implementation loops, ci-maintenance placement, `explain-change -> verify -> pr`, and the absence of named lane classifications.

Update autoprogression tests so workflow-managed completion no longer routes `verify -> explain-change`; the final route should be `ci-maintenance when triggered -> explain-change -> verify -> pr`, with direct `verify` still isolated unless workflow-managed context or explicit continuation exists.

Add or update static checks that fail when public skills contain old fast-lane routing, old `verify -> explain-change` ordering, local RigorLoop examples, or RigorLoop repository-internal paths and commands that should stay in maintainer surfaces.

Static checks should fail when public workflow or skill surfaces contain:

- `fast lane`;
- `fast-lane`;
- `mini-spec`;
- `full-feature lane`;
- `full lane`;
- `small-change lane`;
- `tiny low-risk`;
- `high-risk lane`;
- `proportional evidence`;
- unconditional `verify -> explain-change`;
- unconditional `code-review -> verify` for milestone-based work;
- public skill references to RigorLoop-internal paths or commands.

Static checks should also prove that public workflow or skill surfaces contain:

- `standard workflow`;
- manual skill invocation isolation;
- `explain-change -> verify -> pr`;
- `ci-maintenance -> explain-change -> verify -> pr` when CI maintenance is triggered;
- `docs/workflows.md` as the workflow guide created or refreshed by the `workflow` skill.

These checks should stay narrow and phrase-based. They should not become semantic prose scoring.

Run existing skill, adapter, lifecycle, and workflow validation through repository-owned scripts. The implementation plan should name the smallest targeted checks first, then the generated-output and broad smoke checks required by the touched surfaces.

## Rollout and rollback

Rollout should update authoritative workflow specs first, then contributor summaries, canonical skills, generated outputs, and validation coverage. The implementation should keep affected surfaces aligned in one PR because workflow-governance changes are compatibility-sensitive.

In-flight work should use the new order from the next handoff. If an active plan has not yet reached final verification, it should use `explain-change -> verify -> pr`. If it already ran verification before `explain-change`, treat that evidence as preliminary and rerun final `verify` after the durable explain-change artifact exists and is current. Add a short workflow transition note only when the transition affects the plan.

Rollback is straightforward but broad: restore the prior fast-lane wording and `verify -> ci-maintenance -> explain-change -> pr` ordering across the same authoritative surfaces, regenerate outputs, and revert the static checks that enforce the new public-surface boundary.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Removing the named fast lane makes focused work feel too heavy. | Document manual individual skill invocation as isolated output, not workflow completion. |
| Public skill portability rules accidentally remove useful RigorLoop contributor guidance. | Keep maintainer-only details in `CONSTITUTION.md`, specs, plans, tests, contributor docs, and repository-specific validation docs; remove them only from shipped public skill wording. |
| Stage-order changes drift across specs, docs, skills, README, generated outputs, and tests. | Add static checks for old ordering and run generated-output drift checks after canonical skill edits. |
| `verify` loses visibility into validation evidence by moving after `explain-change`. | Keep validation command execution and branch-ready proof under `verify`; `explain-change` records available evidence and validation gaps, and `verify` validates the final record. |
| Existing autoprogression rules assume a named full-feature lane. | Update autoprogression terminology to route the single standard workflow with conditional stages while preserving isolated direct-stage behavior. |
| The first implementation becomes too broad. | Keep the first slice to workflow contract, docs, skill text, generated output, and static tests; defer generator work and deeper validator redesign unless needed to enforce the new invariants. |

## Open questions

None currently blocking proposal review.

The previously open policy choices are settled for this proposal: use one recommended standard workflow; treat manual individual skill invocation as isolated by default; block RigorLoop-repository-specific paths and local examples in published skills; have the `workflow` skill create or refresh `docs/workflows.md` by instruction without adding a generator script; and update affected active plans with a short workflow transition note from the next handoff.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-08 | Draft a focused workflow-optimization proposal covering the lane model, final-stage order, and public skill surface boundary. | The three issues affect the same workflow specs, docs, skills, generated outputs, and validation checks. | Separate proposals for each issue; only moving `explain-change`; keeping the existing lane model. |
| 2026-05-08 | Recommend one standard workflow with conditional, on-demand, and periodic stages. | This removes named-lane routing complexity and keeps complete workflow claims evidence-based. | Keep fast-lane/full-lifecycle as separate public lanes. |
| 2026-05-08 | Recommend `ci-maintenance -> explain-change -> verify -> pr` for final closeout. | The explanation should describe the final diff, and verification should validate the final artifact pack. | Keep `verify -> ci-maintenance -> explain-change -> pr`; move only `explain-change` before `pr`. |
| 2026-05-08 | Recommend public-skill wording that avoids maintainer-only RigorLoop repository mechanics. | Shipped skills are a user-facing interface and should work in projects without this repository's internal layout. | Leave existing internal path and script references in shipped skills. |
| 2026-05-08 | Resolve proposal policy questions: use one recommended standard workflow; treat manual skill invocation as isolated; block RigorLoop-specific paths and local examples from published skills; have `workflow` refresh `docs/workflows.md` without a generator script; update affected active plans with a short transition note from the next handoff. | These decisions keep one workflow, preserve portability, avoid premature automation, and keep active-plan migration concise. | Introduce a small-change lane; allow local examples in public skills; add a workflow-guide generator now; require active plans to explain the old order in detail. |
| 2026-05-08 | Incorporate changes-requested review feedback before spec handoff. | The proposal needed sharper acceptance criteria for evidence boundaries, explain/verify claim boundaries, public skill allow and block policy, workflow guide shape, static checks, active-plan transition surfaces, and `ci-maintenance` trigger scope. | Move to spec with broad direction only. |
| 2026-05-08 | Resolve spec-review SR1 by removing the alternate evidence-path contract term. | Manual skill invocation isolation gives users flexibility without creating a second evidence path or ambiguous size-based floor. | Patch the alternate evidence-path wording while keeping size and risk categories. |

## Next artifacts

- `proposal-review` for this proposal.
- Updated workflow spec covering the standard workflow, manual skill invocation isolation, final-stage order, public-skill boundary, workflow-guide responsibility, and active-plan transition note.
- Updated workflow test spec covering old-order rejection, lane removal, manual skill isolation, and public-skill leakage checks.
- Architecture or ADR only if review determines that workflow guide generation or public-skill validation introduces a new durable boundary.
- Execution plan for coordinated updates across specs, docs, skills, generated outputs, and validation.
- Test spec or test-plan updates for static validators and generated-output checks.

## Follow-on artifacts

- `proposal-review`: approved in `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/proposal-review-r2.md`.
- `spec`: draft amendments in `specs/rigorloop-workflow.md`, `specs/workflow-stage-autoprogression.md`, and `specs/skill-contract.md`.

## Readiness

Accepted after `proposal-review`.

Ready for feature spec review after the downstream spec amendments are drafted.
