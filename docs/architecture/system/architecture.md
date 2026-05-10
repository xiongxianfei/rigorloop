# RigorLoop Canonical System Architecture

## Status

- approved

## Related artifacts

- Proposal: `docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md`
- Proposal refinement: `docs/proposals/2026-04-29-c4-arc42-package-quality.md`
- Spec: `specs/architecture-package-method.md`
- Test spec: `specs/architecture-package-method.test.md`
- Legacy normalization plan: `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
- Method ADR: `docs/adr/ADR-20260428-architecture-package-method.md`
- Method amendment ADR: `docs/adr/ADR-20260509-architecture-skill-surface-simplification.md`
- Change-local architecture delta: `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/architecture.md`
- Package-quality architecture delta: `docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md`
- Legacy normalization delta: `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
- Architecture skill surface simplification proposal: `docs/proposals/2026-05-09-simplify-architecture-skill-surfaces.md`
- Workflow governance update: `docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md`
- Workflow governance change metadata: `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`
- C4 system context diagram: `diagrams/context.mmd`
- C4 container diagram: `diagrams/container.mmd`

## Introduction and Goals

RigorLoop is a Git-first starter kit for AI-assisted software delivery. Its architecture is the repository system that keeps proposals, specs, architecture artifacts, plans, tests, implementation evidence, generated adapters, and review gates traceable.

This canonical architecture package is the long-lived current architecture source of truth for the repository architecture method. It adopts C4 for structural views, all 12 official arc42 sections for architecture documentation, and ADRs for durable decisions.

The goals are:

- make current repository structure visible through reviewable C4 source diagrams;
- keep architecture reasoning complete without requiring heavy prose;
- separate canonical architecture from historical or exceptional change-local evidence;
- keep architecture updates on the lowest sufficient architecture surface;
- preserve durable decisions in ADRs;
- preserve review, verification, and closeout evidence in repository artifacts;
- keep generated output reproducible from canonical sources;
- keep first adoption and package-quality refinement review-based until real package usage proves which checks are worth automating.

## Architecture Constraints

- `CONSTITUTION.md` is the highest-priority repository governance artifact below external runtime instructions.
- `specs/architecture-package-method.md` owns the C4, arc42, ADR, template, canonical-package, architecture-surface, and historical change-local evidence contract.
- `specs/rigorloop-workflow.md` owns only workflow stage routing and handoff language for this method.
- The canonical package path is `docs/architecture/system/architecture.md` with default diagrams under `docs/architecture/system/diagrams/`.
- Architecture and ADR scaffolds live under `templates/`; live architecture and ADR records live under `docs/architecture/` and `docs/adr/`.
- Architecture work uses the lowest sufficient architecture surface: no-impact rationale for changes with no architecture impact, direct canonical package update for clear current-architecture changes, ADR when a durable decision is introduced or revised, and proposal/spec routing when direction or behavior is not ready.
- Change-local architecture deltas are not part of the normal architecture authoring path. Existing deltas remain historical evidence, and new deltas are limited to legacy closeout or explicit exceptional evidence.
- `.codex/skills/` and `dist/adapters/` are generated output and must not be hand-edited.
- `docs/releases/<version>/release.yaml` and `docs/releases/<version>/release-notes.md` are authored release evidence, not generated release-note substitutes.
- First implementation remains review-based for architecture package completeness; required package-shape, C4-file, and ADR-presence enforcement automation is deferred.
- Top-level legacy documents under `docs/architecture/*.md` are archived historical artifacts after accepted current content has been merged into this canonical package.
- Package diagrams live as separate authored source files under `diagrams/`; default Mermaid diagrams use `.mmd` files and are linked from `architecture.md` by relative path.
- Mermaid flowchart C4 diagrams use explicit person, system, external, and container styling; container labels include technology when relevant to review.

## Context and Scope

RigorLoop operates inside a repository boundary. Contributors and agents author changes through repository artifacts, reviewers inspect the diff and evidence, GitHub and local shells execute validation, and adapter consumers receive generated guidance for supported agent runtimes.

