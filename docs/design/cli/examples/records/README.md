# Stored-record examples

These examples belong to [Record Format](../../records.md). V3 examples describe the supported stored contract and can be validated against its schema. Historical v2 illustrations, validators and continuation commands are retired. Every assessment, result and identity here is illustrative; none approves real work.

| Example | Version | Purpose and scope |
| --- | --- | --- |
| [All five record kinds](v3-complete-store/README.md) | V3 | Complete linked change, Review, evidence, material-decisions and Verify records; a representation example, not complete lifecycle proof. |
| [Review limitations update](v3-review-limitations-update/README.md) | V3 | Complete before/after records for a narrow edit; multiline rationale, complete findings remain unchanged. |
| [Finding correction](v3-finding-correction/README.md) | V3 | Explicitly correct evidence and required outcome under a stable ID, with no origin snapshot. |
| [Verify without proof references](v3-verify-without-evidence/README.md) | V3 | Complete record with empty proof references: structural recordability does not establish justified success. |
| [Verify limitations update with Git basis](v3-verify-limitations-update/README.md) | V3 | Self-contained before/after pair preserving the optional seven-value basis object; synthetic values establish no branch readiness. |

Historical v2 illustrations are recoverable at `7ad33e1b1827c84dfa4e9fbbfc8b52a204b5139e` under their original `docs/design/cli/examples/` paths; exact files are recorded in the [cleanup disposition](../../../../changes/2026-09-14-retire-specs-and-stale-tests/m6-design-reconciliation.json). They are not current inputs or acceptance examples.

Each scenario has its own folder and README. A single-record scenario uses a descriptive record filename; an update uses before.json and after.json; the five-kind collection uses the stored layout. Repeated-digit identities stand for exact assessed bytes; external engineering files are not supplied. Do not combine records from different rows into a change store unless their scenario explicitly connects them. The v3 complete collection documents its virtual-path mapping and internal references.

[CLI examples](../README.md) show requests and responses separately from these stored objects. Request, result, stored-record and internal digest versions are independent domains; a request schema_version of 1 does not mean it stores v1 records.
