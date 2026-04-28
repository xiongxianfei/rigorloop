# Architecture Package Method

## Status

- approved

## Related proposal

- [Architecture Skills with C4, arc42, and ADRs](../docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md)

## Goal and context

This spec defines RigorLoop's contributor-visible architecture package method for architecture work that is required by the workflow. The method standardizes one living canonical architecture baseline, change-local architecture deltas when a specific change needs working design reasoning, C4 diagrams for structural views, arc42 for the written architecture structure, and ADRs for durable decisions.

The goal is to make architecture work consistent and reviewable without making every feature rewrite the architecture baseline. Architecture-changing work should update the smallest affected part of the canonical package, record durable decisions as ADRs, and preserve enough change-local evidence for review when design reasoning happens before merge-back.

## Glossary

- architecture package: the set of architecture artifacts that describe current system structure, runtime/deployment concerns, quality concerns, risks, and decision references.
- canonical architecture package: the long-lived current architecture source of truth for the repository.
- change-local architecture delta: a temporary working architecture artifact for one change, stored under `docs/changes/<change-id>/`, that is merged back into the canonical package before the architecture-significant change is complete.
- complete architecture-significant change: a change whose required architecture work has passed review, whose durable architecture content has been merged back into the canonical package, and whose durable decisions have been recorded as ADRs before final verification or PR handoff.
- C4: the diagram model used for default system context, container, and conditional component views.
- arc42: the 12-section architecture document structure used for `architecture.md`.
- ADR: an Architecture Decision Record under `docs/adr/` that preserves an important architecture decision, alternatives, consequences, and follow-up.
- durable architecture decision: a decision that changes or constrains long-lived system boundaries, packaging, validation, generated output, portability, release behavior, caching/indexing, or major workflow architecture.
- diagram-as-code: a C4 diagram stored as reviewable text in the repository rather than only as an external image or proprietary binary.
- merge-back: the act of incorporating accepted change-local architecture content into the canonical architecture package and recording durable decisions as ADRs.
- legacy architecture artifact: an existing architecture document under `docs/architecture/` created before this method is adopted and not yet normalized into the canonical package lifecycle.

## Examples first

### Example E1: architecture-changing feature updates the canonical package

Given a change modifies generated adapter packaging boundaries
When the change reaches the architecture stage
Then contributors update the affected canonical Building Block View, C4 container or component view, and Deployment View as needed
And they add an ADR if the packaging decision is durable.

### Example E2: leaf change does not move architecture docs

Given a change fixes a typo or adjusts a local test fixture without changing boundaries, data flow, generated output, deployment, or long-lived decisions
When the change is classified for architecture impact
Then the canonical architecture package and ADR set remain unchanged
And the no-architecture rationale can stay in the plan, test spec, change metadata, or PR evidence for the change.

### Example E3: change-local delta is merged back after acceptance

Given a feature needs design reasoning before implementation
When contributors create `docs/changes/2026-04-28-example-change/architecture.md`
Then that file is treated as the working architecture delta for the change
And before the architecture-significant change is complete, durable content is merged into the canonical architecture package
And the delta remains only historical evidence under `docs/changes/2026-04-28-example-change/`.

### Example E4: section 9 links ADRs

Given a change chooses a new validation architecture after rejecting alternatives
When contributors update `architecture.md`
Then arc42 section 9, `Architecture Decisions`, summarizes and links the relevant ADR
And the ADR under `docs/adr/` records context, decision, alternatives considered, consequences, and follow-up.

### Example E5: all arc42 sections are present without heavy prose

Given a small architecture-affecting workflow change has no deployment impact
When contributors update the canonical architecture package
Then `architecture.md` still contains `Deployment View`
And that section may say `Not applicable` with a short rationale instead of inventing deployment detail.

### Example E6: legacy architecture docs are not silently normalized

Given older approved architecture documents already exist under `docs/architecture/`
When this method is adopted
Then the repository may apply the new canonical package rule prospectively
And it must not claim all legacy architecture artifacts have been normalized until a migration artifact inventories and classifies them.

## Requirements

R1. RigorLoop MUST standardize required architecture work around C4, arc42, and ADRs.

R2. The detailed normative architecture package contract MUST live in this spec.

R3. `specs/rigorloop-workflow.md` MUST contain only stage-level routing and handoff rules for this method, including a pointer to this spec, rather than duplicating the full C4, arc42, ADR, template, or package lifecycle contract.

R4. The canonical architecture package MUST be the long-lived current architecture source of truth for the repository.

R5. The default canonical architecture package path MUST be:

