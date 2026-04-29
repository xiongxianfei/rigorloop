# C4, arc42, and Architecture Skill Quality Refinement Architecture Delta

## Status

- approved

## Related Artifacts

- Proposal: `docs/proposals/2026-04-29-c4-arc42-package-quality.md`
- Governing spec: `specs/architecture-package-method.md`
- Canonical architecture package: `docs/architecture/system/architecture.md`
- Canonical context diagram: `docs/architecture/system/diagrams/context.mmd`
- Canonical container diagram: `docs/architecture/system/diagrams/container.mmd`
- Architecture method ADR: `docs/adr/ADR-20260428-architecture-package-method.md`
- Change metadata: `docs/changes/2026-04-29-c4-arc42-package-quality/change.yaml`

## Introduction and Goals

This change-local architecture delta defines the 2026-04-29 quality refinement for the canonical C4, arc42, and ADR architecture package method. It is the working architecture artifact for this change, not a competing canonical source.

Goals:

- make the canonical context and container diagrams recognizable as C4 diagrams;
- make `architecture.md` link diagram source by relative path;
- make the Building Block View hierarchical enough for review;
- keep Architecture Decisions link-focused so ADRs own rationale;
- express Quality Requirements as concise scenarios;
- optimize architecture and architecture-review skills without adding enforcement automation.

## Architecture Constraints

- `specs/architecture-package-method.md` is the governing contract and is approved after spec-review.
- The canonical package path remains `docs/architecture/system/architecture.md`.
- Required default diagrams remain Mermaid `.mmd` files under `docs/architecture/system/diagrams/`.
- Each diagram has one authored source file; `.mmd` is specific to default Mermaid diagrams.
- `architecture.md` must reference diagrams by relative links, not embedded Mermaid blocks.
- The first refinement remains review-based and must not add package-shape, C4-file, or ADR-presence enforcement automation.
- Generated `.codex/skills/` and `dist/adapters/` output may be refreshed only through the existing generator when canonical skill guidance changes.

## Context and Scope

This change affects the architecture method's package quality and the skills that author and review that package. It touches the canonical architecture package, default diagrams, focused method spec, proposal lifecycle metadata, and this change-local evidence pack.

Later implementation is expected to touch architecture templates, diagram style scaffolding, architecture skills, generated mirrors/adapters, and a focused test spec. This architecture delta does not implement those later surfaces.

## Solution Strategy

Update the canonical package directly because the proposal's core review target is the current system architecture package. Use this delta to show what this change owns and how the canonical edits map back to the approved spec.

The design uses four refinements:

- C4 diagrams remain Mermaid source but use C4 role styling, technology labels, and intent-labeled relationships.
- Building Block View changes from a flat folder catalog to a Level 1 white-box with one prose Level 2 decomposition for validation and generation scripts.
- Deployment View describes repository execution and publication boundaries instead of repeating every source path.
- Architecture Decisions and Quality Requirements become link-focused and scenario-focused.

No new ADR is required because this change sharpens the accepted architecture package method without changing the durable method decision recorded in `ADR-20260428`.

## Building Block View

| Building block | Responsibility in this change | Canonical target |
| --- | --- | --- |
| Change-local architecture delta | Records this change's architecture ownership and review scope | `docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md` |
| Canonical architecture package | Carries the durable accepted package-quality content after review | `docs/architecture/system/architecture.md` |
| Context diagram | Shows contributors, reviewers, validation execution, Git/PR review, adapter consumers, and the repository as one system | `docs/architecture/system/diagrams/context.mmd` |
| Container diagram | Shows major repository containers with technologies and intent-labeled relationships | `docs/architecture/system/diagrams/container.mmd` |
| Focused method spec | Owns the diagram-source, C4 semantics, skill-content, template, and review-finding contracts | `specs/architecture-package-method.md` |
| Architecture skills | Teach and review the sharpened method during implementation | `skills/architecture/SKILL.md`, `skills/architecture-review/SKILL.md` |
| Templates and diagram styles | Provide scaffolding and shared C4 role classes during implementation | `templates/architecture.md`, `templates/diagram-styles.mmd` |

The validation and generation script container is the only candidate for a later component diagram. It has enough internal structure to warrant component detail if future work changes selector, validator, generator, and CI-wrapper relationships. This refinement does not add that component diagram yet because the updated container view plus Building Block View prose is sufficient for the current change.

## Runtime View

### Architecture refinement flow

1. Spec-review approves the focused spec update.
2. Architecture updates this change-local delta and the canonical package draft.
3. Architecture-review checks C4 semantics, relative diagram links, Building Block View hierarchy, Deployment View boundaries, ADR link focus, quality scenarios, and review-finding contract alignment.
4. Plan defines implementation milestones for templates, skills, generated output, and validation evidence.
5. Implementation updates canonical skills and templates, then refreshes generated output through existing generators when required.
6. Verify proves lifecycle, change metadata, generated drift, and selected checks named by the plan and test spec.

