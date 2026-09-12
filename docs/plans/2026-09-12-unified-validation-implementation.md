# Unified Validation implementation

## Purpose / big picture

Implement the approved Validation contract: useful independent cases, one catalog and bounded executor, honest current-run evidence, no validation-result cache, and removal of the exact superseded sources and machinery. The result must prove the published skills and CLI together without making repository engineering tools a customer prerequisite.

## Current Handoff Summary

Owning change record: [unified validation and model hierarchy](../changes/2026-09-12-unified-validation-model/change.json). It owns activity, milestone state, review applicability and remaining work. This plan carries stable intent only.

This plan replaces the [directory plan](2026-09-12-design-directory-layout.md) as the primary allocation for remaining work. Preserve that plan, its `directory-m1`/`directory-m2` work identities and its exact review/evidence basis. The five `validation-mN` IDs below are additional work, never renamed or reset directory milestones. The directory work remains part of the complete final initiative diff and final assessment.

## Source artifacts

- Direction: [unified Validation proposal](../proposals/2026-09-12-unified-validation-model.md) and [three-model hierarchy proposal](../proposals/2026-09-12-skill-cli-engineering-model-hierarchy.md), with their separate Proposal Reviews in the owning change.
- Governing model: [Validation](../design/engineering/validation.md), including TEST-SR-01–14, VAL-SR-01–18, all eight boundary scenarios, technical constraints and exact source/consumer maps.
- Composition and realization: [System](../design/system.md), [Engineering](../design/engineering/engineering.md), [Skill](../design/skill/skill.md), [CLI](../design/cli/cli.md), [Packaging](../design/engineering/packaging.md), [Installation](../design/cli/installation.md) and [Release](../design/engineering/release.md).
- Assessment and representation: [Assessment](../design/skill/assessment.md), [Workflow](../design/skill/workflow.md), [Design method](../design/skill/authoring/design.md) and [Records](../design/cli/records.md).
- Design basis: original complete `design-review` plus current `directory-design-review`; the latter preserves relocated subjects and the explicit repository path override. Neither directory Delivery nor directory Code Review approves this remaining implementation.
- Retained legacy contracts: the seven specification/test-specification pairs and cache ADR listed in the source-retirement table below supply preserved proof intent under Validation's exact displacement map. The mixed simplification specification and system architecture retain their unselected obligations. They do not restore superseded cache or performance requirements.

## Context and orientation

Direct source inspection supplied orientation; `docs/project-map.md` predates the selected record/runtime and directory work and is not used as implementation authority. Recheck actual callers at each removal boundary rather than assuming this inventory remains exhaustive.

| Current surface | Observed implementation and necessary change |
| --- | --- |
| `scripts/validation_selection.py`, `scripts/select-validation.py` | Catalog and selector already own check IDs, templates, routing, reasons and `parallel_safe`. Extend the existing catalog with dependency, execution-unit and isolation constraints; preserve its public JSON/status/exit meanings. |
| `scripts/ci.sh` | Contains a selected-check Python scheduler, separate broad-smoke Bash scheduling/aggregation, duplicated broad-smoke sequential membership and direct-main product gates. Extract to `scripts/validation_execution.py`; preserve the wrapper's modes and release interception. |
| Historical broad-smoke metadata | `ci.sh` reads the June 27 classification YAML and baseline; the classification checker also depends on the June 26 classification. Replace runtime dependence with current catalog definitions; preserve historical bytes. |
| `scripts/test-select-validation.py` | Custom unittest loader, names/`-k` filtering and output contract; isolated CI workspaces explicitly copy module dependencies. Preserve these real entrypoint and wrapper boundaries when adding case execution. |
| `scripts/test-artifact-lifecycle-validator.py` | Unittest entrypoint, process/global-environment tests, current record and retained lifecycle/release assertions, and cache-specific cases. Retire cache-only expectations before the surviving case-isolation audit. |
| `scripts/test-change-metadata-validator.py` | Custom unittest loader/output contract, dynamically named output fixtures, actual v3 validator subprocesses and cache-measurement cases. Preserve discovery hooks and v3 negatives while retiring measurement acceptance. |
| `scripts/validate-artifact-lifecycle.py` | Imports `validation_cache`, supports `explicit-paths-inner-loop` and cache options, and can write cache/evidence. Remove that branch while retaining real direct validation and supported modes. |
| `scripts/validate-change-metadata.py` | Separately dispatches cache measurement YAML; current record validation delegates to the Node validator. Remove only measurement functionality and its exclusive helpers. |
| Shared published guidance | `templates/shared/test-quality.md` and `test-maintenance.md` feed selectively mapped resources checked by `scripts/skill_validation.py`. Update source and existing consumer copies coherently. |

