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
- Change-Record Catalog Registration and Bounded Read Model proposal: `docs/proposals/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`
- Change-Record Catalog Registration and Bounded Read Model spec: `specs/change-record-catalog-registration-and-bounded-read-model.md`
- Change-Record Catalog Registration and Bounded Read Model ADR: `docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md`
- Change-Record Catalog Registration and Bounded Read Model change metadata: `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`
- Validation Idempotency and Cache-Hit Safety proposal: `docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md`
- Validation Idempotency and Cache-Hit Safety spec: `specs/validation-idempotency-and-cache-hit-safety.md`
- Validation Idempotency and Cache-Hit Safety ADR: `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md`
- Validation Idempotency and Cache-Hit Safety change metadata: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml`
- Cache-Aware Inner-Loop Lifecycle Validation Helper proposal: `docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md`
- Cache-Aware Inner-Loop Lifecycle Validation Helper change metadata: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
- Release Process Contract proposal: `docs/proposals/2026-05-23-release-process-contract.md`
- Release Process Contract spec: `specs/release-process-contract.md`
- Release Process Contract ADR: `docs/adr/ADR-20260523-release-process-contract.md`
- Release Process Contract change metadata: `docs/changes/2026-05-23-release-process-contract/change.yaml`
- Target-Native Init proposal: `docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md`
- Target-Native Init spec: `specs/target-native-init.md`
- Target-Native Init ADR: `docs/adr/ADR-20260524-target-native-init-state-boundary.md`
- Target-Native Init change metadata: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`
- Published Skill Resource Integrity proposal: `docs/proposals/2026-06-22-published-skill-resource-integrity-architecture-pilot.md`
- Published Skill Resource Integrity spec amendment: `specs/skill-contract.md` R46-R55
- Published Skill Resource Integrity spec-review: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/spec-review-r1.md`
- Published Skill Resource Integrity ADR: `docs/adr/ADR-20260623-published-skill-resource-integrity.md`
- Evidence-Bound and Incremental `project-map` proposal: `docs/proposals/2026-06-23-evidence-bound-incremental-project-map.md`
- Evidence-Bound and Incremental `project-map` spec: `specs/project-map.md`
- Evidence-Bound and Incremental `project-map` proposal-review: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/proposal-review-r1.md`
- Evidence-Bound and Incremental `project-map` spec-review: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/spec-review-r1.md`
- Evidence-Bound and Incremental `project-map` change metadata: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`
- Workflow-State Projection and Pre-Transition Synchronization Gate proposal: `docs/proposals/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md`
- Workflow-State Projection and Pre-Transition Synchronization Gate spec amendment: `specs/single-source-of-workflow-state.md`
- Workflow-State Projection and Pre-Transition Synchronization Gate spec-review: `docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/spec-review-r2.md`
- Workflow-State Projection and Pre-Transition Synchronization Gate change metadata: `docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`
- Proposal-Gated Authoring Autoprogression proposal: `docs/proposals/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md`
- Proposal-Gated Authoring Autoprogression spec amendments: `specs/workflow-stage-autoprogression.md`, `specs/rigorloop-workflow.md`
- Proposal-Gated Authoring Autoprogression spec-review: `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/spec-review-r2.md`
- Proposal-Gated Authoring Autoprogression ADR: `docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md`
- Proposal-Gated Authoring Autoprogression change metadata: `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
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
- retire public `--adapter` init syntax in favor of target-native `rigorloop init codex`, `rigorloop init claude`, and `rigorloop init opencode`;
- make default target-native init install-only while keeping explicit `--write-state` as the managed project-state path for target-oriented `rigorloop.yaml` and `rigorloop.lock` schemas;
- require release smoke for target-native init to use real non-dry-run packed-package and live-registry install paths rather than dry-run output alone;
- make published skill-local resource dependencies explicit, packageable, hash-verifiable, and present across canonical source, generated output, packed release candidates, and clean installed target trees;
- keep `project-map` as a current-state orientation reference with freshness metadata, cited material claims, visible inference, root/area registration, and downstream reliance boundaries;
- improve enterprise-network recovery through bounded proxy diagnostics while deferring programmatic proxy dispatcher support;
- let the CLI scaffold a draft change-local artifact pack for `docs/changes/<change-id>/change.yaml` without claiming lifecycle stage completion or creating durable-looking placeholder artifacts;
- publish the first public `@xiongxianfei/rigorloop` npm package only through a reviewable release-hardening boundary that preserves npm as delivery, not source of truth;
- make public release skill token-friendliness measurable through release reports, structured metadata, and fixture-backed runtime benchmarks;
- make dynamic token-friendliness coverage visible across the core delivery workflow without requiring every optional skill benchmark for every release;
- keep repository script output proportional to actionability: compact on success, specific on failure, and expandable through explicit verbose modes;
- treat change records as queried catalogs with registered deterministic evidence classes, selector routing, and bounded read paths for common stage-owned questions;
- reduce repeated validation work only through unchanged-input cache hits that preserve validator behavior and closeout actual-run gates, and make the safe inner-loop cached path easy through a named lifecycle validator helper mode;
- define the release process once as a standing contract, then execute routine publishes as operations with durable release evidence;
- keep first adoption and package-quality refinement review-based until real package usage proves which checks are worth automating.
- keep planned-initiative workflow state single-owned by the active plan while making plan-index, milestone-state, readiness, review, and change-metadata surfaces mechanically synchronized before downstream readiness claims.
- reduce redundant post-proposal authoring prompts through a separately armed, change-local `authoring-through-plan-review` profile that preserves proposal judgment, formal review recording, review independence, and stop-on-ambiguity behavior.

## Architecture Constraints

- `CONSTITUTION.md` is the highest-priority repository governance artifact below external runtime instructions.
- `specs/architecture-package-method.md` owns the C4, arc42, ADR, template, canonical-package, architecture-surface, and historical change-local evidence contract.
- `specs/rigorloop-workflow.md` owns only workflow stage routing and handoff language for this method.
- `specs/single-source-of-workflow-state.md` owns planned-initiative live-state ownership, projection, pointer, ledger, evidence, and state-sync gate behavior.
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
- Change records under `docs/changes/<change-id>/` are queried catalogs, not append-only transcripts. Deterministic change-local evidence files require registered evidence-class routing or explicit registration debt.
- Evidence-class registry behavior belongs to the selector architecture. The first slice may centralize registry data when the selector supports it, or keep a selector-owned registry table with fixture-backed regression coverage.
- Bounded change-record reads belong to a new query-helper script rather than `validate-change-metadata.py`; validation remains proof work, while querying returns scoped metadata slices.
- Workstream A, evidence registration and selector routing, ships before Workstream B, bounded query helper and stage-skill guidance, so CI-routing risk and skill-behavior risk remain separately reviewable and rollbackable.
- Validation idempotency starts with the explicit-path lifecycle command family only: direct `validate-artifact-lifecycle.py --mode explicit-paths` and helper `validate-artifact-lifecycle.py --mode explicit-paths-inner-loop`.
- Direct `--mode explicit-paths` remains the actual-run command for closeout, verify, branch readiness, PR readiness, CI, and other first-slice final gates.
- `--mode explicit-paths-inner-loop` is a cache-aware inner-loop helper mode. It normalizes to canonical direct `--mode explicit-paths` argv for cache identity, prior passing event matching, and input-surface identity, while formal evidence records both displayed helper argv and canonical cache argv.
- Cache hits require a previous actual-run pass trace, identical canonical normalized command, identical input-surface hash, identical implementation manifest hash, and identical policy/config manifest hash.
- Validation cache execution state is untracked, branch-local, worktree-local, and change-local. It is not lifecycle evidence and must not be reused across branches, worktrees, machines, remote/shared caches, or CI jobs.
- Formal cache-hit evidence lives in `docs/changes/<change-id>/validation-cache-evidence.yaml`, while Workstream A measurement evidence lives in `docs/changes/<change-id>/validation-cache-measurement.yaml`.
- Helper cache-hit evidence is written or merged only when a safe change root or safe evidence path is supplied or inferable; local ad hoc helper use may print cache status without writing formal evidence.
- `cache-hit-inner-loop` evidence cannot satisfy stage or milestone closeout. First-slice closeout requires actual-run evidence, with primary rejection owned by `validate-artifact-lifecycle.py` and consistency checks owned by `validate-change-metadata.py`.
- Helper measurement keeps helper invocations, cache hits, cache misses, disabled evaluations, actual-run fallbacks, actual runs, and closeout actual runs distinct.
- Workstream B edit-scoped validation remains outside this architecture until Workstream A measurement is reviewed and a separate approved proposal or spec amendment authorizes it.
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
- For `0.3.0`, the public init surface is target-native: `rigorloop init codex`, `rigorloop init claude`, and `rigorloop init opencode`. `--adapter` is removed and fails before mutation with migration guidance.
- Default target-native init is install-only: it installs verified target support and must not create, update, delete, rename, or reformat `rigorloop.yaml` or `rigorloop.lock`.
- Managed project state is explicit through `rigorloop init <target> --write-state`. New state files use target-oriented schemas: `rigorloop.yaml` schema v2 with top-level `targets`, and `rigorloop.lock` schema v3 with `generated.targets`.
- Existing state files are byte-preserved by default, but byte preservation does not prevent safety reads. When default init plans target-root mutation, existing state is parsed enough to detect selected-target drift, overlapping roots, or conflicting root mappings. Malformed or ambiguous state blocks non-dry-run mutation.
- Historical archive filename values and non-user-visible `dist/adapters/` implementation names may continue to use adapter naming until a separate internal/archive rename is approved.
- Target-native release readiness requires real non-dry-run packed-package smoke before publish and live registry/download smoke after publish for every supported target. Dry-run output is not release install-smoke proof.
- Published skills declare required skill-local resources through `Resource map` entries. Untransformed mapped resources preserve skill-root relative path plus raw-byte SHA-256 from canonical source through generated output, packed release candidates, and installed target trees.
- Resource-integrity migration starts in audit mode for existing published skills, but new or changed skills cannot introduce unmapped skill-local resource references or missing mapped resources.
- `templates/` is not an implicit packaged skill resource class. Legacy `templates/...` references are migration lint input until removed, mapped to `assets/` or `references/`, or explicitly excepted.
- The `project-map` skill describes current repository orientation only. Project maps are living references and do not override source code, runtime configuration, schemas, build manifests, tests, CI, or governing workflow artifacts.
- Root project maps use `docs/project-map.md` by default. Area maps use `docs/project-map/<area>.md` only for durable boundaries and require registration from the root map when any area map exists.
- Project maps record their own baseline, coverage, exclusions, known gaps, status, and parent-map relationship. Dirty Git baselines use `<sha>+dirty` and list inspected uncommitted paths.
- Material current-state claims in project maps cite repository paths, inferences are labeled, unknowns are recorded as open questions, configured commands are distinct from executed commands, and executed commands include exit codes.
- The `project-map` skeleton is a packaged skill-local asset at `skills/project-map/assets/project-map-skeleton.md`, declared with `COPY` in the skill `Resource map`, carried through generated adapter output, and validated by the existing published skill resource-integrity path.
- Existing project maps are not automatically migrated by this change; they satisfy the revised contract only when intentionally refreshed or recreated.
- First-slice proxy behavior uses Node built-in env-proxy support only when the runtime supports and enables it. Programmatic Undici proxy dispatcher support is out of scope until a later approved change.
- Public npm publication of `@xiongxianfei/rigorloop@0.1.4` is allowed only through the approved npm publication slice: package-content allowlist, lifecycle-script and dependency policy, exactly one publication mode, publication evidence, packed-package smoke, and real Codex adapter install proof.
- Normal npm publication uses trusted publishing through `.github/workflows/release.yml`. One-time bootstrap publication may be used only for `@xiongxianfei/rigorloop@0.1.4` if trusted publishing cannot be configured before package creation, and it may publish only the exact verified tarball recorded in publication evidence.
- After the `v0.1.3` adapter untracking migration, the tracked default adapter support surface under `dist/adapters/` is limited to `README.md` and `manifest.yaml` unless a later approved spec explicitly names more tracked metadata or templates.
- `docs/releases/<version>/release.yaml` and `docs/releases/<version>/release-notes.md` are authored release evidence, not generated release-note substitutes.
- Routine publish operations execute the standing release-process contract and record durable version-scoped evidence under `docs/releases/v<version>.md`; related change records link to that evidence when applicable.
- Routine release evidence does not update `docs/plan.md` unless the release is part of an active lifecycle plan; `docs/releases/` and the release index own routine publish records.
- Release-process changes, new package names or scopes, new adapter targets, changed authentication/provenance policy, and changed publish mechanics remain normal lifecycle-managed work before any publish operation uses them.
- Emergency release deferrals are narrow owner-approved exceptions to release gate timing, not an alternate normal release path. Release evidence creation, secret suppression, source/package/version/dist-tag recording, publish-path recording, registry verification, and recovery/follow-up recording are non-deferrable.
- Planned-initiative live state is owned by the active plan `Current Handoff Summary`; `docs/plan.md`, milestone-state fields, `Readiness`, review artifacts, and change metadata are projections, pointers, ledgers, or evidence surfaces and must not become competing live next-stage owners.
- State-changing handoffs run parser-scoped state-sync validation over bounded live-state surfaces before downstream readiness is claimed. Historical ledgers and review evidence remain append-only and are excluded from stale-token rejection.
- `authoring-through-plan-review` is a separately armed workflow-managed profile. It is not a repository-wide default and cannot silently widen to `test-spec`, implementation, PR, release, deploy, merge, or automatic review-fix loops.
- Profile activation requires both an armed profile and a gate-ready proposal. Proposal gate readiness is artifact and review state; user authorization is separate intent and cannot substitute for accepted proposal status or approved recorded proposal-review.
- Durable profile authorization must be recorded before any profile-driven transition. The canonical policy surface is `docs/changes/<change-id>/change.yaml`; `docs/changes/<change-id>/workflow-policy.yaml` is allowed only when the change-metadata contract rejects policy data, and that fallback decision must be audit-visible.
- Profile policy metadata records authorization and profile policy only. It must not own current stage, next stage, review status, branch readiness, PR readiness, or active-plan live state.
- The recorded architecture assessment micro-stage after approved `spec-review` owns routing to `architecture`, `plan`, or pause for ambiguity under the profile.
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

`Project maps` is a first-class repository artifact container because it has a distinct current-state orientation responsibility, canonical root and area-map paths, freshness semantics, and downstream consumers.

It is separate from `Architecture`: project maps describe observed repository reality, while architecture artifacts own design structure and decisions.

| Container | Responsibility | Technology / source |
| --- | --- | --- |
| Governance and workflow guidance | Defines source-of-truth order, repository defaults, workflow routing, and contributor expectations | Markdown in `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md` |
| Lifecycle artifacts and ADRs | Carry proposal, spec, architecture, ADR, plan, test-spec, active plan current-state owners, plan-index projections, queryable change metadata, validation cache-hit evidence, validation cache measurement, and registered change-record evidence states | Markdown/YAML in `docs/proposals/`, `specs/`, `docs/architecture/`, `docs/adr/`, `docs/plans/`, `docs/changes/` |
| Project maps | Carry living current-state repository orientation, map metadata, cited evidence, inference and unknown labels, root/area registration, risks, and open questions | Markdown in `docs/project-map.md` and `docs/project-map/` |
| Token-cost benchmark fixtures and reports | Carry executable benchmark prompts, clean downstream fixtures, raw or sanitized run evidence, analyzer summaries, and longitudinal token-friendliness reports | Markdown/YAML/JSONL under `benchmarks/token-cost/` and `docs/reports/token-cost/` |
| RigorLoop CLI package | Provides the `rigorloop` binary, project scaffolding, change metadata scaffolding, stable human/JSON command envelopes, bundled adapter metadata, verified adapter archive installation for supported adapters, proxy-safe download diagnostics, and durable lockfile writes for verified generated adapter output | Node/npm package under `packages/rigorloop`, published as `@xiongxianfei/rigorloop` only through the approved npm publication boundary |
| Canonical architecture package | Long-lived current architecture source of truth, including arc42 prose and C4 diagram source | Markdown and Mermaid in `docs/architecture/system/` |
| Change-local evidence | Historical architecture evidence, explicit exceptional architecture evidence, change metadata, registered deterministic evidence files, validation cache-hit evidence, validation cache measurement, explanation, review resolution, and verification evidence | Markdown/YAML in `docs/changes/<change-id>/` |
| Templates and diagram styles | Canonical scaffolding for architecture, ADRs, and shared Mermaid C4 role styling | Markdown/Mermaid under `templates/` |
| Canonical skills and adapter templates | Source instructions, packaged skill-local resources, workflow stages, and thin adapter entrypoints | Markdown in `skills/`, skill-local resources under each skill root, templates in `scripts/adapter_templates/` |
| Validation and generation scripts | Select checks, route registered change-local evidence, compute validation cache keys for eligible explicit-path lifecycle validation, validate artifacts, compare workflow-state owners and projections, query bounded change-record slices, refresh generated output, prove drift status, validate mapped skill-local resources, and compare resource parity across generated, packed, and installed outputs | Python and shell under `scripts/` |
| Generated runtime state and adapters | Derived local Codex runtime state and public adapter packages for supported agent tools; local runtime state and public adapter packages are generated from canonical sources and are not authored sources | Ignored local files under `.codex/skills/`, tracked adapter support metadata under `dist/adapters/`, generated temporary or release-output package directories, and release asset archives |
| Release evidence | Authored release contract, release notes, standing process evidence, adapter artifact metadata, package publication evidence, registry verification, checksums, emergency deferrals, and maintainer smoke evidence | Markdown/YAML under `docs/releases/v<version>.md`, `docs/releases/<version>/`, and `docs/reports/adapter-artifacts/releases/` |
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
- evidence registration: the selector owns deterministic evidence-class matching for recurring change-local evidence files, rejects broad or ambiguous patterns through regression coverage, routes registered classes to declared checks, and surfaces stable `manual-routing-required` diagnostics for unregistered deterministic evidence;
- validation idempotency: cache helpers compute normalized argv, repository-relative explicit paths, input-surface hashes, implementation manifest hashes, and policy/config hashes for the eligible explicit-path lifecycle command family. Direct `--mode explicit-paths` remains actual-run for closeout and final gates, while helper `--mode explicit-paths-inner-loop` supplies inner-loop cache context, normalizes to canonical direct argv for cache identity, and records displayed-versus-canonical argv in formal helper evidence. Unsupported or uncertain manifests disable caching and run the validator;
- lifecycle and change validators: `scripts/validate-artifact-lifecycle.py`, `scripts/validate-change-metadata.py`, and `scripts/validate-review-artifacts.py` validate artifact status, planned-initiative owner/projection synchronization, change metadata, and material review closeout structure;
- workflow-state synchronization: the lifecycle validator exposes shared parser and comparison helpers for `Current Handoff Summary`, current milestone-state projection, active or blocked `docs/plan.md` projection rows, pointer-only `Readiness`, review-log and review-resolution consistency, and derived change-metadata summaries. Any direct state-sync command is a thin wrapper around the same helpers, not an independent parser;
- change-record query helper: `scripts/query-change-record.py` exposes bounded `summary`, `artifacts`, `validation --latest`, and `validation --stage <stage>` reads over valid legacy and compact metadata shapes without executing validation commands;
- skill and adapter generation: `scripts/build-skills.py`, `scripts/build-adapters.py`, and adapter distribution helpers generate local runtime state, public adapter output, and release artifact outputs from canonical sources;
- release and adapter validation: `scripts/validate-adapters.py`, `scripts/validate-release.py`, and `scripts/release-verify.sh` check generated packages, manifests, release metadata, adapter artifact metadata, tracked release notes, package preview, registry verification, emergency deferral records, checksums, and smoke evidence. For public releases, `release-verify.sh` is the maintainer-facing gate and `validate-release.py` owns structured release validation delegated from that gate. For `v0.1.3` and later, these checks validate generated temporary or release-output adapter packages and release archives instead of tracked adapter package trees.
- published skill resource integrity: skill validation checks `Resource map` verb-to-class rules, path containment, canonical resource existence, and bounded unmapped legacy references; generated-output and adapter validation compare mapped resource relative paths and raw-byte SHA-256; clean-install smoke inspects installed target skill roots for Codex, Claude, and opencode.
- project-map contract validation: the first slice validates the normalized skill contract, resource-map entry, skeleton asset, generated adapter inclusion, and a small representative output set for required sections, material citations, inference labels, unknowns, configured/executed command separation, correction notes, and absence of unfilled placeholders. A dedicated project-map artifact validator remains deferred until concrete drift appears in at least two produced maps.
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
7. When `authoring-through-plan-review` is armed for a workflow-managed change, the workflow first proves proposal gate readiness from tracked artifacts: accepted proposal status, approved recorded proposal-review, no material proposal-review findings, no open blockers, settled scope/non-goals, non-blocking open questions, satisfied standing gates, and unambiguous change ID and artifact placement.
8. Activation requires `armed && gate-ready` plus durable authorization persistence. Missing, malformed, partial, or failed authorization persistence pauses before `spec` with `authorization-not-persisted`; session-only pre-pack intent must be reasserted after the change pack exists.
9. After activation, the profile may run `spec`, `spec-review`, recorded architecture assessment, conditional `architecture`, conditional `architecture-review`, `plan`, and `plan-review`, with each review invoked as a distinct formal review over tracked artifacts rather than hidden authoring reasoning.
10. Architecture assessment records exactly one of `architecture-required`, `architecture-not-required`, or `architecture-ambiguous`. Ambiguity pauses; `architecture-required` routes to `architecture` and `architecture-review`; `architecture-not-required` routes to `plan`.
11. Non-approved review status, material findings, open owner decisions, unresolved ambiguity, contradictory workflow state, user pause/cancellation, unreliable partial completion, or exhausted transition budget pauses the profile. Clean `plan-review` marks the profile completed and reports `test-spec` next without invoking it.
12. Direct review-only invocations remain isolated even when a profile is armed, unless the user explicitly invokes workflow-managed resume.
13. Final closeout runs `ci-maintenance` when triggered, then `explain-change`, `verify`, and `pr`.
14. `explain-change`, `verify`, and `pr` use the change-local evidence pack, plan state, validation output, and review closeout state before claiming readiness.

### Change-record catalog flow

1. A contributor or agent adds deterministic evidence under `docs/changes/<change-id>/`.
2. The changed-path selector matches the path against registered evidence classes before verify.
3. A registered evidence file routes to the evidence class's declared check IDs and governing change metadata context.
4. An unregistered deterministic evidence file receives a stable `manual-routing-required` diagnostic and becomes registration debt.
5. Registration debt is resolved before verify by adding a supported registry route, removing or renaming the unsupported evidence, or recording owner-approved deferral with validation impact and follow-up.
6. Workstream B adds `scripts/query-change-record.py` as the bounded read surface for common questions such as artifact paths, latest validation state, and stage-scoped validation evidence.
7. Query helper reads never execute validation bundle commands and never replace full forensic reads when evidence is disputed, ambiguous, unsupported, or the whole change record is the review target.
8. Stage-skill guidance may reference query helper commands only after those commands are stable and generated adapter output has been validated.

### Validation flow

1. Changed paths are inspected with `python scripts/select-validation.py --mode explicit --path ...`.
2. Supported changed paths are executed through `bash scripts/ci.sh --mode explicit --path ...`.
3. The selector emits stable check IDs such as `artifact_lifecycle.validate`, `change_metadata.validate`, `change_metadata.regression`, `review_artifacts.validate`, and generated-output checks.
4. Lifecycle-managed artifacts are checked with `scripts/validate-artifact-lifecycle.py`.
5. When planned-initiative live-state surfaces are in scope, `scripts/validate-artifact-lifecycle.py` parses exact owner fields, projection fields, and pointer sections; compares owner/projection values; checks review-log, review-resolution, and derived change metadata consistency; and rejects stale live-state tokens only inside bounded live-state surfaces.
6. Change metadata is checked with `scripts/validate-change-metadata.py`.
7. Review artifact closeout is checked with `scripts/validate-review-artifacts.py` when review files are in scope.
8. Architecture diagram source files and historical or exceptional change-local architecture evidence route only to existing non-enforcement lifecycle checks; C4 sufficiency, arc42 completeness, ADR need, and package shape remain architecture-review or code-review evidence.
9. Unclassified paths do not fail open; they require explicit manual routing or a later selector contract update.
10. Final broad smoke runs only when an authoritative trigger requires it.
11. Normal script and wrapper output is summary-first and failure-focused: passing checks collapse into counts and durations, failed checks expand with actionable details, and full passing detail remains available through `--verbose`.
12. `--quiet` is a script-local success-silencing mode, not a failure-hiding mode. Successful quiet runs produce no stdout or stderr, while usage errors, validation failures, test failures, and zero-test safety failures may emit bounded actionable diagnostics.
13. For branches adding deterministic change-local evidence, actual changed-path routing proof is required before verify. Supplemental fixtures and explicit-path validation do not replace routing the branch's own changed paths.

### Published skill resource-integrity flow

1. Canonical skill validation reads each changed `skills/<skill>/SKILL.md` and any packaged skill-local resources under that skill root.
2. For every `Resource map` entry, validation checks that the verb maps to the allowed class: `COPY` to `assets/`, `READ` to `references/`, and `RUN` to `scripts/`.
3. The mapped path is resolved relative to the skill root. Paths that traverse outside the skill root, depend on repository-root internals, or point to missing canonical files fail validation.
4. Bounded migration lint inspects recognized resource-loading instructions and approved skill-local prefixes, including legacy `templates/`, to catch unmapped skill-local resource references without broad path-like Markdown scanning.
5. Adapter generation carries mapped resources into generated output without transformation by default.
6. Generated-output parity compares the canonical skill-root relative path and raw-byte SHA-256 for every untransformed mapped resource.
7. If a resource is intentionally transformed, the transformation contract supplies input path, transformation owner, output path, expected output identity, and validation command. Missing transformation contracts fail parity validation.
8. Pre-publish clean-install smoke installs the locally packed release candidate into empty Codex, Claude, and opencode target projects, then inspects the real installed skill roots for mapped resources at the expected relative paths and raw-byte identities.
9. Live registry installation remains release-owned post-publish evidence unless the release contract explicitly requires it before implementation closeout.
10. Runtime fallback is not package proof: missing mapped resources still fail package validation, and missing normative, schema, security, legal, or non-obvious structural resources stop execution with a package-integrity blocker.

### Project-map authoring and refresh flow

1. The `project-map` skill classifies the invocation as `create`, `refresh`, `area`, or `audit` before broad repository reading.
2. The skill resolves artifact placement from explicit user path, existing artifact metadata or active workflow context, project workflow guidance, and then portable defaults.
3. For create or refresh, the map records metadata before the substantive sections: status, scope, baseline, last-reviewed date, coverage, exclusions, parent map, and known gaps.
4. When Git is available and inspected files include uncommitted changes, the baseline records `<sha>+dirty` and the inspected uncommitted paths so later readers can reconstruct what evidence was actually mapped.
5. The map writes current-state claims from source-ranked evidence. Material claims cite repository paths, inferences are labeled, and unknowns move to `Open questions` instead of being guessed.
6. Runtime and data-flow statements name their evidence mode: statically traced, demonstrated by tests, observed through execution, or partially inferred.
7. Configured commands and executed commands remain separate. Executed commands include exit codes; mutation, network, build, and test-suite commands require user go-ahead before execution.
8. Area maps are created only for durable repository boundaries and only when the root-map section would otherwise exceed roughly a screen of content, unless the area has its own deploy, release, ownership, package, domain, or data lifecycle.
9. When an area map exists, the root map remains the entry point and registers the area map in the stable area-map table. Overlap names one map as detail owner and makes the other link rather than duplicate.
10. If a refresh discovers a previous map claim was wrong at its recorded baseline, the result includes a correction note. Map status remains `current`, `partial`, or `stale`.
11. Risks and open questions remain orientation evidence. Any action routes through proposal, plan, learn, review resolution, release evidence, or other workflow-owned follow-up surfaces.
12. Downstream stages may use current maps for orientation, but inspect source directly when the relevant map is stale, partial, conflicting, missing cited paths, inferred, unknown, security-sensitive, or exact-behavior critical.

### Validation idempotency cache-hit flow

1. A contributor requests inner-loop lifecycle validation through `python scripts/validate-artifact-lifecycle.py --mode explicit-paths-inner-loop ...`, or a contributor, CI wrapper, or final gate requests actual lifecycle validation through direct `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`.
2. Cache eligibility checks confirm the command surface is part of the first-slice explicit-path lifecycle command family and is not being used for a stage or milestone closeout full-bundle gate.
3. For helper invocations, the cache helper keeps the displayed helper argv for evidence but normalizes cache identity to the canonical direct `--mode explicit-paths` argv. For direct actual-run invocations, the canonical argv is the direct command.
4. The cache helper normalizes the command as an ordered argv vector, normalizes `--path` values as repository-relative POSIX paths, rejects unsafe or duplicate explicit paths, and computes the command hash.
5. The cache helper computes the input-surface hash from every explicit path's content hash or missing-file marker.
6. The cache helper computes the validator implementation manifest hash from the entrypoint, resolved repository-local imports/helpers, and manifest-generation logic, and computes the policy/config manifest hash from declared lifecycle policy/spec/config files.
7. If a matching local execution cache entry exists for the same branch, worktree, change ID, canonical command hash, input-surface hash, implementation hash, policy hash, and previous `pass` that traces to an actual run, the helper may emit bounded `[CACHE HIT]` output and write or merge formal cache-hit evidence when a safe change root or safe evidence path is supplied or inferable.
8. If any cache component is missing, malformed, unsupported, changed, unsafe, non-local, expired, non-passing, or not traceable to an actual run, the validator actually runs and preserves existing pass/fail behavior and exit semantics.
9. Formal cache-hit evidence in `validation-cache-evidence.yaml` is reviewable proof that a prior pass still applies. Helper-produced evidence records `displayed_command_argv`, `canonical_cache_argv`, `cache-hit-inner-loop`, `scope: inner-loop`, and `closeout_evidence: false`; it is not a new pass.
10. Closeout validation ignores cache hits as pass evidence. A closeout bundle is satisfied only by compact `schema_version: 2` validation events with `result: pass` and `evidence_kind: actual-run-pass` from the direct actual-run command or another approved actual-run bundle.
11. Workstream A measurement in `validation-cache-measurement.yaml` records eligible commands, helper invocations, cache hits, misses, disabled evaluations, helper actual-run fallbacks, actual runs, closeout actual runs, time saved, remaining cost, cache-hit rate, and Workstream B recommendation state.

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

### CLI target-native init, download, state, and release-smoke flow

1. A user runs `rigorloop --help`, `rigorloop version`, `rigorloop init <target>`, or `rigorloop init <target> --write-state` from a locally installed, globally installed, packed, or npm-delivered `@xiongxianfei/rigorloop` package.
2. The CLI resolves its concrete package name and version before producing human or JSON output.
3. For `init`, the CLI accepts exactly `codex`, `claude`, or `opencode` as the target. `--adapter`, target aliases, unknown targets, and mixed target syntaxes block before mutation with migration or usage guidance.
4. Internally, the target maps to the existing descriptor model. Descriptors supply possible roots and serialization shape: Codex `.agents/skills`, Claude Code `.claude/skills`, and opencode `.opencode/skills` plus `.opencode/commands` when trusted metadata requires commands.
5. The CLI verifies the package-bundled release index and metadata hash before using metadata to choose a release, archive name, official URL, expected roots, archive hash, size, tree-hash algorithm, per-root hashes, and opencode command aliases.
6. In dry-run mode, the CLI reports planned target-root writes, blockers, warnings, and artifacts without creating directories, writing files, downloading archives, or extracting archives. Planned state-file writes are reported only when `--write-state` is present.
7. Default `init <target>` is install-only and must not create, update, delete, rename, or reformat `rigorloop.yaml` or `rigorloop.lock`. When existing state files are present and target-root mutation is planned, the CLI parses enough valid state to detect selected-target drift, overlapping roots, or conflicting root mappings. Valid unrelated state is byte-preserved; drifted, conflicting, malformed, or ambiguous state blocks non-dry-run mutation.
8. In network mode, the CLI fetches only the exact official GitHub release archive URL selected from trusted metadata. If download fails before verification, the CLI reports the selected target, release, trusted public archive URL, bounded failure class, Node env-proxy status, detected proxy environment variable names only, and `--from-archive` fallback guidance.
9. In local archive mode, `--from-archive <path>` verifies the local archive against the same bundled official metadata and records only the archive basename in explicit durable state when `--write-state` is requested.
10. The CLI verifies archive filename, target identity, release, size when known, SHA-256, metadata compatibility, root allowlist, archive path safety, symlink absence, installed tree hash, and file counts before claiming installation success.
11. The CLI extracts only selected expected roots, refuses user-file overwrite conflicts by default, and never treats runtime install roots as authored source.
12. For older compatible opencode metadata without `command_aliases.opencode`, the CLI installs only `.opencode/skills`, omits `.opencode/commands`, emits warning code `opencode-command-aliases-not-declared`, and records only the installed skills root if `--write-state` writes state.
13. If `--write-state` is absent, the CLI reports successful verified install with state-file writes skipped.
14. If `--write-state` is present, the CLI writes deterministic UTF-8/LF state only after generated output is installed and verified. `rigorloop.yaml` uses schema v2 with target-oriented `targets`; `rigorloop.lock` uses schema v3 with `generated.targets`. New user-visible schema keys must not use `adapter` or `adapters`, while historical archive filename values may keep adapter naming until a later internal/archive rename.
15. If state writing fails after target installation, the CLI reports that target files were installed but state was not recorded and must not claim durable state success.
16. Release readiness runs real non-dry-run packed-package smoke before publish and live registry/download smoke after publish for every supported target. Dry-run output remains useful for planning and JSON shape checks but is not install-smoke proof.
17. The CLI reports success, warning, blocked, or error using the stable JSON envelope and exit-code contract from the approved specs.

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

### Standing release-process flow

1. A maintainer classifies the release as routine, prerelease, breaking publish, emergency, process-changing, new package/scope, new adapter target, or republish recovery before publish work begins.
2. Routine publishes proceed only when no new product, process, package-surface, authentication, provenance, adapter-target, or publish-mechanics decision is being introduced. Otherwise the upstream change follows the normal proposal/spec/review path before release execution.
3. The release operator records version, release type, source commit, branch, package name, npm dist-tag, publish path, provenance mode, and release evidence path before publish.
4. The pre-publish release gate proves a clean or intentionally release-scoped worktree, release notes or not-required rationale, generated-output currency, test or broad smoke status, package preview, packed local install smoke, selected publish path, and unresolved-blocker state.
5. Generated-output currency is proven by repository-owned drift or generated-output checks such as `skills.drift`, `adapters.drift`, or current equivalents. Currency is not asserted from memory.
6. Package preview and packed install smoke inspect the exact package artifact that may be published, not repository-local source in place of package contents.
7. Preferred publication uses trusted publishing/OIDC. Manual fallback is allowed only as a recorded fallback or emergency path and does not relax gate evidence, package preview, registry verification, or secret-suppression requirements.
8. After publish, verification reads from the public registry and records version, dist-tag, integrity metadata, and a fresh install or `npx` smoke result when not emergency-deferred.
9. Emergency releases may defer only deferrable gate items, and each deferral records owner approval, rationale, validation impact, accepted risk, follow-up location, and deadline or next lifecycle stage before publish.
10. Release evidence remains open for deferred gate follow-up until the gate completes, an approved recovery action replaces it, or an owner closes the risk explicitly.
11. Failed package contents recover through fix-forward, dist-tag correction when only tags are wrong, or deprecation when necessary. Published npm versions are not overwritten.

## Deployment View

RigorLoop has no deployed service, database, or runtime infrastructure for this architecture method. The deployment boundary is repository packaging and publication.

Authored content is reviewed in Git and distributed as repository files. Generated guidance is produced from canonical sources by existing repository generators. Tracked generated surfaces are validated for drift while they remain tracked; untracked generated surfaces are validated through temporary output or release artifact output. GitHub Actions do not own validation behavior; they set up execution and delegate to repository-owned scripts.

The main execution and publication boundaries are:

- local contributor shell: runs selector, CI wrapper, validation, change-record query helper, generation, and drift checks;
- CLI package execution: runs the additive `rigorloop` command from a local package artifact, local/global install, or future npm package; the package is a delivery mechanism and not a canonical workflow source;
- npm registry: public delivery boundary for `@xiongxianfei/rigorloop`; the registry serves the CLI package, but canonical workflow content, skills, schemas, templates, adapter definitions, and release evidence remain repository-owned;
- routine release evidence: `docs/releases/v<version>.md`, a version-scoped standing process record for release type, version decision, gate status, package contents, publish event, registry verification, emergency deferrals, recovery notes, and follow-up;
- downstream change metadata scaffold: `docs/changes/<change-id>/change.yaml` created by `rigorloop new-change`; it is draft traceability state and not proof that proposal, review, verification, or PR stages are complete;
- profile policy metadata: change-local `workflow.autoprogression` authorization data in `change.yaml`, or `workflow-policy.yaml` only when change metadata rejects policy data; it is audit and activation evidence, not live workflow state;
- GitHub Actions: runs the same repository-owned scripts in hosted CI when configured;
- local validation execution cache: untracked branch-local, worktree-local, and change-local state that can speed eligible repeated local validation but is not portable and is not lifecycle evidence;
- local Codex runtime state: `.codex/skills/`, ignored by Git and installed locally from public Codex adapter output when contributors need local Codex use;
- public adapter packages: tracked `dist/adapters/` output during the compatibility window through `v0.1.2`, then generated temporary or release-output packages and release archives for `v0.1.3` and later;
- mapped skill-local resource parity: canonical `skills/<skill>/` resources, generated adapter output, locally packed release candidates, and clean installed target skill roots preserve skill-root relative paths and raw-byte SHA-256 unless an explicit transformation contract applies;
- adapter support metadata: `dist/adapters/manifest.yaml` and `dist/adapters/README.md`, tracked guidance and support surfaces rather than authored skill bodies;
- adapter artifact metadata: `docs/reports/adapter-artifacts/releases/<version>.yaml`, tracked release evidence with source commit, generator command, required per-adapter archive list, optional combined archive details, checksums, install roots, and validation result;
- adapter release artifacts: generated per-adapter archives, plus optional combined archive, uploaded as release assets rather than committed by default;
- bundled CLI adapter metadata: official adapter artifact metadata included in the CLI package for compatible supported adapter releases so local archive installation can verify one user-supplied archive without a separate metadata flag;
- downstream project manifest: `rigorloop.yaml` written at the target project root only when `rigorloop init <target> --write-state` is requested; schema v2 records target-oriented `targets` and does not claim workflow readiness;
- downstream project lockfile: `rigorloop.lock` written at the target project root only when `rigorloop init <target> --write-state` is requested after verified target installation; schema v3 records `generated.targets`, while legacy schema v1/v2 state remains compatibility input rather than canonical output;
- downstream runtime adapter roots: `.agents/skills`, `.claude/skills`, `.opencode/skills`, and `.opencode/commands` inside a user project; these are installed generated output, not authored RigorLoop source;
- durable reports: `docs/reports/`, authored from local measurement evidence and linked from change-local artifacts when produced by a change;
- validation cache evidence: `docs/changes/<change-id>/validation-cache-evidence.yaml` for formal cache-hit claims and `docs/changes/<change-id>/validation-cache-measurement.yaml` for Workstream A measurement;
- token-cost benchmark fixtures: `benchmarks/token-cost/`, authored prompt and fixture inputs used to exercise public skills in a downstream-style project;
- token-cost temporary runs: isolated directories under system temp or `$RUNNER_TEMP`, disposable and not durable release evidence;
- token-cost release evidence: `docs/reports/token-cost/releases/<version>.md`, `docs/reports/token-cost/releases/<version>.yaml`, and tracked raw or sanitized run summaries under `docs/reports/token-cost/runs/<version>/`;
- release evidence: tracked `docs/releases/v<version>.md`, `docs/releases/<version>/release.yaml`, release notes, and maintainer smoke evidence used by release verification.
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

For change-record evidence, the selector's routing responsibility includes registered evidence-class matching. `manual-routing-required` is a diagnostic and registration-debt signal for deterministic in-repo evidence, not a durable CI workaround. The query helper belongs beside validation scripts but has a separate role: it reads bounded metadata slices and must not run proof commands.

Validation idempotency is a proof-preserving optimization layer inside validation execution. It may skip work only when the eligible validator's complete input surface, canonical normalized command, implementation manifest, policy/config manifest, and previous actual-run passing result trace are unchanged. It does not change selector routing, selected check IDs, validator semantics, failure detection, exit codes, or closeout requirements.

The helper mode is an adoption surface, not an expansion of cache power. It makes the safe inner-loop path short enough to use, while preserving direct actual-run validation for closeout and final gates. Formal helper evidence records both the user-visible helper command and the canonical direct command used for cache identity so reviewers can see what was invoked and what prior pass was reused.

The local execution cache is an optimization surface, not evidence. Formal cache-hit evidence is change-local YAML that explains why the prior pass still applies. Closeout gates require actual-run evidence and reject cache-only pass claims. Workstream B edit-scoped validation is a separate future architecture decision because it would reduce selected validators based on changed inputs rather than identical input surfaces.

Workflow-state synchronization is a bounded lifecycle-validation responsibility. The parser reads exact owner and projection fields rather than arbitrary prose, treats `Current Handoff Summary` as the active plan live-state owner, treats `docs/plan.md` and current milestone state as projections, treats `Readiness` as a pointer, and treats progress, review logs, review resolutions, validation notes, explain-change, verify, and PR evidence as ledgers or evidence with narrower ownership. This preserves historical text while letting the state-sync gate fail a transition before a stale projection or contradictory evidence reaches downstream review, verify, or PR readiness.

### Authoring autoprogression policy

Authoring autoprogression is opt-in, change-local workflow policy. The closed profile set starts with `off` and `authoring-through-plan-review`; unknown values fail closed. The user-facing `auto-through: plan-review` maps to the internal `autoprogression.profile: authoring-through-plan-review`.

Authorization and proposal readiness are deliberately separate. Gate-ready proposals prove accepted direction and clean proposal-review evidence; armed profiles prove user intent. Activation requires both, plus durable authorization persistence, before any profile-driven transition may run.

The profile preserves review independence by invoking each review as a separate formal stage that reads tracked artifacts, governing sources, formal criteria, and relevant recorded findings. If a fresh execution context is unavailable, the review context is reset to those inputs rather than continuing the authoring narrative.

The transition budget is six stage slots per activation: `spec`, `spec-review`, `architecture`, `architecture-review`, `plan`, and `plan-review`. Skipped architecture slots do not authorize other stages. Resumed rereview budgets include only uncompleted stages plus explicitly authorized rereview stages. Manual edits never auto-resume a paused profile.

Stop results are part of the audit trail. They name the last completed stage, stopped stage, reason, required next action, and whether the profile remains armed or paused. Clean completion records that the profile stopped at `plan-review` and that `test-spec` is the next stage but was not invoked.

### Published skill resource integrity

Published skill resource integrity is a cross-cutting validation and packaging rule. `skills/` remains the only authored skill source. Packaged skill-local resources live beneath their skill root and are valid only when mapped in `SKILL.md`, present in canonical source, included in generated output, included in packed release candidates, and present after target installation.

The default resource identity is skill-root relative path plus raw-byte SHA-256. This rejects stale generated copies and accidental line-ending or content rewrites. Intentional resource transformations are exceptions only when a transformation contract names the input path, owner, output path, expected identity, and validation command.

The migration lint is intentionally bounded. It catches legacy resource-loading instructions such as `templates/...` without treating ordinary artifact paths, customer-project paths, or code examples as package dependencies. Existing drift starts as audit-mode migration debt, but new or changed skills must satisfy the resource-integrity rules immediately once implemented.

Runtime fallback is an emergency work-continuation rule, not package validation. A missing mapped resource keeps package validation failing; runtime may continue only for redundant convenience resources whose complete contract is already in `SKILL.md` and whose contents do not require invention.

### Project-map current-state orientation

Project maps are living orientation references. They are useful for locating likely modules, entry points, tests, CI surfaces, external boundaries, risks, and known gaps, but they do not outrank source, runtime configuration, schemas, build manifests, tests, CI workflows, or governing workflow artifacts.

The root map stays concise and remains the repository entry point whenever area maps exist. Area maps provide bounded depth only for durable repository boundaries and must be registered from the root map. Overlapping maps name the overlap and assign detailed ownership to one map to avoid contradictory parallel architecture descriptions.

Map trust is evidence-bound. Every map records freshness metadata, baseline, coverage, exclusions, and known gaps. Material current-state claims cite repository paths, observed and inferred claims remain distinguishable, and unknowns are recorded rather than silently filled. Intent artifacts such as proposals, specs, architecture plans, ADRs, and execution plans may explain expected or planned behavior, but they are not current-state proof.

Correction notes preserve downstream safety when a refresh finds the earlier map was wrong at its recorded baseline rather than merely stale. A correction note is result evidence, not a fourth map status.

The project-map skeleton owns reusable output structure only. Evidence ranking, inference policy, refresh triggers, future-design prohibitions, handoff rules, and claim boundaries stay in `SKILL.md` so the packaged asset cannot become a hidden policy surface.

### Change-record catalog model

Change records are cataloged by evidence class and queried by bounded slices. `change.yaml` remains authoritative for validation inventory and summary metadata, but current live workflow state belongs to the active plan, durable rationale belongs to `explain-change.md`, and material review status belongs to review artifacts. Full change-record reads remain valid for forensic reconstruction, disputed evidence, selector debugging, migration checks, unsupported query shapes, and whole-record review.

### Diagram source policy

Package diagrams have one authored source file and are linked from `architecture.md` by relative path. Default Mermaid diagrams use `.mmd` files under the package `diagrams/` directory. Mermaid flowchart or graph C4 diagrams use shared role classes for people, the system under review, external systems, and containers; generated images, if added later for publication, are derived output and are not edited by hand.

### Generated output

Canonical skills and adapter templates are authored sources. `.codex/skills/`, public adapter skill copies, adapter archives, and OpenCode command aliases are generated or installed runtime outputs produced from canonical sources and approved templates or metadata. Public adapter output may be copied into `.codex/skills/` only as local ignored runtime installation; generated output must not become an authored source of truth.

After `.codex/skills/` is untracked, non-release local Codex mirror validation proves generation into a non-tracked output surface rather than tracked-file equality. Release validation for the `v0.1.1` transition release does not use `.codex/skills/` as release evidence; it proves the public adapter path works. Public adapter skill copies stay tracked until at least one stable public release has shipped downloadable adapter artifacts and release-artifact installation docs. `v0.1.2` satisfies that compatibility-window rule. For `v0.1.3` and later, public adapter skill-copy drift checks are replaced by generated temporary-output or release-artifact validation, and root guidance points ordinary contributors to `dist/adapters/README.md` as the active adapter install-contract surface.

### Release and adapter evidence

Release verification uses tracked `docs/releases/<version>/release.yaml` and `release-notes.md` plus maintainer smoke evidence. Generated release notes are not authoritative for adapter compatibility claims.

The standing release-process contract adds `docs/releases/v<version>.md` as the durable routine publish evidence surface. It records release type, version decision, source identity, package identity, dist-tag, publish path, provenance mode, pre-publish gate results, package contents, publication event, registry verification, smoke results, recovery notes, and follow-up. Related change records link to this release evidence when a publish is tied to a lifecycle change, but the release record remains version-scoped.

Routine publish evidence is operational evidence, not a substitute for upstream lifecycle review. It can prove that already-approved work was packaged and published correctly; it cannot approve new package-surface decisions, release-process changes, new adapter targets, or changed authentication/provenance policy.

Release evidence must suppress secrets and machine-local details. It records command families, public registry references, package identity, checksums or integrity values, and bounded results, but not npm tokens, OTPs, credentials, raw environment dumps, private hostnames, usernames, or machine-local absolute paths.

Emergency deferrals are part of the release evidence surface. A deferral must name the deferred gate item, approving owner or owning stage, emergency rationale, reason for deferral, validation impact, accepted risk, follow-up location, and deadline or next lifecycle stage. Failed gate evidence must remain visible as failed or deferred-with-owner-risk, not rewritten as passed.

Generated adapter releases have an additional artifact evidence layer. `docs/reports/adapter-artifacts/releases/<version>.yaml` records release version, source commit, generator command, canonical source, manifest path, generated archive names, SHA-256 checksums, validation command, and validation result. Public releases that distribute generated adapters publish separate per-adapter archives as release assets and may publish a combined archive for convenience. The repository tracks metadata and checksums, not generated archive files by default.

The `v0.1.1` transition release does not require downloadable adapter archives. `dist/adapters/` remains the public adapter install path, and release notes or adapter docs state whether archives are absent or separately published. If a separate accepted plan publishes optional archives for `v0.1.1`, repository-tree installation from `dist/adapters/` remains the required public install path for that release and archive metadata becomes additional evidence rather than a replacement for tracked public adapter validation.

The `v0.1.2` archive-introduction release keeps repository-tree adapter packages for the compatibility window while publishing downloadable archives and metadata. For `v0.1.3` and later, release archives are the active install surface, `dist/adapters/README.md` and `dist/adapters/manifest.yaml` remain tracked, and generated adapter package contents are validated from temporary or release-output directories rather than tracked `dist/adapters/<adapter>/` package trees.

### CLI package, project scaffold, and lockfile boundary

The CLI package is an additive delivery surface. It can carry executable command code, small project scaffolds, and bundled official adapter metadata, but it does not own canonical workflow content, skill bodies, adapter generation rules, validation authority, or release readiness.

For `0.3.0`, target-native init supersedes the public `init --adapter` command shape. The canonical commands are `rigorloop init codex`, `rigorloop init claude`, and `rigorloop init opencode`; `--adapter` is rejected before mutation.

The generated project manifest is `rigorloop.yaml`. It is written only when `rigorloop init <target> --write-state` is requested. Schema v2 uses target-oriented user-visible keys, with top-level `targets`, and does not claim validation success, workflow readiness, branch readiness, PR readiness, or lockfile authority. Default `init <target>` never writes state files but may read existing state files for safety before mutating target roots.

`rigorloop new-change` is also a scaffold command, but it scaffolds change-local traceability rather than project installation state. It creates only `docs/changes/<change-id>/change.yaml` in the first slice, with empty `artifacts`, `requirements`, `tests`, `validation`, and `changed_files` until later workflow stages produce real evidence. It deliberately omits `explain-change.md` and `artifacts.explain_change` so a placeholder file cannot be mistaken for durable reasoning.

The `new-change` mutation boundary is local and non-networked. It validates option domains and safe path segments before planning writes, blocks on symlinks and overwrite conflicts before mutation, reports every planned directory and file action, and uses the shared CLI JSON status and exit-code contract. Partial write failures are observable rather than atomic: already-completed actions are reported, the failed path is reported, and the command does not claim success.

`rigorloop.lock` is machine-owned downstream project state. It records verified generated target output after successful init only when `--write-state` is requested. It is written only by the CLI. Schema v3 uses `generated.targets`; schema v1 Codex-only and schema v2 mixed-adapter lockfiles remain compatibility input for safety parsing and migration behavior, not canonical output for new target-native state.

State write ordering is intentionally one-way: planned target-root writes are reported first, existing state files are parsed enough for safety before mutation when present, drift and root conflicts block before destructive replacement, archive and generated-output verification happen before target-oriented state is written, and partial installation failures must not create state claims.

The CLI updates only the fields it owns when `--write-state` is requested: package identity/version, normalized manifest hash where specified, and the matching target entry or schema wrapper. Unknown state shape, unsupported schema versions, unsupported target or legacy adapter entries, unsupported source values, unsupported tree hash algorithms, malformed YAML, invalid field types, ambiguous state, and drifted generated output block according to the approved exit-code contract. `--force` does not replace arbitrary state in this slice.

Local archive mode keeps the user command to one archive path and moves metadata responsibility into the CLI package. This creates a package-content obligation: each package version that supports local archive install must include official adapter metadata for its compatible supported adapter releases. If that metadata is absent, local archive init blocks instead of falling back to unverified extraction.

Network archive download remains a release-asset boundary. The CLI may use Node built-in env-proxy behavior only when the runtime supports and enables it, but the first proxy-aware slice does not add programmatic Undici dispatcher ownership. Failed downloads report bounded diagnostics and point users to the verified local archive fallback without printing credentials, raw proxy URLs, private hostnames, tokens, request headers, raw environment values, or machine-local paths.

Public npm publication is an approved deployment boundary for `@xiongxianfei/rigorloop@0.1.4` only when the npm publication spec is satisfied. The package may still be built and tested locally or from a packed artifact, but FU-010 closes only after public publication evidence and real Codex install proof exist. For the target-native `0.3.0` boundary, pre-publish release proof uses packed-package non-dry-run smoke for every supported target, and post-publish proof uses live registry/download smoke.

### Authoring autoprogression policy boundary

`authoring-through-plan-review` is a repository workflow policy profile, not a new service, background worker, external scheduler, or CLI deployment boundary. It executes only inside an active workflow-managed interaction and uses the existing stage skills and review-recording surfaces.

The policy record is change-local. `change.yaml` is the canonical persistence surface when its contract accepts policy data. `workflow-policy.yaml` is a fallback only for an explicit change-metadata contract rejection, and the activation audit trail records that fallback. The record carries the profile name, authorizing user, authorization timestamp, change ID, profile status, and fallback-path evidence when relevant. It does not carry secrets or external credentials.

The workflow-state ownership boundary stays unchanged: active-plan handoff state, stage readiness, review results, branch readiness, PR readiness, and review-resolution closeout remain owned by their existing surfaces. Profile policy metadata can prove that automatic authoring continuation is authorized; it cannot prove that a stage is complete or that a downstream handoff is ready.

Rollback is local to workflow policy: setting the profile to `off`, after durable cancellation recording succeeds, restores explicit `proposal-review -> spec` triggering for that change. Already-created specs, plans, architecture artifacts, and formal review records remain historical evidence and are not deleted merely because automation is disabled.

### Public npm package boundary

The npm package is a delivery artifact for the CLI. It can include runtime CLI code, package metadata, package-local README and license files, and bundled official adapter metadata for the compatible Codex adapter release. It must not include adapter archives, generated public adapter skill bodies, repository lifecycle artifacts, tests, local fixtures, secrets, `.codex`, `.agents`, or generated adapter package trees.

Publication has one selected mode. Trusted-publishing mode uses `.github/workflows/release.yml` and npm OIDC. Bootstrap mode is a one-time manual publication path for `@xiongxianfei/rigorloop@0.1.4` only when trusted publishing cannot be configured before package creation. Bootstrap mode separates release readiness ownership from npm publish execution: `release.yml` or `release-verify.sh` owns readiness, and the maintainer publishes only the exact verified tarball recorded in publication evidence.

For release-process-contract releases after the bootstrap publication boundary, trusted publishing/OIDC remains the preferred npm path. Manual token or manual 2FA fallback is operationally allowed when trusted publishing is not available, but it must record the reason and satisfy the same non-deferrable evidence, package identity, registry verification, recovery, and secret-suppression boundaries. Staged publishing is deferred until trusted publishing works reliably.

The npm package does not replace GitHub release assets for adapter archives. `rigorloop init codex`, `rigorloop init claude`, and `rigorloop init opencode` install generated target support from official GitHub release archives or verified local archives matched against package-bundled metadata.

### Release token-friendliness evidence

Public releases add a token-friendliness evidence layer beside adapter release evidence. Markdown reports are for reviewers; YAML metadata is for release gates. The first required runtime benchmark is Codex; Claude Code and opencode dynamic benchmarks remain optional until stable runners and comparable reports exist. Final public releases require `dynamic_runtime.status: pass` or a valid approved waiver. RC and draft reports may record `blocked` or `not-run` dynamic status only with structured incomplete-state metadata.

Raw Codex JSONL may be omitted when it is too large or sensitive, but durable evidence must remain structured through analyzer summaries or sanitized summaries. Release validation checks for raw JSONL or a valid sanitized substitute, not raw JSONL unconditionally.

`skill-token-runtime-v2` expands dynamic coverage with a required core suite, one-release transition carryover benchmarks, optional extended benchmarks, and changed-skill-required benchmarks. Optional benchmark problems remain warnings unless the benchmark is required by changed-skill policy or explicitly claimed as release coverage. Claimed optional coverage is gated coverage: missing, invalid, failed, not reviewed, or unwaived inconclusive claimed results block final release.

Release validation owns changed public skill detection and generated-adapter-to-canonical-skill tracing. Token-cost validation owns proving that the report satisfies the required benchmark context supplied by release validation.

Manual result-quality review is structured release evidence for v2. Required or claimed coverage must have passing result quality or a valid role-scoped waiver. Optional unclaimed failures and inconclusive results use stable warning codes and must not be summarized as passing coverage.

### Measurement reports

Reports under `docs/reports/` are durable authored evidence for longitudinal comparison. Token-cost reports live under `docs/reports/token-cost/` and summarize measured static skill cost, Codex session cost, tool-output amplification, top cost drivers, conclusions, and next actions. Release token-friendliness reports live under `docs/reports/token-cost/releases/` and compare against the previous public release report when one exists or declare the first report as the baseline. Change-local artifacts should link to these reports rather than duplicating their body.

Validation cache measurement lives under `docs/changes/<change-id>/validation-cache-measurement.yaml` for the implementing change. It records Workstream A cache-hit value, helper adoption, actual-run fallbacks, closeout actual runs, and remaining validation cost. That measurement is the required evidence gate before any future edit-scoped validation or broader cache-eligibility proposal can argue that riskier scope narrowing or expansion is worth pursuing.

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
- `docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md`: change records as registered and queryable catalogs, with evidence-class selector routing and bounded query-helper reads.
- `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md`: validation cache hits for unchanged explicit-path lifecycle inputs, with a cache-aware inner-loop helper mode, canonical direct-command cache identity, local-only cache state, formal cache-hit evidence, closeout actual-run gates, and Workstream B measurement gating.
- `docs/adr/ADR-20260523-release-process-contract.md`: standing release-process boundary, routine publish evidence under `docs/releases/v<version>.md`, preferred trusted publishing, manual fallback limits, emergency deferral contract, and fix-forward/deprecate recovery for bad package content.
- `docs/adr/ADR-20260524-target-native-init-state-boundary.md`: target-native init, explicit state-write boundary, target-oriented state schemas, default state byte preservation with safety reads, and real non-dry-run release smoke gates.
- `docs/adr/ADR-20260623-published-skill-resource-integrity.md`: mapped skill-local resource integrity, bounded legacy-reference lint, raw-byte parity, packed clean-install proof, and runtime fallback/package-validity separation.
- `docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md`: closed `authoring-through-plan-review` profile, durable change-local authorization persistence, review-independent bounded authoring chain, and stop-before-test-spec boundary.

No additional ADR is required for the 2026-04-29 package-quality refinement because it sharpens the accepted method without changing the durable architecture decision.

No additional ADR is required for `rigorloop new-change` because it is an additive command inside the existing CLI package boundary and does not introduce a new durable source-of-truth, packaging, release, validation, or persistence decision.

No additional ADR is required for the 2026-05-12 record-every-formal-review amendment because it refines the existing review artifact and workflow evidence architecture under the approved formal review recording spec. The durable rule is carried by `specs/formal-review-recording.md`, and this canonical package records the affected runtime and crosscutting architecture.

No additional ADR is required for the `v0.1.1` single-authored-source transition release because ADR-20260512 already records the durable generated-output and adapter release artifact migration. This package revision records the release-specific validation and packaging architecture for the transition window.

No additional ADR is required for script output optimization because it refines repository-owned validation output presentation inside the existing selector, test-runner, and CI-wrapper architecture. It does not introduce a new system boundary, persistence model, packaging model, release model, or durable source-of-truth decision.

No additional ADR is required for the evidence-bound `project-map` update because it applies existing published skill resource-integrity, generated-output, and living-reference workflow decisions to one skill and one packaged skeleton asset. The durable current behavior is carried by `specs/project-map.md` and this canonical package.

ADR `docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md` is required because this change introduces a durable workflow orchestration and persistence decision: a separately armed authoring profile, mandatory change-local authorization persistence, profile metadata ownership boundaries, recorded architecture-assessment routing, and a formal stop boundary before `test-spec` and implementation.

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
| CLI init safety | A user runs default `rigorloop init codex` in a project with existing files. | The CLI builds a write plan, refuses user-file overwrites by default, verifies bundled metadata and archive contents before extraction, preserves existing state files byte-for-byte, performs required safety reads before target-root mutation, and reports success/block/error through the stable command contract. |
| Multi-target init safety | A user runs `rigorloop init codex`, `rigorloop init claude`, or `rigorloop init opencode`. | The CLI selects an explicit internal descriptor, verifies a trusted release or local archive, installs only descriptor and metadata-selected roots, rejects unsupported targets and `--adapter` before mutation, and does not create state files by default. |
| Managed state opt-in | A user runs `rigorloop init codex --write-state`. | The CLI writes target-oriented `rigorloop.yaml` schema v2 and `rigorloop.lock` schema v3 only after verified install; new user-visible schema keys do not use `adapter` or `adapters`, and historical archive filename values may remain unchanged. |
| Release smoke fidelity | A maintainer prepares the target-native `0.3.0` release. | Packed-package pre-publish smoke and live registry/download post-publish smoke run real non-dry-run init for `codex`, `claude`, and `opencode`; dry-run output alone is not accepted as install proof. |
| Skill resource self-containment | A published skill maps a skill-local resource. | The resource exists in canonical source, generated output, locally packed release candidates, and clean installed target skill roots with matching relative path and raw-byte SHA-256 unless a transformation contract applies. |
| Project-map reliance safety | A downstream skill uses a project map to orient work. | The map exposes status, baseline, coverage, exclusions, known gaps, material path citations, inference labels, unknowns, correction notes when applicable, and configured-versus-executed command evidence; stale, partial, inferred, unknown, conflicting, or missing-path claims require direct source inspection before reliance. |
| Legacy resource migration safety | A skill contains legacy `templates/...` instructions outside the `Resource map`. | Bounded migration lint reports the unmapped skill-local resource reference without classifying ordinary artifact paths or examples as package dependencies. |
| opencode command alias integrity | A user installs opencode from an archive whose metadata declares command aliases. | The CLI installs `.opencode/skills` and `.opencode/commands` or fails verification; older compatible skills-only archives emit `opencode-command-aliases-not-declared` and record only installed roots. |
| CLI new-change safety | A user runs `rigorloop new-change <change-id> --title <title>` in a project with existing or missing `docs/changes/` paths. | The CLI validates the option domains, builds a write plan naming every affected path, blocks on unsafe change IDs, symlinks, existing planned files, and path-type conflicts, writes only `change.yaml`, and reports partial write failures without claiming success. |
| Lifecycle claim boundary | A user sees `docs/changes/<change-id>/change.yaml` created by `new-change`. | The generated metadata has empty artifact and evidence arrays, `review.status: pending`, and no `explain_change` artifact; file existence does not imply proposal acceptance, review completion, verification, or PR readiness. |
| Evidence routing determinism | A branch adds `docs/changes/<change-id>/behavior-preservation.md`. | The changed-path selector routes it through a registered evidence class before verify, or emits stable `manual-routing-required` registration debt. |
| Bounded readability | A stage needs the latest validation result or canonical artifact paths for a change. | `scripts/query-change-record.py` returns the requested slice without requiring full validation history or executing validation commands. |
| Cache-hit safety | A repeated explicit-path lifecycle validation command is requested after an unrelated edit. | Cache hit occurs only when previous result was `pass` and normalized command, input-surface hash, implementation hash, and policy/config hash all match; otherwise the validator runs. |
| Inner-loop helper adoption | A contributor repeats lifecycle validation after change-local evidence edits. | `--mode explicit-paths-inner-loop` supplies cache context by default, normalizes to canonical direct `--mode explicit-paths` cache identity, and records displayed helper argv separately from canonical cache argv in formal evidence. |
| Workflow-state synchronization | A planned-initiative handoff updates `Current Handoff Summary` but leaves `docs/plan.md`, current milestone state, `Readiness`, review evidence, or change metadata stale. | The lifecycle state-sync check reports the owner/projection or evidence mismatch and blocks downstream readiness until the bounded live-state surfaces agree. |
| Authoring autoprogression safety | A user arms `auto-through: plan-review` for a workflow-managed change. | The workflow activates only after `armed && gate-ready` and durable authorization persistence, records each automatic stage and review, pauses on ambiguity or non-clean evidence, and stops after clean `plan-review` without invoking `test-spec` or implementation. |
| Closeout gate safety | A milestone closeout record cites only `cache-hit-inner-loop` evidence. | Lifecycle or change-metadata validation rejects the closeout because first-slice closeout requires `actual-run-pass`. |
| Local archive verification | A user runs `rigorloop init codex --from-archive <path>`. | The CLI verifies the archive against bundled official metadata for the installed package's compatible target release and blocks with `metadata-unavailable` if metadata is absent. |
| State determinism | A user reruns `rigorloop init codex --write-state` after a verified install with unchanged generated output. | The CLI computes the same normalized manifest hash and `rigorloop-tree-hash-v1`, preserves supported unrelated entries, and produces byte-identical target-oriented state content for identical state. |
| Lockfile schema v2 compatibility | A user adds Claude Code or opencode to a project with a valid schema v1 Codex lockfile. | The CLI verifies existing Codex generated output against the recorded hash before upgrading to schema v2; drift blocks before unrelated adapter mutation. |
| State drift safety | A user reruns `rigorloop init codex` after generated files under `.agents/skills` were modified while existing state records Codex. | The CLI reports drift with expected and actual tree hashes when available and blocks destructive replacement by default before target-root mutation. |
| Proxy diagnostic safety | A network archive download fails in a proxied environment. | JSON diagnostics expose only bounded fields and allowed enum values; human output recommends `--from-archive`; neither mode prints raw proxy values, credentials, private hostnames, request headers, or machine-local paths. |
| npm publication safety | A maintainer publishes `@xiongxianfei/rigorloop@0.1.4`. | Publication evidence records exactly one publication mode, package-content validation, packed-package smoke, trusted-publishing or bootstrap identity, npm package URL, and real Codex install smoke before FU-010 closes. |
| Standing release-process safety | A maintainer publishes a routine release after the release-process contract is active. | Release evidence under `docs/releases/v<version>.md` records release type, version decision, source commit, package identity, dist-tag, full gate, package preview, packed install smoke, publish path, provenance mode, registry verification, recovery notes, and follow-up without requiring a new proposal/spec/plan when no new decision is introduced. |
| Emergency deferral safety | A maintainer publishes an emergency release with a deferred gate item. | Evidence records owner approval, rationale, deferred item, validation impact, accepted risk, follow-up location, and deadline; non-deferrable evidence, secret suppression, package/source/version/dist-tag recording, publish-path recording, registry verification, and recovery/follow-up recording still pass. |
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
| Routine publish could smuggle a release-process or package-surface change | Release evidence must classify the release type before publish. Process changes, new package names or scopes, new adapter targets, changed auth/provenance policy, and changed publish mechanics stay lifecycle-managed and cannot be treated as routine operations. |
| Emergency release deferrals could become generic gate bypasses | Deferrals require owner approval, reason, validation impact, accepted risk, follow-up location, and deadline. Non-deferrable release requirements remain mandatory, and failed gate evidence must be recorded rather than hidden. |
| Release evidence could leak credentials or machine details | The release evidence boundary records command families and bounded public facts only. Tokens, OTPs, credentials, private environment dumps, private hostnames, usernames, and machine-local absolute paths are forbidden. |
| Dry-run smoke could hide a broken real target install | Target-native `0.3.0` release readiness requires actual non-dry-run packed-package smoke before publish and live registry/download smoke after publish for `codex`, `claude`, and `opencode`. Historical FU-010 closeout still requires real Codex install proof for the `0.1.4` publication boundary. |
| Local archive extraction could overwrite or escape project boundaries | The CLI write plan refuses user-file overwrites by default, rejects absolute paths, parent traversal, symlinks, drive-letter paths, and paths outside `.agents/skills`, and maps expected verification failures to exit code `3`. |
| Lockfile could be mistaken for canonical source or release metadata | The lockfile records downstream generated-output state only. Canonical workflow, skill, schema, adapter metadata, and release evidence stay in repository-authored or release-evidence surfaces. |
| Unknown future lockfile shape could be silently erased by older CLIs | The first lockfile schema blocks on unknown top-level sections, unknown fields, unsupported schema versions, unsupported adapters, unsupported source values, and unsupported tree hash algorithms before mutation. |
| Target installation could succeed while state writing fails | The CLI reports state-write failure explicitly and must not claim durable manifest or lockfile state was recorded; later recovery or repair commands require a separate spec. |
| Users could rely on `latest` for reproducible setup | The public command model allows `latest` for quick starts but pinned package versions are the reproducible path. `latest` with incompatible local archives blocks unless a compatibility rule exists. |
| `new-change` scaffolds could be mistaken for completed workflow evidence | The first `new-change` slice writes only `change.yaml`, leaves `artifacts` and evidence arrays empty, sets review state to pending, and avoids durable-looking Markdown placeholders. Later status or validate commands must inspect actual artifacts rather than assuming scaffolded metadata means readiness. |
| Partial `new-change` filesystem writes could confuse users | The command preflights path conflicts, creates directories before files, reports completed and failed actions, and does not claim artifact-pack success after partial failure. It does not promise atomic rollback in the first slice. |
| Release validation could keep treating `.codex/skills/` as a privileged internal release path | The `v0.1.1` transition release gate validates public adapter output and only confirms `.codex/skills/` ignored/untracked state; optional local Codex smoke installs from the public Codex adapter path and stays outside required release evidence. |
| Generated adapter archives could create binary churn in Git | Generated archives are release assets by default; Git tracks artifact metadata and checksums instead of archive files. |
| Warning-only token budgets could be mistaken for CI gates | The first measurement slice treats budget thresholds as report warnings; hard gates require a later accepted proposal and spec. |
| Optional benchmark failures could be mistaken for passing release coverage | `skill-token-runtime-v2` separates optional warning evidence from claimed optional release coverage; claimed coverage follows required benchmark evidence and result-quality gates. |
| Shorter validation output could hide changed coverage or failure evidence | Script output optimization is presentation-only. Behavior-preservation evidence must prove selected checks, exit codes, failure detection, and failure evidence remain unchanged, and quiet mode must not hide non-success diagnostics. |
| Incomplete input surfaces could create stale validation cache hits | First-slice cache eligibility is limited to explicit-path lifecycle validation with deterministic input, implementation, and policy manifests; any unsupported or uncertain surface disables caching and runs the validator. |
| Helper mode could be mistaken for closeout proof | `explicit-paths-inner-loop` is explicitly inner-loop only, formal helper evidence uses `cache-hit-inner-loop` with `closeout_evidence: false`, and closeout validation rejects helper cache hits as sole proof. |
| Canonical helper cache identity could hide what command the user ran | Formal helper cache-hit evidence records both `displayed_command_argv` and `canonical_cache_argv`, so reviewers can distinguish the user-facing helper command from the direct command identity used for reuse. |
| Cache-hit evidence could be mistaken for closeout evidence | `cache-hit-inner-loop` is inner-loop evidence only. Closeout requires `actual-run-pass`, and lifecycle/change-metadata validators reject cache-only closeout claims. |
| Local cache state could leak machine details or become portable evidence | Local cache state remains untracked and may use local worktree identity only for invalidation. Tracked cache-hit evidence must use repository-relative paths and omit secrets, usernames, hostnames, credentials, machine-local absolute paths, and environment dumps. |
| Workstream B scope narrowing could be introduced without evidence | Workstream B remains out of scope until Workstream A measurement is recorded, reviewed, and a separate proposal or spec amendment authorizes the riskier behavior. |
| Evidence-class patterns could become too broad | Registry validation rejects broad catch-all patterns and ambiguous matches, and selector regression coverage proves registered recurring patterns route only their intended evidence classes. |
| `manual-routing-required` could become a permanent workaround | Deterministic in-repo evidence treats the diagnostic as registration debt, and verify readiness blocks unless debt is resolved or an owner-approved deferral records path, reason, validation impact, and follow-up. |
| Bounded query output could hide failures or blockers | Query helper outputs include blockers, unsupported-shape diagnostics, and detail pointers; full forensic reads remain required for disputed evidence, summary inconsistency, unsupported shapes, and whole-record review. |
| Stage-skill guidance could drift from query helper commands | Workstream B updates stage skills only after query helper commands are stable, and generated adapter validation is required whenever canonical stage-skill text changes. |
| Workflow-state validation could overreach into historical evidence | The state-sync gate parses bounded owner/projection/pointer fields and excludes historical ledgers and review records from stale-token rejection, while review-artifact consistency checks compare only structured finding and closeout evidence. |
| Workflow-state projections could become competing owners | The architecture assigns ownership to `Current Handoff Summary` and keeps `docs/plan.md`, milestone-state fields, `Readiness`, and change metadata as projections, pointers, or derived evidence; validators compare them to owners instead of deriving live next stage from them. |
| Authoring autoprogression could bypass proposal judgment | Activation requires a gate-ready accepted proposal, approved recorded proposal-review, no material findings, settled scope, and explicit user authorization before any profile-driven transition. |
| Profile policy could become live workflow state | Profile metadata records authorization only; active plans, review artifacts, readiness surfaces, and workflow-state validation keep current stage, next stage, review status, branch readiness, and PR readiness ownership. |
| Authorization audit could be missing on resume | Durable change-local authorization persistence is required before activation; missing, malformed, partial, or failed persistence pauses with `authorization-not-persisted`. |
| Consecutive stages could collapse review independence | Each profile review is a distinct formal invocation over tracked artifacts, governing sources, formal criteria, and recorded findings, with context reset when fresh context is unavailable. |
| Profile scope could creep into implementation | `authoring-through-plan-review` stops after clean `plan-review`; `test-spec`, implementation, verification, PR, release, deploy, and automatic review-fix loops require separate proposals and spec amendments. |
| Resource-integrity lint could over-classify examples as dependencies | Migration lint is bounded to recognized resource-loading instructions and approved skill-local prefixes; ordinary artifact paths, customer-project paths, and code examples stay outside the package contract unless used as load/copy/read/run instructions. |
| Runtime fallback could hide a broken package | Package validation remains failing for missing mapped resources, and fallback is allowed only for redundant convenience resources whose full contract already exists in `SKILL.md`. |
| Project maps could be mistaken for source-of-truth behavior contracts | The `project-map` contract makes maps living references only, requires source-ranked evidence for material current-state claims, and forces direct source inspection when map evidence is stale, partial, inferred, unknown, conflicting, security-sensitive, or exact-behavior critical. |
| Area maps could fragment repository orientation | The root map remains the required entry point whenever area maps exist, area maps require durable boundaries and root registration, and overlap names one detail owner rather than duplicating descriptions. |
| Project-map validation could overfit natural language | The first slice validates contract structure, skeleton presence, resource-map mapping, generated adapter inclusion, and small representative outputs; a dedicated artifact validator stays deferred until repeated produced-map drift appears. |

## Glossary

- ADR: architecture decision record that preserves a durable decision, alternatives, consequences, and follow-up.
- arc42: the 12-section architecture documentation model used by `architecture.md`.
- C4: context, container, component, and code-level structural diagram model.
- canonical architecture package: the long-lived current architecture source under `docs/architecture/system/`.
- change-local architecture delta: historical or explicitly exceptional evidence under `docs/changes/<change-id>/`; not part of the normal architecture authoring path.
- generated output: derived files under `.codex/skills/`, public adapter skill paths under `dist/adapters/`, generated adapter archives, and generated command aliases.
- mapped skill-local resource: a packaged resource under a skill root that is declared in that skill's `Resource map`.
- resource parity identity: the skill-root relative path plus raw-byte SHA-256 for an untransformed mapped resource.
- transformation contract: explicit ownership and expected identity for a resource intentionally changed between canonical source and generated, packed, or installed output.
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
- project map: living Markdown repository orientation reference that records current-state evidence, inference, unknowns, freshness metadata, risks, and open questions without overriding source code or workflow authority.
- root map: repository-level project map, normally `docs/project-map.md`, that remains the entry point when area maps exist.
- area map: bounded project map under `docs/project-map/<area>.md` for a durable service, package group, application, data platform, infrastructure subsystem, ownership area, or domain.
- material project-map claim: current-state claim a downstream agent could use to choose a module, trust a boundary, select tests, assess runtime or data flow, or decide whether a map is safe to rely on.
- correction note: project-map refresh result note that says a previous map claim was wrong at its recorded baseline rather than merely stale because the repository later changed.
- CLI package: the repository package boundary published as `@xiongxianfei/rigorloop` and exposing the `rigorloop` binary through local, packed, or npm delivery.
- publication mode: the selected public npm publication path, either `trusted-publishing` through `release.yml` and npm OIDC or one-time `bootstrap` manual publication of an exact verified tarball.
- publication evidence: durable release evidence under `docs/releases/<version>/npm-publication.md` recording package identity, selected publication mode, tarball identity, smoke results, npm URL, trusted publishing or bootstrap details, and real Codex install proof.
- standing release-process contract: approved release architecture and spec that define how already-reviewed source is packaged, published, verified from the registry, and recorded without re-running proposal/spec/plan ceremony for routine publishes.
- routine publish: publish operation for already-reviewed work that introduces no new product, release-process, package-surface, authentication, provenance, adapter-target, or publish-mechanics decision.
- emergency deferral: owner-approved temporary release-gate exception that records rationale, validation impact, accepted risk, follow-up location, and deadline while preserving non-deferrable release requirements.
- bundled adapter metadata: official adapter artifact metadata included in the CLI package for the package's compatible adapter release.
- adapter descriptor: CLI-owned adapter install contract that maps an adapter name to archive filename pattern, possible roots, manifest shape, and lockfile shape.
- planned lockfile content: lockfile-shaped command output that previews generated-output hashes without writing durable `rigorloop.lock`.
- durable lockfile: downstream project `rigorloop.lock` written by the CLI after verified adapter install to record generated-output state.
- `rigorloop-tree-hash-v1`: normalized tree-hash algorithm for generated adapter output, based on sorted relative file paths and normalized file hashes.
- proxy-safe diagnostic: download failure diagnostic that reports bounded recovery facts without credentials, raw proxy URLs, request headers, private hostnames, raw environment values, usernames, or machine-local paths.
- change metadata scaffold: draft `docs/changes/<change-id>/change.yaml` produced by `rigorloop new-change` before downstream workflow stages fill in real requirements, tests, validation, changed files, reviews, and durable reasoning artifacts.
- evidence class registry: repository-owned selector contract that maps recurring deterministic change-local evidence filenames to allowed roots, routes, validators, lifecycle expectations, and allowed or required conditions.
- registration debt: required resolution work created when deterministic in-repo evidence produces `manual-routing-required`.
- bounded read: a query path that returns the authoritative slice needed for a common change-record question without loading unrelated history.
- query helper: repository-owned command that returns bounded change-record slices without running validation proof commands.
- validation cache hit: reuse of a previous passing validator result when the normalized command, input surface, implementation manifest, and policy/config manifest are unchanged.
- cache-aware inner-loop helper mode: `validate-artifact-lifecycle.py --mode explicit-paths-inner-loop`, the user-facing helper command that supplies approved cache context for repeated inner-loop lifecycle validation.
- canonical cache argv: the normalized direct `validate-artifact-lifecycle.py --mode explicit-paths` argv used for helper cache identity.
- state-sync gate: parser-scoped lifecycle validation that compares planned-initiative live-state owners, projections, pointers, and structured evidence before downstream readiness is claimed.
- authoring autoprogression profile: closed workflow policy value that authorizes a bounded automatic authoring and review sequence for one change.
- gate-ready proposal: proposal artifact and review state proving accepted direction and clean proposal-review evidence, independent of user authorization.
- profile policy metadata: change-local authorization record that proves an autoprogression profile was authorized but does not own live stage or readiness state.
- architecture assessment: recorded workflow-managed micro-stage after approved `spec-review` that routes to `architecture`, `plan`, or pause for ambiguity.
- live-state surface: a bounded current-state artifact location, such as `Current Handoff Summary`, current milestone state, `Readiness`, the active or blocked plan-index row, and compact live-state metadata fields.
- displayed command argv: the normalized helper argv the user invoked, recorded in formal helper cache-hit evidence separately from canonical cache argv.
- local execution cache: untracked branch-local, worktree-local, change-local cache state used only to avoid repeated local validation execution.
- formal cache-hit evidence: tracked change-local YAML that records why a previous validator pass still applies and remains inner-loop evidence only.
- `cache-hit-inner-loop`: evidence kind for unchanged-input reuse; not eligible to satisfy stage or milestone closeout.
- `actual-run-pass`: evidence kind that the required validator or bundle actually executed and passed; eligible for first-slice closeout when it covers the required bundle.
- validation cache measurement: change-local YAML evidence that records Workstream A cache hits, misses, disabled evaluations, actual runs, time saved, remaining cost, and Workstream B recommendation state.

## Next artifacts

- Architecture-review for the proposal-gated authoring autoprogression architecture update and ADR.

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
- Change-Record Catalog Registration and Bounded Read Model: accepted proposal, approved spec, and accepted ADR define deterministic evidence-class registration, selector routing for recurring change-local evidence, registration-debt handling for `manual-routing-required`, and a bounded query-helper model for common stage-owned reads.
- Validation Idempotency and Cache-Hit Safety: accepted proposal, approved spec, and accepted ADR define first-slice explicit-path lifecycle validation cache hits, the cache-aware inner-loop helper mode, local-only execution cache state, formal cache-hit evidence, closeout actual-run gates, Workstream A measurement, and Workstream B deferral.
- Workflow-State Projection and Pre-Transition Synchronization Gate: accepted proposal and approved spec amendment define active-plan live-state ownership, mechanical projections, pointer-only readiness, bounded stale-token detection, review-evidence consistency, and the pre-transition state-sync gate.
- Target-Native Init Commands and Adapter Terminology Retirement: accepted proposal, approved spec, and accepted ADR define the 0.3.0 target-native init boundary, full public removal of `--adapter`, install-only default behavior, explicit `--write-state`, target-oriented state schemas, default state byte preservation with safety reads, and real non-dry-run release smoke gates.
- Published Skill Resource Integrity with an Architecture-Skill Pilot: accepted proposal, approved spec amendment, and accepted ADR define mapped resource integrity, bounded legacy lint, raw-byte generated and installed parity, locally packed release-candidate clean-install proof, and architecture-skill pilot resource-chain evidence.
- Evidence-Bound and Incremental `project-map`: accepted proposal and approved spec define evidence-bound map metadata, freshness, root/area registration, source-ranked claims, skeleton asset packaging, generated adapter inclusion, correction notes, and downstream reliance boundaries.
- Proposal-Gated Authoring Autoprogression: accepted proposal and approved spec amendments define a separately armed `authoring-through-plan-review` profile, mandatory durable authorization persistence, recorded architecture assessment, formal review independence, profile-state audit trail, direct-review isolation, and stop-before-test-spec boundary.

## Readiness

This canonical package revision records the current repository architecture for generated skill output, adapter release artifact migration, the `v0.1.1` single-authored-source transition release, the `v0.1.3` public adapter untracking release, the first RigorLoop CLI package plus Codex init slice, the durable lockfile extension for verified Codex init, the `new-change` metadata scaffolding slice, the first public npm publication boundary for `@xiongxianfei/rigorloop@0.1.4`, descriptor-driven multi-adapter init with proxy-safe download diagnostics, first-slice repository script output optimization, the change-record catalog model for registered evidence routing plus bounded reads, first-slice validation idempotency/cache-hit safety for unchanged explicit-path lifecycle validation inputs, the cache-aware inner-loop lifecycle validation helper mode, the target-native 0.3.0 init/state/release-smoke boundary, the published skill resource-integrity boundary for mapped skill-local resources, the evidence-bound `project-map` orientation boundary with root/area registration, skeleton asset packaging, generated adapter inclusion, correction notes, and downstream reliance limits, workflow-state synchronization through bounded lifecycle validation over active-plan owner fields, projections, pointers, and structured review evidence, and proposal-gated authoring autoprogression through a durable change-local profile policy boundary.

ADR `docs/adr/ADR-20260512-generated-skill-output-release-artifacts.md` records the durable decision to move generated local and public skill copies out of ordinary authored Git state through staged temp-output and release-artifact validation. ADR `docs/adr/ADR-20260513-v0-1-3-adapter-release-archive-install-surface.md` records the durable `v0.1.3` decision to make release archives the active public adapter install surface and retire tracked generated adapter package fragments. ADR `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md` records the first CLI package boundary, bundled local-archive metadata decision, planned-lockfile boundary, and original publication block. ADR `docs/adr/ADR-20260516-rigorloop-cli-lockfile.md` records the durable lockfile boundary, strict schema handling, drift comparison, and partial-failure write ordering for Codex init. ADR `docs/adr/ADR-20260516-rigorloop-npm-publication.md` records the first public npm publication boundary, package-content and publication-mode decisions, and real install closeout proof. ADR `docs/adr/ADR-20260518-multi-adapter-init-and-proxy-download.md` records descriptor-driven multi-adapter init, schema v2 mixed-root lockfiles, opencode skills-only compatibility, and proxy-safe diagnostics. ADR `docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md` records the durable decision to treat change records as registered and queryable catalogs. ADR `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md` records the durable decision to add validation cache hits for unchanged explicit-path lifecycle inputs, including the cache-aware inner-loop helper mode, while preserving actual-run closeout gates. ADR `docs/adr/ADR-20260524-target-native-init-state-boundary.md` records the durable target-native init, explicit state-write, target-oriented schema, state safety, and real smoke-gate decision. ADR `docs/adr/ADR-20260623-published-skill-resource-integrity.md` records the durable mapped-resource identity and clean-install proof decision. ADR `docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md` records the durable proposal-gated authoring autoprogression profile, policy persistence, and review-independence decision. No additional ADR is required for `rigorloop new-change` because it is an additive command inside the existing CLI package boundary and does not introduce a new durable source-of-truth, packaging, release, validation, or persistence decision. No new ADR is required for the cache-aware inner-loop helper because it amends the existing validation cache-hit safety decision rather than introducing a separate validation architecture. No additional ADR is required for the evidence-bound `project-map` update because it applies existing generated-output, skill resource-integrity, and living-reference workflow decisions to one published skill and one packaged skeleton asset. No new ADR is required for workflow-state synchronization because the accepted spec amends the existing single-source workflow-state contract and composes through the existing lifecycle-validation architecture instead of adding a new system boundary, storage boundary, parser authority, or service. No change-local architecture delta is produced because the canonical package carries the intended durable guidance directly.
