# Proposed v3 review limitations update

This scenario applies [CLI-SR-24–27](../../cli.md#requirements) to the [stored Review before](../records/v3-review-limitations-update/before.json) and [after](../records/v3-review-limitations-update/after.json). Messages are complete v3 envelopes with synthetic values, not actual assessments.

The omitted v3 store example-change registers design-review at `docs/changes/example-change/reviews/design-review.json`. Its starting revision is the synthetic `b` digest, and the declared external subject matches the `a` identity. Applicability is already current with the actor and reason shown in the read response; the narrow edit does not change it. The fictional reviewer has determined that this particular clarification preserves meaning. New missing evidence would require a separate explicit applicability/correction decision.

| Step | Proposed command or condition | Message and expected meaning |
| --- | --- | --- |
| Update limitations | `rigorloop review set design-review --root . --change example-change --input - --format json` | [set-request.json](set-request.json) replaces the whole limitations field. |
| Save | The expected `b` revision and declared subject still match | [set-saved-response.json](set-saved-response.json) records the resulting `c` revision; only the named review is changed. |
| Read selected content | `rigorloop review show design-review --root . --change example-change --fields limitations,rationale --format json` | [show-fields-response.json](show-fields-response.json) matches the stored after values, with complete omission metadata. |
| Retry the original request | The store is now at `c`, but the request still expects `b` | [set-stale-response.json](set-stale-response.json) reports conflict; no fields are reapplied. |
| Repeat an equal value after rereading | Submit the same values with expected_revision changed to the current `c` revision | [set-unchanged-response.json](set-unchanged-response.json) retains `c` and has no changed targets. |

The before/after JSON differs only in limitations. Its rationale has actual paragraphs and a code block, Unicode, and a literal backslash-n; the selected response preserves the same decoded string. Complete findings are unchanged. The response's `d` file identity and all repeated-digit revisions are synthetic, not computed hashes of these files.

Scope.complete means the selected fields were retrieved. It does not mean the caller read the omitted judgment, subjects, findings or complete assessment. A saved/unchanged result establishes storage only; it does not approve the change or renew applicability.
