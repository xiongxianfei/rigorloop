# Separate Operational Records from the Engineering Definition

## Challenge

RigorLoop needs durable, inspectable engineering work that humans and local agents can resume without reconstructing a conversation. Today, operational Changes and their supporting records live under `docs/changes/`, alongside the version-controlled engineering definition. The current Records contract requires registered JSON files, while CLI consumers discover, reference and publish that file-based store. Retained work therefore adds repository files and path dependencies even when the current engineering model already contains the accepted result.

The requested direction is one local checkout, one user and one or more local agents, with SQLite holding operational records and separate files holding bulky evidence. The engineering definition must remain understandable without that local history. This changes an established persistence and portability choice; it is not merely directory cleanup or a new implementation of unchanged storage requirements.

Before proposing new requirements, this proposal analyzes the existing Initial Requirements in `design/requirements/`. These REM records own the need statements under examination; earlier proposals supply historical context, not substitutes for those IRs. The REM model remains draft, while the current Constitution and retained `docs/design/` contracts govern existing product behavior until explicitly reconciled.

## Goals

- Preserve durable, traceable and resumable Changes, decisions, reviews, findings and verification evidence without requiring operational history in the current Git tree.
- Keep the current engineering definition, implementation and applicable design rationale independently readable and usable from the repository.
- Let humans and agents create work and retrieve relevant context through RigorLoop without managing record directories, manifests or storage paths.
- Support safe concurrent local agents and retain assessment identities, explicit decision ownership and evidence provenance.
- Make operational history recoverable and transferable together with its retained evidence.
- Decide whether the need requires a new REM IR or refinement of existing IRs, preserving stable identities and existing responsibility boundaries.

## Scope and non-goals

### Initial intent treatment

| User goal or constraint | Treatment | Destination |
| --- | --- | --- |
| Analyze existing IR before adding direction | in scope | Existing-direction analysis below |
| Git owns the current engineering definition; SQLite owns operational records | in scope | Three storage classes and authority boundary |
| One project-local database for one checkout and multiple local agents | in scope | Local operating model |
| Searchable semantic records and bounded context instead of file bookkeeping or database dumps | in scope | CLI-mediated inspection and recording |
| Large content-addressed evidence outside the database | in scope | Artifact storage with referenced identities |
| Backup, restoration, stable project identity and versioned storage | in scope | Durability and adoption obligations |
| Preserve prior evidence and safely retire `docs/changes/` | in scope | Explicit migration and historical disposition |
| SQLite transaction and concurrency details, including WAL selection | deferred follow-up | CLI and Records Design; no setting is mandated here |
| Local web UI enabled by the new store | out of scope | Possible future consumer; no UI delivery commitment |
| Move requirements, features, functions, modules or interfaces into SQLite | rejected option | Engineering definition remains repository-owned |
| Rename the current engineering documentation tree | out of scope | Existing `design/`, retained `docs/design/`, proposal and plan locations remain |

### Scope budget

| Work family | Treatment | Boundary |
| --- | --- | --- |
| Operational storage authority and retention | core to this proposal | Select local SQLite plus an artifact store |
| Bounded CLI reads and explicit writes | core to this proposal | Remove storage-layout work from ordinary callers |
| Backup/restore, project association and storage versioning | same-slice dependency | Required for trustworthy adoption, not optional later hardening |
| Migration and historical preservation | same-slice dependency | Resolve current reliance before retiring operational files |
| Skills, governance, validation, packaging and release consumers | same-slice dependency | Reconcile every affected supported consumer before activation |
| Implementation milestones and proof allocation | separate implementation slice | Delivery owns sequencing after Design review |
| Hosted services, distributed synchronization and multi-user authorization | out of scope | No new server or collaboration platform |
| Broader requirement-model redesign and engineering-model relocation | out of scope | Preserve existing authoring responsibilities |

This is an isolated proposal-authoring request. It creates no Change registry, workflow transition or approval. Existing proposals and plans remain in Git for this scope; only operational record authority and its required consumers change. A specific dependency inventory belongs to Design and Delivery, rather than an unbounded repository cleanup.

