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
- Publish Next Release transition proposal: `docs/proposals/2026-05-12-publish-next-release-with-single-authored-skill-source.md`
- Publish Next Release transition spec: `specs/publish-next-release-with-single-authored-skill-source.md`
- Publish Next Release transition change metadata: `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/change.yaml`
- Public Adapter Artifact Migration proposal: `docs/proposals/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md`
- Public Adapter Artifact Migration spec: `specs/public-adapter-artifact-migration-examples-concise-skill-release.md`
- Public Adapter Artifact Migration change metadata: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml`
- Stop Tracking Generated Public Adapter Skill Bodies proposal: `docs/proposals/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md`
- Stop Tracking Generated Public Adapter Skill Bodies spec: `specs/stop-tracking-generated-public-adapter-skill-bodies.md`
- Stop Tracking Generated Public Adapter Skill Bodies change metadata: `docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/change.yaml`
- v0.1.3 adapter release archive install ADR: `docs/adr/ADR-20260513-v0-1-3-adapter-release-archive-install-surface.md`
- RigorLoop Scaffolding CLI proposal: `docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md`
- RigorLoop CLI Package and Codex Init spec: `specs/rigorloop-cli-package-and-codex-init.md`
- RigorLoop CLI Package and Codex Init ADR: `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md`
- RigorLoop CLI Package and Codex Init change metadata: `docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml`
- RigorLoop CLI Lockfile spec: `specs/rigorloop-cli-lockfile.md`
- RigorLoop CLI Lockfile ADR: `docs/adr/ADR-20260516-rigorloop-cli-lockfile.md`
- RigorLoop CLI Lockfile change metadata: `docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml`
- RigorLoop CLI New Change spec: `specs/rigorloop-cli-new-change.md`
- RigorLoop CLI New Change change metadata: `docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
- RigorLoop npm Publication proposal: `docs/proposals/2026-05-16-first-public-npm-release.md`
- RigorLoop npm Publication spec: `specs/rigorloop-npm-publication.md`
- RigorLoop npm Publication ADR: `docs/adr/ADR-20260516-rigorloop-npm-publication.md`
- RigorLoop npm Publication change metadata: `docs/changes/2026-05-16-first-public-npm-release/change.yaml`
- Multi-Adapter Init and Proxy-Aware Adapter Download proposal: `docs/proposals/2026-05-18-multi-adapter-init-and-proxy-aware-download.md`
- Multi-Adapter Init and Proxy-Aware Adapter Download spec: `specs/multi-adapter-init-and-proxy-aware-download.md`
- Multi-Adapter Init and Proxy-Aware Adapter Download ADR: `docs/adr/ADR-20260518-multi-adapter-init-and-proxy-download.md`
- Multi-Adapter Init and Proxy-Aware Adapter Download change metadata: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/change.yaml`
- Script Output Optimization proposal: `docs/proposals/2026-05-21-script-output-optimization.md`
- Script Output Optimization spec: `specs/script-output-optimization.md`
- Record Every Formal Review proposal: `docs/proposals/2026-05-12-record-every-formal-review.md`
- Formal Review Recording spec: `specs/formal-review-recording.md`
- Record Every Formal Review change metadata: `docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml`
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
- add a small CLI package boundary that scaffolds projects and installs verified Codex release archives without becoming a second source of truth;
- let the CLI record verified generated Codex adapter output in a downstream `rigorloop.lock` without making the lockfile canonical workflow, skill, schema, release, or adapter metadata;
- extend CLI adapter init through descriptors for Codex, Claude Code, and opencode while preserving Codex `.agents/skills`, strict release-archive verification, and local archive fallback;
- let the CLI record mixed single-root and multi-root generated adapter output in `rigorloop.lock` schema v2 without making downstream lockfiles canonical adapter metadata;
- improve enterprise-network recovery through bounded proxy diagnostics while deferring programmatic proxy dispatcher support;
- let the CLI scaffold a draft change-local artifact pack for `docs/changes/<change-id>/change.yaml` without claiming lifecycle stage completion or creating durable-looking placeholder artifacts;
- publish the first public `@xiongxianfei/rigorloop` npm package only through a reviewable release-hardening boundary that preserves npm as delivery, not source of truth;
- make public release skill token-friendliness measurable through release reports, structured metadata, and fixture-backed runtime benchmarks;
- make dynamic token-friendliness coverage visible across the core delivery workflow without requiring every optional skill benchmark for every release;
- keep repository script output proportional to actionability: compact on success, specific on failure, and expandable through explicit verbose modes;
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
- `.codex/skills/` is ignored local Codex runtime state and must not be hand-edited, required as tracked Git state, or treated as release evidence after its migration slice.
- Public adapter skill copies under `dist/adapters/**/skills` are generated adapter output and remain tracked only until the release-artifact compatibility window is satisfied.
- `dist/adapters/manifest.yaml`, `dist/adapters/README.md`, and `docs/reports/adapter-artifacts/releases/<version>.yaml` are tracked support and release evidence surfaces; generated adapter archives are release assets rather than committed repository files by default.
- The `v0.1.1` transition release validates canonical `skills/`, tracked public adapter output under `dist/adapters/`, release notes, adapter install guidance, and token-cost metadata; it does not build or validate `.codex/skills/` as release evidence.
- The `v0.1.2` archive-introduction release publishes per-adapter release archives for Codex, Claude Code, and opencode while keeping tracked public adapter skill bodies available for the stable compatibility window.
- The first public adapter untracking release occurs only after at least one stable release has shipped downloadable adapter archives and release-archive install documentation, unless an approved compatibility-window exception explicitly says otherwise.
- For `v0.1.3` and later, release archives are the active public adapter install surface. Generated adapter skill bodies, generated adapter instruction entrypoints, and generated opencode command wrappers are release or temporary output, not tracked package fragments under `dist/adapters/<adapter>/`.
- The first RigorLoop CLI package candidate is `@xiongxianfei/rigorloop` with one public binary, `rigorloop`.
- The completed first CLI slice was limited to help, version, and `init --adapter codex` with dry-run JSON, safe `rigorloop.yaml` generation, verified Codex adapter archive installation, and planned lockfile output only.
- The next CLI scaffolding slice adds `rigorloop new-change <change-id>` to create `docs/changes/<change-id>/change.yaml` only. It must not create `explain-change.md`, review artifacts, plans, specs, proposals, lockfiles, adapters, or any lifecycle artifact that would imply a later stage has completed.
- The CLI package may contain CLI code, small scaffolds, and bundled official adapter metadata for the package's compatible Codex adapter release. It must not contain adapter archives as authored npm source or generated adapter skill bodies as canonical source.
- `rigorloop init --adapter codex --from-archive <path>` verifies local archives against bundled adapter metadata shipped with the installed CLI package version and does not require a separate user metadata path in the first slice.
- `rigorloop init` may write durable `rigorloop.lock` only for the approved Codex lockfile-writing surface after archive verification, extraction safety checks, generated-output mutation, installed-tree verification, and lockfile shape validation have succeeded.
- `rigorloop.lock` records verified generated Codex adapter output state in a downstream project. It is not canonical workflow content, canonical skill content, release metadata, adapter metadata, or validation authority.
- The first lockfile schema is strict: unknown top-level sections, unknown fields, unsupported schemas, unsupported adapters, unsupported source values, and unsupported tree hash algorithms block before mutation.
- The multi-adapter init slice extends the existing CLI package boundary to `init --adapter codex`, `init --adapter claude`, and `init --adapter opencode` through explicit adapter descriptors.
- Codex remains a single-root `.agents/skills` adapter; the CLI must not migrate Codex output to `.codex/skills`.
- Claude Code is a single-root `.claude/skills` adapter. opencode is a possible multi-root adapter with `.opencode/skills` and `.opencode/commands`.
- Trusted CLI-bundled metadata determines required opencode roots. Older compatible opencode archives without `command_aliases.opencode` may install skills only with warning code `opencode-command-aliases-not-declared`.
- Multi-adapter lockfiles use `schema_version: 2`; existing schema v1 Codex lockfiles remain readable and may be upgraded only after drift checks pass.
- First-slice proxy behavior uses Node built-in env-proxy support only when the runtime supports and enables it. Programmatic Undici proxy dispatcher support is out of scope until a later approved change.
- Public npm publication of `@xiongxianfei/rigorloop@0.1.4` is allowed only through the approved npm publication slice: package-content allowlist, lifecycle-script and dependency policy, exactly one publication mode, publication evidence, packed-package smoke, and real Codex adapter install proof.
- Normal npm publication uses trusted publishing through `.github/workflows/release.yml`. One-time bootstrap publication may be used only for `@xiongxianfei/rigorloop@0.1.4` if trusted publishing cannot be configured before package creation, and it may publish only the exact verified tarball recorded in publication evidence.
- After the `v0.1.3` adapter untracking migration, the tracked default adapter support surface under `dist/adapters/` is limited to `README.md` and `manifest.yaml` unless a later approved spec explicitly names more tracked metadata or templates.
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
| RigorLoop CLI package | Provides the `rigorloop` binary, project scaffolding, change metadata scaffolding, stable human/JSON command envelopes, bundled adapter metadata, verified adapter archive installation for supported adapters, proxy-safe download diagnostics, and durable lockfile writes for verified generated adapter output | Node/npm package under `packages/rigorloop`, published as `@xiongxianfei/rigorloop` only through the approved npm publication boundary |
| Canonical architecture package | Long-lived current architecture source of truth, including arc42 prose and C4 diagram source | Markdown and Mermaid in `docs/architecture/system/` |
| Change-local evidence | Historical architecture evidence, explicit exceptional architecture evidence, change metadata, explanation, review resolution, and verification evidence | Markdown/YAML in `docs/changes/<change-id>/` |
| Templates and diagram styles | Canonical scaffolding for architecture, ADRs, and shared Mermaid C4 role styling | Markdown/Mermaid under `templates/` |
| Canonical skills and adapter templates | Source instructions for workflow stages and thin adapter entrypoints | Markdown in `skills/`, templates in `scripts/adapter_templates/` |
| Validation and generation scripts | Select checks, validate artifacts, refresh generated output, and prove drift status | Python and shell under `scripts/` |
| Generated runtime state and adapters | Derived local Codex runtime state and public adapter packages for supported agent tools; local runtime state and public adapter packages are generated from canonical sources and are not authored sources | Ignored local files under `.codex/skills/`, tracked adapter support metadata under `dist/adapters/`, generated temporary or release-output package directories, and release asset archives |
| Release evidence | Authored release contract, notes, adapter artifact metadata, package publication evidence, checksums, and maintainer smoke evidence | YAML/Markdown under `docs/releases/<version>/` and `docs/reports/adapter-artifacts/releases/` |
| Legacy architecture archive | Historical architecture records retained after accepted current content is merged here | Archived Markdown under `docs/architecture/*.md` |

### Level 2 White-Box: RigorLoop CLI Package

The CLI package remains an additive delivery container. For multi-adapter init, it has these internal architecture responsibilities:

- command parsing and output envelope: keeps help, version, `init`, `new-change`, JSON, human output, warnings, blockers, errors, and exit-code mapping stable;
- adapter descriptor registry: maps supported adapter names to archive filename patterns, possible install roots, manifest shape, and lockfile shape;
- bundled metadata trust root: reads the package-bundled release index and adapter metadata, verifies metadata hashes before use, and selects only package-compatible releases;
- archive acquisition: chooses network download from the trusted official GitHub release URL or local archive bytes from `--from-archive`;
- proxy diagnostics: classifies network download failures and reports only safe diagnostic fields without raw proxy values or credentials;
- archive verifier and extractor: checks archive filename, adapter identity, release, size, SHA-256, traversal safety, symlink policy, expected roots, and installed tree hashes;
- project manifest writer: creates or updates `rigorloop.yaml` with single-root `install_root` or multi-root `install_roots` entries only after verification succeeds;
- lockfile parser and serializer: reads existing schema v1/v2 lockfiles, checks drift before replacement, and writes schema v2 generated adapter entries after installed output verifies;
- generated-output mutation planner: plans root creation and file writes before mutation, refuses unsafe conflicts, and reports partial failures without claiming success.

### Level 2 White-Box: Validation and Generation Scripts

The validation and generation container has these important internal responsibilities:

- selector and CI wrapper: `scripts/validation_selection.py`, `scripts/select-validation.py`, and `scripts/ci.sh` classify paths, select stable check IDs, run repository-owned proof commands, summarize successful selected checks, and surface failed check output with stable check identity;
- lifecycle and change validators: `scripts/validate-artifact-lifecycle.py`, `scripts/validate-change-metadata.py`, and `scripts/validate-review-artifacts.py` validate artifact status, change metadata, and material review closeout structure;
- skill and adapter generation: `scripts/build-skills.py`, `scripts/build-adapters.py`, and adapter distribution helpers generate local runtime state, public adapter output, and release artifact outputs from canonical sources;
- release and adapter validation: `scripts/validate-adapters.py`, `scripts/validate-release.py`, and `scripts/release-verify.sh` check generated packages, manifests, release metadata, adapter artifact metadata, tracked release notes, checksums, and smoke evidence. For public releases, `release-verify.sh` is the maintainer-facing gate and `validate-release.py` owns structured release validation delegated from that gate. For `v0.1.3` and later, these checks validate generated temporary or release-output adapter packages and release archives instead of tracked adapter package trees.
- measurement, benchmark, and reporting scripts: repository-local commands measure skill size, run token-cost benchmark prompts in disposable fixtures, analyze Codex JSONL session exports, summarize tool-output amplification, validate token-cost release metadata, and produce reviewable evidence for reports without requiring hosted telemetry.
- required-benchmark context: release validation determines the release-specific required dynamic benchmark set from core suite policy, transition carryover policy, changed public skills, and claimed optional coverage, then passes that context to token-cost validation in process or through a transient YAML file for CLI and debugging use.
- first-slice script-output shaping: `scripts/test-select-validation.py` is the first standalone runner surface for compact `[PASS]` success summaries, actionable `[FAIL]` details, explicit `--verbose`, silent successful `--quiet`, reliable-only rerun guidance, and behavior-preservation evidence.

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
4. Every supported formal lifecycle review records change-local review evidence or reports blocked recording. Clean no-finding reviews use lightweight receipts; material findings use detailed review records.
5. `review-log.md` indexes clean receipts and detailed review records so review events are discoverable without chat history.
6. `review-resolution.md` closes material findings only after final dispositions, actions, rationale, and validation evidence are recorded. Clean no-finding reviews do not create empty `review-resolution.md` solely because a receipt exists.
7. Final closeout runs `ci-maintenance` when triggered, then `explain-change`, `verify`, and `pr`.
8. `explain-change`, `verify`, and `pr` use the change-local evidence pack, plan state, validation output, and review closeout state before claiming readiness.

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
10. Normal script and wrapper output is summary-first and failure-focused: passing checks collapse into counts and durations, failed checks expand with actionable details, and full passing detail remains available through `--verbose`.
11. `--quiet` is a script-local success-silencing mode, not a failure-hiding mode. Successful quiet runs produce no stdout or stderr, while usage errors, validation failures, test failures, and zero-test safety failures may emit bounded actionable diagnostics.

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
5. For Codex benchmarks, the runner installs current public Codex adapter skills from tracked public adapter output while that output remains tracked, or from generated temporary adapter output or release artifact output after public adapter skill copies move out of tracked Git. For `v0.1.3` and later, dynamic benchmark inputs use generated public adapter output or release archive output. The runner does not use repository-local `.codex/skills/` as the public benchmark source.
6. The runner executes prompt fixtures with `codex exec --json --ephemeral`, writes raw JSONL under `docs/reports/token-cost/runs/<release-version>/` when raw JSONL is tracked, and invokes the JSONL analyzer automatically.
7. Analyzer summaries are written beside run evidence and carry structured usage, tool-output, signal, verdict, and raw-or-sanitized evidence identity fields.
8. Maintainers manually review `skill-token-runtime-v2` benchmark result quality and record structured criteria for each dynamic run until stable expected-output checks justify automation.
9. Maintainers write a human-readable Markdown report and structured YAML metadata under `docs/reports/token-cost/releases/<release-version>.md` and `.yaml`.
10. `scripts/validate-token-cost-report.py` validates the token-cost metadata schema, waiver fields, run references, runner metadata, portability status, raw-or-sanitized evidence, result-quality evidence, required benchmark coverage, optional warning evidence, claimed optional coverage, and comparison shape.
11. Release validation delegates token-cost report validation before public release readiness is claimed.

### Generated guidance flow

1. Canonical skill sources under `skills/` are edited.
2. Adapter entrypoint templates under `scripts/adapter_templates/` provide thin authored package guidance.
3. Existing generators produce local runtime state and public adapter output from canonical skill guidance. After `.codex/skills/` is untracked, non-release local mirror validation uses temp-output generation rather than tracked-file drift comparison.
4. For local Codex use in the transition-release model, contributors use the public Codex adapter path and install or copy public Codex adapter skills into ignored `.codex/skills/` local runtime state.
5. OpenCode command aliases are generated prompt wrappers for a curated lifecycle command set and remain derived from canonical skill inclusion decisions.
6. While public adapter skill copies remain tracked, adapter validation and release verification keep checking tracked adapter drift.
7. For the `v0.1.1` transition release, release validation checks canonical `skills/`, tracked public adapter output under `dist/adapters/`, adapter manifest and install guidance, tracked release notes, token-cost metadata, and `.codex/skills/` tracked-state absence. It does not build or structurally validate `.codex/skills/` as release evidence.
8. For the `v0.1.2` archive-introduction release, release artifact preparation generates separate per-adapter archives for Codex, Claude Code, and opencode, may generate an optional combined archive, records tracked adapter artifact metadata under `docs/reports/adapter-artifacts/releases/<version>.yaml`, and keeps tracked public adapter skill bodies available.
9. Release validation for the archive-introduction release checks canonical skills, tracked adapter output, generated adapter archives, adapter artifact metadata, checksums, token-cost evidence, tracked release notes, install guidance, and the retained compatibility path.
10. For the `v0.1.3` public adapter untracking release, repository-tree adapter package fragments under `dist/adapters/<adapter>/` are retired. Complete packages are generated into temporary or release-output directories and published as release archives.
11. Adapter validation checks generated temporary or release artifact output instead of tracked public skill-copy drift.
12. Release validation checks manifest shape, generated output structure, archive structure, artifact metadata, checksums, tracked release notes, root guidance alignment, token-cost evidence, smoke evidence, and security constraints. For `v0.1.3` and later, release validation fails if tracked generated public adapter skill bodies remain under `dist/adapters/**/skills`.

### CLI multi-adapter init, download, and lockfile flow

1. A user runs `rigorloop --help`, `rigorloop version`, or `rigorloop init --adapter <adapter>` from a locally installed, globally installed, packed, or npm-delivered `@xiongxianfei/rigorloop` package.
2. The CLI resolves its concrete package name and version before producing human or JSON output.
3. For `init`, the CLI selects an adapter descriptor. Supported descriptors are Codex, Claude Code, and opencode. Unsupported adapters block before mutation.
4. The descriptor supplies possible roots and serialization shape: Codex `.agents/skills`, Claude Code `.claude/skills`, and opencode `.opencode/skills` plus `.opencode/commands` when trusted metadata requires commands.
5. The CLI verifies the package-bundled release index and adapter metadata hash before using metadata to choose a release, archive name, official URL, expected roots, archive hash, size, tree-hash algorithm, per-root hashes, and opencode command aliases.
6. In dry-run mode, the CLI reports planned writes, planned lockfile content, blockers, warnings, and artifacts without creating directories, writing files, downloading archives, or extracting archives.
7. Before mutating generated output when an existing `rigorloop.lock` is present, the CLI parses and validates the existing lockfile shape. Valid schema v1 Codex entries remain readable; adding Claude Code or opencode may upgrade to schema v2 only after existing Codex generated-output drift checks pass.
8. The CLI computes current installed tree hashes for recorded generated output and blocks destructive replacement by default when drift is detected.
9. In network mode, the CLI fetches only the exact official GitHub release archive URL selected from trusted metadata. If download fails before verification, the CLI reports the selected adapter, release, trusted public archive URL, bounded failure class, Node env-proxy status, detected proxy environment variable names only, and `--from-archive` fallback guidance.
10. In local archive mode, `--from-archive <path>` verifies the local archive against the same bundled official metadata and records only the archive basename in durable project output.
11. The CLI verifies archive filename, adapter identity, release, size when known, SHA-256, metadata compatibility, root allowlist, archive path safety, symlink absence, and installed tree hash before claiming installation success.
12. The CLI extracts only selected expected roots, refuses user-file overwrite conflicts by default, and never treats runtime install roots as authored source.
13. For older compatible opencode metadata without `command_aliases.opencode`, the CLI installs only `.opencode/skills`, omits `.opencode/commands`, emits warning code `opencode-command-aliases-not-declared`, and records only the installed skills root.
14. After generated output is installed and verified, the CLI writes deterministic UTF-8/LF `rigorloop.lock` YAML. Schema v2 records mixed single-root entries with `installed_root`, `tree_sha256`, and `file_count`, and multi-root entries with `installed_roots` plus per-root `root_hashes`.
15. If lockfile writing fails after adapter installation, the CLI reports that lockfile state was not recorded and must not claim durable lockfile success.
16. The CLI reports success, warning, blocked, or error using the stable JSON envelope and exit-code contract from the approved specs.

### CLI new-change flow

1. A user runs `rigorloop new-change <change-id> --title <title>` from the same `@xiongxianfei/rigorloop` CLI package boundary.
2. The CLI validates public option values before planning filesystem writes: `<change-id>` must be a single safe path segment, `--type` must be a lowercase classification token when supplied, `--risk` must be `low`, `medium`, or `high`, and unsupported profiles or missing required inputs fail as invalid usage.
3. The CLI builds a non-destructive write plan for `docs`, `docs/changes`, `docs/changes/<change-id>`, and `docs/changes/<change-id>/change.yaml`.
4. The write plan reports existing directories, planned directories, planned files, and blockers. It blocks before mutation on existing planned files, directory paths occupied by files or other non-directories, and symlinks at planned directory paths.
5. In dry-run mode, the CLI reports the plan using the stable JSON or human output contract and writes nothing.
6. In actual mode, the CLI creates directories before writing files and writes only `change.yaml` for this first slice.
7. If a mutation fails after earlier mutations, the CLI reports completed actions as `done`, the failed action as `failed`, names the failed path, does not claim artifact-pack creation success, and does not promise atomic rollback.
8. Generated `change.yaml` is deterministic UTF-8/LF YAML with the first-release required fields, empty `artifacts`, empty traceability arrays, and `review.status: pending`.
9. The command does not run validation, create durable Markdown reasoning placeholders, install adapters, mutate `rigorloop.yaml`, write `rigorloop.lock`, inspect Git or PR state, or claim lifecycle stage completion.

### Public npm publication flow

1. A maintainer prepares repository tag `v0.1.4` and release evidence for `@xiongxianfei/rigorloop@0.1.4`.
2. The release gate `bash scripts/release-verify.sh v0.1.4` owns release readiness and delegates to repository-owned checks.
3. Package-content validation inspects the packed npm tarball allowlist and forbidden paths before publication.
4. Packed-package smoke installs the generated `.tgz` into a temporary project and runs the installed `rigorloop` binary, not repository-local scripts.
5. Publication evidence selects exactly one mode: `trusted-publishing` or `bootstrap`.
6. In trusted-publishing mode, `.github/workflows/release.yml` publishes through npm trusted publishing/OIDC after release verification, package-content validation, and packed-package smoke.
7. In bootstrap mode, used only if trusted publishing cannot claim the unpublished package, `release.yml` or `release-verify.sh` still owns readiness but a maintainer manually publishes the exact tarball whose filename, SHA-256, source commit, pack command, package-content result, and smoke result are recorded.
8. The publication process records npm package URL, source commit, selected mode, trusted publishing or bootstrap details, provenance status when available, and rollback/deprecation notes.
9. FU-010 remains open until actual non-dry-run `init --adapter codex --json` succeeds from the packed or published package against the official `v0.1.4` Codex adapter archive. Dry-run smoke is not enough.

## Deployment View

RigorLoop has no deployed service, database, or runtime infrastructure for this architecture method. The deployment boundary is repository packaging and publication.

Authored content is reviewed in Git and distributed as repository files. Generated guidance is produced from canonical sources by existing repository generators. Tracked generated surfaces are validated for drift while they remain tracked; untracked generated surfaces are validated through temporary output or release artifact output. GitHub Actions do not own validation behavior; they set up execution and delegate to repository-owned scripts.

The main execution and publication boundaries are:

- local contributor shell: runs selector, CI wrapper, validation, generation, and drift checks;
- CLI package execution: runs the additive `rigorloop` command from a local package artifact, local/global install, or future npm package; the package is a delivery mechanism and not a canonical workflow source;
- npm registry: public delivery boundary for `@xiongxianfei/rigorloop`; the registry serves the CLI package, but canonical workflow content, skills, schemas, templates, adapter definitions, and release evidence remain repository-owned;
- downstream change metadata scaffold: `docs/changes/<change-id>/change.yaml` created by `rigorloop new-change`; it is draft traceability state and not proof that proposal, review, verification, or PR stages are complete;
- GitHub Actions: runs the same repository-owned scripts in hosted CI when configured;
- local Codex runtime state: `.codex/skills/`, ignored by Git and installed locally from public Codex adapter output when contributors need local Codex use;
- public adapter packages: tracked `dist/adapters/` output during the compatibility window through `v0.1.2`, then generated temporary or release-output packages and release archives for `v0.1.3` and later;
- adapter support metadata: `dist/adapters/manifest.yaml` and `dist/adapters/README.md`, tracked guidance and support surfaces rather than authored skill bodies;
- adapter artifact metadata: `docs/reports/adapter-artifacts/releases/<version>.yaml`, tracked release evidence with source commit, generator command, required per-adapter archive list, optional combined archive details, checksums, install roots, and validation result;
- adapter release artifacts: generated per-adapter archives, plus optional combined archive, uploaded as release assets rather than committed by default;
- bundled CLI adapter metadata: official adapter artifact metadata included in the CLI package for compatible supported adapter releases so local archive installation can verify one user-supplied archive without a separate metadata flag;
- downstream project manifest: `rigorloop.yaml` written at the target project root by the CLI after verified init planning; it records selected adapter source and single-root or multi-root install locations without claiming workflow readiness;
- downstream project lockfile: `rigorloop.lock` written at the target project root by the CLI only after verified adapter installation; schema v2 records mixed single-root and multi-root generated-output state and is not a canonical repository source;
- downstream runtime adapter roots: `.agents/skills`, `.claude/skills`, `.opencode/skills`, and `.opencode/commands` inside a user project; these are installed generated output, not authored RigorLoop source;
- durable reports: `docs/reports/`, authored from local measurement evidence and linked from change-local artifacts when produced by a change;
- token-cost benchmark fixtures: `benchmarks/token-cost/`, authored prompt and fixture inputs used to exercise public skills in a downstream-style project;
- token-cost temporary runs: isolated directories under system temp or `$RUNNER_TEMP`, disposable and not durable release evidence;
- token-cost release evidence: `docs/reports/token-cost/releases/<version>.md`, `docs/reports/token-cost/releases/<version>.yaml`, and tracked raw or sanitized run summaries under `docs/reports/token-cost/runs/<version>/`;
- release evidence: tracked `docs/releases/<version>/release.yaml`, release notes, and maintainer smoke evidence used by release verification.
- npm publication evidence: `docs/releases/v0.1.4/npm-publication.md`, recording selected publication mode, tarball identity, package-content checks, packed-package smoke, trusted publishing or bootstrap details, npm package URL, and real Codex install smoke.

Rollback before public adapter skill-copy untracking keeps `dist/adapters/**/skills` tracked and defers archive publication or fixes archive metadata, install docs, and validation before release. Rollback before `v0.1.3` publication may regenerate and restore tracked adapter output from `skills/` if the release cannot validate generated packages or archives. Rollback after public adapter skill-copy untracking preserves generation from `skills/` and either republishes release artifacts from last known good generated output or uses a later approved recovery release. No runtime data migration is required.

Rollback before public CLI publication removes or disables the package candidate and leaves existing release-archive install guidance and repository scripts unchanged. Rollback after public CLI publication uses a fixed patch release plus documentation or deprecation of the bad version; published npm versions are not mutated in place.

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

Validation output is part of the proof surface. Default human-readable output should scale with actionability rather than work volume: success output records status, identity, counts, and duration; failure output records responsible checks, names, messages, locations when available, and reliable rerun guidance when available. `--verbose` is the explicit expansion path for full passing detail. `--quiet` suppresses successful script output only and must not hide failure reasons.

### Diagram source policy

Package diagrams have one authored source file and are linked from `architecture.md` by relative path. Default Mermaid diagrams use `.mmd` files under the package `diagrams/` directory. Mermaid flowchart or graph C4 diagrams use shared role classes for people, the system under review, external systems, and containers; generated images, if added later for publication, are derived output and are not edited by hand.

### Generated output

Canonical skills and adapter templates are authored sources. `.codex/skills/`, public adapter skill copies, adapter archives, and OpenCode command aliases are generated or installed runtime outputs produced from canonical sources and approved templates or metadata. Public adapter output may be copied into `.codex/skills/` only as local ignored runtime installation; generated output must not become an authored source of truth.

After `.codex/skills/` is untracked, non-release local Codex mirror validation proves generation into a non-tracked output surface rather than tracked-file equality. Release validation for the `v0.1.1` transition release does not use `.codex/skills/` as release evidence; it proves the public adapter path works. Public adapter skill copies stay tracked until at least one stable public release has shipped downloadable adapter artifacts and release-artifact installation docs. `v0.1.2` satisfies that compatibility-window rule. For `v0.1.3` and later, public adapter skill-copy drift checks are replaced by generated temporary-output or release-artifact validation, and root guidance points ordinary contributors to `dist/adapters/README.md` as the active adapter install-contract surface.

### Release and adapter evidence

Release verification uses tracked `docs/releases/<version>/release.yaml` and `release-notes.md` plus maintainer smoke evidence. Generated release notes are not authoritative for adapter compatibility claims.

Generated adapter releases have an additional artifact evidence layer. `docs/reports/adapter-artifacts/releases/<version>.yaml` records release version, source commit, generator command, canonical source, manifest path, generated archive names, SHA-256 checksums, validation command, and validation result. Public releases that distribute generated adapters publish separate per-adapter archives as release assets and may publish a combined archive for convenience. The repository tracks metadata and checksums, not generated archive files by default.

The `v0.1.1` transition release does not require downloadable adapter archives. `dist/adapters/` remains the public adapter install path, and release notes or adapter docs state whether archives are absent or separately published. If a separate accepted plan publishes optional archives for `v0.1.1`, repository-tree installation from `dist/adapters/` remains the required public install path for that release and archive metadata becomes additional evidence rather than a replacement for tracked public adapter validation.

The `v0.1.2` archive-introduction release keeps repository-tree adapter packages for the compatibility window while publishing downloadable archives and metadata. For `v0.1.3` and later, release archives are the active install surface, `dist/adapters/README.md` and `dist/adapters/manifest.yaml` remain tracked, and generated adapter package contents are validated from temporary or release-output directories rather than tracked `dist/adapters/<adapter>/` package trees.

### CLI package, project scaffold, and lockfile boundary

The CLI package is an additive delivery surface. It can carry executable command code, small project scaffolds, and bundled official adapter metadata, but it does not own canonical workflow content, skill bodies, adapter generation rules, validation authority, or release readiness.

The generated project manifest is `rigorloop.yaml`. It records selected adapters, package/source metadata, and either `install_root` for single-root adapters or `install_roots` for multi-root adapters. It does not claim validation success, workflow readiness, branch readiness, PR readiness, or lockfile authority.

`rigorloop new-change` is also a scaffold command, but it scaffolds change-local traceability rather than project installation state. It creates only `docs/changes/<change-id>/change.yaml` in the first slice, with empty `artifacts`, `requirements`, `tests`, `validation`, and `changed_files` until later workflow stages produce real evidence. It deliberately omits `explain-change.md` and `artifacts.explain_change` so a placeholder file cannot be mistaken for durable reasoning.

The `new-change` mutation boundary is local and non-networked. It validates option domains and safe path segments before planning writes, blocks on symlinks and overwrite conflicts before mutation, reports every planned directory and file action, and uses the shared CLI JSON status and exit-code contract. Partial write failures are observable rather than atomic: already-completed actions are reported, the failed path is reported, and the command does not claim success.

`rigorloop.lock` is machine-owned downstream project state. It records verified generated adapter output after successful init. It is written only by the CLI. Schema v1 remains the strict Codex-only compatibility shape; schema v2 records mixed Codex, Claude Code, and opencode installs. Single-root adapter entries use `installed_root`, `tree_sha256`, and `file_count`; multi-root entries use `installed_roots` and per-root `root_hashes`.

Lockfile write ordering is intentionally one-way: planned writes are reported first, existing lockfiles are parsed and validated before mutation, drift is checked before destructive replacement, archive and generated-output verification happen before a success entry is written, and partial installation failures must not create lockfile claims.

The CLI updates only the fields it owns: package identity/version, normalized manifest hash, and the matching adapter entry or schema wrapper when a validated schema v1 Codex lockfile upgrades to schema v2. Unknown lockfile shape, unsupported schema versions, unsupported adapter entries, unsupported source values, unsupported tree hash algorithms, malformed YAML, invalid field types, and drifted generated output block according to the approved exit-code contract. `--force` does not replace arbitrary lockfile state in this slice.

Local archive mode keeps the user command to one archive path and moves metadata responsibility into the CLI package. This creates a package-content obligation: each package version that supports local archive install must include official adapter metadata for its compatible supported adapter releases. If that metadata is absent, local archive init blocks instead of falling back to unverified extraction.

Network archive download remains a release-asset boundary. The CLI may use Node built-in env-proxy behavior only when the runtime supports and enables it, but the first proxy-aware slice does not add programmatic Undici dispatcher ownership. Failed downloads report bounded diagnostics and point users to the verified local archive fallback without printing credentials, raw proxy URLs, private hostnames, tokens, request headers, raw environment values, or machine-local paths.

Public npm publication is an approved deployment boundary for `@xiongxianfei/rigorloop@0.1.4` only when the npm publication spec is satisfied. The package may still be built and tested locally or from a packed artifact, but FU-010 closes only after public publication evidence and real Codex install proof exist.

### Public npm package boundary

The npm package is a delivery artifact for the CLI. It can include runtime CLI code, package metadata, package-local README and license files, and bundled official adapter metadata for the compatible Codex adapter release. It must not include adapter archives, generated public adapter skill bodies, repository lifecycle artifacts, tests, local fixtures, secrets, `.codex`, `.agents`, or generated adapter package trees.

Publication has one selected mode. Trusted-publishing mode uses `.github/workflows/release.yml` and npm OIDC. Bootstrap mode is a one-time manual publication path for `@xiongxianfei/rigorloop@0.1.4` only when trusted publishing cannot be configured before package creation. Bootstrap mode separates release readiness ownership from npm publish execution: `release.yml` or `release-verify.sh` owns readiness, and the maintainer publishes only the exact verified tarball recorded in publication evidence.

The npm package does not replace GitHub release assets for adapter archives. `rigorloop init --adapter codex`, `rigorloop init --adapter claude`, and `rigorloop init --adapter opencode` still install generated adapter output from official GitHub release archives or verified local archives matched against package-bundled metadata.

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

Clean formal review receipts are also authored change-local evidence. When no existing change root exists, an isolated or review-only clean formal review uses a minimal clean-receipt root containing `change.yaml`, `review-log.md`, and `reviews/<stage>-r<n>.md`. That root omits `review-resolution.md` unless material findings, a blocking or revision outcome, or another approved review-resolution trigger requires it.

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
- `docs/adr/ADR-20260513-v0-1-3-adapter-release-archive-install-surface.md`: `v0.1.3` public adapter archive install surface and tracked adapter package retirement.
- `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md`: one-package CLI boundary, bundled metadata for local Codex archive verification, planned lockfile-only behavior, and npm publication block.
- `docs/adr/ADR-20260516-rigorloop-cli-lockfile.md`: CLI-owned durable lockfile boundary, strict schema handling, generated-output drift comparison, and partial-failure write ordering for Codex init.
- `docs/adr/ADR-20260516-rigorloop-npm-publication.md`: first public npm publication boundary, trusted-publishing/bootstrap modes, package-content proof, and real install closeout proof.
- `docs/adr/ADR-20260518-multi-adapter-init-and-proxy-download.md`: descriptor-driven multi-adapter init, schema v2 mixed-root lockfile handling, opencode skills-only compatibility, and proxy-safe download diagnostics.

No additional ADR is required for the 2026-04-29 package-quality refinement because it sharpens the accepted method without changing the durable architecture decision.

No additional ADR is required for `rigorloop new-change` because it is an additive command inside the existing CLI package boundary and does not introduce a new durable source-of-truth, packaging, release, validation, or persistence decision.

No additional ADR is required for the 2026-05-12 record-every-formal-review amendment because it refines the existing review artifact and workflow evidence architecture under the approved formal review recording spec. The durable rule is carried by `specs/formal-review-recording.md`, and this canonical package records the affected runtime and crosscutting architecture.

No additional ADR is required for the `v0.1.1` single-authored-source transition release because ADR-20260512 already records the durable generated-output and adapter release artifact migration. This package revision records the release-specific validation and packaging architecture for the transition window.

No additional ADR is required for script output optimization because it refines repository-owned validation output presentation inside the existing selector, test-runner, and CI-wrapper architecture. It does not introduce a new system boundary, persistence model, packaging model, release model, or durable source-of-truth decision.

## Quality Requirements

| Quality | Scenario | Measure |
| --- | --- | --- |
| Reviewability | A reviewer opens a PR that changes the canonical architecture package. | The affected arc42 sections, diagram source files, and ADR links are visible as repository text in the PR diff; no external binary diagram is required to review the change. |
| Traceability | A contributor changes architecture guidance for diagrams, skills, templates, or generated output. | The change links the accepted proposal, approved spec, canonical package update or explicit no-impact rationale, ADR decision if required, plan, test spec, and validation evidence. |
| Proportionality | A change needs architecture handling. | No-impact work records a rationale, clear current-architecture changes update this package directly, durable decisions create or update ADRs, and unsettled direction or behavior routes back to proposal or spec. |
| Determinism | Canonical skill guidance changes and generated guidance must be refreshed. | Generated local mirrors, public adapter output, and adapter release artifacts are produced from `skills/` through repository generators; tracked generated surfaces use drift checks and untracked generated surfaces use temp-output or release-artifact validation. |
| Adapter artifact reproducibility | A maintainer publishes generated adapter archives. | Tracked adapter artifact metadata records source commit, generator command, archive names, SHA-256 checksums, validation command, and validation result. |
| Transition release compatibility | A maintainer prepares `v0.1.1`. | `release-verify.sh` delegates structured checks to `validate-release.py`; release validation proves canonical skills and tracked public adapter output are current, release notes and adapter docs describe the transition, token-cost metadata uses public adapter output, and `.codex/skills/` is only checked for ignored/untracked state. |
| Public adapter untracking | A maintainer prepares `v0.1.3`. | Release validation proves no tracked generated adapter skill bodies remain, `dist/adapters/README.md` and `manifest.yaml` remain tracked, generated temporary or release-output packages validate, release archives validate, metadata and checksums validate, and root guidance no longer advertises retired repository-tree adapter skill bodies as the active install model. |
| CLI init safety | A user runs `rigorloop init --adapter codex` in a project with existing files. | The CLI builds a write plan, refuses user-file overwrites by default, verifies bundled metadata and archive contents before extraction, writes durable lockfile state only after generated output is verified, and reports success/block/error through the stable command contract. |
| Multi-adapter init safety | A user runs `rigorloop init --adapter codex`, `claude`, or `opencode`. | The CLI selects an explicit descriptor, verifies a trusted release or local archive, installs only descriptor and metadata-selected roots, records single-root and multi-root state correctly, and rejects unsupported adapters before mutation. |
| opencode command alias integrity | A user installs opencode from an archive whose metadata declares command aliases. | The CLI installs `.opencode/skills` and `.opencode/commands` or fails verification; older compatible skills-only archives emit `opencode-command-aliases-not-declared` and record only installed roots. |
| CLI new-change safety | A user runs `rigorloop new-change <change-id> --title <title>` in a project with existing or missing `docs/changes/` paths. | The CLI validates the option domains, builds a write plan naming every affected path, blocks on unsafe change IDs, symlinks, existing planned files, and path-type conflicts, writes only `change.yaml`, and reports partial write failures without claiming success. |
| Lifecycle claim boundary | A user sees `docs/changes/<change-id>/change.yaml` created by `new-change`. | The generated metadata has empty artifact and evidence arrays, `review.status: pending`, and no `explain_change` artifact; file existence does not imply proposal acceptance, review completion, verification, or PR readiness. |
| Local archive verification | A user runs `rigorloop init --adapter codex --from-archive <path>`. | The CLI verifies the archive against bundled official metadata for the installed package's compatible adapter release and blocks with `metadata-unavailable` if metadata is absent. |
| Lockfile determinism | A user reruns `rigorloop init --adapter codex` after a verified install with unchanged generated output. | The CLI computes the same normalized manifest hash and `rigorloop-tree-hash-v1`, preserves supported unrelated entries, and produces byte-identical lockfile content for identical state. |
| Lockfile schema v2 compatibility | A user adds Claude Code or opencode to a project with a valid schema v1 Codex lockfile. | The CLI verifies existing Codex generated output against the recorded hash before upgrading to schema v2; drift blocks before unrelated adapter mutation. |
| Lockfile drift safety | A user reruns `rigorloop init --adapter codex` after generated files under `.agents/skills` were modified. | The CLI reports drift with expected and actual tree hashes when available and blocks destructive replacement by default. |
| Proxy diagnostic safety | A network archive download fails in a proxied environment. | JSON diagnostics expose only bounded fields and allowed enum values; human output recommends `--from-archive`; neither mode prints raw proxy values, credentials, private hostnames, request headers, or machine-local paths. |
| npm publication safety | A maintainer publishes `@xiongxianfei/rigorloop@0.1.4`. | Publication evidence records exactly one publication mode, package-content validation, packed-package smoke, trusted-publishing or bootstrap identity, npm package URL, and real Codex install smoke before FU-010 closes. |
| Measurement usefulness | A contributor optimizes skill token cost. | Static skill measurement, JSONL analysis, and baseline reports identify measured cost drivers before hard token-budget gates are introduced. |
| Release token-friendliness | A maintainer prepares a public release. | Markdown and YAML token-friendliness reports exist under `docs/reports/token-cost/releases/`, Codex benchmark evidence or a valid waiver is recorded, portability passes, and release validation delegates to the token-cost report validator. |
| Dynamic benchmark coverage | A maintainer prepares a public release with `skill-token-runtime-v2`. | The report records required core coverage, transition carryover coverage when applicable, changed-skill-required coverage, claimed optional coverage, optional warnings, and per-run result-quality evidence. |
| Review closeout | Architecture-review records a material finding. | The finding includes evidence, required outcome, and a safe resolution path or `needs-decision` rationale before it drives fixes. |
| Script output actionability | A contributor runs `scripts/test-select-validation.py` or selected checks through `scripts/ci.sh`. | Successful default output is compact and count-bearing; failed output preserves actionable failure evidence; `--verbose` exposes suppressed passing detail; `--quiet` success is silent while non-success diagnostics remain visible. |
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
| Root guidance could preserve the retired repository-tree install model | The `v0.1.3` spec requires `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` to be updated or explicitly recorded as unaffected, with ordinary contributors pointed to `dist/adapters/README.md` as the install-contract surface. |
| Partial tracked adapter package fragments could look installable | The `v0.1.3` architecture keeps only `dist/adapters/README.md` and `manifest.yaml` tracked by default; complete adapter packages are generated in temporary or release-output directories and attached as release archives. |
| CLI package contents could be mistaken for canonical workflow source | The CLI package is limited to command code, scaffolds, and bundled metadata. Canonical workflow content stays in repository-authored paths, and adapter archives remain release artifacts. |
| Bundled adapter metadata could drift from official release metadata | The first-slice package must include official metadata for the package's compatible adapter release, and tests should verify matching archive name, size, SHA-256, install root, tree hash, and validation result. Public publication requires package-content checks and real Codex install smoke. |
| Descriptor-driven adapter support could under-install a runtime surface | Adapter descriptors define possible roots, trusted metadata defines required roots, and opencode declared commands must install or fail verification. Skills-only older opencode archives emit a stable warning and record only installed roots. |
| Schema v2 lockfile upgrade could mask existing generated-output drift | The CLI must verify existing schema v1 Codex generated output before upgrading the lockfile wrapper or adding unrelated adapter entries. Drift blocks before mutation. |
| Proxy diagnostics could leak enterprise network details | Diagnostics expose only safe fields and enum values. Raw proxy URLs, credentials, request headers, raw environment values, private hostnames, usernames, and machine-local paths are forbidden. |
| Programmatic proxy dispatch could add dependency and credential-handling complexity | The first proxy-aware slice uses Node built-in env-proxy support only when available and defers Undici dispatcher support to a later approved proposal or spec. |
| npm package tarball could include unintended repository internals | The npm publication spec requires a package-content allowlist, forbidden-path checks, package-local license, no adapter archives, no generated adapter skill bodies, no lifecycle artifacts, and no secrets before publication. |
| Bootstrap publication could become a shadow release path | Bootstrap mode is limited to the first `0.1.4` publication when trusted publishing cannot be configured before package creation. It publishes only the exact verified tarball recorded in evidence, and trusted publishing must be configured before the next npm publication. |
| Dry-run smoke could hide a broken real adapter install | FU-010 closeout requires actual non-dry-run `init --adapter codex --json` from the packed or published package against the official `v0.1.4` Codex archive. |
| Local archive extraction could overwrite or escape project boundaries | The CLI write plan refuses user-file overwrites by default, rejects absolute paths, parent traversal, symlinks, drive-letter paths, and paths outside `.agents/skills`, and maps expected verification failures to exit code `3`. |
| Lockfile could be mistaken for canonical source or release metadata | The lockfile records downstream generated-output state only. Canonical workflow, skill, schema, adapter metadata, and release evidence stay in repository-authored or release-evidence surfaces. |
| Unknown future lockfile shape could be silently erased by older CLIs | The first lockfile schema blocks on unknown top-level sections, unknown fields, unsupported schema versions, unsupported adapters, unsupported source values, and unsupported tree hash algorithms before mutation. |
| Adapter installation could succeed while lockfile writing fails | The CLI reports lockfile failure explicitly and must not claim durable lockfile state was recorded; later recovery or repair commands require a separate spec. |
| Users could rely on `latest` for reproducible setup | The public command model allows `latest` for quick starts but pinned package versions are the reproducible path. `latest` with incompatible local archives blocks unless a compatibility rule exists. |
| `new-change` scaffolds could be mistaken for completed workflow evidence | The first `new-change` slice writes only `change.yaml`, leaves `artifacts` and evidence arrays empty, sets review state to pending, and avoids durable-looking Markdown placeholders. Later status or validate commands must inspect actual artifacts rather than assuming scaffolded metadata means readiness. |
| Partial `new-change` filesystem writes could confuse users | The command preflights path conflicts, creates directories before files, reports completed and failed actions, and does not claim artifact-pack success after partial failure. It does not promise atomic rollback in the first slice. |
| Release validation could keep treating `.codex/skills/` as a privileged internal release path | The `v0.1.1` transition release gate validates public adapter output and only confirms `.codex/skills/` ignored/untracked state; optional local Codex smoke installs from the public Codex adapter path and stays outside required release evidence. |
| Generated adapter archives could create binary churn in Git | Generated archives are release assets by default; Git tracks artifact metadata and checksums instead of archive files. |
| Warning-only token budgets could be mistaken for CI gates | The first measurement slice treats budget thresholds as report warnings; hard gates require a later accepted proposal and spec. |
| Optional benchmark failures could be mistaken for passing release coverage | `skill-token-runtime-v2` separates optional warning evidence from claimed optional release coverage; claimed coverage follows required benchmark evidence and result-quality gates. |
| Shorter validation output could hide changed coverage or failure evidence | Script output optimization is presentation-only. Behavior-preservation evidence must prove selected checks, exit codes, failure detection, and failure evidence remain unchanged, and quiet mode must not hide non-success diagnostics. |

## Glossary

- ADR: architecture decision record that preserves a durable decision, alternatives, consequences, and follow-up.
- arc42: the 12-section architecture documentation model used by `architecture.md`.
- C4: context, container, component, and code-level structural diagram model.
- canonical architecture package: the long-lived current architecture source under `docs/architecture/system/`.
- change-local architecture delta: historical or explicitly exceptional evidence under `docs/changes/<change-id>/`; not part of the normal architecture authoring path.
- generated output: derived files under `.codex/skills/`, public adapter skill paths under `dist/adapters/`, generated adapter archives, and generated command aliases.
- transition release: a stable release that preserves repository-tree adapter installation from `dist/adapters/` while `.codex/skills/` remains ignored local runtime state and adapter archives remain a follow-on migration by default.
- compatibility-window release: a stable release that preserves repository-tree adapter packages while also providing release archives and install guidance, giving downstream users one release to transition install models.
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
- CLI package: the repository package boundary published as `@xiongxianfei/rigorloop` and exposing the `rigorloop` binary through local, packed, or npm delivery.
- publication mode: the selected public npm publication path, either `trusted-publishing` through `release.yml` and npm OIDC or one-time `bootstrap` manual publication of an exact verified tarball.
- publication evidence: durable release evidence under `docs/releases/<version>/npm-publication.md` recording package identity, selected publication mode, tarball identity, smoke results, npm URL, trusted publishing or bootstrap details, and real Codex install proof.
- bundled adapter metadata: official adapter artifact metadata included in the CLI package for the package's compatible adapter release.
- adapter descriptor: CLI-owned adapter install contract that maps an adapter name to archive filename pattern, possible roots, manifest shape, and lockfile shape.
- planned lockfile content: lockfile-shaped command output that previews generated-output hashes without writing durable `rigorloop.lock`.
- durable lockfile: downstream project `rigorloop.lock` written by the CLI after verified adapter install to record generated-output state.
- `rigorloop-tree-hash-v1`: normalized tree-hash algorithm for generated adapter output, based on sorted relative file paths and normalized file hashes.
- proxy-safe diagnostic: download failure diagnostic that reports bounded recovery facts without credentials, raw proxy URLs, request headers, private hostnames, raw environment values, usernames, or machine-local paths.
- change metadata scaffold: draft `docs/changes/<change-id>/change.yaml` produced by `rigorloop new-change` before downstream workflow stages fill in real requirements, tests, validation, changed files, reviews, and durable reasoning artifacts.

## Next artifacts

- Architecture-review for the Multi-Adapter Init and Proxy-Aware Adapter Download architecture update.

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
- Publish Next Release With Single Authored Skill Source: accepted proposal and approved spec define the `v0.1.1` transition-release architecture: validate canonical `skills/`, tracked public adapter output, release notes, adapter install guidance, and token-cost metadata; keep `.codex/skills/` out of required release evidence; retain `dist/adapters/` as the public install path; defer downloadable adapter archives unless separately planned.
- Stop Tracking Generated Public Adapter Skill Bodies: accepted proposal and approved spec define the `v0.1.3` public adapter untracking release architecture: retire tracked generated adapter package fragments under `dist/adapters/<adapter>/`, keep `dist/adapters/README.md` and `manifest.yaml`, validate generated temporary or release-output packages and release archives, update root guidance, and preserve `v0.1.2` as compatibility-window evidence.
- RigorLoop CLI Package and Codex Init: accepted proposal and approved spec define the first CLI slice: one package candidate, one `rigorloop` binary, help/version, `init --adapter codex`, dry-run JSON, non-destructive write planning, generated `rigorloop.yaml`, bundled metadata for Codex archive verification in both default and local archive modes, planned lockfile output only, and no public npm publication until release hardening.
- RigorLoop CLI Lockfile: approved spec and accepted ADR define durable `rigorloop.lock` writes for verified Codex init, strict lockfile shape handling, `rigorloop-tree-hash-v1`, drift blocking, local and network source recording, and partial-failure write ordering.
- Architecture-review for the RigorLoop CLI Lockfile architecture update: approved in `docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/architecture-review-r1.md` with no material findings.
- RigorLoop CLI New Change: approved spec defines `rigorloop new-change <change-id>` as a change metadata scaffolding command that creates only `docs/changes/<change-id>/change.yaml`, preserves lifecycle claim boundaries, validates public option domains, reports complete write plans, blocks symlinks and overwrites, and exposes partial write failures.
- Architecture-review for the RigorLoop CLI New Change architecture update: approved in `docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md` with no material findings.
- RigorLoop npm Publication: accepted proposal and approved spec define the first public `@xiongxianfei/rigorloop@0.1.4` npm release, package-content allowlist, dependency and lifecycle-script policy, trusted-publishing and bootstrap modes, publication evidence, packed-package smoke, real Codex install smoke, and FU-010 closeout boundary.
- Multi-Adapter Init and Proxy-Aware Adapter Download: accepted proposal, approved spec, and accepted ADR define descriptor-driven CLI init for Codex, Claude Code, and opencode; keep Codex on `.agents/skills`; define schema v2 mixed-root lockfile handling; preserve release-archive and local-archive verification; and add proxy-safe download diagnostics while deferring programmatic Undici dispatcher support.
- Script Output Optimization: accepted proposal and approved spec define first-slice `scripts/test-select-validation.py` output shaping, reliable-only rerun guidance, silent quiet success, behavior-preservation evidence, and minimal `scripts/ci.sh` wrapper adjustment only when needed to preserve quiet-success and loud-failure behavior.

## Readiness

This canonical package revision records the current repository architecture for generated skill output, adapter release artifact migration, the `v0.1.1` single-authored-source transition release, the `v0.1.3` public adapter untracking release, the first RigorLoop CLI package plus Codex init slice, the durable lockfile extension for verified Codex init, the `new-change` metadata scaffolding slice, the first public npm publication boundary for `@xiongxianfei/rigorloop@0.1.4`, descriptor-driven multi-adapter init with proxy-safe download diagnostics, and first-slice repository script output optimization.

ADR `docs/adr/ADR-20260512-generated-skill-output-release-artifacts.md` records the durable decision to move generated local and public skill copies out of ordinary authored Git state through staged temp-output and release-artifact validation. ADR `docs/adr/ADR-20260513-v0-1-3-adapter-release-archive-install-surface.md` records the durable `v0.1.3` decision to make release archives the active public adapter install surface and retire tracked generated adapter package fragments. ADR `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md` records the first CLI package boundary, bundled local-archive metadata decision, planned-lockfile boundary, and original publication block. ADR `docs/adr/ADR-20260516-rigorloop-cli-lockfile.md` records the durable lockfile boundary, strict schema handling, drift comparison, and partial-failure write ordering for Codex init. ADR `docs/adr/ADR-20260516-rigorloop-npm-publication.md` records the first public npm publication boundary, package-content and publication-mode decisions, and real install closeout proof. ADR `docs/adr/ADR-20260518-multi-adapter-init-and-proxy-download.md` records descriptor-driven multi-adapter init, schema v2 mixed-root lockfiles, opencode skills-only compatibility, and proxy-safe diagnostics. No additional ADR is required for `rigorloop new-change` because it is an additive command inside the existing CLI package boundary and does not introduce a new durable source-of-truth, packaging, release, validation, or persistence decision. No change-local architecture delta is produced because the canonical package carries the intended durable guidance directly.
