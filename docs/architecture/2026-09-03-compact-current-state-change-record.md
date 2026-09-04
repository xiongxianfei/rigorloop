# Compact Current-State Change Record Architecture

## Owning change record

- `docs/changes/2026-09-03-compact-current-state-change-record/change.yaml`

## Related artifacts

- Proposal: `docs/proposals/2026-09-03-compact-current-state-change-record.md`
- Spec: `specs/compact-current-state-change-record.md` (pending specification reconciliation)
- Plan: pending Delivery planning
- ADRs: `docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md`

## Introduction and Goals

This architecture replaces the history-oriented governed change pack with a compact current-state system. A fresh reader must be able to determine current lifecycle coordination, current independent judgments, open findings, materially constraining resolved decisions, current evidence and freshness, blockers, remaining work, and final readiness without reading procedural history.

The design keeps semantic responsibility with stage skills and reviewers while assigning mechanical consistency, lifecycle-derived operation eligibility, concurrency, freshness, projection, and recovery to the lifecycle CLI. The CLI does not authenticate callers or grant permissions; filesystem and execution access are the enclosing trust boundary. The model intentionally does not preserve superseded non-material chronology and does not depend on Git history, pull-request history, local logs, or an external service.

## Architecture Constraints

- `change.yaml` remains the sole coordinator of mutable lifecycle and routing state; it references rather than duplicates review, decision, and evidence contents.
- Proposals, specifications, architecture, ADRs, and plans remain canonical engineering contracts in their existing repository locations.
- Independent Proposal Review, Design Review, Delivery Review, milestone Code Review, final Code Review, and Verify remain distinct authorities.
- `skills/` remains the sole authored skill source, with deterministic supported-adapter generation from canonical content.
- The lifecycle CLI mechanically derives coordination state from stage-owned semantic input. It is not a product author, reviewer, workflow decision maker, test runner, or hosted service.
- Current state must remain self-sufficient after squash, rebase, missing PR history, a fresh checkout, another machine, or unavailable local logs.
- Historical completed changes remain valid under their recorded contracts and are not bulk rewritten.
- New compact changes activate only after all authoritative, executable, and published consumers support one coherent versioned contract.
- Unknown kinds, statuses, operations, authorities, evidence states, and retention classes fail closed.

## Context and Scope

The system remains repository-local. Humans and stage skills supply semantic content; route selects lifecycle direction; the CLI validates and applies structural operations; validators and CI check the resulting repository state; supported adapters deliver the same contract to target runtimes.

```text
human or stage skill
        │ semantic request and stage-owned content
        ▼
route / lifecycle CLI ──► compact current-state transaction
        │                            │
        │                            ├─ change.yaml
        │                            ├─ stable current review record
        │                            ├─ material-decisions.md
        │                            ├─ evidence.yaml
        │                            └─ verify-report.md
        ▼
bounded current projections ──► stage skill, reviewer, validator, CI
```

Git, pull-request hosts, and machine-local logs may exist around this boundary but are not inputs to governed resumption, progression, review, or verification. No network service, database, daemon, or background scheduler is introduced.

Separate C4 Mermaid sources are not needed because the change modifies an existing repository-owned workflow protocol and file transaction boundary rather than adding a deployable container or network interaction.

## Solution Strategy

Use five applicable durable surfaces with distinct responsibility and one transaction boundary:

1. keep coordination and references in `change.yaml`;
2. update one stable record for the current judgment of each review target;
3. promote only still-constraining resolved decisions into `material-decisions.md`;
4. keep only currently applicable proof metadata in `evidence.yaml`;
5. bind one successful `verify-report.md` to the exact final subject;
6. submit semantic operations as transient inputs;
7. have one pure engine construct the only eligible coordinator state and complete candidate transaction;
8. apply affected files through a lock, recoverable staged replacement, complete-set validation, and read-back; and
9. expose bounded projections derived only from the authoritative current set.

The core safety rule is promotion before replacement: no operation may discard a record until all information that still affects resumption, decision justification, or readiness exists in another current authoritative surface.

## Building Block View

### Current-state coordinator

`change.yaml` stores change identity, lifecycle contract, lifecycle revision, current stage, canonical artifact identities, current package and milestone states, blockers, open-finding and evidence references, typed remaining work, and readiness. A pending implementation milestone remains a typed `remaining_work` item until an exact semantic operation selects it; the evaluator then removes that item and derives the sole active milestone. It does not contain transition, review-round, correction, request, evidence-event history, or a caller-maintained operation list. The projection service derives allowed structural operations from the current snapshot.

