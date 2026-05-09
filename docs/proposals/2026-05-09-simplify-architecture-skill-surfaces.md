# Simplify Architecture Skill Surfaces

## Status

- accepted

## Problem

The current architecture and architecture-review guidance makes change-local architecture deltas a normal architecture surface. That adds an unnecessary intermediate artifact for many changes and blurs responsibility between proposal, spec, architecture, and ADR work.

The confusing part is not the canonical architecture package itself. The confusing part is using architecture artifacts to explore unsettled direction. When design direction or behavior is still uncertain, architecture can become a temporary option-selection document instead of a record of accepted system shape.

## Goals

- Make the architecture skill choose the smallest valid architecture action.
- Keep unresolved product or design direction in proposals and proposal review.
- Keep unresolved behavior contracts in specs and spec review.
- Make architecture record accepted design in the canonical architecture package.
- Make ADRs record durable architecture decisions.
- Let architecture-review review canonical architecture updates, ADRs, no-impact rationale, or readiness gaps without requiring a change-local architecture delta.
- Preserve portability for published skills by describing project-configured canonical architecture paths instead of hardcoding RigorLoop-only paths as universal requirements.

## Non-goals

- Removing the canonical architecture package.
- Removing C4, arc42, or ADRs from RigorLoop's architecture method.
- Requiring ADRs for every small architecture edit.
- Using architecture-review to settle product direction.
- Replacing proposal-review, spec-review, plan, or implementation sequencing.
- Normalizing all legacy architecture artifacts as part of this proposal.
- Implementing the skill and spec edits in this proposal artifact.

## Vision fit

fits the current vision

The change supports RigorLoop's commitment to reviewable, traceable artifacts by sharpening which artifact owns each kind of truth. It reduces ceremony where architecture impact is absent or already clear, while keeping accepted design and durable decisions visible in tracked files.

## Context

`CONSTITUTION.md` requires architecture-affecting changes to update the relevant architecture document or ADR in the same change. It also says change-local artifacts should stay concise and link back to approved top-level artifacts instead of becoming a second long-form source of truth.

`specs/architecture-package-method.md` currently defines change-local architecture deltas as temporary working artifacts under `docs/changes/<change-id>/architecture.md`. The same spec requires merge-back into the canonical architecture package before an architecture-significant change is complete.

`skills/architecture/SKILL.md` follows that model by listing change-local deltas as a normal output shape when working design reasoning is needed. `skills/architecture-review/SKILL.md` also reviews change-local deltas and merge-back as part of the approved package model.

The proposed simplification keeps the useful invariant from the current method: current architecture truth belongs in the canonical architecture package, and durable decisions belong in ADRs. It removes the routine expectation that architecture creates or reviews a temporary delta to resolve uncertainty.

## Options considered

### Option 0: Keep the current architecture delta model

This preserves the existing approved spec and skill behavior. It avoids immediate artifact churn.

The downside is that the architecture stage can keep attracting unsettled option selection. Contributors still need to decide when a temporary delta is helpful, when it must be merged back, and whether review should focus on the delta or the canonical package.

### Option 1: Keep change-local deltas but make them rare

This would retain the current output surface but warn that deltas should be exceptional.

The downside is that the normal review model would still need to understand change-local architecture deltas, merge-back, and temporary truth. That keeps the highest-friction concept in the workflow even if it is discouraged.

### Option 2: Route uncertainty away from architecture and update canonical surfaces directly

This model makes proposal resolve direction, spec resolve behavior, architecture record accepted design, and ADRs record durable decisions. Architecture can still record no-impact rationale, update the canonical architecture package, or create/update ADRs. Architecture-review reviews those concrete surfaces and blocks unresolved direction or behavior back to proposal or spec.

The downside is that contributors lose a dedicated architecture-stage scratchpad for speculative design. That is acceptable because proposal artifacts already compare options, and unaccepted design truth should not enter architecture.

### Option 3: Collapse architecture decisions into ADRs only

This would make ADRs the primary design surface.

The downside is that ADRs explain decisions, not the current system shape. The canonical architecture package would become stale or underused, and small architecture edits that are not durable decisions would have no natural home.

## Recommended direction

Choose Option 2.

Adopt this core invariant:

```text
Proposal resolves uncertainty.
Architecture records accepted design.
ADR records durable decisions.
```

Add the best-practice rule:

```text
Do not put unaccepted design truth into architecture.
```

