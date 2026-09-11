# Proposed v3 Verify limitations update

The [before record](before.json) and [after record](after.json) are complete proposed v3 Verify records governed by [RF-SR-09/10/11](../../record-format.md#requirements). Only limitations changes. The verifier, exact subjects, evidence/review references, success-only outcome, changes, rationale and complete optional verification_basis object are preserved.

This is an editorial clarification in a synthetic record whose empty proof references do not justify real success or branch readiness. Object preservation must not be interpreted as reassessment or evidence freshness. Changing the actual basis requires the full verify.record operation under the CLI design. The [matching CLI scenario](../../../cli/examples/v3-verify-limitations-update/README.md) shows a narrow update, a field projection and a separate absent-basis projection. Schema conformance does not establish the claimed assessment or evidence freshness.
