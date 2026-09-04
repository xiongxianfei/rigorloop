# Execution Plan: Compact Current-State Change Record

## Purpose / big picture

Replace the history-oriented active change pack with a bounded current-state contract that remains fully resumable without Git history, pull-request history, committed operation requests, transport receipts, superseded review rounds, or machine-local logs. Build the compact model behind a withheld writer, prove its schemas and recoverable multi-file transaction boundary, align every canonical and published consumer, then activate one coherent writer set.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-09-03-compact-current-state-change-record/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-09-03-compact-current-state-change-record.md`
- Spec: `specs/compact-current-state-change-record.md`
- Architecture: `docs/architecture/2026-09-03-compact-current-state-change-record.md`
- Applicable ADR: `docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md`
- Approved Design package: `design-review-r13`
- Prior-contract test spec: none; v3 uses this plan's verification allocation.

## Context and orientation

The executable lifecycle package is under `packages/rigorloop/`. Its current pure evaluation, snapshot, operation, CLI, and transaction responsibilities are divided across `dist/lib/lifecycle-*.js` with Node regression coverage under `packages/rigorloop/test/`. The current transaction adapter is centered on `change.yaml`; the compact contract expands that boundary to all applicable current surfaces and requires every reader to withhold state during an unresolved transaction.

Canonical workflow and validation behavior spans `CONSTITUTION.md`, `AGENTS.md`, `specs/rigorloop-workflow.md`, `docs/architecture/system/`, `schemas/`, `scripts/`, `templates/`, and the stage skills under `skills/`. `skills/` is the only authored skill source. Supported adapter packages and package metadata must be regenerated or checked through repository tooling and must never be hand edited.

The current history-oriented lifecycle remains authoritative for this implementing change and for existing records. Compact writing stays disabled until the final activation milestone proves that the CLI, schemas, validators, skills, documentation, fixtures, and supported adapters agree on `compact-current-state-v1`. Historical completed changes remain readable, and no milestone rewrites or compacts them.

## Non-goals

- Preserve or reconstruct every superseded command, route, receipt, review wording, validation event, or routine resolved finding.
- Use Git, a pull-request host, CI output, network access, or machine-local logs as a correctness, recovery, freshness, or resumption dependency.
- Add authentication, a hosted service, database, daemon, distributed transaction protocol, dependency without approved justification, or tamper-proof audit ledger.
- Fold proposals, specifications, architecture, ADRs, or plans into a monolithic change record.
- Bulk migrate completed historical changes or infer compact authority from file names.
- Publish a release, open a pull request, push, merge, or mutate another external system.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| SR-01–SR-06, SR-37–SR-42; BND-INPUT-001, BND-STATE-001, BND-STATE-002, BND-AUTH-002, BND-COMPOSE-001 | M1 schemas, normalization, whole-set identity, current-set validation, and read-only projection model |
| SR-22–SR-33, SR-43–SR-45; BND-INPUT-002, BND-AUTH-001, BND-AUTH-002, BND-COMPOSE-002, BND-TEMPORAL-001, BND-TEMPORAL-002, BND-RECOVERY-001, BND-ENV-002; INT-001–INT-004 | M2 pure evaluator, lock, persistence, recovery, retry, containment, and durability boundary |
| SR-07–SR-26, SR-31–SR-34, SR-46–SR-48; BND-STATE-002, BND-STATE-003, BND-AUTH-001, BND-AUTH-002, BND-COMPOSE-001, BND-COMPOSE-002, BND-TEMPORAL-002, BND-RECOVERY-002, BND-COMPAT-003, BND-ENV-001; INT-001–INT-003, INT-006, INT-007 | M3 semantic operations, stable review judgment, occurrence-stable findings, material acceptance, derived progression, bounded CLI views, and the closed bootstrap operation |
| SR-02–SR-05, SR-08–SR-12, SR-19–SR-26, SR-32–SR-36, SR-47–SR-48; BND-STATE-001, BND-STATE-003, BND-COMPAT-001, BND-COMPAT-002, BND-COMPAT-003, BND-ENV-001; INT-003, INT-005–INT-007 | M4 canonical governance, workflow, architecture, skills, validators, templates, fixtures, and contributor guidance |
| SR-01–SR-48; all boundary IDs except BND-STATE-004; INT-001–INT-007 | M5 coherent activation, exact implementing-change bootstrap, supported-adapter parity, legacy-write denial and rollback proof, bounded-context proof, and complete-change validation |
| SR-23, SR-25–SR-27, SR-31, SR-46–SR-49; BND-INPUT-001, BND-STATE-003, BND-STATE-004, BND-AUTH-001, BND-AUTH-002, BND-TEMPORAL-001, BND-TEMPORAL-002, BND-RECOVERY-001, BND-RECOVERY-002, BND-COMPAT-003, BND-ENV-001; INT-006–INT-008 | M6 append-only planned-work extension, corrected review/finding semantics, bootstrap completion, and final correction proof |

## Milestones

### M1. Define and normalize the compact authoritative set

- Milestone kind: implementation
- Engineering purpose: Establish one strict, independently testable data model and whole-set identity before any mutation path can write compact records.
- Requirements: SR-01–SR-06, SR-37–SR-42; BND-INPUT-001, BND-STATE-001, BND-STATE-002, BND-AUTH-002, BND-COMPOSE-001.
- Architecture responsibility: authoritative current-set schemas, safe parsing, closed vocabularies, normalized snapshot, lifecycle revision manifest, and read-only projection model.
- Dependencies:
  - approved Design package `design-review-r4`;
  - existing YAML dependency and lifecycle parsing conventions;
  - compact writer remains disabled.
- Implementation scope: Add exact compact schema definitions and package-side parsers/normalizers for the coordinator, stable review, decision, evidence, Verify, operation, result, and recovery records. Implement exact byte identities, the SR-40 lifecycle revision manifest, complete-set reference validation, size limits, optional-surface absence semantics, and read-only normalized projections. Preserve existing v3 parsing and writing behavior unchanged.
- Files/components likely touched:
  - `schemas/` compact schema definitions and activation metadata;
  - `packages/rigorloop/dist/lib/` compact contract, parsing, identity, snapshot, and projection modules;
  - `packages/rigorloop/test/` schema, vocabulary, identity, projection, and compatibility regressions;
  - compact fixtures under the repository's existing fixture conventions.
- Required verification:
  - TG-01 — Every valid authoritative surface and reusable nested record parses to one normalized model, while missing, duplicate, extra, unknown, malformed, unsafe, or oversized data fails in the specified order without fallback.
  - TG-02 — Independent test vectors produce the exact SR-40 lifecycle revision; every relevant authoritative byte changes it, while excluded requests, logs, and transaction-private files do not.
  - TG-03 — Equal current authoritative sets yield equal bounded projections regardless of unrelated procedural files, and absent optional surfaces project as empty collections without placeholder creation.
  - TG-04 — Existing historical and stage-owned v3 fixtures retain their current read and write behavior while the compact writer is disabled.
- Evidence expectations: Table-driven valid/invalid fixtures for every closed schema and vocabulary; `unknown_value` regressions for new constants; byte-level identity vectors; bounded-projection comparisons with synthetic procedural history; and unchanged legacy package tests.
- Implementation steps:
  - Add failing parser, schema, closed-vocabulary, size, and lifecycle-revision vectors first.
  - Implement compact parsing and normalization without mutation or activation authority.
  - Implement current-set reference and identity validation plus bounded read-only projection objects.
  - Prove existing v3 behavior is unaffected and compact mutation remains unavailable.
- Validation commands:
  - `node --test packages/rigorloop/test/compact-contract.test.js packages/rigorloop/test/compact-projection.test.js`
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/compact-current-state-change-record.md`
- Expected observable result: The package can validate and project a complete compact candidate deterministically, but no public command can create or mutate a compact change.
- Completion criteria: TG-01 through TG-04 pass; all new closed vocabularies reject unknown values explicitly; identity vectors are byte-unambiguous; existing lifecycle tests pass; writer activation remains withheld.
- Required evidence: `docs/changes/2026-09-03-compact-current-state-change-record/evidence/m1-compact-model.md`
- Review handoff: Code Review of exact schemas, parsing order, whole-set identity, optional-surface behavior, bounded projection, and unchanged legacy behavior.
- Optional commit boundary: `M1: define compact current-state model`
- Risks:
  - YAML or Markdown-front-matter normalization could accidentally replace the exact-byte identity contract.
  - A permissive parser could let unknown fields or vocabularies bypass consistency checks.
