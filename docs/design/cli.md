# CLI Model Design

Model validation contract: explicit-recording-v1

## Drafting basis and authority

This is an initial, unapproved model Design draft under the user's explicit exception permitting these two model files before formal registration. It combines requirements, architecture and decisions without creating separate specification or ADR files. It does not change executable CLI behavior, activate a contract or confer implementation authority. No owning change record has been established for these drafts.

Direction: [Explicit Workflow Recording and Model-Centered Design](../proposals/2026-09-05-explicit-recording-and-model-centered-design.md). The [Workflow model](workflow.md) owns lifecycle meaning, decision responsibilities and model-document conventions. The current [Constitution](../../CONSTITUTION.md) remains operative pending approved adoption. This file addresses workflow recording, not a redesign of installation, release or every public CLI command.

## Introduction and Goals

Make the CLI a small repository-local tool that reads records, reports observations, validates explicit updates and persists them safely. The user or agent supplies status and decisions. The CLI never chooses a stage or turns another edit into a workflow decision.

Simplicity means removing semantic transition orchestration, not removing schema validation, concurrency protection or recovery. A lifecycle may need human judgment; safely writing bytes must not require the lifecycle first to become semantically complete.

## Architecture Constraints

Use exact local identities and explicit paths. Do not require Git, PR access, network services or a daemon. Data safety is enforced mechanically; workflow authority is not inferred from a caller's role string. Never use the new recorder as an implicit interpreter for an old contract.

The [existing transaction module](../../packages/rigorloop/dist/lib/compact-transaction.js) is a candidate source of persistence machinery, not evidence that the proposed contract already works. Its coupling to complete-set lifecycle validation must be assessed before reuse. No project-map inference is used: the proposed boundary is grounded in the proposal, governance and directly inspected persistence surface.

## Context and Scope

The CLI receives an exact change target, explicit candidate records and expected current identities from an actor. It returns stored content, observations or a persistence result. The Workflow model interprets that result and decides what to do next. Filesystem permissions and runtime restrictions bound execution; the CLI cannot grant external permissions.

This draft selects four commands under `rigorloop record-store`: `inspect`, `check`, `record` and `recover`. These are proposed commands, not currently shipped functionality. The separate namespace prevents collision with historical semantic command handlers. Existing unrelated command families remain outside this change.

## Solution Strategy

Separate structural validation from workflow diagnosis and separate both from persistence. A candidate update replaces explicitly named record content rather than invoking semantic operations such as advance-stage, settle-review or reopen-owner. The CLI may generate content hashes, storage revisions and transaction bookkeeping, but all substantive status values come from submitted records.

An old reviewed-subject hash is a legitimate reference to what was reviewed, not a foreign key that must equal today's file hash. Observed drift must be visible without making it impossible to save the correction that addresses it.

## Requirements