```text
docs/architecture/system/architecture.md
docs/architecture/system/diagrams/context.mmd
docs/architecture/system/diagrams/container.mmd
```

R6. A later approved architecture document or ADR MAY supersede the default canonical package path, but it MUST identify the replacement path and migration expectations before downstream work relies on the new path.

R7. The canonical `architecture.md` MUST use these 12 arc42 section headings in this order:

1. Introduction and Goals
2. Architecture Constraints
3. Context and Scope
4. Solution Strategy
5. Building Block View
6. Runtime View
7. Deployment View
8. Crosscutting Concepts
9. Architecture Decisions
10. Quality Requirements
11. Risks and Technical Debt
12. Glossary

R8. The canonical `architecture.md` MUST include repository lifecycle status metadata using the architecture artifact status vocabulary before the arc42 section sequence.

R9. Repository lifecycle metadata sections MUST NOT replace, remove, or rename any of the 12 required arc42 section headings.

R10. The architecture method MUST keep arc42 lightweight through concise content and explicit `Not applicable` rationale, not by removing or renaming official arc42 sections.

R11. Every canonical architecture package update MUST preserve all 12 arc42 section headings.

R12. Any arc42 section marked `Not applicable` MUST include a rationale that explains why the concern is irrelevant for the current package or update.

R13. Sections 1 through 5 SHOULD contain substantive current-system content for real architecture work. If any of sections 1 through 5 is marked `Not applicable`, the artifact MUST explain why an architecture package exists while that core concern is irrelevant.

R14. Section 6, `Runtime View`, MUST be updated when behavior, orchestration, failure paths, command flow, generated-output flow, or operational flow changes.

R15. Section 7, `Deployment View`, MUST be updated when environments, packaging, generated outputs, adapters, release layout, infrastructure, or execution boundaries change.

R16. Section 8, `Crosscutting Concepts`, MUST be updated when a change introduces or revises a cross-cutting architecture rule such as validation strategy, security boundary, caching pattern, portability rule, generation policy, or observability pattern.

R17. Section 9, `Architecture Decisions`, MUST always be present and MUST either summarize and link relevant ADRs or state that no ADRs are required for the current package or update.

R18. Section 10, `Quality Requirements`, MUST name the most relevant quality attributes for the architecture package, even when the section is short.

R19. Section 11, `Risks and Technical Debt`, MUST record known architecture risks, deferred cleanup, and technical debt that affect the package or update.

R20. Section 12, `Glossary`, MUST be present. It MAY say `Not applicable` with rationale when no architecture terms need definition.

R21. The default canonical architecture package MUST include a C4 system context diagram.

R22. The default canonical architecture package MUST include a C4 container diagram.

R23. A C4 component diagram MUST be added or updated when container-level structure is not enough to explain changed responsibilities, internal boundaries, or interactions.

R24. Code-level diagrams MUST NOT be required by default.

R25. Deployment diagrams MUST be added only when infrastructure, runtime environment, packaging, adapter distribution, or deployment mapping needs visual explanation beyond the arc42 Deployment View prose.

R26. C4 diagrams MUST be stored as reviewable source text in the repository.

R27. The first implementation of this method MUST use Mermaid `.mmd` files for the default context and container diagrams unless an approved architecture artifact chooses another source-text format before implementation.

R28. Additional diagram source formats MAY be used only when they are text-based, reviewable in diffs, and documented in the architecture package or an ADR. Acceptable examples are Mermaid, Structurizr DSL, and PlantUML.

R29. A generated image, exported diagram, screenshot, or external diagram link MUST NOT be the only source of truth for a required C4 diagram.

R30. Feature work MUST update only the arc42 sections and C4 views that the feature actually affects.

R31. Feature work SHOULD update the lowest affected C4 level first and propagate changes upward only when the change affects the higher-level view.

R32. A feature-specific architecture delta MUST be used only when a change is architecture-significant enough to need reviewable working design reasoning before accepted content is merged into the canonical package.

R33. The default change-local architecture delta path MUST be:

```text
docs/changes/<change-id>/architecture.md
```

R34. Optional supporting diagrams for a change-local architecture delta MUST live under:

```text
docs/changes/<change-id>/diagrams/
```

R35. A change-local architecture delta MUST NOT be treated as a competing canonical architecture document.

R36. During an active change, a change-local architecture delta MAY be the working architecture artifact for that change.

R37. Before an architecture-significant change is considered complete, durable content from the change-local architecture delta MUST be merged into the canonical architecture package when it changes current architecture truth.

R38. Before an architecture-significant change is considered complete, durable decisions from the change-local architecture delta MUST be recorded as ADRs under `docs/adr/` when they meet ADR creation criteria.