## Governing principle

Keep the engineering definition independently understandable, and make the work that establishes it durable, traceable and recoverable without exposing storage mechanics to its users.

## Proposed direction

### Existing IR analysis: refine the existing requirements

The [REM requirements index](../../design/requirements/README.md) identifies ten Initial Requirements, each represented by an `ir.json` with a stable identity, need statement and 5W2H analysis. The [REM requirement model](../../rem/models/requirements.md) defines an IR as a durable stakeholder need; a proposal is a change artifact, not an IR entity. The older proposal-level convention in `templates/shared/requirement-to-delivery-model.md` does not describe these REM records. This proposal organizes the incoming request as RR input to Requirement Analysis. It uses the REM meaning requested by the user, without claiming that the existing product contracts have already migrated. Proposal approval does not itself create, approve or establish satisfaction of an IR.

| Existing IR | Coverage relevant to this proposal | Recommended treatment |
| --- | --- | --- |
| [IR-001 — Preserve engineering knowledge across sessions](../../design/requirements/IR-001-preserve-engineering-knowledge-across-sessions/ir.json) | Current definitions and still-applicable reasoning remain understandable independently of the originating session. SR-004 excludes history replay; SR-005 retains applicable rationale. Its assumptions do not supply a backup service. | Reuse the need and SRs. Clarify their application to an engineering model that remains usable without the operational database. Keep operational backup ownership under IR-003. |
| [IR-002 — Trace engineering obligations and responsibilities](../../design/requirements/IR-002-trace-engineering-obligations-and-responsibilities/ir.json) | Typed engineering relationships and bounded navigation, including explicit completeness under SR-009. | Preserve model traceability. Do not relocate engineering entities to SQLite or treat database foreign keys as sufficient engineering traceability. Change-specific provenance belongs to IR-003. |
| [IR-003 — Control engineering changes and recover prior states](../../design/requirements/IR-003-control-engineering-changes-and-recover-prior-states/ir.json) | Change continuity, original decisions, retained states and provenance. SR-006 owns resumption; SR-020–024 cover retained baselines, comparison, recovery, controlled transitions and retirement. | Primary need owner. Refine its analysis and scope to include backup, restoration and transfer of local operational records and retained artifacts. Preserve its identity and broad need statement. Derive missing obligations beneath it rather than inventing a storage-specific IR. |
| [IR-004 — Assess engineering claims using applicable evidence](../../design/requirements/IR-004-assess-engineering-claims-using-applicable-evidence/ir.json) | Applicable observed evidence, explicit gaps and scoped judgments; SR-027/028 distinguish evidence applicability and assessment. | Preserve the need. Reconcile evidence availability and identity across database, artifacts and transfers without treating import or migration as renewed approval. |
| [IR-008 — Operate on recorded engineering work through reliable explicit commands](../../design/requirements/IR-008-operate-on-recorded-engineering-work-through-reliable-explicit-commands/ir.json) | Selected reads, explicit recording, coherent publication, recovery and bounded outcomes under SR-040–047. Its analysis explicitly covers the existing v3 workflow store and retains the old CLI contracts. | Primary operational-interface owner. Refine the selected storage scope and assumptions, then reconcile affected SRs and ARs with the replacement store. Keep actor authority and bounded results intact. |
| IR-005, IR-006, IR-007, IR-009 and IR-010 | Model interpretation, authoring guidance, learning, portable engineering activities and compatible tooling. | Retain their need identities. Reconcile affected schemas, guidance, handoff and distribution consumers downstream; none supplies a distinct new stakeholder need for SQLite itself. |

**Recommendation: refine IR-003 and IR-008; do not create a new IR for SQLite or removal of `docs/changes/`.** The stakeholders and desired outcomes already have owners. The storage choice changes realization and the supported recovery scope, not the identity of the underlying needs. Reuse IR-001, IR-002 and IR-004 for their adjacent obligations rather than duplicating those obligations under a new root.

