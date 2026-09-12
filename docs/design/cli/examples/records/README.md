# Stored-record examples

These examples belong to [Record Format](../../records.md). V2 examples are non-operational historical illustrations; their stored validators and continuation commands are retired. V3 examples describe the supported stored contract and can be validated against its schema. Do not convert or execute the historical examples. Every assessment, result and identity here is illustrative; none approves real work.

| Example | Version | Purpose and scope |
| --- | --- | --- |
| [All five record kinds](v3-complete-store/README.md) | V3 | Complete linked change, Review, evidence, material-decisions and Verify records; a representation example, not complete lifecycle proof. |
| [Review limitations update](v3-review-limitations-update/README.md) | V3 | Complete before/after records for a narrow edit; multiline rationale, complete findings remain unchanged. |
| [Finding correction](v3-finding-correction/README.md) | V3 | Explicitly correct evidence and required outcome under a stable ID, with no origin snapshot. |
| [Verify without proof references](v3-verify-without-evidence/README.md) | V3 | Complete record with empty proof references: structural recordability does not establish justified success. |
| [Verify limitations update with Git basis](v3-verify-limitations-update/README.md) | V3 | Self-contained before/after pair preserving the optional seven-value basis object; synthetic values establish no branch readiness. |

Historical navigation only; these files are not current operational examples.

| Historical example | Version | Original purpose |
| --- | --- | --- |
| [Change before supporting records](v2-minimal-change/README.md) | V2 | Complete manifest before supporting records are registered. |
| [Review without assessment subjects](v2-review-without-subjects/README.md) | V2 | Complete structurally recordable review whose exact assessment subjects are missing. |
| [Review reassessment](v2-review-reassessment/README.md) | V2 | Complete before/after records: subjects and judgment change, but the unresolved finding and its origin remain. |

Each scenario has its own folder and README. A single-record scenario uses a descriptive record filename; an update uses before.json and after.json; the five-kind collection uses the stored layout. Repeated-digit identities stand for exact assessed bytes; external engineering files are not supplied. Do not combine records from different rows into a change store unless their scenario explicitly connects them. The v3 complete collection documents its virtual-path mapping and internal references.

[CLI examples](../README.md) show requests and responses separately from these stored objects. Request, result, stored-record and internal digest versions are independent domains; a request schema_version of 1 does not mean it stores v1 records.