### Diagram review flow

1. Reviewers open `architecture.md`.
2. Section 3 links `diagrams/context.mmd`; Section 5 links `diagrams/container.mmd`.
3. Reviewers inspect `.mmd` source for C4 role classes, technology labels, and intent-labeled relationships.
4. If rendering support is unavailable, source inspection remains sufficient because diagrams are reviewable text.

## Deployment View

This change has no deployed service, database, or runtime infrastructure.

Deployment impact is repository packaging:

- canonical architecture changes remain under `docs/architecture/system/`;
- change-local architecture evidence remains under `docs/changes/2026-04-29-c4-arc42-package-quality/`;
- later template and skill changes remain authored source under `templates/` and `skills/`;
- later generated guidance refreshes, if needed, affect `.codex/skills/` and `dist/adapters/` through existing generators only.

Rollback reverts the proposal/spec lifecycle metadata, canonical architecture edits, diagram source edits, this change-local pack, and any later template, skill, or generated-output changes. No runtime data migration is required.

## Crosscutting Concepts

### Source of Truth

The canonical package remains the long-lived source after review. This delta records the change's design scope and remains historical evidence after accepted content is merged or retained in the canonical package.

### Diagram Source Policy

Each diagram has one authored source file. Default Mermaid diagrams use `.mmd`; other future text-based diagram formats remain allowed only through the focused spec's approved format rules.

### Review Finding Contract

Architecture-review findings use the simple finding, location, severity, and recommendation shape. Material findings also keep the repository-wide evidence, required outcome, and safe resolution or `needs-decision` requirements.

### Generated Output

Canonical skill changes require generated `.codex/skills/` and `dist/adapters/` refresh through existing generators. Generated output is not hand-edited.

## Architecture Decisions

Relevant ADR:

- `docs/adr/ADR-20260428-architecture-package-method.md`

No new ADR is required for this refinement because it clarifies the accepted package method without changing system boundaries, generated packaging ownership, validation architecture, release architecture, or workflow-stage behavior.

## Quality Requirements

| Quality | Scenario | Measure |
| --- | --- | --- |
| Reviewability | A reviewer inspects the package-quality refinement. | C4 diagrams, arc42 section changes, and ADR links are visible as repository text in one diff. |
| C4 clarity | A reviewer opens the context or container diagram source. | People, system, external systems, and containers are distinguishable by role classes; container labels include technologies where relevant. |
| Traceability | Implementation changes skills, templates, or generated output. | Plan, test spec, change metadata, and validation cite the approved spec requirements and this architecture delta. |
| Proportionality | The container view explains current repository containers. | No component diagram is added unless review identifies a concrete unresolved internal-structure question. |
| Material finding safety | Architecture-review records a material finding. | Evidence, required outcome, and safe resolution path or `needs-decision` rationale are present before fixes proceed. |

## Risks and Technical Debt

| Risk | Mitigation |
| --- | --- |
| The canonical package remains in draft too long after architecture-review | Restore status to `approved` only after architecture-review passes. |
| Diagram style conventions are copied inconsistently before `templates/diagram-styles.mmd` exists | Add the shared style template during implementation and keep diagrams aligned with the same class definitions. |
| Skill guidance becomes too verbose | Keep full examples out of `skills/architecture/SKILL.md` and use templates or references for structure and style. |
| Review finding shape loses material-finding safeguards | Keep the simple architecture-review fields additive to the repository-wide material-finding contract. |
| Component diagram is added prematurely | Refine the container view first; add a component diagram only when review identifies an unanswered container-internal question. |

## Glossary

- C4 role class: Mermaid styling class that identifies a node as a person, system, external system, or container.
- diagram-source policy: one authored source file per diagram, linked from `architecture.md`.
- package-quality refinement: this change's focused improvement to the accepted architecture method package, templates, and skills.

## Next artifacts

- Implementation for the package-quality refinement.
- Code-review after implementation completes.

## Follow-on artifacts

- Architecture-review approved this change-local architecture delta and the canonical package update on 2026-04-29 with no findings.
- Plan-review approved `docs/plans/2026-04-29-c4-arc42-package-quality.md` on 2026-04-29 after PR-F1 corrected M5 sequencing.
- Test spec update `specs/architecture-package-method.test.md` is active for R76-R118 and AC14-AC20.

## Readiness

This architecture delta is approved and ready to support implementation. Durable architecture content has been merged into `docs/architecture/system/architecture.md`; this change-local delta remains working and historical evidence for the 2026-04-29 refinement.