No catalog-wide isolation claim follows from separate command names. Shell-scraped labels and historical classifications are migration inputs, not continuing owners. The current default cache directory was observed as a directory with one immediate entry; that is not a content-safety determination. M1 must inspect it again without following symlinks before any cleanup.

## Non-goals

No new Validation skill, public runner CLI, distributed worker, daemon, matrix fan-out, cache replacement, permanent measurement ledger, mandatory speed target or inventory-wide test rewrite. Keep record hashes, transaction safety, dependency-download caches, historical records and arbitrary user-selected caches. No release publication, remote configuration, PR, merge or customer-governance activation is authorized by this plan. Product requirements outside the approved hierarchy/Validation transfer remain with their owners.

## Requirements covered

All TEST criteria apply proportionately to the changed proof and cleanup scope. TEST-SR-14 retains its earlier necessary-design-only applicability; VAL-SR-13 separately authorizes this initiative's cleanup. Neither becomes a global test-removal or rerun waiver.

| Requirement basis | Allocation | Verification groups |
| --- | --- | --- |
| TEST-SR-01–06 | Every milestone derives independent expected observations and preserves useful boundary/property/regression protection. | TG-CACHE, TG-EXEC, TG-COMPOSE, TG-CASES, TG-ADOPT, TG-FINAL |
| TEST-SR-07–10, TEST-SR-12 | M1/M3/M4/M5 classify actual removals, discovery and fixture impact; establish retained protection first. | TG-CACHE, TG-COMPOSE, TG-CASES, TG-ADOPT |
| TEST-SR-11, TEST-SR-13–14 | M5 preserves selective portable criteria, scoped policy and separate assessment authority. Earlier directory proof is reassessed for current reliance. | TG-ADOPT, TG-FINAL |
| VAL-SR-01 | M4 corrects and executes cases independently in all three selected suites. | TG-CASES |
| VAL-SR-02, VAL-SR-04–05 | M2 defines validated trusted catalog/graph constraints; M3 applies them to broad/main; M4 adds audited units. | TG-EXEC, TG-COMPOSE, TG-CASES |
| VAL-SR-03, VAL-SR-06 | M1/M2 preserve routing and preflight; M3 preserves focused/boundary/main/release scope and diagnostic failure. | TG-CACHE, TG-EXEC, TG-COMPOSE, TG-FINAL |
| VAL-SR-07–10 | M2 establishes budgets/process ownership/reporting; M3 unifies modes; M4 proves nested and case execution. | TG-EXEC, TG-COMPOSE, TG-CASES, TG-FINAL |
| VAL-SR-11 | M1 removes result caching and measurement support; M5 retires remaining source consumers. | TG-CACHE, TG-ADOPT, TG-FINAL |
| VAL-SR-12, VAL-SR-18 | All milestones record actual scope/outcomes and limitations; M2/M3 preserve result interfaces without baseline dependence. | All groups |
| VAL-SR-13 | M1/M3 retire exclusive runtime machinery; M4 retains discovered protection; M5 completes exact source/consumer retirement. | TG-CACHE, TG-COMPOSE, TG-CASES, TG-ADOPT |
| VAL-SR-14–15 | All milestones preserve complete direct commands, owner checks, broad-smoke triggers and release/assessment boundaries. | All groups |
| VAL-SR-16 | M5 updates governance, skills, model consumers and generated candidate proof. | TG-ADOPT, TG-FINAL |
| VAL-SR-17 | M1 protects old state; M2–M4 own scratch/process resources; M5 preserves portable public guidance. | TG-CACHE, TG-EXEC, TG-COMPOSE, TG-CASES, TG-ADOPT |
| ENG-SR-01–12; SYS-SR-01–09; SKL-SR-24–27 | M5 integrates the selected hierarchy with delivered skill/CLI instructions and actual candidate proof; M1–M4 realize Engineering Validation. Preserve mapped original Skill/CLI/Packaging/Installation/Release contracts; this is no reopening of unselected product features. | TG-ADOPT, TG-FINAL |

## Milestones

### M1. Remove validation-result cache and measurement machinery

