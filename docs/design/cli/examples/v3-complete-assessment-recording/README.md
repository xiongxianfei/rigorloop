# Proposed v3 complete assessment recording

These two independent scenarios apply [CLI-SR-12/26/27](../../cli.md#requirements) and [Record Format RF-SR-09–11](../../../record-format/record-format.md#requirements). Each supplies a complete actor-authored assessment through a proposed targeted request. Neither uses body for Review or Verify. Metadata and registry construction belong to the CLI; a saved receipt makes no approval claim.

| Scenario | Proposed invocation | Complete request | Illustrative saved response | Resulting stored assessment |
| --- | --- | --- | --- | --- |
| Create final Code Review | `rigorloop review record final-code-review --root . --change example-change --input - --format json` | [review-record-request.json](review-record-request.json) | [review-record-saved-response.json](review-record-saved-response.json) | [Review](../../../record-format/examples/v3-complete-store/reviews/final-code-review.json) |
| Create local Verify | `rigorloop verify record --root . --change example-change --input - --format json` | [verify-record-request.json](verify-record-request.json) | [verify-record-saved-response.json](verify-record-saved-response.json) | [Verify](../../../record-format/examples/v3-complete-store/verify-report.json) |

For Review creation, the omitted v3 store exists at synthetic revision `b`, registers the collection's evidence only, and has no Review, material decisions or Verify yet. The target file and registry entry are absent. The request supplies explicit applicability and all assessment fields; the CLI constructs schema/change/id metadata and empty findings. The illustrated stored Review matches the request values, but the complete collection's later manifest is not the immediate result of this one operation.

For Verify creation, start independently at synthetic revision `b` with the complete collection except its Verify file and associated registry/applicability entries. Its Review, evidence and material decisions already exist and all references resolve. The request references those checks and the final review, supplies explicit applicability, and omits optional verification_basis for a local-only claim. No missing proof is synthesized. In both scenarios, declared engineering identities match the synthetic read set; the saved receipt's `c` revision represents the respective candidate, not a computed fixture hash or a link between scenarios.

Existing-record replacements use the same complete assessment operations. Review replacement preserves existing findings. Full Verify replacement omitting verification_basis removes an earlier object, unlike verify.set, which cannot alter it. Those rules belong to the Design; these creation examples do not simulate replacement execution.

All people, judgments, check results and identities are fictional. These examples specify contract behavior rather than claim successful runtime execution or lifecycle completion.