| ID | Required behavior |
| --- | --- |
| CLI-SR-01 | Inspect MUST return recorded values and separately labeled observations without altering authoritative records or performing recovery. It MUST NOT compute an authoritative next stage, approval, completion or applicability value. |
| CLI-SR-02 | Check and record MUST reject malformed records, unknown schema versions, unknown closed-vocabulary values, duplicate identities, dangling internal record references and unsafe targets before any authoritative write. Validity MUST NOT depend on whether the current workflow stage permits a proposed decision. |
| CLI-SR-03 | Record MUST accept a complete, explicit candidate for every named replacement and identify the expected revision, expected identities and exact target set. Unnamed files and omitted workflow decisions MUST remain unchanged. It MUST NOT merge stale decisions, fill semantic defaults or rewrite an old review to claim it assessed new content. |
| CLI-SR-04 | An update MUST exclude competing CLI writers and check expected revision, target identities and declared decision-basis identities before publication. Observed mismatches reject the update with a conflict; the caller must reread and decide again. External edits are covered at the observed checks, not atomically with replacement; the Save safety and recovery boundary applies. |
| CLI-SR-05 | Related replacements MUST be published as one logical transaction. Supported readers MUST receive a coherent before/after snapshot or an explicit busy/recovery-required result, never a mixed snapshot presented as usable current state. A successful result means all requested bytes are durably committed. |
| CLI-SR-06 | Interrupted writes MUST preserve sufficient local recovery information to restore a verified before-state or complete the exact prepared candidate. Recovery MUST NOT generate new workflow decisions and MUST stop when a target check observes bytes matching neither recorded state. Missing or tampered recovery evidence requires a reported recovery stop, not guessed repair. The same external-edit boundary applies to record and recovery. |
| CLI-SR-07 | Workflow observations, including changed review subjects, failed proof or contradictory readiness claims, MUST remain separate from structural rejection and saved content. They MUST NOT silently alter decisions or prohibit recording a structurally sound blocker, invalidation or correction. A successful record result MUST explicitly limit its claim to persistence. |
| CLI-SR-08 | Repeated submission MUST NOT duplicate findings or apply incremental semantic effects. Record uses explicit replacement content; a lost-response retry returns a conflict or an identical already-recorded result only when that result can be established from exact identities. It MUST NOT imply that the workflow action was newly approved. |
| CLI-SR-09 | All public, helper and recovery write paths MUST use the same containment, identity and transaction protections. Cross-change writes, path traversal, symlink escape and unexpected overwrite are rejected. This interface MUST NOT offer arbitrary repository file writes disguised as workflow updates. |
| CLI-SR-10 | Unsupported or historical lifecycle contracts MUST be identified explicitly and MUST NOT be silently rewritten using this recording contract. An adoption mechanism requires its own approved exact mapping and recovery contract. Ordinary inspect, check and record MUST NOT migrate data. |
| CLI-SR-11 | Results MUST distinguish saved, unchanged, rejected, conflict, busy and recovery-required outcomes, name affected identities where available, and separate observations from errors. Errors MUST NOT echo arbitrary record payloads or secrets. Human and machine-readable forms must preserve the same outcome meaning. |

## Building Block View

```text
Actor-supplied decisions and expected identities
                    |
              Request decoder
                    |
         Shape / reference / path checks
                    |
          Snapshot and conflict checks
                    |
            Transactional persistence
                    |
        Stored values + persistence result

Read-only observations accompany snapshots and results.
Workflow interpretation remains outside this pipeline.
```

The decoder recognizes the selected contract and bounded record kinds. The structural validator checks only data representation and integrity. The snapshot reader and transaction layer coordinate access to authoritative files. The observer reports factual differences without selecting decisions. The renderer makes the distinction visible to humans and agents.

### Candidate update contract

The transient request is UTF-8 JSON with exactly `schema_version: 1`, `contract: explicit-recording-v1`, `change_id`, `expected_revision`, `writes` and `reads`. `writes` is a nonempty array of `{path, expected_identity, content}`; `reads` is an array of `{path, expected_identity}`. Content is a UTF-8 string containing the complete replacement file. Expected identities are exact SHA-256 digests; null means the target must be absent. Null `expected_revision` is allowed only when creating an absent change root. IDs and record kinds come from the Workflow model. Duplicate keys, duplicate paths and unknown fields reject the request.

The first contract stores JSON-subset YAML: `.yaml` files contain a single JSON object; Markdown records begin with `---`, a single JSON metadata object, another `---`, then the Markdown body. Delimiters occupy their own lines. JSON objects admit no duplicate keys, comments or nonfinite numbers. Content uses LF newlines, no BOM and a final newline; other encodings are rejected rather than silently normalized. The CLI parses content to validate it but persists the exact supplied bytes. Object order and whitespace are not semantically significant, but remain significant to byte identity. No serialization rewrite or semantic default is performed.