- Work ID and kind: `validation-m1`, implementation.
- Engineering purpose: make actual validation the only current execution path before auditing cases, so intentionally retired cache cases are not promoted into the new runner.
- Requirements and owner: VAL-SR-03/04/06/11–17, TEST-SR-02/04/07–12; Validation's cache and removal maps.
- Dependencies: approved current Design and this Delivery package; preserve the completed directory slice and existing record APIs.
- Scope and components: `validate-artifact-lifecycle.py`, `validate-change-metadata.py`, both corresponding test scripts, `validation_selection.py`, selector regressions, `validation_cache.py`, `test-validation-cache.py`, cache-only measurement fixtures and the exact root cache/ignore entry. Update active invocation guidance that otherwise tells users to call removed options; broader source consolidation remains M5.
- Steps: write no-write retired-input and actual-execution regressions; remove cache dispatch and selector registration; remove cache-only helpers/tests/fixtures after classifying protection; inspect and remove only the confirmed disposable default directory and exclusive ignore line. Check remaining callers before deleting helpers.
- Required verification: TG-CACHE. Run C1/C2/C3 and selected current v3 integrity proof C8. Record actual cleanup paths, symlink/content disposition, retained exceptions and source/fixture recovery identity.
- Expected result and completion: retained commands actually validate on repeated calls; retired flags/helper mode/measurement input reject; no runtime cache import or current cache-check route remains. Root cleanup is completed or a concrete unexpected-content finding blocks its completion. Mere inventory is insufficient.
- Review handoff: independent M1 Code Review of the caller/selector/removal slice and preserved failure detection.
- Risks and recovery: shared helpers or historical evidence can be mistaken for cache-only content. Restore the caller, selector and removed source slice together if surviving detection fails; never restore an unsupported cache as a hidden fallback. A symlink or unexpected default-cache content needs an explicit bounded owner disposition, not recursive deletion.

### M2. Extract the common executor and trusted task catalog

- Work ID and kind: `validation-m2`, implementation.
- Engineering purpose: establish one tested engine through the selected-check path before switching the more complicated broad/main graphs.
- Requirements and owner: VAL-SR-02–10/12/14/15/17/18, TEST-SR-03–06/10; Validation catalog, scheduler, process and reporting contracts.
- Dependencies: M1 review/corrections closed; no cache branch to preserve.
- Scope and components: extend `CheckCatalogEntry`/catalog validation in `validation_selection.py`; extract selected Python scheduling from `ci.sh` into the Design-named internal `validation_execution.py`; add focused `test-validation-execution.py` and register it in the existing selector. No new public runner interface. Preserve isolated CI fixture dependency closure.
- Steps: establish independent graph/process regressions first; validate complete metadata before launch; resolve argv from trusted catalog and scope; implement bounded dependency scheduling, exclusive barriers, scratch capture and process-tree cleanup; delegate selected local/explicit/PR/release execution to the module. Broad/main remain their existing paths until M3, with no claim that their duplication is already retired.
- Required verification: TG-EXEC and preserved selected/preflight cases from TG-COMPOSE. Run C1/C4; C3 when lifecycle execution boundaries change. Existing wrapper tests must use the real wrapper/module boundary, retaining controlled child processes rather than replacing execution with a passing mock.
- Expected result and completion: selected work uses the shared module; jobs default is capped as designed; explicit jobs/timeout, dependency failures, fail-fast, stable output and POSIX tree reaping satisfy the model. Unknown/malformed catalog metadata rejects before launch. Initial command units remain conservative until M4 case audit.
- Review handoff: independent M2 Code Review including catalog-to-launch trust, nested resource limits and extraction equivalence.
- Risks and recovery: extracting code can drop fields, leak descendants or break copied-workspace fixtures. Restore the selected wrapper/module/catalog slice together on regression; jobs=1 only reduces concurrency and cannot recover missing semantics. Retain full diagnostics and a reproducible failing process fixture.

### M3. Unify broad-smoke and main execution; retire historical classification readers

