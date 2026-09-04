<!-- Template: spec-skeleton-v1; Skill: spec; Template status: normative -->

# Compact Current-State Change Record

## Owning change record

`docs/changes/2026-09-03-compact-current-state-change-record/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

- `docs/proposals/2026-09-03-compact-current-state-change-record.md`
- `docs/architecture/2026-09-03-compact-current-state-change-record.md`
- `docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md`

## Goal and context

RigorLoop MUST make the current effective state of a governed change directly resumable from a bounded authoritative working set. Current lifecycle coordination, review judgments, open findings, materially constraining decisions, applicable evidence, blockers, remaining work, and final readiness MUST remain available without Git history, pull-request history, committed command requests, transport receipts, machine-local logs, or superseded review rounds.

This contract replaces procedural accumulation with current-state replacement. It preserves every consequence still needed to continue or justify the change and permits non-material superseded procedure to disappear. The CLI owns validation, concurrency, coordinated persistence, recovery, and projection. Stage owners and reviewers continue to own semantic content and decisions.

## Glossary

| Term | Meaning |
| --- | --- |
| Compact change | A change explicitly governed by the compact current-state lifecycle contract. |
| Authoritative current set | The applicable compact files plus referenced canonical engineering artifacts whose current identities determine governed behavior. |
| Current review record | The single stable record containing the latest authoritative judgment for one review target. |
| Material decision | A resolved decision whose rationale still constrains requirements, architecture, authority, security, compatibility, accepted risk, implementation, or verification. |
| Current evidence basis | Evidence entries presently eligible to support review, progression, or final verification. |
| Promotion | Retaining a continuing consequence in its durable current owner before replacing or removing its prior record. |
| Semantic operation | Structured intent supplied transiently to the CLI; it is not itself governed evidence. |
| Responsibility metadata | Owner, reviewer, and producer labels that record workflow responsibility or provenance; they do not authenticate a caller or grant filesystem permission. |
| Observable atomicity | Readers observe the complete prior set or complete resulting set and fail closed while recovery is unresolved. |

## Examples first

Example E1: resume on a fresh machine

Given a compact change with two open findings, one material decision, and three current evidence entries, when a developer requests the current context on a fresh checkout with no local logs or pull-request access, then the projection identifies the current stage, authoritative artifact and review paths, both findings, the decision reference, the evidence and freshness states, blockers, remaining work, and permitted operations.

Example E2: replace a review safely

Given a stable review record with one open finding, when a later review candidate omits that finding without a valid final disposition, then the mutation fails unchanged. When the finding is resolved as materially constraining and the same transaction adds a valid material decision, the replacement may succeed.

Example E3: reject stale proof

Given current passing evidence bound to a specification identity, when that specification identity changes, then the same accepted mutation removes that evidence from the current readiness basis or marks it stale and exposes the required rerun. A timestamp, unchanged command string, or prior pull-request check cannot keep it current.

Example E4: recover an interrupted write

Given a process interruption after only part of a candidate set was replaced, when any governed reader or writer encounters the change, then it reports recovery required rather than consuming the partial set. An explicit recovery operation restores the exact prior complete set or completes the exact staged candidate without consulting Git or a hosted service.

## Requirements

### Authoritative record and retention

| ID | Requirement |
| --- | --- |
| SR-01 | A compact change MUST declare one closed, versioned lifecycle-contract identity. Readers and writers MUST select compact behavior from that identity and MUST NOT infer it from file presence or directory shape. |
| SR-02 | The authoritative current set MUST consist only of applicable instances of `change.yaml`, stable current review records, `material-decisions.md`, `evidence.yaml`, and `verify-report.md`, plus current canonical proposal, specification, architecture, ADR, and plan artifacts referenced from `change.yaml`. Optional surfaces MUST be absent when they contain no applicable current information. |
| SR-03 | `change.yaml` MUST own current lifecycle coordination: change identity, contract identity, lifecycle revision, current stage, current canonical artifact identities, current review targets and identities, active milestone or correction, open-finding and evidence references, blockers, remaining work, and readiness state. It MUST NOT retain transition, routing, review-round, request, receipt, evidence-event history, or a caller-maintained permitted-operation list. Permitted operations MUST be derived for projection from the current snapshot. |
| SR-04 | Each datum MUST have exactly one retention class: current authoritative state, material decision memory, current evidence basis, disposable superseded procedure, or optional operational diagnostics. A committed change-local artifact MUST be rejected unless its contents are required by one of the first three classes or are the successful final Verify report. |
| SR-05 | Successful operation requests, transport receipts, routine correction route or return files, routine authoring evidence, `review-log.md`, broad review-resolution ledgers, correction histories, workflow histories, and raw command output MUST NOT be required or treated as authoritative for a compact change. Implementations MUST support requests supplied without adding them to the governed working set. |
| SR-06 | Replacing or removing a current record MUST preserve every continuing consequence needed to identify current state, an open finding, a material decision, current evidence, a blocker, remaining work, or final readiness. If preservation cannot be established, the operation MUST fail unchanged. |

### Stable reviews, findings, and decisions

| ID | Requirement |
| --- | --- |
| SR-07 | A review target MUST have at most one current stable path: `reviews/proposal-review.md`, `reviews/design-review.md`, `reviews/delivery-review.md`, `reviews/code-review-<milestone-id>.md`, or `reviews/code-review-final.md`. A later round MUST replace the same target path rather than create a round-suffixed current record. |
| SR-08 | A current review record MUST expose its schema version, review ID, target, current round, reviewed subject identities, reviewer responsibility label (`reviewer_authority` for v1 compatibility), judgment, recording status, open findings, material-decision references, current limitations, and recorded-at metadata. Judgment MUST express only `clear`, `findings-open`, or `blocked`; it MUST NOT represent owner acceptance or stored progression authority. The label records provenance and MUST NOT be interpreted as authentication or permission. Round is informational and MUST NOT be used as freshness proof. |
| SR-09 | Every open finding MUST expose a stable finding ID, affected artifact or implementation surface, severity, blocking effect, current owner, required next action, disposition `open`, and evidence. Open findings MUST be obtainable from the current review projection without reading a prior record. |
| SR-10 | A replacement review MUST carry every prior open finding occurrence forward or include a valid final disposition for that occurrence. Finding identity and disposition MUST be independent of the identity of any containing review or resolution file. The closed disposition vocabulary MUST be `accepted`, `rejected`, `deferred`, or `partially-accepted`; uncertainty MUST remain open rather than being encoded as a final disposition. |
| SR-11 | A resolved finding MUST create or retain a material decision when it changes a governed requirement, architecture invariant, authority, privacy or security boundary, compatibility or migration behavior, accepted limitation or residual risk, non-obvious implementation direction, or downstream verification obligation. The reviewer supplies materiality; the named decision owner MUST explicitly accept the decision before it can satisfy progression. Ambiguous materiality MUST remain an open finding until the responsible owner decides. |
| SR-12 | Each current material decision MUST expose schema version, decision ID, source finding or issue, decision, rationale, affected artifacts or surfaces, decision owner, explicit acceptance `accepted`, applicability `applicable`, and applicable-since identity. Routine clear review MUST NOT create a decision. Removal MUST fail while a current artifact, review, evidence entry, blocker, remaining-work item, or Verify report references the decision. |
| SR-13 | Routine resolved comments MAY disappear when they have a final disposition, are classified non-material by current review input, and have no remaining current reference or effect. The compact contract MUST NOT require reconstruction of their former wording or chronology. |
| SR-47 | Changing an artifact, review, decision, evidence, or container MUST invalidate only current records that declare a typed dependency on the changed identity. It MUST NOT reopen a settled finding occurrence. If current work violates a settled material decision, a reviewer MUST create a new finding ID that references that decision rather than mutate the old occurrence back to open. |

### Current evidence and Verify

| ID | Requirement |
| --- | --- |
| SR-14 | `evidence.yaml` MUST contain only current or explicitly stale evidence still needed to explain a current blocker or required rerun. Each entry MUST expose schema version, evidence ID, verified claims or requirement/verification-group IDs, exact subject paths and identities, method, outcome, covered system or delivery surfaces, freshness, typed invalidating dependencies, producer responsibility label (`producer_authority` for v1 compatibility), and an optional bounded detail location. A dependency MUST resolve to a subject in the same entry or to a current artifact, review, or material decision. The label records provenance and MUST NOT be interpreted as authentication or permission. |
| SR-15 | Evidence freshness MUST derive from direct comparison of each typed dependency with its current identity. A governed read MUST hash only explicitly referenced subject paths and MUST report a bounded drift blocker when a current subject identity no longer matches; it MUST NOT silently mutate the evidence record. A mutation that changes an invalidating dependency MUST, in the same transaction, replace the evidence with valid new evidence, mark it stale with a required rerun, or remove it when it no longer explains current work. Review, progression, and Verify MUST reject while required evidence has unresolved drift. Filenames alone, timestamps, command text, Git ancestry, logs, and caller assertions MUST NOT establish freshness. |
| SR-16 | Raw command output MUST remain outside the governed set by default. A detail location MAY reference CI or another bounded governed source, but current review, progression, and verification MUST remain explainable from evidence metadata when that location is unavailable. Secrets, credentials, unrestricted environment dumps, and unrelated user or host data MUST NOT be recorded. |
| SR-17 | A successful final Verify MUST create or replace one `verify-report.md` in the same transaction that records final readiness. The report MUST identify the exact verified subject and evidence basis, verdict, impact classification, evidence reused and rerun, limitations and residual risks, final explanation, and handoff state. Failed or interrupted Verify MUST NOT leave a successful current report. |
| SR-18 | Any later mutation that invalidates the verified subject, required review, material decision, evidence basis, or remaining-work conclusion MUST remove the Verify report from current readiness or mark final readiness non-current in the same transaction. |

### Minimal CLI boundary

| ID | Requirement |
| --- | --- |
| SR-19 | The public CLI MUST provide three capabilities for compact changes: bounded current-state projection, application of a versioned semantic operation, and explicit recovery or recovery-status handling. Separate convenience commands MAY exist, but MUST delegate to these capabilities and MUST NOT establish competing state semantics. |
| SR-20 | The projection capability MUST support human-readable and JSON output, an optional exact requested operation, and named views for summary, reviews, open findings, material decisions, evidence, remaining work, verification, and a named skill context. Each view MUST derive from the authoritative current set and direct identity observations of only the evidence subjects selected by that view. It MUST return exact paths and identities needed for its question and MUST NOT scan the repository or reconstruct procedural history. |
| SR-21 | A successful skill-context projection MUST include change and lifecycle-contract identity, lifecycle revision, current stage, relevant current artifact and review identities, relevant findings and decisions, relevant evidence and freshness, active milestone or correction, overall progression readiness, progression blockers, remaining work, permitted operations, requested-operation eligibility when one operation is selected, and exact required paths. Progression blockers MUST remain visible but MUST NOT prohibit a requested operation unless an applicable operation-scoped diagnostic also blocks it. A globally blocked change MUST expose a structurally eligible corrective operation as permitted. It MUST omit unrelated current content unless requested by another bounded view. |
| SR-22 | The mutation capability MUST accept a transient, versioned semantic request through arguments, standard input, or a temporary file. The request MUST contain only the operation, target, expected lifecycle revision and relevant prior identities, plus stage-owned semantic content required by that operation. It MUST NOT contain a caller identity, claimed authority, caller-constructed `change.yaml`, derived lifecycle fields, or an arbitrary resulting candidate set. Request location MUST NOT affect semantics, and success MUST NOT require retaining the request. |
| SR-23 | Supported semantic operations MUST cover current artifact registration or revision, stage progression, stable review replacement and settlement, finding disposition and material-decision maintenance, correction route and return, reviewed append-only planned-work extension, milestone progression, evidence update or invalidation, final Verify recording, and the closed implementing-change bootstrap. Unknown operations, responsibility labels, statuses, kinds, fields, or retention classes MUST fail closed before consistency evaluation. |
| SR-24 | The CLI MUST return one result model for human and JSON renderers. Every result MUST identify success, rejection, busy, or recovery-required status; change identity when safely known; prior and resulting lifecycle revisions when applicable; affected paths without secret content; blockers or stable error codes; and whether authoritative bytes changed. Diagnostics MUST NOT become evidence merely because the command succeeded. |
| SR-46 | When current stage is `implement` and no work is active, `advance-milestone` MUST be able to select exactly one pending `milestone` entry from `remaining_work` by ID using `from_status: null` and `to_status: planned`. The evaluator MUST require that entry to be implementation-owned and pending, remove it from `remaining_work`, and derive the new `ActiveMilestone`; it MUST reject missing, blocked, non-milestone, non-implementation, or ambiguous selection unchanged. Closing an exact reviewed milestone MUST clear `active_work`. If another pending milestone remains, the only forward Code Review edge is `code-review → implement`, after which explicit milestone selection is required; otherwise current CI, finding, and remaining-work state selects the existing downstream edge. The request chooses semantic work by current ID but MUST NOT supply an `ActiveMilestone`, ordering claim, status result, or coordinator candidate. |
| SR-49 | After planned work has been initialized, `append-planned-work` MUST be eligible only when a current `clear` Delivery Review covers the exact revised primary Plan and no work is active. The reviewed Plan's previously registered milestones, in their original order, MUST exactly preserve every registered milestone ID, kind, completion contract, and evidence allocation; their current lifecycle states MUST remain unchanged. The operation MAY append only new, unique, implementation-owned milestone entries as one suffix in Plan order, initially `pending`. Rename, deletion, reorder, mutation, reopening, insertion, or an empty suffix MUST reject unchanged. The request MUST bind the exact Plan and Delivery Review identities and name only the proposed suffix; the evaluator MUST derive the coordinator update. Exact replay MAY return `already-applied`; stale or competing extension MUST reject without changing bytes. Before compact activation, this operation MAY also be selected exactly once for change `2026-09-03-compact-current-state-change-record` solely to append its reviewed M6 suffix without changing its lifecycle contract or any M1–M5 state; every other legacy change MUST reject it. That bridge expires when the exact suffix is present. This operation records reviewed delivery intent and does not authenticate a caller or grant permission. |

### Transactions, concurrency, and recovery

| ID | Requirement |
| --- | --- |
| SR-25 | One pure evaluator MUST consume a normalized current snapshot, bounded identity observations, and one semantic request and produce either the only eligible complete candidate transaction or a rejection. It MUST mechanically derive `change.yaml`, cross-record references, progression, readiness, invalidations, projected operation eligibility, serialization, and the resulting lifecycle revision. Ordinary gate progression MUST require a `clear` exact-subject review judgment, no blocking findings, every required accepted material decision, current required evidence, and the applicable transition rule; it MUST NOT require or store a duplicate approval outcome. The evaluator MUST perform no filesystem, Git, network, logging, workflow-choice, review, or validation-command execution and MUST NOT invent stage-owned semantic content or materiality. |
| SR-26 | Every mutation MUST bind the expected lifecycle revision and exact identity or expected absence of every authoritative file it reads, replaces, creates, or removes, plus every evidence-subject path observed for the decision. Missing, extra, stale, contradictory, escaped, or unsafe identities and paths MUST reject without authoritative modification. One resulting lifecycle revision MUST cover every current authoritative record that can affect routing, review, evidence, or readiness and MUST be used only for optimistic concurrency; it MUST NOT imply that every current record semantically depends on every other record. Semantic invalidation MUST follow only declared typed dependencies. Observed subject paths remain bounded freshness inputs rather than governed record files. |
| SR-27 | At most one writer MAY operate on a compact change at a time. A live competing writer MUST receive a bounded busy result. Of two requests based on the same lifecycle revision, at most one may succeed; the other MUST reject stale without modifying authoritative files. |
| SR-28 | A multi-file mutation MUST provide observable atomicity through an exclusive change lock, same-filesystem candidate staging, durable recovery data for exact prior and candidate states, deterministic replacement, complete-set validation, read-back, and cleanup or restoration before unlocking. Unaffected authoritative files MUST retain identical bytes. |
| SR-29 | Every governed reader and writer MUST detect an active transaction or unresolved recovery state before consuming authoritative content. It MUST return busy or recovery-required and MUST NOT project, review, advance, or verify a possibly partial set. |
| SR-30 | Recovery MUST be deterministic from the private transaction data and current file identities alone. It MUST restore the exact prior complete set or complete the exact candidate set; ambiguity, tampering, missing recovery content, or identity mismatch MUST fail closed for explicit operator intervention. Recovery MUST NOT use Git, pull-request data, local command logs, or network access. |
| SR-31 | An identical retry after a reported or uncertain success MUST reread the complete current basis. It MAY return `already-applied` only when the semantic result, candidate identities, and resulting invariants exactly match; otherwise it MUST reject stale or conflicting without a second mutation. |

### Responsibility, local trust, compatibility, and activation

| ID | Requirement |
| --- | --- |
| SR-32 | Semantic responsibility MUST remain stage-scoped: authors supply canonical artifact content, independent reviewers supply judgments and finding materiality, named decision owners explicitly accept material decisions, route supplies lifecycle direction, and Verify supplies final readiness. The CLI MUST derive whether an operation is structurally eligible from current state and MUST validate responsibility metadata for consistency, but it MUST NOT authenticate a caller, treat metadata as permission, or choose judgments, routes, decisions, acceptance, or evidence sufficiency. Operating-system, sandbox, or enclosing-runner controls—not this record contract—govern who can execute the CLI or edit repository files. |
| SR-33 | Compact paths, request paths, detail references, lock data, and recovery data MUST be repository-contained or use an explicitly allowed machine-local state root. Path traversal, symlink escape, unsupported file kinds, oversized bounded fields, and secret-bearing diagnostic fields MUST reject or be redacted before persistence or rendering. |
| SR-34 | Completed historical changes MUST remain readable under their recorded lifecycle contract and MUST be denied compact writes. An ordinary legacy change already in flight when compact v1 activates MUST finish under its registered contract. Compact v1 MUST NOT provide automatic, inferred, or in-place legacy migration. |
| SR-35 | Compact writing MUST activate only when the canonical governance, workflow specification, architecture and ADR, skills and assets, schemas, validators, CLI and package, fixtures, contributor guidance, and all supported adapter outputs declare one compatible contract version. A mixed or unknown writer set MUST withhold activation. |
| SR-36 | Rollback MUST stop new compact writers without rewriting completed compact changes. Readers for every released compact contract MUST remain able to project its authoritative current set, and rollback MUST NOT depend on reconstructing discarded procedure. |
| SR-48 | Before compact writers activate, `bootstrap-closeout` MUST be eligible only for change `2026-09-03-compact-current-state-change-record` and MUST NOT change its lifecycle-contract discriminator or file shape. Its exact-current-set input MUST bind the current proposal, architecture, applicable ADR, specification, plan, complete planned-work set, implementation surfaces, latest applicable review judgments, current evidence basis, lifecycle revision, and activation manifest. Validation MUST consider only current consequential state, MUST require no active or pending planned work, and MUST treat individually settled superseded finding occurrences as closed even if a legacy aggregate container identity changed. For the implementing change's exact current legacy final-review record only, the bootstrap reader MUST derive `clear` when the review completed independently against the exact bootstrap subject and records no open blocking finding; the legacy outcome label neither grants clearance by itself nor becomes compact vocabulary. Missing input, identity drift, unfinished planned work, a current open blocker, stale required evidence, a non-clear exact-subject final review, failed Verify, or incoherent activation MUST reject unchanged. Successful final closeout and compact-writer activation MUST occur in one recoverable transaction without Git, branch, diff, pull-request, hosted-service, or local-log identity. The operation MUST expire after that exact activation and MUST reject every other change; it is not migration or a general validation bypass. |

### Serialization and durability

| ID | Requirement |
| --- | --- |
| SR-37 | Every compact surface and CLI envelope MUST declare exactly one schema identity from `compact-change-v1`, `compact-review-v1`, `compact-decisions-v1`, `compact-evidence-v1`, `compact-verify-v1`, `compact-operation-v1`, `compact-result-v1`, or `compact-recovery-v1`. Unknown, absent, duplicated, or mismatched schema identities MUST fail closed. |
| SR-38 | `change.yaml` and `evidence.yaml` MUST be UTF-8 YAML mappings in the supported safe YAML 1.2 subset. Current review records, `material-decisions.md`, and `verify-report.md` MUST begin with one UTF-8 YAML front matter mapping delimited by `---`; that mapping is the sole machine authority and following Markdown is explanatory only and MUST NOT contradict it. Duplicate keys, aliases, custom tags, merge keys, multiple documents, non-string mapping keys, and non-finite numbers MUST reject. |
| SR-39 | The top-level and entry shapes in the Compact schema tables are normative. Undeclared fields MUST reject unless the containing schema explicitly names an `extensions` mapping; v1 schemas define no such mapping. Required collections MAY be empty only where their table permits an applicable empty state. All IDs and repository paths MUST be unique within their declared scope. |
| SR-40 | The lifecycle revision MUST be `sha256` of the exact Lifecycle revision manifest defined below. The coordinator identity MUST hash the exact `change.yaml` bytes after byte-replacing only the required plain-style `lifecycle_revision` value with the 71-byte ASCII sentinel `sha256:` followed by 64 zeroes; quoted, tagged, folded, or otherwise styled values MUST reject. No other coordinator byte may be normalized. The manifest MUST use the exact keys and row shape below, lexicographically sorted object keys and file rows, `,` and `:` separators without insignificant whitespace, UTF-8 encoding, and exactly one trailing LF. |
| SR-41 | A transient semantic request MUST use `compact-operation-v1` and contain only `schema`, `operation`, `change_id`, `expected_lifecycle_revision`, `expected_files`, and `payload`. `expected_files` MUST bind every read or affected path to its expected absence or SHA-256 byte identity. A result MUST use `compact-result-v1` and contain the common SR-24 fields using the closed status vocabulary `success`, `already-applied`, `rejected`, `busy`, or `recovery-required`. |
| SR-42 | The stable review, decision, evidence, Verify, and change schemas MUST use the required fields and closed vocabularies in the Compact schema tables. Human prose MAY elaborate evidence and rationale but MUST NOT supply a field required for mutation, projection, recovery, review, progression, or verification. |
| SR-43 | Transaction-private state MUST live under repository-local `.rigorloop/transactions/<change-id>/` on the same filesystem as the governed files. It MUST contain one exclusive `lock` and, after preparation, one `recovery.yaml` plus complete `prior/` and `candidate/` content for every affected path. The transaction directory and files MUST be excluded from governed artifacts and version-control selection. On platforms that expose owner permissions they MUST use directory mode `0700` and file mode `0600`; an adapter unable to provide equivalently private access MUST reject before preparation. |
| SR-44 | `compact-recovery-v1` MUST use phases `prepared`, `replacing`, or `persisted` and bind transaction ID, change ID, prior and candidate lifecycle revisions, ordered affected paths, prior and candidate identities, and content locations. Recovery MUST discard an untouched `prepared` candidate, restore the complete prior set from any valid mixed `replacing` state, accept and clean a fully validated candidate in `persisted`, and return recovery-required for every unknown, missing, contradictory, or tampered state. |
| SR-45 | A request body MUST be at most 1 MiB, each authoritative compact file at most 8 MiB, and the combined prior plus candidate content of one transaction at most 64 MiB; excess MUST reject before authoritative replacement with `RL_LIMIT_EXCEEDED`. A mutation MUST report success only after candidate files and recovery metadata have been flushed, replacements have completed, the resulting set and lifecycle revision have read back correctly, every affected file and parent-directory durability barrier has completed, recovery content has been removed, and the transaction-directory removal has been durably synchronized. A platform without the required file and directory durability primitives MUST reject mutation as unsupported before replacement. |

## Important scenarios

| Scenario | Governing requirements | Required outcome |
| --- | --- | --- |
| New compact change | SR-01–SR-06, SR-35 | Only applicable current surfaces are created; no empty decision, evidence, review, or Verify file is required. |
| Clean rereview | SR-07–SR-13 | The stable review path is replaced, current round and subject change, and no round-suffixed record or empty resolution ledger is created. |
| Finding remains open | SR-09–SR-10, SR-26 | It remains visible with owner, next action, evidence, and blocking effect or the transaction fails unchanged. |
| Material resolution | SR-10–SR-12 | Review disposition and decision memory become current together. |
| Non-material resolution | SR-10, SR-13 | The final disposition is validated, then superseded detail may disappear. |
| Settled finding after document change | SR-10, SR-15, SR-26, SR-47 | The settled occurrence stays closed; only declared dependent judgment or evidence becomes non-current, and a real recurrence receives a new finding ID linked to the decision. |
| Artifact changes | SR-14–SR-15, SR-18 | Dependent evidence and final readiness become non-current in the same transaction. |
| Concurrent stable-review writers | SR-26–SR-28 | Exactly one candidate becomes authoritative and the stale candidate changes no bytes. |
| Crash at each replacement boundary | SR-28–SR-30 | Readers block until exact restoration or completion; no partial state is accepted. |
| Missing local logs and PR host | SR-19–SR-24, SR-30 | Projection, mutation, recovery, review, and Verify retain their defined behavior. |
| Historical legacy change | SR-34 | It remains readable and unchanged; compact-only operations reject. |
| Ordinary in-flight legacy change | SR-34–SR-35 | It continues under its registered contract; compact-only operations reject and no migration is inferred or offered by compact v1. |
| Implementing-change bootstrap | SR-23, SR-35, SR-48 | Only the named implementing change can bind its exact current consequential set; clear final review, passing Verify, and coherent activation close and activate atomically without migration or Git/PR identity. |
| Invalid or oversized compact data | SR-37–SR-39, SR-45 | Validation rejects before replacement with a stable schema, vocabulary, path, or limit error. |
| Whole-set identity check | SR-40–SR-42 | Independent implementations produce the same lifecycle revision for identical authoritative bytes and a different revision for every relevant byte change. |
| Prepared, mixed, and persisted recovery | SR-43–SR-45 | The fixed recovery state machine discards an untouched candidate, restores prior bytes from a mixed state, accepts an exact persisted candidate, and blocks on ambiguity. |
| First and next milestone selection | SR-23, SR-25–SR-27, SR-46 | At `implement` with no active work, one exact pending implementation milestone moves from `remaining_work` to derived planned active work; missing, blocked, wrong-kind, wrong-owner, stale, duplicate, or caller-constructed alternatives reject unchanged. |
| Reviewed Plan extension | SR-23, SR-25–SR-27, SR-49 | A clear Delivery Review of the exact revised Plan may append new pending suffix milestones while every registered milestone and state remains unchanged; every rewrite, insertion, stale request, or conflicting replay rejects unchanged. |

## Acceptance conditions

- A fresh-machine consumer can answer every resume-contract question from one bounded CLI projection and the exact paths it returns.
- Repeated review and correction rounds do not add current round-suffixed reviews, request files, route receipts, review logs, or resolution ledgers.
- Removing an unresolved finding, a referenced material decision, or current evidence without its required replacement is impossible through supported mutation paths.
- Changing a document or aggregate container cannot reopen a settled finding; a later regression is represented by a new occurrence linked to its applicable decision.
- Subject-changing mutations invalidate dependent evidence and readiness atomically.
- Fault injection at every multi-file persistence boundary never permits a reader to accept a partial current set.
- Current compact behavior and recovery are unchanged when Git metadata, pull-request access, network access, and local diagnostic logs are absent.
- Legacy completed changes remain readable and cannot accidentally acquire compact writer authority.
- The named implementing change can close exactly once through current consequential validation and atomic activation without Git or PR identity; every other legacy change and every stale or incomplete bootstrap attempt rejects unchanged.
- Independently implemented parsers agree on every compact schema, lifecycle revision, limit, recovery phase, and successful-durability point.
- First and subsequent implementation milestones are selectable from bounded current state without plan-prose parsing or caller-constructed active work.
- A reviewed Plan revision can add necessary implementation as a new suffix milestone without rewriting, reopening, or silently mutating completed work.

## Inputs and outputs

The projection input is an exact change identity, view or skill name, optional `requested_operation: Operation`, and output format. The requested operation may be supplied to any named view and selects only the operation-specific eligibility evaluation; it does not broaden that view's current-state content. When it is absent, the projection must set both `requested_operation` and `operation_eligibility` to null. Its output is a bounded result with lifecycle revision, relevant identities, current facts, paths, and stable blockers.

The mutation input is a transient versioned semantic operation containing exact change identity, expected lifecycle revision, operation-specific current identities, and candidate semantic content or content references. It contains no caller identity or permission claim. Its output is the common result model described by SR-24. The request is not an output and has no retention requirement.

The recovery input is an exact change identity plus the expected recovery identity when recovery state exists. Its output identifies whether no recovery was needed, the exact prior set was restored, the exact persisted candidate was accepted, or manual intervention remains required.

## Compact schema tables

Every field below is machine-authoritative. All mappings are closed: an undeclared key rejects. A required field is never omitted. `null` is allowed only where its type explicitly includes `null`. Arrays preserve the stated order and reject duplicate scalar values or duplicate entry IDs. ID-keyed mappings are serialized in lexicographic key order, and each entry's identity field must equal its mapping key.

### Scalar types and workflow vocabulary

| Type | Exact representation |
| --- | --- |
| `Id` | UTF-8 string matching `^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$`. |
| `Text` | Non-empty UTF-8 string of at most 16 KiB after YAML decoding. |
| `Content` | UTF-8 string of at most 8 MiB after decoding; used only for candidate authoritative-file bytes. |
| `Path` | Normalized repository-relative UTF-8 string of at most 1024 bytes using `/`, with no empty, `.`, or `..` segment and no symlink escape. |
| `Digest` | String matching `^sha256:[a-f0-9]{64}$`. |
| `Timestamp` | RFC 3339 UTC string ending in `Z`; informational only. |
| `Stage` | One of `proposal`, `proposal-review`, `architecture`, `spec`, `design-review`, `plan`, `delivery-review`, `implement`, `code-review`, `review-resolution`, `ci-maintenance`, `verify`, or `pr`. |
| `Authority` | A legacy-named responsibility/provenance label: one of the `Stage` values or `workflow`. It is used only in durable owner, reviewer, and producer metadata and never authenticates a caller or grants permission. |
| `Operation` | One of `record-artifact`, `advance-stage`, `replace-review`, `settle-review`, `resolve-finding`, `upsert-decision`, `remove-decision`, `route-correction`, `return-correction`, `append-planned-work`, `advance-milestone`, `update-evidence`, `invalidate-evidence`, `record-verify`, `bootstrap-closeout`, or `recover`. |
| `ArtifactKind` | One of `proposal`, `architecture`, `adr`, `spec`, or `plan`. |
| `ArtifactRole` | One of `primary` or `supporting`. |
| `ArtifactStatus` | One of `authoring`, `review-required`, `accepted`, `active`, `revision-required`, `blocked`, or `superseded`. Review clearance and progression are derived and are not artifact statuses. |
| `ReviewJudgment` | One of `clear`, `findings-open`, or `blocked`. |
| `Severity` | One of `critical`, `major`, `minor`, or `note`. |
| `BlockingEffect` | One of `blocks-progression` or `advisory`. |
| `Disposition` | One of `open`, `accepted`, `rejected`, `deferred`, or `partially-accepted`. |
| `Freshness` | One of `current` or `stale`. |

### Reusable closed records

| Record | Required fields and exact types |
| --- | --- |
| `Subject` | `subject_id: Id`, `path: Path`, `identity: Digest`; the enclosing mapping key equals `subject_id`. |
| `DependencyRef` | `kind: subject | artifact | review | decision`, `id: Id`, `identity: Digest`; `subject` resolves to the same evidence entry's `subjects[id]`, while other kinds resolve to the matching current coordinator reference. Dependency pairs `(kind, id)` are unique and sorted first by `kind`, then `id`. |
| `ArtifactRef` | `artifact_id: Id`, `kind: ArtifactKind`, `role: ArtifactRole`, `path: Path`, `identity: Digest`, `owner: Authority`, `status: ArtifactStatus`. |
| `ReviewRef` | `target_id: Id`, `path: Path`, `identity: Digest`, `review_id: Id`, `judgment: ReviewJudgment`, `reviewer_authority: Authority`, `status: current | review-required | blocked`. |
| `Finding` | `finding_id: Id`, `affected_surfaces: Text[1..*]`, `severity: Severity`, `blocking_effect: BlockingEffect`, `owner: Authority`, `required_next_action: Text`, `disposition: open`, `evidence: Text`. |
| `FindingRef` | `finding_id: Id`, `review_target_id: Id`, `review_path: Path`, `review_identity: Digest`, `owner: Authority`, `severity: Severity`, `blocking_effect: BlockingEffect`. |
| `DecisionRef` | `decision_id: Id`, `path: Path`, `identity: Digest`, `acceptance: accepted`, `applicability: applicable`. |
| `EvidenceRef` | `evidence_id: Id`, `manifest_path: Path`, `manifest_identity: Digest`, `freshness: Freshness`. |
| `Diagnostic` | `code: Id`, `summary: Text`, `invariant: Id`, `scope: progression | operation`, `operation: Operation | null`, `identities: Text[0..*]`, `next_operation: Operation | null`; `progression` requires null `operation`, while `operation` requires a non-null operation. A condition that affects both scopes is represented once in each applicable collection. |
| `OperationEligibility` | `operation: Operation`, `status: permitted | prohibited`, `blockers: Diagnostic[0..*]`; `permitted` requires an empty blocker list and `prohibited` requires at least one operation-scoped diagnostic for that operation. |
| `RemainingWork` | `work_id: Id`, `kind: milestone | task`, `owner: Authority`, `required_action: Text`, `status: pending | blocked`. A selectable milestone has `kind: milestone`, `owner: implement`, and `status: pending`; an active milestone is absent from this mapping until it returns as new required work through another stage-owned operation. |
| `ExpectedFile` | `path: Path`, `state: absent | present`, `identity: Digest | null`; `identity` is required for `present` and must be `null` for `absent`. |
| `ContentInput` | `path: Path`, `identity: Digest`, `source: inline | path`, `content: Content | null`, `source_path: Path | null`; `inline` requires `content` and null `source_path`, while `path` requires null `content` and a `source_path`. The identity MUST match the supplied bytes. Referenced source files are transient inputs and never enter the authoritative set merely by being read. |
| `FindingResolution` | `finding_id: Id`, `disposition: accepted | rejected | deferred | partially-accepted`, `materiality: material | non-material`, `decision_id: Id | null`; `decision_id` is non-null exactly when materiality is `material`. |
| `DetailLocation` | `kind: repository | external | machine-local`, `value: Text`; it is informational and never supplies required current semantics or freshness. |
| `ActiveMilestone` | `kind: milestone`, `milestone_id: Id`, `status: planned | implementing | review-required`, `owner: Authority`. Closed work is not active. |
| `CorrectionInput` | `finding_ids: Id[1..*]`, `source_stage: Stage`, `destination_stage: Stage`, `return_stage: Stage`, `owner: Authority`, `reason: Id`, `return_condition: Text`, `expected_review_target: Id`. This is semantic route intent and contains no durable `kind` or derived `status`. |
| `ActiveCorrection` | `kind: correction`, `finding_ids: Id[1..*]`, `source_stage: Stage`, `destination_stage: Stage`, `return_stage: Stage`, `owner: Authority`, `reason: Id`, `return_condition: Text`, `expected_review_target: Id`, `status: authoring | review-required | blocked`. A new route starts in `authoring`; return changes the same correction to `review-required`; only settlement of its exact required review may clear it. |

### Authoritative surface schemas

| Schema | Required fields and exact container types |
| --- | --- |
| `compact-change-v1` | `schema: compact-change-v1`; `change_id: Id`; `title: Text`; `lifecycle_contract: compact-current-state-v1`; `lifecycle_revision: Digest`; `current_stage: Stage`; `artifacts: mapping<Id, ArtifactRef>`; `reviews: mapping<Id, ReviewRef>`; `active_work: ActiveMilestone | ActiveCorrection | null`; `open_findings: mapping<Id, FindingRef>`; `material_decisions: mapping<Id, DecisionRef>`; `evidence: mapping<Id, EvidenceRef>`; `blockers: Diagnostic[0..*]`; `remaining_work: mapping<Id, RemainingWork>`; `readiness: not-ready | blocked | ready-for-review | verified`. |
| `compact-review-v1` | `schema: compact-review-v1`; `review_id: Id`; `target: {target_id: Id, target_kind: proposal | design-package | delivery-package | milestone | final-code}`; `round: integer >= 1`; `subjects: mapping<Id, Subject>`; `reviewer_authority: proposal-review | design-review | delivery-review | code-review`; `judgment: ReviewJudgment`; `recording_status: recorded | blocked`; `open_findings: mapping<Id, Finding>`; `material_decisions: Id[0..*]`; `limitations: Text[0..*]`; `recorded_at: Timestamp`. `clear` requires no finding with `blocks-progression`; `findings-open` requires at least one open finding; `blocked` records why judgment could not complete and grants no progression. |
| `compact-decisions-v1` | `schema: compact-decisions-v1`; `decisions: mapping<Id, {decision_id: Id, source: {kind: finding | issue, id: Id}, decision: Text, rationale: Text, affected_surfaces: Text[1..*], owner: Authority, acceptance: accepted, applicability: applicable, applicable_since: Digest}>`; the file is absent instead of serializing an empty `decisions` mapping. |
| `compact-evidence-v1` | `schema: compact-evidence-v1`; `evidence: mapping<Id, {evidence_id: Id, verifies: Id[1..*], subjects: mapping<Id, Subject>, method: Text, outcome: passed | failed | inconclusive | not-run, surfaces: Id[1..*], freshness: Freshness, invalidating_dependencies: DependencyRef[1..*], producer_authority: Authority, detail_location: DetailLocation | null, required_rerun: Text | null}>`; every dependency resolves exactly and its identity matches while freshness is `current`; `required_rerun` is non-null exactly when freshness is `stale`; the file is absent instead of serializing an empty `evidence` mapping. |
| `compact-verify-v1` | `schema: compact-verify-v1`; `verification_id: Id`; `subjects: mapping<Id, Subject>`; `verdict: passed`; `impact: low | standard | high | critical`; `evidence_reused: Id[0..*]`; `evidence_rerun: Id[0..*]`; `limitations: Text[0..*]`; `residual_risks: Text[0..*]`; `explanation: Text`; `handoff: ready | ready-with-limitations`; `recorded_at: Timestamp`; every evidence ID resolves to one current entry and the file is absent unless final readiness is current. |

The YAML front matter for `compact-review-v1`, `compact-decisions-v1`, and `compact-verify-v1` contains exactly the fields above. Markdown after the closing delimiter is optional explanatory text and is excluded from semantic field lookup, but its bytes remain part of that file's identity.

### Operation and result schemas

`compact-operation-v1` contains exactly `schema: compact-operation-v1`, `operation: Operation`, `change_id: Id`, `expected_lifecycle_revision: Digest`, `expected_files: mapping<Path, ExpectedFile>`, and `payload: mapping`. The expected-file mapping key must equal each row's `path`. Every authoritative path or evidence-subject path read by evaluation must occur exactly once. Caller identity, role, authority, candidate `change.yaml`, derived lifecycle fields, and arbitrary candidate-file mappings are undeclared and therefore reject.

Each payload contains only the fields in its matching row. Content inputs carry stage-owned bytes; the evaluator derives every coordinator and reference update:

| Operation | Additional required payload fields |
| --- | --- |
| `record-artifact` | `artifact: ArtifactRef`, `content: ContentInput`; both paths and identities must agree. |
| `advance-stage` | `from_stage: Stage`, `to_stage: Stage`. |
| `replace-review` | `target_id: Id`, `prior_review_identity: Digest | null`, `review: ContentInput`, `resolutions: mapping<Id, FindingResolution>`; every omitted prior finding has one resolution and every material resolution has a decision already current or supplied through `resolve-finding`. |
| `settle-review` | `target_id: Id`, `review_id: Id`; the evaluator rereads the exact current review and derives authoring return, blocked review, correction continuation or closure, invalidated downstream gates, and progression from its judgment and current dependencies. |
| `resolve-finding` | `resolution: FindingResolution`, `review: ContentInput`, `decisions: ContentInput | null`; `decisions` is non-null for a newly promoted material decision and the candidate review must omit exactly the resolved finding. |
| `upsert-decision` | `decision_id: Id`, `decisions: ContentInput`. |
| `remove-decision` | `decision_id: Id`; the evaluator removes the optional decision file when its last entry is removed. |
| `route-correction` | `correction: CorrectionInput`; the evaluator constructs the durable `ActiveCorrection` by adding `kind: correction` and `status: authoring`. Caller-supplied `kind`, `status`, or any other derived or undeclared correction field rejects. |
| `return-correction` | `finding_ids: Id[1..*]`, `return_stage: Stage`, `satisfied_condition: Text`. |
| `append-planned-work` | `plan_artifact_id: Id`, `plan_identity: Digest`, `delivery_review_target_id: Id`, `delivery_review_id: Id`, `milestones: RemainingWork[1..*]`; every supplied entry has `kind: milestone`, `owner: implement`, and `status: pending`. |
| `advance-milestone` | `milestone_id: Id`, `from_status: null | planned | implementing | review-required`, `to_status: planned | implementing | review-required | closed`. The only activation pair is `null → planned`; the continuing pairs are `planned → implementing`, `implementing → review-required`, and `review-required → closed`. |
| `update-evidence` | `evidence_ids: Id[1..*]`, `evidence: ContentInput`. |
| `invalidate-evidence` | `evidence_ids: Id[1..*]`, `reason: Text`, `evidence: ContentInput | null`; null is allowed only when all remaining evidence is removed. |
| `record-verify` | `verification_id: Id`, `report: ContentInput`, `evidence_ids: Id[1..*]`. |
| `bootstrap-closeout` | `subjects: mapping<Id, Subject>`, `final_review_target_id: Id`, `final_review_id: Id`, `verification_id: Id`, `activation_manifest: Subject`; allowed only by SR-48, and the evaluator derives the exact-current-set identity and atomic activation result. |
| `recover` | `transaction_id: Id`, `expected_recovery_identity: Digest`, `action: restore-prior | accept-candidate`. |

### Operation eligibility matrix

Except for recovery status, `recover`, SR-49's one preactivation implementing-change `append-planned-work`, and SR-48's one preactivation `bootstrap-closeout`, every operation requires a supported compact contract. Every operation requires no live lock or unresolved recovery, the exact current lifecycle revision, all required expected-file bindings, and a structurally valid set under its selected contract. The two implementing-change operations use the same transient `compact-operation-v1` envelope solely as the closed bridges named by SR-49 and SR-48; they grant no other compact operation to a legacy change and do not change its lifecycle contract. These predicates are the sole source of `Projection.permitted_operations` and `OperationEligibility`; stored or caller-supplied lists, overall readiness, and progression-only blockers grant or deny no operation eligibility.

| Operation | Additional eligibility predicate |
| --- | --- |
| `record-artifact` | The current stage is the artifact kind's authoring stage (`adr` maps to `architecture`), or an active correction names that stage as its destination; the artifact ID and canonical path are absent or match the current registration exactly. |
| `advance-stage` | `from_stage` equals the current stage; `to_stage` is the next edge in `proposal → proposal-review → architecture → spec → design-review → plan → delivery-review → implement → code-review → review-resolution → ci-maintenance → verify → pr`, with `code-review → implement`, `code-review → ci-maintenance`, `code-review → verify`, `review-resolution → implement`, and `review-resolution → verify` admitted only when current milestone, finding, review, and triggered-CI state select that edge. After milestone closure, `code-review → implement` is also selected when a pending implementation milestone remains and no finding correction is active. Every required exact-subject review judgment is `clear`, every required material decision is explicitly accepted, and no blocking finding, blocker, stale required evidence, or required unfinished work forbids the selected edge. |
| `replace-review` | The exact target is due at its review stage, or its current reference is `review-required`; target kind maps to reviewer responsibility (`proposal` → `proposal-review`, `design-package` → `design-review`, `delivery-package` → `delivery-review`, `milestone` or `final-code` → `code-review`); the prior identity matches or is absent for the first occurrence. |
| `settle-review` | The exact current review target, review ID, identity, judgment, and responsibility metadata match. `clear` requires no open blocking finding and satisfies the target's package or subject identity rules; it derives progression or closes an exact returning correction only after every routed finding has a valid final disposition and every continuing material consequence has an accepted decision. `findings-open` derives the owning authoring stage from one coherent set of current open findings and, for a correction review, keeps the same correction active in `authoring`. `blocked` remains at the review gate and keeps a returning correction active as `blocked`. An ambiguous or inconsistent destination rejects unchanged. |
| `resolve-finding` | The finding is currently open in the exact current review; the current stage is `review-resolution` or the finding's active correction is returning to its expected review; the supplied review preserves all other open findings and every material resolution has applicable decision content. |
| `upsert-decision` | The current stage is `review-resolution` or the stage responsible for an already current decision; a new decision names a current finding or issue and an update preserves the same decision identity. |
| `remove-decision` | The current stage is `review-resolution`; the decision is current, no current artifact, review, evidence, blocker, remaining work, or Verify report references it, and removal does not erase an unresolved material consequence. |
| `route-correction` | No correction is active; every named finding is currently open; the current stage is a review gate or `verify`; source stage, destination stage, return stage, owner responsibility, return condition, and expected review target are consistent with those findings. The resulting active correction has status `authoring`. |
| `return-correction` | The exact correction is active in `authoring`; finding IDs, destination owner, stored return stage, and expected review target match; required revised content is current. Return changes the same correction to `review-required` and makes its stored return stage current, but does not clear the correction, dispose a finding, approve the required review, or grant progression authority. |
| `append-planned-work` | No work is active; the exact primary Plan and current `clear` Delivery Review identities match; the review covers that Plan; every registered milestone remains an unchanged ordered prefix with unchanged current state; and the supplied non-empty suffix equals the Plan's new unique implementation milestones in order. The evaluator appends them as pending `remaining_work`. Any insertion, rewrite, omission, duplicate, stale identity, or caller-supplied state other than pending rejects unchanged. A legacy contract is admitted only for SR-49's exact implementing change, exact M6 suffix, and unused bridge. |
| `advance-milestone` | For `null → planned`, no work is active, current stage is `implement`, the exact named `remaining_work` entry is a pending implementation-owned milestone, and the evaluator removes that entry while constructing `ActiveMilestone`. Otherwise the exact active milestone matches and the transition is only `planned → implementing`, `implementing → review-required`, or `review-required → closed`; closure additionally requires its exact current `clear` Code Review judgment and required evidence and clears active work. A retry binds the resulting lifecycle revision and cannot select the same removed work twice. |
| `update-evidence` | The current stage or active correction owns the evidence-producing work; every subject path and dependency resolves and matches observed identity; the producer field is consistent responsibility metadata, not caller permission. |
| `invalidate-evidence` | Every named evidence entry is current or is the source of a read-time drift blocker; the replacement marks it stale with a rerun or removes it without losing a current blocker or explanation. |
| `record-verify` | The current stage is `verify`; final Code Review is current and `clear`; every required material decision is accepted; every required evidence entry and observed subject is current; no blocking finding, blocker, active work, or required remaining work exists; the report and readiness are produced together. |
| `bootstrap-closeout` | SR-48's exact change, preactivation state, subject set, current consequential validation, independently completed exact-subject legacy final review normalized to `clear`, passing Verify, and activation manifest all match; the exception is unused and no current blocker remains. A legacy outcome label alone cannot satisfy clearance. Every other change, replay after activation, missing or stale subject, current consequential blocker, or incoherent activation rejects according to SR-48; an aggregate-only blocker caused solely by container drift of individually settled occurrences is ignored. |
| `recover` | The named private transaction and recovery identity exist and no live process owns the lock; the requested action is valid for the recorded recovery phase and exact observed file identities. |

The evaluator may return fewer permitted operations when a target-specific predicate is not satisfied; it must never broaden this matrix. A new stage edge, target category, or eligibility outcome requires a new reviewed contract version.

`Projection` contains exactly `view: summary | reviews | open-findings | material-decisions | evidence | remaining-work | verification | skill-context`, `change_id: Id`, `lifecycle_contract: compact-current-state-v1`, `lifecycle_revision: Digest`, `current_stage: Stage`, `artifacts: mapping<Id, ArtifactRef>`, `reviews: mapping<Id, ReviewRef>`, `open_findings: mapping<Id, FindingRef>`, `material_decisions: mapping<Id, DecisionRef>`, `evidence: mapping<Id, EvidenceRef>`, `active_work: ActiveMilestone | ActiveCorrection | null`, `progression_status: blocked | ready`, `blockers: Diagnostic[0..*]`, `remaining_work: mapping<Id, RemainingWork>`, `permitted_operations: Operation[0..*]`, `requested_operation: Operation | null`, `operation_eligibility: OperationEligibility | null`, and `required_paths: Path[0..*]`. `blockers` contains only progression-scoped diagnostics. `requested_operation` and `operation_eligibility` are both null when no operation was selected and otherwise are non-null and name the same operation. `permitted_operations` and operation eligibility are computed from the matrix above and are never copied from caller input, durable state, or `progression_status`. Every view carries the three change and lifecycle identities so a bounded result remains attributable without an enclosing transport. A bounded view uses empty mappings or arrays for categories unrelated to the requested view; it never omits fields or fills them by scanning disposable procedure.

`compact-result-v1` contains exactly `schema: compact-result-v1`, `status: success | already-applied | rejected | busy | recovery-required`, `change_id: Id | null`, `prior_lifecycle_revision: Digest | null`, `resulting_lifecycle_revision: Digest | null`, `affected_paths: Path[0..*]`, `bytes_changed: boolean`, `blockers: Diagnostic[0..*]`, `errors: Diagnostic[0..*]`, `next_operation: Operation | null`, and `projection: Projection | null`. Read-only projection success requires a non-null projection and null lifecycle revisions; mutation and recovery results require `projection: null`.

### Recovery schema

`compact-recovery-v1` contains exactly `schema: compact-recovery-v1`, `transaction_id: Id`, `change_id: Id`, `phase: prepared | replacing | persisted`, `prior_lifecycle_revision: Digest`, `candidate_lifecycle_revision: Digest`, and `affected_files: RecoveryFile[1..*]` sorted lexicographically by `path`.

`RecoveryFile` contains exactly `path: Path`, `prior_state: absent | present`, `prior_identity: Digest | null`, `prior_content: Path | null`, `candidate_state: absent | present`, `candidate_identity: Digest | null`, `candidate_content: Path | null`, and `replacement_status: pending | replaced`. An identity and content path are non-null exactly when their matching state is `present`. Content paths must be descendants of the current transaction's `prior/` or `candidate/` directory respectively.

### Lifecycle revision manifest

The exact preimage is this JSON object followed by one LF:

```json
{"change_id":"<Id>","contract":"compact-current-state-v1","coordinator_sha256":"<Digest>","files":[{"path":"<Path>","sha256":"<Digest>"}]}
```

Object keys are emitted lexicographically, so the actual serialized top-level order is `change_id`, `contract`, `coordinator_sha256`, `files`; each file row is `path`, then `sha256`. `files` contains every other applicable authoritative compact file and every referenced canonical proposal, specification, architecture, ADR, and plan, sorted by UTF-8 path bytes. It excludes `change.yaml`, transaction-private state, requests, logs, superseded procedure, and unreferenced files. `coordinator_sha256` is the `Digest` of the exact coordinator bytes after the SR-40 byte replacement. The resulting lifecycle revision is the `Digest` of the complete manifest bytes.

`recorded_at` never establishes identity, ordering, freshness, or authority even though its bytes contribute to file identity. Repository paths use normalized forward slashes and identities always include the `sha256:` prefix.

## State and invariants

- Exactly one lifecycle-contract discriminator governs a change.
- Exactly one lifecycle revision identifies the complete authoritative current set.
- Each formal review target has zero or one current stable record.
- Every `change.yaml` finding, decision, evidence, review, and artifact reference resolves to one current identity.
- Every open finding exists in its current review record, and every settled finding occurrence remains settled independently of container revisions.
- An explicit correction remains active from routing through return and clears only through settlement of its exact required review; return alone grants no review or progression authority.
- Every material resolution required by SR-11 exists as one explicitly accepted applicable material decision.
- Every current evidence entry has resolvable explicit dependencies and a freshness state consistent with them.
- Final readiness implies one current successful Verify report bound to the current subject and evidence basis.
- A lock or unresolved recovery state withholds every governed read and write except status and an explicit eligible recovery operation.
- Disposable procedure never establishes operation eligibility or freshness.

## Error and boundary behavior

Validation MUST fail closed in this order: parse and size limits; path containment and supported contract version; closed vocabularies and required fields; change identity and lifecycle-derived operation eligibility; expected revision and file identities; semantic cross-record invariants; candidate complete-set validation. A failure MUST identify the earliest safely reportable stable error and leave authoritative bytes unchanged.

Unknown input, a missing optional surface, and an empty applicable surface are distinct. Unknown input rejects. A genuinely inapplicable surface is absent. An applicable surface whose schema requires content cannot be created merely as an empty placeholder.

Busy and recovery-required are not semantic rejections. They MUST be observable distinct statuses, change no authoritative bytes, and identify the safe next capability without exposing private recovery content.

## Boundary model

Boundary model version: boundary-first-v1

Boundary model scope: SR-01, SR-02, SR-03, SR-04, SR-05, SR-06, SR-07, SR-08, SR-09, SR-10, SR-11, SR-12, SR-13, SR-14, SR-15, SR-16, SR-17, SR-18, SR-19, SR-20, SR-21, SR-22, SR-23, SR-24, SR-25, SR-26, SR-27, SR-28, SR-29, SR-30, SR-31, SR-32, SR-33, SR-34, SR-35, SR-36, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-44, SR-45, SR-46, SR-47, SR-48, SR-49

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | SR-01, SR-04, SR-08, SR-09, SR-10, SR-11, SR-12, SR-14, SR-22, SR-23, SR-24, SR-33, SR-37, SR-38, SR-39, SR-41, SR-42, SR-45, SR-46, SR-48, SR-49 | BND-INPUT-001, BND-INPUT-002 | - |
| state-lifecycle | applicable | SR-01, SR-02, SR-03, SR-06, SR-07, SR-08, SR-09, SR-10, SR-11, SR-12, SR-13, SR-14, SR-15, SR-16, SR-17, SR-18, SR-21, SR-23, SR-25, SR-26, SR-27, SR-31, SR-34, SR-35, SR-36, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-44, SR-45, SR-46, SR-47, SR-48, SR-49 | BND-STATE-001, BND-STATE-002, BND-STATE-003, BND-STATE-004 | - |
| identity-authority | applicable | SR-08, SR-09, SR-10, SR-11, SR-12, SR-14, SR-15, SR-16, SR-17, SR-18, SR-21, SR-22, SR-23, SR-24, SR-25, SR-26, SR-27, SR-32, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-45, SR-46, SR-47, SR-48, SR-49 | BND-AUTH-001, BND-AUTH-002 | - |
| composition-path | applicable | SR-02, SR-05, SR-06, SR-19, SR-20, SR-21, SR-22, SR-23, SR-24, SR-25, SR-35, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-48 | BND-COMPOSE-001, BND-COMPOSE-002 | - |
| temporal-retry | applicable | SR-15, SR-18, SR-22, SR-26, SR-27, SR-28, SR-29, SR-30, SR-31, SR-40, SR-41, SR-43, SR-44, SR-45, SR-46, SR-47, SR-48, SR-49 | BND-TEMPORAL-001, BND-TEMPORAL-002 | - |
| failure-recovery | applicable | SR-17, SR-18, SR-24, SR-26, SR-27, SR-28, SR-29, SR-30, SR-31, SR-37, SR-40, SR-41, SR-43, SR-44, SR-45, SR-48, SR-49 | BND-RECOVERY-001, BND-RECOVERY-002 | - |
| compatibility-migration | applicable | SR-01, SR-34, SR-35, SR-36, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-44, SR-45, SR-48 | BND-COMPAT-001, BND-COMPAT-002, BND-COMPAT-003 | - |
| external-environment | applicable | SR-05, SR-16, SR-19, SR-28, SR-29, SR-30, SR-33, SR-38, SR-40, SR-41, SR-43, SR-44, SR-45, SR-48 | BND-ENV-001, BND-ENV-002 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | SR-01, SR-04, SR-08, SR-09, SR-10, SR-11, SR-12, SR-14, SR-22, SR-23, SR-24, SR-33, SR-37, SR-38, SR-39, SR-41, SR-42, SR-45, SR-46, SR-48, SR-49 | valid; malformed; missing; extra; unknown; oversized; selectable milestone; missing milestone; wrong-kind milestone; blocked milestone; exact reviewed suffix; empty or non-suffix extension | Closed schemas and vocabularies precede consistency checks. | Valid input, exact pending milestone selection, and exact reviewed suffix proceed; every other partition rejects unchanged with a bounded safe error. | SR-22 |
| BND-INPUT-002 | input-domain | SR-01, SR-04, SR-08, SR-09, SR-10, SR-11, SR-12, SR-14, SR-22, SR-23, SR-24, SR-33, SR-37, SR-38, SR-39, SR-41, SR-42, SR-45, SR-46, SR-48, SR-49 | contained safe path; traversal; symlink escape; unsupported location; sensitive content | Only declared governed or allowed local roots may be touched. | Unsafe or sensitive input is rejected or safely redacted before output. | SR-33 |
| BND-STATE-001 | state-lifecycle | SR-01, SR-02, SR-03, SR-06, SR-07, SR-08, SR-09, SR-10, SR-11, SR-12, SR-13, SR-14, SR-15, SR-16, SR-17, SR-18, SR-21, SR-23, SR-25, SR-26, SR-27, SR-31, SR-34, SR-35, SR-36, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-44, SR-45, SR-46, SR-47, SR-48, SR-49 | legacy; compact active; compact read-only; mixed; unknown | Contract identity selects exactly one reader and at most one writer. | Supported states project; mixed and unknown states block; compact v1 never converts a legacy change. | SR-01 |
| BND-STATE-002 | state-lifecycle | SR-01, SR-02, SR-03, SR-06, SR-07, SR-08, SR-09, SR-10, SR-11, SR-12, SR-13, SR-14, SR-15, SR-16, SR-17, SR-18, SR-21, SR-23, SR-25, SR-26, SR-27, SR-31, SR-34, SR-35, SR-36, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-44, SR-45, SR-46, SR-47, SR-48, SR-49 | absent; current; open; resolved material; resolved non-material; stale; invalidated; final; pending milestone; active milestone | Continuing consequences are never lost during replacement or milestone selection. | Valid transitions update all affected current surfaces together; exact pending milestone selection moves one item into active work, and invalid selection rejects. | SR-06 |
| BND-STATE-003 | state-lifecycle | SR-01, SR-02, SR-03, SR-06, SR-07, SR-08, SR-09, SR-10, SR-11, SR-12, SR-13, SR-14, SR-15, SR-16, SR-17, SR-18, SR-21, SR-23, SR-25, SR-26, SR-27, SR-31, SR-34, SR-35, SR-36, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-44, SR-45, SR-46, SR-47, SR-48, SR-49 | open occurrence; settled occurrence with unchanged container; settled occurrence with changed container; later regression | Finding disposition belongs to the occurrence, while invalidation follows declared semantic dependencies. | Open stays open until disposition; settled stays settled across container change; a regression creates a new finding linked to the applicable decision. | SR-47 |
| BND-STATE-004 | state-lifecycle | SR-01, SR-02, SR-03, SR-06, SR-07, SR-08, SR-09, SR-10, SR-11, SR-12, SR-13, SR-14, SR-15, SR-16, SR-17, SR-18, SR-21, SR-23, SR-25, SR-26, SR-27, SR-31, SR-34, SR-35, SR-36, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-44, SR-45, SR-46, SR-47, SR-48, SR-49 | initialized work; exact unchanged prefix plus new suffix; renamed, deleted, reordered, modified, reopened, or inserted work; suffix pending; suffix active; suffix closed | Registered milestone identities, order, contracts, evidence allocation, and lifecycle states are immutable; only reviewed new suffix entries may be appended. | Exact reviewed suffix becomes pending work; every rewrite or insertion rejects unchanged; appended work then follows ordinary milestone selection, review, and closure. | SR-49 |
| BND-AUTH-001 | identity-authority | SR-08, SR-09, SR-10, SR-11, SR-12, SR-14, SR-15, SR-16, SR-17, SR-18, SR-21, SR-22, SR-23, SR-24, SR-25, SR-26, SR-27, SR-32, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-45, SR-46, SR-47, SR-48, SR-49 | eligible current state/target; ineligible current state/target; consistent responsibility metadata; mismatched responsibility metadata; caller authority field present; exact pending work selection; reviewed Plan extension | Semantic decisions retain one documented stage responsibility, while execution permission remains outside the CLI and coordinator state is evaluator-derived. | Eligible, consistent content may be validated and persisted; ineligible operations, inconsistent metadata, caller authority fields, constructed active work, and unreviewed extension reject unchanged. | SR-32 |
| BND-AUTH-002 | identity-authority | SR-08, SR-09, SR-10, SR-11, SR-12, SR-14, SR-15, SR-16, SR-17, SR-18, SR-21, SR-22, SR-23, SR-24, SR-25, SR-26, SR-27, SR-32, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-45, SR-46, SR-47, SR-48, SR-49 | exact current identities; stale; omitted; contradictory; caller-asserted freshness; exact Plan and Delivery Review identity | Current content and dependencies determine operation eligibility and freshness. | Exact current identity may proceed; all other partitions reject or invalidate proof. | SR-26 |
| BND-COMPOSE-001 | composition-path | SR-02, SR-05, SR-06, SR-19, SR-20, SR-21, SR-22, SR-23, SR-24, SR-25, SR-35, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-48 | summary; named view; skill context; direct file consumer | All supported reads normalize the same authoritative set. | Views may differ in bounded content but never in state semantics. | SR-20 |
| BND-COMPOSE-002 | composition-path | SR-02, SR-05, SR-06, SR-19, SR-20, SR-21, SR-22, SR-23, SR-24, SR-25, SR-35, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-48 | primary mutation; convenience command; temporary-file request; stdin request; unsupported bypass | One evaluator and transaction path owns every mutation. | Supported entry paths produce equivalent results; bypass cannot create operation eligibility. | SR-19 |
| BND-TEMPORAL-001 | temporal-retry | SR-15, SR-18, SR-22, SR-26, SR-27, SR-28, SR-29, SR-30, SR-31, SR-40, SR-41, SR-43, SR-44, SR-45, SR-46, SR-47, SR-48, SR-49 | first writer; concurrent writer; stale writer; sequential fresh writer | One writer and one expected complete-set revision apply. | First valid writer succeeds; competing or stale writers change no authoritative bytes. | SR-27 |
| BND-TEMPORAL-002 | temporal-retry | SR-15, SR-18, SR-22, SR-26, SR-27, SR-28, SR-29, SR-30, SR-31, SR-40, SR-41, SR-43, SR-44, SR-45, SR-46, SR-47, SR-48, SR-49 | first application; identical retry; conflicting replay; later invalidating mutation; repeated milestone selection; repeated suffix extension | Repetition cannot duplicate effects, append work twice, reactivate removed work, or preserve invalid readiness. | Exact retry reports already applied; conflict, repeated extension, or repeated selection rejects; later dependency change invalidates proof. | SR-31 |
| BND-RECOVERY-001 | failure-recovery | SR-17, SR-18, SR-24, SR-26, SR-27, SR-28, SR-29, SR-30, SR-31, SR-37, SR-40, SR-41, SR-43, SR-44, SR-45, SR-48, SR-49 | before prepare; prepared; partially replaced; completely replaced; cleanup interrupted | Readers never accept an unresolved transaction state. | Restore exact prior or complete exact candidate; otherwise remain recovery-required. | SR-30 |
| BND-RECOVERY-002 | failure-recovery | SR-17, SR-18, SR-24, SR-26, SR-27, SR-28, SR-29, SR-30, SR-31, SR-37, SR-40, SR-41, SR-43, SR-44, SR-45, SR-48, SR-49 | Verify success; Verify failure; interrupted Verify; later invalidation; pending appended work | Successful readiness and its report are current together or absent together, and unfinished appended work precludes final readiness. | Only exact success with no active or pending work yields current report; every other outcome withholds readiness. | SR-17 |
| BND-COMPAT-001 | compatibility-migration | SR-01, SR-34, SR-35, SR-36, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-44, SR-45, SR-48 | completed legacy; ordinary in-flight legacy; new compact change; attempted cross-contract write | File shape never selects contract or writer authority. | Completed legacy remains readable; ordinary in-flight legacy finishes under its contract; compact v1 rejects cross-contract conversion. | SR-34 |
| BND-COMPAT-002 | compatibility-migration | SR-01, SR-34, SR-35, SR-36, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-44, SR-45, SR-48 | coherent activation; mixed deployment; rollback; future supported reader | Writers activate as one versioned set; released compact records remain readable. | Mixed deployment blocks; rollback stops writers without destroying current records. | SR-35 |
| BND-COMPAT-003 | compatibility-migration | SR-01, SR-34, SR-35, SR-36, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-44, SR-45, SR-48 | exact implementing change; another legacy change; exact current subjects; stale or missing subject; current blocker; superseded aggregate-only blocker; first activation; replay | The bootstrap is one current-consequence closeout, not migration, and never uses Git or PR identity. | Only the exact complete clear and verified implementing set closes and activates atomically; every other partition rejects unchanged. | SR-48 |
| BND-ENV-001 | external-environment | SR-05, SR-16, SR-19, SR-28, SR-29, SR-30, SR-33, SR-38, SR-40, SR-41, SR-43, SR-44, SR-45, SR-48 | Git present or absent; PR available or unavailable; network online or offline; logs present or absent | External history and diagnostics never supply correctness state. | All governed capabilities retain their semantics in every partition. | SR-19 |
| BND-ENV-002 | external-environment | SR-05, SR-16, SR-19, SR-28, SR-29, SR-30, SR-33, SR-38, SR-40, SR-41, SR-43, SR-44, SR-45, SR-48 | ordinary success; permission failure; disk full; process interruption; tampered recovery data | Failure cannot authorize a partial set or expose sensitive recovery bytes. | Exact rollback/completion occurs or governed access remains blocked with safe diagnostics. | SR-28 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | SR-06, SR-10, SR-11, SR-12, SR-26, SR-27, SR-28, SR-29, SR-30, SR-38, SR-39, SR-40, SR-43, SR-44, SR-45 | BND-STATE-002, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001 | A concurrent or interrupted review replacement drops an open finding or material decision. | The complete old set remains authoritative or the complete eligible replacement contains the required finding disposition and decision. |
| INT-002 | SR-14, SR-15, SR-16, SR-17, SR-18, SR-26, SR-27, SR-28, SR-29, SR-30, SR-31, SR-40, SR-41, SR-44, SR-45 | BND-STATE-002, BND-AUTH-002, BND-TEMPORAL-002, BND-RECOVERY-002 | Retry or subject revision leaves stale evidence or Verify readiness current. | Dependency comparison and final readiness update atomically; retry cannot restore invalid proof. |
| INT-003 | SR-19, SR-20, SR-21, SR-22, SR-23, SR-24, SR-25, SR-32, SR-37, SR-38, SR-39, SR-41, SR-42, SR-46 | BND-AUTH-001, BND-COMPOSE-001, BND-COMPOSE-002 | A convenience command, projection, caller assertion, or milestone selection bypasses lifecycle-derived eligibility or semantic responsibility checks. | Every path uses the same normalized snapshot and evaluator; no renderer, adapter, caller claim, or constructed active-work record creates eligibility. |
| INT-004 | SR-28, SR-29, SR-30, SR-33, SR-38, SR-39, SR-43, SR-44, SR-45 | BND-INPUT-002, BND-RECOVERY-001, BND-ENV-002 | Filesystem failure combines with unsafe or tampered recovery paths. | Recovery remains contained, rejects ambiguity, exposes no private bytes, and blocks governed reads. |
| INT-005 | SR-01, SR-34, SR-35, SR-36, SR-37, SR-38, SR-39, SR-40, SR-41, SR-42, SR-43, SR-44, SR-45 | BND-STATE-001, BND-COMPAT-001, BND-COMPAT-002, BND-ENV-001 | A mixed rollout or rollback interprets a legacy or compact change with the wrong writer. | The explicit contract and supported-reader set select behavior; unsupported writers withhold mutation without external reconstruction. |
| INT-006 | SR-10, SR-11, SR-12, SR-15, SR-26, SR-47 | BND-STATE-003, BND-AUTH-002, BND-TEMPORAL-002 | A document or aggregate container revision resurrects settled findings or stales unrelated proof. | Occurrence dispositions remain stable, declared dependents invalidate, and a real recurrence receives a new finding linked to the applicable decision. |
| INT-007 | SR-23, SR-26, SR-28, SR-30, SR-35, SR-43, SR-44, SR-45, SR-48 | BND-STATE-001, BND-COMPAT-003, BND-RECOVERY-001, BND-ENV-001 | The replacement depends forever on legacy history, Git identity, or a partially activated writer set. | The exact implementing current set closes and activates atomically once, or the prior writer authority remains unchanged. |
| INT-008 | SR-23, SR-25, SR-26, SR-27, SR-31, SR-46, SR-49 | BND-INPUT-001, BND-STATE-004, BND-AUTH-001, BND-AUTH-002, BND-TEMPORAL-001, BND-TEMPORAL-002, BND-RECOVERY-002 | A late reviewed correction needs new implementation, but extending work could rewrite closed milestones, race another update, duplicate work, or bypass Delivery Review. | Only the exact reviewed suffix is appended once as pending work; all registered milestones and states remain unchanged, and final readiness stays withheld until the suffix completes ordinary Code Review. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | SR-19, SR-20, SR-21 | BND-COMPOSE-001, BND-ENV-001 | - | - |
| E2 | illustration | SR-06, SR-07, SR-10, SR-11, SR-12, SR-13, SR-26 | BND-STATE-002, BND-AUTH-001 | - | - |
| E3 | illustration | SR-14, SR-15, SR-18 | BND-STATE-002, BND-AUTH-002, BND-TEMPORAL-002 | - | - |
| E4 | illustration | SR-28, SR-29, SR-30, SR-43, SR-44, SR-45 | BND-RECOVERY-001, BND-ENV-002 | - | - |
| E5 | regression | SR-23, SR-25, SR-26, SR-27, SR-46 | BND-INPUT-001, BND-STATE-002, BND-AUTH-001, BND-TEMPORAL-002 | CCSR-M3-CR7 | - |
| E6 | regression | SR-10, SR-15, SR-26, SR-47 | BND-STATE-003, BND-AUTH-002, BND-TEMPORAL-002 | CCSR-DR12-1 | - |
| E7 | regression | SR-23, SR-25, SR-26, SR-27, SR-31, SR-46, SR-49 | BND-INPUT-001, BND-STATE-004, BND-AUTH-001, BND-AUTH-002, BND-TEMPORAL-001, BND-TEMPORAL-002, BND-RECOVERY-002 | CCSR-DLR10-1 | - |
| E8 | regression | SR-23, SR-35, SR-48 | BND-COMPAT-003, BND-RECOVERY-001, BND-ENV-001 | CCSR-DR12-2 | - |

No example creates normative behavior; SR-01 through SR-48 and the boundary definitions own every illustrated outcome.

## Compatibility and prospective adoption

The first compact contract applies prospectively. Existing completed records keep their exact files and remain readable through their recorded legacy discriminator. An ordinary legacy change already in flight finishes under its registered contract. Compact v1 has no bulk compaction, inferred conversion, or in-place migration capability, and no requirement to recover discarded history into the new surfaces.

The sole exception is SR-48's preactivation closeout for the implementing change. That operation leaves the change structurally legacy, ignores only superseded procedure whose individual consequences are already settled, validates the exact current consequential set, and activates compact writing atomically. It creates no reusable migration route and grants no authority to another legacy change.

Activation is one coherent release boundary. Canonical governance, behavior specifications, architecture, skills, templates, schemas, validators, CLI behavior, fixtures, documentation, and supported adapters must agree before any compact writer is enabled. A rollback may disable writers, but supported readers must remain available for already-created compact changes.

## Observability

Human and JSON results MUST share status and stable error semantics. Bounded local diagnostics MAY record command identity, start and finish state, duration, safe affected-path summaries, and stable error codes. Logs MUST be size- and retention-bounded, non-authoritative, safe to delete, and excluded from projection, review, evidence, progression, recovery decisions, and Verify.

The current evidence manifest records evidence provenance and outcomes, not diagnostic output. Recovery status exposes transaction identity and safe next action but not prior file bytes, secrets, arbitrary request content, or environment values.

## Security and privacy

This feature does not add user authentication or protect against a repository owner who can edit files directly. It does require all supported CLI paths to enforce repository containment, reject path traversal and symlink escape, use restrictive permissions for lock and recovery content, avoid recording request bodies or environment dumps in logs, redact secret-bearing values from errors, and fail closed on tampered recovery state.

Network access, a hosted identity provider, a pull-request host, and external credentials are not required. Evidence detail references must not make an unavailable external system the only source for understanding the recorded claim, scope, outcome, or freshness.

## Accessibility and UX

No graphical interface is introduced. Human CLI output MUST use text labels in addition to color, remain understandable with color disabled, and provide a concise status, blockers, and next safe action. JSON output is the automation interface. Stable review and decision Markdown must remain readable without custom rendering.

## Performance expectations

Projection work MUST be bounded by the applicable authoritative current files and selected view, not by the number of historical review rounds, corrections, requests, transitions, or evidence executions. A skill-context view MUST NOT enumerate unrelated current record bodies. Mutation and recovery may validate the complete current set but MUST NOT walk Git history or contact a network service.

No fixed millisecond target is imposed. Delivery verification must demonstrate that projection input volume remains constant for equal current-state size even when synthetic prior workflow history differs.

## Edge cases

EC1. A review target without a prior occurrence creates its stable record; a later occurrence replaces it.

EC2. A change with no material decisions or current evidence has no placeholder `material-decisions.md` or `evidence.yaml`; projections return an empty bounded collection.

EC3. One finding is partially accepted. It may close only when the accepted and rejected portions and any continuing material consequence are explicit; otherwise it remains open.

EC4. Evidence covers multiple subjects and only one changes. The entry becomes stale unless its schema explicitly supports separable independently identified coverage; the CLI does not infer partial freshness.

EC5. A raw output location disappears. The evidence entry may remain current if its recorded metadata is sufficient and no declared dependency changed; disappearance alone cannot change the recorded outcome or broaden its claim.

EC6. A temporary request path is inside the repository. The CLI may read it but must not register, stage, or require it as part of the resulting governed set.

EC7. The process reports failure after persistence actually completed. An exact retry reports `already-applied` only after validating the complete resulting set.

EC8. Recovery data is missing or corrupted after a partial replacement. The change remains recovery-required for explicit intervention; the CLI must not guess from surviving files or Git.

EC9. A direct manual edit changes a current authoritative file. Its identity no longer matches the lifecycle revision, so governed projection and mutation fail closed until an explicit eligible reconciliation operation establishes a complete valid set.

EC10. A historical change happens to contain files with compact names. Its legacy discriminator prevails and compact writes remain denied.

EC11. A source path named by current evidence changes outside the lifecycle CLI. The next evidence, review, progression, or Verify projection hashes that exact declared path, returns a drift blocker, and permits no reliance on the evidence until an explicit evidence mutation records the current result or stale state.

EC12. An open finding and invalidated downstream package make overall progression blocked while the exact owning artifact correction is structurally eligible. The projection reports `progression_status: blocked`, retains the progression diagnostics, and reports the requested corrective operation as permitted with no operation blockers.

EC13. Corrected content satisfies an active correction's return condition. Return moves the same correction from `authoring` to `review-required` at its stored return stage. A `clear` exact-subject settlement with valid finding dispositions and accepted material decisions clears it; `findings-open` keeps a coherently retargeted correction active, and `blocked` keeps it active as blocked.

EC14. No work is active and two pending milestone entries remain. Selecting one exact ID moves only that entry to planned active work; selecting a missing, blocked, task-kind, non-implementation-owned, or already-selected ID rejects unchanged. After its reviewed closure, the other entry remains visible and `code-review → implement` becomes eligible for a new explicit selection.

EC15. A legacy aggregate resolution file changes after a finding occurrence was individually settled. The old finding remains closed. Any current review or evidence that directly depends on the changed file becomes non-current; unrelated records remain current. If the revised subject violates the settled decision, the reviewer creates a new finding that references the decision.

EC16. The implementing change reaches preactivation closeout with all exact subjects current, no current open blocker, clear final review, passing Verify, and a coherent activation manifest. Closeout and activation succeed together. If any fact differs, or another change invokes the operation, no authority changes.

## Non-goals

- Preserving or reconstructing every workflow event, command input, route, prior review wording, or routine resolved finding.
- Providing an audit ledger, tamper-proof store, hosted service, database, or distributed transaction protocol.
- Making machine-local logs, Git metadata, pull requests, CI output, or network services authoritative.
- Folding canonical proposal, specification, architecture, ADR, or plan content into one change-local file.
- Authenticating repository owners or preventing intentional direct filesystem modification.
- Rewriting completed historical changes.
- Defining test filenames, frameworks, fixture layout, milestone allocation, release version, or deployment date.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC-01 | Every SR has direct downstream verification allocation and every applicable boundary and selected interaction has direct proof. |
| AC-02 | One bounded projection answers the full resume contract without Git, PR, network, logs, request files, or superseded records. |
| AC-03 | Supported review replacement cannot lose an open finding or required material decision. |
| AC-04 | Supported artifact and review mutation cannot leave dependent evidence or final readiness falsely current. |
| AC-05 | Concurrency and injected interruption at every transaction boundary preserve or recover one complete authoritative set. |
| AC-06 | All unknown closed-vocabulary values and unsafe paths fail before semantic consistency checks and change no authoritative bytes. |
| AC-07 | Human and JSON projections and results agree on status, identities, blockers, mutations, and next safe action. |
| AC-08 | Compact writer activation is withheld until every canonical, executable, validation, fixture, documentation, and supported-adapter surface agrees on one contract version. |
| AC-09 | Completed legacy records remain readable and unchanged, ordinary in-flight legacy changes finish under their registered contract, and compact v1 rejects every inferred or requested cross-contract conversion. |
| AC-10 | Equal current-state sizes produce bounded equal-scope context regardless of synthetic procedural-history length. |
| AC-11 | Independent readers and writers agree on all eight v1 schema shapes, whole-set lifecycle revision, size limits, recovery outcomes, and the post-sync success boundary. |
| AC-12 | A globally blocked correction fixture exposes its exact eligible recovery operation, while the same fixture continues to prohibit downstream advancement and a target, identity, authority, or recovery mismatch prohibits the requested operation with an operation-scoped diagnostic. |
| AC-13 | Correction fixtures prove that route creates `authoring`, return preserves the correction as `review-required`, only an exact `clear` review settlement with valid dispositions and accepted decisions can clear it, and every `findings-open`, `blocked`, or inconsistent settlement retains or rejects without losing its findings, owner, return condition, or required review. |
| AC-14 | Multi-milestone fixtures prove first selection, implementation handoff, reviewed closure, next selection, final exhaustion, stale retry, and every invalid remaining-work partition without parsing plan prose or accepting caller-constructed active state. |
| AC-15 | Finding-lifecycle fixtures prove that aggregate or document revision cannot reopen a settled occurrence, dependency-scoped invalidation affects only declared consumers, and a recurrence uses a new finding ID linked to the retained decision. |
| AC-16 | Bootstrap fixtures prove exact named-change eligibility, exact-current-set binding, current-only consequential validation, clear final review, passing Verify, atomic activation, rejection of Git/PR inputs, rejection for every other change, stale-input rejection, and one-time expiry without migration. |

## Open questions

None. Parser library, internal module layout, temporary filename suffixes below the fixed transaction root, and other mechanics that do not alter SR-01 through SR-48 may be selected during planning and implementation; any choice that changes an observable outcome returns to Design.

## Next artifacts

- Design Review of this specification, the compact current-state architecture, and the applicable ADR as one exact package.
- Delivery plan after a clear Design Review judgment and derived progression eligibility.

## Follow-on artifacts

None yet

## Readiness

The specification is ready for Design Review reconciliation with the architecture and ADR. It does not claim a clear Design Review judgment, Delivery readiness, implementation readiness, verification, branch readiness, or PR readiness.