The canonical scope includes:

- authored governance, workflow, specification, architecture, ADR, plan, test, report, and change-local artifacts;
- canonical skills, adapter entrypoint templates, architecture templates, and ADR templates;
- repository-owned validation and generation scripts;
- generated Codex runtime skills, public adapter packages, adapter manifests, and command aliases;
- authored release metadata, tracked release notes, and maintainer smoke evidence;
- archived legacy architecture documents that remain historical evidence after lifecycle normalization.

The canonical scope excludes runtime application infrastructure, databases, service APIs, and production telemetry because this repository is a workflow and adapter starter kit rather than a deployed service.

See [`diagrams/context.mmd`](diagrams/context.mmd) for the C4 system context view.

## Solution Strategy

Use one canonical architecture package as the current baseline and choose the lowest sufficient architecture surface for each change. Leaf or no-impact work records a no-architecture-impact rationale. Clear current-architecture changes update the canonical package directly. ADRs preserve durable decisions. Unsettled direction routes back to proposal or proposal revision, and unsettled behavior routes back to spec or spec revision.

Historical or exceptional change-local architecture evidence never competes with this package. When such evidence contains durable current architecture truth, that truth must be represented directly in the canonical package before completion.

The repository keeps structural documentation in C4 Mermaid source diagrams, written architecture in the official arc42 section model, and durable decision rationale in ADRs. Existing validation remains path-scoped and review-based for architecture sufficiency, with narrow lifecycle compatibility for canonical architecture packages, diagrams, historical or exceptional change-local architecture evidence, review artifacts, change metadata, and generated-output drift.

This strategy keeps the method practical for normal contributors while making architecture review compare structure, runtime flow, deployment boundaries, cross-cutting concerns, quality requirements, risks, and decision history consistently.

## Building Block View

See [`diagrams/container.mmd`](diagrams/container.mmd) for the C4 container view.

### Level 1 White-Box: RigorLoop Repository System

The repository system is composed of authored guidance, lifecycle artifacts, validation and generation scripts, generated adapter outputs, and release evidence. Authored surfaces define intent and contracts; scripts provide deterministic proof and generated-output refresh; generated surfaces are derived and must not become sources of truth.

| Container | Responsibility | Technology / source |
| --- | --- | --- |
| Governance and workflow guidance | Defines source-of-truth order, repository defaults, workflow routing, and contributor expectations | Markdown in `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md` |
| Lifecycle artifacts and ADRs | Carry proposal, spec, architecture, ADR, plan, test-spec, and change metadata states | Markdown/YAML in `docs/proposals/`, `specs/`, `docs/architecture/`, `docs/adr/`, `docs/plans/`, `docs/changes/` |
| Reports and measurement baselines | Carry longitudinal evidence that is compared across changes or releases instead of duplicated in change-local artifacts | Markdown under `docs/reports/`, including token-cost baselines under `docs/reports/token-cost/` |
| Canonical architecture package | Long-lived current architecture source of truth, including arc42 prose and C4 diagram source | Markdown and Mermaid in `docs/architecture/system/` |
| Change-local evidence | Historical architecture evidence, explicit exceptional architecture evidence, change metadata, explanation, review resolution, and verification evidence | Markdown/YAML in `docs/changes/<change-id>/` |
| Templates and diagram styles | Canonical scaffolding for architecture, ADRs, and shared Mermaid C4 role styling | Markdown/Mermaid under `templates/` |
| Canonical skills and adapter templates | Source instructions for workflow stages and thin adapter entrypoints | Markdown in `skills/`, templates in `scripts/adapter_templates/` |
| Validation and generation scripts | Select checks, validate artifacts, refresh generated output, and prove drift status | Python and shell under `scripts/` |
| Generated runtime mirrors and adapters | Derived Codex runtime skills and public adapter packages for supported agent tools | Generated files under `.codex/skills/` and `dist/adapters/` |
| Release evidence | Authored release contract, notes, and maintainer smoke evidence | YAML/Markdown under `docs/releases/<version>/` |
| Legacy architecture archive | Historical architecture records retained after accepted current content is merged here | Archived Markdown under `docs/architecture/*.md` |

