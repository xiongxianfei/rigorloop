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
- Release Token-Friendliness benchmark proposal: `docs/proposals/2026-05-10-release-token-friendliness-benchmark-for-skills.md`
- Release Token-Friendliness benchmark spec: `specs/release-token-friendliness-benchmark-for-skills.md`
- Release Token-Friendliness benchmark change metadata: `docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml`
- Expanded dynamic Token-Friendliness benchmark proposal: `docs/proposals/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Expanded dynamic Token-Friendliness benchmark spec: `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Expanded dynamic Token-Friendliness benchmark change metadata: `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`
- Single Authored Skill Source proposal: `docs/proposals/2026-05-12-single-authored-skill-source-and-generated-adapter-output-cleanup.md`
- Single Authored Skill Source spec: `specs/single-authored-skill-source-generated-output.md`
- Generated output migration ADR: `docs/adr/ADR-20260512-generated-skill-output-release-artifacts.md`
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
- keep `skills/` as the only authored skill source while moving local and public generated skill copies out of ordinary authored Git state in staged releases;
- make public release skill token-friendliness measurable through release reports, structured metadata, and fixture-backed runtime benchmarks;
- make dynamic token-friendliness coverage visible across the core delivery workflow without requiring every optional skill benchmark for every release;
- keep first adoption and package-quality refinement review-based until real package usage proves which checks are worth automating.

## Architecture Constraints

- `CONSTITUTION.md` is the highest-priority repository governance artifact below external runtime instructions.
- `specs/architecture-package-method.md` owns the C4, arc42, ADR, template, canonical-package, architecture-surface, and historical change-local evidence contract.
- `specs/rigorloop-workflow.md` owns only workflow stage routing and handoff language for this method.
- The canonical package path is `docs/architecture/system/architecture.md` with default diagrams under `docs/architecture/system/diagrams/`.
- Architecture and ADR scaffolds live under `templates/`; live architecture and ADR records live under `docs/architecture/` and `docs/adr/`.
- Architecture work uses the lowest sufficient architecture surface: no-impact rationale for changes with no architecture impact, direct canonical package update for clear current-architecture changes, ADR when a durable decision is introduced or revised, and proposal/spec routing when direction or behavior is not ready.
- Change-local architecture deltas are not part of the normal architecture authoring path. Existing deltas remain historical evidence, and new deltas are limited to legacy closeout or explicit exceptional evidence.
- `skills/` is the only authored skill source.
- `.codex/skills/` is generated local Codex runtime output and must not be hand-edited or required as tracked Git state after its migration slice.
- Public adapter skill copies under `dist/adapters/**/skills` are generated adapter output and remain tracked only until the release-artifact compatibility window is satisfied.
- `dist/adapters/manifest.yaml`, `dist/adapters/README.md`, and `docs/reports/adapter-artifacts/releases/<version>.yaml` are tracked support and release evidence surfaces; generated adapter archives are release assets rather than committed repository files by default.
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
- generated Codex runtime skills, public adapter packages, adapter manifests, adapter install guidance, adapter artifact metadata, release asset archives, and command aliases;
- authored release metadata, tracked release notes, and maintainer smoke evidence;
- token-cost benchmark prompts, clean fixtures, runner-produced run evidence, analyzer summaries, and release token-friendliness reports;
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
| Token-cost benchmark fixtures and reports | Carry executable benchmark prompts, clean downstream fixtures, raw or sanitized run evidence, analyzer summaries, and longitudinal token-friendliness reports | Markdown/YAML/JSONL under `benchmarks/token-cost/` and `docs/reports/token-cost/` |
| Canonical architecture package | Long-lived current architecture source of truth, including arc42 prose and C4 diagram source | Markdown and Mermaid in `docs/architecture/system/` |
| Change-local evidence | Historical architecture evidence, explicit exceptional architecture evidence, change metadata, explanation, review resolution, and verification evidence | Markdown/YAML in `docs/changes/<change-id>/` |
| Templates and diagram styles | Canonical scaffolding for architecture, ADRs, and shared Mermaid C4 role styling | Markdown/Mermaid under `templates/` |
| Canonical skills and adapter templates | Source instructions for workflow stages and thin adapter entrypoints | Markdown in `skills/`, templates in `scripts/adapter_templates/` |
| Validation and generation scripts | Select checks, validate artifacts, refresh generated output, and prove drift status | Python and shell under `scripts/` |
| Generated runtime mirrors and adapters | Derived Codex runtime skills and public adapter packages for supported agent tools; local mirrors and public adapter skill bodies are not authored sources | Generated files under `.codex/skills/`, tracked adapter metadata under `dist/adapters/`, and release asset archives |
| Release evidence | Authored release contract, notes, adapter artifact metadata, checksums, and maintainer smoke evidence | YAML/Markdown under `docs/releases/<version>/` and `docs/reports/adapter-artifacts/releases/` |
| Legacy architecture archive | Historical architecture records retained after accepted current content is merged here | Archived Markdown under `docs/architecture/*.md` |

