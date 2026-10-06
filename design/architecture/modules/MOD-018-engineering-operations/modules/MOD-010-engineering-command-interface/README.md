# Command interface: current engineering handoff

This defines the `targeted-recording-v2` interface for [v4 current-state records](../MOD-011-operational-record-persistence/README.md), refining SR-006 and SR-040–045 under AR-040. The successor package implements the operational families under the [current CLI contract](command-contract.md); browser-family entries remain designed capabilities. Use the executing package’s capabilities to distinguish availability. This project has explicitly adopted selected operational work; installing the package does not activate customer policy or migrate other work.

## Public task surface

Humans and agents supply goals, authority, scope, judgments and useful evidence. RigorLoop maintains a coherent current handoff, constructs links and performs safe persistence. It does not record every action, choose a semantic next step, run checks on behalf of verification record or infer approval from a save.

```text
rigorloop
├── init <agent>
├── change
│   ├── create
│   ├── context
│   ├── update
│   └── complete
├── review
│   ├── prepare
│   ├── show
│   └── record
├── verification
│   ├── show
│   └── record
├── browser
│   ├── generate
│   ├── check
│   └── recover
└── store
    ├── backup
    ├── restore
    └── migrate
```

Four supporting entries are --help, version, capabilities and logs. The catalogue has twenty entries: sixteen tasks plus these utilities. SQLite owns database transaction recovery; the unimplemented change recover draft is withdrawn. Optional attachments are supplied through existing evidence-bearing tasks, not an additional artifact command family.

## Command syntax and ID scope

Retain `rigorloop <resource> <action> [item-id] [options]`. Operational commands select `--root PATH --change ID`; Change is not an additional positional argument. Review prepare/show/record and verification record take their Change-local item ID. Verification show takes an optional ID. IDs address project → Change → kind → ID; finding IDs additionally require their Review. No cross-Change fallback exists.

Mutation JSON uses `--input -` on stdin, including shell redirection from a caller-owned file. Arbitrary input-path flags are not introduced. `--format text|json` defaults to text. Ordinary mutations admit --dry-run; reads reject it. Help works at root, family and command level without repository access, scope flags or stdin. Unknown/duplicate flags and selector disagreement reject before access.

| Command after rigorloop | Input and effect |
| --- | --- |
| init AGENT | No Change; codex or claude argument. Existing Installation options and replacement authority apply. |
| change create | Explicit initial intent, request, authority and activity; creates one absent Change. |
| change context | Read the seven-section handoff; optional bounded exact selectors through --input -. |
| change update | Explicit related progress, evidence, rationale and retention updates; never review approval or closeout. |
| change complete | Select successful final Verify and provide compact final account; guarded historical closeout. |
| review prepare ID | Assemble/update the current review input; no judgment or automatic reliance. |
| review show ID | Read prepared scope, actual assessment, open issues and current applicability. |
| review record ID | Record assessor-owned judgment, issue dispositions or explicit applicability. |
| verification show [ID] | Read current verification basis, or one exact current Verification account. |
| verification record ID | Save/replace the assessor's Verification and optional actual evidence; no execution or automatic completion. |
| store backup/restore/migrate | Project-level maintenance, explicit input and destination/source expectations; no Change lifecycle authority. |
| browser generate/check/recover | Separate browser-v1 project/input/output contract, no Change. |
| capabilities | --root required, no Change or stdin; actually supported operations and backend availability. |
| logs | No scope/body required; optional --invocation ID selects bounded retained diagnostic events. |
| version | Executing package identity. |
| --help | Usage without repository access. |

Browser generate/recover do not advertise dry-run; check is their read-only comparison. Installation retains its qualified preliminary dry-run. Diagnostics, installation and browser retain separate result domains.

## Successor package and compatibility boundary

The installed executable selects one operational command contract. The successor package implements targeted-recording-v2 / rigorloop-records-v4. Explicitly retained prior executables implement their original targeted-recording-v1 / rigorloop-records-v3 contract for unmigrated work. Overlapping spellings such as review show are interpreted only by that executable's declared contract. Neither repository residue, a missing database nor an input body selects a fallback backend. Help and capabilities identify the executing package's actual contract and operations without claiming customer workflow activation.

The successor rejects v1/v3 operational envelopes and retired recording commands; it does not include a parallel v3 dispatcher or permit live v3 writes. Its explicitly invoked migration adapter may read only qualified legacy formats and preserve selected originals under the migration contract. Before upgrade, the owner preserves access to a qualified prior executable for unfinished v3 work and recovery. A legacy store is never silently upgraded by a read or ordinary write. During migration, old writers must be quiescent because the new package's maintenance fence cannot control them.

Version-scoped v3 guarantees in IF-003/004 and retained contracts describe the preceding executable until its use is retired. They are not promises of simultaneous operation inside the successor. Package installation and explicit per-Change workflow adoption remain distinct; new commands cannot promote old judgments to new approvals. Delivery must prove legacy-input rejection, absent-database behavior, help/capability identity and migration preservation before adoption.

## Admission and version domains

Ordinary mutation envelope is `{schema_version: 2, interface: "targeted-recording-v2", contract: "rigorloop-records-v4", change_id, expected_revision, reads: [Subject], input}`. Revision is an opaque token, null only for absent-Change creation. It need not encode a retained historical revision. The selected task determines input; no arbitrary patch, SQL, raw storage path or nested operation list is admitted. SQLite recovery is internal to opening the store; there is no alternate public record-transaction recovery envelope.