- Work ID and kind: `validation-m3`, implementation.
- Engineering purpose: remove duplicate membership/schedulers only after the common engine is established, with explicit artifact dependencies and one worker budget.
- Requirements and owner: VAL-SR-02–10/12–15/17/18, TEST-SR-04/07–10; Validation composition and Release-owned interception.
- Dependencies: M2 review/corrections closed.
- Scope and components: `ci.sh`, shared catalog/executor and their regressions; remove `validate-broad-smoke-classification.py` after replacement protection is demonstrated. Stop active reads of both June classification sources and the June 27 baseline. Preserve their bytes. Reconcile `.github/workflows/` only if actual callers require it; retain thin wrappers.
- Steps: inventory current sequential/parallel broad leaves, conditional review/lifecycle scopes and direct-main product checks; map each to retained identity/args/phase or explicit Design retirement. Put this current membership/dependencies in the catalog; resolve one invocation-owned adapter output and build-success dependency; flatten triggered broad smoke into the same graph. Preserve `release-coordinator.py check-ci` interception before PR/main, per-mode scope and diagnostic behavior. Delete old Bash/Python duplication and label scraping after replacement proof.
- Required verification: TG-COMPOSE and TG-EXEC through C1/C4. Controlled subprocess tests cover all modes without live publication. Run actual broad smoke C5 and C6 on the same engineering basis, recording applicable environment/input limits rather than bypassing blockers. C9 covers coordinator compatibility if its local callers are touched.
- Expected result and completion: selected, broad and main paths share the catalog/engine; required leaf membership survives; build failure prevents archive validation; current runs do not read historical classifications/baselines. `RIGORLOOP_BROAD_SMOKE_CLASSIFICATION` rejects explicitly. Existing result-output support and `cache_status: not-applicable` labels remain without a cache; unavailable historical comparisons are explicitly limited.
- Review handoff: independent M3 Code Review of complete mode/phase composition and removed-reader protection.
- Risks and recovery: flattening can lose scope, accidentally merge different proof, duplicate package writes or clear a diagnostic failure. Restore graph/catalog/wrapper together, preserve distinct subject/phase identity, and rerun affected mode tests. Sequential mode is a resource fallback, not permission to omit a graph branch.

### M4. Adopt genuinely independent cases in the three selected suites

- Work ID and kind: `validation-m4`, implementation.
- Engineering purpose: deliver the user-requested per-case independence and real concurrency, using the established shared budget rather than merely marking whole scripts parallel-safe.
- Requirements and owner: VAL-SR-01/02/04/05/07–10/12/14/17/18, TEST-SR-01–10; Validation case execution and scoped initial population.
- Dependencies: M3 review/corrections closed; cache/classification-only cases have explicit dispositions.
- Scope and components: `test-select-validation.py`, `test-artifact-lifecycle-validator.py`, `test-change-metadata-validator.py`, their shared mutable fixture dependencies, catalog discovery adapters and `validation_execution.py`/regressions. Node checks use native runner concurrency only within an allocated share. Other Python suites remain command tasks without a case-independence claim.
- Steps: audit each suite's normal loader, custom name/pattern hooks, dynamically named fixtures, imports, class/module setup, temporary roots, environment changes, nested wrappers and external resources. Preserve meaningful subtests within one case. Correct mutable fixture coupling, declare genuine external conflicts, add isolated normal-loader discovery, and invoke each discovered case through its own existing script/selector. Preserve the complete default suite and single-case reproduction.
- Required verification: TG-CASES plus process ownership TG-EXEC. Run C1/C2/C3 directly; execute all surviving discovered cases in each suite individually, sequentially and with allocated concurrency through C4's real integration path. Record per-suite discovered/started/completed sets and dispositions of deliberate retirements. Run C5/C6 after enabling adapters to prove the wrapper actually reaches these cases.
- Expected result and completion: all three selected populations demonstrate actual independent case execution and concurrent overlap where safe, with jobs=1 agreement and bounded descendants. Collection failure, duplicate/zero/disagreeing discovery and required skips cannot pass. A remaining externally constrained case can be visibly serialized, but declaring every suite serial or leaving its cases unaudited cannot complete this milestone.
- Review handoff: independent M4 Code Review of actual case/fixture isolation, complete discovery, representative nested-resource hazards and required real subprocess boundaries.
- Risks and recovery: subprocess startup can outweigh savings; repeated class setup can expose hidden assumptions. Make no speed claim without measurement. Retain complete direct commands and restore adapter/fixture/catalog changes together when protection differs. A normal ordered scenario remains one independent case; do not split its internal steps into dependent tests.

### M5. Complete source retirement, consumer adoption and product integration

