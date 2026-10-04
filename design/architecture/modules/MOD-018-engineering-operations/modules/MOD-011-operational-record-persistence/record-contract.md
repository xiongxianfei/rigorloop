# Operational records

Owner: [MOD-011 Work record storage](module.json). This is supporting contract detail, not a separate REM entity. Source-qualified clause IDs retain their existing meaning.

Model validation contract: model-document-v1

[Work records (MOD-011)](README.md) owns the current `rigorloop-records-v4` model, SQLite realization, selective payloads and maintenance contract. [The v4 schema](../../../../../../schemas/rigorloop-records-v4.schema.json) defines record values. [CLI](../MOD-010-engineering-command-interface/command-contract.md) exposes engineering tasks; [Workflow](../../../MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/workflow.md) and [Review and Closeout](../../../MOD-017-engineering-governance/modules/MOD-007-engineering-verification-and-assurance/assessment.md) own decisions.

## Storage ownership

| Information | Authority and location |
| --- | --- |
| Current IR/SR/AR, Feature, Scenario, Function, Module, Interface, implementation and applicable rationale | Repository engineering definition, portable in Git |
| Current Change handoff, Review/Finding, Evidence metadata, Decision, Verification and Adoption | Project-local `.rigorloop/rigorloop.db` |
| Explicitly retained large reports/attachments | Named files under `.rigorloop/artifacts/changes/`, referenced by records |
| Backup/import originals and interrupted replacement state | Explicit selected preservation and recovery scope |

The entire `.rigorloop/` runtime directory stays outside Git. Project-owned `.rigorloop.json` declares the stable UUID shared by configuration and database. Reads never initialize, migrate or select a recovery outcome. A mismatched, corrupt or unsupported store is unavailable; it must not be replaced with an empty store merely to proceed.

## Current state and support

Active work maintains enough information for a new actor to identify the next sound authorized action without reconstructing conversation or all activity. Comparable current Evidence may replace an older working account. Open obligations survive omission and require explicit disposition. Assessment attribution, actual scope and concise support preserve the meaning of judgments still relied upon. Old detailed logs are not mandatory.

SQLite transactions make a complete account update atomic and opaque Change revisions protect against stale writers. Lost output does not imply rollback: inspect coherent current state before reconciling another request. Do not replay old intent automatically. Attachment publication can leave an unused file after a failed record commit; explicit cleanup checks current references before removing only selected unused payloads.

Completion stores a compact historical account with supporting review/Verify conclusions, limits and selected attachments. It does not continuously track the current system. Safe explicit compaction may remove unused working detail while preserving completion, unresolved obligations and retained dependencies.

## Durability and compatibility

Use the qualified Node/SQLite profile, WAL, full synchronization and foreign keys. A live database and its sidecars are one operational state; backup uses SQLite's backup API plus selected payload capture under maintenance exclusion. Restore validates a complete bundle and preserves displaced bytes before staged activation. Interrupted replacement stays fenced for an explicit observed finish/rollback request; activated replacement cannot be undone as a retry.

Legacy import admits only qualified source versions and explicit per-record dispositions. Source bytes remain unchanged and required originals are preserved externally. Missing registered content, unresolved source transactions, hidden obligations or incompatible judgment mappings block activation. No dual writes or filesystem v4 adapter are supported. Prior v3 shapes and procedures are recoverable at commit `39be9c81`, path `docs/design/cli/records.md`; their historical meaning remains unchanged.

## Requirements

These stable local references reconcile the prior document contract with the current REM and Module owners linked above. They do not retain the superseded workflow or filesystem interface.

