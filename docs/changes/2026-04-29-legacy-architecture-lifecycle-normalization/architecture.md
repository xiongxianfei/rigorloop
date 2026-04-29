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

## M2 Domain Comparison

M2 compares all eight top-level legacy Markdown architecture records by domain and records reviewable recommendations for M3 canonical merge-back and M4 lifecycle disposition. M2 does not edit `docs/architecture/system/`, does not edit legacy architecture status metadata, and does not create ADRs.

### Domain A: Source Layout, Generated Output, and Adapters

| Legacy architecture record | M3 merge-back candidates | Historical-only content | ADR handling | Conflict or M3 handling | Disposition recommendation |
| --- | --- | --- | --- | --- | --- |
| `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md` | Repository source-of-truth roots, `docs/changes/<change-id>/` change memory, `schemas/`, `scripts/`, `.codex/skills/` as generated output, `docs/plans/0000-00-00-example-plan.md`, and CI thin-wrapper expectations. | First-release template context, early skill-drift examples, and the first-release rejection of a larger `dist/` layout. | Covered by `docs/adr/ADR-20260419-repository-source-layout.md`; no new ADR recommended unless M3 changes the source-layout boundary. | Canonical architecture now also includes `templates/` and `dist/adapters/`; M3 must merge only still-current source-boundary details and not revive old "no dist" wording. | Supersede or archive after M3 with canonical replacement `docs/architecture/system/architecture.md` plus `ADR-20260419-repository-source-layout`. |
| `docs/architecture/2026-04-24-multi-agent-adapter-distribution.md` | Public generated adapter package layout under `dist/adapters/`, authored adapter templates, generated manifest, release metadata and release notes under `docs/releases/<version>/`, separate `.codex/skills/` local mirror, and release/CI validation boundaries. | First public release implementation context, RC and final release gate details, and rejected adapter-layout alternatives. | Covered by `docs/adr/ADR-20260424-generated-adapter-packages.md`; no new ADR recommended unless M3 changes generated package ownership. | Canonical architecture currently names generated adapters but is thin on release metadata, adapter templates, and separate generated-surface validation; M3 should merge concise Deployment View and Crosscutting Concepts detail. | Supersede or archive after M3 with canonical replacement `docs/architecture/system/architecture.md` plus `ADR-20260424-generated-adapter-packages`. |
| `docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md` | OpenCode command alias package shape, curated generated command alias set, manifest `command_aliases`, v0.1.1 release target evidence, and command-alias validation/security constraints. | Patch-release-specific rollout details, smoke-evidence examples, and rejected command wrapper alternatives. | Existing generated-adapter ADR is sufficient; the legacy record explicitly treats command aliases as an additive adapter-package extension, so M3 should record a no-new-ADR rationale if it merges this content. | Current generated output includes OpenCode command aliases; M3 should merge the current generated-command surface without treating aliases as authored skill bodies. | Supersede or archive after M3 with canonical replacement `docs/architecture/system/architecture.md` and generated-adapter ADR coverage. |

### Domain B: Workflow, Lifecycle, and Review

