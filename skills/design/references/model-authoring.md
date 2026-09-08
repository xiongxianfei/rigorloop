# Living-model authoring

Keep one current normative Design per coherent responsibility. Use `docs/design/M/M.md`, where directory and filename share stable model ID M; model-owned examples live under its `examples/` directory. An explicitly selected existing historical flat model may be revised in place under project authority; do not create a flat copy, silently relocate it or retarget an assessment. Model paths cannot point into examples or arbitrary extra normative nesting. Reject unsafe or ambiguous targets.

## Contract and structure

Explain goals, context, scope/non-goals, constraints, responsibility structure, runtime/operational and deployment boundaries, technical choices, quality, risks and necessary terminology to the depth needed for the claims. Cover invalid inputs, state/authority transitions, compatibility/migration, retries, concurrency, recovery, observability, security/privacy and accessibility where applicable. Explain material non-applicability instead of inventing components or metrics. Keep intended outcomes distinct from concrete downstream tests and mutable execution status.

Declare exactly once `Model validation contract: model-document-v1`. This document-format marker is independent of runtime record versions. Revise an older document marker only under the project's authoring authority; installing this skill does not authorize rewriting project models. The current validator rejects retired or unknown markers rather than selecting another runtime format. Use one level-two `Requirements` section with exactly `ID` and `Required behavior` columns. IDs are unique, nonempty, start with a letter and contain only letters, digits and hyphens. Normative text is nonempty.

Use one level-three `Boundary scan and acceptance scenarios` section with exactly `Dimension`, `Requirement basis` and `Distinct outcome to demonstrate` columns. Include each dimension once: Input domain; State/lifecycle; Identity/authority; Composition/path; Temporal/retry; Failure/recovery; Compatibility/migration; External/environment. Applicable rows cite unique model-local requirement IDs separated by comma and one space and give an observable outcome. Non-applicable rows use `-` and an outcome beginning `Not applicable:` with a reason. Unknown markers/dimensions, malformed tables, missing cells and undeclared/duplicate IDs reject.

Refer to a scenario using its model path and exact dimension label. Describe material combined hazards in concise requirement-linked prose nearby; no additional boundary/proof ID series is required. Delivery allocates every affected requirement, scenario and integrated hazard to concrete proof; structural checks cannot judge semantic adequacy.

## Decisions and references

Record important decisions once in the owning model with stable identity, context, selected outcome, meaningful alternatives, consequences and still-applicable constraints. Explain why the choice fits the required behavior. Do not require a duplicate current ADR. Preserve requirement/decision references across revisions or give explicit replacement mappings. Retain historical decisions and judgments with their original subjects.

## Supporting examples

The parent indexes each example's purpose, governing requirements, complete/excerpt scope and material synthetic identities or starting assumptions. Shared examples have one owner with consumer references. Load them on demand; they illustrate existing obligations and never become a second normative owner.

JSON examples must parse without explanatory invented fields. Complete records must conform to their selected schema when available; explicitly disclose absent-schema limits. Excerpts must state their omitted context and cannot claim complete-record conformance. Keep explanation in the parent or accompanying prose.

Before/after pairs must preserve the invariant they claim to demonstrate. Two individually valid records can still form an invalid transition; examine identity, authority, unchanged neighbors and prohibited side effects as applicable. Syntax checks do not establish the illustrated invariant.

Independent review covers affected examples alongside their owner, with exact identities when relied upon. Separately test the applicability contrast: if only a relied-on example changes, include its new exact subject and unchanged owning model in selection/handoff. Earlier approval of the parent or example does not by itself assess the revised example. Responsible assessors judge current reliance under existing review policy; selectors supply identities and retain model/example validation pairing, not automatic invalidation.

Keep one text source for a diagram and reference it; do not maintain competing inline/external copies. Images, external links or color alone cannot be the sole engineering truth. Keep examples free of secrets and private debug data.
