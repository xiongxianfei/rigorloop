# ADR-20260903: Compact Current-State Transaction Boundary

## Owning change record

`docs/changes/2026-09-03-compact-current-state-change-record/change.yaml`

## Context

RigorLoop's governed lifecycle currently stores mutable coordination in `change.yaml` while formal reviews, review logs, review resolutions, operation requests, correction receipts, stage-authoring evidence, and validation events preserve overlapping procedural history. ADR-20260824 established one pure lifecycle engine, optimistic concurrency, exact artifact identities, and a recoverable transaction adapter, but limited mutation to `change.yaml` and treated other records as separately authored evidence.

The accepted compact current-state proposal changes the persistence boundary. A governed change must remain resumable and justifiable from current lifecycle state, current review judgment and open findings, materially constraining resolved decisions, current evidence, remaining work, and final verification. Superseded non-material procedure is disposable. Git history, pull-request history, committed operation requests, and local logs are not part of the correctness or resumption contract.

The CLI must therefore protect a small set of coordinated files without becoming an append-only event store or semantic author. A successful operation may need to update several current records together, while a crash or stale actor must never expose a partially updated state as valid.

## Decision

Extend the governed lifecycle engine and transaction adapter from a single-file `change.yaml` mutation boundary to one recoverable compact-current-state transaction boundary.

The authoritative current-state set consists only of applicable instances of:

1. `change.yaml` for lifecycle coordination, current artifact identities, review-package and milestone state, blockers, open-finding references, evidence references, remaining work, and readiness;
2. one stable current review record per formal gate or Code Review target for current judgment and open findings;
3. `material-decisions.md` for resolved decisions that continue to constrain requirements, architecture, authority, security, compatibility, residual risk, implementation, or verification;
4. `evidence.yaml` for current evidence provenance, subject identities, covered claims, outcomes, and freshness; and
5. `verify-report.md` for the exact successful final-verification subject, evidence basis, residual risks, explanation, and PR handoff.

Canonical proposals, specifications, architecture, ADRs, and plans remain separate engineering contracts referenced by `change.yaml`; they are not folded into the compact set.

A review record owns independent judgment only: the exact current subject is `clear`, has `findings-open`, or is `blocked` because judgment cannot complete. A clear judgment is not an approval or owner decision. The evaluator derives progression from a clear exact-subject judgment, no blocking findings, accepted material decisions when required, current evidence, and the applicable transition rule. A decision owner records explicit acceptance only for a discretionary direction, exception, limitation, or residual risk that must persist in `material-decisions.md`.

Keep one pure transition evaluator. It consumes a normalized snapshot plus a versioned semantic request containing expected identities and stage-owned semantic content, then constructs a complete candidate transaction or rejects. It derives structural operation eligibility from one closed table over current lifecycle state, active work, target, blockers, findings, and readiness. It mechanically constructs `change.yaml`, derived references, readiness, the allowed-operation projection, and the lifecycle revision; callers cannot submit those resulting coordination fields or an arbitrary final candidate set. The evaluator does not accept a caller identity or claimed authority, read the filesystem, infer semantic decisions, author review prose, choose materiality, run validation commands, choose routes, or preserve an event history.

Each candidate transaction is evaluator output. It contains the expected lifecycle revision, exact prior identities for every read or replaced authoritative file or observed evidence subject, the derived candidate bytes for every affected file, the resulting identities, and the invariant checks that must pass. The lifecycle revision is an optimistic-concurrency token for the current set, not a semantic dependency edge among all records. Semantic invalidation follows declared artifact, review, decision, and evidence dependencies. Unaffected files are not rewritten. A no-op or identical retry succeeds only after rereading and validating the complete current basis.

Use one change-local exclusive lock and one private recovery bundle for a transaction. Because ordinary filesystems do not provide atomic replacement of several independent files, observable atomicity is achieved through isolation and recovery:

1. acquire the change-local lock before reading mutation inputs;
2. reconcile or reject any existing recovery state;
3. reread all declared authoritative inputs and verify expected identities and lifecycle revision;
4. generate and validate the complete candidate set in a staging area on the same filesystem;
5. durably record prior and candidate identities and recoverable prior bytes before replacement;
6. replace affected files in a deterministic order while the lock remains held;
7. validate the complete persisted set and its resulting revision;
8. restore the complete prior set on a recoverable failure, otherwise leave an explicit recovery-required state; and
9. remove recovery state before releasing the lock.

All governed readers must detect the lock or recovery state and return busy or recovery-required rather than treating a partially replaced set as authoritative. Exact file names, bundle encoding, size limits, and fsync policy are specification decisions, but recovery must not depend on Git or a hosted service.

Before a stable review record is replaced, the engine must prove that every previously open finding occurrence remains open in the candidate record or has a valid final disposition. Each occurrence has identity and disposition independent of the identity of any containing review or resolution file. A resolved finding that still constrains the change must have a corresponding applicable, explicitly accepted entry in `material-decisions.md`; a non-material resolved finding may disappear. Changing a document or container invalidates only current judgments and evidence that declare that dependency and never reopens a settled occurrence. A later violation of a retained decision creates a new finding that references the decision. Materiality comes from reviewer input and acceptance from the decision owner, while the engine enforces references, responsibility metadata, lifecycle-derived operation eligibility, status consistency, and non-loss invariants.

The CLI is not a permission system. Owner, reviewer, and producer labels record workflow responsibility and provenance, not the authenticated identity of the invoking process. Operating-system permissions, sandbox policy, or an enclosing authenticated runner control who may invoke the tool or modify the repository. A request-level `authority` claim would add no security and is therefore excluded from the operation envelope.

Evidence freshness uses typed explicit dependencies. A dependency resolves either to a subject path and identity declared in the same evidence entry or to the current identity of an artifact, review, or material decision. The adapter reads only those bounded paths, and the evaluator compares the observations with the declared identities. A read-time mismatch blocks reliance without silently mutating the record. Before progression, an explicit operation must replace the evidence, mark it stale with a required rerun, or remove it when no current consequence needs it. The engine does not infer continued validity from timestamps, Git ancestry, pull-request state, or prior execution logs.

Successful operation requests are transient inputs. The CLI may accept arguments, stdin, or a temporary request path, but a request file or transport receipt is never an authoritative output of the compact contract. Local diagnostic logs remain bounded, disposable, secret-safe observability and never satisfy review, progression, evidence, verification, or resumption requirements.

Read-only CLI projections are derived from the current authoritative set plus direct identity observations of explicitly referenced evidence subjects. Required projections cover lifecycle summary, artifact identities, review states, open findings, material decisions, current evidence and freshness, active milestone, overall progression readiness, progression blockers, remaining work, derived permitted operations, requested-operation eligibility, and exact paths needed by a named skill. Progression blockers and operation blockers are distinct derived views: a global blocker continues to prohibit downstream advancement but cannot prohibit a structurally eligible correction unless an invariant applicable to that exact operation fails. Overall status is therefore never an authorization primitive. Governed historical reconstruction is not provided and no mutation or gate depends on repository or pull-request history.

Activate the compact model under an explicit versioned lifecycle-contract discriminator only after CLI mutation and recovery, schemas, validators, skills, workflow guidance, fixtures, canonical architecture, contributor documentation, and supported adapter packages agree. Compact v1 applies only to new changes created after activation. Completed historical changes remain readable, and ordinary in-flight legacy changes finish under their registered contract; compact v1 provides no in-place migration operation. No reader infers compact semantics from file presence.

One closed bootstrap exception applies only to the implementing change `2026-09-03-compact-current-state-change-record`. It does not migrate that change or reinterpret its registered contract. Before activation, the CLI derives one deterministic exact-current-set identity over its authoritative contracts, implementation surfaces, latest applicable review judgments, current evidence basis, lifecycle revision, and activation manifest. It validates only current consequential state: current open findings, applicable material decisions, required evidence and validation, exact-subject final review, Verify, and activation coherence. Superseded requests, receipts, review rounds, and already-settled finding occurrences are not readiness inputs. Missing input, identity drift, a current blocker, stale required evidence, non-clear final review, failed Verify, or activation inconsistency rejects unchanged. Successful closeout and compact-writer activation occur in one recoverable transaction without Git, branch, diff, pull-request, hosted-service, or local-log identity. The exception expires after that exact activation and cannot be selected by another change.