R39. After merge-back, a change-local architecture delta MUST remain historical evidence only and MUST NOT be used as the canonical architecture source for downstream work.

R40. Architecture changes MUST be reviewed in the same PR as the code, workflow, template, skill, or documentation change that requires them unless an approved plan explicitly sequences the architecture update first.

R41. For non-trivial changes with new or changed operational flow, contributors SHOULD write or update the relevant Runtime View before implementation begins.

R42. For small changes whose architecture impact is clear only after implementation, contributors MAY update the canonical package after implementation and before final verification.

R43. A leaf change that does not affect architecture boundaries, data flow, generated-output flow, deployment, packaging, adapters, quality targets, cross-cutting rules, or durable decisions MUST NOT be required to update the architecture package.

R44. An ADR MUST be created when a change introduces or revises a durable architecture decision.

R45. Durable architecture decision triggers MUST include at least:
- system boundary changes;
- adapter generation or packaging rules;
- validation architecture;
- cache or indexing strategy;
- portability constraints;
- release architecture;
- major workflow architecture decisions.

R46. Each ADR created under this method MUST include title, status, context, decision, alternatives considered, consequences, and follow-up.

R47. ADR status vocabulary MUST align with repository lifecycle guidance: `draft`, `proposed`, `accepted`, `active`, `deprecated`, `superseded`, `archived`, and `abandoned`.

R48. Accepted or active ADRs MUST be append-only for decision history. Later changes MUST supersede or deprecate an old ADR with a new ADR or explicit lifecycle update rather than rewriting the old decision as if it had always been different.

R49. `templates/architecture.md` MUST exist as the default architecture package scaffold.

R50. `templates/adr.md` MUST exist as the default ADR scaffold.

R51. Architecture and ADR templates MUST live under `templates/`, not under `docs/architecture/` or `docs/adr/`.

R52. `docs/architecture/` and `docs/adr/` MUST contain real lifecycle-managed artifacts, not disguised templates.

R53. Adding `templates/` for architecture and ADR scaffolding MUST be treated as a canonical-source boundary update.

R54. The first implementation of this spec MUST update `CONSTITUTION.md` and `AGENTS.md` when adding `templates/` as canonical authored workflow content.

R55. The first implementation of this spec MUST update `docs/workflows.md` with concise contributor-facing summary guidance and a pointer to this spec.

R56. `skills/architecture/SKILL.md` MUST be updated to use this C4, arc42, canonical package, change-local delta, and ADR method.

R57. `skills/architecture-review/SKILL.md` MUST be updated to review C4 sufficiency, all 12 arc42 sections, Runtime View and Deployment View conditions, change-local delta merge-back, and ADR completeness.

R58. Generated `.codex/skills/` and public adapter package output MUST be refreshed only through the existing generation path when canonical skill guidance changes.

R59. The first positive example of this method MUST be the architecture-method change itself.

R60. The first positive example MUST NOT be only a synthetic example.

R61. The first positive example MAY use a change-local architecture delta, but accepted durable content MUST be merged back into the canonical architecture package before the architecture-method change is considered complete.

R62. The canonical architecture package rule applies prospectively once this spec is approved and implemented.

R63. Existing approved architecture documents under `docs/architecture/` MAY remain valid historical or legacy artifacts until a migration artifact normalizes their lifecycle.

R64. This spec MUST NOT require immediate full migration of every legacy architecture artifact before the first implementation can complete.

R65. Rollout MUST include a follow-on legacy architecture lifecycle normalization artifact that inventories existing `docs/architecture/` documents and classifies each as current canonical package content, superseded, archived or historical snapshot, or another explicitly documented historical status.

R66. Until the legacy normalization artifact is complete, repository guidance MUST NOT claim that all existing architecture artifacts have already been normalized into one canonical architecture package.

R67. The first implementation of this spec MUST remain review-based and MUST NOT add required structural validators for arc42 section presence, required C4 diagram files, ADR presence, or package shape.

R68. Required architecture-package enforcement automation MAY be introduced only after at least one real architecture package has used this method and a later approved spec, plan, or ADR defines the automation contract.

R69. A non-blocking helper for architecture package inspection MAY be added later only if it does not become a required pass gate before R68 is satisfied.

R70. The first implementation MUST NOT add a new external dependency solely to author templates, update architecture guidance, store Mermaid diagram source, or record ADRs.

R71. Existing artifact lifecycle validation MUST be updated only as needed to accept the new canonical arc42 architecture package shape under `docs/architecture/system/` without requiring the older architecture section names on that canonical package.

