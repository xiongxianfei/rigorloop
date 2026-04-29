# RigorLoop Canonical System Architecture

## Status

- approved

## Related artifacts

- Proposal: `docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md`
- Spec: `specs/architecture-package-method.md`
- Test spec: `specs/architecture-package-method.test.md`
- Legacy normalization plan: `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
- Method ADR: `docs/adr/ADR-20260428-architecture-package-method.md`
- Change-local architecture delta: `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/architecture.md`
- Legacy normalization delta: `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
- C4 system context diagram: `docs/architecture/system/diagrams/context.mmd`
- C4 container diagram: `docs/architecture/system/diagrams/container.mmd`

## Introduction and Goals

RigorLoop is a Git-first starter kit for AI-assisted software delivery. Its architecture is the repository system that keeps proposals, specs, architecture artifacts, plans, tests, implementation evidence, generated adapters, and review gates traceable.

This canonical architecture package is the long-lived current architecture source of truth for the repository architecture method. It adopts C4 for structural views, all 12 official arc42 sections for architecture documentation, and ADRs for durable decisions.

The goals are:

- make current repository structure visible through reviewable C4 source diagrams;
- keep architecture reasoning complete without requiring heavy prose;
- separate canonical architecture from change-local working deltas;
- preserve durable decisions in ADRs;
- preserve review, verification, and closeout evidence in repository artifacts;
- keep generated output reproducible from canonical sources;
- keep first adoption review-based until real package usage proves the shape.

## Architecture Constraints

- `CONSTITUTION.md` is the highest-priority repository governance artifact below external runtime instructions.
- `specs/architecture-package-method.md` owns the C4, arc42, ADR, template, canonical-package, and change-local-delta contract.
- `specs/rigorloop-workflow.md` owns only workflow stage routing and handoff language for this method.
- The canonical package path is `docs/architecture/system/architecture.md` with default diagrams under `docs/architecture/system/diagrams/`.
- Architecture and ADR scaffolds live under `templates/`; live architecture and ADR records live under `docs/architecture/` and `docs/adr/`.
- Change-local architecture deltas live under `docs/changes/<change-id>/` and become historical evidence after durable content is merged back.
- `.codex/skills/` and `dist/adapters/` are generated output and must not be hand-edited.
- `docs/releases/<version>/release.yaml` and `docs/releases/<version>/release-notes.md` are authored release evidence, not generated release-note substitutes.
- First implementation remains review-based for architecture package completeness; required package-shape, C4-file, and ADR-presence enforcement automation is deferred.
- Legacy documents under `docs/architecture/` remain valid historical or legacy artifacts until a follow-on normalization artifact classifies them.

## Context and Scope

RigorLoop operates inside a repository boundary. Contributors and agents author changes through repository artifacts, reviewers inspect the diff and evidence, GitHub and local shells execute validation, and adapter consumers receive generated guidance for supported agent runtimes.

The canonical scope includes:

- authored governance, workflow, specification, architecture, ADR, plan, test, and change-local artifacts;
- canonical skills, adapter entrypoint templates, architecture templates, and ADR templates;
- repository-owned validation and generation scripts;
- generated Codex runtime skills, public adapter packages, adapter manifests, and command aliases;
- authored release metadata, tracked release notes, and maintainer smoke evidence;
- legacy architecture documents that still need lifecycle normalization.

The canonical scope excludes runtime application infrastructure, databases, service APIs, and production telemetry because this repository is a workflow and adapter starter kit rather than a deployed service.

See `docs/architecture/system/diagrams/context.mmd` for the C4 system context view.

## Solution Strategy

Use one canonical architecture package as the current baseline, supported by change-local deltas only for architecture-significant work that needs temporary design reasoning. Accepted durable content from a delta is merged into this package before the change is complete, while durable decisions are preserved in ADRs.

The repository keeps structural documentation in C4 Mermaid source diagrams, written architecture in the official arc42 section model, and durable decision rationale in ADRs. Existing validation remains path-scoped and review-based for architecture sufficiency, with narrow lifecycle compatibility for canonical architecture packages, diagrams, change-local architecture deltas, review artifacts, change metadata, and generated-output drift.