### Level 2 White-Box: Validation and Generation Scripts

The validation and generation container has four important internal responsibilities:

- selector and CI wrapper: `scripts/validation_selection.py`, `scripts/select-validation.py`, and `scripts/ci.sh` classify paths, select stable check IDs, and run repository-owned proof commands;
- lifecycle and change validators: `scripts/validate-artifact-lifecycle.py`, `scripts/validate-change-metadata.py`, and `scripts/validate-review-artifacts.py` validate artifact status, change metadata, and material review closeout structure;
- skill and adapter generation: `scripts/build-skills.py`, `scripts/build-adapters.py`, and adapter distribution helpers refresh `.codex/skills/` and `dist/adapters/` from canonical sources;
- release and adapter validation: `scripts/validate-adapters.py`, `scripts/validate-release.py`, and `scripts/release-verify.sh` check generated packages, manifests, release metadata, tracked release notes, and smoke evidence.
- measurement and reporting scripts: repository-local commands measure skill size, analyze Codex JSONL session exports, summarize tool-output amplification, and produce reviewable evidence for reports without requiring hosted telemetry.

This decomposition is prose-only for now. A component diagram should be added when future validation work changes these internal responsibilities enough that prose no longer explains the selector, validator, generator, and CI-wrapper relationships.

## Runtime View

### Architecture update flow

1. Contributor or agent reads the governing proposal, spec, existing architecture, ADRs, active plan, and test spec.
2. The architecture stage chooses the lowest sufficient architecture surface.
3. If the change has no architecture impact, the contributor records a short rationale in plan, test-spec, change metadata, or PR evidence.
4. If current architecture truth changes clearly, the contributor updates the smallest affected canonical arc42 section or C4 diagram directly.
5. If direction is unsettled, the contributor stops architecture authoring and routes the issue to proposal or proposal revision.
6. If behavior is unsettled, the contributor stops architecture authoring and routes the issue to spec or spec revision.
7. Durable decisions are captured, amended, superseded, or deprecated in ADRs under `docs/adr/`.
8. If historical or exceptional change-local architecture evidence contains durable current architecture truth, the contributor represents that truth directly in the canonical package before completion.

### Workflow and review flow

1. Non-trivial work records `change.yaml` plus durable Markdown reasoning under `docs/changes/<change-id>/`.
2. Workflow-managed delivery follows one recommended standard workflow, stage triggers, completed stage outcomes, and stop conditions.
3. Direct manual skill requests remain isolated unless the user explicitly asks to continue through the standard workflow.
4. Material review findings are recorded in detailed review records and summarized in `review-log.md`.
5. `review-resolution.md` closes material findings only after final dispositions, actions, rationale, and validation evidence are recorded.
6. Final closeout runs `ci-maintenance` when triggered, then `explain-change`, `verify`, and `pr`.
7. `explain-change`, `verify`, and `pr` use the change-local evidence pack, plan state, validation output, and review closeout state before claiming readiness.

### Validation flow

1. Changed paths are inspected with `python scripts/select-validation.py --mode explicit --path ...`.
2. Supported changed paths are executed through `bash scripts/ci.sh --mode explicit --path ...`.
3. The selector emits stable check IDs such as `artifact_lifecycle.validate`, `change_metadata.validate`, `change_metadata.regression`, `review_artifacts.validate`, and generated-output checks.
4. Lifecycle-managed artifacts are checked with `scripts/validate-artifact-lifecycle.py`.
5. Change metadata is checked with `scripts/validate-change-metadata.py`.
6. Review artifact closeout is checked with `scripts/validate-review-artifacts.py` when review files are in scope.
7. Architecture diagram source files and historical or exceptional change-local architecture evidence route only to existing non-enforcement lifecycle checks; C4 sufficiency, arc42 completeness, ADR need, and package shape remain architecture-review or code-review evidence.
8. Unclassified paths do not fail open; they require explicit manual routing or a later selector contract update.
9. Final broad smoke runs only when an authoritative trigger requires it.