The change revision is computed, never written into the record: hash the compact JSON encoding of a path-sorted array of `[path, exact-byte-digest]` pairs for `change.yaml` and every file listed by its `records` registry. Paths use ASCII and sort by byte order. This avoids a self-referential hash and catches supporting-record changes even when the manifest bytes did not change. Candidate revision uses the candidate registry and bytes. Broken current references can be repaired: inspect reports missing registered content using a null digest in the revision array, and record validates the complete candidate rather than demanding a semantically valid before-state. An unreadable/malformed manifest cannot supply a registry and requires explicit external repair under user authority; the CLI does not guess one from directory scans.

The first recording contract supports creation and replacement of allowed workflow records only, not unrestricted deletion or arbitrary edits to engineering documents. Authors edit model documents through their normal scoped editing workflow and include their identities in the recording read set. This avoids pretending that a review-record transaction also atomically edited all design or implementation files.

The write set is restricted to the exact selected change's recognized record surfaces. Decision-basis reads may reference safe repository-local model documents and proof inputs. An entire repository scan is neither required nor permitted as a substitute for a declared basis. Undeclared semantic dependencies remain an actor/reviewer responsibility.

### Paths and command interface

CLI-SR-02/03/09/10/11 own this interface. `--root` is an explicit existing repository directory and `--change` is a Workflow-model change ID. Inputs and outputs are not inferred from the current working directory. Supported authoritative paths relative to that root are exactly `docs/changes/<id>/change.yaml`, `docs/changes/<id>/reviews/<review-id>.md`, and the three conditional files `evidence.yaml`, `material-decisions.md`, `verify-report.md` in that change directory. Registry entries cannot expand this allowlist. The review filename and metadata ID must agree.

| Proposed invocation | Input and behavior |
| --- | --- |
| `rigorloop record-store inspect --root PATH --change ID --format json` | No stdin; returns the registered snapshot, byte identities, computed revision and observations. An absent root is an absent observation, not an invitation to create it. |
| `rigorloop record-store check --root PATH --change ID --input - --format json` | Reads one request from stdin, validates the candidate against a snapshot, writes nothing and makes no reservation. |
| `rigorloop record-store record --root PATH --change ID --input - --format json` | Reads the same request form, repeats all freshness checks and commits only explicit writes. CLI and envelope change IDs must match. |
| `rigorloop record-store recover --root PATH --change ID --transaction ID --expected-recovery DIGEST --action restore --format json` | Explicitly restores the verified before-state of an interrupted transaction; `--action complete` selects the exact candidate instead. No other action is accepted. |

`--format` accepts `json` or `text`, defaulting to text; all other shown selectors are required. Unknown flags, extra positional arguments, contradictory selectors or non-stdin input selectors reject. No permanent operation request file is created. `record` also performs initial creation using absent preconditions; a separate automatic initialization step is unnecessary. An existing directory, even without a manifest, is not an absent root and cannot be adopted by creation.

New-root creation may create only the selected change directory and required `reviews` directory; it may not claim an existing root. Existing registry membership cannot be removed in this first version: retirement is recorded with explicit applicability and retained bytes. Registered missing files may be restored through an explicit absent write precondition. A candidate can introduce a new registered file in the same transaction. Writes to unregistered sidecars, unsupported paths or existing unregistered files reject. Abandoned unrelated files are never overwritten or silently imported.

All paths are nonempty ASCII repository-relative paths with `/` separators, no empty, dot or dot-dot segments, backslashes, control characters or absolute prefixes. Symlinks in the root's descendants and hard-linked authoritative files are rejected; targets must be regular files or explicitly absent. The implementation must protect path resolution against concurrent substitution, not merely check a string once. Decision-basis paths cannot name transient store data. The request read set is not required to repeat historical subject hashes as current expectations: doing so would recreate the stale-review correction cycle.

### Result schema and exit behavior

Every JSON result has exactly `{schema_version: 1, operation, status, change_id, revision, files, snapshot, observations, errors, transaction, claim}`. `operation` is one of the four command names; `claim` is always `storage-only`. `revision` is a digest or null when unavailable; `files` is an array of `{path, identity}` where identity is a digest or null for an absent path. `transaction` is null or `{id, recovery_identity}` with a digest when recoverable metadata exists, otherwise null for that identity. Observations and errors are arrays of `{code, path, message}`, with path null for non-path-specific conditions. Messages are safe summaries, not raw payloads.