### Stable review store

The review store contains one current record per Proposal Review, Design Review, Delivery Review, milestone Code Review, and final Code Review target. A record identifies its target and exact subject, current round, current judgment, open findings, owners, blocking effects, material-decision references, recording state, and current limitations. The judgment says only whether the reviewed subject is clear, has open findings, or could not be judged; it is not an approval, owner decision, or stored progression grant. A new round replaces the same path through the transaction boundary.

### Material decision memory

`material-decisions.md` contains resolved decisions that continue to constrain the change. The responsible decision owner supplies explicit acceptance, the decision, rationale, source finding, affected surfaces, owner metadata, and applicability; the engine validates identity, references, closed status, operation eligibility, and consistency with the current review set. Routine review clearance creates no decision entry. Decisions that cease to apply may be removed only through an eligible operation and only when no current contract, evidence, blocker, or remaining work references them.

### Current evidence manifest

`evidence.yaml` records only evidence currently relied upon. Entries bind claims or verification groups to exact subject paths and identities, method, outcome, covered surfaces, optional detail location, and freshness. A dependency is a typed reference to a subject in that evidence entry or to a current artifact, review, or material decision. The reader resolves only those declared references and hashes only declared subject paths. A mismatch produces a bounded drift blocker; review, progression, and Verify cannot rely on that evidence until an explicit operation replaces it or records it stale. Raw command output remains outside the governed set by default.

### Final Verify report

`verify-report.md` exists only for a successful final Verify result. It binds the verdict and explanation to the exact final subject and current evidence basis. A later invalidating mutation makes the report non-current or removes it from readiness; failed Verify attempts do not create a successful report.

### Pure lifecycle evaluator

The evaluator consumes one normalized current snapshot and one versioned semantic request containing only the requested operation, expected identities, and stage-owned content. A single eligibility table maps current stage, active work, target kind and state, blockers, findings, and readiness to admitted operations. The evaluator checks that table, responsibility metadata, finding preservation, decision promotion, evidence invalidation, stage and milestone consistency, and resulting-state invariants; then it mechanically derives progression from the current exact-subject judgment, absence of blocking findings, required accepted material decisions, current evidence, and applicable transition rules. It serializes the resulting references, readiness, projection state, `change.yaml`, and lifecycle revision into a complete candidate transaction. It accepts no caller identity, claimed authority, caller-constructed coordinator, derived lifecycle fields, or arbitrary candidate file set, and performs no I/O.

### Transaction and recovery adapter

The adapter discovers the exact change, acquires a private exclusive lock, rereads declared inputs, stages candidate bytes, writes recovery information containing prior and candidate identities and recoverable prior content, replaces affected files deterministically, validates and reads back the complete set, and either commits cleanup or restores the prior set. Readers refuse to consume a set while an unresolved transaction or recovery condition exists.

### Projection service

Read-only CLI projections expose current lifecycle, artifacts, reviews, open findings, material decisions, evidence, milestone, overall progression readiness, progression blockers, remaining work, permitted operations, requested-operation eligibility, and named-skill paths. Projection code reads the normalized current snapshot and never reconstructs history. Progression and operation diagnostics are evaluated separately: a progression blocker remains visible and prevents downstream advancement, but it does not prohibit a safe corrective operation unless the same condition violates an invariant applicable to that operation.

### Compatibility and packaging adapters

Compatibility readers select semantics from an explicit lifecycle-contract discriminator. Canonical skills, schemas, validators, documentation, fixtures, and adapter metadata ship as one coherent contract version. Historical readers remain read-only; new writers never emit a mixed shape. The first compact release creates only new compact changes; ordinary legacy changes, including changes already in flight at activation, finish under their registered contract and have no compact migration operation. The implementing change named in the closed bootstrap rule below remains structurally legacy but may use that rule solely for final preactivation closeout.

## Runtime View

### Stable review replacement