| ID | Required behavior |
| --- | --- |
| RF-SR-01 | Stored operational facts MUST conform to the closed rigorloop-records-v4 types. Unknown fields, values, versions, duplicate identities and malformed internal references MUST reject before authoritative mutation. |
| RF-SR-02 | SQLite MUST own the current semantic records and their relationships. Supporting IDs are Change-local; references MUST select one admissible typed object. Files outside selected retained attachment metadata MUST NOT become authority by discovery. |
| RF-SR-03 | Records MUST preserve actor-supplied subjects, provenance, decisions and narrative without inferring approval, applicability or completion. Finding and blocker identity and disposition representation MUST retain the distinction between reporter and correction owner. |
| RF-SR-04 | Open issues MUST retain stable identity, reporter, meaningful basis, required outcome, owner and explicit disposition. Omission or replacement of an assessment MUST NOT erase unresolved obligations. |
| RF-SR-05 | Structural validity MUST remain separate from workflow adequacy. A completed activity, failed evidence or changed external subject MUST NOT alone invalidate a correction candidate; malformed internal references still reject. |
| RF-SR-06 | The successor runtime MUST use rigorloop-records-v4 directly in SQLite. Earlier contracts are admissible only through qualified explicit import with source preservation and complete disposition; no legacy writer or filesystem v4 adapter is supported. |
| RF-SR-07 | Selected reads MUST expose sufficient current handoff and assessment support, including limitations, findings, evidence and compact completion. Projection MUST NOT create a second authoritative record. |
| RF-SR-08 | Ordinary updates MUST be atomic SQLite transactions. Backup, restore and import MUST validate the complete selected record set and retained payloads; interrupted replacement remains fenced for explicit observed recovery. |
| RF-SR-09 | Creation MUST declare the stable project identity and new v4 Change without inferring engineering acceptance. Supporting record types use their closed schemas and retain actual assessor/basis/judgment attribution. |
| RF-SR-10 | Updates MUST preserve omitted meaning and narrative values; comparable working evidence may be replaced. Retention is selective, not blanket append-only history. |
| RF-SR-11 | Evidence and assessments MUST identify their actual reported or compared basis honestly. No universal Git identity or mandatory per-file hashing is required; compared claims require actual supported comparison. |
| RF-SR-12 | Legacy import MUST leave source bytes unchanged, preserve required originals outside the operational store and reject unsupported, incomplete or conflicting sources. Historical judgments MUST NOT be promoted. |
| RF-SR-13 | Findings and blockers MUST survive omission until explicit justified disposition. Current judgments preserve their meaning, attribution and relied-upon support even when replaceable working detail is compacted. |
| RF-SR-14 | Completion MUST preserve a compact delivered outcome and acceptance basis. Later current-system changes MUST NOT continuously invalidate that historical account. Explicit completion corrections and linked later work remain distinguishable. |

### Boundary scan and acceptance scenarios

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | RF-SR-01 | Unknown contracts, malformed references or unsupported scope stop the affected operation without inferred defaults. |
| State/lifecycle | RF-SR-01 | Progress, accepted basis, review judgment, final Verify and historical completion remain distinct; saved state alone advances none. |
| Identity/authority | RF-SR-01 | The actual responsible actor, declared scope and current support govern reliance; an identifier or role label does not establish authority. |
| Composition/path | RF-SR-01 | Changed producer and consumer contracts are reconciled together, including packaged conditional resources and referenced engineering definitions. |
| Temporal/retry | RF-SR-01 | A changed basis requires rereading and proportionate reassessment; an old submission does not acquire current authority on retry. |
| Failure/recovery | RF-SR-01 | Interrupted work exposes its actual outcome and an owned next step without erasing unresolved issues or inventing success. |
| Compatibility/migration | RF-SR-01 | Retired procedures remain historical; successor behavior requires explicit applicable adoption/import and cannot relabel old approval. |
| External/environment | RF-SR-01 | Local engineering results remain separate from installed, published or hosted outcomes; required observations must actually be made. |

## Test design

Inspect the current responsibilities and boundary scenarios against the owning REM model and Module contract. Structural checks establish format only; independent review judges semantic coverage. Runtime record behavior is exercised by the package’s operational store, update, reliance, review and maintenance tests; skill guidance is assessed in actual generated archives with the resource validator and independent scenario inspection. Required combined and negative proof is allocated in the adoption plan.
