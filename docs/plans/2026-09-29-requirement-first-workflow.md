# Requirement-first workflow and SQLite adoption plan

## Purpose / big picture

Deliver one usable requirement-first workflow through coordinated skills, task-oriented CLI and SQLite operational storage. Engineering definitions remain in Git. Current handoffs, actor-owned assessments and selected support live in one project-local operational store. This plan allocates implementation against the design committed at `39be9c81` and the independently assessed interface/capacity corrections recorded with this adoption package; it does not create architectural obligations or claim that a committed design has passed independent assessment.

## Current Handoff Summary

The user authorized continuation through implementation, review, final verification and PR submission. Bootstrap Change: `2026-10-03-requirement-first-sqlite-adoption`, at `docs/changes/2026-10-03-requirement-first-sqlite-adoption/change.json`, created through the currently supported v3 CLI before M1. Preserve an executable copy of package sources and locked dependencies from commit 39be9c81 in private operational storage before replacing dispatch. That executable records bootstrap activity/work and references exact design/delivery review inputs and attributable private reports. No new CLI command is assumed available before implementation. The Constitution's document-based exception covers design/planning assessment, not a waiver of implementation review or PR readiness. The supported workflow-context discovery supplies current project facts; it does not infer adoption or create a Change automatically. Introduce the new store only through its qualified public interface and explicit project association.

## Source artifacts