1. The reviewer receives a bounded projection naming the exact review target, subject identity, current open findings, and required paths.
2. The reviewer produces the candidate current judgment and finding dispositions. A decision owner separately accepts any material decision that must persist.
3. The CLI acquires the change lock and rereads all relevant current identities.
4. The evaluator compares prior and candidate findings. Still-open findings must remain; resolved findings require a valid final disposition; materially constraining resolutions require accepted decision-memory entries.
5. The evaluator invalidates only current judgments, evidence, or readiness whose declared dependency changed. Editing a container that also mentions settled findings does not reopen them. A later regression against a settled material decision is a new finding that references that decision, never resurrection of the old finding occurrence.
6. The adapter stages, validates, replaces, and reads back the complete affected set.
7. Success exposes the new current judgment and mechanically derived progression. Failure restores the prior complete set or blocks all governed reads pending explicit recovery.

### Artifact revision and evidence freshness

1. An authoring stage supplies canonical artifact content and identifies the exact prior subject.
2. The adapter reads the bounded paths named by current evidence; the pure evaluator compares those observations with typed subject, artifact, review, and decision dependencies.
3. Unaffected evidence remains current; invalidated evidence becomes stale or leaves the readiness basis.
4. The evaluator constructs `change.yaml` with the new artifact identity, derived coordination, and current evidence references in the same recoverable transaction.
5. A read-time subject mismatch returns a drift blocker without silently mutating records; the projection reports the exact evidence and required invalidation or rerun.

### Correction route and return

1. Route submits current source finding, destination owner and stage, reason, required return condition, and expected next review.
2. `change.yaml` exposes that active correction as current coordination; no route receipt is required.
3. On return, the author and reviewer update the affected artifact, current judgment, decisions, and evidence.
4. The correction state clears only when the return condition and required rereview are current and consistent.

### Milestone selection and progression

1. Delivery leaves each not-yet-active implementation milestone as a typed pending current-work item; active work is separate and singular.
2. At `implement` with no active work, route supplies one current milestone ID through `advance-milestone` with `null → planned`; it does not supply an active-work record, ordering claim, or derived status.
3. The evaluator verifies the selected entry is present, pending, milestone-kind, and implementation-owned, removes it from remaining work, and constructs the planned active milestone in one transaction.
4. The existing adjacent transitions move that active milestone to implementing, review-required, and then closed after exact Code Review and evidence. Closure clears active work rather than retaining milestone history.
5. If another pending milestone remains, projection selects `code-review → implement`, where another explicit current-ID selection is required. If none remains, findings, triggered CI work, and final-review state select the downstream route.
6. Missing, blocked, wrong-kind, wrong-owner, duplicated, or stale selection rejects unchanged. Exact retry cannot reactivate an item already removed from remaining work.

### Successful final verification

1. Verify receives the exact final subject, current review state, current decisions, current evidence, and remaining-work projection.
2. It reuses or reruns evidence according to explicit freshness and coverage.
3. On success, the transaction writes the current evidence basis, final readiness state, and one exact `verify-report.md` together.
4. On failure, current blockers and evidence may update, but no successful report or branch-ready state appears.

### Implementing-change bootstrap closeout

The bootstrap applies only to `2026-09-03-compact-current-state-change-record` before compact writers activate. It does not migrate or reinterpret that change. One deterministic identity binds the current proposal, architecture, applicable ADR, specification, plan, implementation surfaces, latest applicable review judgments, current evidence basis, current lifecycle revision, and activation manifest. The bootstrap validator evaluates only current consequential state: current open findings, still-applicable material decisions, current evidence, required validation, exact-subject final review, Verify, and activation coherence. Superseded requests, receipts, review rounds, and already-settled finding occurrences are outside that decision basis.

Any missing member, identity drift, current open blocker, stale required evidence, non-clear final review, failed Verify, or incoherent activation input rejects unchanged. When all conditions hold, final closeout and compact-writer activation are one recoverable transaction. No Git commit, branch, diff, pull request, hosted service, or local diagnostic log is an identity or readiness input. The exception expires when that exact activation succeeds and cannot be selected by another change.

### Stale, concurrent, or interrupted operation

An expected-revision or input-identity mismatch rejects unchanged. A live lock returns busy. An interrupted prepared transaction is abandoned or restored according to exact identities; a partially replaced or unverifiable transaction blocks all governed consumption until explicit recovery. No recovery path consults Git or PR history.

## Deployment View

The change ships inside the existing repository and npm package boundaries:

- canonical workflow guidance and stage skills under `skills/`, `specs/`, `docs/`, `schemas/`, `scripts/`, and templates;
- the lifecycle engine, CLI handlers, snapshot reader, projector, and transaction adapter under `packages/rigorloop/`;
- repository-owned Python and Node validation during activation, with one final executable authority after parity;
- deterministic adapter metadata and generated release archives for supported runtimes; and
- bounded machine-local diagnostic logs in the existing platform state/log location, never as governed evidence.

No new service, database, credential, network call, repository daemon, or hosted dependency is introduced. Activation and rollback operate through versioned package and contract compatibility, not historical change rewriting.

## Crosscutting Concepts

### Responsibility, eligibility, and local trust

Stage skills and human owners supply semantic content within their documented responsibilities. Reviewers decide findings and materiality; route decides lifecycle direction; Verify decides final readiness. Owner, reviewer, and producer fields preserve that responsibility and provenance but do not identify or authenticate the process invoking the CLI. The CLI derives structural operation eligibility from the current lifecycle state and target, validates responsibility metadata, constructs derived coordination state, and persists only the valid result. Operating-system permissions, sandbox policy, or an enclosing authenticated runner govern who may execute the CLI or edit repository files.

Overall readiness is not an authorization primitive. The projector derives progression status and requested-operation eligibility from the same normalized snapshot but applies their distinct predicates. Skills may act only when their exact requested operation is permitted and has no operation-scoped blocker; they must continue to report progression blockers and must not interpret local actionability as downstream readiness.

### Identity and optimistic concurrency

Every mutation binds the current lifecycle revision and all relevant prior file identities. Unknown, omitted, stale, extra, or contradictory inputs fail unchanged. The lifecycle revision is a whole-current-set optimistic-concurrency token only; it is not evidence that every record semantically depends on every other record. Semantic invalidation follows explicit typed dependencies, so changing an unrelated current file cannot reopen a settled finding or stale unrelated evidence merely because the lifecycle revision changed.

### Promotion before replacement

The engine treats current open finding occurrences, materially constraining accepted decisions, current evidence, blockers, and remaining work as non-lossy classes. A finding occurrence has its own stable identity and disposition; its resolution does not depend on the identity of the file that happens to contain the resolution. Superseded wording, routine resolved findings, transport inputs, and diagnostic events are disposable only after current invariants prove that no continuing consequence depends on them.

### Evidence freshness

Evidence dependencies are typed and identity-bound. `subject` resolves to an exact path and identity within the same evidence entry; `artifact`, `review`, and `decision` resolve to their current coordinator references. Readers observe only those bounded paths. A changed dependency blocks reliance immediately and must be persisted as stale, removed, or replaced before progression. Timestamps, filenames alone, command text, history, and local logs cannot establish freshness.

### Transaction isolation and recovery

Multi-file atomicity is an observable contract implemented with one writer lock, staged candidate files, durable recovery data, deterministic replacement, complete-set validation, read-back, and restoration. Readers fail closed while recovery is unresolved.

### Security and privacy

Paths remain repository-relative and contained. Current files, transient requests, recovery bundles, and logs reject secrets and unsafe paths. Lock and recovery data use restrictive permissions and bounded content. Raw validation output and environment-specific diagnostics remain untracked by default.

### Compatibility and prospective adoption

Contract identity, not file-shape inference, selects legacy or compact semantics. Historical and ordinary in-flight legacy changes remain readable and writable only under their registered contract. Compact v1 applies only to newly created changes after coherent activation; it defines no migration operation. The one implementing-change bootstrap changes neither its contract discriminator nor its file shape and grants no general legacy write path. Compact writers activate only with compatible skills, validators, CLI, docs, fixtures, and adapters, and rollback restores the prior coherent writer set.

### Validation

Structural validation checks closed vocabularies before consistency, exact cross-file references, open-finding preservation, decision applicability, evidence dependency and freshness, transaction-state absence, projection consistency, historical read-only compatibility, and generated-package parity. Semantic review remains responsible for adequacy and materiality.

## Architecture Decisions

- [ADR-20260903 Compact Current-State Transaction Boundary](../adr/ADR-20260903-compact-current-state-transaction-boundary.md) — extend the pure lifecycle engine to a recoverable multi-file current-state boundary and make superseded procedure disposable.
- [ADR-20260824 Governed Lifecycle CLI Transaction Boundary](../adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md) — retained for pure-engine, authority, revision, parsing, locking, recovery, and local-trust foundations, with the single-file boundary superseded after activation.