This strategy keeps the method practical for normal contributors while making architecture review compare structure, runtime flow, deployment boundaries, cross-cutting concerns, quality requirements, risks, and decision history consistently.

## Building Block View

| Building block | Responsibility | Current source |
| --- | --- | --- |
| Governance and workflow summaries | Define source-of-truth order, repository defaults, workflow routing, and contributor expectations | `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md` |
| Lifecycle artifacts | Carry proposal, spec, architecture, ADR, plan, test-spec, and change metadata states | `docs/proposals/`, `specs/`, `docs/architecture/`, `docs/adr/`, `docs/plans/`, `docs/changes/` |
| Canonical architecture package | Long-lived current architecture source of truth | `docs/architecture/system/` |
| Change-local deltas | Temporary working architecture for architecture-significant changes and historical evidence after merge-back | `docs/changes/<change-id>/architecture.md` and optional diagrams |
| Change-local evidence pack | Machine-readable traceability and durable reasoning for non-trivial work | `docs/changes/<change-id>/change.yaml`, `explain-change.md`, conditional `review-resolution.md`, conditional `verify-report.md`, and `reviews/*.md` |
| Templates | Canonical scaffolding for architecture and ADR authoring | `templates/architecture.md`, `templates/adr.md` |
| Canonical skills and adapter templates | Source instructions for workflow stages and thin adapter entrypoints | `skills/`, `scripts/adapter_templates/` |
| Validation selector and CI wrapper | Classify changed paths, select stable check IDs, and run repository-owned proof commands | `scripts/validation_selection.py`, `scripts/select-validation.py`, `scripts/ci.sh` |
| Artifact validators | Validate lifecycle artifacts, change metadata, review artifacts, adapter packages, release metadata, and generated drift | `scripts/validate-artifact-lifecycle.py`, `scripts/validate-change-metadata.py`, `scripts/validate-review-artifacts.py`, `scripts/build-adapters.py --check`, `scripts/validate-adapters.py`, `scripts/validate-release.py`, `scripts/release-verify.sh` |
| Generated runtime mirrors and adapters | Derived guidance for Codex and public adapter packages | `.codex/skills/`, `dist/adapters/`, `dist/adapters/manifest.yaml`, `dist/adapters/opencode/.opencode/commands/` |
| Release evidence | Authored release contract, notes, and smoke evidence | `docs/releases/<version>/release.yaml`, `docs/releases/<version>/release-notes.md` |
| Legacy architecture documents | Previously approved architecture records awaiting normalization classification | `docs/architecture/*.md` |

See `docs/architecture/system/diagrams/container.mmd` for the C4 container view.

## Runtime View

### Architecture-significant change flow

1. Contributor or agent reads the governing proposal, spec, existing architecture, ADRs, active plan, and test spec.
2. Architecture-significant work creates or updates a change-local architecture delta when working design reasoning is needed.
3. Durable decisions are captured in ADRs under `docs/adr/`.
4. Implementation updates the lowest affected C4 level and affected arc42 sections first, then updates broader views only when the change affects them.
5. Durable current architecture content is merged into the canonical package before the architecture-significant change is complete.
6. The change-local delta remains under `docs/changes/<change-id>/` as historical evidence only.

### Workflow and review flow

1. Non-trivial work records `change.yaml` plus durable Markdown reasoning under `docs/changes/<change-id>/`.
2. Workflow stages follow the active lane, invocation context, completed stage outcome, and stop conditions.
3. Direct review-only or isolated stage requests remain isolated unless workflow-managed context authorizes continuation.
4. Material review findings are recorded in detailed review records and summarized in `review-log.md`.
5. `review-resolution.md` closes material findings only after final dispositions, actions, rationale, and validation evidence are recorded.
6. `verify`, `explain-change`, and `pr` use the change-local evidence pack, plan state, validation output, and review closeout state before claiming readiness.

