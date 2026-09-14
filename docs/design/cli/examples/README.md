# CLI request and response examples

These examples belong to the [CLI design](../cli.md). Stored objects are indexed separately in [Record Format](records/README.md). Each request/response below is a complete envelope; the surrounding scenario supplies omitted repository state. Identities and decisions are synthetic unless a computed internal digest is explicitly identified. No example reports actual execution or approval.

| Scenario | Contract | What it illustrates |
| --- | --- | --- |
| [Observation freshness](observation-freshness/README.md) | Internal digest contract | Same record revision and messages, different observed subjects; these JSON files are digest inputs/expectations, not public envelopes. |
| [Complete assessment recording](v3-complete-assessment-recording/README.md) | V3 | Complete review.record and verify.record values, explicit creation applicability and saved receipts. |
| [Review limitations update](v3-review-limitations-update/README.md) | V3 | Whole-field edit, saved result, selected-field read, stale retry and semantic no-op. |
| [Finding correction](v3-finding-correction/README.md) | V3 | Explicit current-field update and saved receipt, preserving the review assessment. |
| [Assessment update failures](v3-assessment-update-errors/README.md) | V3 interface | New-command failures before v3 selection, with a retained schema-2 unknown-command control. |
| [Verify limitations update](v3-verify-limitations-update/README.md) | V3 | Whole-field edit preserving conditional basis, plus projections distinguishing present and absent basis. |

Historical v2 illustrations are recoverable at `7ad33e1b1827c84dfa4e9fbbfc8b52a204b5139e` under their original `docs/design/cli/examples/` paths; exact files are recorded in the [cleanup disposition](../../../changes/2026-09-14-retire-specs-and-stale-tests/m6-design-reconciliation.json). They are not current inputs or acceptance examples.

V3 requests retain targeted-recording-v1/schema_version 1; v3 stored records and the v3 result profile use their separately selected version 3. Schema and command conformance do not turn synthetic decisions into actual assessments. Do not infer a workflow approval or complete assessment read from a successful storage receipt or scope.complete alone.