This decision supersedes ADR-20260824 only where that ADR limits the transaction adapter to replacing `change.yaml`, requires separately committed procedural evidence for supported operations, relies on current event-oriented change records, or treats caller-asserted stage authority as authorization. It retains the pure engine, semantic-operation boundary, optimistic concurrency, exact identities, fail-closed parsing, lock and recovery principles, stage-scoped responsibility, workflow-owned routing, local trust boundary, and no external database decision.

## Alternatives considered

- Keep the current history-oriented active record: rejected because current truth remains distributed and resumption cost grows with procedural rounds.
- Update stable files independently: rejected because a crash or stale actor could remove a finding, retain stale evidence, or expose inconsistent current state.
- Store one monolithic YAML or Markdown record: rejected because it creates a large merge surface, mixes distinct ownership, and weakens bounded projections.
- Retain an append-only event log and derive current state: rejected because history becomes a correctness dependency and restores the context-growth problem.
- Use Git or pull-request history as the recovery or audit source: rejected because preservation varies by commit and merge policy and is unnecessary for the approved resume contract.
- Use a hosted database or transaction service: rejected because it violates the repository-local product boundary and adds availability, trust, migration, and credential requirements.
- Require every semantic author to edit the stable files directly: rejected because cross-file loss, freshness, and recovery invariants require one mechanical boundary, while semantic judgment still remains with stage owners.
- Accept a caller-constructed final `change.yaml` and candidate set: rejected because it duplicates state-construction logic, permits callers to propose derived authority fields, and reduces the CLI to a patch validator rather than the single transition engine.
- Migrate in-flight legacy changes in compact v1: rejected because prospective adoption achieves the goal without a second source-schema evaluator, consequence-extraction protocol, or mixed-contract transaction.

## Consequences

- Current state becomes bounded and directly queryable, while non-material procedural chronology may be permanently lost.
- The CLI transaction adapter becomes more complex because it must isolate and recover a coordinated file set rather than one file.
- Stable review files create contention at one target, mitigated by exact identities, exclusive ownership during a transaction, and stale-write rejection.
- Reviewers and resolution owners must classify whether a resolved finding remains materially constraining; uncertain cases remain retained until settled.
- Review judgment, material decision acceptance, and lifecycle progression have distinct owners and storage; routine clearance no longer creates duplicate approval state.
- A settled finding occurrence stays settled across unrelated document or container revisions; a genuine recurrence is a new finding linked to the retained decision.
- Evidence invalidation becomes explicit and reviewable but requires every relied-on evidence entry to name its dependency basis.
- Skills become smaller consumers of bounded projections and semantic producers of candidate content; they no longer scan or maintain procedural ledgers.
- Historical and ordinary in-flight legacy changes remain structurally different and require compatibility readers, but compact v1 needs no migration writer; the implementing change has only the closed preactivation bootstrap described above.
- Adapter and validator activation must be coordinated because a mixed package could disagree about which files are authoritative.
- Repository and PR history may still exist incidentally, but no supported operation, review, or readiness claim may require it.

## Follow-up

- Specify the compact schemas, semantic inputs and derived outputs, projection shapes, lifecycle-derived operation-eligibility matrix, typed dependency resolution, responsibility metadata, multi-file recovery protocol, evidence invalidation rules, material-decision applicability, compatibility discriminator, and activation requirements.
- Reconcile the architecture and specification through Design Review before Delivery planning.
- Amend the canonical architecture package and ADR index during implementation when the approved specification fixes the final contract.
- Preserve ADR-20260824 as history and add explicit supersession links there only when implementation activates this decision.