## Quality Requirements

| Quality | Scenario | Measure |
| --- | --- | --- |
| Resumability | A new agent opens a compact change on a fresh machine with no PR or local logs | One bounded projection identifies current state, open findings, decisions, evidence, blockers, remaining work, and required paths. |
| Corrective actionability | A change is globally blocked by an open finding and invalidated downstream package | The owning correction is projected as permitted while downstream advancement remains blocked; any target-specific invariant failure prohibits the correction explicitly. |
| Multi-milestone resumption | A change has no active work and one or more pending implementation milestones | The projection exposes current pending IDs; one exact selection creates planned active work atomically, and invalid or stale selection changes no current bytes. |
| Non-loss | A reviewer resolves or removes a finding while replacing a stable review record | The operation fails unless the finding remains open, has a valid final disposition, or has a required material-decision entry. |
| Resolution stability | A current document or resolution container changes after an older finding was settled | The old finding stays settled; only declared current dependencies invalidate, and a genuine regression creates a new finding referencing the retained decision. |
| Freshness | An artifact changes after evidence was recorded | Every explicitly dependent evidence entry leaves the current readiness basis in the same transaction. |
| Concurrency | Two actors mutate the same review target from one revision | Exactly one succeeds; the stale operation fails without modifying any authoritative file. |
| Recovery | The process stops after replacing only part of the candidate set | Readers block, and deterministic reconciliation restores the prior complete set or completes the exact candidate without Git history. |
| Bounded context | A skill requests one stage context | The projection returns only current applicable facts and exact required paths, with no procedural event scan. |
| Portability | A repository uses squash merges or loses hosted PR history | Current routing, review, evidence, and Verify behavior is unchanged. |
| Compatibility | A completed historical change uses per-round reviews and request files | It remains readable under its recorded contract and cannot authorize compact writes. |
| Bootstrap | The implementing change reaches preactivation closeout without Git or PR identity | Exact-current-set validation, clear final review, passing Verify, and coherent activation succeed atomically or leave the prior writer authority unchanged. |
| Security | A request, evidence path, recovery item, or log field contains an unsafe path or secret-like value | Validation rejects before authoritative replacement and does not echo sensitive content. |

## Risks and Technical Debt

- Multi-file recovery is more complex than the current single-file adapter and requires exhaustive fault injection at every replacement and cleanup boundary.
- A Markdown material-decision surface requires a strict machine-readable field contract or a bounded companion parser; vague prose cannot protect non-loss invariants.
- Stable review paths increase local contention and make stale identity checks mandatory for both human and automated reviewers.
- Materiality remains a semantic judgment. Over-retention recreates noise; under-retention loses constraints. Ambiguous cases must remain retained until the responsible reviewer or decision owner settles them.
- Explicit evidence dependencies can be incomplete. Design Review and validators must challenge coverage, while Verify must not infer freshness from absence of a dependency.
- During activation, legacy Python validators and the Node engine may disagree. Activation must fail until shared fixtures prove parity and the writer authority is singular.
- The current canonical architecture still describes the history-oriented catalog and single-file transaction model. Implementation must update it coherently rather than leaving this change-specific package as competing current truth.

## Glossary

- **Authoritative current set:** applicable current-state files whose complete contents are sufficient for governed resumption and justification.
- **Promotion:** moving a continuing consequence from a record about to be replaced into its durable current owner.
- **Material decision:** a resolved decision whose rationale continues to constrain later work or readiness.
- **Current evidence basis:** evidence entries presently allowed to support review, progression, or verification.
- **Disposable procedure:** superseded non-material wording, events, requests, receipts, or diagnostics with no continuing consequence.
- **Observable atomicity:** readers see either the complete prior state or complete candidate state and block during unresolved recovery.
- **Semantic request:** transient structured intent submitted to the CLI without becoming a governed artifact or carrying an authentication claim.

## Next artifacts

- Specification reconciliation.
- Design Review of this architecture, its ADR, and the resulting specification as one exact package.

## Follow-on artifacts

- None yet.

## Readiness

Architecture correction is complete and ready for ADR and specification reconciliation. Design progression remains withheld until Design Review records a clear judgment for the exact architecture, ADR, and specification package with no blocking findings.