### Validation flow

1. Changed paths are inspected with `python scripts/select-validation.py --mode explicit --path ...`.
2. Supported changed paths are executed through `bash scripts/ci.sh --mode explicit --path ...`.
3. The selector emits stable check IDs such as `artifact_lifecycle.validate`, `change_metadata.validate`, `change_metadata.regression`, `review_artifacts.validate`, and generated-output checks.
4. Lifecycle-managed artifacts are checked with `scripts/validate-artifact-lifecycle.py`.
5. Change metadata is checked with `scripts/validate-change-metadata.py`.
6. Review artifact closeout is checked with `scripts/validate-review-artifacts.py` when review files are in scope.
7. Architecture diagram source files and change-local architecture deltas route only to existing non-enforcement lifecycle checks; C4 sufficiency, arc42 completeness, ADR need, and package shape remain architecture-review or code-review evidence.
8. Unclassified paths do not fail open; they require explicit manual routing or a later selector contract update.
9. Final broad smoke runs only when an authoritative trigger requires it.

### Generated guidance flow

1. Canonical skill sources under `skills/` are edited.
2. Adapter entrypoint templates under `scripts/adapter_templates/` provide thin authored package guidance.
3. Existing generators refresh `.codex/skills/` and public adapter output when canonical skill guidance changes.
4. OpenCode command aliases are generated prompt wrappers for a curated lifecycle command set and remain derived from canonical skill inclusion decisions.
5. Adapter validation and release verification check manifest shape, generated file drift, release metadata, tracked release notes, smoke evidence, and security constraints.

## Deployment View

RigorLoop has no deployed service, database, or runtime infrastructure for this architecture method. Deployment is repository packaging and publication:

- authored source artifacts remain in `docs/`, `specs/`, `skills/`, `schemas/`, `scripts/`, and `templates/`;
- canonical architecture lives in `docs/architecture/system/`;
- ADRs live in `docs/adr/`;
- change-local evidence lives in `docs/changes/<change-id>/`;
- review records, review logs, review resolutions, and verify reports live in the relevant change-local pack when their workflow triggers apply;
- release metadata and tracked release notes live in `docs/releases/<version>/`;
- generated Codex runtime skills live in `.codex/skills/`;
- generated public adapter packages, manifests, and OpenCode command aliases live in `dist/adapters/`;
- GitHub Actions remain thin wrappers around repository-owned scripts.

Rollback reverts the authored method artifacts, canonical package, templates, skill changes, generated refresh, and narrow lifecycle compatibility. No runtime data migration is required.

## Crosscutting Concepts

### Source of truth

The focused architecture package method spec owns the normative package contract. This canonical package owns current architecture shape after merge-back. ADRs own durable decisions. Change-local deltas do not compete with the canonical package after merge-back.

### Lifecycle status

Lifecycle-managed artifacts keep status in the artifact. Current architecture artifacts use `approved`; ADRs use the ADR lifecycle vocabulary. Terminal or historical artifacts must preserve replacement or closeout evidence where required.

### Validation layering

The selector owns routing and stable check IDs. Validation scripts own proof work. Manual review owns C4 diagram sufficiency, arc42 completeness, ADR need, and architecture package shape until a later approved automation contract changes that. Architecture support paths may select lifecycle checks for deterministic CI routing, but that routing is not architecture-package enforcement.

### Generated output

Canonical skills and adapter templates are authored sources. `.codex/skills/`, `dist/adapters/`, adapter manifests, and OpenCode command aliases are generated outputs refreshed only through existing repository generators. Generated output must not become the source for another generated surface.

### Release and adapter evidence

Release verification uses tracked `docs/releases/<version>/release.yaml` and `release-notes.md` plus maintainer smoke evidence. Generated release notes are not authoritative for adapter compatibility claims.

### Review artifact closeout

Review records are authored change-local evidence. The review artifact validator checks structure, references, allowed dispositions, and closeout completeness; it does not decide whether a finding is substantively correct.

### Security and privacy