### Token-cost measurement flow

1. Static skill measurement reads canonical skill files and reports byte size, line count, estimated token count, and largest sections where Markdown headings are available.
2. Codex JSONL session analysis reads a contributor-supplied exported session, reports token usage when present, and summarizes tool calls, command-output size, broad reads, high output caps, repeated reads, and top measured cost drivers.
3. Command-output amplification starts inside the JSONL analyzer because recorded sessions are the first evidence source for this workflow; live command wrapping remains a later optional surface.
4. The first baseline report is authored under `docs/reports/token-cost/`.
5. Change-local artifacts link to the durable baseline report when the report is produced by a change.
6. Token-cost thresholds are warning-only in the first slice and do not replace required validation, review, or workflow gates.

### Generated guidance flow

1. Canonical skill sources under `skills/` are edited.
2. Adapter entrypoint templates under `scripts/adapter_templates/` provide thin authored package guidance.
3. Existing generators refresh `.codex/skills/` and public adapter output when canonical skill guidance changes.
4. OpenCode command aliases are generated prompt wrappers for a curated lifecycle command set and remain derived from canonical skill inclusion decisions.
5. Adapter validation and release verification check manifest shape, generated file drift, release metadata, tracked release notes, smoke evidence, and security constraints.

## Deployment View

RigorLoop has no deployed service, database, or runtime infrastructure for this architecture method. The deployment boundary is repository packaging and publication.

Authored content is reviewed in Git and distributed as repository files. Generated guidance is produced from canonical sources by existing repository generators, then validated for drift before release or PR readiness. GitHub Actions do not own validation behavior; they set up execution and delegate to repository-owned scripts.

The main execution and publication boundaries are:

- local contributor shell: runs selector, CI wrapper, validation, generation, and drift checks;
- GitHub Actions: runs the same repository-owned scripts in hosted CI when configured;
- generated local Codex mirror: `.codex/skills/`, derived from canonical `skills/`;
- public adapter packages: `dist/adapters/`, derived from canonical skills and adapter templates;
- durable reports: `docs/reports/`, authored from local measurement evidence and linked from change-local artifacts when produced by a change;
- release evidence: tracked `docs/releases/<version>/release.yaml`, release notes, and maintainer smoke evidence used by release verification.

Rollback reverts the authored method artifacts, canonical package changes, templates, skill changes, generated refresh, and narrow lifecycle compatibility. No runtime data migration is required.

## Crosscutting Concepts

### Source of truth

The focused architecture package method spec owns the normative package contract. This canonical package owns current architecture shape for direct updates and for durable current truth represented from exceptional evidence. ADRs own durable decisions. Change-local deltas are not a normal architecture authoring path and never compete with the canonical package.

### Lowest sufficient architecture surface

Architecture work should choose the smallest durable surface that makes the design reviewable:

- no-impact rationale when architecture boundaries, generated-output flow, deployment, packaging, quality targets, cross-cutting rules, and durable decisions are unchanged;
- direct canonical package update when the current architecture change is clear enough to review directly;
- ADR when a durable architecture decision is introduced, superseded, or deprecated.
- proposal/spec routing when direction or behavior is not ready for architecture.

### Lifecycle status

Lifecycle-managed artifacts keep status in the artifact. Current architecture artifacts use `approved`; ADRs use the ADR lifecycle vocabulary. Terminal or historical artifacts must preserve replacement or closeout evidence where required.

### Validation layering

The selector owns routing and stable check IDs. Validation scripts own proof work. Manual review owns C4 diagram sufficiency, arc42 completeness, ADR need, and architecture package shape until a later approved automation contract changes that. Architecture support paths may select lifecycle checks for deterministic CI routing, but that routing is not architecture-package enforcement.

### Diagram source policy

Package diagrams have one authored source file and are linked from `architecture.md` by relative path. Default Mermaid diagrams use `.mmd` files under the package `diagrams/` directory. Mermaid flowchart or graph C4 diagrams use shared role classes for people, the system under review, external systems, and containers; generated images, if added later for publication, are derived output and are not edited by hand.

