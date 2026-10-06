# Skills and commands composition

[MOD-018](module.json) owns the cooperation of capability guidance, command admission and operational persistence. This is proposed composition for SR-079–083, not a new workflow submodel or adopted runtime contract. Direct entities and their realization facets retain their authority; [Governance](../MOD-017-engineering-governance/README.md) owns gate and adoption semantics.

## Authoring, assessment and handoff protocol

Each handoff identifies the requested scope, current subject set, governing requirement/design basis, unresolved findings, relevant evidence and responsible next owner. An absent item is either explicitly inapplicable or an identified gap. It is not synthesized from a stage label.

| Activity | Owned result | Reliance condition and next owner |
| --- | --- | --- |
| Requirement Analysis | RR interpretation; IR/SR reuse/refinement/creation; stakeholder Feature/Scenario analysis | Independent Requirement Review assesses the exact proposed basis, including justified reuse. |
| Requirement Review | Scoped requirement judgment and findings | Accepted basis permits authorized System/Architecture Design; Function/AR completion is not required here. |
| System Design | Logical behavior and Feature/SR–Function relationships | Work iterates with Architecture Design; changed stakeholder obligations return upstream. |
| Architecture Design | Accountable Modules, Interfaces, realization and ARs | One integrated Design Review assesses the complete affected design composition. |
| Design Review | Integrated judgment and correction ownership | Planning relies on the accepted design. Missing architectural responsibility cannot become a delivery task. |
| Plan and Delivery Review | Delivery intent, sequencing, dependencies and proof allocation; reviewed adequacy | Authorized implementation begins only with an applicable delivery basis. |
| Implement | Actual work, required checks, blockers and remaining scope | Eligible milestones continue; full implementation readiness requests one whole-change gate. |
| Code Review, advisory scope | Attributable feedback on explicitly selected interim subjects | No lifecycle approval. Material defects still require correction or disposition. |
| Code Review, whole-change scope | Exact complete candidate, governing basis, judgment and findings | Corrections return to owners and reassessment remains in the same gate. Applicable approval permits distinct Verify. |
| Verify | Current criterion support and scoped completion conclusion | Engineering defects return to their owners; evidence-only retries repeat affected verification without inventing a new review gate. Optional PR retains separate authority. |

Stage validity, artifact completeness, approval applicability, execution authority and recorded persistence outcome are separate predicates. FUNC-054 composes them; the CLI supplies observations and accepts explicit decisions without becoming a semantic router. Missing or unknown stage/scope values must reject before consistency inference. Concrete closed vocabularies and literal operation schemas belong to the replacement CLI/Records contract and require negative tests during implementation.

## Current handoff composition

SR-006 owns the seven-section resumption outcome. MOD-006 interprets current work and authority; MOD-007 owns assessment semantics; MOD-010 assembles context and admits explicit task updates; MOD-011 publishes one coherent current state. The handoff is a projection of these facts, not a new subsystem or editable duplicate. Keep the latest relevant evidence, unresolved issues and important rationale. Replace comparable working summaries, compact superseded detail after current reliance is resolved, and retain selected attachments only where their bytes help decisions.

Preserve attribution, review scope and assessed support still relied upon. Replacing evidence cannot silently transfer approval to a new basis. Reassessment can replace a current assessment within the same gate without a permanent attempt chain. Safe revisions, SQLite transactions and attachment coordination remain necessary even though activity history is optional.

## Operational preservation and resumption