Request JSON and selected query content are each bounded to 1 MiB; a task permits at most 64 supplied engineering entries. Reject overflow explicitly without silently omitting findings or truncating evidence. Payload bytes stream separately under the Records attachment limits. Subject identities are computed by tooling where supported; callers need not hash files. BasisObservation distinguishes reported, compared and unknown support. Mechanical comparison covers selected regular-file bytes only, not semantic adequacy or whole-repository snapshots.

Each retained account must remain retrievable through its smallest supported exact-selector JSON response within 1 MiB, including envelope, metadata, escaping and identity overhead. The storage contract reserves disposition capacity for every retained Issue, so accepting more findings cannot prevent later resolution. Each non-null Issue disposition is limited to 16 KiB of encoded UTF-8 JSON, including actor, reason and follow_up. A task's 64-entry limit is a maximum, not a guarantee that 64 maximum-sized entries fit one account. Check the complete prospective response and reserve before mutation or import; reject excess with size-limit before commitment.

When a Review cannot admit more concerns, use another explicitly prepared Review and keep all unresolved findings visible across retained Reviews. Do not silently replace or compact them. An admitted account retains capacity for every Issue's maximum-sized disposition, including revision of an earlier disposition. Larger supporting explanation can be referenced in a selected source or attachment while the disposition itself preserves the decision-relevant reason and follow-up. An aggregate handoff may still exceed its response limit; return the bounded exact-selector route without claiming full context.

Supporting record input omits engine-owned schema, contract and change_id. The engine builds references and current-state candidates atomically. Optional input sections mean no action when omitted. Different tasks retain their authority boundaries even when they share storage. Role labels cannot authenticate independence or expand permission.

## Public request and result schema

This section is the normative field contract for the successor operational families. Packaged JSON Schema files and parser dispatch implement these envelopes. All listed request members are required unless explicitly optional, unknown members reject, duplicate JSON keys reject, and closed discriminator values reject before cross-field consistency checks. Task-specific semantic fields reuse the existing Records types; no field names a SQL table, database file, transaction handle or stored-row encoding.

| Request family | Transport and field rules |
| --- | --- |
| Ordinary mutation | `--root`, `--change`, `--input -`; Review/Verification item ID is positional. Body has exactly schema_version=2, interface=targeted-recording-v2, contract=rigorloop-records-v4, change_id, expected_revision, reads and input. Body and CLI Change IDs must agree. Creation alone uses null expected_revision. |
| Operational read | Root and Change scope; review show requires its item ID, verification show permits one. change context alone permits its documented optional stdin selector body. Other reads reject an unexpected body, item ID or dry-run. The implementation selects the result contract; it does not copy an untrusted requested version into a response. |
| Store maintenance | Root and `--input -`, no `--change` or item ID. Body has exactly schema_version=1, interface=store-maintenance-v1 and input. Initial versus resume input is exclusive. Expected source/destination observations belong to its task input. |

Root/family/task help and version admission retain their no-project/no-stdin behavior. Resolve known command, flags and selectors before opening project data or consuming stdin. Parse bounded UTF-8 JSON, validate the selected envelope and task fields, then dispatch its normalized typed request through IF-003. A request's actor labels and claimed authority remain supplied facts, not authentication or approval.

Operational JSON results require schema_version=4, interface, operation, status, claim=storage-only, errors, observations, items, changed and committed. interface is the known selected targeted-recording-v2 or store-maintenance-v1 family, never inferred from an unreadable database. operation is the dotted recognized task or null when that task could not be identified. Unknown root/family commands remain under the existing generic CLI error contract. errors and observations are arrays of `{code,message}`; errors is empty on success. items is an array of `{kind,id,value}`; mutation receipts use an empty items array rather than echoing assessments. Read projections retain their task-owned field meanings and explicit completeness/limitations.

changed is `{count, entries: [RecordKey], omitted}` from the storage outcome, or null when individual effects are unknown or a whole-store replacement is not enumerated. Reads, exact no-ops and confirmed precommit rejections use the empty summary. RecordKey is `{kind,id}` and includes review_id for a finding; kind selects an existing record/account, not a SQL table. count equals entries.length plus omitted; ordering is kind, review_id when present, then id. Omitted change detail never hides a failure or truncates an authored finding. The revision identifies the coherent result for subsequent context reads. Mandatory receipts fit the same 1 MiB result limit; optional changed-entry detail is reduced before refusing an otherwise valid write. Read content that cannot fit returns size-limit and a bounded selector route, not silent narrative truncation.

change_id, revision and record_contract are optional result fields, present only when their valid scope/basis is established. Omit unavailable identities instead of setting them to guessed values. The Change-only discovery result additionally requires available_selectors as defined by change context; other results omit it. Maintenance additionally permits store_revision and its defined maintenance object; nested unknown values there use the declared nulls. committed is required and means this invocation's requested authoritative effect: false for read, preview, unchanged and confirmed no commit; true only for confirmed record commit, complete backup publication or activated replacement; null if that outcome cannot be established. It does not mean a previous command never committed. A saved Review result reports persistence, not a new approval supplied by the CLI.

### Outcome mapping

The first error is the primary actionable diagnostic. These are the closed target primary codes; private SQL/OS errors are translated and bounded, with sensitive/raw detail kept out of supported results. Secondary observations use the same codes and explanatory messages; implementation cannot introduce new public codes silently. Stable machine clients branch on code/status/committed, not message wording. invalid-request includes a forbidden transition, unresolved mandatory obligation, invalid typed reference or inconsistent complete candidate; record-missing identifies an absent required account. Neither category supplies an engineering disposition.