- Rollback/recovery:
  - Revert the M1 model, fixtures, and tests together; because writing remains disabled, no compact record requires migration.

### M2. Implement the recoverable multi-file transaction boundary

- Milestone kind: implementation
- Engineering purpose: Make coordinated current-record replacement safe under stale writers, retries, permission failures, disk failures, and interruption before exposing semantic compact operations.
- Requirements: SR-22–SR-33, SR-43–SR-45; BND-INPUT-002, BND-AUTH-001, BND-AUTH-002, BND-COMPOSE-002, BND-TEMPORAL-001, BND-TEMPORAL-002, BND-RECOVERY-001, BND-ENV-002; INT-001, INT-002, INT-003, INT-004.
- Architecture responsibility: pure evaluator boundary, exact expected-file binding, exclusive writer lock, private same-filesystem staging and recovery, deterministic replacement, durability barriers, identical retry, safe result model, and fail-closed readers.
- Dependencies:
  - accepted M1 implementation and Code Review;
  - exact compact snapshot and identity functions;
  - filesystem durability capabilities checked before replacement;
  - compact writer remains disabled outside tests.
- Implementation scope: Add the pure candidate evaluator contract and recoverable adapter under `.rigorloop/transactions/<change-id>/`. Bind every read and affected path, enforce containment and private permissions, stage complete prior and candidate bytes, inject failures at each boundary, restore or accept only exact states, block all governed consumers during live or unresolved transactions, and return one human/JSON-compatible result model. Do not yet expose the full public semantic operation set or activate compact writers.
- Files/components likely touched:
  - `packages/rigorloop/dist/lib/` evaluator, transaction, recovery, filesystem, error, and renderer modules;
  - `packages/rigorloop/dist/bin/rigorloop.js` internal/test-only wiring without public compact activation;
  - `packages/rigorloop/test/` transaction, concurrency, retry, path, permission, fault-injection, recovery, and result-rendering tests;
  - ignore and packaging rules for `.rigorloop/transactions/`.
- Required verification:
  - TG-05 — Of concurrent or stale requests based on one revision, at most one succeeds and every loser preserves all authoritative bytes.
  - TG-06 — Fault injection before preparation, after every replacement, after persisted read-back, and during cleanup yields only exact prior restoration, exact candidate acceptance, or `recovery-required`; no reader consumes a partial set.
  - TG-07 — Traversal, symlink escape, permission weakness, unsupported durability, oversized transaction content, tampered recovery metadata, and missing recovery bytes reject safely without echoing private content.
  - TG-08 — An exact uncertain-success retry returns `already-applied` only after complete-set validation; conflicting replay rejects without a second mutation.
