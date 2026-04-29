# Legacy Architecture Lifecycle Normalization Plan

- Status: active
- Owner: maintainers
- Start date: 2026-04-28
- Last updated: 2026-04-29
- Related issue or PR: none yet
- Supersedes: none

## Goal

Normalize legacy architecture artifacts under `docs/architecture/` after adoption of the canonical C4, arc42, and ADR architecture package method.

This plan is the required follow-on artifact for `specs/architecture-package-method.md` R65. It inventories every current file under `docs/architecture/`, classifies each file, records rationale, names a canonical replacement or merge-back target where applicable, and identifies the remaining work needed to complete lifecycle normalization.

This plan does not claim that legacy architecture normalization is complete. It is the starting inventory and routing artifact for that later work.

## Why Now

The architecture package method now defines one canonical architecture package under `docs/architecture/system/`. Existing approved architecture documents predate that lifecycle and may still contain useful historical or current design information. They need explicit classification so contributors do not mistake older change-specific architecture snapshots for the current canonical architecture source.

## Source Artifacts

- Governing spec: `specs/architecture-package-method.md`, especially `R63`-`R66` and `R72`.
- Existing test spec: `specs/architecture-package-method.test.md`, especially `T9`, `T12`, `T13`, and `T15`.
- Focused test spec: `specs/legacy-architecture-lifecycle-normalization.test.md`.
- Canonical architecture package: `docs/architecture/system/architecture.md`.
- Architecture method ADR: `docs/adr/ADR-20260428-architecture-package-method.md`.
- Plan index: `docs/plan.md`.
- Planned change-local pack:
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/explain-change.md`

## Requirements Covered

| Requirement IDs | Plan coverage |
| --- | --- |
| `R63`-`R66` | Inventory, comparison, canonical merge-back, and final legacy lifecycle disposition |
| `R37`-`R39` | Merge durable current architecture truth into the canonical package before legacy records stop acting as current sources |
| `R44`-`R48` | Identify durable decisions in legacy architecture records and add or link ADRs when needed |
| `R67`-`R72` | Keep normalization review-based; selector routing may be used only as non-enforcement CI routing |
| `R73`-`R75` | Keep touched architecture artifacts publishable, readable, and free of secrets |

## Scope

### In Scope

- Inventory every current file from `find docs/architecture -type f | sort`.
- Classify each file as `current canonical content`, `superseded`, `archived/historical snapshot`, or another documented historical status.
- Record rationale for every classification.
- Record canonical replacement or merge-back target where applicable.
- Review legacy Markdown records for durable current architecture content and durable decisions.
- Merge accepted current architecture truth into the canonical architecture package.
- Update legacy lifecycle dispositions after content review and merge-back decisions are complete.
- Record follow-up work needed after lifecycle normalization, if any.

### Out of Scope

- Rewriting historical legacy architecture body content beyond concise lifecycle disposition notes and replacement pointers.
- Changing legacy artifact statuses before comparison, merge-back review, and disposition decisions are recorded.
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

0. M0. Create change-local pack and test-spec routing
   - Goal: establish the baseline change-local evidence pack and focused test-spec route before touching legacy architecture content.
   - Requirements: `R63`-`R66`, `R73`-`R75`.
   - Files/components likely touched:
     - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
     - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
     - `specs/legacy-architecture-lifecycle-normalization.test.md`
     - this plan
   - Dependencies: PR #20 merged and local `main` synchronized with `origin/main`.
   - Tests to add/update:
     - focused test spec mapping legacy normalization requirements, examples, edge cases, manual comparison proof, lifecycle validation, and final closeout proof.
   - Implementation steps:
     - Create `change.yaml` with proposal/spec/architecture/plan/test-spec references, requirements, planned tests, changed-file tracking, and validation entries.
     - Create the change-local architecture delta as the working comparison surface for legacy architecture normalization.
     - Use the active `specs/legacy-architecture-lifecycle-normalization.test.md` proof map instead of overloading the completed architecture-method test spec.
     - Keep this milestone free of legacy lifecycle status changes.
   - Validation commands:
     - `python scripts/select-validation.py --mode explicit --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path specs/legacy-architecture-lifecycle-normalization.test.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
     - `python scripts/validate-change-metadata.py docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
     - `python scripts/test-change-metadata-validator.py`
     - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path specs/legacy-architecture-lifecycle-normalization.test.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/plan.md`
     - `git diff --check -- docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization specs/legacy-architecture-lifecycle-normalization.test.md docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
   - Expected observable result: a routed change-local pack and test spec exist before legacy architecture files are modified.
   - milestone commit message: `M0: add legacy architecture normalization test routing`
   - milestone closeout checklist:
     - [x] targeted validation passed
     - [x] lifecycle state unchanged; no `docs/plan.md` update required
     - [x] progress updated
     - [x] decision log updated
     - [x] validation notes updated
     - [x] milestone committed

1. M1. Refresh inventory and comparison basis
   - Goal: re-establish the architecture inventory from the current tree and prepare a comparison matrix without changing canonical architecture truth yet.
   - Requirements: `R63`-`R66`, `R73`-`R75`.
   - Files/components likely touched:
     - `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
     - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
     - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
   - Dependencies: M0 complete.
   - Tests to add/update:
     - test-spec inventory proof entry that every current architecture path is present in the plan inventory and comparison surface.
   - Implementation steps:
     - Re-run the inventory command and update the inventory if the tree changed.
     - Add a comparison matrix to the change-local architecture delta with one row per legacy Markdown record.
     - Record for each row whether the legacy document may contain current canonical content, historical-only rationale, or durable decision material needing ADR review.
     - Do not edit legacy document statuses or the canonical package in this milestone.
   - Validation commands:
     - `find docs/architecture -type f | sort`
     - `while IFS= read -r path; do rg -F -q "$path" docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md || printf 'missing-from-plan %s\n' "$path"; done < <(find docs/architecture -type f | sort)`
     - `while IFS= read -r path; do rg -F -q "$path" docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md || printf 'missing-from-delta %s\n' "$path"; done < <(find docs/architecture -maxdepth 1 -type f -name '*.md' | sort)`
     - `python scripts/select-validation.py --mode explicit --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
     - `python scripts/validate-change-metadata.py docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
     - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
     - `git diff --check -- docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization`
   - Expected observable result: current inventory and comparison evidence are complete before domain-level review starts.
   - milestone commit message: `M1: refresh legacy architecture inventory`
   - milestone closeout checklist:
     - [ ] targeted validation passed
     - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
     - [ ] progress updated
     - [ ] decision log updated if needed
     - [ ] validation notes updated
     - [ ] milestone committed