- Work ID and kind: `validation-m5`, implementation.
- Engineering purpose: finish repository cleanup and publishable consumer coherence only after replacement execution and proof exist.
- Requirements and owner: VAL-SR-11–18, TEST-SR-07–14, ENG-SR-01–12 and affected SYS/SKL mappings; Validation owns retirement, Skill owns content, CLI owns executable boundaries, Packaging/Release retain artifact and publication contracts.
- Dependencies: M4 review/corrections closed; every selected source has an established retained/retired protection disposition.
- Scope and components: exact source-retirement table below; current governance/navigation; ten mapped skills and selective quality/maintenance resources; `templates/shared/`, `skill_validation.py` and relevant guide/model/selector consumers; generated skill/CLI candidates in isolated output. Preserve stable directory work, record formats and historical identities.
- Steps: reconcile current owner wording and independent/no-cache guidance at actual consumers; update canonical shared text then its existing projections; remove the seven source pairs/cache ADR and exact obsolete mixed-architecture sections/diagrams only after searching their readers and preserving necessary meaning. Resolve FU-012 within its selected scope. Build and validate current supported skill archives and the actual packed CLI; prove referenced resources and documented CLI instructions agree.
- Required verification: TG-ADOPT and TG-FINAL via C1–C8/C10, with C9 only where release integration changes. Retain existing mandatory unknown-value negatives and independently required release checks. Inspect mapped deletion/retention results and remaining references; historical source citations are explicitly distinguished from unresolved active readers.
- Expected result and completion: no mapped cache/classification runtime or duplicate current source survives; portable skills and contributor/CI commands agree on the merged owner; generated/packed products preserve content and executable compatibility. Unknown live consumers block affected removals; they are not dismissed as historical by path. This includes actual cleanup, not an audit-only milestone.
- Review handoff: independent M5 Code Review; then a fresh independent final whole-change Code Review of the complete initiative, including prior directory and hierarchy changes and all M1–M5 interactions.
- Risks and recovery: editing generated output, over-removing source files, or exposing internal IDs in public skills would violate retained owners. Correct canonical source and regenerate; restore a failed source/consumer/package slice coherently. Preserve historical records and user-owned files. Public installation evidence in local temporary destinations supplies no live publication permission.

## Verification groups

| Group | Objective and representative observable failures | Evidence expectations |
| --- | --- | --- |
| TG-CACHE | Repeated retained validation invokes the real validator, including second-run failure; retired cache flags/mode and measurement filenames reject before work/writes. Old caches remain unchanged during commands; only the specifically inspected default directory is eligible for one-time cleanup. V3 malformed/unknown/unsafe record inputs still reject. | Actual lifecycle/metadata/selector subprocess tests; before/after bytes and validator-invocation observations. Include absent default, disposable default, symlink and unexpected content paths without touching arbitrary user caches. Explicitly record cache-only obligation retirement, not equivalence with cache hits. |
| TG-EXEC | Trusted argv and full graph validation precede execution: unknown unit/field/status/check, duplicate IDs, command-basis drift, missing dependency/cycle and contradictory isolation metadata launch nothing. Ready work overlaps within budget; exclusive and dependency work do not. Stable first-required-failure exit survives reversed completion; fail-fast reports queued remainder and started failures. Timeout includes no queue time, uses the 300-second default and five-second grace, reaps descendant processes and cleans owned scratch. Invalid encoding/missing result/unavailable command are visible failures. | Independent process fixtures with barriers/markers and controlled clocks where appropriate; actual child/grandchild tests, deterministic case/result sets and unchanged unrelated sentinels. Test invalid positive-integer overrides, CPU-unavailable fallback, allocated Node/nested workers and prelaunch unsupported-platform handling. Avoid timing-only assertions or the executor calculating its own expected result. |
| TG-COMPOSE | Explicit/local/PR/release/main/broad retain distinct scope and JSON/exit interfaces. Input/preflight/focused failures prevent dependent boundary work; diagnostic broad smoke keeps the original failure. Deleted/renamed/shared paths select required proof. Flattening retains all reasons, merges only identical ID/argv/subject/phase, preserves main membership and `check-ci` interception. Build and archive verification share isolated output and a success dependency. | Real wrapper processes with synthetic safe repositories and controlled children plus actual sequential/concurrent broad runs. Missing-route sensitivity must fail even when broad smoke passes. Test classification override rejection and operation with historical metadata absent from the sandbox; historical repository files remain untouched. |
| TG-CASES | Normal discovery and custom filters identify complete, unique case IDs; a named selector executes exactly that case. Isolated setup survives order reversal and concurrent execution. Three-suite direct, individual, jobs=1 and bounded-parallel sets agree after explicit retirement dispositions. Subtests/property counterexamples retain diagnostics. Nested subprocess demand cannot multiply the budget. | Actual cases from all three scripts, not only a toy suite; standalone reproduction commands and discovered/started/completed ID comparison. Controlled negative discovery/import/worker mismatch, duplicate and zero-case cases; no success from skipped or lost required tests. Record external-resource constraints and unaudited populations without universal safety claims. |
| TG-ADOPT | Retained protection is established before deleting each selected script/source/assertion. Active owners/links, canonical guidance/projections and generated skill resources agree. Public skills remain selectively loaded and independently usable without repository paths, internal IDs or the CLI except current governed recording/CLI installation. No competing Test/Validation approval owner appears. | Actual consumer searches, source-qualified proof disposition, domain validator and package regressions, resource/hash parity, exact current subjects and preserved historical bytes. Reader-specific checks replace old-path assertions; do not delete unknown protection. |
| TG-FINAL | All milestones coexist: the actual wrapper selects/discovers/runs the needed candidate proof once within budget, reports real failures and uses no result cache/historical classification. Skills and packed CLI agree at resource, command, record and installation boundaries; private/temp/historical state stays protected. The final complete diff includes directory work, source transfers and every remaining implementation/correction. | Actual final C5/C6/C7/C8/C10 results under one declared engineering basis, mode/error integration proof from C1/C4, exact generated/packed identities, independent final whole-change review and distinct final Verify. Prior evidence reuse requires explicit unaffected-basis assessment; a passing subset or a recorded label is insufficient. |