CLI-SR-02/11 defines one narrow selector-error exception: before dispatch, an unavailable `operation` or `change_id` is represented by null, never a fabricated sentinel or an echo of invalid input. An operation is available only when the subcommand is one of the four recognized names. A change ID is available only when exactly one `--change` selector supplies a valid Workflow-model ID. Missing, invalid or repeated change selectors make that identity unavailable, even when repeated values are equal. Each independently available selector is retained. Unknown flags or other argument errors do not erase otherwise available identities.

Any result with a null selector MUST have `status: rejected`, exit code 2, `revision: null`, `files: []`, `snapshot: null`, `observations: []`, `transaction: null`, `claim: storage-only`, and exactly one non-path-specific `invalid-input` error with a safe message. All argument-validation failures use that same empty, non-mutating rejection shape, retaining available selectors; they perform no repository access or stdin read. Every non-rejected result requires both valid selectors. Unknown non-null values remain invalid. This extends the single result envelope rather than adding a separate usage-error schema or weakening request and persisted-record identities. For invalid or repeated `--format`, output falls back to text with exit code 2; exactly one valid `--format json` selects JSON even when another argument is invalid. No raw rejected selector value appears in text, JSON or diagnostic logs. These input-rejection rules do not change command-scoped storage failures or successful results.

For `inspect` with status `inspected`, `snapshot` is exactly `{records: [{path, content}]}`. It contains `change.yaml` and every registered supporting record in path order, with the same paths and identities as `files`, all obtained from one coherent snapshot. `content` is the exact UTF-8 file content as a JSON string, using the record encodings and Workflow-model definitions already specified; this introduces no second schema for activity, reviews or evidence. Missing registered supporting files remain present with null content and null identity and a `subject-drift` observation. They are not silently omitted or synthesized. An absent change root returns an empty records array, empty files array, null revision and the existing `absent-change` observation. An unreadable, malformed or unsafe manifest cannot establish the registry and returns a rejection with null snapshot.

For every other operation or any non-`inspected` result, `snapshot` is null. In particular, busy or recovery-required inspection never exposes partial content as a usable snapshot, and check/record/recover do not echo record bodies. Text inspection presents the same content and missing-file distinctions. Content belongs only in the explicit inspection payload, never diagnostic messages. These presence rules realize CLI-SR-01/05/11; inspect remains read-only and its content is recorded data, not derived workflow judgment.

Status and exit pairs are `inspected/0`, `valid/0`, `saved/0`, `unchanged/0`, `recovered/0`, `rejected/2`, `conflict/3`, `busy/4`, `recovery-required/5`. `inspected` and `valid` belong only to inspect/check; `saved` and `unchanged` to record; `recovered` to recover. Failure statuses apply to any relevant operation. `unchanged` requires both satisfied current preconditions and identical candidate bytes; a lost-response retry with an old revision returns conflict even if the candidate was already saved. This intentionally avoids an operation ledger.

The closed v1 diagnostic codes are `invalid-input`, `unsupported-contract`, `unsafe-path`, `broken-reference`, `identity-conflict`, `store-busy`, `recovery-needed`, `io-failure`, `limit-exceeded`, `absent-change`, `subject-drift`, `failed-evidence`, `inconsistent-claim`. Only the last four are observations. The observer reports absent roots, missing/changed referenced subjects, explicitly failed evidence checks, and a recorded completed activity coexisting with an open blocker or failed evidence. It does not implement general workflow eligibility. Unknown diagnostic codes require a version change rather than silent consumer fall-through. Diagnostics alone do not change record status or an exit-0 storage outcome.

## Runtime View

### Read and check

Resolve the exact target and contract, establish a coherent snapshot and report stored values plus observations. An unknown contract can be identified without claiming its state was interpreted. Check evaluates candidate structure against a snapshot without writing; a check result is not a reservation and record must repeat freshness checks.