The material gap is explicit: IR-003 currently guarantees recovery only from an available intact retained Baseline, excludes destruction of retained storage, and assumes that storage remains accessible. IR-008 similarly introduces no disaster-recovery promise. Those provisions do not already satisfy the proposed backup/restore capability. Refine them to require creation and use of recoverable operational backups, with retained artifact coverage and explicit completeness. A recovery claim remains conditional on an available valid backup; this does not promise recovery after every copy has been destroyed or provide a hosted backup service. Backup placement, failure handling, retention and supported transfer need downstream requirements and acceptance criteria.

IR-008's existing byte-preservation, v3-registration and explicit transaction-recovery obligations also need deliberate reconciliation, not mechanical renaming. Preserve semantic content, record and subject identities, unrelated work and safe stale-write behavior while revising representation-specific requirements. Separate database transaction recovery from restoring a backup; neither proves the other. Each new SR must have exactly one IR parent, with shared use expressed through relationships rather than duplicate parentage.

A new IR would be justified only if subsequent analysis reveals a distinct stakeholder need that cannot coherently fit these existing scopes. No such need has been established here. Following the [Requirement Analysis method](../../rem/methods/requirement-analysis.md), downstream work should refine the relevant 5W2H analysis and Scenarios before deriving or changing SRs, Functions and architectural allocations. This proposal does not edit or approve those draft records.

### Relationship to earlier proposals and retained contracts

The [compact-record proposal](2026-09-03-compact-current-state-change-record.md) already seeks compact resumption and less repository noise; retain those goals. The [explicit-recording proposal](2026-09-05-explicit-recording-and-model-centered-design.md) preserves actor-owned judgments and separate engineering definitions; retain that boundary. Earlier [CLI architecture direction](2026-08-28-governed-repository-cli-architecture.md) excluded database persistence, and the current [Records contract](../design/cli/records.md) requires registered JSON files. Those choices require explicit reconciliation before adoption. The [v2 retirement direction](2026-09-11-retire-v2-record-format.md) continues to protect historical meaning without reviving unsupported runtime formats.

These historical proposals explain the storage change; they do not determine whether a new REM IR is needed. Preserve them unchanged. The new proposal records a proposed refinement to existing requirements and a new persistence direction, with independent review and downstream contract reconciliation still required.

### Three storage classes

| Information class | Authority and placement |
| --- | --- |
| Current engineering definition | Repository files, tracked in Git for this project: `design/requirements/`, `design/system/`, `design/architecture/`, retained governing contracts, source code and currently applicable rationale |
| Operational engineering records | One project-local SQLite store: Changes, work state, reviews, findings, decisions, verification, evidence metadata and retained provenance/history |
| Bulky evidence | A local content-addressed artifact store, referenced by operational records and included in applicable retention and backup |

Use an ignored project-local `.rigorloop/` runtime area for the database, artifacts and necessary recovery material. Keep the logical record-persistence responsibility distinct from SQLite as its physical realization. Store useful relationships and queryable facts rather than treating the database solely as a collection of existing JSON blobs. Exact schema, filenames, public commands and database access library remain Design decisions.

RigorLoop should provide the supported operational interface for humans and agents, including bounded inspection across Changes and subjects. Accepted engineering outcomes and their applicable rationale must be incorporated into canonical Designs; understanding the current model must not require dereferencing private database history. Current operational projections and retained historical assessments remain distinguishable.

### Durability, adoption and historical continuity

A repository without the local database must remain understandable, buildable and capable of validating its current engineering definition. It must not claim that unavailable operational history is empty, or that missing review evidence proves readiness. Operational resumption and evidence-dependent assessment require access to the applicable records or an explicitly restored/imported package.

Backup and restoration must preserve project association, supported storage version, record relationships and retained artifact identities. Transfer supports another local environment without promising automatic database merging or distributed synchronization. Retention may remove disposable payloads under an explicit policy, but must preserve evidence required for ongoing work or current reliance.

