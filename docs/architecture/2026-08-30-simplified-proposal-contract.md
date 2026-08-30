# Simplified Proposal Contract Architecture

## Owning change record

- `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/change.yaml`

## Related artifacts

- Proposal: `docs/proposals/2026-08-30-simplify-rigorloop-proposal-contract.md`
- Specification: `specs/simplified-proposal-contract.md`
- Plan: None yet.
- ADRs: None. The change narrows one existing artifact contract without introducing a new long-lived component or cross-system mechanism.

## Introduction and Goals

This design makes a proposal a direction-only Markdown artifact while preserving lifecycle ownership, vision alignment, independent review, and historical compatibility. It removes repeated metadata and downstream design content from proposals without weakening the traceable path from proposal to Design.

The design affects proposal authoring and review, proposal-specific lifecycle validation, workflow guidance, canonical templates and references, and generated adapter release surfaces.

## Architecture Constraints

- `change.yaml` remains the sole mutable lifecycle state and ownership record for a governed proposal.
- Proposal Markdown must remain meaningful without a change record so that portable drafting stays possible.
- Proposal Review remains independent from proposal authorship.
- Historical settled proposals remain readable without per-document version markers or migration rewrites.
- Architecture, specification, plan, and test-specification lifecycle contracts are unchanged.
- Canonical skills remain authored under `skills/`; generated adapter release output is derived rather than hand-edited.

## Context and Scope

The affected flow is:

```text
proposal author
  -> seven-section proposal
  -> Proposal Review reads proposal + VISION.md
  -> review evidence records alignment and decision
  -> change.yaml references the proposal when governed
  -> Design consumes the accepted direction
```

The proposal contains stable decision content only. Proposal Review owns judgment. `change.yaml` owns governed identity, lifecycle state, and the link to the proposal. Validators check structure but do not invent proposal meaning or vision judgment.

A separate C4 diagram is not justified because the change does not add a runtime component, deployment unit, or external integration.

## Solution Strategy

Use one canonical contract across skill guidance, templates, review criteria, and repository validation:

1. Author exactly seven required level-two sections, with one optional impact section.
2. Keep lifecycle status and ownership out of proposal Markdown.
3. Store the proposal path and mutable state only in the governing `change.yaml` entry.
4. Have Proposal Review compare the proposal with `VISION.md` and record a concise alignment result in review evidence.
5. Accept both historical and simplified proposal shapes in compatibility-aware repository scans; require the simplified shape through current authoring, review, and changed-proposal validation paths after cutover.
6. Update canonical sources first, then regenerate and validate adapter release artifacts through existing tooling.

This avoids a proposal schema marker, content hash, reverse ownership pointer, compatibility interpreter, or new lifecycle command.

## Building Block View

| Building block | Responsibility | Change |
| --- | --- | --- |
| `skills/proposal` | Author proposal content | Emit only the simplified proposal contract and proportional feasibility. |
| `skills/proposal-review` | Decide direction sufficiency | Review vision alignment, feasibility, bounds, impact, and downstream deferral without demanding design detail. |
| Proposal templates and references | Reusable structure and examples | Provide seven required sections plus the conditional impact section. |
| Proposal lifecycle validator | Structural compatibility | Recognize simplified proposals without requiring embedded status, reverse ownership, or routine vision metadata. |
| `change.yaml` | Governed proposal ownership and state | Continue to reference the proposal path and own mutable lifecycle state. No new field is required. |
| Workflow and constitutional guidance | Repository policy | Remove obsolete proposal-section requirements and state the new review-owned vision rule. |
| Adapter build and release validation | Published projection | Generate and verify the revised skills from canonical sources. |

No new shared runtime service, storage system, command, or adapter-specific authored implementation is introduced.

## Runtime View

### Portable proposal

The proposal skill writes a proposal with the seven required sections and, when material, the optional impact section. No `change.yaml`, status, ownership pointer, or ordinary vision field is required. The invocation stops at a review-ready artifact.

### Governed proposal

Workflow creates or selects a change record and stores the proposal path in the primary proposal entry. Lifecycle state changes only through the existing governed lifecycle boundary. The proposal file is not rewritten to add reverse metadata.

### Proposal Review

The reviewer reads the complete proposal and current `VISION.md`. Review evidence records one concise alignment outcome. Ordinary alignment permits normal decision review. A conflict, revision request, or missing-vision bootstrap condition must be visible in the proposal when it could affect approval; otherwise review blocks or requests revision.

### Design handoff

