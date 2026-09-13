# Proposed v3 review limitations update

[Before](before.json) and [after](after.json) are complete proposed v3 Review records under [RF-SR-09/10/13](../../../records.md#requirements). Only limitations differs. Judgment, current subjects, multiline rationale, complete findings remain identical.

The rationale contains actual paragraph/code-block line breaks, Unicode, and a literal backslash-n example. JSON escapes actual newlines as `\n` and the literal backslash as `\\`; a renderer decodes JSON once and must not reinterpret the literal escape as a newline.

The fictional reviewer treats this edit as clarification of the same assessment scope. That assumption does not generalize to newly missing evidence or a changed assessment basis. No actual independent review, new approval or applicability renewal is established. The containing v3 store is omitted; the [matching CLI scenario](../../v3-review-limitations-update/README.md) supplies its starting-state assumptions and proposed messages. Schema conformance does not establish the claimed assessment or evidence freshness.