| Legacy architecture record | M3 merge-back candidates | Historical-only content | ADR handling | Conflict or M3 handling | Disposition recommendation |
| --- | --- | --- | --- | --- | --- |
| `docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md` | Artifact lifecycle validator components, artifact-local status as source of truth, class-specific lifecycle contracts, scope-resolution modes, block-versus-warning behavior, and lifecycle validator/CI integration. | Pre-implementation context, alternatives rejected for the lifecycle validator, and old rollout sequencing. | Source-layout ADR covers repository-owned scripts, but the durable lifecycle-validator architecture is not directly ADR-covered; M3 must either link it as spec-owned/no-ADR or create an ADR if reviewers consider the executable lifecycle registry a durable architecture decision. | Canonical architecture currently names lifecycle artifacts and validation scripts but lacks the validator boundary details; M3 should merge concise Building Block, Runtime View, and Crosscutting Concepts detail. | Supersede or archive after M3, with final disposition dependent on whether M3 adds a new ADR or explicit no-ADR rationale. |
| `docs/architecture/2026-04-21-docs-changes-usage-policy.md` | Baseline `docs/changes/<change-id>/change.yaml` plus durable Markdown reasoning, default `explain-change.md`, conditional `review-resolution.md` and `verify-report.md`, scalar artifact-map shape, and legacy `docs/explain/` compatibility. | Original packaging-policy motivation, old top-level explain migration context, and rejected registry/schema redesign alternatives. | Covered by `ADR-20260419-repository-source-layout` for `docs/changes/` as authored source; no new ADR recommended if M3 records this as workflow/spec-owned packaging policy. | Canonical architecture names change-local deltas but does not fully describe the baseline change-local pack; M3 should merge only concise current packaging boundaries. | Supersede or archive after M3 with canonical package and workflow/spec references as replacement. |
| `docs/architecture/2026-04-21-workflow-stage-autoprogression.md` | Lane-aware autoprogression responsibilities, isolated direct stage requests, direct `pr` behavior, stop conditions, and stage-local continuation boundaries. | V1 rollout details, skill-update checklist context, and rejected executable-router alternatives. | No new ADR recommended unless M3 introduces executable workflow orchestration; the legacy record explicitly states no separate ADR is needed for guidance-only autoprogression. | Canonical architecture does not yet describe workflow-stage autoprogression in Runtime View; M3 should decide whether current stage-flow text needs a concise update. | Supersede or archive after M3, with canonical Runtime View and workflow specs as replacement. |
| `docs/architecture/2026-04-24-review-finding-resolution-contract.md` | Detailed review record files, `review-log.md`, `review-resolution.md`, material Finding ID rules, closeout-gated validation, and review artifact validator boundaries. | Historical review-artifact parser design discussion, skill/generated-output update context, and rejected semantic-review automation. | No new ADR recommended; the design follows the source-layout ADR and keeps review decisions as authored change-local artifacts. M3 should add an explicit no-new-ADR rationale if this is merged. | Canonical architecture names review gates generally but not the review-artifact validation boundary; M3 should merge concise Building Block and Runtime View detail. | Supersede or archive after M3 with canonical package and review-finding spec as replacement. |

### Domain C: Validation and CI

| Legacy architecture record | M3 merge-back candidates | Historical-only content | ADR handling | Conflict or M3 handling | Disposition recommendation |
| --- | --- | --- | --- | --- | --- |
| `docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md` | Selector module as validation-routing source, stable check IDs, check catalog, broad-smoke trigger model, `scripts/ci.sh` execution wrapper, non-fail-open unclassified paths, and manual-proof ownership. | First-slice path-category rollout details, old selector fallback discussion, and rejected dependency-graph alternatives. | No separate ADR recommended; the legacy record treats selector routing as a spec-approved contract. M3 should record no-new-ADR rationale unless selector ownership changes. | At M2, current selector behavior routed architecture diagrams and change-local architecture deltas to existing lifecycle validation while canonical architecture still contained stale manual-routed wording; M3 corrected the Runtime View validation flow. | Supersede or archive after M3 with canonical package and selector/test-layering spec as replacement. |

### Selector and CI Current-State Check

M2 also compared the validation/CI record against current `scripts/validation_selection.py` behavior:

- `docs/changes/<change-id>/architecture.md` is classified as `change-local-lifecycle` and routes to existing `artifact_lifecycle.validate` for the delta plus its governing `change.yaml`.
- `docs/architecture/system/diagrams/*.mmd` is classified as `architecture-diagram` and routes to existing `artifact_lifecycle.validate` for the package context.
- `review-log.md`, `review-resolution.md`, and `reviews/` route to `review_artifacts.validate`.
- `change.yaml` routes to `change_metadata.validate` and `change_metadata.regression`.
- None of these selected checks validate C4 diagram sufficiency, arc42 section completeness, ADR presence, or architecture package shape. Those remain manual review evidence under the review-based rollout.

