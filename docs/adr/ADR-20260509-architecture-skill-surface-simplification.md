# ADR-20260509-architecture-skill-surface-simplification: Architecture Skill Surface Simplification

## Status

accepted

## Context

`ADR-20260428-architecture-package-method` adopted C4 plus official arc42 plus ADRs as RigorLoop's default architecture package method. That decision introduced one canonical architecture package, ADRs for durable decisions, and change-local architecture deltas for architecture-significant work that needed working design reasoning before accepted content was merged into the canonical package.

The accepted proposal `docs/proposals/2026-05-09-simplify-architecture-skill-surfaces.md` and the approved amendment to `specs/architecture-package-method.md` narrow that method. The current architecture skill and architecture-review skill should no longer treat change-local architecture deltas as a normal authoring or review surface. Unsettled product direction belongs in proposal work, unsettled behavior belongs in spec work, accepted architecture truth belongs in the canonical architecture package, and durable decisions belong in ADRs.

The original C4 plus arc42 plus ADR method remains valid. This ADR amends and narrows the change-local delta part of `ADR-20260428-architecture-package-method`; it does not supersede the whole method.

## Decision

Keep C4 plus official arc42 plus ADRs as RigorLoop's default architecture package method.

Remove change-local architecture deltas from the normal architecture authoring path.

Normal architecture authoring now chooses the smallest valid surface:

- no-architecture-impact rationale;
- direct canonical architecture package update;
- ADR creation, amendment, supersession, or deprecation for durable decisions;
- blocked routing to proposal or spec when direction or behavior is not ready.

Existing change-local architecture deltas remain valid historical evidence. New change-local architecture deltas may exist only as legacy closeout or explicit exceptional evidence. They are not the default or recommended architecture surface and must not become competing current architecture truth.

Architecture-review must first classify the review surface as one of:

- `canonical-architecture-update`;
- `ADR`;
- `no-architecture-impact-rationale`;
- `proposal-or-spec-gap`.

Architecture-review must not require a change-local architecture delta for a canonical architecture update. If direction is unsettled, architecture-review routes back to proposal or proposal revision. If behavior is unsettled, architecture-review routes back to spec or spec revision.

## Alternatives considered

### Keep the 2026-04-28 delta model unchanged

Rejected because it keeps a normal temporary architecture surface that can attract unaccepted option selection and duplicate canonical architecture truth.

### Keep change-local deltas as a rare but normal architecture output

Rejected because review and authoring guidance would still need to preserve delta creation, merge-back, and temporary truth as normal concepts. That keeps the complexity the simplification is meant to remove.

### Replace the entire C4 plus arc42 plus ADR method

Rejected because the problem is not the structural architecture package, the arc42 section model, C4 diagrams, or ADRs. The problem is the normal use of temporary architecture deltas to resolve unsettled direction.

## Consequences

- Architecture authoring becomes simpler and more portable for published skills.
- Canonical architecture package updates become the normal surface for accepted current architecture truth.
- Proposal and spec stages retain ownership of unresolved direction and behavior.
- ADRs remain the durable decision history for architecture decisions.
- Existing change-local architecture deltas remain historical evidence and do not need to be deleted.
- Architecture-review no longer requires or expects a change-local architecture delta before reviewing a canonical architecture update.
- Canonical skills, generated Codex skill mirrors, and public adapter packages must be updated through existing generation paths.
- Adapter drift check and adapter validation are required for the later skill text change.

## Follow-up

- Update `skills/architecture/SKILL.md` and `skills/architecture-review/SKILL.md` to match the approved simplification contract.
- Update `specs/architecture-package-method.test.md` to cover the new R32-R39, R56-R57, R61, R85-R86, R110, R119-R124, AC21, and AC22 behavior.
- Regenerate generated skill mirrors and public adapter packages after canonical skill changes.
- Run adapter drift check and adapter validation, normally:

```bash
python scripts/build-adapters.py --check
python scripts/validate-adapters.py
```
