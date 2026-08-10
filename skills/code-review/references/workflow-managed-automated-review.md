# Workflow-managed automated review

Load this reference only when the invocation is a formally armed
workflow-managed automated review or correction loop. The parent `code-review`
skill remains the policy, status, recording, finding, stop, claim, and handoff
owner. This reference supplies automation-only procedure.

## Automated Independent Review Gate

For workflow-managed automated `code-review`, review through the independent
adversarial review gate before the result may advance the profile.

The orchestrator owns an orchestrator-owned review invocation manifest and a neutral initial packet. It may contain the target, actual diff, governing artifacts, formal criteria, and neutral workflow facts. It excludes R5 forbidden initial-context items: author hidden reasoning, author chain-of-thought, author self-assessment, claims that the change is correct, desired review outcome, autoprogression round budget, message that approval is needed to continue, auto-fix budget, auto-fix eligibility, implementation-stage safety narrative, prior reviewer conclusion, prior finding content, validation-result summaries, and evidence menu.

Begin blind-first. Before later evidence is released, record an independent risk map before validation-result summaries, evidence menus, implementation notes, or prior finding content are released. Cover affected behavior, highest-impact failure modes, changed
boundaries, expected evidence, direct-inspection areas, intentionally
out-of-scope areas, applicable and non-applicable risk classes, and falsifiable
questions. Record `risk-map-recorded` before releasing the evidence menu.

Evidence challenge happens only after the risk map. Passing validation proves
only the selected checks. Challenge selection adequacy, negative and boundary
coverage, generated or derived evidence, and scope coverage before verdict.

Prior finding reconciliation happens only after the blind-first pass. Classify
each prior or discovered issue as `resolved`, `still-present`,
`failed-remediation`, `reopened`, `superseded`, or `new-finding`. Use
`failed-remediation` when a prior finding was claimed or expected to be fixed but is independently rediscovered during the blind-first pass. Reviewers MUST NOT downgrade it to `still-present`.

Clean automated reviews require a clean-review sufficiency receipt containing target identity, independence level, inspected authority, risk classes, adversarial hypotheses, direct proofs or reproductions, challenged validation, uncertain surfaces, confidence, and no-finding rationale. A clean automated review may advance only when the manifest, phase receipts, clean receipt, risk-tier escalation, unresolved-finding, and second-review gates are satisfied.

A final holistic code review is required before `explain-change` or `verify`.
It covers the complete final diff, cross-milestone interactions, governing
proposal, spec, test spec, architecture, plan, resolutions, final validation
selection, generated or derived artifacts, and cross-milestone scope. It is
separate from the last milestone-local review.

Do not introduce a minimum-finding quota. Finding count is not a quality target. The reviewer must not edit the reviewed target during review. Direct or profile-off review behavior remains isolated and does not require automated-review manifests unless the result is used as a workflow-managed automated handoff gate.

## Requirement-Fidelity Gate

Requirement fidelity is a sibling gate to independent review: independence reduces anchoring, while fidelity checks the complete normative spec projection.

For workflow-managed automated `code-review`, use the requirement-fidelity gate when the applicability manifest says `applicable`.

Start from the relevant spec clause before comparing implementation text, validator assertions, validation evidence, or prior findings.

Decompose each relevant spec clause into requirement properties before artifact comparison unless accepted decomposition evidence already exists.

For multi-surface contracts, check every requirement property on every required surface; a global substring match is insufficient.

Applicable clean automated reviews require a requirement-fidelity receipt. A clean automated review may advance only when both the independent-review gate and the requirement-fidelity gate pass when both apply.

Requirement compression is a material finding when an implementation, validator, skill, workflow, schema, fixture, generated output, or review-recording surface omits a required property.

Do not introduce a minimum-finding quota. Direct or profile-off review behavior remains isolated and does not require requirement-fidelity manifests unless the result is used as a workflow-managed automated handoff gate.

## Reviewer-owned correction classification

After findings and verdict are recorded, the reviewer may assign
`auto_fix_class`. Missing classification is `none` and pauses automated
correction. Use `mechanical` only for a closed deterministic fix kind with
affected paths, deterministic authority, and required validation. Use
`declared-safe` only when the record supplies a deterministic recipe, named
inputs and outputs, forbidden paths, acceptance criteria, required validation,
and no owner decision. The orchestrator never upgrades an unclassified finding.

## Bounded correction and rereview

Only recorded, accepted findings whose reviewer-owned classification permits
automation may enter the bounded correction loop. Apply the smallest approved
fix within its declared paths and budget, run the named direct validation, and
return the same milestone to review-requested. Use a context-reset rereview of
the changed target. New findings remain possible in every round. Exhausted
budgets, expanded scope, forbidden-path changes, validation failure, or an
owner decision pause the loop; they never convert automatically to approval.

## Phase receipts

Record receipts in order for `risk-map-recorded`, evidence-menu release,
evidence-results release, prior-finding release when applicable, and verdict.
Record the manifest identity, target identity, context-separation mechanism,
risk tier and triggers, requirement-fidelity applicability, second-review
requirement, and any pause or failure reason. Receipts describe procedure; they
do not replace the parent skill's formal review record.

## Promotion, pause, and failure

Promotion requires the native review outcome plus every applicable automation
receipt and escalation gate. Pause when the manifest is missing or stale, the
neutral packet leaks forbidden context, phase order is violated, independence
is insufficient for the selected risk tier, a required second review is absent,
findings remain unresolved, fidelity proof is incomplete, or correction exceeds
its declared boundary. Report the precise failed gate to workflow. This
procedure does not redefine the parent skill's native statuses, downstream
authority, recording obligations, or universal stop conditions.