The selector/CI comparison created an M3 task that is now complete: canonical wording now says diagrams and change-local architecture deltas route to existing non-enforcement lifecycle checks, while architecture sufficiency remains manual review evidence.

## M3 Canonical Merge-Back

M3 merged accepted current architecture truth into `docs/architecture/system/architecture.md` without changing C4 context or container boundaries. The existing C4 diagrams already contain the same repository actors and containers; the merge-back changed canonical arc42 prose only.

| Legacy architecture record | Canonical merge-back result | Historical-only content left for M4 | ADR handling |
| --- | --- | --- | --- |
| `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md` | Source-of-truth roots, `docs/changes/<change-id>/`, plan template, generated `.codex/skills/`, and thin CI wrapper details are represented in Architecture Constraints, Building Block View, Runtime View, Deployment View, Crosscutting Concepts, and Architecture Decisions. | First-release template context, early drift examples, and rejected larger initial layout. | Existing `ADR-20260419-repository-source-layout` remains linked. |
| `docs/architecture/2026-04-24-multi-agent-adapter-distribution.md` | `dist/adapters/`, `scripts/adapter_templates/`, generated manifest, release metadata, tracked release notes, release verification, and generated-surface validation are represented in Context and Scope, Building Block View, Runtime View, Deployment View, Crosscutting Concepts, and Quality Requirements. | RC/final release gate details and rejected adapter-layout alternatives. | Existing `ADR-20260424-generated-adapter-packages` remains linked. |
| `docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md` | OpenCode command aliases, curated lifecycle command wrappers, `command_aliases` manifest detail, and command-alias validation/security constraints are represented in Building Block View, Runtime View, Crosscutting Concepts, and Deployment View. | Patch-release-specific rollout details, smoke-evidence examples, and rejected command-wrapper alternatives. | Existing generated-adapter ADR is sufficient because command aliases remain an additive generated package detail. |
| `docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md` | Artifact-local status, lifecycle validator ownership, class-specific lifecycle contracts, explicit scope modes, block-versus-warning behavior, and CI integration are represented in Building Block View, Runtime View, Crosscutting Concepts, and Quality Requirements. | Pre-implementation context, old rollout sequencing, and rejected broad schema/framework alternatives. | No new ADR: M3 documents existing validation architecture and does not change the executable lifecycle registry. Future validation-architecture changes should create or supersede an ADR when they meet `R44`-`R45`. |
| `docs/architecture/2026-04-21-docs-changes-usage-policy.md` | Baseline `change.yaml` plus durable Markdown reasoning, default `explain-change.md`, conditional `review-resolution.md` and `verify-report.md`, and scalar artifact-map shape are represented in Building Block View and Runtime View. | Original packaging-policy motivation and old top-level explain migration context. | Existing source-layout ADR covers `docs/changes/` as authored source; no new ADR is required for this documentation merge-back. |
| `docs/architecture/2026-04-21-workflow-stage-autoprogression.md` | Lane-aware continuation, isolated direct stage requests, direct `pr` boundary, and stop conditions are represented in Runtime View. | V1 rollout checklist and rejected executable-router alternatives. | No new ADR: M3 does not introduce executable orchestration or change workflow-stage behavior. |
| `docs/architecture/2026-04-24-review-finding-resolution-contract.md` | Detailed review records, `review-log.md`, `review-resolution.md`, material finding closeout, and review artifact validator boundaries are represented in Building Block View, Runtime View, Crosscutting Concepts, and Quality Requirements. | Historical parser design detail, skill/generated-output update context, and rejected semantic-review automation. | No new ADR: review artifacts remain authored change-local evidence under the source-layout boundary. |
| `docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md` | Selector ownership, stable check IDs, broad-smoke triggers, `scripts/ci.sh`, non-fail-open unclassified paths, manual proof ownership, and current architecture support path routing are represented in Runtime View and Crosscutting Concepts. | First-slice path-category rollout detail and rejected dependency-graph alternatives. | No new ADR: selector routing remains a spec-approved validation contract, and M3 does not change selector behavior. |