- Evidence expectations: Deterministic race harness; byte snapshots before and after every injected fault; mode and containment assertions; explicit fsync/directory-sync test seams; human/JSON status parity; and no-network/no-Git recovery runs.
- Implementation steps:
  - Add failure-injection and competing-writer tests before expanding the adapter.
  - Implement the pure candidate transaction envelope and exact expected-file validation.
  - Implement lock acquisition, private recovery preparation, deterministic replacement, read-back, durability barriers, cleanup, and restoration.
  - Gate every compact reader and writer on transaction state and implement explicit recovery status/action handling.
  - Prove identical retry and unchanged-file byte preservation.
- Validation commands:
  - `node --test packages/rigorloop/test/compact-transaction.test.js packages/rigorloop/test/compact-recovery.test.js packages/rigorloop/test/compact-concurrency.test.js`
  - `npm test --prefix packages/rigorloop`
  - `python scripts/validate-npm-package.py`
- Expected observable result: Test-only compact mutations preserve one complete authoritative set across concurrency and every injected interruption, and all consumers fail closed during unresolved recovery.
- Completion criteria: TG-05 through TG-08 pass on supported platforms; unsupported durability rejects before replacement; no recovery path uses Git, PR data, network access, or local logs; public compact writing remains withheld.
- Required evidence: `docs/changes/2026-09-03-compact-current-state-change-record/evidence/m2-transaction-recovery.md`
- Review handoff: Code Review of transaction isolation, prior/candidate durability, replacement ordering, restoration, retry semantics, error redaction, and reader blocking.
- Optional commit boundary: `M2: add recoverable compact transactions`
- Risks:
  - Platform-specific flush behavior could permit success before durable cleanup.
  - Fault tests could exercise injected exceptions without proving persisted byte states.
- Rollback/recovery:
  - Revert the complete M2 adapter and tests while retaining the read-only M1 model; no public compact writer has produced records.

### M3. Add compact semantic operations and bounded CLI capabilities

- Milestone kind: implementation
- Engineering purpose: Expose the minimum public CLI boundary and enforce lifecycle-derived operation eligibility, non-loss, freshness, responsibility consistency, and final-readiness invariants through one evaluator and transaction path.
- Requirements: SR-07–SR-26, SR-31–SR-34, SR-46–SR-48; BND-STATE-002, BND-STATE-003, BND-AUTH-001, BND-AUTH-002, BND-COMPOSE-001, BND-COMPOSE-002, BND-TEMPORAL-002, BND-RECOVERY-002, BND-COMPAT-003, BND-ENV-001; INT-001, INT-002, INT-003, INT-006, INT-007.
- Architecture responsibility: stable review replacement, clear/findings-open/blocked review judgment, explicit material-decision acceptance, mechanically derived progression, occurrence-stable finding disposition, dependency-scoped invalidation, evidence freshness, Verify coupling, typed pending-milestone selection, stage and milestone transitions, explicit correction route/return/review settlement, the closed implementing-change bootstrap, named bounded views, transient request transports, and legacy read-only compatibility.
- Dependencies:
  - accepted M2 implementation and Code Review;
  - pure evaluator and recoverable adapter;
  - compact writer activation remains withheld by the compatibility gate.
- Implementation scope: Implement all SR-23 operations and their lifecycle-state/target eligibility matrix without accepting caller identity, authority claims, or derived correction fields; validate responsibility metadata as provenance rather than permission; record review judgment separately from material owner acceptance and derive progression from current facts; preserve each finding occurrence's settlement independently of aggregate container identity, invalidate only declared dependents, and assign a new finding ID to a genuine recurrence; preserve an active correction through return and required clear review settlement; let `advance-milestone` select one exact typed pending milestone from `null` to `planned`, remove it from remaining work, and derive active work atomically without parsing plan prose; implement `bootstrap-closeout` as an exact-change, exact-current-set, one-use operation over the same evaluator and recoverable transaction path; support arguments, stdin, and temporary request files without retaining requests; add summary, review, finding, decision, evidence, remaining-work, verification, and named skill-context views; update `workflow-context` to consume the bounded model for compact candidates; reject compact migration of every other legacy change; and retain existing historical readers. Convenience commands, if retained, must delegate to the same evaluator. Do not activate new compact changes until canonical consumers are aligned.
- Files/components likely touched:
  - `packages/rigorloop/dist/lib/lifecycle-contract.js`, `lifecycle-read.js`, `lifecycle-operations.js`, `lifecycle-transaction.js`, `lifecycle-cli.js`, and focused compact modules;
  - `packages/rigorloop/dist/bin/rigorloop.js` command and input handling;
  - `packages/rigorloop/test/` operation, projection, correction lifecycle, review, evidence, Verify, transport, compatibility, and CLI-result tests;
  - package README and command help where public behavior is documented.
- Required verification:
  - TG-09 — Review replacement preserves every open finding or valid final disposition, requires explicit owner acceptance for every material consequence, and permits non-material disposal only when no current reference remains. Editing an unrelated section or aggregate container cannot reopen a settled occurrence; a reproduced violation receives a new finding ID linked to the applicable material decision.
  - TG-10 — Artifact, review, decision, and remaining-work mutations invalidate exactly dependent evidence and successful Verify readiness in the same transaction; partial multi-subject evidence follows EC4.
  - TG-11 — All three public capabilities and every convenience entry path produce equivalent normalized semantics and bounded human/JSON results; request transport never affects or enlarges the governed set, and `route-correction` rejects caller-supplied kind, status, or other derived fields.
  - TG-12 — Named projections answer their exact questions from current files only, omit unrelated bodies, and behave identically without Git metadata, PR access, network access, local logs, or disposable procedural files. A globally blocked fixture keeps progression blocked while an explicitly requested safe correction is permitted, and omitting the requested operation yields null eligibility fields.
  - TG-13 — Correction route creates `authoring`, return preserves the same correction as `review-required`, and exact `clear` judgment with no open blocker and every required material acceptance lets the evaluator clear it; findings-open, blocked, or inconsistent settlement retains, revises, blocks, or rejects without loss. With no active work, `advance-milestone` selects one exact pending milestone, rejects missing, blocked, wrong-kind, wrong-owner, ambiguous, or stale selection unchanged, and reviewed closure exposes another explicit selection or the downstream gate. `bootstrap-closeout` accepts only this implementing change's exact current consequential set, independently completed exact-subject clear final review, passing Verify result, and coherent activation manifest; every stale, blocked, other-change, replay, or partial-activation case rejects unchanged without Git or PR identity.