| Condition and primary code | status / exit | committed and required behavior |
| --- | --- | --- |
| Successful read | ok / 0 | false; report recorded facts and gaps. |
| Committed mutation/publication | saved / 0 | true; report actual revision and effect scope. |
| Exact no-op | unchanged / 0 | false; fresh expected revision still required. |
| Valid preview | preview / 0 | false; prospective summary grants no reservation. |
| invalid-request, unsupported-contract, unsupported-runtime, size-limit | rejected / 2 | false; no requested authoritative effect. Reject before dependent access where the cause is already knowable. |
| record-missing, project-mismatch, schema-unsupported, payload-unavailable | rejected / 2 | false when known before commit; missing old evidence may instead be an observation while a truthful loss update is saved. |
| revision-conflict, source-conflict, destination-conflict | conflict / 3 | false; preserve newer/unrelated work and require reconciliation. |
| store-busy | busy / 4 | false; no semantic replay. |
| store-unavailable, maintenance-required | recovery-needed / 5 | false if this invocation performed no effect; null for interrupted replacement with unresolved activation. No ordinary transaction complete/restore instruction is inferred. |
| write-failed | failed / 1 | false only when rollback/no publication is established, otherwise null. Never guess no effects after an uncertain commit. |
| output-failed | failed / 1 | Preserve true/false/null already established. When stdout delivery itself fails, a complete JSON envelope may be impossible; emit only the available bounded diagnostic to stderr and keep actual storage state. |
| internal-error | failed / 1 | Actual known commitment or null. No raw SQL exception becomes a public code. |

Recovery in explicitly retained v3 executables keeps its original result semantics; the designed browser-v1 family has its own result contract. Preview's no-write claim concerns engineering records and retained payload publication; temporary admission leases and SQLite journal housekeeping remain storage coordination. An interrupted SQLite write leads to a coherent current read or explicit unavailability. Maintenance resume is the separate project-store task defined below. No status or exit value grants workflow progression.

## Change tasks

### Start work

change create input is `{intent, request, authority, activity, next_action}` using Records types; next_action may be null, visibly not yet decided. Goal, scope, exclusions and authority source/limits are explicit. Missing authority cannot be fabricated; an unknown grant is recorded as such and cannot support dependent action. The command sets empty work, blockers, reviews, attachments and completion_notes, and null selected bases, plan, adoption and completion. These are empty-state defaults, not lifecycle approvals.

An occupied Change ID rejects. First creation may initialize an absent SQLite database only against the explicitly authored project identity described by Records. It does not edit repository design or project configuration. Unknown project/schema or damaged existing storage rejects without replacement. After receipt loss, inspect context instead of guessing whether creation occurred. Independent browser use and installation create no Change. Reads never initialize unavailable operational data.

### Resume and inspect work

change context returns these seven sections from their authoritative records: goal/scope/authority; governing basis; progress; open issues and important rationale; relevant evidence; review standing; next action and reason. Each includes the necessary owner/source, explicit gaps and bounded links to detail. Include unresolved findings from all retained formal and advisory Reviews, even when another Review is selected for the purpose; selection is not issue disposition. It is the primary resumption surface. An earlier accepted Basis whose approval is no longer currently supported retains its recorded decision and exposes an explicit reliance gap. Current evidence summaries are included where needed for the selected work/review decision; bulky attachment bytes are not included.

An optional body is `{schema_version: 2, interface, contract, selectors: [{kind,id}], include_observations: boolean}` with 1–64 selectors. Kind is change, work, blocker, basis, review, evidence, decision, verification, adoption or attachment. Embedded accounts use their Change-local ID; attachment uses its name and returns metadata plus an engine-selected read location for the retained bytes; findings are read with their owning Review. The scoped result reports its limits and cannot claim complete context. Default full context either fits or returns an explicit size-limit result; never hide unresolved work to fit.

The exact Change-only selector with include_observations=false is the guaranteed discovery response. It returns the Change record and a required available_selectors result field containing the complete deterministic list of `{kind,id}` selectors for every retained selectable account, including unselected and advisory Reviews, Work, blockers and attachments. Sort by kind then id; findings remain discoverable within their indexed owning Review. The index is derived from authoritative accounts, not another editable registry. Its complete encoded response, including the Change's Issue disposition reserve, must fit 1 MiB; every mutation/import enforces that additional candidate invariant.

A full-context size-limit diagnostic gives the exact Change-only selector body for the known requested Change. The caller obtains that bounded complete index, then retrieves individual accounts. Each account's smallest response is also admission-bounded. This route exposes all retained Review identities without truncation, hidden obligations, guessed IDs or a pagination protocol. If adding an account would overflow the discovery response, reject before commitment; existing accounts and their discovery route remain intact.

For a completed Change, default context presents its compact historical completion and explicit notes. It does not compare completion subjects with current files, report ongoing applicability or infer current system health. Missing deliberately discarded detail is different from corruption of required retained data. Reads can report selected attachment availability without reassessing the completed product.

### Record progress and engineering outputs

change update accepts a nonempty selection of the following sections. One task may record a useful handoff after several local runs; no run-by-run summary is required.