### Boundary and integrated allocation

| Validation boundary dimension | Allocated proof and distinguishing outcome |
| --- | --- |
| Input domain | TG-CACHE/TG-EXEC: retired/unknown/malformed inputs reject before work and writes; supported cases run. |
| State/lifecycle | TG-COMPOSE/TG-FINAL: preflight/focused failure cannot become readiness through diagnostic execution or saved results. |
| Identity/authority | TG-EXEC/TG-ADOPT: catalog identity/argv/adapter basis is trusted; actual assessment and external authorization stay separate. |
| Composition/path | TG-COMPOSE/TG-CASES/TG-ADOPT: real public boundary and case selection survives shared-reader/source moves and packed resources. |
| Temporal/retry | TG-EXEC/TG-CASES: bounded overlap, serial barriers, complete reordered results and fresh execution on retry. |
| Failure/recovery | TG-EXEC/TG-CACHE: process-tree cleanup and visible partial results; unrelated state and historical data remain unchanged. |
| Compatibility/migration | TG-CACHE/TG-ADOPT: supported interfaces remain; exact retired surfaces reject and their exclusive sources disappear. |
| External/environment | TG-EXEC/TG-ADOPT/TG-FINAL: POSIX ownership capability, resource limits, portable skills and separate publication boundaries are enforced. |

Material combined hazards are nested case execution plus wrapper self-tests, failed preflight plus diagnostic broad smoke, package output sharing plus build failure, source deletion plus lost selector discovery, and cache retirement plus historical-evidence preservation. They require the combined groups above even when every local unit test passes.

## Exact source retirement and retained protection

Each row is bounded to Validation's approved source-qualified map, including letter-suffixed requirement children and unnumbered behavior. M1/M3 remove exclusive runtime machinery; M5 removes the remaining current normative sources. Preserve historical source identities in existing change evidence or explicitly stop relying on their old approval; do not manufacture archive copies or redirect stubs.