- Request and requirements: [requirement analysis](../../design/requirements/workflow-refactor.md), [sources](../../design/requirements/sources.md) and the referenced IR/SR/AR records.
- Architecture: [composition](../../design/architecture/README.md#requirement-first-workflow-composition), [Operations](../../design/architecture/modules/MOD-018-engineering-operations/README.md), and [Governance](../../design/architecture/modules/MOD-017-engineering-governance/README.md).
- Contracts: [CLI v2](../../design/architecture/modules/MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/README.md), [Records v4 and SQLite](../../design/architecture/modules/MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/README.md), IF-004 public admission and IF-003 typed storage.
- Verification intent: [Operations coverage](../../design/architecture/modules/MOD-018-engineering-operations/test-design.md), [Governance coverage](../../design/architecture/modules/MOD-017-engineering-governance/test-design.md), and [shared test rules](../design/test-design/rules.md).
- Distribution and replacement: MOD-013/014 owning designs, [Packaging](../design/engineering/packaging.md), [Installation](../design/cli/installation.md), and [Release](../design/engineering/release/release.md) for candidate qualification; release publication is excluded.

## Context and orientation

Canonical skills are under `skills/`; runtime CLI sources are under `packages/rigorloop/dist/`, with Node tests under `packages/rigorloop/test/`. The package's dist directory contains the checked-in executable sources; generated skill adapters are separate and must not be hand-edited. Repository validators, generators, schema sources and adapter templates are under `scripts/`, `schemas/` and `templates/`. Reconcile owning contracts under `docs/design/` at adoption instead of leaving old Proposal-first instructions active beside the replacement.

The initial v4 backend is directly SQLite; there is no intermediate v4 file adapter, dual write or silent legacy fallback. The successor package runs v2/v4 operational commands only. V3 customer contracts remain attributable to the preceding executable, whose sources and dependencies are retained privately for this project during bootstrap. The successor has a bounded explicit import reader, not a v3 dispatcher. Historical source records and judgments retain their meaning. New skills consume supported CLI contracts, never SQL, schema tables or private coordination files. The database binding and packaged migrations belong to MOD-011.

Require the designed Node/SQLite minima and actual runtime qualification. The development machine's current Node 24.14.1 / SQLite 3.51.2 is below that basis; use an isolated qualified runtime for new-store tests and reconcile package/CI runtime declarations before activation. Do not weaken the floor to make local tests pass.

### Bootstrap and handoff bridge

Create the named v3 Change through current change create with stage plan and pending work. Its required proposal slot points to the original requirement-analysis source solely as the legacy container's direction reference; it does not establish Proposal approval, IR equivalence or a new requirement judgment. Register current design/model and plan subjects with CLI-computed identities. Keep original reviewer reports private with exact subject manifests; record their actual design/delivery judgment through supported v3 review operations and reference those originals. No role label or author assessment becomes independent approval.

Before M1, the bootstrap record must make the reviewed packages and allowed next work discoverable. Continue recording progress using the preserved prior executable while the successor is incomplete. M5 qualifies an explicit import of necessary current work, unresolved obligations and source references, retaining the original bootstrap store outside Git before any removal of that selected source. Imported old assessments retain their meaning; record fresh attributable requirement/design/delivery/code/Verify assessments as needed by the new contract, rather than relabeling old purposes. Final Verify and PR readiness consume discoverable current support and exact final subject identity. Private reports alone cannot bypass that reconciliation.

## Non-goals

- Hosted services, activity event sourcing, mandatory per-attempt archives, automatic attachment hashing/deduplication and continuous reassessment of completed Changes.
- Bulk removal of `docs/changes/`, deletion of historical evidence, or automatic rewriting of historical approvals.
- A new Rust architecture-browser engine, customer browser command implementation or a separate browser website redesign. Existing generated documentation remains usable; capabilities advertises only implemented operations.
- Cross-Change subject-history search (SR-078 / FUNC-077). It remains a draft requirement for a separately designed bounded query; this adoption does not implement its selection/continuation protocol or claim its satisfaction. Selected Change context is not a substitute for that capability.
- Merge, release publication, force-push, deletion of remote branches or automatic activation in customer projects.

## Requirements covered

| Existing basis | Allocation and required observation |
| --- | --- |
| SR-006/007 and SR-023/024 | M1/M2/M3: usable handoff, authority limits, explicit issue disposition, selective retention and compact historical completion. |
| SR-027–029 and SR-082 | M3/M4: assessor-owned judgments, current support and one whole-change review gate; changed support never silently renews Verify. |
| SR-040–046; IF-003/004 | M1–M3: closed admission, typed tasks, bounded truthful results, revision conflicts and actual storage outcomes. |
| SR-053–055 and SR-079–081 | M4: selective portable guidance, requirement reuse, separated authoring responsibilities and integrated design review. |
| SR-065, SR-074–077 and SR-083 | M5: selected-scope preservation, backup/restoration/import, compatible packaging and explicit adoption. |
| AR-011–026, AR-029–042 and AR-052–055 where allocated by the owning model | Apply at the respective accountable Module and integrated proof; planning does not substitute task assignments for ARs. |

## Milestones

### M1. Create and resume work through SQLite

- Milestone kind: implementation.
- Engineering purpose: establish the real public-command-to-store boundary with a small usable workflow.
- Requirements: SR-006/007, SR-040–044 and the Records project association/schema/runtime contract.
- Architecture responsibility: MOD-010 admission/output; MOD-011 typed queries, relational schema and transactions.
- Dependencies: integrated design assessment, Delivery Review and qualified Node/SQLite runtime.
- Implementation scope: closed transport/record schemas, project association, packaged schema 1, connection settings, scoped reads, create/context and bounded receipts. The successor explicitly rejects v1/v3 operational envelopes and retired commands; overlapping spellings use its declared v2/v4 semantics. Preserve the prior executable for bootstrap access, not a parallel dispatcher in the successor.
- Files/components likely touched: `packages/rigorloop/dist/bin/rigorloop.js`, new cohesive operational-record modules/migrations under `packages/rigorloop/dist/lib/`, schema sources and their package consumers, package metadata and owning CLI/Records contracts.
- Required verification: TG-M1 — absent/ready/mismatched/unsupported/corrupt stores; valid creation and reopening; early unknown-value rejection; no initialization on read/preview; relational identity and reference enforcement; receipt bounds, individually retrievable accounts, a complete bounded Change-selector discovery index including unselected Reviews, reserved Issue-disposition capacity, and opaque revision precision.
- Evidence expectations: real CLI subprocesses and isolated SQLite files, independently inspected stored state and explicit before/after effects. Parser-only success cannot prove storage behavior.
- Implementation steps: qualify runtime; derive exact schema artifacts; implement typed model validation and adapter; connect create/context; reconcile affected discovery/help and tests.
- Validation commands: `npm test --prefix packages/rigorloop` for the affected native population; focused native Node tests during iteration; `bash scripts/ci.sh --mode explicit --path packages/rigorloop/dist/bin/rigorloop.js` expanded to all changed paths.
- Expected observable result: one actor creates a Change and a second process reads its coherent seven-section handoff without a conversation or directory scan.
- Completion criteria: required valid/invalid paths demonstrated, no missing v4 source/packaged schema, legacy operational input rejected by the successor, and the preserved prior executable remains usable for bootstrap.
- Required evidence: runtime identity, command inputs/outcomes and actual test results in operational evidence.
- Review handoff: retain this slice and proof for whole-change assessment; optional advisory review may examine storage safety.
- Optional commit boundary: `M1: create and resume operational Changes in SQLite`.
- Risks and recovery: reject unsupported/mismatched stores without replacement; remove only owned disposable fixtures; never reset a real store to repair a test or initialize over corruption.

### M2. Record progress, issues and selected support safely

- Milestone kind: implementation.
- Engineering purpose: add useful mutable work without lost updates or erased obligations.
- Requirements: SR-006/023/024, SR-043–045 and the retention/concurrency clauses of Records.
- Architecture responsibility: MOD-010 task normalization; MOD-011 current-account updates, dependencies and named payloads.
- Dependencies: M1 coherent schema and transaction boundary.
- Implementation scope: change update, Work/Basis/Evidence/Decision accounts, blockers, selected attachments, explicit compaction, no-op handling and revision protection.
- Files/components likely touched: operational model/task/adapter/payload modules and Node integration tests; owning input schemas and CLI documentation.
- Required verification: TG-M2 — omitted issues survive, unrelated failures remain visible, duplicate identities reject, stale writers cannot overwrite, no-op preserves revision, at-capacity accounts still accept maximum-sized Issue dispositions, interrupted transactions are coherent, unsafe/changed attachment sources reject, cleanup cannot delete retained/in-flight support.
- Evidence expectations: real competing processes and controlled interruption with independently observed stored effects; simulated successful copying is insufficient.
- Implementation steps: implement candidate construction and complete-candidate constraints; publish selected bytes before metadata commit; add retention and dependency effects; expose precise conflict/busy/unknown outcomes.
- Validation commands: focused native tests plus the same changed-path CI selector as M1, including new test/schema paths.
- Expected observable result: a new actor sees current progress and unresolved obligations after an update or interrupted invocation.
- Completion criteria: failure/retention/concurrency proof complete and no mandatory activity-history mechanism introduced.
- Required evidence: losing/winning writer outcomes, retained byte observations and recovery reads.
- Review handoff: M1/M2 interactions enter the final whole-change subject.
- Optional commit boundary: `M2: preserve current work and selected evidence safely`.
- Risks and recovery: unused payloads may remain after a failed commit; cleanup requires explicit ownership and current-use checks. Lost responses require context reads, not replay or rollback guesses.

### M3. Record assessments and compact completion

- Milestone kind: implementation.
- Engineering purpose: preserve the distinction between supplied judgments, current reliance, final Verify and closeout.
- Requirements: SR-027–029, SR-042–045 and SR-082.
- Architecture responsibility: MOD-006/007 supply semantic rules; MOD-010/011 admit and persist explicit assessment tasks.
- Dependencies: M2 references, support summaries and atomic dependency updates.
- Implementation scope: review prepare/show/record, verification show/record and change complete; current applicability, persisted Verify support state and completion notes/compaction.
- Files/components likely touched: task admission/model rules, context/result projections, schemas and real workflow integration tests.
- Required verification: TG-M3 — advisory feedback cannot approve; missing review blocks governed final success; omitted findings remain; corrections share a gate; evidence/review replacement invalidates dependent reliance; final success is distinct from save and closeout; completed Changes do not track current files.
- Evidence expectations: execute the design's review-recording walkthrough and adverse variants; inspect assessor attribution, scope, selections, persisted support state and compact final account after reopening.
- Implementation steps: implement preparation and assessment variants; enforce dependency rules; add verification and closeout; verify exact retries and post-completion notes without an immutable attempt ledger.
- Validation commands: focused native workflow tests and changed-path CI for all affected subjects.
- Expected observable result: a complete representative Change passes through explicit review/correction/Verify and an authorized completion declaration without any CLI-created engineering judgment.
- Completion criteria: all scoped lifecycle and preservation outcomes demonstrated, including negative completion and stale support.
- Required evidence: actual request/result/state observations and remaining semantic limitations.
- Review handoff: complete assessment interactions enter whole-change review.
- Optional commit boundary: `M3: support review, verification and compact closeout`.
- Risks and recovery: uncertain applicability stays explicit; no state label, timestamp or role claim supplies proof of independence or scope adequacy.

### M4. Prepare the requirement-first skill contracts

- Milestone kind: implementation.
- Engineering purpose: make the available runtime usable through coherent engineering guidance.
- Requirements: SR-053–055 and SR-079–083.
- Architecture responsibility: MOD-008 canonical methods, MOD-012 published procedures and MOD-006/007 coordination/assessment policy.
- Dependencies: M1–M3 executable contracts. Drafting may overlap earlier work; adoption waits for compatible capability availability.
- Implementation scope: replace proposal/proposal-review/combined design with requirement-analysis/requirement-review/system-design/architecture-design; reconcile route, plan, delivery-review, implement, code-review and verify, their transitive references/templates and owning Workflow/Assessment/authoring contracts. Prepare the coherent Constitution/contributor update and package resources; actual project activation waits for M5 qualification.
- Files/components likely touched: `skills/`, `docs/design/skill/`, `CONSTITUTION.md`, `AGENTS.md`, schema/skill inventories, adapter templates and existing skill validators/tests. Installed local skills are not canonical inputs.
- Required verification: TG-M4 — already-covered RR reuses requirements; architecture gaps return to their owner; eligible milestones continue without review gates; optional advice does not approve; one-milestone work has one whole-change review; missing capabilities are not advertised as available.
- Evidence expectations: independent semantic walkthroughs using representative tasks and generated customer skill packages, supplemented by structural/resource validation. String matches alone do not establish correct agent behavior.
- Implementation steps: derive selective references from canonical REM; replace responsibilities and consumers together; remove obsolete internal skill paths after dependency reconciliation; use supported public requests and opaque revisions; retain explicit external compatibility.
- Validation commands: `bash scripts/ci.sh --mode explicit --path skills/route/SKILL.md` expanded to every changed skill, contract, template and validator; generated package checks from Packaging.
- Expected observable result: a fresh agent follows the new workflow and resumes work through the CLI without SQL knowledge or conversational reconstruction.
- Completion criteria: no mixed active Proposal-first/requirement-first contract and no hidden per-milestone approval requirement; each published skill's required resources are present.
- Required evidence: actual package subjects, walkthrough findings/dispositions and validation results.
- Review handoff: instructions, examples, runtime and packaging form one whole-change review subject.
- Optional commit boundary: `M4: adopt requirement-first engineering skills`.
- Risks and recovery: source edits do not activate customer policy. Retain recoverable source history and stop dependent use when installed resources are mixed or missing.

### M5. Qualify maintenance, packaging and project adoption

- Milestone kind: implementation.
- Engineering purpose: make local operational data durable and migrate deliberately without losing historical meaning.
- Requirements: SR-065, SR-074–077 and SR-083; MOD-013/014 package and replacement obligations.
- Architecture responsibility: MOD-011 maintenance; MOD-013 production; MOD-014 installation; MOD-006 explicit adoption.
- Dependencies: complete M1–M4 contract and candidate inventory; maintenance may be implemented earlier but must pass before real-store adoption.
- Implementation scope: store backup/restore/migrate, whole-store expectations, access leases/fences, staged activation/resume, qualified supported import dispositions and retained originals; runtime/package metadata, CLI capabilities/logs contract, workflow descriptor and installation replacement consumers. Reconcile release notes and current public documentation without publishing a release.
- Files/components likely touched: maintenance/migration modules and packaged SQL, `packages/rigorloop/package.json` and lockfile, installer replacement, `scripts/build-adapters.py` and packaging/validation consumers, release notes, repository configuration and guidance.
- Required verification: TG-M5 — coherent WAL snapshot with selected payloads, project/schema mismatch, destination conflicts, interrupted activation/resume, stale store token, missing payloads, dependency-blocked import, truthful old judgments, conflicting installed content and mixed/unknown workflow descriptors.
- Evidence expectations: real packed CLI and generated target archives in isolated roots for both supported adapters; migration of a disposable project copy; independently inspect originals, restored records/payloads and unrelated-file preservation. Archive construction alone is insufficient.
- Implementation steps: implement maintenance/exclusion and failure handling; qualify import adapter and byte preservation; produce candidate; validate installation/adoption; exercise this project's selected operational scope only after disposable rehearsal and retained recovery basis.
- Validation commands: owning Packaging/Release candidate commands, `npm test --prefix packages/rigorloop`, and `bash scripts/ci.sh --mode local` for the complete changed scope, with required tools/runtime explicitly selected.
- Expected observable result: another checkout can restore selected operational context while Git remains sufficient to understand the engineering model; the installed skill/CLI pair agrees on actual capabilities.
- Completion criteria: required maintenance and consumer proof passed, explicit adoption disposition retained, no silent v3 fallback or bulk historical deletion.
- Required evidence: candidate identities, actual archive/install outputs, migration/recovery observations and classified remaining limitations.
- Review handoff: complete delivered scope, including migration, package resources and guidance, enters the mandatory whole-change gate.
- Optional commit boundary: `M5: qualify operational maintenance and coordinated adoption`.
- Risks and recovery: whole-store replacement uses explicit staged recovery and incarnation renewal; old expected revisions must not become valid after restore. Installation does not itself activate workflow authority.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all in-scope implementation and required corrections complete, with actual proof.
- Assessment: one independent whole-change Code Review covering the complete PR diff and cross-milestone interactions. Optional interim advice does not settle this gate or gate each milestone.
- Evidence: actual nonauthor reviewer, exact assessed subjects, judgment, findings and current applicability. Corrections return to the appropriate author and receive proportionate independent reassessment within the same gate.
- Successor: distinct final Verify of the accepted current subject; only then prepare and submit the authorized PR. No merge or release follows automatically.

## Change-level verification

### TG-FINAL-1. Complete customer workflow

Covers M1–M5, SR-006/027–029/040–045/079–083 and IF-003/004. Use the packaged CLI and generated skills in an isolated project: capture a request, reuse/refine requirements, prepare accepted governing bases, record checked milestones, obtain a whole-change assessment, correct an issue, reassess, Verify and complete. A different actor resumes from context between stages. Observe authority limits, open obligations, reported versus mechanically compared basis and selected support. Semantic walkthroughs and real command/storage effects remain distinct evidence.

### TG-FINAL-2. Adoption and recovery across boundaries

Covers M1–M5 and selected SR-065/074–077/083 obligations. Combine competing writers, attachment publication, backup, interrupted replacement, restore and supported import. Verify runtime/package identity, source originals, changed incarnation, current schema and actual installed resources. A save/installation must not invent approval, and a lost response must not trigger semantic replay. Reuse applicable milestone evidence where the composed observation adds no distinct protection.

## Validation plan

Use focused native tests during each implementation step and repository selectors over the exact changed paths at milestone handoff. Record commands actually executed and their results. Before PR submission, run complete required changed-scope validation and qualified package checks, assess generated currency, and verify the final committed subject against the current remote base. Local success is not hosted CI success. Observe hosted CI for the PR head and resolve relevant failures through their owners.

## Risks and recovery

Mixed contracts, unqualified runtime builds, lost operational support, false approval and unsafe installation/replacement are the principal risks. Each milestone allocates the corresponding proof and recovery boundary. Required unknowns remain gaps; neither a partial passing suite nor a successful retry establishes the missing guarantee. Preserve original source/record bytes where promised, but do not create a permanent event archive to support ordinary current-state updates.

## Dependencies

Integrated design assessment and Delivery Review establish the implementation basis. Required independent reviewers must be actual nonauthors; changing role labels is insufficient. The branch's PR diff also includes earlier unpushed REM/design commits, so final review and Verify must cover those changes or explicitly establish their applicable reviewed basis. Public GitHub submission is authorized; the exact base/head and remote state still require verification immediately before push and PR creation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-10-03 | One coordinated plan across three owners | Skills, CLI and storage must compose into one usable outcome. | Independently declared completion with incompatible interfaces. |
| 2026-10-03 | SQLite is the first v4 backend | Matches the committed persistence design and removes an unnecessary migration stage. | Intermediate v4 filesystem adapter and dual write. |
| 2026-10-03 | Deliver usable behavior across boundaries | Each milestone has concrete public observations and safe dependencies. | Completing all storage internals before exercising the CLI. |
| 2026-10-03 | One whole-change review gate before Verify | User-selected workflow; milestones retain their own checks and bounded scope. | Mandatory milestone approval cycles. |
| 2026-10-03 | Qualify maintenance before real adoption | Operational support needs an explicit recovery basis. | Using the new store on irreplaceable data before restore proof. |

## Readiness

This revision supplies delivery intent and proof allocation; it does not assert review approval, completed implementation or PR readiness. Current assessments, progress and blockers belong to operational evidence. Implementation proceeds only on the applicable assessed basis and within the user's continuation authority.