| Section | Effect and boundary |
| --- | --- |
| intent, request, authority, activity, next_action | Replace the explicitly selected current account. Authority changes require an attributable actual source; editing text grants no permission. |
| work | Add/replace named Work accounts, preserving omitted neighbors. Completed/cancelled work includes reason. |
| evidence | Add/replace comparable Evidence summaries, optionally with attachments. Procedure and relevant scope cannot silently change under an existing ID. |
| decisions | Add/replace current important rationale. No repository definition is edited by the command. |
| blockers | Add/update named Issue accounts. Omitted issues persist; non-open state requires explicit disposition. |
| basis | One `{id, kind, decision, selection, actor, rationale, review}` outcome. Selection is explicit present/absent paths; the CLI observes Subjects and selects the Basis. Creating or replacing acceptance requires the actual current formal approved Review of those subjects; no Function/AR completion prerequisite for requirements. |
| plan | Select a present Path or explicitly clear with null; selecting does not approve it. |
| adoption | Current explicit Adoption account; prepared saves facts only, activated selects, unavailable clears. Governance compatibility conditions still apply. |
| retention | `{drop: [{kind,id}], reason, actor}` explicitly compacts unused detail. Kind is basis, review, evidence, decision, verification, adoption, work, blocker or attachment; attachment ID is its name, including an explicitly selected unused managed file left by a failed save. Cleanup rechecks references and in-flight publication under SQLite writer exclusion. Refuse open issues, unresolved obligations and surviving dependencies. Active Changes protect selected records and work; disposed Review findings use their owning review task. Closed compaction may remove terminal work and clear obsolete selectors for dropped records under the Records completion rules. |
| completion_note | `{actor, reason, explanation}` annotates an error in an original completed account without silently changing it. |

No section can author Review or Verification conclusions or set completion. In a completed Change, only completion_note and safe retention changes are admitted. A later regression starts a new Change, linked by its request locator; it does not reopen or continuously qualify the old completion.