If direction or design is unsettled, route to proposal or proposal revision. If behavior is unsettled, route to spec or spec revision. Architecture should not create a temporary architecture document to explore options. Proposal compares options, proposal-review settles direction, and architecture records the accepted shape.

Use this architecture decision tree:

1. No architecture impact: record a no-architecture-impact rationale in the plan, spec, change metadata, or PR evidence.
2. Direction or design is unclear: stop and route to proposal or proposal revision.
3. Behavior contract is unclear: stop and route to spec or spec revision.
4. Architecture impact is clear: update the canonical architecture package directly.
5. Durable architecture decision exists: create or update an ADR.

Revise the `architecture` skill to own:

- deciding whether architecture work is needed;
- updating the canonical architecture package directly;
- creating or updating ADRs for durable decisions;
- recording no-impact rationale when architecture is not needed;
- stopping when direction or spec is not ready.

Revise the `architecture` skill to stop owning:

- product direction selection;
- speculative design exploration;
- temporary change-local architecture deltas;
- implementation sequencing.

Revise the `architecture-review` skill so it classifies the review surface before reviewing:

- `canonical-architecture-update`;
- `ADR`;
- `no-architecture-impact-rationale`;
- `proposal-or-spec-gap`.

For canonical architecture updates, review changed canonical architecture sections, diagrams, and ADR links directly. Do not require a change-local architecture delta. For ADRs, review context, decision, alternatives, consequences, and compatibility with canonical architecture. For no-impact rationale, check that the rationale is credible. For proposal or spec gaps, return a finding that routes back to the owning stage instead of settling direction in architecture-review.

Keep ADRs separate from ordinary canonical architecture edits. Create or update an ADR when a change introduces or revises a durable decision, such as runtime/platform choice, system boundary, data-flow ownership, validation architecture, adapter generation model, public skill surface boundary, deployment or packaging model, cache/indexing strategy, or security boundary.

Use portable public-skill wording:

```text
Use the project's canonical architecture package.

Common default paths are:

- docs/architecture/system/architecture.md
- docs/architecture/system/diagrams/
- docs/adr/

If the project uses different architecture paths, follow the project's configured paths.
```

## Expected behavior changes

- Architecture no longer creates change-local deltas as a normal surface for unsettled design reasoning.
- Architecture work either records no impact, updates canonical architecture, creates or updates ADRs, or blocks on proposal/spec readiness.
- Architecture-review stops requiring change-local architecture deltas and reviews the actual surface under consideration.
- Published skill text becomes more portable across projects with different canonical architecture paths.
- The architecture package method spec needs revision because its current requirements still define change-local architecture deltas as part of the normal method.

## Architecture impact

This change affects workflow architecture and public skill-surface boundaries.

Expected authoritative updates include:

- `specs/architecture-package-method.md` to remove existing change-local delta requirements from the normal architecture skill contract.
- `skills/architecture/SKILL.md` to replace delta-oriented output guidance with the architecture surface decision model.
- `skills/architecture-review/SKILL.md` to replace delta-oriented review assumptions with review-surface classification.
- `docs/workflows.md` if its architecture-stage summary implies change-local deltas or architecture-owned option selection.
- `CONSTITUTION.md` and `AGENTS.md` only if their concise governance language needs alignment after the spec change.
- Generated adapter or local skill mirrors only through the repository's normal generation process, not by hand-editing `.codex/skills/` or `dist/adapters/`.

A new ADR amending or narrowing `ADR-20260428-architecture-package-method` is warranted because the change revises a durable workflow architecture decision: architecture will record accepted design directly in canonical surfaces rather than using temporary architecture deltas as a normal stage artifact. The later change should preserve the existing accepted ADR as decision history and should not fully supersede that ADR unless the whole C4 plus arc42 plus ADR method is being replaced. The existing ADR may receive only an explicit lifecycle cross-reference if the later spec or ADR contract requires it.

The later spec should make the normal architecture authoring path explicit:

```text
Change-local architecture deltas are not part of the normal architecture authoring path.

Existing change-local deltas remain valid historical evidence.

New deltas may exist only as legacy closeout or explicit exceptional evidence, not as the default or recommended architecture surface.
```

The later spec and test spec should also require architecture-review to classify the review surface before applying checks:

```text
Architecture-review must first classify the review surface as one of:

- canonical-architecture-update
- ADR
- no-architecture-impact-rationale
- proposal-or-spec-gap

It must not require a change-local architecture delta for a canonical architecture update.

If the issue is unsettled direction, route to proposal.
If the issue is unsettled behavior, route to spec.
```