- Evidence expectations: Operation-eligibility matrix tests across current stage, active work, target, and requested operation, including every unknown value; explicit rejection of caller identity, authority, and derived correction fields; responsibility-metadata consistency; route/return/review/settlement state-machine proof; first and subsequent milestone selection with valid, invalid, ambiguous, closure, and stale-retry cases; finding and decision non-loss mutations; dependency graph invalidation; Verify success/failure/interruption cases; projection byte/count bounds; transport equivalence; and legacy write-denial fixtures.
- Implementation steps:
  - Add failing semantic-operation and lifecycle-eligibility-matrix tests first, including progression-versus-operation outcomes, first and subsequent milestone selection, invalid selection preserving all authoritative bytes, deterministic stale retry, and rejection of caller identity, authority, and derived correction fields.
  - Implement stable review, finding, decision, evidence, Verify, routing, milestone, artifact, and stage operations in the pure evaluator.
  - Route every public transport and convenience command through the recoverable adapter.
  - Add named bounded projections, optional exact operation selection, and compact skill-context selection.
  - Add explicit legacy migration rejection and historical write denial, with the sole closed SR-48 bootstrap exception for this implementing change.
- Validation commands:
  - `node --test packages/rigorloop/test/compact-operations.test.js packages/rigorloop/test/compact-cli.test.js packages/rigorloop/test/compact-migration.test.js`
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-lifecycle-cli-conformance.py`
  - `python scripts/test-cli-result-measurement.py`
  - `python scripts/validate-governed-lifecycle-cli.py`
- Expected observable result: The CLI implements projection, semantic application, and recovery for compact candidates with one state model, while activation policy still rejects creation by an incoherent writer set.
- Completion criteria: TG-09 through TG-13 pass; no supported operation needs a committed request, receipt, review log, resolution ledger, authoring evidence, Git/PR history, network, or local diagnostics; compact creation remains gated.
- Required evidence: `docs/changes/2026-09-03-compact-current-state-change-record/evidence/m3-cli-operations.md`
- Review handoff: Code Review of lifecycle-derived eligibility, typed pending-milestone selection and retry, correction lifetime and settlement, responsibility provenance, non-loss, evidence freshness, Verify coupling, transport equivalence, bounded projections, legacy write denial, and compatibility.
- Optional commit boundary: `M3: expose compact CLI boundary`
- Risks:
  - Convenience commands could retain old side effects or become competing mutation paths.
  - Bounded views could omit a current fact needed for a stage decision or include unrelated full records.
- Rollback/recovery:
  - Revert M3 public commands and operations while retaining the reviewed model and adapter; the activation gate continues to deny compact creation.

### M4. Replace the canonical history-oriented workflow contract

- Milestone kind: implementation
- Engineering purpose: Align every authoritative and contributor-facing semantic consumer before compact writing can be activated.
- Requirements: SR-02–SR-05, SR-08–SR-12, SR-19–SR-26, SR-32–SR-36, SR-47–SR-48; BND-STATE-001, BND-STATE-003, BND-COMPOSE-001, BND-COMPOSE-002, BND-COMPAT-001, BND-COMPAT-002, BND-COMPAT-003, BND-ENV-001; INT-003, INT-005, INT-006, INT-007.
- Architecture responsibility: coherent workflow ownership, stable review and evidence semantics, bounded skill consumption, validator parity, prospective adoption, and compatibility documentation.
- Dependencies:
  - accepted M3 implementation and Code Review;
  - exact executable compact behavior available but writer activation withheld;
  - canonical source ownership under `skills/`, `specs/`, `docs/`, `schemas/`, `scripts/`, and `templates/`.
- Implementation scope: Amend current governance, the canonical `specs/rigorloop-workflow.md`, canonical system architecture, this change's approved architecture/ADR integration points, prior ADR supersession links, root guidance, affected stage skills and references, templates, change schemas, Python validators, workflow automation/state logic, query/context scripts, examples, project map, and contributor documentation to the compact contract. Remove current requirements for round-suffixed reviews, review logs, resolution ledgers, committed requests, route receipts, routine authoring evidence, and history reconstruction only for compact changes. Treat focused specifications owned by prior changes as read-only compatibility inputs unless their own governed owner separately authorizes revision. Preserve historical readers and current implementation-change evidence.
- Files/components likely touched:
  - `CONSTITUTION.md`, `AGENTS.md`, `README.md`, and the canonical `specs/rigorloop-workflow.md`; prior lifecycle-managed focused specifications remain read-only;
  - `docs/architecture/system/`, `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md`, `docs/project-map.md`, and contributor guides;
  - `skills/route`, all lifecycle authoring/review/implementation/verification skills that consume or create change-local records, and shared assets/references;
  - `schemas/change.schema.json`, activation schemas, compact schemas, `scripts/change_metadata_semantics.py`, review/lifecycle/workflow validators, selectors, query/context logic, and fixtures;
  - `templates/` current review, evidence, Verify, and shared-policy assets.
- Required verification:
  - TG-14 — Every current canonical instruction names the compact current owners and bounded projection route, while historical-only text is explicitly scoped and cannot grant current writer authority.
  - TG-15 — Skills read only projected current facts and required paths, preserve their semantic responsibility without claiming CLI-granted permission, create no routine retired artifacts for compact changes, record independent review judgment separately from explicit material owner acceptance, and still preserve open findings, current evidence, and successful Verify through the CLI.
  - TG-16 — Python and Node validators agree on all compact valid/invalid fixtures, closed vocabularies, identities, reference invariants, optional absence, compatibility states, and activation blockers.
  - TG-17 — Existing historical fixtures remain readable, existing non-compact changes are not rewritten, and current v3 implementation evidence for this change remains valid until closeout.
- Evidence expectations: Canonical terminology scan; focused skill mutation tests; shared cross-runtime fixtures; current/historical validation matrices; workflow-context projection checks; no-unscoped-history-authority scan; and generated-source cleanliness checks.
- Implementation steps:
  - Add failing canonical-contract and cross-validator fixture tests.
  - Amend governance, workflow, architecture, ADR, and root contributor guidance as one coherent semantic package.
  - Update canonical stage skills, references, and templates to consume projections and submit transient semantic operations.
  - Update schemas, Python validators, workflow state/automation, selectors, query tooling, fixtures, and examples.
  - Prove historical compatibility and eliminate contradictory current instructions without editing generated skill bodies.
- Validation commands:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-workflow-automation-state.py`
  - `python scripts/test-workflow-automation.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-guide-system.py`
  - `python scripts/validate-documentation-prose.py --mode audit`
