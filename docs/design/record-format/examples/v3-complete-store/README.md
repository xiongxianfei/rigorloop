# Proposed v3 stored-record examples

This collection shows all five stored record kinds together under the [Record Format design](../../record-format.md#structured-assessment-explanations), particularly RF-SR-01/02/03/07/09–12. Each JSON file is a complete example record, not a field excerpt. The records illustrate registry, applicability and reference relationships; they do not demonstrate a complete engineering lifecycle or establish a real successful assessment.

| Record | Example | What to inspect |
| --- | --- | --- |
| Change | [change.json](change.json) | The v3 discriminator, current activity/work, supporting-record registry and explicit applicability declarations. |
| Review | [reviews/final-code-review.json](reviews/final-code-review.json) | Existing judgment, actors and subjects alongside summary, assessment_scope, rationale and limitations; no body. |
| Evidence | [evidence.json](evidence.json) | Independently addressable checks with actors, subjects, procedures, results and summaries; the assessment explanation remains with its owning record. |
| Material decisions | [material-decisions.json](material-decisions.json) | Decision rationale and source references; the existing shared body remains. |
| Verify | [verify-report.json](verify-report.json) | Evidence/review references, success-only outcome, the four shared explanation fields and delivered changes; no body or universal Git requirement. |

The virtual root is `docs/changes/example-change/`. Map paths beginning with that prefix to files in this directory when following registry entries and EntryRefs. For example, `docs/changes/example-change/evidence.json` maps to the local evidence.json. These virtual paths are schema-shaped examples; they do not register this directory as an operational change. Every registered supporting record is present, every applicability declaration names a registered record, and every EntryRef selects an admissible object in the collection.

All actors, observed results, judgments, requirement IDs and external engineering subjects are fictional. Repeated-digit sha256 identities are synthetic placeholders for exact file identities, not hashes of repository files. The referenced proposal, model, plan, implementation and tests are not supplied. Earlier lifecycle assessments are not reproduced. Consequently, the success/current/completed values illustrate storage representation and must not be used as proof of readiness, independence or actual execution.

The [v3 review before a limitations-only update](../v3-review-limitations-update/before.json) and [after the update](../v3-review-limitations-update/after.json) illustrate a narrow edit preserving all other fields, including complete findings. The historical, non-operational [v2 review before reassessment](../v2-review-reassessment/before.json) and [after reassessment](../v2-review-reassessment/after.json) illustrate changed subjects and judgment while preserving an unresolved finding and its origin. The [conditional Verify basis example](../v3-verify-limitations-update/before.json) illustrates the optional Git/PR object. These are separate scenarios, not additional registered records in this collection. The [CLI examples](../../../cli/examples/v3-review-limitations-update/README.md) illustrate request and response envelopes, which are different from the stored records here.

These examples use the v3 schema and contract. Historical validation is not a current conformance path. No existing record is converted, and no example save or schema check activates the new contract.
