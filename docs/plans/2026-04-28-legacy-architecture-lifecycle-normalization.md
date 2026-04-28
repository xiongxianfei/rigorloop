# Legacy Architecture Lifecycle Normalization Plan

- Status: active
- Owner: maintainers
- Start date: 2026-04-28
- Last updated: 2026-04-28
- Related issue or PR: none yet
- Supersedes: none

## Goal

Normalize legacy architecture artifacts under `docs/architecture/` after adoption of the canonical C4, arc42, and ADR architecture package method.

This plan is the required follow-on artifact for `specs/architecture-package-method.md` R65. It inventories every current file under `docs/architecture/`, classifies each file, records rationale, names a canonical replacement or merge-back target where applicable, and identifies the remaining work needed to complete lifecycle normalization.

This plan does not claim that legacy architecture normalization is complete. It is the starting inventory and routing artifact for that later work.

## Why Now

The architecture package method now defines one canonical architecture package under `docs/architecture/system/`. Existing approved architecture documents predate that lifecycle and may still contain useful historical or current design information. They need explicit classification so contributors do not mistake older change-specific architecture snapshots for the current canonical architecture source.

## Scope

### In Scope

- Inventory every current file from `find docs/architecture -type f | sort`.
- Classify each file as `current canonical content`, `superseded`, `archived/historical snapshot`, or another documented historical status.
- Record rationale for every classification.
- Record canonical replacement or merge-back target where applicable.
- Record follow-up work needed to complete lifecycle normalization.

### Out of Scope

- Rewriting legacy architecture documents in this first follow-on artifact.
- Changing legacy artifact statuses before a normalization review accepts the disposition.
- Adding package-shape, C4-file, or ADR-presence enforcement automation.
- Claiming every legacy architecture artifact has already been normalized.

## Constraints

- `docs/architecture/system/architecture.md` is the current canonical architecture source.
- `docs/architecture/system/diagrams/context.mmd` and `docs/architecture/system/diagrams/container.mmd` are current canonical C4 source diagrams.
- Legacy Markdown files under `docs/architecture/*.md` remain approved historical records until a later normalization pass changes their lifecycle status or records supersession.
- Durable current-system content discovered in a legacy document must merge into the canonical package before downstream work relies on it as current architecture truth.
- Durable decisions discovered in legacy documents must remain linked to existing ADRs or be captured in a new ADR if no suitable ADR exists.

## Inventory Command

The inventory source is:

```sh
find docs/architecture -type f | sort
```

Current output:

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

## Classification Inventory

