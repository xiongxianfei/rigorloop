# Assessment update failures

These complete example JSON responses illustrate [CLI-SR-27](../../cli.md#version-domains-and-dispatch). They are independent failure scenarios, not a transaction sequence or recorded execution. The current targeted schema defines these response envelopes. A schema-3 response does not imply a v3 store was found.

Use the complete [Review update request](../v3-review-limitations-update/set-request.json) or [Verify update request](../v3-verify-limitations-update/set-request.json) for the corresponding command, with --root ., --change example-change, --input - and --format json in a synthetic repository. For Review use review set design-review; for Verify use verify set. The request and repeated-digit subject/revision values are illustrative. The valid-request store scenarios reach store dispatch; prior request or selector errors take precedence.

| Scenario | Starting condition | Expected response |
| --- | --- | --- |
| review.set: invalid-arguments | Add --unknown-option; reject before reading stdin or the repository. | [review-invalid-arguments-response.json](review-invalid-arguments-response.json) |
| review.set: missing-store | The selected change store is absent. | [review-missing-store-response.json](review-missing-store-response.json) |
| review.set: v2-store | The selected store identifies retired v2; the operation rejects without validating its historical assessment. | [review-v2-store-response.json](review-v2-store-response.json) |
| verify.set: invalid-arguments | Add --unknown-option; reject before reading stdin or the repository. | [verify-invalid-arguments-response.json](verify-invalid-arguments-response.json) |
| verify.set: missing-store | The selected change store is absent. | [verify-missing-store-response.json](verify-missing-store-response.json) |
| verify.set: v2-store | The selected store identifies retired v2; the operation rejects without validating its historical assessment. | [verify-v2-store-response.json](verify-v2-store-response.json) |
| review.set: unknown-store | The stored discriminator is rigorloop-records-unknown. | [unknown-store-response.json](unknown-store-response.json) |
| verify.set: mixed-store | The manifest selects v3 but a registered record has schema_version 2. | [mixed-store-response.json](mixed-store-response.json) |
| verify.set: invalid-change-selector | Use verify set with --change ../invalid; omit the invalid change identity and reject before I/O. | [invalid-change-selector-response.json](invalid-change-selector-response.json) |
| Unrecognized command: unknown-command | Use the unrecognized command review frobnicate with a valid change selector; retain schema 2 and operation null. | [unknown-command-response.json](unknown-command-response.json) |

All examples exit 2 and make no writes. They omit record_contract and revision: no contract is claimed in a failure envelope and these examples promise no coherent snapshot revision. Valid change selectors remain available independently of store existence; the invalid selector example omits change_id entirely. Error messages are safe summaries, never raw input.

The existing [stale Review update](../v3-review-limitations-update/set-stale-response.json) and saved Review/Verify receipts cover validated-v3 outcomes. Batch remains a retained operation tag and uses schema 2 before validated v3 selection, regardless of new operation strings inside stdin. Unknown response versions must reject in consumers; do not reinterpret a new operation as an older operation.