[Work record storage](modules/MOD-011-operational-record-persistence/README.md#database-schema-backup-and-migration) owns SR-074–077 through existing AR-052–055 and FUNC-074–076. MOD-012 submits explicit authorized maintenance through MOD-018-provided IF-004; MOD-010 admits requests and consumes MOD-011-provided IF-003. Backup, same-project transfer and qualified migration preserve finite retained scope and original meaning. After activation, the same current-context path returns retained facts to Governance for resumption, authority and support interpretation. A maintenance receipt supplies actual effects without approving engineering work or adopting workflow policy.

## Recording cooperation

Governance owns engineering meaning, including work context and supplied judgments; persistence owns coherent storage and recovery. This distinction does not create two authored copies. Governance responses reference the same operational facts and subject identities that the caller read. The participant doing a review makes the judgment; MOD-012 applies the review method, MOD-007 supplies common assurance interpretation, and MOD-011 persists the explicitly supplied result when required.

The successor [v4 record specification](modules/MOD-011-operational-record-persistence/README.md) is owned by MOD-011; MOD-010 owns the [v2 command interface](modules/MOD-010-engineering-command-interface/README.md). The successor implements the ordinary operational tasks under those current contracts. The executing package's help and capabilities identify actual availability; installing it does not adopt customer policy or migrate earlier work. Browser generation and subject-history queries retain their separately proposed contracts and qualification prerequisites. [Parent-owned test design](test-design.md) covers handoff and assurance interactions; actual execution results belong outside the current design.

### Interface ownership

| Boundary | Owner and responsibility |
| --- | --- |
| Skill or engineer → CLI, IF-004 | MOD-012 supplies procedure; the actor supplies meaning and authority. MOD-010 owns command syntax, bounded stdin envelopes, public results and diagnostics. |
| CLI → store, IF-003 | MOD-010 normalizes the task; MOD-011 takes closed typed requests and returns current facts and actual outcomes. SQL, connection handles and arbitrary callbacks do not cross this v4 request boundary. |
| Store → SQLite and attachments | MOD-011 alone owns database transactions, query/schema mapping, connection admission and payload publication. SQLite is its embedded mechanism. |
| Receipt preparation | A shared pure MOD-010-owned codec establishes bounded output readiness before commitment; it has no storage authority. Actual outcome still governs the emitted receipt. |

[IF-004](../../interfaces/IF-004-scoped-public-command-execution/interface.json) and [IF-003](../../interfaces/IF-003-operational-record-access-and-publication/interface.json) distinguish current v4 tasks, version-qualified v3 file-candidate/recovery operations in explicitly retained prior executables, and separately proposed extensions. The successor has no fallback v3 dispatcher or writer. The [public schema and outcomes](modules/MOD-010-engineering-command-interface/README.md#public-request-and-result-schema) and [typed boundary](modules/MOD-011-operational-record-persistence/README.md#typed-cli-to-storage-boundary) hold their respective field contracts. Skills need the supported CLI contract and opaque revisions, not SQL or database schema knowledge.

## Task-oriented public interaction

The current CLI task surface includes change create/context/update/complete, review prepare/show/record, verification show/record, store backup/restore/migrate, and parameterized skill installation. Browser generate/check/recover and subject-history selection are separate proposed capabilities, not advertised current operations. These are task boundaries, not one command per stored kind. One milestone progress update can carry its work, actual checks, decisions and blockers while persistence constructs their identities and links coherently in SQLite. Engineering definitions and applicable design rationale stay in Git; operational decisions reference those owners rather than copying the design. Review and Verify remain separate actor-owned assessments. A read or save never supplies a semantic routing decision. Successful final Verify supplies the completion assessment; an authorized change complete records closeout against that exact result. Completed accounts are historical and stop tracking repository applicability. Later regressions start linked new work; an error in an original account can receive an explicit note.

[The CLI owner](modules/MOD-010-engineering-command-interface/README.md#walkthroughs-and-acceptance-intent) owns the end-to-end walkthroughs and retired-command disposition. [Records](modules/MOD-011-operational-record-persistence/README.md#current-records) preserves the supporting facts regardless of how many public operations expose them. Existing requirements and Functions are reused; consolidation changes interaction design rather than introducing another engineering model or authority owner.

## Process projection boundary

### Record a handoff update

This target sequence follows one browser Change: the agent reports completed navigation work, passing checks, an explicitly resolved blocker and one selected report. The agent supplies engineering facts; command handling admits the request; MOD-011 coordinates selected files and one SQLite transaction. The database is an embedded mechanism inside MOD-011, not another REM Module or service. Without an attachment, omit capture/publication; the database commit boundary is unchanged.

<!-- architecture-diagram: record-handoff-update -->

```d2
shape: sequence_diagram
agent: "Engineering agent"
cli: "Command handling\nMOD-010"
store: "Work record storage\nMOD-011"
db: "Embedded SQLite"
agent -> cli: "change update: progress, checks, disposition and selected report"
cli -> store: "Validate input and submit expected revision"
store -> store: "Capture optional report into owned staging"
store -> db: "Begin immediate transaction; read current Change"
db -> store: "Return consistent state and revision"
store -> store: "Check revision, build candidate and validate support"
store -> store: "Publish selected attachment without overwriting retained bytes"
store -> db: "Write related records, dependencies and next revision"
store -> store: "Check external observations and receipt readiness"
store -> db: "Commit the coherent update"
db -> store: "Confirm commitment"
store -> store: "Recheck declared external basis; preserve saved outcome and any drift"
store -> cli: "Return actual committed revision and changed accounts"
cli -> agent: "Report saved state; no approval is implied"
```

SQLite commits the related records together. The attachment file is outside that transaction: it must be safely available before its reference commits, while a rolled-back record update may leave an unused copy. Explicit cleanup rechecks current use under writer exclusion; it never deletes an in-flight publication. Stale revisions or failed checks abort the database transaction rather than partially updating the handoff. Opening after interruption establishes coherent database state or reports unavailability; no application-managed record-file restoration is needed.

The [transaction states](modules/MOD-011-operational-record-persistence/README.md#transaction-states) explain commitment and uncertain caller outcomes. The older generated Publication and Recovery flowcharts remain qualified observations of the supported v3 implementation. They are not the target SQLite algorithm.

### Record a review assessment

The [complete request/result walkthrough](modules/MOD-010-engineering-command-interface/README.md#review-recording-walkthrough) starts with prepared whole-change input and an independent reviewer's explicit judgment. Recording does not conduct the review, erase omitted findings or approve a revised basis on the reviewer's behalf. The v4 sequence separates task admission, storage semantics and public receipt preparation.

<!-- architecture-diagram: record-review-assessment -->

```d2
shape: sequence_diagram
reviewer: "Reviewer"
cli: "Command handling\nMOD-010"
store: "Work record storage\nMOD-011"
db: "Embedded SQLite"
reviewer -> cli: "review record: judgment, support and applicability"
cli -> cli: "Validate bounded stdin envelope and task fields"
cli -> store: "Execute typed task with expected Change revision"
store -> db: "Begin transaction; read current records and revision"
db -> store: "Return coherent current state"
store -> store: "Check revision; preserve issues; validate support"
store -> cli: "Prepare bounded receipt with shared pure codec"
cli -> store: "Receipt ready; no approval or commit is inferred"
store -> db: "Write Review, selections and revision; commit"
db -> store: "Confirm commitment"
store -> store: "Recheck declared external basis; preserve saved outcome and any drift"
store -> cli: "Return actual typed outcome and committed revision"
cli -> reviewer: "Saved means persisted; final Verify remains separate"
```

A rejection before commitment leaves the prior records authoritative. Receipt preparation is a pure in-process call, not reentry into CLI dispatch or an actor-supplied callback. If response delivery fails after commitment, follow the current-context inspection below. Unknown effects remain unknown until inspection; do not label them a clean rejection or repeat the old intent automatically.

### Discover a saved update after a lost response

This path assumes the update committed, but the response did not reach the caller. The caller does not know whether the write succeeded. A new read supplies current facts rather than replaying the old request.

<!-- architecture-diagram: discover-saved-update -->

```d2
shape: sequence_diagram
agent: "Engineering agent"
cli: "Command handling\nMOD-010"
store: "Work record storage\nMOD-011"
store -> cli: "Committed update and revision"
cli -> cli: "Response delivery fails"
agent -> cli: "change context: inspect before retrying"
cli -> store: "Read the coherent current Change"
store -> cli: "Return current facts, revision and explicit limitations"
cli -> agent: "Show saved progress, evidence and issue disposition"
agent -> agent: "Reconcile intended update with current facts"
```

When the inspected current account already satisfies the intended update, no resubmission is needed. If another agent has since changed it, reconcile with that newer state; do not replay old mutable intent or infer a permanent operation receipt from matching IDs. If commitment or storage availability remains uncertain, opening SQLite follows the [storage-owned inspection sequence](modules/MOD-011-operational-record-persistence/README.md#inspect-after-an-interrupted-update). A coherent current snapshot is not a permanent receipt for the earlier request. A lost response alone never authorizes rollback or backup restoration.

The [Process projection contract](../../../support/README.md#process-projection-refinement) distinguishes authored interaction detail from the projected runtime topology. Operations owns the composed handoff conditions; Governance retains gate meaning and the accountable Module/Interface facets retain execution facts. Actor roles and skills do not imply separate runtime processes. The D2 sequences above are registered from this owning source into the existing browser; they do not require the deferred structured activity projection extension. Customer generation and publication are addressed by the [proposed browser composition](../../README.md#customer-architecture-browser-composition). Diagram availability does not claim implemented workflow support.

## Selected subject history

[The owning history contract](modules/MOD-011-operational-record-persistence/history-selection.md) defines SR-078 through FUNC-077 and AR-086/087. MOD-018 composes command admission and storage selection, with existing ordinary query contracts intact. SCN-074 supplies the stakeholder walkthrough without promoting its draft lifecycle.

<!-- architecture-diagram: select-subject-history -->

```d2
shape: sequence_diagram
actor: "Reviewer"
cli: "Command handling\nMOD-010 / IF-004"
store: "Work record storage\nMOD-011 / IF-003"
db: "Existing qualified\nSQLite history"
actor -> cli: "Project, recorded subject, scope, filters and page bound"
cli -> cli: "Admit separate history profile and normalize exact selection"
cli -> store: "Typed read-only history request"
store -> db: "Read state, coverage, associations and facts in one snapshot"
db -> store: "Original identities and retained scope or explicit unavailability"
store -> store: "Match literal facts; order whole units; bind next cursor"
store -> cli: "State-bound page, provenance and completeness limits"
cli -> actor: "Bounded complete outcome; no current approval inferred"
actor -> cli: "Same selection and continuation"
cli -> store: "Normalized selection with opaque continuation"
store -> db: "Read current activation and generation in new snapshot"
db -> store: "Same state or changed history"
store -> cli: "Next deterministic page or conflict with no page units"
cli -> actor: "Preserve result; changed state requires a fresh request"
```

The database, history generation and protected cursor key remain inside MOD-011. Writer/maintenance qualification must establish that every relevant mutation invalidates prior continuation. A read cannot backfill identities, initialize a store or perform recovery. Exhaustion and retained-scope completeness are distinct; absent or partially retained history is not an empty complete past. Installed command availability remains separate from this target Process view.