| Surface | Retained proof or explicit retirement | Final disposition |
| --- | --- | --- |
| `specs/test-layering-and-change-scoped-validation.md` and `.test.md` | R1–26/T1–18 routing, scope, commands, boundary and portable proof → TG-EXEC/COMPOSE/ADOPT. Obsolete v2/mirror populations remain retired. | Remove pair in M5 after consumer reconciliation. |
| `specs/test-and-ci-speed-optimization.md` and `.test.md` | R1–20/T1–19 complete execution, isolation, budget, diagnostics and failure protection → TG-EXEC/CASES. Old uncapped CPU and 60-second default explicitly replaced by approved defaults. | Remove pair in M5. |
| `specs/validation-execution-performance-and-preflight.md` and `.test.md` | R1–22 preflight, boundary gating and evidence/committed-state limits → TG-COMPOSE/FINAL. Profiling rollout ceremony and cache functionality are retired. | Remove pair in M5. |
| `specs/validation-runtime-follow-through.md` and `.test.md` | R1–25/T1–12 missing-route sensitivity, failure/diagnostic identity and external boundaries → TG-COMPOSE/ADOPT. Classify-only rollout and mandatory baselines are retired. | Remove pair in M5; preserve historical measurements. |
| `specs/selector-regression-runtime-reduction.md` and `.test.md` | R1–30/T1–10 complete default suite, real subprocess boundary, fixture isolation and failure sensitivity → TG-CASES/COMPOSE. Percentage targets and old override/profile mandates retire. | Remove pair in M5; preserve useful selector cases. |
| `specs/broad-smoke-safe-parallelism.md` and `.test.md` | R1–42/BSP-T1–12 metadata safety, required leaves, bounds, failure, recovery and network isolation → TG-EXEC/COMPOSE. Historical classification shape, opt-in-only rule and savings thresholds retire. | Remove pair in M5 after M3 catalog proof. |
| `specs/validation-idempotency-and-cache-hit-safety.md`, `.test.md`, and `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md` | Cache identity/hit/evidence/measurement functionality explicitly retires. Actual-run integrity, safe inputs, honest evidence and privacy → TG-CACHE/ADOPT under VAL-SR-11 and RC-SR-15. | Remove three sources in M5; never recreate cache-hit behavior merely to compare performance. |
| `scripts/validation_cache.py`, `scripts/test-validation-cache.py`; cache-specific dispatch/helpers/options; `tests/fixtures/change-metadata/measurement-*/validation-cache-measurement.yaml` | Cache-only obligations retire; actual execution, unsupported-input and continuing v3 negatives remain in existing suites. Confirm the cache-specific contents and any shared helpers before removal. | M1 removes exclusive machinery/fixtures and current catalog route. |
| `scripts/validate-broad-smoke-classification.py`; embedded broad/selected schedulers and shell-label scraping | Missing/stale/contradictory metadata and command/dependency safety move to current catalog/executor proof. | M2/M3 replace, then remove exclusives; retain wrapper entrypoint. |
| June 26/27 classification and June 27 baseline files under `docs/changes/` | Historical observations remain identities; no runtime gate or active inventory dependence. | Retain bytes; remove active reads in M3. |
| `.rigorloop-validation-cache/` and its exclusive ignore line | Disposable-default-only, no symlink following; actual repeated execution and no-write rejection remain protected. | Inspect/remove in M1. Preserve arbitrary external cache directories and historical cache evidence. |
| Mixed `specs/published-skill-first-repository-simplification.md`; mixed `docs/architecture/system/architecture.md` | Only mapped R14/R15/R17–20/R22/R25 allocation and named validation/cache descriptions change. Adjacent lifecycle, generation, release and other obligations remain. | Amend exact sections in M5; remove only exclusive obsolete diagrams whose readers are reconciled. |
| Governance, current model/navigation readers, `docs/follow-ups.md` FU-012; ten mapped skills and shared quality/maintenance resources | One merged owner; selective portable procedure, complete resource parity, separate assessment and preserved historical identities. | Reconcile in M5, preserving unselected specialist/installation/release responsibilities. |

## Validation plan

Commands below are implementation proof requirements, not claims of execution during planning. C4 is the only newly allocated test entrypoint; it tests the Design-selected internal module and is added/registered in M2. Existing public command interfaces stay intact. For commands with a changed subject/basis, record the actual invocation and result; do not rerun unaffected proof solely because another review happened.

| ID | Exact command | Purpose and timing |
| --- | --- | --- |
| C1 | `python scripts/test-select-validation.py` | Complete selector/custom-loader/wrapper regressions at each affected milestone. |
| C2 | `python scripts/test-change-metadata-validator.py` | Measurement retirement, current v3 real subprocess proof and case entrypoint/fixture protection. |
| C3 | `python scripts/test-artifact-lifecycle-validator.py` | Complete retained lifecycle suite, retired cache input and actual-execution proof; preserve independent record/release negatives. |
| C4 | `python scripts/test-validation-execution.py` | New M2 executor/catalog/process regression suite, extended by M3/M4 to actual wrapper/mode/three-suite case integration. Must discover the complete allocated groups by default. |
| C5 | `bash scripts/ci.sh --mode broad-smoke --jobs 1` | Actual complete sequential broad scope after integration; do not bypass required preflight/scope with diagnostic shortcuts. |
| C6 | `bash scripts/ci.sh --mode broad-smoke --jobs 2` | Actual bounded-parallel counterpart, including three-suite case execution at M4/M5. Compare complete required IDs/results on the same basis. |
| C7 | `python scripts/validate-skills.py`; `python scripts/test-skill-validator.py`; `python scripts/test-guide-system-validator.py`; `python scripts/test-boundary-first-reference.py`; `python scripts/test-boundary-first-validation.py` | Source/projection/resource and necessary current-reader invariants. Exact mandatory domain checks remain; no cache or model-text pass substitutes. |
| C8 | `npm --prefix packages/rigorloop test` | Full current CLI/record/installation regression, with its actual package fixture boundaries. Applies to final integrated proof and affected v3/package changes. |
| C9 | `python scripts/test-release-transaction.py` | Existing Release coordinator/candidate/publication-boundary regressions when that integration is touched. No live public write. |
| C10 | `python scripts/test-adapter-distribution.py`; `python scripts/test-npm-package-publication.py` | Generated skill archive and actual npm tarball/resource/invocation proof; use existing tests and temporary output. |
| C11 | `git diff --check`; `python scripts/validate-documentation-prose.py --mode enforce --path docs/plans/2026-09-12-unified-validation-implementation.md` | Whitespace and authored-plan prose; not runtime/semantic approval. |