## Testing and verification strategy

The spec change should map each revised architecture responsibility to tests in `specs/architecture-package-method.test.md`.

Likely coverage:

- no-impact changes can record rationale without architecture package edits;
- unclear direction routes to proposal or proposal revision;
- unclear behavior routes to spec or spec revision;
- clear architecture impact updates the canonical package directly;
- durable decisions create or update ADRs;
- change-local architecture deltas are removed from the normal architecture authoring path and remain only historical, legacy-closeout, or explicit exceptional evidence;
- architecture-review classifies the review surface before applying checks;
- architecture-review accepts review surfaces without requiring change-local deltas;
- public skill wording remains portable and does not impose RigorLoop-only paths on downstream projects.

Verification should include the repository-owned validation commands named by the later plan or test spec.

Because this change updates published skill text, the later plan should require adapter drift check plus adapter validation, normally:

```bash
python scripts/build-adapters.py --check
python scripts/validate-adapters.py
```

## Rollout and rollback

Rollout should update the approved architecture package spec first, then update architecture and architecture-review skills to match it. Contributor-facing workflow guidance should be adjusted only where it currently implies the older delta model.

Generated skill mirrors and adapter packages should be regenerated through existing scripts after canonical skill edits. Before handoff, the change should pass adapter drift check and adapter validation, normally `python scripts/build-adapters.py --check` and `python scripts/validate-adapters.py`.

Rollback is straightforward before downstream artifacts depend on the new model: restore the previous spec and skill guidance that permits change-local architecture deltas as a normal working artifact. After adoption, rollback would need to clarify whether any canonical-only updates created under the simplified model need additional change-local evidence.

## Risks and mitigations

- Risk: removing change-local deltas may leave complex design reasoning with no home. Mitigation: route option comparison to proposal and keep architecture tradeoffs limited to accepted design rationale.
- Risk: contributors may skip architecture entirely for changes that have real impact. Mitigation: keep the decision tree explicit and require no-impact rationale to be credible.
- Risk: canonical architecture updates may be made before direction is accepted. Mitigation: add the invariant that unaccepted design truth does not belong in architecture.
- Risk: ADRs may become overused for small edits. Mitigation: keep ADR triggers focused on durable decisions and explicitly say ADRs are not required for every small architecture edit.
- Risk: existing tests and docs may still enforce change-local deltas. Mitigation: revise the spec and test spec together before implementation.

## Open questions

- None.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-09 | Draft proposal recommends routing uncertainty to proposal/spec and updating canonical architecture directly when design is clear. | This preserves traceable architecture truth while removing temporary architecture deltas as a normal review surface. | Keeping the current delta model, making deltas merely rare, or using ADRs as the only architecture surface. |
| 2026-05-09 | Remove existing change-local delta requirements from the normal architecture skill contract. | The simplified model should make canonical architecture updates, ADRs, no-impact rationale, and proposal/spec blockers the normal architecture surfaces. | Retaining deltas as a normal or rare architecture-skill output. |
| 2026-05-09 | Create a new ADR amending or narrowing `ADR-20260428-architecture-package-method` instead of fully superseding it. | The change narrows one decision inside the C4 plus arc42 plus ADR method; it does not replace the whole method. The existing accepted ADR should remain decision history and may receive only an explicit lifecycle cross-reference if the later spec or ADR contract requires it. | Fully superseding the ADR for a scoped responsibility change, or rewriting the accepted ADR as if the original decision had always been different. |
| 2026-05-09 | Require adapter drift check plus adapter validation for the later skill-text change. | Published skill changes must prove generated adapters are current and valid. | Relying only on generic validation or manual inspection. |

## Next artifacts

- Test-spec revision for `specs/architecture-package-method.test.md`.
- New ADR amending or narrowing `ADR-20260428-architecture-package-method` for the durable workflow architecture decision.
- Execution plan for updating specs, skills, generated outputs, docs, and validation.

## Follow-on artifacts

- Proposal-review: approved in [proposal-review-r2](../docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/proposal-review-r2.md).
- Spec revision: [Architecture Package Method](../../specs/architecture-package-method.md).

## Readiness

Accepted after proposal-review R2. Follow-on spec revision has been drafted in `specs/architecture-package-method.md`; implementation should wait for downstream spec-review, test-spec, ADR, architecture, and plan artifacts.