2. M2. Compare legacy architecture records by domain
   - Goal: review legacy records in smaller domain groups and decide what durable current content or decisions must merge back.
   - Requirements: `R37`-`R39`, `R44`-`R48`, `R63`-`R66`, `R73`-`R75`.
   - Files/components likely touched:
     - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
     - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
     - this plan
   - Dependencies: M1 complete.
   - Tests to add/update:
     - test-spec domain comparison cases for source layout/generated boundaries, workflow/lifecycle/review, and validation/CI.
   - Implementation steps:
     - Compare source layout and generated-output boundary records:
       - `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md`
       - `docs/architecture/2026-04-24-multi-agent-adapter-distribution.md`
       - `docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md`
     - Compare workflow, lifecycle, and review records:
       - `docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md`
       - `docs/architecture/2026-04-21-docs-changes-usage-policy.md`
       - `docs/architecture/2026-04-21-workflow-stage-autoprogression.md`
       - `docs/architecture/2026-04-24-review-finding-resolution-contract.md`
     - Compare validation and CI records:
       - `docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md`
       - current selector routing behavior from `scripts/validation_selection.py`
     - For each domain group, record merge-back candidates, historical-only content, ADR links needed, and final disposition recommendation.
     - Do not edit canonical architecture or legacy lifecycle statuses in this milestone.
   - Validation commands:
     - `rg -n "source layout|generated|adapter|workflow|lifecycle|review|validation|selector|CI|ADR|merge-back|historical-only" docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
     - `python scripts/select-validation.py --mode explicit --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
     - `python scripts/validate-change-metadata.py docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
     - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
     - `git diff --check -- docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
   - Expected observable result: the branch has reviewable evidence for what will and will not be merged into the canonical package.
   - milestone commit message: `M2: compare legacy architecture domains`
   - milestone closeout checklist:
     - [ ] targeted validation passed
     - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
     - [ ] progress updated
     - [ ] decision log updated if needed
     - [ ] validation notes updated
     - [ ] milestone committed