- Expected observable result: Canonical and contributor-facing sources describe one compact current-state contract and retain explicitly bounded historical compatibility, but new compact writing is still withheld pending published-package parity.
- Completion criteria: TG-14 through TG-17 pass; all affected current instructions and validators agree; no generated source is hand edited; historical fixtures pass; activation remains withheld.
- Required evidence: `docs/changes/2026-09-03-compact-current-state-change-record/evidence/m4-canonical-contract.md`
- Review handoff: Code Review of governance precedence, semantic ownership, skill boundedness, validator parity, historical scoping, and removal of contradictory current requirements.
- Optional commit boundary: `M4: align compact workflow contract`
- Risks:
  - Broad text replacement could accidentally alter historical evidence or unrelated workflow behavior.
  - Python and Node validators could accept different schema subsets during cutover.
- Rollback/recovery:
  - Revert the whole M4 semantic package while the compact writer remains disabled; retain historical behavior until a corrected package is reviewed.

### M5. Activate one coherent compact writer set

- Milestone kind: implementation
- Engineering purpose: Prove canonical-to-package parity and integrated behavior before enabling prospective compact changes while keeping every legacy change on its registered contract.
- Requirements: SR-01–SR-48; all boundary IDs except BND-STATE-004; INT-001–INT-007.
- Architecture responsibility: activation discriminator, supported-adapter parity, rollout and rollback, complete workflow integration, bounded-context scaling, historical readership, and no-external-dependency proof.
- Dependencies:
  - accepted M4 implementation and Code Review;
  - every prior milestone's evidence remains current;
  - repository-owned adapter generation, package validation, and broad-smoke tooling.
- Implementation scope: Refresh deterministic package and adapter metadata from canonical source; update the activation manifest/discriminator only after all required component versions and fixture identities agree; prove a new compact change, repeated review/correction, occurrence-stable finding settlement, dependency-scoped invalidation, final Verify, ordinary legacy write and migration denial, the exact one-use implementing-change bootstrap, rollback-to-read-only, and recovery flow end to end; measure equal-current-state projections with unequal synthetic histories. Do not publish, open a PR, push, merge, or release.
- Files/components likely touched:
  - compact lifecycle and activation metadata under `specs/`, `schemas/`, and `packages/rigorloop/dist/metadata/`;
  - package checksum fixtures and release-candidate metadata only when deterministically affected;
  - adapter manifest/support metadata and adapter-distribution tests;
  - integrated compact and token/context fixtures and repository validation selection.
- Required verification:
  - TG-18 — A coherent version matrix is the only state that permits new compact writing; mixed, unknown, disabled, and rolled-back states retain readers but reject writers. The exact implementing change can cross that boundary only through the one-use atomic bootstrap and never becomes a compact-shaped migrated record.
  - TG-19 — A full prospective change selects its first and each subsequent typed pending milestone, proceeds through current review judgment, explicit correction return, required clear rereview, material owner acceptance when triggered, derived progression, evidence, milestone closure, final review, and Verify using only the compact set and transient requests, with no plan-prose, Git/PR/network/log dependency.
  - TG-20 — Completed and in-flight legacy changes remain byte-identical, readable under their registered contract, and denied compact writes or migration before and after activation and rollback.
  - TG-21 — Every supported adapter candidate contains the same compact contract, resources, commands, and schemas as canonical source, and mixed or stale candidates fail validation.
  - TG-22 — Equal current-state fixtures produce equal-scope bounded projections despite materially different counts of synthetic prior requests, routes, reviews, corrections, and evidence events.
  - TG-23 — Full fault, security, compatibility, package, documentation, adapter, and repository smoke validation passes on the exact activated candidate.