Migrate supported current records through an explicit adoption process, preserving IDs, subject identities and provenance without renewing old judgments. Unsupported historical records remain archival evidence with explicit disposition of active dependencies. The [Constitution's cleanup policy](../../CONSTITUTION.md#repository-cleanup-and-historical-retention) permits recoverable Git history for retired committed material; an external archive is needed where that does not preserve required content, including uncommitted originals. No wholesale historical conversion or deletion is authorized by this proposal.

Retire `docs/changes/` as an operational store only after its active responsibilities and consumers have supported replacements. Do not retain permanent dual-write stores or automatic fallback to obsolete runtime formats. Current links and explanations must resolve through current owners or identify recoverable historical sources, rather than require private local history merely to understand the repository.

## Feasibility

Assessment: credible enough for Design, with substantial migration and consumer-reconciliation work. Current [Records](../design/cli/records.md) already separates Changes, reviews, evidence and decisions conceptually, while [CLI](../design/cli/cli.md) owns inspection and safe persistence. These responsibilities support changing the storage realization without moving semantic judgment into the tool. The assessment uses owning contracts directly, not an assumption that the project map is current.

SQLite provides a supported [online database backup mechanism](https://www.sqlite.org/backup.html), but a database snapshot alone does not preserve external artifact payloads. Design must settle supported runtime/library packaging, concurrent-writer and stale-read behavior, crash boundaries between records and artifacts, version migration, coherent backups, retention and restoration. Transactional database writes alone do not prove those composed outcomes. This proposal makes no performance or implementation-parity claim.

The declared operating assumption is one local checkout and user with multiple local agents. Git is this repository's engineering-definition store, not a new mandatory dependency for every customer project; the Constitution retains optional Git integration. Branch changes and imported history must not make evidence apply to different subjects automatically. CI and external reviewers need an explicit way to receive required evidence when it is absent from a clone.

No conceptual blocker to Design has been identified. Unresolved data loss, active recovery dependencies, unavailable evidence for required gates, or an unsupported runtime packaging choice would block adoption until resolved. The prior `workflow-context` attempt in this conversation returned `RL_CLI_INTERNAL`; no governed Change identity or approval state is inferred from it. This isolated draft does not rely on that discovery succeeding.

## Impact and major trade-offs

Operational history will no longer travel automatically with Git clone, branch or pull-request operations. Users gain a smaller current repository and structured local inspection, but backup and explicit transfer become essential to the product's promise of durable work. A database and its backups require more care than disposable local caches. Losing the only copy would lose history even while the engineering definition survives.

The change preserves the vision's traceability and reviewability commitments while changing how users obtain the evidence. It does not narrow the product's broader audience to local-only teams or promise distributed collaboration. Human-readable views and export must keep local records inspectable; new private storage must not hide decision rationale required by the current model.

This direction replaces current file-location requirements and affects governance references, skills, discovery, validators, packaging and evidence consumers. Required independent review, final Verify, explicit actor ownership and external-action permissions remain intact. Simplification is an expected architectural benefit, not a demonstrated reduction in code or maintenance cost.

## Decision requested

Approve refinement of existing REM IR-003 and IR-008, reusing IR-001, IR-002 and IR-004 where their obligations already apply, and select project-local SQLite with a separate artifact store as the proposed replacement for repository-file operational storage. Keep the current engineering definition and applicable rationale in repository files, and make backup/restore, project association, bounded inspection and safe migration required parts of adoption.

Accept the existing-IR analysis above: no new IR is currently justified. Preserve existing IR identities, explicitly extend the operational backup and restoration scope, reconcile affected SR/AR obligations and retain predecessor proposals as historical direction. The proposal remains separate from the IR entities; neither this draft nor storage migration changes their approval or satisfaction status.

The next stage is independent Proposal Review, with particular attention to history portability, evidence access, preservation and migration scope. Approval selects the direction for Design; it does not approve a database schema, exact command interface, implementation plan, data migration, deletion of `docs/changes/`, activation or release.