### Level 2 White-Box: Validation and Generation Scripts

The validation and generation container has four important internal responsibilities:

- selector and CI wrapper: `scripts/validation_selection.py`, `scripts/select-validation.py`, and `scripts/ci.sh` classify paths, select stable check IDs, and run repository-owned proof commands;
- lifecycle and change validators: `scripts/validate-artifact-lifecycle.py`, `scripts/validate-change-metadata.py`, and `scripts/validate-review-artifacts.py` validate artifact status, change metadata, and material review closeout structure;
- skill and adapter generation: `scripts/build-skills.py`, `scripts/build-adapters.py`, and adapter distribution helpers generate `.codex/skills/`, public adapter output, and release artifact outputs from canonical sources;
- release and adapter validation: `scripts/validate-adapters.py`, `scripts/validate-release.py`, and `scripts/release-verify.sh` check generated packages, manifests, release metadata, adapter artifact metadata, tracked release notes, checksums, and smoke evidence.
- measurement, benchmark, and reporting scripts: repository-local commands measure skill size, run token-cost benchmark prompts in disposable fixtures, analyze Codex JSONL session exports, summarize tool-output amplification, validate token-cost release metadata, and produce reviewable evidence for reports without requiring hosted telemetry.
- required-benchmark context: release validation determines the release-specific required dynamic benchmark set from core suite policy, transition carryover policy, changed public skills, and claimed optional coverage, then passes that context to token-cost validation in process or through a transient YAML file for CLI and debugging use.

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

### Release Token-Friendliness benchmark flow

1. A maintainer preparing a public release runs static skill measurement and the tracked benchmark suite under `benchmarks/token-cost/`.
2. For `skill-token-runtime-v2`, release validation determines the effective required dynamic benchmark set from required core benchmarks, one-release transition carryover benchmarks, changed public skill benchmarks, and optional benchmarks that are explicitly claimed as release coverage.
3. Release validation passes that required benchmark context to token-cost validation in process. The standalone validator may receive the same context as YAML through `--required-benchmark-context`; that YAML is normally transient and tracked only when it becomes release decision evidence.
4. The benchmark runner copies the clean minimal downstream fixture into an isolated temporary directory outside the repository.
5. For Codex benchmarks, the runner installs current public Codex adapter skills from tracked public adapter output while that output remains tracked, or from generated temporary adapter output or release artifact output after public adapter skill copies move out of tracked Git. The runner does not use repository-local `.codex/skills/` as the public benchmark source.
6. The runner executes prompt fixtures with `codex exec --json --ephemeral`, writes raw JSONL under `docs/reports/token-cost/runs/<release-version>/` when raw JSONL is tracked, and invokes the JSONL analyzer automatically.
7. Analyzer summaries are written beside run evidence and carry structured usage, tool-output, signal, verdict, and raw-or-sanitized evidence identity fields.
8. Maintainers manually review `skill-token-runtime-v2` benchmark result quality and record structured criteria for each dynamic run until stable expected-output checks justify automation.
9. Maintainers write a human-readable Markdown report and structured YAML metadata under `docs/reports/token-cost/releases/<release-version>.md` and `.yaml`.
10. `scripts/validate-token-cost-report.py` validates the token-cost metadata schema, waiver fields, run references, runner metadata, portability status, raw-or-sanitized evidence, result-quality evidence, required benchmark coverage, optional warning evidence, claimed optional coverage, and comparison shape.
11. Release validation delegates token-cost report validation before public release readiness is claimed.

### Generated guidance flow