R72. The R71 compatibility update MUST NOT add required arc42 section validation, required C4 diagram validation, ADR-presence validation, package-shape validation, selected check coverage changes, command output changes, or command exit behavior changes.

R73. Architecture artifacts, diagrams, templates, and ADRs MUST NOT include secrets, credentials, private keys, or machine-local debug-only data unless an approved example explicitly justifies the data and keeps it non-sensitive.

R74. Architecture diagrams and prose SHOULD describe trust boundaries, permissions, data exposure, and secret handling when the change affects those concerns.

R75. Contributor-facing Markdown templates and diagrams SHOULD use clear headings, stable paths, and concise text so reviewers can navigate them with ordinary repository review tools.

## Inputs and outputs

Inputs:

- accepted proposal direction for C4, arc42, ADRs, canonical architecture, change-local deltas, templates, and review-based rollout;
- requests or workflow stages that require architecture work;
- existing specs, architecture documents, ADRs, plans, test specs, workflow summaries, skills, templates, generated skill output, and adapter packages;
- change-local artifacts under `docs/changes/<change-id>/`;
- review findings from `spec-review`, `architecture-review`, and later lifecycle stages.

Outputs:

- a focused architecture package method contract in this spec;
- a canonical architecture package under `docs/architecture/system/`;
- Mermaid source-text C4 context and container diagrams by default;
- optional C4 component or deployment diagrams when required by the change;
- ADRs under `docs/adr/` for durable decisions;
- change-local architecture deltas under `docs/changes/<change-id>/` only when needed;
- templates under `templates/`;
- updated governance, workflow summary, and architecture skill guidance;
- review evidence rather than new required enforcement automation in the first implementation.

## State and invariants

- The canonical architecture package is the current architecture source of truth after this method is implemented.
- Change-local architecture deltas are temporary working artifacts and historical evidence, not permanent competing current architecture sources.
- ADRs preserve durable decisions separately from the arc42 architecture narrative.
- The arc42 12-section model remains intact even when sections are concise or marked `Not applicable`.
- C4 diagrams remain source-text artifacts that reviewers can diff.
- `templates/` is canonical authored workflow content once the first implementation updates the governing source-boundary guidance.
- `.codex/skills/` and `dist/adapters/` remain generated output and are not hand-edited.
- Existing legacy architecture artifacts are not automatically normalized merely because this spec is approved.

## Error and boundary behavior

- If architecture work omits one of the 12 required arc42 sections, `architecture-review` must treat that as a review finding before the package can be relied on.
- If a required C4 context or container diagram is missing from the canonical package, `architecture-review` must require adding it unless a later approved artifact supersedes the default diagram requirement.
- If a change-local architecture delta contains durable current architecture truth but no merge-back path, `architecture-review`, `verify`, or PR review must treat the change as incomplete.
- If a durable architecture decision is captured only in prose and no ADR is created, architecture review must require either an ADR or an explicit rationale that the decision is not durable.
- If an external or binary diagram is provided without a source-text diagram, it may supplement review but must not satisfy required C4 diagram evidence.
- If a legacy architecture artifact conflicts with the canonical package before migration completes, downstream work must rely on the approved spec, accepted ADRs, and canonical package, and the conflict must be recorded for the legacy normalization artifact.
- If a proposed implementation adds required architecture-package validation automation in the first slice, it violates this spec unless the spec has first been superseded or amended.

## Compatibility and migration

This method is a documentation, workflow, and architecture-guidance change. It does not change runtime behavior, public APIs, data formats, release artifacts, or command behavior by itself.

Adoption is prospective. New architecture work after implementation must follow this method. Existing `docs/architecture/` documents may remain in their current lifecycle state until the follow-on legacy normalization artifact inventories and classifies them.

Rollback can revert the focused spec, templates, workflow pointer, governance boundary update, skill updates, generated skill refresh, canonical package baseline, and first example artifacts. Because this method does not create runtime state, rollback requires no data migration.

## Observability

The observable proof for this method is repository artifact state and review evidence:

- `spec-review` validates this contract before architecture or planning relies on it;
- `architecture-review` validates the first canonical package and any architecture-significant change-local delta against this method;
- artifact lifecycle validation checks statuses for touched proposals, specs, architecture documents, test specs, and ADRs;
- skill validation checks canonical skill shape after architecture skill updates;
- adapter and generated skill drift checks prove generated output was refreshed when canonical skill guidance changes;
- final verification names the exact validation commands run.

No runtime logs, metrics, traces, audit events, or user-visible service status changes are required by this spec.

## Security and privacy

R73 defines the security boundary for architecture artifacts, diagrams, templates, and ADRs.