The canonical sweep also removed stale current-state references to the completed architecture-method rollout plan, old M3/M4/M5 handoff text, and outdated wording that said diagrams and change-local architecture deltas were manual-routed. Current wording says those paths route to existing non-enforcement lifecycle checks while architecture sufficiency remains manual review evidence.

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

| Building block | Responsibility | Current state |
| --- | --- | --- |
| `docs/architecture/system/architecture.md` | Canonical architecture source of truth | updated in M3 |
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

Validation uses existing selector, change metadata, artifact lifecycle, CI-wrapper, and whitespace checks. It does not add or require new architecture package enforcement.

## Architecture Decisions

No new ADR is required for M3. M3 merged current architecture documentation only; it did not introduce or revise source layout, adapter generation or packaging, validation architecture, release architecture, or workflow-stage behavior.

The governing architecture method decision remains `docs/adr/ADR-20260428-architecture-package-method.md`. The source-layout and generated-adapter decisions remain `docs/adr/ADR-20260419-repository-source-layout.md` and `docs/adr/ADR-20260424-generated-adapter-packages.md`.

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
| Legacy status changes happen too early | M0 through M3 explicitly exclude legacy architecture status edits. |
| Later comparison misses a legacy record | M1 must refresh inventory and add one comparison row per top-level legacy Markdown record. |
| Canonical merge-back creates false final-normalization claims | M3 records that M4 lifecycle disposition and M5 closeout remain pending. |

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

## M2 Evidence

- Same-slice requirements: `R37`-`R39`, `R44`-`R48`, `R63`-`R66`, `R73`-`R75`.
- Same-slice tests: `T3`, `T4`, `T9`.
- Legacy Markdown records compared: 8.
- Domain groups compared: source layout/generated output/adapters; workflow/lifecycle/review; validation/CI.
- Merge-back candidates recorded: yes, for every legacy record.
- Historical-only content recorded: yes, for every legacy record.
- ADR handling recorded: yes, either existing ADR coverage, no-new-ADR rationale for M3, or M3 ADR review.
- Final disposition recommendations recorded: yes, pending M3 canonical merge-back and M4 lifecycle edits.
- Selector current-state check: architecture diagram and change-local architecture paths route to existing lifecycle checks only; no architecture package enforcement was added.
- Test spec edits: none; `T3`, `T4`, and `T9` already cover the M2 proof.
- Legacy architecture status edits: none in M2.
- Canonical architecture edits: none in M2.
- T9 security/readability inspection: touched artifacts use repository-relative paths and contain no secrets, credentials, tokens, private keys, or machine-local debug-only data.

## M3 Evidence

- Same-slice requirements: `R37`-`R39`, `R44`-`R48`, `R63`-`R66`, `R72`-`R75`.
- Same-slice tests: `T5`, `T6`, `T9`, `T12`.
- Canonical package edits: `docs/architecture/system/architecture.md` updated with accepted current content from all eight legacy records.
- C4 diagram edits: none; no actor, system boundary, or container boundary changed.
- Legacy architecture status edits: none in M3.
- ADR edits: none; no new durable decision was introduced or revised by this documentation merge-back.
- Historical-only content left for M4: legacy release rollout details, old implementation sequencing, rejected alternatives, historical parser detail, old smoke examples, and first-slice path-category rollout detail remain in the legacy records.
- Selector current-state sweep: canonical Runtime View now says architecture diagram source files and change-local architecture deltas route to existing non-enforcement lifecycle checks, while C4 sufficiency, arc42 completeness, ADR need, and package shape remain manual review evidence.
- Forbidden automation check: M3 did not add validators, dependencies, command output changes, command exit behavior changes, or package-shape enforcement.
- T9 security/readability inspection: touched artifacts use repository-relative paths and contain no secrets, credentials, tokens, private keys, or machine-local debug-only data.

## Next Artifacts

- M4 legacy lifecycle disposition after M3 code-review.

## Follow-on Artifacts

- None yet.

## Readiness

This change-local architecture delta has completed the M3 canonical merge-back slice. It is ready for M3 code-review; M4 legacy lifecycle disposition may start only after that review passes.
