# Proposed v3 Verify limitations update

This scenario applies [CLI-SR-24–27](../../cli.md#requirements) to the [stored Verify before](../../../record-format/examples/v3-verify-limitations-update/before.json) and [after](../../../record-format/examples/v3-verify-limitations-update/after.json). These complete proposed records contain an optional Git basis but no real proof of branch readiness. The edit clarifies the existing synthetic limitation; it does not add missing proof or change the basis.

The omitted v3 store registers `docs/changes/example-change/verify-report.json` at synthetic revision `b`. Its subject matches the declared `a` identity, and its existing applicability equals the actor/value/reason shown in the response. The update preserves that declaration.

| Step | Proposed invocation | Complete message |
| --- | --- | --- |
| Replace limitations | `rigorloop verify set --root . --change example-change --input - --format json` | [set-request.json](set-request.json) |
| Receive save result | Successful storage produces the synthetic `c` revision | [set-saved-response.json](set-saved-response.json) |
| Select explanation and basis | `rigorloop verify show --root . --change example-change --fields changes,limitations,verification_basis --format json` | [show-fields-response.json](show-fields-response.json) |

Only limitations changes; the complete verification_basis object and all other stored fields remain identical. Changing or removing the actual basis requires complete verify.record reassessment. Narrow updates cannot rewrite it, and the saved result cannot restore its applicability or freshness.

[show-absent-basis-response.json](show-absent-basis-response.json) is a separate read-only scenario using the [complete collection's local Verify](../../../record-format/examples/v3-complete-store/verify-report.json), not another step in the update sequence. It uses the same --fields selection. Verification_basis is absent from item.fields and explicitly named in scope.absent_fields, while unrequested members remain in omitted_fields. No null object, Git assessment or not-applicable judgment is invented. Both response scenarios use their own synthetic `c` revision/`d` file identity; those repeated values do not equate their underlying stores.

V3 runtime/schema support is not implemented. JSON parsing and these linked examples illustrate intended behavior, not executed recording, proof or approval.
