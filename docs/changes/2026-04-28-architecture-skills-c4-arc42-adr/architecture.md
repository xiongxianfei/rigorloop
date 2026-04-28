# Architecture Method Change Architecture Delta

## Status

- approved

Historical note: after M3 merge-back, this change-local delta is evidence for this change and no longer the current architecture source.

## Related artifacts

- Proposal: `docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md`
- Spec: `specs/architecture-package-method.md`
- ADR: `docs/adr/ADR-20260428-architecture-package-method.md`
- Canonical package: `docs/architecture/system/architecture.md`
- Canonical context diagram: `docs/architecture/system/diagrams/context.mmd`
- Canonical container diagram: `docs/architecture/system/diagrams/container.mmd`
- Context diagram: `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/diagrams/context.mmd`
- Container diagram: `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/diagrams/container.mmd`

## Introduction and Goals

This architecture delta defines how RigorLoop adopts the approved architecture package method for the architecture-method change itself. It is a change-local working artifact, not the canonical architecture package.

After M3, durable current architecture content from this delta is merged into `docs/architecture/system/architecture.md`. Downstream architecture work must rely on the canonical package and accepted ADRs, while this delta remains historical evidence for this change.

The implementation must create a canonical architecture package, add architecture and ADR templates, update workflow and governance guidance, update architecture skills, refresh generated skill and adapter output through existing generators, and preserve legacy architecture artifacts until a later normalization artifact classifies them.

Primary goals:

- introduce one canonical architecture package based on C4, arc42, and ADRs;
- keep feature-specific architecture deltas temporary and change-local;
- make diagrams diffable source text;
- record the durable method decision in an ADR;
- keep the first implementation review-based except for the narrow lifecycle-validator compatibility required by the spec.

## Architecture Constraints

- `specs/architecture-package-method.md` is the governing contract for this change.
- `specs/rigorloop-workflow.md` may receive only a short routing and output pointer, not a duplicate package contract.
- The canonical package path must be `docs/architecture/system/architecture.md` with default C4 diagrams under `docs/architecture/system/diagrams/`.
- The first canonical C4 diagrams must use Mermaid `.mmd` source files unless an approved architecture artifact supersedes that choice.
- `templates/` becomes canonical authored workflow content and therefore requires `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` updates.
- `.codex/skills/` and `dist/adapters/` remain generated output and must be refreshed only through existing generation commands.
- The first slice must not add required package-shape validation, required C4-file checks, or ADR-presence enforcement.
- The existing artifact lifecycle validator currently expects the older architecture document section model under `docs/architecture/`; implementation must add only the narrow compatibility needed for the new canonical arc42 package shape.
- Existing approved architecture documents remain legacy or historical until a later migration artifact classifies them.

## Context and Scope

RigorLoop currently has architecture documents under `docs/architecture/`, ADRs under `docs/adr/`, workflow specs under `specs/`, source skills under `skills/`, generated Codex runtime skills under `.codex/skills/`, and generated public adapter packages under `dist/adapters/`.

The existing architecture skill still describes the older repository-specific architecture document structure. The approved spec changes the future architecture package method to official arc42 sections plus C4 diagrams and ADRs.

This delta is scoped to the architecture of adopting that method. It does not implement templates, validators, skill edits, generated output, or legacy migration. Those belong to the later execution plan and implementation.

External actors and systems:

- Contributor or agent authors architecture artifacts.
- Reviewer checks the method, diagrams, ADRs, and merge-back path.
- Repository validation scripts check lifecycle status, change metadata, skill structure, generated drift, and adapter drift.
- Git and PR review carry the authoritative diff.

## Solution Strategy

Use this change-local delta as the first live example of the method while keeping the durable baseline implementation separate:

1. Architecture stage creates this change-local delta and a draft ADR.
2. Architecture-review validates the delta, diagrams, ADR trigger, and implementation boundaries.
3. Plan splits implementation so governance, workflow summaries, templates, skills, generated output, validator compatibility, canonical package baseline, and legacy normalization planning are reviewable.
4. Implementation creates `docs/architecture/system/architecture.md` and `docs/architecture/system/diagrams/*.mmd` after adding the narrow lifecycle-validator compatibility required by the approved spec.
5. Durable content from this delta is merged into the canonical package before the architecture-method change is complete.
6. The change-local delta remains historical evidence under `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/`.

This sequence avoids making the current validator reject the first canonical arc42 package while still dogfooding the method in a real architecture artifact.

## Building Block View

| Building block | Responsibility | Source status |
| --- | --- | --- |
| `specs/architecture-package-method.md` | Normative method contract for C4, arc42, ADRs, canonical package, deltas, templates, and first-slice boundaries | approved spec |
| `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/architecture.md` | Change-local working architecture for this adoption change | authored delta |
| `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/diagrams/` | Change-local C4 source diagrams for review | authored delta diagrams |
| `docs/adr/ADR-20260428-architecture-package-method.md` | Durable decision record for the architecture package method | accepted ADR |
| `docs/architecture/system/` | Canonical architecture package and C4 source diagrams after M3 merge-back | implementation deliverable |
| `templates/architecture.md` and `templates/adr.md` | Canonical scaffolds for package and ADR authoring after M2 | implementation deliverable |
| `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md` | Governance and operational summaries that must acknowledge `templates/` and the focused spec pointer | implementation deliverable |
| `skills/architecture/SKILL.md` and `skills/architecture-review/SKILL.md` | Canonical skill guidance for authoring and reviewing the new method | implementation deliverable |
| `.codex/skills/` and `dist/adapters/` | Generated runtime and public adapter surfaces refreshed from canonical skills | generated deliverable |
| lifecycle validation scripts | Existing lifecycle validation plus narrow compatibility for the new canonical arc42 package path | implementation deliverable |
| legacy normalization artifact | Follow-on plan or architecture artifact classifying older `docs/architecture/` documents | follow-on deliverable |