| Path | Classification | Rationale | Canonical replacement or merge-back target | Remaining follow-up work |
| --- | --- | --- | --- | --- |
| `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md` | archived/historical snapshot | Approved pre-canonical first-release architecture record. It explains the original repository source layout and generated-output boundary, but it is not the current canonical package after `docs/architecture/system/` exists. | `docs/architecture/system/architecture.md` sections 3, 5, 7, and 8; `docs/adr/ADR-20260419-repository-source-layout.md`. | Review for any current source-layout details not yet represented in the canonical package, merge durable current content if needed, then update this artifact with an explicit archived or superseded disposition. |
| `docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md` | archived/historical snapshot | Approved change-specific design for artifact lifecycle ownership before the canonical package lifecycle. It remains useful history for validator and lifecycle decisions but is not the current architecture baseline. | `docs/architecture/system/architecture.md` sections 5, 6, and 8; related lifecycle specs and validator scripts. | Extract any still-current lifecycle architecture rules missing from the canonical package, decide whether an ADR is needed for durable lifecycle-validator architecture, then record final archived or superseded status. |
| `docs/architecture/2026-04-21-docs-changes-usage-policy.md` | archived/historical snapshot | Approved change-specific design for `docs/changes/` usage. The canonical package now owns current repository architecture, while this file preserves the historical design rationale for the docs-changes policy. | `docs/architecture/system/architecture.md` sections 5, 6, and 8; `specs/docs-changes-usage-policy.md`. | Check whether current change-local artifact rules are fully represented in canonical architecture and workflow guidance, then mark the legacy document archived or superseded. |
| `docs/architecture/2026-04-21-workflow-stage-autoprogression.md` | archived/historical snapshot | Approved architecture record for a prior workflow-stage change. It predates the canonical package and should not be treated as the current system architecture source. | `docs/architecture/system/architecture.md` sections 5, 6, and 8; `specs/workflow-stage-autoprogression.md`; `specs/rigorloop-workflow.md`. | Confirm active autoprogression boundaries are represented in canonical architecture and workflow specs, then archive or supersede this file with explicit replacement text. |
| `docs/architecture/2026-04-24-multi-agent-adapter-distribution.md` | archived/historical snapshot | Approved adapter distribution architecture created before the canonical package. It remains historical evidence for adapter packaging and generated-output decisions but is not the current canonical architecture package. | `docs/architecture/system/architecture.md` sections 5, 7, and 8; `docs/adr/ADR-20260424-generated-adapter-packages.md`. | Compare adapter packaging details against the canonical Deployment View and generated-output sections, merge any missing current content, then record final archived or superseded status. |
| `docs/architecture/2026-04-24-review-finding-resolution-contract.md` | archived/historical snapshot | Approved change-specific design for review finding resolution. It is historical evidence for review artifact structure and closeout rules, while current system architecture now belongs in the canonical package. | `docs/architecture/system/architecture.md` sections 5, 6, and 8; `specs/review-finding-resolution-contract.md`. | Review whether review artifact boundaries and closeout flow are represented in canonical architecture, then mark this document archived or superseded. |
| `docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md` | archived/historical snapshot | Approved architecture for adapter command aliases and invocation surfaces. It predates canonical architecture and remains historical design evidence for adapter release behavior. | `docs/architecture/system/architecture.md` sections 5, 7, and 8; `docs/adr/ADR-20260424-generated-adapter-packages.md`. | Merge any still-current command-alias packaging details into the canonical Deployment View if absent, then record final archived or superseded status. |
| `docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md` | archived/historical snapshot | Approved design for validation selector and CI layering before canonical architecture adoption. It remains historical evidence for validation architecture but is not the current canonical package. | `docs/architecture/system/architecture.md` sections 5, 6, and 8; `specs/test-layering-and-change-scoped-validation.md`. | Check selector and CI layering against canonical validation flow, merge missing durable content, then archive or supersede the legacy document. |
| `docs/architecture/system/architecture.md` | current canonical content | This file is the canonical architecture package created by the C4, arc42, and ADR method rollout. | Self; change-local deltas merge accepted durable content here. | Keep updated for architecture-significant changes; normalize legacy content into this package where still current. |
| `docs/architecture/system/diagrams/container.mmd` | current canonical content | This Mermaid source-text C4 container diagram is part of the default canonical architecture package. | Self; referenced by `docs/architecture/system/architecture.md`. | Keep synchronized with canonical Building Block View and generated-output/container boundary changes. |
| `docs/architecture/system/diagrams/context.mmd` | current canonical content | This Mermaid source-text C4 system context diagram is part of the default canonical architecture package. | Self; referenced by `docs/architecture/system/architecture.md`. | Keep synchronized when external actors, systems, or repository context changes. |

## Milestones

1. M1. Review legacy Markdown records for current durable content
   - Compare each `docs/architecture/*.md` legacy record with the canonical package.
   - Merge still-current architecture truth into `docs/architecture/system/architecture.md`.
   - Identify any durable decisions that need new or updated ADR links.
   - verification: updated canonical package diff and lifecycle validation for touched architecture and ADR artifacts.
   - milestone commit message: `M1: merge legacy architecture content into canonical package`
   - milestone closeout checklist:
     - [ ] targeted validation passed
     - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
     - [ ] progress updated
     - [ ] decision log updated if needed
     - [ ] validation notes updated
     - [ ] milestone committed