Architecture artifacts and diagrams must not include secrets, credentials, private keys, or machine-local debug-only data. When a change affects trust boundaries, permissions, data exposure, or secret handling, the relevant architecture section and diagrams should state that explicitly.

### Legacy architecture handling

Existing legacy architecture documents remain in place until the follow-on normalization artifact inventories and classifies each one. Until then, the repository must not claim that every older architecture artifact has already been normalized into this package.

## Architecture Decisions

- `docs/adr/ADR-20260428-architecture-package-method.md` records the durable decision to adopt C4 plus official arc42 plus ADRs, one canonical architecture package, change-local deltas for architecture-significant work, templates under `templates/`, Mermaid source diagrams for the first implementation, and review-based first adoption.
- `docs/adr/ADR-20260419-repository-source-layout.md` records the repository source layout decision that separates canonical sources from generated runtime output.
- `docs/adr/ADR-20260424-generated-adapter-packages.md` records the generated adapter package boundary that this method preserves.
- No new ADR is created by the legacy normalization M3 merge-back because it documents current architecture truth without changing source layout, adapter generation or packaging, validation architecture, release architecture, or workflow-stage behavior. Existing approved specs and legacy architecture records remain the historical evidence for those prior implementation choices until M4 assigns final legacy lifecycle disposition.

## Quality Requirements

| Quality | Requirement |
| --- | --- |
| Reviewability | Architecture, diagrams, templates, and ADRs are repository text that can be reviewed in diffs. |
| Traceability | Architecture changes link proposal, spec, plan, test spec, ADRs, and validation evidence. |
| Compatibility | Legacy architecture records remain valid until explicitly normalized, superseded, or archived. |
| Proportionality | Leaf changes that do not affect architecture boundaries or decisions are not forced to update this package. |
| Determinism | Generated skill and adapter output remains reproducible from canonical sources. |
| Maintainability | The workflow spec stays stage-level while the focused method spec owns the detailed architecture contract. |
| Security | Architecture artifacts avoid secrets and document trust boundaries when relevant. |
| Review closeout | Material findings stay open until review-resolution evidence records final dispositions and required validation. |

## Risks and Technical Debt

| Risk or debt | Current handling |
| --- | --- |
| Legacy architecture documents can confuse contributors before normalization is complete | The legacy normalization plan inventories, compares, merges current content, and then assigns final lifecycle disposition. |
| First implementation relies on review rather than structural package enforcement | Approved spec intentionally defers enforcement automation until a real package proves the shape. |
| C4 context and container views may be too coarse for future module-level changes | Add component diagrams only when container-level structure no longer explains affected responsibilities. |
| Change-local deltas could become competing sources if merge-back is skipped | Architecture-review, code-review, and verify must treat unmerged durable architecture truth as incomplete. |

## Glossary

- ADR: architecture decision record that preserves a durable decision, alternatives, consequences, and follow-up.
- arc42: the 12-section architecture documentation model used by `architecture.md`.
- C4: context, container, component, and code-level structural diagram model.
- canonical architecture package: the long-lived current architecture source under `docs/architecture/system/`.
- change-local architecture delta: temporary working architecture under `docs/changes/<change-id>/`.
- generated output: derived files under `.codex/skills/` and `dist/adapters/`.
- merge-back: incorporating accepted durable content from a change-local delta into the canonical architecture package.
- non-enforcement lifecycle routing: selector-selected validation that checks artifact lifecycle compatibility without proving C4 sufficiency, arc42 completeness, ADR need, or architecture package shape.
- review artifact: authored change-local review evidence such as `reviews/*.md`, `review-log.md`, or `review-resolution.md`.

## Next artifacts

- M4 legacy architecture lifecycle disposition in `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`.
- M5 final closeout for the legacy normalization plan.

## Follow-on artifacts

- None yet.

## Readiness

This package is the current canonical architecture baseline after legacy-domain merge-back. Legacy top-level architecture records still require M4 lifecycle disposition and M5 final closeout before the repository may claim all legacy architecture artifacts are normalized.