### Explicit status recording

An actor submits the complete intended change record and any related replacements. The CLI validates targets and representations, prevents conflicting saves, rechecks expected identities and prepares recoverable before/candidate data. It commits the named replacements and returns their identities. It does not select another stage or change any review judgment as a consequence.

### Artifact changed after review

A retained review can cite an earlier hash while the current model file has a newer one. This is a drift observation, not malformed data. The author can save explicit applicability and correction updates without first making the old review match the file. If the model file changes again after the author read it, the decision-basis identity check rejects the write as a conflict.

### Concurrent update and ambiguous retry

Two CLI candidates based on the same revision cannot both replace it unnoticed. The losing actor receives busy or conflict, not an automatic merge. If a result is lost after commit, the actor inspects current bytes; retry must not add another finding or duplicate an action. No permanent request ledger is required merely to repeat replacement content.

### Interrupted transaction

Readers and writers encountering an unfinished transaction report recovery-required instead of interpreting partial records. Explicit recovery verifies the recorded before/candidate identities and either completes the candidate or restores the before-state according to the caller's explicit action. An observed unrelated external edit stops recovery for reconciliation. Recovery bookkeeping is private mechanical support, not durable workflow evidence or a review receipt.

### Save safety and recovery boundary

CLI-SR-04/05/06 define observable save-safety outcomes, not an operating-system protocol. OS selection, platform exclusions, filesystem-specific mechanisms and a separate OS-lock feasibility investigation are outside this design's scope by user direction. Retain the existing project's execution assumptions; this draft makes no expanded platform-support claim.

Do not manually edit record files, or let other tools edit them, while `record` or `recover` is running. CLI writers coordinate with each other; outside tools do not. For external edits, freshness is guaranteed only at the observed identity checks. An exact-target edit after the final check and before replacement may be overwritten; preventing that race is not a requirement. This limit applies equally to save, completion and restoration. Observed conflicts and unknown third states still stop the operation, and path containment—including protection against substituted ancestors—remains required under CLI-SR-09. This is the user-selected scope refinement for ER-M2-005, not a new storage mechanism.

Private transaction data lives under `.rigorloop/record-store/<change-id>/`, outside lifecycle authority. A competing save returns busy or conflict without overwriting newer work. Readers receive a coherent snapshot or busy/recovery-required, never partially saved records presented as usable state. Inspect and check do not create transaction data or repair records. The implementation mechanism for meeting these outcomes is not prescribed here.

Before replacing authoritative content, retain enough private before/candidate data to recover the exact requested transaction. Report saved only when all requested replacements are committed; an incomplete save remains explicitly recoverable and cannot be consumed as current state. At most one unfinished transaction exists per change. A private manifest identifies the exact write/read set, before/candidate identities and whether the transaction is prepared or committed. Its digest is the expected-recovery identity; transaction IDs are opaque storage identifiers, not workflow IDs.

Explicit `complete` requires unchanged declared read-set inputs and verified candidate snapshots; `restore` requires verified before snapshots and leaves external read-set files untouched. In either case each authoritative target must equal its before or candidate bytes (including absence) at the identity check; an observed unknown third state stops recovery. A committed manifest permits only completion/cleanup, never rollback of acknowledged success. Restoring initial creation removes only transaction-created files and empty transaction-created directories, never preexisting or externally added content within the external-edit boundary above. Recovery can itself be interrupted and repeated with refreshed recovery identity. After a verified terminal outcome, private transaction snapshots may be removed; they are not part of current workflow evidence.

Decision-basis files are checked immediately before publication and again before reporting commitment. They are outside the recorder's write set. Observed drift after replacement triggers restoration when safe, otherwise recovery-required; drift after the final check is an ordinary new external edit. The guarantee is freshness at the observed check, not prevention of every out-of-band edit. Downstream actors must still inspect current identities before reliance.

## Deployment View