3. M3. Merge current architecture truth into the canonical package
   - Goal: update the canonical architecture package with accepted current content from the domain comparison, sweep stale canonical current-state references, and correct known stale selector-routing wording.
   - Requirements: `R37`-`R39`, `R44`-`R48`, `R63`-`R66`, `R72`-`R75`.
   - Files/components likely touched:
     - `docs/architecture/system/architecture.md`
     - `docs/architecture/system/diagrams/context.mmd` if context changed
     - `docs/architecture/system/diagrams/container.mmd` if container boundaries changed
     - `docs/adr/` only if a new durable decision is required
     - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
     - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
     - this plan
   - Dependencies: M2 complete and domain comparison accepted.
   - Tests to add/update:
     - test-spec canonical merge-back case proving accepted durable content is represented in the canonical package.
     - test-spec canonical current-state sweep case proving Related artifacts, Next artifacts, Readiness, completed-plan references, old milestone references, and selector-routing wording are no longer stale.
     - test-spec stale-selector-routing case proving the canonical Runtime View no longer says `.mmd` diagrams and change-local architecture deltas are manual-routed when selector routing now exists.
   - Implementation steps:
     - Merge accepted current content into the affected arc42 sections of `docs/architecture/system/architecture.md`.
     - Add or update ADR links in section 9 when durable decisions are discovered.
     - Update C4 diagrams only when a domain comparison changes context or container boundaries.
     - Sweep `docs/architecture/system/architecture.md` canonical current-state text, including Related artifacts, Next artifacts, Readiness, completed-plan references, old milestone references, and stale selector-routing wording.
     - Named task: update the stale selector-routing architecture wording in the canonical Runtime View / Validation flow so it reflects current selector behavior: architecture diagram source files and change-local architecture deltas route to existing non-enforcement lifecycle or regression checks, while diagram sufficiency and package completeness remain manual review evidence.
     - Record in the change-local architecture delta which legacy content was merged and which content was intentionally left historical.
   - Validation commands:
     - `python scripts/select-validation.py --mode explicit --path docs/architecture/system/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
     - `bash scripts/ci.sh --mode explicit --path docs/architecture/system/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
     - `python scripts/validate-change-metadata.py docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
     - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/architecture/system/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
     - `rg -n "manual-routed|selector routing|non-enforcement|change-local architecture|\\.mmd" docs/architecture/system/architecture.md docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
     - `python -c 'from pathlib import Path; bt=chr(96); text=Path("docs/architecture/system/architecture.md").read_text(); stale=[p for p in ("docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md", "M3 "+bt+"code-review"+bt, "M3 "+bt+"verify"+bt, "M4 skill and generated-output update", "M5 legacy architecture normalization follow-on artifact before final completion claims", "diagrams and change-local architecture deltas remain manual-routed review evidence in the first adoption slice") if p in text]; assert not stale, stale'`
     - `git diff --check -- docs/architecture/system docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
   - Expected observable result: canonical architecture reflects accepted legacy current content, current selector-routing behavior, and no stale current-state references to the completed architecture-method rollout.
   - milestone commit message: `M3: merge legacy architecture content into canonical package`
   - milestone closeout checklist:
     - [ ] targeted validation passed
     - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
     - [ ] progress updated
     - [ ] decision log updated if needed
     - [ ] validation notes updated
     - [ ] milestone committed

4. M4. Normalize legacy lifecycle disposition
   - Goal: update each legacy architecture record with accepted historical lifecycle disposition after merge-back decisions are complete.
   - Requirements: `R63`-`R66`, `R73`-`R75`.
   - Files/components likely touched:
     - all eight legacy Markdown files under `docs/architecture/*.md`
     - `docs/architecture/system/architecture.md`
     - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
     - this plan
   - Dependencies: M3 complete.
   - Tests to add/update:
     - test-spec lifecycle disposition case requiring explicit archived or superseded status plus replacement or archive rationale for each legacy architecture record.
   - Implementation steps:
     - Update each legacy architecture record with an accepted disposition: `superseded`, `archived`, or another approved historical state.
     - Add replacement pointers, archive rationale, or canonical package references required by lifecycle policy.
     - Keep historical content intact except for lifecycle metadata and concise disposition/closeout notes.
     - Confirm no legacy document still implies it is the current architecture source of truth.
   - Validation commands:
     - `python scripts/select-validation.py --mode explicit --path docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md --path docs/architecture/2026-04-21-workflow-stage-autoprogression.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/architecture/system/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
     - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md --path docs/architecture/2026-04-21-workflow-stage-autoprogression.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/architecture/system/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
     - `python scripts/validate-change-metadata.py docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
     - `rg -n "Status|superseded|archived|canonical architecture|docs/architecture/system/architecture.md" docs/architecture/*.md`
     - `git diff --check -- docs/architecture docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
   - Expected observable result: legacy records have explicit historical lifecycle disposition and current architecture truth points to the canonical package.
   - milestone commit message: `M4: normalize legacy architecture lifecycle status`
   - milestone closeout checklist:
     - [ ] targeted validation passed
     - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
     - [ ] progress updated
     - [ ] decision log updated if needed
     - [ ] validation notes updated
     - [ ] milestone committed

5. M5. Close normalization evidence
   - Goal: prove the inventory, canonical package, every changed legacy artifact disposition, change-local evidence, and plan/index lifecycle are synchronized.
   - Requirements: `R63`-`R66`, `R73`-`R75`.
   - Files/components likely touched:
     - `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
     - `docs/plan.md`
     - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
     - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/explain-change.md`
     - final validation scope includes all eight legacy Markdown files changed in M4, even if M5 does not edit them again.
   - Dependencies: M4 complete.
   - Tests to add/update:
     - final test-spec closeout case proving inventory completeness, canonical baseline freshness, every changed legacy artifact lifecycle state, and validation evidence.
   - Implementation steps:
     - Re-run `find docs/architecture -type f | sort` and compare every path with this inventory.
     - Confirm repository guidance no longer overstates legacy normalization.
     - Confirm the canonical architecture baseline no longer contains completed-plan references, old milestone references, stale readiness wording, or stale selector-routing wording.
     - Confirm every legacy architecture document changed in M4 reached its intended lifecycle state and appears in final closeout validation.
     - Create or update `explain-change.md` with problem-to-diff rationale.
     - Update this plan and `docs/plan.md` with final lifecycle state when the outcome is known.
     - If selector output selects `broad_smoke.repo`, run broad smoke and record it.
   - Validation commands:
     - `find docs/architecture -type f | sort`
     - `while IFS= read -r path; do rg -F -q "$path" docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md || printf 'missing-from-plan %s\n' "$path"; done < <(find docs/architecture -type f | sort)`
     - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/explain-change.md`
     - `python scripts/select-validation.py --mode explicit --path docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md --path docs/architecture/2026-04-21-workflow-stage-autoprogression.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/architecture/system/architecture.md`
     - `python scripts/validate-change-metadata.py docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
     - `python scripts/test-change-metadata-validator.py`
     - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/explain-change.md --path specs/legacy-architecture-lifecycle-normalization.test.md --path docs/architecture/system/architecture.md`
     - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md --path docs/architecture/2026-04-21-workflow-stage-autoprogression.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/architecture/system/architecture.md`
     - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/explain-change.md --path docs/architecture/system/architecture.md`
     - `bash scripts/ci.sh --mode explicit --path docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md --path docs/architecture/2026-04-21-workflow-stage-autoprogression.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/architecture/system/architecture.md`
     - `python -c 'from pathlib import Path; bt=chr(96); text=Path("docs/architecture/system/architecture.md").read_text(); stale=[p for p in ("docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md", "M3 "+bt+"code-review"+bt, "M3 "+bt+"verify"+bt, "M4 skill and generated-output update", "M5 legacy architecture normalization follow-on artifact before final completion claims", "diagrams and change-local architecture deltas remain manual-routed review evidence in the first adoption slice") if p in text]; assert not stale, stale'`
     - `rg -n "Status|superseded|archived|canonical architecture|docs/architecture/system/architecture.md" docs/architecture/*.md`
     - `bash scripts/ci.sh --mode broad-smoke` if the selector output includes selected check `broad_smoke.repo`.
     - `git diff --check -- .`
   - Expected observable result: the legacy normalization plan is closed, the plan index agrees with the plan body, the canonical baseline is no longer stale, every changed legacy artifact reached its intended lifecycle state, and final validation evidence is durable.
   - milestone commit message: `M5: close legacy architecture normalization`
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
- 2026-04-29: plan revised after plan-review to add M0 change-local/test-spec routing, split broad legacy review into inventory, domain comparison, and canonical merge-back milestones, add exact validation commands, and name the stale selector-routing architecture wording task.
- 2026-04-29: plan revised after follow-up plan-review to require an M3 canonical current-state sweep and M5 final closeout validation for every legacy architecture document changed in M4.
- 2026-04-29: active focused test spec created at `specs/legacy-architecture-lifecycle-normalization.test.md`.
- 2026-04-29: M0 implemented the change-local metadata and working architecture delta under `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/`; no legacy architecture statuses or canonical architecture content changed.
- 2026-04-29: M0 code-review-r1 requested an explicit canonical architecture package citation in change metadata; the fix added `canonical_artifacts.architecture_package` and recorded the accepted disposition in change-local review artifacts.

## Decision Log

- 2026-04-28: kept this artifact as a follow-on plan rather than editing every legacy architecture document immediately because `specs/architecture-package-method.md` R64 explicitly avoids immediate full migration during first implementation.
- 2026-04-28: classified legacy Markdown architecture records as `archived/historical snapshot` instead of `superseded` because the repository still needs a normalization review to decide which records require explicit supersession pointers versus archive-only rationale.
- 2026-04-28: classified the two `.mmd` files as `current canonical content` because they are required C4 source-text diagrams for the canonical package, not historical records.
- 2026-04-29: chose a focused test spec `specs/legacy-architecture-lifecycle-normalization.test.md` for this follow-on instead of reusing the completed architecture-method test spec, because this work now has its own change-local pack, milestones, and final lifecycle closeout.
- 2026-04-29: split canonical merge-back from lifecycle disposition so legacy files are not archived or superseded until current content and durable decisions have been reviewed.
- 2026-04-29: used `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md` as the M0 durable Markdown reasoning surface; `explain-change.md` remains a planned M5 closeout artifact as defined by the approved plan.

## Surprises and Discoveries

- The current `docs/architecture/` tree includes Mermaid source diagrams as files that must be listed by the inventory proof.
- Legacy architecture records are all Markdown files at the top of `docs/architecture/`; the new canonical package is the only subdirectory-based architecture package today.
- The canonical architecture package still contains wording from the first adoption slice that says `.mmd` diagrams and change-local architecture deltas remain manual-routed, while current selector behavior now routes those paths to existing non-enforcement checks. M3 must correct this wording.
- The canonical architecture package also contains current-state references to the completed architecture-method rollout plan and old milestone handoffs. M3 must sweep those along with selector-routing wording.

## Validation Notes

- 2026-04-28: `find docs/architecture -type f | sort` produced 11 paths, all listed in this plan's inventory.
- 2026-04-28: `while IFS= read -r path; do rg -F -q "$path" docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md || printf 'missing %s\n' "$path"; done < <(find docs/architecture -type f | sort)` produced no output, proving every current architecture path appears in this plan.
- 2026-04-28: `python scripts/select-validation.py --mode explicit --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/plan.md` returned `status: ok` and selected `artifact_lifecycle.validate`.
- 2026-04-28: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/plan.md` passed with `validated 0 artifact files`.
- 2026-04-29: plan-revision `python scripts/select-validation.py --mode explicit --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/plan.md` returned `status: ok` and selected `artifact_lifecycle.validate`.
- 2026-04-29: plan-revision `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/plan.md` passed with `validated 0 artifact files`.
- 2026-04-29: plan-revision `git diff --check -- docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md` passed.
- 2026-04-29: follow-up plan-revision `python scripts/select-validation.py --mode explicit --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/plan.md` returned `status: ok` and selected `artifact_lifecycle.validate`.
- 2026-04-29: follow-up plan-revision `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/plan.md` passed with `validated 0 artifact files`.
- 2026-04-29: follow-up plan-revision `git diff --check -- docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md` passed.
- 2026-04-29: test-spec `python scripts/select-validation.py --mode explicit --path specs/legacy-architecture-lifecycle-normalization.test.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/plan.md` returned `status: ok` and selected `artifact_lifecycle.validate`.
- 2026-04-29: test-spec `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/legacy-architecture-lifecycle-normalization.test.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/plan.md` passed with `validated 1 artifact files`.
- 2026-04-29: test-spec `bash scripts/ci.sh --mode explicit --path specs/legacy-architecture-lifecycle-normalization.test.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/plan.md` passed selected check `artifact_lifecycle.validate`.
- 2026-04-29: test-spec `git diff --check -- specs/legacy-architecture-lifecycle-normalization.test.md docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md` passed.
- 2026-04-29: M0 red proof `python scripts/validate-change-metadata.py docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml` failed as expected before the change-local metadata file existed.
- 2026-04-29: M0 `python scripts/select-validation.py --mode explicit --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path specs/legacy-architecture-lifecycle-normalization.test.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md` returned `status: ok` and selected `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- 2026-04-29: M0 `python scripts/validate-change-metadata.py docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml` passed.
- 2026-04-29: M0 `python scripts/test-change-metadata-validator.py` passed.
- 2026-04-29: M0 `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path specs/legacy-architecture-lifecycle-normalization.test.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/plan.md` passed with `validated 3 artifact files`.
- 2026-04-29: M0 `git diff --check -- docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization specs/legacy-architecture-lifecycle-normalization.test.md docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md` passed.
- 2026-04-29: M0 `bash scripts/ci.sh --mode explicit --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path specs/legacy-architecture-lifecycle-normalization.test.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md` passed selected artifact lifecycle and change metadata checks.
- 2026-04-29: M0 review-fix `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization` passed after recording `code-review-r1` and accepting `CR1-F1`.
- 2026-04-29: M0 review-fix `python scripts/select-validation.py --mode explicit --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/review-log.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/review-resolution.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/reviews/code-review-r1.md --path specs/legacy-architecture-lifecycle-normalization.test.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md` returned `status: ok` and selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- 2026-04-29: M0 review-fix `bash scripts/ci.sh --mode explicit --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/review-log.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/review-resolution.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/reviews/code-review-r1.md --path specs/legacy-architecture-lifecycle-normalization.test.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md` passed selected review artifact, artifact lifecycle, and change metadata checks.

## Outcome and Retrospective

- This follow-on plan is active. Legacy normalization has not yet been executed.
- The repository must continue to avoid claiming that all legacy architecture artifacts have already been normalized until this plan is completed.

## Readiness

- Plan-review approved this plan on 2026-04-29.
- Active test spec exists at `specs/legacy-architecture-lifecycle-normalization.test.md`.
- M0 code-review-r1 finding `CR1-F1` is resolved. Ready for `code-review` rerun of the M0 slice before M1.

## Risks and Follow-Ups

- Risk: contributors may still cite an older architecture snapshot as current architecture truth.
  Mitigation: use `docs/architecture/system/architecture.md` as the canonical package and this plan as the legacy classification map until normalization completes.
- Risk: archiving legacy records without content review could lose current architecture details.
  Mitigation: M1 refreshes inventory, M2 records domain comparison, and M3 performs canonical merge-back before M4 records final legacy lifecycle disposition.