Evidence replacement updates current work support. The engine preserves assessment-owned support summaries and exposes affected dependencies. It marks selected reviews needs-reassessment and persists Verification support_state changes under the [Records dependency rules](../MOD-011-operational-record-persistence/README.md#updating-current-state-without-losing-decision-meaning). The same rules apply to review tasks and other relevant completion-input changes, not just evidence replacement. Only an explicit verifier assessment can renew affected Verify support; a newer approval at the same Review ID cannot renew it implicitly. An exact no-op does not invalidate anything. Omission cannot make a failure disappear. The actor decides comparability and semantic impact; closed fields and references cannot prove those judgments.

### Optional attachment input

Evidence input may include `retain: [{name, source, media_type}]` as a task-only field in addition to its stored attachment-name references. Source is a contained project-relative regular file selected by the caller, not a destination. The CLI stages bytes and builds the named Attachment metadata and Evidence references together. Existing retained attachments can be selected by name without resupplying source bytes. Attachment names cannot silently overwrite retained content.

Keep routine logs caller-owned and replaceable. Retain only outputs needed for an unresolved issue, important rationale or selected acceptance support. Failed record publication may leave an unreferenced retained copy; expose that outcome and use byte-checked orphan reuse or guarded cleanup, never claim a record saved. Dry-run reads/admit-checks sources but retains no payloads. Missing old attachments do not prevent recording their loss; they do prevent a new unsupported claim of availability. [Records](../MOD-011-operational-record-persistence/README.md#selective-attachments) owns limits, naming, cleanup and physical placement.

### Complete the Change

change complete input is `{actor, verification: ID, summary, reason, delivered_scope, governing_references: [Text], limitations: [Text], retained_attachments: [name]}`. The CLI assembles acceptance entries from the selected actual assessment summaries, including accountable sources and scope, and atomically records Completion with verify/completed activity. The actor confirms that these summaries adequately support the declaration; persistence invents no judgment. Full logs are optional.

Before first closeout, expose accepted governing bases, reviewed delivery intent, current whole-change approval, applicable final-success Verification, completed or explicitly cancelled work and issue dispositions. Refuse unfinished work, open issues, unsupported mandatory deferrals, missing necessary support or unknown applicability. Where applicability is actor-reported, label it as such; current repository observations do not prove independence or adequacy. Evidence-only retries require no automatic extra review; material changes return to the appropriate owner and assessment.

Completion is a historical declaration. Exact input retry after the ordinary current revision guard is unchanged and does not recheck old subjects against today's repository. Compare the supplied fields, including verification against Completion.verification_id, even when working support has been compacted. Differing completion payload rejects; an original-account error uses an explicit note. Store enough acceptance meaning in Completion that superseded working records can later be compacted safely. Carry any accepted deferred follow-up into that account before dropping its working issue. Completion is not an archive of all activity, an external publication grant or a permanent health assertion.

### Inspect after an interrupted write

After interruption or response loss, read change context before reconciling a retry. MOD-011 opens the associated SQLite database, lets SQLite establish its transaction state and returns a coherent snapshot or a precise inability to read one. Database recovery does not rerun engineering work, replay the previous update or choose an assessment. Reads never initialize/migrate the store, modify engineering accounts or clean attachments; SQLite's internal journal housekeeping is not a semantic record mutation.

The proposed change recover command and its complete/restore/finish envelope are removed. A normal SQLite transaction does not need the caller to choose which record files to restore. Missing/corrupt stores, incompatible schemas and explicit backup restoration remain maintenance concerns under SR-074–077, through the store maintenance interface below, whose runtime qualification is required before adoption. They are not hidden fallback behavior in ordinary tasks. Browser recover remains a separate operation for browser output publication; supported v3 record-store recovery keeps its original versioned contract.

The result identifies what is known about the save. A confirmed commit survives response failure. An unknown outcome stays committed null until current inspection establishes available facts; matching IDs alone do not supply a permanent historical receipt. Reconcile against the latest revision rather than retrying stale intent. Optional unused attachment cleanup remains an explicit retention task under the Records writer-coordination rules.

## Preparing and reading review input

### Preparation

review prepare ID input is `{purpose, scope, selection: [{path,state}], basis_refs: [Ref], plan_path: Path or null, coverage_rationale, description, actor}`; description is a nonempty scope explanation. Purpose is requirements, design, delivery or code; scope is formal or advisory (advisory is code-only). Selection contains distinct explicit file paths, not globs or directories. When plan_path is non-null, that path must be included in the selection. The engine constructs ReviewInput and a Review with null assessment when absent, or updates the prepared input for the same-purpose existing Review. It creates no judgment. New or changed input has needs-reassessment applicability; unchanged preparation preserves standing. No Candidate, gate record or predecessor chain is created.

A Review's assessment retains what was actually reviewed while its prepared scope identifies what is currently offered. Source copies and mechanical identities for every repository file are not required. The actor must make missing comparison support explicit; current file names and timestamps alone never prove what was assessed.

### Read the review

review show ID returns the current prepared input, actual assessment if recorded, applicability, selected formal-purpose standing, unresolved relevant findings and support summaries. It distinguishes not-recorded from approval, and actor-reported unchanged scope from mechanical comparison. It does not return or promise a complete attempt history. Evidence and named retained attachments have bounded follow-up references.

### Record an assessment, finding or reliance decision

review record ID accepts optional `assessment`, `findings`, `applicability` and `compact_findings`, with at least one supplied. Assessment uses the complete assessor-owned Records fields; findings are Issue accounts updated by ID with omission preserving others. compact_findings is `{ids, actor, reason}` for explicitly disposed findings no longer required by current reliance. It cannot remove open issues. New assessment does not silently clear earlier issues or make an advisory Review formal.

An explicit formal assessment selects that Review as the purpose's current account, but approval does not automatically select current applicability. A changed assessment resets applicability to needs-reassessment unless the same task explicitly supplies a valid disposition; an old current label is not inherited. Applicability input uses the Records fields. Current requires an actual approved formal assessment, adequate scope and a responsible impact disposition. A harmless edit can retain its assessed conclusion with cumulative comparison and rationale; material changes require independent reassessment. Assessment replacement preserves the open-issue set and support still needed by the new conclusion; superseded intermediate reports need no permanent copies. Reviewer provenance is supplied, not inferred from a role label.

All sections commit together. Historical or adverse assessment facts can be recorded without falsely asserting current applicability. The expected revision protects concurrent updates. For receipt uncertainty, read current context before resubmitting; only an identical current account is unchanged. Never replay old mutable intent against a newer revision merely because an ID matches.

### Review recording walkthrough

This is a synthetic customer example, not an assessment of this repository. Paths, actors and revision tokens are illustrative. Assume chg-123 already has accepted requirement/design bases, reviewed delivery intent, completed implementation, navigation-checks Evidence and a prepared formal code Review rev-001 covering the complete delivered scope. There are no open findings and no final Verification yet. Reviewer B supplies the judgment after independent assessment; neither the skill label nor the CLI establishes independence.

Read current context and review input first, then submit the explicit assessment:

```bash
rigorloop change context --root . --change chg-123 --format json
rigorloop review show rev-001 --root . --change chg-123 --format json
rigorloop review record rev-001 --root . --change chg-123 --input - --format json < review.json
```

The caller-owned review.json contains the following complete request. Use the actual opaque revision returned by the read. Empty reads requests no additional mechanical comparison; null subject identities and the reported observation do not claim unchanged bytes.

```json
{
  "schema_version": 2,
  "interface": "targeted-recording-v2",
  "contract": "rigorloop-records-v4",
  "change_id": "chg-123",
  "expected_revision": "opaque-token-from-context",
  "reads": [],
  "input": {
    "assessment": {
      "reviewer": {
        "id": "reviewer-b",
        "role": "review"
      },
      "contributors": [],
      "independence_basis": "Reviewer B did not author the delivered change.",
      "judgment": "approved",
      "assessed_subjects": [
        {
          "path": "src/navigation.js",
          "state": "present",
          "identity": null
        },
        {
          "path": "tests/navigation.test.js",
          "state": "present",
          "identity": null
        }
      ],
      "governing_basis": [
        {
          "path": "design/browser.md",
          "state": "present",
          "identity": null
        }
      ],
      "summary": "Navigation and its interactions satisfy the reviewed browser design.",
      "rationale": [
        "Reviewed the complete delivered scope and the relevant checks."
      ],
      "limitations": [
        "Publication was excluded from this Change."
      ],
      "evidence_refs": [
        {
          "kind": "evidence",
          "id": "navigation-checks"
        }
      ],
      "support": [
        {
          "source": {
            "kind": "evidence",
            "id": "navigation-checks"
          },
          "scope": "View selection and navigation links",
          "basis": [
            {
              "path": "src/navigation.js",
              "state": "present",
              "identity": null
            }
          ],
          "result": "passed",
          "explanation": "Reported navigation checks cover the delivered behavior.",
          "limitations": [
            "The reviewer assessed the reported result; no byte comparison was requested."
          ],
          "attachments": []
        }
      ]
    },
    "findings": [],
    "applicability": {
      "value": "current",
      "actor": {
        "id": "reviewer-b",
        "role": "review"
      },
      "rationale": "The reviewed candidate is the complete delivered scope; no subsequent relevant changes were reported.",
      "observation": {
        "method": "reported",
        "actor": {
          "id": "reviewer-b",
          "role": "review"
        },
        "scope": "Delivered navigation implementation and checks",
        "summary": "Current applicability is reported by the reviewer, not mechanically established."
      }
    }
  }
}
```

Findings is empty because this example adds none. It does not erase existing findings; an unresolved issue would still require its explicit owned disposition before current approval could be relied on. On the stated initial conditions, storage updates the Review and the Change's selected formal code-review account together. A complete illustrative JSON receipt is:

```json
{
  "schema_version": 4,
  "interface": "targeted-recording-v2",
  "operation": "review.record",
  "status": "saved",
  "claim": "storage-only",
  "errors": [],
  "observations": [],
  "items": [],
  "changed": {
    "count": 2,
    "entries": [
      {
        "kind": "change",
        "id": "chg-123"
      },
      {
        "kind": "review",
        "id": "rev-001"
      }
    ],
    "omitted": 0
  },
  "committed": true,
  "change_id": "chg-123",
  "revision": "opaque-token-returned-after-save",
  "record_contract": "rigorloop-records-v4"
}
```

The Change is still active. Saved means the assessor's submitted conclusion was persisted, not that RigorLoop performed review or Verify. The responsible actor may now select authorized final Verify after checking the other prerequisites; change complete remains separate. This example implies neither automatic stage advancement nor publication authority.

| Alternative outcome | Caller response |
| --- | --- |
| invalid-request or missing Review/Evidence | Correct the explicit input or obtain the missing basis; no assessment is invented. |
| revision-conflict | Read context and reconcile with newer work before a new submission. |
| store-busy | Wait or inspect coordination, then read current context before reconciling intent. |
| write-failed with committed=false | Previous records remain authoritative; correct the cause and reread before retry. |
| output-failed with committed=true, or no usable response | Read current context to discover saved facts. Do not assume rollback or automatically replay the assessment. |
| committed=null | Treat the effect as unknown until a coherent read or qualified maintenance establishes it. |

The parent [review-recording sequence](../../README.md#record-a-review-assessment) shows this request crossing IF-004 and IF-003. It is a design walkthrough; executable schemas, dispatch and runtime proof remain implementation work.

## Verification tasks

verification show without ID assembles current governing basis, delivery and whole-change review standing, work, open issues, relevant evidence and explicit support gaps. With ID it reads that exact current Verification account, including persisted support_state, and its limits. A successful outcome with needs-reassessment support is shown as the recorded conclusion with a current support gap; it does not qualify closeout. It does not execute tests or select the latest favorable result by timestamp.

verification record ID accepts `{assessment, evidence}` where evidence is optional and assessment contains the assessor-owned Records Verification fields, excluding engine-maintained support_state. It can add or replace the current assessment and related actual evidence, including optional retain inputs, atomically. Resolve evidence updates and dependency effects first, then admit the explicit assessment against that complete candidate. A combined task cannot renew support while leaving a required Review needs-reassessment. Final success requires applicable whole-change approval and adequately supported completion scope; scoped, failed and inconclusive assessments remain recordable. The verifier supplies the outcome, support summaries and applicability observation, including the disposition of changed support when renewing an existing account. The engine sets current for that admitted assessment. Recording runs no checks or fixes and does not close the Change. Replaced working evidence or Reviews cannot silently change a saved Verification's assessed support; renewed reliance needs the verifier's explicit assessment, without automatically repeating unaffected tests.

## Store maintenance

These three project-level tasks preserve or deliberately replace operational storage. They use `--root PATH --input - --format text|json`; `--dry-run` validates and reports intended scope without record, backup-output or replacement writes. It can use temporary admission leases and returns no reservation. The request is read from stdin, optionally redirected from a caller-owned JSON file; input filename flags are rejected consistently with ordinary mutations. They do not accept `--change`, raw SQL or arbitrary record patches. The separate input envelope is `{schema_version: 1, interface: "store-maintenance-v1", input}`; the task determines the closed input shape.

| Task | Input and meaning |
| --- | --- |
| store backup | `{scope: {changes: "all" or [ID]}, output: Path, actor}`. A nonempty explicit list selects complete currently retained Changes and their attachments. Output is an absent backup directory outside active database/managed attachment paths. Result declares included/excluded scope and integrity. |
| store restore | `{backup: Path, expected_backup: Digest, expected_store: StoreExpectation, replace: boolean, actor, reason}`. Validate a complete compatible backup and explicitly activate its declared scope. Empty destination requires replace=false and absent expectation; occupied destination requires replace=true and a current destination observation. No merge or project-ID rewriting. |
| store migrate | `{mode, expected_store: StoreExpectation, actor, reason, ...mode_fields}`. Mode is schema-upgrade or legacy-import; unknown modes reject. Upgrade fields are `{target_schema: integer, backup_output: Path}`. Import fields are `{source_contract, source_root: Path, changes: [ID], expected_source: Digest, originals_output: Path, dispositions: [SourceDisposition]}`. Only packaged supported source adapters/ordered upgrades are admitted. |

Maintenance Paths are explicitly supplied local paths, allowed outside the project for backup/transfer, normalized and checked against active storage and unrelated occupied output. They are not the contained repository Subject Path type. Digest is a tagged SHA-256 observation of the selected manifest or source set, not an attachment name. StoreExpectation is `{kind: absent}` or `{kind: current, revision: Text}` or `{kind: unavailable, observation: Digest}`; the last is restore-only and identifies the exact inaccessible destination set without pretending to have a coherent database revision.

SourceDisposition is `{source_record: Text, action: import or retain or block, reason: Text, target: {change_id, kind, id, parent_id: ID or null} or null}`. Target kinds are the existing record kinds plus change, work, blocker and finding; finding requires its Review parent. It identifies the qualified source record and its intended meaning under the supported adapter, not a SQL table operation. Blocked records prevent activation. Retained originals cannot hide unresolved active dependencies. Migration dry-run returns classified source observations and their digest so the caller can supply an exact expected_source; an execution rechecks them. Null expected_source is accepted only for that inspection preview, never publication. Legacy import requires an absent SQLite destination and an absent originals output. Schema upgrade requires a current store expectation and creates its coherent pre-upgrade backup before replacement. Import does not delete or edit source records.

To resume an interrupted maintenance operation, use its original store task with input `{resume: {operation_id, expected_observation, action}, actor, reason}` instead of a new request. action is finish or rollback; rollback is prohibited after activated replacement or complete backup publication. For backup, finish only validates/publishes the already complete captured candidate; missing capture data requires rollback of identified incomplete staging and a new explicit backup request. Backup rollback removes only owned unactivated staging and its fence, preserving the source and existing backups. A failed or stale recovery observation stops without overwrite. capabilities can expose the active maintenance ID, original task, phase and manifest observation while ordinary access is fenced. No caller-selected record-transaction repair task is reintroduced.

Capabilities also reports `store` as `{state, revision, observation, database_schema, maintenance}`: state is absent, ready, unavailable or maintenance; unavailable identities stay null unless actually observed. revision is a current whole-store token only for ready state; observation is an exact bounded filesystem/maintenance observation when available, otherwise null. database_schema is null when unknown. maintenance is null or `{operation_id, task, phase, observation}`. These facts support explicit maintenance admission and do not infer engineering readiness. Every replacement rechecks its expected state under exclusion; receiving a token does not reserve the store.

Maintenance uses the common result envelope with interface store-maintenance-v1 and optional `store_revision` and `maintenance` fields. maintenance reports `{operation_id, phase, output, retained_prior, scope, integrity, limitations}` with unavailable values null; phases are prepared, activated, complete or unavailable, never inferred approval. Backup committed=true means a complete backup output was durably published; restore/migrate committed=true means replacement activation was established. Failure after either boundary preserves that truth, and uncertain outcomes use committed=null. A failed partial replacement remains fenced and recovery-needed, not an empty ready store. Output failure never repeats replacement automatically. [Records](../MOD-011-operational-record-persistence/README.md#database-schema-backup-and-migration) owns format, exclusion, integrity, staged activation and recovery behavior.

The [owning maintenance cooperation](../MOD-011-operational-record-persistence/README.md#maintenance-cooperation-and-preserved-scope) composes these existing operations for SR-074–077. Transfer uses backup plus same-project restoration into an empty operational destination; occupied history is a conflict, not an implicit merge. Migration requires source-owner quiescence through activation, verified originals and explicit reconciliation of current consumers. These are storage and participant responsibilities, not additional request fields or automatic authority supplied by parsing.

## Supporting commands

init AGENT delegates to IF-006 and the existing [Installation contract](../../../MOD-019-product-delivery/modules/MOD-014-verified-skill-installation/installation.md). --force and --dry-run retain their qualified meanings. A successful installation does not activate workflow policy.

capabilities --root PATH reports `{interface, record_contract, workflow_contract, operations: [Text], backend_available: boolean, limitation: Text or null, identity, store}` for the executing implementation. Operations list only actually supported spellings, sorted; identity is the canonical capability-description digest for compatibility, not an attachment identifier. Unimplemented target commands are never advertised by the current runtime.

logs returns the configured diagnostic location; --invocation ID selects bounded events under the existing privacy/retention contract. Diagnostics are not mandatory engineering activity records. Version and help remain informational; none grants authority or chooses workflow.

## Result, retry and preservation

The [public result schema](#public-request-and-result-schema) and [outcome mapping](#outcome-mapping) own fields, diagnostics and exit behavior. A recovery-needed result requests investigation or qualified maintenance; it is not an instruction to invoke the withdrawn change recover draft and carries no invented record-transaction repair token.

Updates are atomic per Change and preserve omitted neighbors. A stale revision requires rereading and reconciling intent. No automatic merge, semantic replay or permanent previous-revision archive is required. Store maintenance uses its distinct whole-store expectation and activation boundary. Artifact publication may precede record commit; an orphan does not imply a saved record. Read limits are explicit. Reads never initialize, migrate, compact or replay engineering state; SQLite may perform database-internal recovery when opening the store.

For an ordinary committed task, [MOD-011's final basis observation](../MOD-011-operational-record-persistence/README.md#atomic-publication-and-recovery) can report source drift or an unestablished comparison after commitment. Preserve saved, committed=true, the committed revision and exit 0, with source-conflict in observations and no invented precommit error. The bounded observation directs current inspection and renewed applicability assessment; it does not declare a new judgment or authorize replay. Prepare room for that mandatory summary before commit, reducing optional detail as needed. Human and JSON results retain the same commitment and limitation; unavailable output delivery follows the existing output-failed rule.

## Disposition of earlier drafts

The earlier unimplemented v4 Candidate/Applicability/FindingUpdate chains and immutable-per-attempt requirement are replaced by current review input, assessment, applicability and issue accounts. Supporting record kinds are not a public command taxonomy. Existing v1/v3 runtime names and historical sources retain their original contract until coordinated replacement. No compatibility aliases for superseded drafts are introduced.

SR-074–078 separately own backup, restoration, transfer, migration and bounded discovery of retained history. Normal recording does not have to retain all history to satisfy those selected-scope operations. Ordinary optional attachment ingestion is specified here and no longer depends on an unspecified import tool. The selected store maintenance tasks and node:sqlite binding must be qualified before runtime adoption. Ordinary transaction recovery is supplied by SQLite and does not add a public record-recovery task.

## Walkthroughs and acceptance intent

| Situation | Intended observation |
| --- | --- |
| Another agent resumes tomorrow | Seven-section context identifies the authorized next step, supporting facts, missing review and uncertainty without conversation history. |
| Three development test runs | Only the latest relevant result need be recorded. Earlier failures remain only if they explain an unresolved issue or important decision. |
| Smoke pass follows integration failure | The different scope cannot replace/hide the failure. The current handoff retains the issue. |
| Reviewer reassesses a correction | Update current standing within one gate; an omitted open finding persists. Explicit resolution permits later compaction. |
| Evidence changes after approval | Preserve assessed support and expose the affected reliance; actor judges impact rather than storage retargeting approval. |
| A referenced Review is replaced after successful Verify | Persist needs-reassessment Verify support, even if the replacement Review is current; the verifier explicitly reassesses before closeout. |
| Two actors update | The stale revision rejects without losing the winning update or requiring a permanent version history. |
| Optional report retention | Copy the selected source through the supported task; a failed record commit leaves at most an identified orphan. |
| Interrupted record write | Open SQLite and inspect coherent current context; reconcile against its revision without replay. Unavailable storage is explicit and may require qualified maintenance. |
| Completion then later regression | Historical account stays unchanged without current-file comparison; new work links back through its request source. |
| Compact completed work and retry closeout | Remove an explicit unused working set and obsolete selectors together; preserve surviving dependencies and compare the historical Verification ID without reopening repository checks. |

A browser Change can therefore move from navigation incomplete to implemented/checks passed in one useful progress update after local iteration. Whole-change Review records its conclusion; Verify records distinct acceptance support; change complete retains a compact account and only selected attachments. External publication remains separately authorized. There is no requirement to keep three run summaries or every revised handoff.

[Operations test design](../../test-design.md) owns integrated observations. Existing structural/projection/browser checks protect model and presentation consistency only. Parser, persistence, recovery, concurrency and authority behavior remain future implementation proof. No new runtime tests are added merely to stabilize this design.

## Browser command family


The proposed `browser-v1` family realizes [IF-012](../../../../interfaces/IF-012-qualified-architecture-snapshot-generation/interface.json). It is separate from `targeted-recording-v2`; no Change creation, lifecycle approval or SQL access occurs. Proposed invocations are `rigorloop browser generate`, `rigorloop browser check` and `rigorloop browser recover`. These names are target design, not available commands or entries in the observed command catalogue.

RigorLoop's own repository is the first consumer of this same packaged boundary. Its thin generation wrapper supplies explicit project, immutable selection and output inputs; there is no repository-only command mode or bypass of capture/publication checks. The initial profile identifies one fixed supported model contract. Additional configurable profiles and independently distributed templates are outside the first adoption; unknown profiles still reject. [MOD-004's first-project design](../../../MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/README.md#rigorloop-as-the-first-supported-project) owns projection and migration boundaries; packaging qualifies the actual installed candidate.

The existing Node JavaScript ESM command layer is a thin adapter to the packaged Rust browser engine under [the technology decision](../../../MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/README.md#technology-decision). Preserve the public CLI and existing unrelated commands. Node owns argument admission, platform/resource checks, shell-free child launch, cancellation and result presentation. The engine owns model interpretation, generation and output mutation/recovery. The repository wrapper invokes this same public boundary rather than launching a different engine directly.

Use the bounded internal `browser-engine-v1` JSON request/result protocol with exact request and resource identities. Do not expose it as another supported customer command or equate its version with public `browser-v1`. Reject mismatched/unknown protocol results before reliance. A child launch failure before execution may establish no engine mutation; termination, malformed output or response loss after launch cannot establish precommit failure. For a potentially mutating operation, preserve the selected output/request identity and report `recovery-required` unless a valid result establishes the actual outcome. Never silently retry, erase recovery state or convert a child exit status into a successful generation claim. Check-mode failures retain their nonmutating meaning.

`generate` requires explicit project/profile, immutable input selection and output. Replacing an existing owned output also requires explicit replacement intent and exact expected current entry identity. `check` compares the same source/tool scope and existing output without mutation. `recover` requires the specific owned output, interrupted operation identity, expected state and bounded recovery disposition; it does not replay generation against newly read facts. Output selection and supported platform/renderer compatibility are admitted before any writer acquisition. Never default to the nearest operational Change or database.

Results identify `browser-v1`, operation, project/profile, captured input identity when available, generator/renderer resource identity, selected output, actual commit identity, diagnostics and unresolved scope. The closed outcome set is `generated`, `current`, `stale`, `recovered`, `rejected`, `failed`, `committed-with-reporting-failure` and `recovery-required`. `generated` applies only after complete generation commitment; `current`/`stale` are check outcomes, not quality judgments; recovery reports the actual selected version. Reject unknown operations/outcomes before consistency checks. Publication, verification success and review approval are never inferred from these values.

The exact machine serialization and platform-specific interruption mechanisms must conform to this semantic contract when implemented; this does not add a schema to the currently supported CLI. Evidence must cover incompatible dependencies before writes, absent/stale expected identity, safe output boundaries, check-mode nonmutation and truthful post-commit failure. MOD-004 owns output recovery, MOD-010 preserves its outcome; neither owner silently repairs source definitions.

### Proposed subject-history query

[The shared history contract](../MOD-011-operational-record-persistence/history-selection.md) defines AR-087 admission, literal filters, bounded output and failure presentation through IF-004/003. This separate proposed operation does not extend the current command catalogue, targeted-recording-v2 fields or ordinary no-cursor results. MOD-011 owns identity association, state and selection; MOD-010 preserves their exact outcomes.

## Supporting contracts

These documents retain detailed clauses and proof under this Module; they are not additional REM entities.

- [Command interface](command-contract.md)