The model remains a local CLI/library within existing distribution boundaries. No new service, database, OS-specific dependency or platform restriction is selected. This change preserves the existing project's execution assumptions and does not add an OS investigation or platform-certification gate. Basic conflict, partial-save and recovery behavior remains subject to normal implementation testing.

Old clients must reject an unknown recording contract; new clients must dispatch historical contracts without changing their meaning. Supporting old contracts does not require extending the old correction engine as a prerequisite to the new recorder.

### Storage replacement inventory

This is the CLI-owned companion to the Workflow model's adoption inventory. The following replacements apply only to `explicit-recording-v1`; existing command handlers, schemas and persisted records retain their registered contracts. A reused implementation helper does not carry its old semantic authority into the new recorder.

| ID | Existing source and exact rule area | Proposed replacement or preservation | New requirement basis |
| --- | --- | --- | --- |
| CLI-MAP-01 | [Compact record contract](../../specs/compact-current-state-change-record.md), SR-19–25 and SR-46: projection, permitted operations, semantic requests, evaluator-derived candidate and milestone transitions | Replace for new contract with record-store commands, explicit candidates and storage-only results. Do not call the old eligibility engine before a record operation. | CLI-SR-01/02/03/07/11 |
| CLI-MAP-02 | Compact record contract, SR-26–31: identities, writer exclusion, multi-file publication, recovery and replay | Preserve safety outcomes with the new revision/read-set, save-safety, explicit recovery and stale-retry rules; do not prescribe OS mechanisms. Existing transaction code is a reuse candidate only. | CLI-SR-04/05/06/08 |
| CLI-MAP-03 | Compact record contract, SR-33 and SR-37–39: path safety, schema identities, YAML/front matter and closed shapes | Preserve fail-closed containment and vocabulary; introduce the explicit-recording schema and exact-byte JSON-subset encoding. Do not widen the old schema to accept new shapes. | CLI-SR-02/03/09/10 |
| CLI-MAP-04 | [Governed lifecycle CLI spec](../../specs/governed-lifecycle-cli.md), R2–5, R7–17, R19–25 and R28: lifecycle commands, effective-state projection, semantic registration/settlement, automatic invalidation and migration | Retain for its historical handlers. New record-store commands reject those contracts; they do not replace `lifecycle` by an alias or use its migration operation. | CLI-SR-01/03/07/10/11 |
| CLI-MAP-05 | [System architecture](../architecture/system/architecture.md), Building Block View → Governed Lifecycle CLI: pure interpretation, transition evaluation and transaction adaptation | Add a contract-separated recording path with no transition evaluator. Keep old engine responsibilities described as historical-contract behavior. | CLI-SR-01–10 |
| CLI-MAP-06 | [Compact schema](../../schemas/compact-current-state-v1.schema.json) and [compact templates](../../templates/compact/current-review.md) with evidence, decisions and Verify siblings | Retain old schema and templates. Author separate new-contract validation/scaffolding from the two model designs during implementation; never reinterpret old front matter. | CLI-SR-02/03/10 and WF-SR-02/10 |
| CLI-MAP-07 | [Metadata validator](../../scripts/validate-change-metadata.py), [metadata regression tests](../../scripts/test-change-metadata-validator.py), [compact canonical-contract tests](../../scripts/test-compact-current-state-canonical-contract.py) | Add explicit contract dispatch and new-record coverage while preserving historical expectations. Split semantic readiness assertions from structural recording checks. | CLI-SR-02/07/10 |

Runtime impact candidates are the [CLI dispatcher](../../packages/rigorloop/dist/bin/rigorloop.js), new record-store parsing/validation/persistence, and compatibility tests. Existing [compact operations](../../packages/rigorloop/dist/lib/compact-operations.js), [eligibility](../../packages/rigorloop/dist/lib/compact-eligibility.js), [projection](../../packages/rigorloop/dist/lib/compact-projection.js) and [transaction code](../../packages/rigorloop/dist/lib/compact-transaction.js) are not deletion targets. Any extracted safety helper must preserve their behavior through regression proof. Exact implementation modules and test files belong to Delivery planning after Design Review; these links identify impact boundaries, not authorization to refactor them now.