1. Canonical skill sources under `skills/` are edited.
2. Adapter entrypoint templates under `scripts/adapter_templates/` provide thin authored package guidance.
3. Existing generators produce `.codex/skills/` and public adapter output from canonical skill guidance. After `.codex/skills/` is untracked, local mirror validation uses temp-output generation rather than tracked-file drift comparison.
4. OpenCode command aliases are generated prompt wrappers for a curated lifecycle command set and remain derived from canonical skill inclusion decisions.
5. While public adapter skill copies remain tracked, adapter validation and release verification keep checking tracked adapter drift.
6. Release artifact preparation generates separate per-adapter archives, optionally a combined all-adapters archive, and tracked adapter artifact metadata under `docs/reports/adapter-artifacts/releases/<version>.yaml`.
7. After public adapter skill copies move to release artifacts, adapter validation checks generated temporary or release artifact output instead of tracked public skill-copy drift.
8. Release validation checks manifest shape, generated output structure, artifact metadata, checksums, tracked release notes, smoke evidence, and security constraints.

## Deployment View

RigorLoop has no deployed service, database, or runtime infrastructure for this architecture method. The deployment boundary is repository packaging and publication.

Authored content is reviewed in Git and distributed as repository files. Generated guidance is produced from canonical sources by existing repository generators. Tracked generated surfaces are validated for drift while they remain tracked; untracked generated surfaces are validated through temporary output or release artifact output. GitHub Actions do not own validation behavior; they set up execution and delegate to repository-owned scripts.

The main execution and publication boundaries are:

- local contributor shell: runs selector, CI wrapper, validation, generation, and drift checks;
- GitHub Actions: runs the same repository-owned scripts in hosted CI when configured;
- generated local Codex mirror: `.codex/skills/`, derived from canonical `skills/` and generated on demand after its untracking slice;
- public adapter packages: tracked `dist/adapters/` output during the compatibility window, then generated release artifact output after public adapter skill copies are untracked;
- adapter support metadata: `dist/adapters/manifest.yaml` and `dist/adapters/README.md`, tracked guidance and support surfaces rather than authored skill bodies;
- adapter artifact metadata: `docs/reports/adapter-artifacts/releases/<version>.yaml`, tracked release evidence with source commit, generator command, artifact list, checksums, and validation result;
- adapter release artifacts: generated per-adapter archives, plus optional combined archive, uploaded as release assets rather than committed by default;
- durable reports: `docs/reports/`, authored from local measurement evidence and linked from change-local artifacts when produced by a change;
- token-cost benchmark fixtures: `benchmarks/token-cost/`, authored prompt and fixture inputs used to exercise public skills in a downstream-style project;
- token-cost temporary runs: isolated directories under system temp or `$RUNNER_TEMP`, disposable and not durable release evidence;
- token-cost release evidence: `docs/reports/token-cost/releases/<version>.md`, `docs/reports/token-cost/releases/<version>.yaml`, and tracked raw or sanitized run summaries under `docs/reports/token-cost/runs/<version>/`;
- release evidence: tracked `docs/releases/<version>/release.yaml`, release notes, and maintainer smoke evidence used by release verification.

Rollback before public adapter skill-copy untracking can restore tracked local mirror handling by reverting ignore, validation, documentation, and generation changes for that slice. Rollback after public adapter skill-copy untracking preserves generation from `skills/` and either re-tracks generated adapter output temporarily or republishes release artifacts from last known good generated output. No runtime data migration is required.

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

Canonical skills and adapter templates are authored sources. `.codex/skills/`, public adapter skill copies, adapter archives, and OpenCode command aliases are generated outputs produced only from canonical sources and approved templates or metadata. Generated output must not become the source for another generated surface.

After `.codex/skills/` is untracked, local Codex mirror validation proves generation into a non-tracked output surface rather than tracked-file equality. Public adapter skill copies stay tracked until at least one stable public release has shipped downloadable adapter artifacts and release-artifact installation docs. After that compatibility window, public adapter skill-copy drift checks move to temp-output or release-artifact validation.

### Release and adapter evidence

Release verification uses tracked `docs/releases/<version>/release.yaml` and `release-notes.md` plus maintainer smoke evidence. Generated release notes are not authoritative for adapter compatibility claims.

Generated adapter releases have an additional artifact evidence layer. `docs/reports/adapter-artifacts/releases/<version>.yaml` records release version, source commit, generator command, canonical source, manifest path, generated archive names, SHA-256 checksums, validation command, and validation result. Public releases that distribute generated adapters publish separate per-adapter archives as release assets and may publish a combined archive for convenience. The repository tracks metadata and checksums, not generated archive files by default.

### Release token-friendliness evidence