R74 defines when architecture artifacts should describe security and privacy concerns.

This spec adds no authentication, authorization, secret storage, telemetry, or personal-data processing behavior.

## Accessibility and UX

No product UI is involved.

R75 defines contributor-facing readability expectations for Markdown templates and diagrams.

## Performance expectations

This method must not add required runtime work.

The first implementation should keep authoring and review overhead proportional by requiring context and container diagrams by default, making component and deployment diagrams conditional, allowing concise arc42 sections, and deferring required enforcement automation.

## Edge cases

1. If a change affects only a component boundary inside an existing container, update the C4 component view when present or add one if needed; do not redraw the system context view unless external actors or systems changed.
2. If a change adds a new external system or actor, update `Context and Scope` and the C4 system context diagram.
3. If a change introduces generated output or adapter packaging behavior, update `Deployment View` when execution or packaging boundaries change, even if no infrastructure is deployed.
4. If a feature introduces no durable decision after review, section 9 must explicitly state that no ADR is required for that update.
5. If two durable decisions are independent, create separate ADRs when one combined ADR would obscure alternatives or consequences.
6. If a change-local delta is rejected or abandoned, do not merge its content into the canonical package unless a later accepted change adopts the content.
7. If legacy architecture artifacts use the older repository architecture structure, leave them in place until the migration artifact classifies them.
8. If an architecture package needs a non-Mermaid diagram format, document the text-based format choice before relying on it.
9. If the architecture-method change itself produces a change-local delta, treat that delta as working evidence and merge durable content into the canonical package before completion.
10. If a future validator is added for this method, update or supersede this spec before making the validator a required pass gate.

## Non-goals

- Requiring architecture artifacts for trivial or leaf changes with no architecture impact.
- Rewriting every legacy architecture document during the first implementation.
- Creating a new canonical architecture document for every feature.
- Treating change-local architecture deltas as permanent current architecture sources.
- Replacing execution plans, test specs, review artifacts, or explain-change artifacts.
- Making 4+1, full UML, or code-level diagrams the default.
- Adding required structural architecture validators in the first implementation.
- Changing validation semantics, selected check coverage, command output, or command exit behavior beyond the narrow existing-lifecycle-validator compatibility update required by R71 and R72.
- Adding a new external diagramming dependency in the first implementation.

## Acceptance criteria

AC1. `docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md` is accepted and linked from this spec.

AC2. This spec defines the canonical architecture package path, change-local architecture delta path, template paths, and ADR path expectations.

AC3. The required ordered arc42 section list contains each of the 12 official section headings exactly once.

AC4. This spec requires default C4 system context and container diagrams and defines when component and deployment diagrams are conditional.

AC5. This spec requires diagrams to be stored as source text and prevents external or binary diagrams from being the only source of truth.

AC6. This spec defines merge-back behavior from change-local architecture deltas into the canonical package.

AC7. This spec defines ADR triggers, required ADR fields, status vocabulary, and append-only decision-history expectations.

AC8. This spec requires `templates/architecture.md` and `templates/adr.md` under `templates/`, and treats `templates/` as a canonical-source boundary update requiring `CONSTITUTION.md` and `AGENTS.md` updates.

AC9. This spec requires the architecture-method change itself to be the first positive example and prevents relying only on a synthetic first example.

AC10. This spec applies the canonical package rule prospectively and requires a follow-on legacy normalization artifact before claiming all legacy architecture artifacts are normalized.

AC11. This spec defers required architecture-package enforcement automation until after one real package uses the method.

AC12. The first implementation includes the R71 lifecycle-validator compatibility update when it adds the canonical arc42 package under `docs/architecture/system/`.

AC13. Targeted validation for this spec passes with artifact lifecycle validation, diff whitespace checks, and the repository CI wrapper for the touched proposal and spec paths.

## Open questions

None.

## Next artifacts

- `spec-review` for this spec.
- Architecture package and architecture-review for the architecture-method change when required.
- Execution plan after spec review and any required architecture work.
- Test spec after plan review.
- First implementation slice for templates, governance boundary updates, workflow pointer, skills, canonical package baseline, and first example.

## Follow-on artifacts

- `spec-review`: approved on 2026-04-28 after lifecycle status metadata, completion timing, workflow-summary update, and lifecycle-validator compatibility clarifications.

## Readiness

Spec review is complete and this spec is approved.

Immediate next repository stage: `architecture`, because this change affects architecture boundaries, canonical architecture package guidance, and ADR/template workflow boundaries.

Eventual `test-spec` readiness: conditionally-ready after required architecture and execution plan work complete.