### Generated output

Canonical skills and adapter templates are authored sources. `.codex/skills/`, `dist/adapters/`, adapter manifests, and OpenCode command aliases are generated outputs refreshed only through existing repository generators. Generated output must not become the source for another generated surface.

### Release and adapter evidence

Release verification uses tracked `docs/releases/<version>/release.yaml` and `release-notes.md` plus maintainer smoke evidence. Generated release notes are not authoritative for adapter compatibility claims.

### Measurement reports

Reports under `docs/reports/` are durable authored evidence for longitudinal comparison. Token-cost baseline reports live under `docs/reports/token-cost/` and summarize measured static skill cost, Codex session cost, tool-output amplification, top cost drivers, conclusions, and next actions. Change-local artifacts should link to these reports rather than duplicating their body.

### Review artifact closeout

Review records are authored change-local evidence. The review artifact validator checks structure, references, allowed dispositions, and closeout completeness; it does not decide whether a finding is substantively correct.

### Security and privacy

Architecture artifacts and diagrams must not include secrets, credentials, private keys, or machine-local debug-only data. When a change affects trust boundaries, permissions, data exposure, or secret handling, the relevant architecture section and diagrams should state that explicitly.

### Legacy architecture handling

The legacy normalization follow-on inventoried every current `docs/architecture/` file, merged accepted current content into this package, and archived the eight top-level legacy Markdown records. Those legacy records remain historical evidence only; downstream architecture work uses this canonical package.

## Architecture Decisions

- `docs/adr/ADR-20260428-architecture-package-method.md`: default C4 plus official arc42 plus ADR architecture package method.
- `docs/adr/ADR-20260509-architecture-skill-surface-simplification.md`: removes change-local deltas from the normal architecture authoring path and requires architecture-review surface classification.
- `docs/adr/ADR-20260419-repository-source-layout.md`: repository source layout and canonical-source/generated-output separation.
- `docs/adr/ADR-20260424-generated-adapter-packages.md`: generated public adapter package boundary.

No additional ADR is required for the 2026-04-29 package-quality refinement because it sharpens the accepted method without changing the durable architecture decision.

## Quality Requirements

| Quality | Scenario | Measure |
| --- | --- | --- |
| Reviewability | A reviewer opens a PR that changes the canonical architecture package. | The affected arc42 sections, diagram source files, and ADR links are visible as repository text in the PR diff; no external binary diagram is required to review the change. |
| Traceability | A contributor changes architecture guidance for diagrams, skills, templates, or generated output. | The change links the accepted proposal, approved spec, canonical package update or explicit no-impact rationale, ADR decision if required, plan, test spec, and validation evidence. |
| Proportionality | A change needs architecture handling. | No-impact work records a rationale, clear current-architecture changes update this package directly, durable decisions create or update ADRs, and unsettled direction or behavior routes back to proposal or spec. |
| Determinism | Canonical skill guidance changes and generated guidance must be refreshed. | `.codex/skills/` and `dist/adapters/` are produced through existing generators and drift checks prove they match canonical sources. |
| Measurement usefulness | A contributor optimizes skill token cost. | Static skill measurement, JSONL analysis, and baseline reports identify measured cost drivers before hard token-budget gates are introduced. |
| Review closeout | Architecture-review records a material finding. | The finding includes evidence, required outcome, and a safe resolution path or `needs-decision` rationale before it drives fixes. |
| Security | Architecture work touches trust boundaries, permissions, data exposure, or secret handling. | The relevant architecture prose or diagram states the boundary, and no artifact includes secrets, credentials, private keys, or machine-local debug-only data. |

## Risks and Technical Debt