Installation, release publication, general observability, cache policy and hosted integrations remain unchanged unless a concrete incompatibility is demonstrated. In particular, the system architecture's CLI Observability and Result Projection section is an integration dependency: the new storage-only result and exit statuses must coexist with its renderer without granting logs lifecycle authority. Any required mapping belongs in this model before implementation, not an unreviewed global renderer change.

## Crosscutting Concepts

### Hard rejection versus observation

| Condition | CLI treatment | Workflow responsibility |
| --- | --- | --- |
| Unknown field in a closed schema, invalid enum or duplicate record ID | Reject structurally | Supply valid explicit data |
| Internal reference names a missing record or finding | Reject structurally | Repair the reference or include the referenced record |
| A check observes a file differing from the caller's expected write/read-set hash | Reject with conflict | Reread and reassess |
| Retained review subject differs from today's model file | Report drift; do not reject solely for that difference | Explicitly assess applicability and correction |
| Caller records completed status while required proof is failed | Preserve explicit data with a visible observation when detectable | Block downstream reliance and correct the decision |
| Requested correction owner was previously completed or is not currently pending | No transition rejection | Route chooses and records justified ownership |
| Caller labels itself reviewer | Treat as attribution, not authenticated permission | Establish actual independent judgment |
| Recovery data is incomplete, unsafe or contradicted by external bytes | Stop recovery | Reconcile safely under explicit authority |

Structural references resolve to record identities; subject hashes describe evaluated content. They must not be conflated. Semantic diagnostics are not a hidden eligibility engine: unknown or undetectable workflow problems are not implied absent by a clean check.

### Boundary scan and acceptance scenarios

