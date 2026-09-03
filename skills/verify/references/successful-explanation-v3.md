# Successful final explanation (v3 staged protocol)

Use this reference only after every applicable evidence obligation and always-current check has passed for one active v3 final-readiness attempt. Failed, inconclusive, interrupted, pending, stale, report-write-failed, or registration-failed attempts must omit the explanation and must not grant `branch-ready`.

Write the explanation inside the successful Verify report. Cover what changed; why it changed; how it realizes approved requirements and Design; important implementation choices; evidence supporting readiness; limitations; and residual risks.

Bind the explanation to the exact reviewed product subject, final Code Review, Design package, Delivery plan, impact classification, evidence decisions, and observed results. Do not introduce new requirements, repair implementation, or reinterpret an upstream decision.

The report must not embed its own Git commit identity. The Verify result itself consists only of the report and its matching Verify-owned lifecycle validation registration. A later PR handoff may also contain current attributable final-review and workflow evidence created after the reviewed subject; those items are inputs to PR suffix classification and do not become part of the Verify result registration. Product, requirement, architecture, plan, dependency, generated-product, unrelated-documentation, identity, policy, evidence, or review drift makes the prior result stale.

Read back the exact whole report; unknown trailing bytes invalidate it. A current Verify result contains exactly the report and `change.yaml#lifecycle_cli.validations.verify-result`. The registration binds the report path and SHA-256 content identity, verified subject revision, and `verify` authority. Missing, duplicate, singleton, mismatched, malformed, or additional Verify result state grants no readiness.

An identical complete registered replay is idempotent. Any changed basis or content is a new attempt and requires re-evaluation. Report write or registration failure leaves no current readiness authority.