The C4 source diagrams for this delta are:

- context: `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/diagrams/context.mmd`
- container: `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/diagrams/container.mmd`

## Runtime View

### Authoring and review flow

1. Contributor or agent reads the accepted proposal and approved spec.
2. Architecture stage creates a change-local architecture delta and draft ADR.
3. Architecture-review validates the delta against the approved method.
4. Plan defines implementation slices and validation commands.
5. Implementation updates source artifacts and generated outputs through existing generation commands.
6. Verify checks touched lifecycle artifacts, generated drift, skill validity, adapter validity, and change metadata.

### Canonical package merge-back flow

1. Implementation adds lifecycle-validator compatibility for `docs/architecture/system/architecture.md`.
2. Implementation creates the canonical package using all 12 official arc42 sections and C4 Mermaid diagrams.
3. Durable design content from this delta is incorporated into the canonical package.
4. Section 9 of the canonical package links the ADR.
5. This delta remains historical and must not be used as the canonical architecture source for downstream changes.

### Generated output refresh flow

1. Canonical skills under `skills/` are edited.
2. Existing generation commands refresh `.codex/skills/` and public adapter output.
3. Existing drift checks prove generated output matches canonical sources.

## Deployment View

This change has no deployed service, runtime infrastructure, database, or network environment.

Deployment is repository packaging:

- authored workflow content remains in `docs/`, `specs/`, `skills/`, `schemas/`, `scripts/`, and after implementation `templates/`;
- generated runtime compatibility remains under `.codex/skills/`;
- generated public adapter packages remain under `dist/adapters/`;
- canonical architecture package content will live under `docs/architecture/system/`;
- ADRs remain under `docs/adr/`;
- change-local evidence remains under `docs/changes/<change-id>/`.

Rollback removes or reverts the authored guidance, templates, canonical package, generated refresh, and validator compatibility for this method. No runtime data migration is needed.

## Crosscutting Concepts

### Source of truth

The focused spec is the normative method contract. The workflow spec receives only routing language. Templates are scaffolds, not lifecycle artifacts. The canonical architecture package becomes the current architecture source only after implementation creates and validates it.

### Lifecycle ownership

Proposal status is `accepted`, spec status is `approved`, this delta is `approved`, and the ADR is `accepted`.

### Validation

The first implementation remains review-based for architecture package completeness. The only validator change in scope is compatibility for the new canonical arc42 package path. Required package-shape enforcement is deferred.

### Generated output

Generated `.codex/skills/` and `dist/adapters/` output must be refreshed through existing generators after canonical skill changes.

### Legacy architecture handling

Existing `docs/architecture/` documents are not normalized by this architecture delta. A follow-on migration artifact must inventory and classify them before the repository claims all architecture artifacts are normalized.

## Architecture Decisions

The durable architecture decision is recorded in:

- `docs/adr/ADR-20260428-architecture-package-method.md`

This ADR records the decision to adopt C4 plus official arc42 plus ADRs, one canonical architecture package, change-local deltas for architecture-significant work, templates under `templates/`, diagrams as source text, and review-based first adoption.

## Quality Requirements

| Quality | Requirement |
| --- | --- |
| Reviewability | Architecture artifacts and diagrams must be diffable text and small enough to review in PR. |
| Traceability | Durable decisions must be linked from section 9 and preserved in ADRs. |
| Compatibility | Legacy architecture documents must remain valid until a migration artifact classifies them. |
| Proportionality | Leaf changes must not be forced to update architecture artifacts. |
| Determinism | Generated skill and adapter output must remain reproducible from canonical sources. |
| Governance clarity | `templates/` must be explicitly added as canonical authored workflow content. |

## Risks and Technical Debt

| Risk | Mitigation |
| --- | --- |
| Canonical arc42 package fails existing lifecycle validation | Add the narrow R71 compatibility update before creating `docs/architecture/system/architecture.md`. |
| This delta becomes a competing source of truth | Merge durable content into the canonical package and keep this file historical after completion. |
| ADR lifecycle drifts from architecture status | Keep this delta, diagrams, and the ADR lifecycle metadata consistent before planning relies on the design. |
| Templates and skills diverge | Update templates, skills, workflow summary, and generated outputs in the same implementation. |
| Legacy documents confuse contributors | Create the required follow-on legacy normalization artifact. |
| Enforcement automation arrives too early | Keep package-shape validation out of the first implementation and document that boundary in the plan. |

## Glossary

- architecture delta: this change-local working architecture artifact.
- canonical package: the `docs/architecture/system/` package that becomes the current architecture source after M3 merge-back.
- lifecycle-validator compatibility: the narrow script change that lets the new canonical arc42 package coexist with existing lifecycle validation.
- merge-back: incorporating accepted durable content from this delta into the canonical package.

## Next artifacts

- `architecture-review` for this architecture delta and ADR.
- Execution plan after architecture-review.
- Plan-review after the plan is drafted.
- Test spec after plan-review.

## Follow-on artifacts

- `architecture-review`: approved on 2026-04-28 after lifecycle/status consistency corrections.

## Readiness

Architecture review is complete and this change-local architecture delta is approved. After M3 merge-back, this delta is historical evidence only; downstream architecture work must use `docs/architecture/system/architecture.md` plus accepted ADRs as current architecture guidance.