These rows use the [Workflow-owned model validation and proof mapping](workflow.md#model-validation-and-proof-mapping). CLI-SR IDs remain local to this model; all eight dimensions apply. Delivery maps these rows and the combined hazards below to concrete checks and evidence. This document does not duplicate the mapping rule or claim that its validator is implemented.

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | CLI-SR-02, CLI-SR-03 | Unknown values and malformed references fail closed; explicit valid replacements preserve supplied semantics. |
| State/lifecycle | CLI-SR-01, CLI-SR-07 | A terminal recorded stage does not prevent safely recording a correction. |
| Identity/authority | CLI-SR-04, CLI-SR-09 | Stale identities and escaped targets reject; role labels confer no execution authority. |
| Composition/path | CLI-SR-05, CLI-SR-09 | Helper and recovery paths cannot bypass protections used by the public command. |
| Temporal/retry | CLI-SR-04, CLI-SR-08 | Competing CLI writers cannot silently overwrite; lost-response retry does not duplicate effects. |
| Failure/recovery | CLI-SR-05, CLI-SR-06 | Interrupted multi-record save yields coherent recovery, never usable mixed state. |
| Compatibility/migration | CLI-SR-10 | A new-contract write cannot reinterpret an old record. |
| External/environment | CLI-SR-04, CLI-SR-06, CLI-SR-09, CLI-SR-11 | Unsafe paths and observed external identity changes stop safely; exact-target edits after the final check are outside the concurrency guarantee. Sensitive payloads stay out of errors. |

Important composed hazards are stale review plus correction recording, concurrent writer plus decision-basis drift, and partial commit plus retry or external edit. CLI-SR-04/05/06/07/08 govern them. Rejecting a conflicting save is a data-safety outcome, not the semantic stage dependency this design removes.

### Observability, security and accessibility

Expose exact result categories and safe path/identity references in text and machine-readable output. Do not require color or a graphical UI. Do not print raw evidence bodies on failure. File permissions, runtime authority and independent reviewer provenance are not supplied by record labels. No telemetry or additional committed operation logs are introduced.

### Performance and limits

Work is bounded by the selected record set and declared decision basis, not project history or network availability. V1 limits are 8 MiB of UTF-8 stdin, 1 MiB per authoritative file, 64 registered supporting records, 65 writes, 256 read-set paths, JSON nesting depth 32 and 1,024 bytes per path. Before/candidate authoritative totals are each bounded by 65 MiB, bounding their combined snapshot payload at 130 MiB plus bounded metadata. Limits apply before allocation or publication where applicable; excess returns limit-exceeded without writes. Decision-basis files are streamed for hashing rather than loaded as request payloads. No latency SLA is claimed. Increasing any limit requires a reviewed contract revision, not an undocumented flag.

## Architecture Decisions

| ID | Decision and rationale | Alternative and consequence |
| --- | --- | --- |
| CLI-DEC-01 | Use explicit replacements plus expected identities, not semantic transition commands. | A richer transition engine can enforce ordering but couples correction writes to workflow state. Explicit replacements require careful callers. |
| CLI-DEC-02 | Separate reference integrity, optimistic concurrency and observed subject drift. | Requiring every old review hash to match today's subject makes invalidation depend on first destroying or falsifying old evidence. |
| CLI-DEC-03 | Preserve transaction machinery as a separately evaluated reuse candidate. | Removing all safety code would simplify code superficially but expose lost updates and partial records. Existing semantic validators cannot be reused unchanged. |
| CLI-DEC-04 | Read operations never repair data; recovery is explicit and mechanical. | Silent recovery during context lookup blurs inspection and mutation and hides interrupted state. |

Decision rationale stays in this model under the approved drafting exception; no separate ADR or implementation change is created.

## Quality Requirements

| Quality | Acceptance condition | Requirement coverage |
| --- | --- | --- |
| Faithful recording | Supplied decisions remain unchanged; no lifecycle field is inferred or added. | CLI-SR-01, CLI-SR-03, CLI-SR-07 |
| Fail-closed input handling | Unknown schema vocabulary and unsafe/dangling references fail before writes. | CLI-SR-02, CLI-SR-09 |
| Concurrency safety | Competing CLI writers are excluded and stale identities reject at the observed checks; simultaneous external target edits are unsupported. | CLI-SR-04 |
| Recoverability | Every interrupted transaction has a verified before/after recovery outcome or an explicit safe stop. | CLI-SR-05, CLI-SR-06 |
| Retry safety | A repeated replacement cannot duplicate workflow effects. | CLI-SR-08 |
| Compatibility and clarity | Old contracts retain identity and every result distinguishes persistence from substantive approval. | CLI-SR-10, CLI-SR-11 |

These are proof obligations for later Delivery allocation, not claims of tests run or behavior implemented.

## Risks and Technical Debt

The main risk is moving the old engine into validators or diagnostics and still blocking correction recording. The inverse risk is callers treating a saved but semantically inconsistent record as readiness; the Workflow model owns preventing that reliance. External edits after the final target check may be overwritten; users must avoid simultaneous manual/tool edits during save or recovery. Observed drift and unknown recovery content still require a safe stop.

The request/result shapes, commands, encoding, revision scope, limits and recovery policy above are proposed Design decisions, not shipped functionality. The storage replacement inventory identifies principal contract and implementation boundaries, not completed adoption diffs. Model validation follows the Workflow-owned mapping; any newly discovered interface gap returns to Design before dependent implementation. There is no OS-lock feasibility prerequisite. Existing historical handlers remain unchanged; this namespace rejects their contracts with unsupported-contract rather than trying to reinterpret them. Independent Design Review assesses adequacy and unnecessary complexity before Delivery planning.

## Glossary

Candidate: explicitly submitted replacement content. Read set: exact inputs on which the caller based its decisions. Conflict: a current identity differs from an expected one. Drift: an observed difference between a record's subject and actual content. Transaction: recoverable publication of a bounded set of replacements. Observation: a fact reported without mutating workflow decisions.

## Next artifacts

Refine these two model designs and their adoption contract before an explicitly authorized independent Design Review. Delivery planning allocates validation and recovery proof after approval.

## Follow-on artifacts

None yet.