- Evidence expectations: Activation-matrix fixtures; end-to-end fresh-machine workflow; legacy write/migration-denial and rollback runs; byte identity snapshots for historical and in-flight legacy changes; adapter archive inventories and hashes; projection size/count comparison; and complete local validation output summarized in stage-owned evidence.
- Implementation steps:
  - Generate and validate supported package and adapter candidates from canonical sources.
  - Refresh only deterministic current-candidate metadata and exact fixtures proven stale.
  - Exercise the complete compact lifecycle, legacy write and migration denial, rollback, and recovery scenarios before changing activation authority.
  - Enable the compact writer discriminator and rerun the complete matrix on the exact activated bytes.
  - Run repository broad smoke and inspect the final diff for historical rewrites, generated-source edits, unsafe transaction files, or external dependencies.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-lifecycle-cli-conformance.py`
  - `python scripts/test-governed-lifecycle-cli-validator.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --check`
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-npm-package.py`
  - `bash scripts/ci.sh --mode broad-smoke`
- Expected observable result: New governed changes can use `compact-current-state-v1` through every supported adapter, while legacy records remain readable and all correctness, recovery, and resumption behavior works without Git, PR access, network access, or local logs.
- Completion criteria: TG-18 through TG-23 pass; the activation matrix is coherent; complete-change proof covers every SR, boundary, and interaction; no external mutation occurs; final holistic Code Review may begin.
- Required evidence: `docs/changes/2026-09-03-compact-current-state-change-record/evidence/m5-activation-parity.md`
- Review handoff: Code Review of coherent activation, integrated lifecycle semantics, legacy write denial and rollback, adapter parity, bounded context, historical preservation, and final validation evidence.
- Optional commit boundary: `M5: activate compact current-state records`
- Risks:
  - Activation metadata could enable a writer before one adapter or validator is current.
  - Generated archive identities could drift incompletely across nested metadata.
- Rollback/recovery:
  - Disable new compact writers while retaining released compact readers and records; never reconstruct discarded procedure or rewrite completed compact changes.

### M6. Complete corrected lifecycle semantics and final-review readiness

- Milestone kind: implementation
- Engineering purpose: Deliver the post-M5 Design corrections as an explicit reviewable slice while proving that reviewed corrective work can be appended without rewriting completed milestone history.
- Requirements: SR-23, SR-25–SR-27, SR-31, SR-46–SR-49; BND-INPUT-001, BND-STATE-003, BND-STATE-004, BND-AUTH-001, BND-AUTH-002, BND-TEMPORAL-001, BND-TEMPORAL-002, BND-RECOVERY-001, BND-RECOVERY-002, BND-COMPAT-003, BND-ENV-001; INT-006, INT-007, INT-008.
- Architecture responsibility: append-only planned-work extension, occurrence-stable finding settlement, review-judgment and owner-acceptance separation, derived progression, exact implementing-change bootstrap, and final holistic-review readiness.
- Dependencies:
  - M1 through M5 remain closed with their identities, order, contracts, evidence allocation, and lifecycle states unchanged;
  - Design Review is clear for the exact Architecture, ADR, and Specification revision that defines SR-49;
  - Delivery Review is clear for this exact Plan revision;
  - route appends M6 through the reviewed suffix operation before milestone selection;
  - compact writer activation remains withheld until M6 Code Review and final Verify succeed.
- Implementation scope: Add `append-planned-work` to the legacy implementing-change coordinator and compact evaluator using exact Plan and Delivery Review identities, immutable-prefix comparison, atomic suffix insertion, stale-write rejection, idempotent replay, and no automatic selection. Finish the R13 evaluator, reader, stable-review, finding, material-acceptance, derived-progression, canonical workflow, validator, fixture, adapter, and bootstrap corrections. Prove M6 follows ordinary `advance-milestone`, implementation, milestone Code Review, final holistic Code Review, Verify, and bootstrap closeout. Do not reopen M1 through M5, infer work from unreviewed prose, or use Git, PR, network, or logs as authority.
- Files/components likely touched:
  - legacy and compact lifecycle evaluators, readers, operations, projections, and CLI wiring under `packages/rigorloop/`;
  - lifecycle and compact schemas, validators, fixtures, and focused tests;
  - canonical workflow, skills, architecture, contributor guidance, activation metadata, and supported-adapter generation inputs;
  - M6 stage-owned evidence and stable Code Review records.
- Required verification:
  - TG-24 — An exact clear Delivery Review and exact revised Plan append M6 once while M1 through M5 remain byte-for-byte equivalent in registered identity, order, contract, evidence allocation, and state; insertion, mutation, reopening, empty suffix, stale identity, concurrency, and conflicting replay reject unchanged.
  - TG-25 — M6 is not auto-selected. Normal milestone selection, implementation, exact milestone Code Review, closure, final holistic Code Review, Verify, and bootstrap readiness each remain separately required and bounded by current state.
  - TG-26 — Review judgment, material owner acceptance, and progression remain distinct; container changes do not resurrect settled findings; genuine recurrence uses a new finding linked to the applicable decision; declared dependencies alone invalidate current proof.
  - TG-27 — The implementing-change bootstrap binds the complete planned-work set and rejects while M6 is pending, active, unreviewed, or stale; exact success remains one-use, atomic, and independent of Git, PR, network, and local logs.
  - TG-28 — Canonical sources, validators, package behavior, fixtures, activation metadata, and supported adapters agree on SR-49 and the corrected R13 semantics before writer activation.
- Evidence expectations: Immutable-prefix and suffix fixtures; before/after coordinator snapshots; stale, concurrent, exact-retry, and conflicting-replay results; M6 milestone and final-review records; per-occurrence finding regressions; owner-acceptance/progression matrix; bootstrap unfinished-work denials; canonical/package/adapter parity; focused and broad validation summaries.
- Implementation steps:
  - Add failing suffix-extension, immutable-prefix, stale/concurrent/replay, and unfinished-bootstrap tests first.
  - Implement append-only extension through the same pure evaluator and recoverable transaction boundary; keep selection explicit.
  - Complete the corrected review, finding, material-acceptance, progression, canonical, validation, and adapter semantics.
  - Record M6 implementation evidence, run its milestone Code Review, then perform final holistic Code Review over the complete candidate.
  - Run change-level Verify on the exact reviewed candidate; only then invoke the one-use bootstrap closeout and activation transaction.