For model checks, run `python scripts/validate-boundary-first.py --check` with explicit paths for the twelve current registered models from the owning change; record the expanded argv in evidence. C4's actual integration cases must invoke the exact discovered `Class.test_method` selectors through each of the three original scripts, collect their actual runs and compare IDs with full direct execution. This avoids inventing a second public discovery CLI in the plan.

Package/regression checks cover both retained targets and packed CLI integration. If a release candidate is actually being prepared or a release policy trigger applies, use the independently applicable Release-owned commands and current profile; do not invent a tag or run a historical release verifier as a generic pass. No release/publication success is claimed by C5–C10 alone.

## Final review checkpoint

- Kind: lifecycle-closeout, not another implementation milestone.
- Dependencies: directory milestones, all five validation milestones and required corrections closed with their scoped reviews; all implementation remains visible in the final diff.
- Assessment: fresh independent final whole-change Code Review of complete hierarchy/directory/Validation/consumer/package changes and cross-milestone interactions. Earlier reviews inform, but do not replace it.
- Successor: distinct final Verify of the full proposal/Design/Delivery/work/review/evidence chain, complete current proof, authoritative/generated surfaces, preserved history and actual cleanup. Only successful Verify owns the final explanation and initiative closeout.
- Failure: return to the named owner, retain failed evidence, obtain affected independent reassessment and renew the final integrated judgment where needed. Do not manufacture successful Verify or treat a failed command as unrelated without an explicit supported disposition.

## Risks and recovery

Untracked directory/model work is part of the candidate, not disposable baseline debt. Preserve user-owned files, including the root abstraction image. Use exact source/record identities before retirement and recover the smallest coherent source/reader/test slice. No whole-directory deletion of historical changes or all tests is selected.

Legacy full-file prose debt can remain independently blocking when touched or authoritative; source-only deletion does not establish semantic preservation. Record the actual failures and make the narrow owner correction or explicit applicable disposition before final Verify. Do not broaden this plan into unrelated contract cleanup merely to make a full check green.

The three-suite audit may expose additional mutable fixtures or resource constraints. Correct those within M4 where behavior is settled; an undecidable supported behavior, unmet ownership boundary or need for a new public interface returns to Design. Such a gap does not authorize skipping a selected population.

## Dependencies

M1 → M2 → M3 → M4 → M5 → fresh final whole-change Code Review → final Verify. Independent milestone Code Review and required correction closure separate each implementation slice. Publication and PR remain separately authorized consumers. Hosted workflows remain thin; invoke CI maintenance only for a demonstrated affected workflow gap.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-12 | Retire caching before auditing cases. | Avoid spending adoption effort on deliberately retired cache tests and make actual execution the common basis. | Keeping dormant cache machinery contradicts the approved scope. |
| 2026-09-12 | Extract selected execution before unifying broad/main, then enable audited cases. | Establish process/graph behavior before composing artifact dependencies and nested case demand. | Rewriting all orchestration and cases in one slice obscures failures; permanent dual schedulers violate the final contract. |
| 2026-09-12 | Remove exact source authorities after replacement runtime/proof, with current consumer adoption last. | Prevents deletion from hiding missing obligations and keeps product compatibility assessable. | Archive copies, stubs, a second ledger or a deletion quota add no protection. |
| 2026-09-12 | Preserve the directory plan and add uniquely named Validation work. | Keeps earlier assessed intent and identities intact while allocating the remaining initiative. | Overwriting or reopening completed directory milestones would erase their meaning. |

## Readiness

See the owning change record for current activity and exact Delivery Review. This plan neither approves itself nor claims implementation or final readiness.