Public releases add a token-friendliness evidence layer beside adapter release evidence. Markdown reports are for reviewers; YAML metadata is for release gates. The first required runtime benchmark is Codex; Claude Code and opencode dynamic benchmarks remain optional until stable runners and comparable reports exist. Final public releases require `dynamic_runtime.status: pass` or a valid approved waiver. RC and draft reports may record `blocked` or `not-run` dynamic status only with structured incomplete-state metadata.

Raw Codex JSONL may be omitted when it is too large or sensitive, but durable evidence must remain structured through analyzer summaries or sanitized summaries. Release validation checks for raw JSONL or a valid sanitized substitute, not raw JSONL unconditionally.

`skill-token-runtime-v2` expands dynamic coverage with a required core suite, one-release transition carryover benchmarks, optional extended benchmarks, and changed-skill-required benchmarks. Optional benchmark problems remain warnings unless the benchmark is required by changed-skill policy or explicitly claimed as release coverage. Claimed optional coverage is gated coverage: missing, invalid, failed, not reviewed, or unwaived inconclusive claimed results block final release.

Release validation owns changed public skill detection and generated-adapter-to-canonical-skill tracing. Token-cost validation owns proving that the report satisfies the required benchmark context supplied by release validation.

Manual result-quality review is structured release evidence for v2. Required or claimed coverage must have passing result quality or a valid role-scoped waiver. Optional unclaimed failures and inconclusive results use stable warning codes and must not be summarized as passing coverage.

### Measurement reports

Reports under `docs/reports/` are durable authored evidence for longitudinal comparison. Token-cost reports live under `docs/reports/token-cost/` and summarize measured static skill cost, Codex session cost, tool-output amplification, top cost drivers, conclusions, and next actions. Release token-friendliness reports live under `docs/reports/token-cost/releases/` and compare against the previous public release report when one exists or declare the first report as the baseline. Change-local artifacts should link to these reports rather than duplicating their body.

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
- `docs/adr/ADR-20260512-generated-skill-output-release-artifacts.md`: staged migration from tracked generated skill mirrors to untracked local mirrors and generated release artifacts.

No additional ADR is required for the 2026-04-29 package-quality refinement because it sharpens the accepted method without changing the durable architecture decision.

## Quality Requirements

| Quality | Scenario | Measure |
| --- | --- | --- |
| Reviewability | A reviewer opens a PR that changes the canonical architecture package. | The affected arc42 sections, diagram source files, and ADR links are visible as repository text in the PR diff; no external binary diagram is required to review the change. |
| Traceability | A contributor changes architecture guidance for diagrams, skills, templates, or generated output. | The change links the accepted proposal, approved spec, canonical package update or explicit no-impact rationale, ADR decision if required, plan, test spec, and validation evidence. |
| Proportionality | A change needs architecture handling. | No-impact work records a rationale, clear current-architecture changes update this package directly, durable decisions create or update ADRs, and unsettled direction or behavior routes back to proposal or spec. |
| Determinism | Canonical skill guidance changes and generated guidance must be refreshed. | Generated local mirrors, public adapter output, and adapter release artifacts are produced from `skills/` through repository generators; tracked generated surfaces use drift checks and untracked generated surfaces use temp-output or release-artifact validation. |
| Adapter artifact reproducibility | A maintainer publishes generated adapter archives. | Tracked adapter artifact metadata records source commit, generator command, archive names, SHA-256 checksums, validation command, and validation result. |
| Measurement usefulness | A contributor optimizes skill token cost. | Static skill measurement, JSONL analysis, and baseline reports identify measured cost drivers before hard token-budget gates are introduced. |
| Release token-friendliness | A maintainer prepares a public release. | Markdown and YAML token-friendliness reports exist under `docs/reports/token-cost/releases/`, Codex benchmark evidence or a valid waiver is recorded, portability passes, and release validation delegates to the token-cost report validator. |
| Dynamic benchmark coverage | A maintainer prepares a public release with `skill-token-runtime-v2`. | The report records required core coverage, transition carryover coverage when applicable, changed-skill-required coverage, claimed optional coverage, optional warnings, and per-run result-quality evidence. |
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
| Raw Codex JSONL could expose sensitive local paths or output | Release metadata supports sanitized summaries, and analyzer summaries do not require private raw JSONL paths when raw evidence is intentionally omitted. |
| Benchmark runners could accidentally measure the repository-local Codex mirror instead of public adapter output | The release benchmark installs public Codex skills from tracked public adapter output while available, generated temporary adapter output, or release artifact output, and rejects `.codex/skills/` as the public benchmark source. |
| Release metadata can become prose-only or unreproducible | Structured YAML records runner invocation, fixture source, public skill source, run evidence, waiver state, and comparison data; release validation reads YAML rather than Markdown prose. |
| Users rely on copying public adapter skills from the repository tree | Public adapter skill copies remain tracked for at least one stable public release after downloadable adapter artifacts and install docs are available; release notes announce the repository-tree install transition. |
| Generated adapter archives could create binary churn in Git | Generated archives are release assets by default; Git tracks artifact metadata and checksums instead of archive files. |
| Warning-only token budgets could be mistaken for CI gates | The first measurement slice treats budget thresholds as report warnings; hard gates require a later accepted proposal and spec. |
| Optional benchmark failures could be mistaken for passing release coverage | `skill-token-runtime-v2` separates optional warning evidence from claimed optional release coverage; claimed coverage follows required benchmark evidence and result-quality gates. |

