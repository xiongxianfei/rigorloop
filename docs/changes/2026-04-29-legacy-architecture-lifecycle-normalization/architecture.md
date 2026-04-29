# Legacy Architecture Lifecycle Normalization Architecture Delta

## Status

- active

This is change-local working architecture for `2026-04-29-legacy-architecture-lifecycle-normalization`. It is not the canonical architecture package. Durable current architecture content accepted during this change must merge into `docs/architecture/system/architecture.md`; after merge-back, this file remains historical evidence only.

## Related Artifacts

- Governing spec: `specs/architecture-package-method.md`
- Active plan: `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
- Active test spec: `specs/legacy-architecture-lifecycle-normalization.test.md`
- Canonical architecture package: `docs/architecture/system/architecture.md`
- Architecture method ADR: `docs/adr/ADR-20260428-architecture-package-method.md`
- Change metadata: `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`

## Introduction and Goals

This delta is the working architecture surface for normalizing pre-canonical architecture documents under `docs/architecture/`.

Goals:

- keep one canonical architecture source under `docs/architecture/system/`;
- compare legacy architecture records before changing their lifecycle state;
- merge any accepted current architecture truth into the canonical package;
- preserve durable decisions through ADR links or new ADRs when required;
- leave legacy records as historical evidence with explicit lifecycle disposition.

## Architecture Constraints

- The canonical architecture package remains `docs/architecture/system/architecture.md`.
- Legacy Markdown records under `docs/architecture/*.md` must not be archived or superseded until comparison and merge-back decisions are recorded.
- Historical body content in legacy records must remain intact except for lifecycle metadata, replacement pointers, archive rationale, and concise disposition notes.
- Selector routing for architecture support paths may use existing non-enforcement checks only; this change must not add package-shape, C4-file, or ADR-presence enforcement.
- M0 creates routing and working evidence only. It must not modify legacy architecture statuses.

## Context and Scope

The current architecture inventory contains one canonical package under `docs/architecture/system/`, two canonical Mermaid diagram sources, and eight top-level legacy Markdown architecture records.

The legacy records may contain:

- durable current architecture details that should merge into the canonical package;
- historical rationale that should remain as archive evidence;
- durable decisions already represented by ADRs;
- durable decisions that require a new ADR or explicit no-ADR rationale.

## M1 Inventory Refresh and Comparison Basis

The M1 inventory source is:

```sh
find docs/architecture -type f | sort
```

The current inventory contains 11 files:

```text
docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md
docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md
docs/architecture/2026-04-21-docs-changes-usage-policy.md
docs/architecture/2026-04-21-workflow-stage-autoprogression.md
docs/architecture/2026-04-24-multi-agent-adapter-distribution.md
docs/architecture/2026-04-24-review-finding-resolution-contract.md
docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md
docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md
docs/architecture/system/architecture.md
docs/architecture/system/diagrams/container.mmd
docs/architecture/system/diagrams/context.mmd
```

The canonical package files are already represented in the active plan as current canonical content. M1 adds the top-level legacy Markdown comparison basis below so M2 can compare by domain without guessing which files are in scope.

| Legacy architecture record | M1 comparison group | May contain current canonical content | Historical-only rationale to preserve | Durable decision / ADR review | M1 status |
| --- | --- | --- | --- | --- | --- |
| `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md` | source layout / generated boundary | Yes: source layout, canonical-source boundaries, generated-output boundaries | First-release repository architecture rationale | Check existing `docs/adr/ADR-20260419-repository-source-layout.md` coverage | pending M2 comparison |
| `docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md` | workflow / lifecycle / validation | Yes: lifecycle ownership, validator boundaries, artifact status rules | Original lifecycle ownership design rationale | Decide whether lifecycle-validator architecture needs ADR coverage | pending M2 comparison |
| `docs/architecture/2026-04-21-docs-changes-usage-policy.md` | workflow / change-local artifacts | Yes: `docs/changes/` ownership and change-local artifact boundaries | Historical docs-changes policy design rationale | Check whether change-local artifact policy is already ADR-covered or spec-only | pending M2 comparison |
| `docs/architecture/2026-04-21-workflow-stage-autoprogression.md` | workflow / stage routing | Yes: autoprogression boundaries and stage handoff behavior | Historical workflow-stage design rationale | Check whether durable workflow-stage decisions need ADR links | pending M2 comparison |
| `docs/architecture/2026-04-24-multi-agent-adapter-distribution.md` | adapters / generated output / release | Yes: adapter packaging, generated output, release boundary details | Historical adapter-distribution design rationale | Check existing `docs/adr/ADR-20260424-generated-adapter-packages.md` coverage | pending M2 comparison |
| `docs/architecture/2026-04-24-review-finding-resolution-contract.md` | review / lifecycle / workflow | Yes: review artifact boundaries and closeout flow | Historical review-resolution contract rationale | Check whether durable review-artifact decisions need ADR coverage | pending M2 comparison |
| `docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md` | adapters / invocation surface | Yes: adapter command alias and invocation surface details | Historical command-surface design rationale | Check existing generated-adapter ADR coverage | pending M2 comparison |
| `docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md` | validation / CI / selector routing | Yes: selector routing, CI wrapper, validation layering | Historical validation-layering design rationale | Check whether durable selector/CI architecture needs ADR coverage | pending M2 comparison |

M1 does not decide final disposition, merge-back content, or ADR creation. It only records a complete comparison basis for M2.

## Solution Strategy

Normalize in a sequence that prevents data loss:

1. Create this change-local pack and active proof map.
2. Refresh inventory and prepare a comparison matrix.
3. Compare legacy records by domain.
4. Merge accepted current content into the canonical package.
5. Add ADR links or new ADRs when durable decisions require them.
6. Update legacy documents with final historical lifecycle disposition.
7. Close with final validation for the canonical package and every changed legacy record.

## Building Block View

| Building block | Responsibility | M0 state |
| --- | --- | --- |
| `docs/architecture/system/architecture.md` | Canonical architecture source of truth | unchanged |
| `docs/architecture/system/diagrams/*.mmd` | Canonical C4 diagram sources | unchanged |
| `docs/architecture/*.md` | Legacy architecture records to compare and later normalize | unchanged |
| `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md` | Working comparison and merge-back evidence for this change | created |
| `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml` | Change metadata and validation routing | created |
| `specs/legacy-architecture-lifecycle-normalization.test.md` | Focused proof map for this follow-on | active |

## Runtime View

### M0 routing flow

1. Contributor or agent reads the approved plan and active test spec.
2. M0 creates `change.yaml` and this change-local architecture delta.
3. Selector inspection classifies the change-local pack and test spec.
4. Change metadata and artifact lifecycle validation prove the new routing surfaces are acceptable.
5. No legacy architecture statuses or canonical architecture content change in M0.

### Later normalization flow

1. M1 refreshes inventory and comparison structure.
2. M2 records domain-level merge-back and disposition recommendations.
3. M3 updates canonical current architecture truth.
4. M4 updates legacy lifecycle dispositions.
5. M5 proves canonical freshness and every changed legacy document's final lifecycle state.

## Deployment View

Not applicable. This change modifies repository architecture artifacts only. It has no deployed service, runtime infrastructure, database, or release package impact in M0.

## Crosscutting Concepts

### Source of Truth

`docs/architecture/system/architecture.md` remains the canonical architecture package. This file is a temporary working delta and must not become a competing canonical source.

### Lifecycle Ordering

Legacy records remain unchanged in M0. Final legacy lifecycle status changes are deferred until after comparison and canonical merge-back decisions.

### Validation Boundary

M0 validation uses existing selector, change metadata, artifact lifecycle, and whitespace checks. It does not add or require new architecture package enforcement.

## Architecture Decisions

No new ADR is required for M0. The governing architecture method decision remains `docs/adr/ADR-20260428-architecture-package-method.md`.

Later milestones must add or link ADRs if domain comparison finds durable architecture decisions not already represented.

## Quality Requirements

| Quality | M0 expectation |
| --- | --- |
| Traceability | Change metadata links the spec, plan, test spec, ADR, and this working delta. |
| Reviewability | The working delta states scope, sequencing, and non-canonical status clearly. |
| Safety | Legacy records and canonical architecture content remain unchanged in M0. |
| Determinism | M0 uses repo-owned validation commands only. |

## Risks and Technical Debt

| Risk | Mitigation |
| --- | --- |
| Change-local delta is mistaken for canonical architecture | The status note and source-of-truth sections identify it as working evidence only. |
| Legacy status changes happen too early | M0 explicitly excludes legacy architecture status edits. |
| Later comparison misses a legacy record | M1 must refresh inventory and add one comparison row per top-level legacy Markdown record. |

## Glossary

- canonical architecture package: the current architecture source under `docs/architecture/system/`.
- change-local architecture delta: working architecture evidence under `docs/changes/<change-id>/`.
- legacy architecture record: a top-level `docs/architecture/*.md` architecture document created before the canonical package lifecycle.
- merge-back: moving accepted current architecture truth into the canonical package.

## M0 Evidence

- Same-slice requirements: `R63`-`R66`, `R73`-`R75`.
- Same-slice tests: `T1`.
- Legacy architecture status edits: none in M0.
- Canonical architecture edits: none in M0.
- Durable Markdown reasoning: this architecture delta is the M0 durable reasoning surface; `explain-change.md` is planned for M5 closeout.

## M1 Evidence

- Same-slice requirements: `R63`-`R66`, `R73`-`R75`.
- Same-slice tests: `T2`.
- Inventory source: `find docs/architecture -type f | sort`.
- Inventory count: 11 files.
- Top-level legacy Markdown comparison rows: 8.
- Legacy architecture status edits: none in M1.
- Canonical architecture edits: none in M1.
- M2 dependency: domain comparison must decide merge-back candidates, ADR needs, and final disposition recommendations.

## Next Artifacts

- M2 domain comparison after M1.

## Follow-on Artifacts

- None yet.

## Readiness

This change-local architecture delta is ready for M0 validation. It becomes the working comparison surface for M1 after M0 validation passes.