2. M2. Normalize legacy lifecycle disposition
   - Update each legacy architecture record with an accepted disposition: `superseded`, `archived`, or another approved historical state.
   - Add replacement pointers or archive rationale where required by lifecycle policy.
   - verification: artifact lifecycle validation for every touched legacy architecture document and the canonical package.
   - milestone commit message: `M2: normalize legacy architecture lifecycle status`
   - milestone closeout checklist:
     - [ ] targeted validation passed
     - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
     - [ ] progress updated
     - [ ] decision log updated if needed
     - [ ] validation notes updated
     - [ ] milestone committed

3. M3. Close normalization evidence
   - Re-run `find docs/architecture -type f | sort` and compare every path with this inventory.
   - Confirm repository guidance no longer overstates legacy normalization.
   - Update this plan and `docs/plan.md` with final lifecycle state.
   - verification: lifecycle validation, broad smoke when triggered, and manual inventory comparison.
   - milestone commit message: `M3: close legacy architecture normalization`
   - milestone closeout checklist:
     - [ ] targeted validation passed
     - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
     - [ ] progress updated
     - [ ] decision log updated if needed
     - [ ] validation notes updated
     - [ ] milestone committed

## Progress

- 2026-04-28: plan created as the required follow-on artifact from the architecture package method rollout.
- 2026-04-28: inventoried 11 current files under `docs/architecture/`.
- 2026-04-28: classified the canonical package and diagrams as `current canonical content`.
- 2026-04-28: classified the eight pre-canonical architecture Markdown records as `archived/historical snapshot` pending a later normalization pass that merges current content and records final lifecycle disposition.

## Decision Log

- 2026-04-28: kept this artifact as a follow-on plan rather than editing every legacy architecture document immediately because `specs/architecture-package-method.md` R64 explicitly avoids immediate full migration during first implementation.
- 2026-04-28: classified legacy Markdown architecture records as `archived/historical snapshot` instead of `superseded` because the repository still needs a normalization review to decide which records require explicit supersession pointers versus archive-only rationale.
- 2026-04-28: classified the two `.mmd` files as `current canonical content` because they are required C4 source-text diagrams for the canonical package, not historical records.

## Surprises and Discoveries

- The current `docs/architecture/` tree includes Mermaid source diagrams as files that must be listed by the inventory proof.
- Legacy architecture records are all Markdown files at the top of `docs/architecture/`; the new canonical package is the only subdirectory-based architecture package today.

## Validation Notes

- 2026-04-28: `find docs/architecture -type f | sort` produced 11 paths, all listed in this plan's inventory.
- 2026-04-28: `while IFS= read -r path; do rg -F -q "$path" docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md || printf 'missing %s\n' "$path"; done < <(find docs/architecture -type f | sort)` produced no output, proving every current architecture path appears in this plan.
- 2026-04-28: `python scripts/select-validation.py --mode explicit --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/plan.md` returned `status: ok` and selected `artifact_lifecycle.validate`.
- 2026-04-28: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/plan.md` passed with `validated 0 artifact files`.

## Outcome and Retrospective

- This follow-on plan is active. Legacy normalization has not yet been executed.
- The repository must continue to avoid claiming that all legacy architecture artifacts have already been normalized until this plan is completed.

## Readiness

- Ready for future implementation of M1, `Review legacy Markdown records for current durable content`, after the C4, arc42, and ADR method rollout is reviewed and verified.

## Risks and Follow-Ups

- Risk: contributors may still cite an older architecture snapshot as current architecture truth.
  Mitigation: use `docs/architecture/system/architecture.md` as the canonical package and this plan as the legacy classification map until normalization completes.
- Risk: archiving legacy records without content review could lose current architecture details.
  Mitigation: M1 requires comparison and merge-back before any final lifecycle disposition.