- Validation commands:
  - `node --test packages/rigorloop/test/lifecycle-evidence.test.js packages/rigorloop/test/lifecycle-stage-advance.test.js packages/rigorloop/test/compact-operations.test.js packages/rigorloop/test/compact-activation.test.js`
  - `npm test --prefix packages/rigorloop`
  - `python scripts/validate-boundary-first.py --check --path specs/compact-current-state-change-record.md`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-governed-lifecycle-cli-validator.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --check`
  - `bash scripts/ci.sh --mode broad-smoke`
- Expected observable result: The reviewed M6 suffix is represented as ordinary current work, all corrected semantics are implemented and independently reviewed, and bootstrap closeout cannot activate until that work and final verification are complete.
- Completion criteria: TG-24 through TG-28 pass; M1 through M5 remain unchanged; M6 milestone Code Review and final holistic Code Review are clear; final Verify passes on the exact candidate; bootstrap closeout succeeds once or leaves prior authority unchanged.
- Required evidence: `docs/changes/2026-09-03-compact-current-state-change-record/evidence/m6-corrected-lifecycle-closeout.md`
- Review handoff: First Code Review M6 against its exact implementation and evidence, then final holistic Code Review of the complete change before Verify.
- Optional commit boundary: `M6: complete corrected lifecycle closeout`
- Risks:
  - A permissive comparison could disguise a rewrite of completed work as an append.
  - Coupling extension to selection could skip the independently visible pending state.
  - Activation could occur against evidence that predates M6.
- Rollback/recovery:
  - Before M6 selection, reject or reverse only an unconsumed exact suffix through the transaction recovery path; never modify M1 through M5.
  - After M6 begins, correct it through normal review and resolution; disable compact activation rather than rewriting completed work.

## Change-level verification

### TG-FINAL-01. Complete current-state resumability and non-loss

- Covers: SR-01–SR-26, SR-32, SR-37–SR-42, SR-46–SR-49; M1, M3, M4, M5, M6; BND-INPUT-001, BND-STATE-001, BND-STATE-002, BND-STATE-003, BND-STATE-004, BND-AUTH-001, BND-AUTH-002, BND-COMPOSE-001, BND-COMPOSE-002, BND-TEMPORAL-002, BND-RECOVERY-002, BND-ENV-001; INT-001, INT-002, INT-003, INT-005, INT-006, INT-008.
- Demonstrate: A fresh-machine consumer resumes and justifies the exact current change from the bounded authoritative set; stable review replacement never loses an open finding or continuing decision; settled occurrences remain settled across unrelated container changes; recurrence creates a new finding linked to the applicable decision; evidence and Verify readiness follow declared dependencies; requests and superseded procedure are unnecessary.
- Evidence expectations: End-to-end lifecycle fixtures, finding/decision/evidence mutation matrices, current-view projections, deleted-log/request/history runs, and exact final subject/evidence binding.
- Non-applicability: Milestone-local checks prove components, but only integrated verification can prove the complete resume contract and cross-surface non-loss.

### TG-FINAL-02. Transaction, recovery, and retry integrity

- Covers: SR-22–SR-31, SR-33, SR-40–SR-46, SR-49; M1–M3, M5, M6; BND-INPUT-002, BND-STATE-004, BND-AUTH-002, BND-TEMPORAL-001, BND-TEMPORAL-002, BND-RECOVERY-001, BND-RECOVERY-002, BND-ENV-002; INT-001, INT-002, INT-004, INT-008.
- Demonstrate: Competing writers, stale identities, every injected interruption, persistence ambiguity, permission failure, disk failure, retry, unsafe path, and tampered recovery data yield one exact complete set or a fail-closed recovery state without private-data disclosure.
- Evidence expectations: Full fault matrix, before/after byte inventories, deterministic recovery outcomes, renderer parity, containment checks, and no-Git/no-network execution.
- Non-applicability: Final integrated proof is required because correctness spans evaluator, adapter, filesystem, reader, renderer, and semantic operation boundaries.

### TG-FINAL-03. Compatibility, activation, and published parity

- Covers: SR-01, SR-19–SR-26, SR-34–SR-49; M3–M6; BND-STATE-001, BND-STATE-003, BND-STATE-004, BND-COMPOSE-001, BND-COMPOSE-002, BND-COMPAT-001, BND-COMPAT-002, BND-COMPAT-003, BND-ENV-001; INT-003, INT-005, INT-006, INT-007, INT-008.
- Demonstrate: Exactly one coherent component matrix permits compact writing across canonical source, CLI package, validators, fixtures, documentation, and supported adapters; historical readers survive activation and rollback; ordinary legacy changes reject compact migration and writes; and only this exact implementing change can close and activate atomically through the bounded bootstrap without changing its legacy shape.
- Evidence expectations: Activation state matrix, canonical/generated byte checks, adapter inventories, legacy write-denial and rollback fixtures, historical byte comparisons, package validation, and broad smoke.
- Non-applicability: No individual milestone can prove coherent public activation across every shipped consumer.

### TG-FINAL-04. Context bounded by current state

- Covers: SR-02–SR-06, SR-19–SR-21; M1, M3–M5; BND-COMPOSE-001, BND-ENV-001; INT-003.
- Demonstrate: For equal authoritative current sets, summary and skill-context inputs, returned paths, and output scope remain equal when synthetic disposable procedure grows across reviews, corrections, transitions, and evidence executions.
- Evidence expectations: Paired fixtures with identical current sets and different procedural-history volumes, exact projection comparison, file-read instrumentation, and token/byte measurement using repository-owned tooling.
- Non-applicability: This is a change-level product outcome and cannot be inferred solely from local parser or CLI unit tests.

### TG-FINAL-05. Review judgment, material acceptance, and bootstrap closeout

- Covers: SR-08–SR-12, SR-15, SR-23, SR-25–SR-27, SR-31, SR-35, SR-46–SR-49; M3–M6; BND-INPUT-001, BND-STATE-001, BND-STATE-003, BND-STATE-004, BND-AUTH-001, BND-AUTH-002, BND-TEMPORAL-001, BND-TEMPORAL-002, BND-RECOVERY-001, BND-RECOVERY-002, BND-COMPAT-003, BND-ENV-001; INT-006, INT-007, INT-008.
- Demonstrate: Independent review judgment, material owner acceptance, and derived progression remain distinct; unrelated container drift cannot reopen a settled occurrence; only declared dependencies invalidate; and the exact implementing current set either closes and activates atomically once or leaves prior writer authority unchanged.
- Evidence expectations: Closed-vocabulary tests, owner-acceptance and progression matrices, per-occurrence resolution identity regression, genuine-recurrence fixture, exact bootstrap subject matrix, fault injection, replay and other-change denial, rollback proof, and runs with Git metadata and PR/network access absent.
- Non-applicability: The claim composes current review semantics, legacy normalization, transaction recovery, activation, and external-independence boundaries and therefore requires change-level proof.

## Validation plan

- Node unit and integration tests prove exact compact parsing, identities, pure evaluation, operations, transaction recovery, CLI projections, compatibility, legacy migration denial, and activation behavior.
- Python validator and workflow tests prove canonical repository semantics and cross-runtime fixture parity.
- Closed-vocabulary tests explicitly pass `unknown_value` or `not_in_vocabulary` for every new constant before consistency checks.
- Fault injection covers every preparation, replacement, persisted read-back, restoration, and cleanup boundary with exact byte inventories.
- Skill, guide, schema, documentation, and generated-package checks prove canonical semantic alignment and forbid hand-edited derived bodies.
- Adapter generation and distribution tests prove deterministic supported-runtime parity without publishing.
- Bounded-context fixtures and measurement prove projection cost follows current-state size rather than procedural-history length.
- `bash scripts/ci.sh --mode broad-smoke` runs only after focused milestone failures are resolved and supplies complete local repository evidence; hosted CI, release publication, and PR operations remain outside this plan.

## Risks and recovery

- Risk: A partial cutover gives two files or two engines authority over the same fact.
  - Recovery: Keep compact writing disabled until M5 proves the complete version matrix, and fail closed on mixed or unknown component identities.
- Risk: Stable-file replacement drops an adverse finding or still-binding rationale.
  - Recovery: Enforce promotion before replacement in the pure evaluator and retain ambiguous materiality as a current decision.
- Risk: Filesystem behavior does not support the specified success durability point.
  - Recovery: Detect capability before preparation and reject mutation as unsupported; do not weaken success semantics.
- Risk: Canonical text and executable validators drift during the broad workflow rewrite.
  - Recovery: Use shared valid/invalid fixtures, focused canonical scans, and one final activation gate across all consumers.
- Risk: The change becomes too large to review coherently.
  - Recovery: Preserve the six dependency-ordered review boundaries; do not combine activation with unreviewed model, transaction, CLI, governance, or post-activation correction work.

## Dependencies

- Accepted proposal; the revised Design package and this exact Plan require fresh Design Review and Delivery Review before M6 may be appended.
- M1 through M5 remain closed and immutable. M6 is a reviewed suffix, and its implementation requires stage-owned evidence and clean milestone Code Review before final holistic Code Review.
- Compact writer activation remains withheld through M4 and is the last mutation in M5 after integrated proof on the exact candidate.
- The current v3 contract governs this implementing change through its own closeout; it is not migrated to the model it implements.
- Existing YAML and standard-runtime filesystem primitives are used; any new dependency or changed durability outcome returns to Design.
- Canonical skills are edited only under `skills/`; adapter and package outputs derive from repository tooling.
- No Git history, pull-request data, network service, or local log is required to implement, test, recover, resume, or verify compact behavior.
- No external mutation, release, publication, PR opening, push, or merge is authorized by this plan.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-04 | Build the model, transaction adapter, CLI semantics, canonical contract, and activation as five ordered milestones. | Each slice has a distinct authority and rollback boundary, and activation cannot safely precede all four foundations. | One broad implementation milestone; one milestone per file; governance-first mixed deployment. |
| 2026-09-04 | Keep the compact writer disabled until the final parity milestone. | The approved contract requires one coherent writer set and rejects mixed consumers. | Progressive writer rollout; infer capability from file presence. |
| 2026-09-04 | Keep this implementing change on its current v3 record through closeout. | Migrating the implementation vehicle to its not-yet-proven output would create circular authority and weaken rollback. | Self-migration during implementation; rewrite its historical evidence. |
| 2026-09-04 | Treat Git, PRs, networks, and local logs only as optional surroundings, never plan dependencies. | The approved proposal and Design package require fresh-machine correctness and recovery from current repository state alone. | Git-based recovery; PR-based audit reconstruction; log-backed freshness. |
| 2026-09-04 | Represent the post-M5 Design correction as appended milestone M6. | Needed implementation must be planned and receive ordinary milestone Code Review; an exact reviewed suffix preserves M1 through M5 without a special final-review bypass. | Rewrite or reopen M1–M5; hide the work in a correction note; route implementation directly to final review. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done. Design Review must clear the revised Design package, Delivery Review must clear this exact Plan, and route must append M6 before implementation resumes.