| Risk or debt | Current handling |
| --- | --- |
| Archived legacy architecture documents can be mistaken for current architecture truth | Each archived record points to this canonical package, and final closeout validation covers every changed legacy document. |
| First implementation relies on review rather than structural package enforcement | Approved spec intentionally defers enforcement automation until a real package proves the shape. |
| C4 context and container views may be too coarse for future module-level changes | Add component diagrams only when container-level structure no longer explains affected responsibilities. |
| Architecture work can overproduce change-local deltas | Deltas are no longer a normal architecture authoring path; use no-impact rationale, direct canonical update, ADR, or proposal/spec routing instead. |
| Historical or exceptional change-local evidence could be mistaken for current truth | Architecture-review, code-review, and verify must treat durable current architecture truth outside the canonical package as incomplete. |
| Architecture-review finding format could be mistaken for a replacement of material-finding closeout | The focused spec and this package keep the simple finding fields separate from the repository-wide material-finding contract. |
| Token-cost reports could expose excessive transcript or command-output content | Measurement reports summarize cost drivers and avoid embedding unnecessary raw transcript content. |
| Warning-only token budgets could be mistaken for CI gates | The first measurement slice treats budget thresholds as report warnings; hard gates require a later accepted proposal and spec. |

## Glossary

- ADR: architecture decision record that preserves a durable decision, alternatives, consequences, and follow-up.
- arc42: the 12-section architecture documentation model used by `architecture.md`.
- C4: context, container, component, and code-level structural diagram model.
- canonical architecture package: the long-lived current architecture source under `docs/architecture/system/`.
- change-local architecture delta: historical or explicitly exceptional evidence under `docs/changes/<change-id>/`; not part of the normal architecture authoring path.
- generated output: derived files under `.codex/skills/` and `dist/adapters/`.
- lowest sufficient architecture surface: the smallest architecture evidence surface that truthfully handles a change: no-impact rationale, direct canonical update, ADR, or proposal/spec routing.
- material finding: review finding that must include evidence, required outcome, and safe resolution path or `needs-decision` rationale before it drives fixes.
- non-enforcement lifecycle routing: selector-selected validation that checks artifact lifecycle compatibility without proving C4 sufficiency, arc42 completeness, ADR need, or architecture package shape.
- report: durable authored evidence under `docs/reports/` used for longitudinal comparison, such as token-cost baselines.
- review artifact: authored change-local review evidence such as `reviews/*.md`, `review-log.md`, or `review-resolution.md`.

## Next artifacts

- Implementation of the active simplification plan milestones.

## Follow-on artifacts

- Legacy architecture lifecycle normalization: completed; top-level legacy architecture records are archived historical evidence.
- Architecture-review for the 2026-04-29 package-quality refinement: approved on 2026-04-29 with no findings.
- Architecture-review for the 2026-05-08 workflow-governance direct canonical package update: approved in `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/architecture-review-r1.md` with no material findings.
- Plan-review for the 2026-04-29 package-quality refinement: approved on 2026-04-29 after PR-F1 corrected M5 sequencing.
- Plan-review for the 2026-05-08 workflow-governance execution plan: approved in `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/plan-review-r2.md` with no material findings.
- Test spec update: `specs/architecture-package-method.test.md` active on 2026-04-29 for R76-R118 and AC14-AC20.
- Architecture skill surface simplification: proposal accepted and spec amendment approved on 2026-05-09; canonical architecture and ADR update approved in this package revision.
- Architecture-review for the 2026-05-09 architecture skill surface simplification: approved in `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/architecture-review-r1.md` with no material findings.
- Plan-review for the 2026-05-09 architecture skill surface simplification: approved in `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/plan-review-r2.md` after PR-F1 corrected milestone review sequencing.
- Token-cost measurement baseline and proposal scope preservation: accepted proposal and approved spec add repository-local measurement scripts, token-cost baseline reports under `docs/reports/token-cost/`, and proposal/proposal-review scope-preservation guidance.

## Readiness

This canonical package revision records the current repository architecture for token-cost measurement baselines and proposal scope preservation.

No ADR is required for this update because it does not revise system boundaries, generated-output architecture, adapter packaging, deployment boundaries, or the architecture method. No change-local architecture delta is produced because the canonical package carries the intended durable guidance directly.