An approved review authorizes architecture and specification work with the accepted challenge, goals, bounds, governing principle, direction, feasibility constraints, material impacts, and any material vision decision. It does not preselect detailed behavior or technical design.

### Failure behavior

- A missing required section or unexpected level-two proposal section fails current-contract structural validation.
- Missing or inadequate feasibility fails Proposal Review.
- Routine absence of `Vision fit`, `Status`, or `Owning change record` does not fail a simplified proposal.
- A material vision conflict not disclosed by the proposal prevents approval.
- A legacy settled proposal remains readable; touching it does not silently rewrite historical evidence.

## Deployment View

The change ships through the existing repository, package build, adapter generation, release archive, and validation paths. It introduces no service deployment, data migration job, feature flag, or new CLI command.

Cutover is one coordinated repository change: canonical skills, templates, governance, workflow guidance, validators, tests, and generated release inputs change together. Release archives are regenerated through existing release tooling.

## Crosscutting Concepts

### Source ownership

`skills/` remains the authored skill source. Proposal Markdown owns direction content, Proposal Review owns judgment, and `change.yaml` owns governed state and ownership.

### Structural validation

Validation checks headings, order, duplicates, forbidden legacy metadata in the simplified form, and presence of a non-empty feasibility assessment. Semantic quality remains review-owned.

Compatibility-aware repository scans may accept untouched historical shapes. Current authoring and review paths require the simplified contract after cutover. No per-document contract version or content hash is introduced.

### Vision alignment

Proposal Review records one of four outcomes: `aligned`, `material-conflict`, `vision-revision-requested`, or `no-vision-bootstrap`. Only `aligned`, or an explicitly owner-resolved exceptional outcome, can support approval.

### Adapter consistency

Canonical source changes flow through existing generator and release checks. Repository-local installed copies and generated archives are never treated as authored truth.

### Observability

Failures name the missing, duplicated, misordered, or forbidden section and the owning correction stage. Review results state alignment, findings, approval authority, and the next owner without exposing internal generation mechanics in public skill text.

## Architecture Decisions

No ADR is required. The proposal already selects the durable direction, and this architecture applies it within existing proposal, review, validation, and change-record boundaries without adding a new component or irreversible platform mechanism.

The principal decisions are:

- proposal content and lifecycle metadata are one-way linked from `change.yaml` to proposal;
- ordinary vision alignment is review evidence, not proposal content;
- compatibility uses existing historical readability plus current-path enforcement, not document versioning;
- no CLI command or lifecycle field is added.

## Quality Requirements

| Quality | Scenario | Measure |
| --- | --- | --- |
| Concision | A developer opens a new proposal. | Only seven required level-two sections appear, plus impact when material. |
| Traceability | A governed proposal is reviewed and handed to Design. | `change.yaml` identifies the proposal and review evidence records the decision and vision alignment. |
| Compatibility | Repository validation encounters an untouched settled historical proposal. | Historical evidence remains readable without migration or a new marker. |
| Consistency | Canonical skills change for a release. | Existing generation and adapter validation report no drift. |
| Review authority | Proposal content conflicts materially with project vision. | Proposal Review withholds approval until the conflict or revision request is explicit and owner-resolved. |

## Risks and Technical Debt

- Compatibility-aware validation can become too permissive if current authoring paths are not tested separately. Mitigation: keep focused fixtures for new simplified, invalid simplified, and untouched historical proposals.
- Moving routine vision alignment to review evidence makes review recording more important. Mitigation: require the concise alignment outcome in Proposal Review results and receipts.
- Existing installed runtime skills may lag canonical sources during development. Mitigation: validate canonical packages and regenerate supported release artifacts before cutover.

No rollback-specific state or compatibility version is introduced. A defect is corrected forward by revising canonical sources and regenerated outputs.

## Glossary

- **Simplified proposal**: a proposal containing seven required decision sections and an optional material-impact section.
- **Portable proposal**: a proposal not yet referenced by a governed change record.
- **Governed proposal**: a proposal referenced by the primary proposal entry in `change.yaml`.
- **Routine vision alignment**: a Proposal Review judgment that the direction fits current vision and needs no proposal-level exception decision.
- **Cutover**: the coordinated repository and release point after which current authoring and review use the simplified contract.

## Next artifacts

- `specs/simplified-proposal-contract.md`
- Design Review over the reconciled architecture and specification package.

## Follow-on artifacts

- None yet.

## Readiness

Ready for specification reconciliation. Design Review must assess the final architecture and specification together before Delivery planning.