## Glossary

- ADR: architecture decision record that preserves a durable decision, alternatives, consequences, and follow-up.
- arc42: the 12-section architecture documentation model used by `architecture.md`.
- C4: context, container, component, and code-level structural diagram model.
- canonical architecture package: the long-lived current architecture source under `docs/architecture/system/`.
- change-local architecture delta: historical or explicitly exceptional evidence under `docs/changes/<change-id>/`; not part of the normal architecture authoring path.
- generated output: derived files under `.codex/skills/`, public adapter skill paths under `dist/adapters/`, generated adapter archives, and generated command aliases.
- adapter artifact metadata: tracked YAML under `docs/reports/adapter-artifacts/releases/<version>.yaml` that records source commit, generator command, archive paths, checksums, and validation evidence for generated adapter release artifacts.
- artifact-install path: installing adapter packages from downloadable release assets rather than copying generated skill bodies from the repository tree.
- release token-friendliness metadata: structured YAML under `docs/reports/token-cost/releases/` that gates public release token-cost evidence.
- required benchmark context: release-validation input that identifies required core, transition carryover, and changed-skill-required dynamic benchmarks for a release.
- result quality: structured manual or future automated evidence that a dynamic benchmark response followed the prompt and made correct readiness or handoff claims.
- token-cost benchmark fixture: prompt and minimal downstream-project inputs under `benchmarks/token-cost/` used by the benchmark runner.
- token-cost benchmark runner: repository-owned script that installs public adapter skills into a temporary fixture, runs prompt fixtures, and invokes the JSONL analyzer.
- lowest sufficient architecture surface: the smallest architecture evidence surface that truthfully handles a change: no-impact rationale, direct canonical update, ADR, or proposal/spec routing.
- material finding: review finding that must include evidence, required outcome, and safe resolution path or `needs-decision` rationale before it drives fixes.
- non-enforcement lifecycle routing: selector-selected validation that checks artifact lifecycle compatibility without proving C4 sufficiency, arc42 completeness, ADR need, or architecture package shape.
- report: durable authored evidence under `docs/reports/` used for longitudinal comparison, such as token-cost baselines.
- review artifact: authored change-local review evidence such as `reviews/*.md`, `review-log.md`, or `review-resolution.md`.

## Next artifacts

- `architecture-review` for the generated skill output and adapter release artifact architecture update.

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
- Release Token-Friendliness benchmark for skills: accepted proposal and approved spec add fixture-backed release token-cost benchmarking, structured release metadata, public-skill-source benchmark installation, analyzer summaries, raw-or-sanitized run evidence, waiver handling, and token-cost release validation delegation.
- Expanded dynamic Token-Friendliness benchmarks for core skills: accepted proposal and approved spec define `skill-token-runtime-v2`, required core coverage, transition carryover coverage, optional extended coverage, changed-skill-required benchmarks, claimed optional coverage gates, required benchmark context, and structured result-quality evidence.
- Single Authored Skill Source and Generated Output: accepted proposal and approved spec define `skills/` as the only authored skill source, untracked `.codex/skills/` local mirror generation, staged public adapter artifact migration, adapter artifact metadata, and temp-output validation for untracked generated trees.

## Readiness

This canonical package revision records the current repository architecture for generated skill output and adapter release artifact migration.

ADR `docs/adr/ADR-20260512-generated-skill-output-release-artifacts.md` records the durable decision to move generated local and public skill copies out of ordinary authored Git state through staged temp-output and release-artifact validation. No change-local architecture delta is produced because the canonical package carries the intended durable guidance directly.
