# Requirement-Fidelity Gate for Spec-Canonical Reviews

## Status

approved

## Related proposal

- [Requirement-Fidelity Gate for Spec-Canonical Reviews](../docs/proposals/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md)
- Proposal-review evidence: [proposal-review-r1](../docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/proposal-review-r1.md)

## Goal and context

RigorLoop needs a requirement-fidelity gate for reviews that implement, validate, teach, or preserve normative spec clauses. The gate prevents requirement compression: a review failure where a spec says A+B+C, but implementation, validators, or review evidence carry only A+B and the reviewer confirms implementation/validator agreement instead of comparing each artifact back to the full spec clause.

The gate is a sibling of independent adversarial review. Independent review reduces anchoring and author-context leakage. Requirement fidelity ensures the comparison reference is the complete normative spec clause and that every required property is checked across every required surface.

The first rollout applies to code-review of validator, skill, workflow, and review-recording changes. Later rollout to other review families is allowed only after the pilot proves the pattern.

## Glossary

- `requirement-fidelity gate`: a review protocol layer that verifies each requirement-bearing artifact against decomposed properties of the governing spec clause.
- `requirement compression`: the defect class where a multi-property, multi-surface, or closed-list requirement is projected as an incomplete subset.
- `requirement property`: one explicit property extracted from a normative spec clause, such as `approved`, `current`, or `recorded`.
- `required surface`: a public, workflow, validator, schema, fixture, review-recording, or generated-output surface that must preserve a requirement property.
- `multi-surface contract`: one normative requirement that must appear in, be enforced by, or be preserved across more than one required surface.
- `applicability manifest`: review evidence that records whether the requirement-fidelity gate applies to the current review, why, and any reviewer override.
- `requirement-fidelity receipt`: clean-review evidence showing that applicable spec clauses were decomposed, matrices were checked, validator assertions were compared to the spec, and no compression risk was found.
- `authoritative decomposition`: a property list or surface list defined by an approved spec, spec annex, accepted proposal during first-slice transition, or other governing artifact.
- `reviewer-authored decomposition`: a decomposition created by the reviewer because no authoritative decomposition exists yet.
- `spec-quality finding`: a finding against the governing spec when a cited clause is too vague to decompose into reviewable properties.
- `Phase B rollout`: the first enforcement phase where requirement-fidelity receipts and calibration sampling are applied to automated review pilots before steady-state sampling is approved by follow-on amendment.
- `calibration cycle`: one review-calibration reporting window. During Phase B, a calibration cycle lasts no more than one calendar month.

## Roles

| Role | Responsibility |
| --- | --- |
| Review-calibration-corpus maintainer | Owns seeded corpus iteration, sampling records, rotation logs, and corrective-action routing for requirement-compression calibration. |
| Workflow orchestrator or pre-review skill | Records automated applicability manifests before review comparison starts. |
| Spec author | Resolves spec-quality findings and owns spec amendments before same-stage spec-review reruns. |

## Examples first

Example E1: R26 compression is caught
Given a spec clause requires implementation eligibility to depend on approved, current, and recorded `test-spec-review` evidence
And the implementation skill and validator both mention only approved and current evidence
When requirement-fidelity review runs
Then the reviewer identifies the `recorded` property in the decomposition
And the review records a requirement-compression finding instead of accepting implementation/validator agreement.

Example E2: deterministic applicability triggers the gate
Given a code-review diff changes `skills/implement/SKILL.md` and `scripts/test-skill-validator.py`
When pre-review applicability is computed
Then the applicability manifest records the gate as applicable because `skills/` and validator paths are in the trigger set
And reviewer override is unavailable without a recorded override direction and justification.

Example E3: multi-surface matrix finds one weakened surface
Given a requirement property appears in workflow-role, inputs, default-evidence, and stop-condition surfaces
And three surfaces are complete while one omits a property
When the reviewer checks the property-by-surface matrix
Then the review does not pass based on a global substring match elsewhere.

Example E4: vague spec routes upstream
Given a spec clause says only that a validator behaves appropriately
When the reviewer cannot extract testable properties from the clause
Then the review records a spec-quality finding against the spec rather than passing the implementation or inventing hidden requirements.

Example E5: not-applicable is constrained
Given a review changes only prose unrelated to normative contracts
When the applicability manifest records `Requirement-fidelity applicability: not-applicable`
Then the receipt uses the closed reason `change unrelated to normative contracts`
And free-form opt-out wording does not satisfy the clean-review path.

Example E6: independent review and fidelity both apply
Given a workflow-managed automated code-review is subject to independent-review gates
And the changed surfaces also trigger requirement-fidelity applicability
When autoprogression evaluates whether to continue
Then both the independent-review receipt and the requirement-fidelity receipt must pass before downstream continuation.

Example E7: voluntary manual application is recorded but not gated
Given a reviewer manually invokes `spec-review` against a changed spec
And the reviewer voluntarily produces a decomposition table and fidelity receipt for a changed requirement clause
When the review is recorded
Then the receipt may be preserved as review evidence
But the orchestrator does not require manual-review risk classification for first-slice continuation.

## Requirements

R1. The requirement-fidelity gate MUST apply to formal automated reviews whose deterministic applicability check evaluates to `applicable`.

R1a. Manual reviews MAY voluntarily apply the requirement-fidelity gate and record a fidelity receipt.

R1b. Mandatory manual-review applicability classification MUST NOT be part of the first-slice normative scope.

R2. The requirement-fidelity gate MUST NOT replace independent adversarial review gates.

R3. When both the independent-review contract and requirement-fidelity contract apply, workflow-managed continuation MUST require both passing receipts before autoprogression continues.

R4. The workflow or pre-review stage MUST compute requirement-fidelity applicability from the affected-path set before the reviewer compares implementation or validator assertions.

R5. The applicability manifest MUST record affected paths, matched path triggers, matched category triggers, applicability result, reviewer override when present, override direction when present, override justification when present, and the review stage.

R6. Applicability result MUST use the closed enum `applicable` or `not-applicable`.

R7. Reviewer override direction MUST use the closed enum `force-applicable` or `force-not-applicable`.

R8. Reviewer override MUST require a non-empty justification. A reviewer MUST NOT silently replace the computed applicability result.

R9. The first-slice path trigger set MUST include `skills/`, `scripts/*validator*`, `scripts/validate-*`, `schemas/`, `specs/`, `templates/`, `docs/workflows.md`, `docs/changes/**/reviews/`, and `docs/changes/**/review-*.md`.

R10. The first-slice category trigger set MUST include `spec-derived validators`, `skill instructions derived from specs`, `review-recording contracts`, `workflow routing contracts`, `closed enums`, `multi-surface public skill guidance`, `artifact lifecycle validators`, `metadata validators`, `generated-output or package parity validators`, `autoprogression gates`, and `material-finding schemas`.

R11. A `not-applicable` receipt MUST use one of the closed reasons `change unrelated to normative contracts`, `decomposition already accepted upstream and unchanged`, or `surfaces covered by spec-derived constants exercised in tests`.

R12. The review packet for applicable requirement-fidelity reviews MUST present relevant spec clauses before implementation diff, validator assertions, validation evidence, and prior findings.

R13. When the review evidence records packet ordering, the relevant spec clause entry MUST be first in the evidence enumeration for requirement-fidelity review.

R14. If an accepted requirement-property decomposition exists, the reviewer MUST use that decomposition as the comparison baseline.

R15. If no accepted decomposition exists, the reviewer MUST create a reviewer-authored decomposition before comparing implementation wording or validator assertions to each other.

R16. Reviewer-authored decomposition evidence MUST identify the source spec clause and mark the decomposition as reviewer-authored.

R17. During Phase B rollout, the baseline calibration sample rate for applicable fidelity receipts MUST be at least 10 percent per calibration cycle.

R17a. During Phase B rollout, reviews whose decomposition is reviewer-authored rather than referenced from an authoritative spec annex MUST be sampled at a rate of at least 30 percent per calibration cycle.

R17b. After Phase B, the baseline calibration sample rate MUST NOT drop below 5 percent and the reviewer-authored decomposition sample rate MUST NOT drop below 15 percent unless a follow-on approved amendment supersedes these floors.

R17c. Sampling records MUST include `sampled_review_id`, `sampling_reason`, `audited_by`, `audit_outcome`, and `corrective_action` when applicable.

R17d. `sampling_reason` MUST use the closed enum `routine`, `reviewer-authored-decomposition`, `rotation-cycle`, or `escape-investigation`.

R18. If a cited spec clause is too vague to decompose into requirement properties, the reviewer MUST record a spec-quality finding against the spec instead of passing the implementation or validator surface.

R19. Applicable review records MUST include a requirement-property decomposition table or equivalent structured evidence with spec clause, requirement property, required surfaces, verification result, and evidence fields.

R20. Multi-surface contracts MUST be checked property by property and surface by surface.

R21. Global substring checks MUST NOT satisfy a multi-surface contract when any required property or required surface can be checked independently.

R22. Specs that define multi-surface contracts SHOULD name required surfaces from a closed surface vocabulary in the spec or a project-wide taxonomy.

R23. Reviewers MUST NOT invent conflicting surface identifiers for the same required surface when an accepted surface vocabulary exists.

R24. Validator tests for changed requirements MUST use a shared property-list by surface-list assertion matrix when the requirement introduces a closed enum, names required fields, names required surfaces, uses `MUST` across more than one section, or produced a compression-class finding in the prior 90 days.

R25. Spec-derived validator constants MUST identify their normative source clause.

R26. Validators MUST include at least one negative fixture or equivalent proof that removing one required property from one required surface fails validation for selected matrix-protected contracts.

R27. Semantic property IDs SHOULD be used unless exact public wording is itself normative.

R28. Exact wording MUST be treated as public contract wording for stage names, review outcome values, error message strings matched by downstream tools, configuration keys read from files, and command-line flags.

R29. Exact wording MUST NOT be required for prose descriptions, comments, or rationale unless a governing artifact makes that wording normative.

R30. Applicable clean reviews MUST include a requirement-fidelity receipt.

R31. The requirement-fidelity receipt MUST include fields for relevant spec clauses decomposed, property matrix complete, multi-surface contracts identified, validator assertions checked against spec, compressed requirement risk, and no-finding rationale.

R32. A receipt value of `yes` for spec-clause decomposition MUST require a decomposition table in the same review record or a link to accepted decomposition evidence.

R33. A receipt value of `not-applicable` MUST require a closed not-applicable reason.

R34. Missing decomposition evidence, empty not-applicable reasons, free-form opt-out reasons, or validator assertions accepted without spec comparison MUST block a clean automated review when the applicability manifest says the gate applies.

R35. Requirement compression MUST be a material finding when it affects required evidence, review or lifecycle gating, workflow routing, validation correctness, published skill behavior, test coverage obligations, package or install integrity, security, privacy, compatibility, or release gates.

R36. Requirement-compression finding titles SHOULD identify the surface, spec clause, and omitted property.

R37. Requirement-compression severity SHOULD default to `major`.

R38. Requirement-compression severity MUST be `blocking` when the omitted property protects an implementation start gate, verification gate, review recording gate, security gate, compatibility gate, or release gate.

R39. A requirement-compression finding MUST be classified as mechanical only when the missing property's phrasing is uniquely determined by the spec text and the fix is to insert that exact phrase into identified surfaces with no other changes.

R40. Compression findings that require rephrasing, choice between alternatives, or coordinated validator or test changes MUST NOT be classified as mechanical.

R41. Review calibration MUST include the seeded-defect family `requirement-compression`.

R42. The seeded-defect corpus MUST include A+B+C compressed to A+B, N surfaces compressed to N-1, closed enum compressed, normative verbs compressed, multi-surface asymmetry, and validator mirrors implementation seed types.

R43. The M2 `approved + current` without `recorded` case MUST be the canonical regression seed for validator and implementation agreement on a compressed subset.

R44. Seeded compression-defect recall MUST be measured against named corpus iterations.

R44a. Each corpus iteration MUST contain at least six defects spanning at least four of the six seed types listed in R42.

R44b. The corpus MUST rotate to a new iteration when any reviewer in the project has been exposed to the current iteration's complete defect set during calibration.

R44c. The corpus MUST rotate to a new iteration when recall against the current iteration exceeds 95 percent across two consecutive calibration cycles.

R44d. The corpus MUST rotate to a new iteration at least every two calibration cycles during Phase B.

R44e. The rotation log MUST record `previous_iteration_id`, `next_iteration_id`, `rotation_trigger`, `rotated_by`, and `rotation_date`.

R44f. Each calibration result MUST record the `iteration_id` measured.

R44g. `rotation_trigger` MUST use the closed enum `complete-defect-set-exposure`, `recall-above-95-two-cycles`, or `scheduled-two-cycle-rotation`.

R45. During Phase B rollout, the orchestrator MUST sample at least 5 percent of `not-applicable` fidelity receipts per calibration cycle.

R45a. During Phase B rollout, not-applicable receipt sampling MUST span review skills proportionally so no single skill differs by more than 10 percentage points from its share of not-applicable receipts in that cycle, unless fewer than five not-applicable receipts exist for the cycle.

R45b. Each sampled not-applicable receipt MUST record `original_not_applicable_reason`, `audit_outcome`, and `corrective_action` when misclassified.

R45c. `audit_outcome` for not-applicable receipt sampling MUST use the closed enum `correct`, `misclassified-should-have-applied`, or `out-of-scope`.

R46. The first implementation slice MUST preserve existing independent-review fixtures and behavior while adding requirement-fidelity checks.

R47. The first implementation slice MUST NOT rewrite all historical reviews, all validators, or all existing specs.

R48. The applicability trigger list and seeded-defect class list introduced by this spec MUST be protected by closed-list tests or equivalent validator coverage when implemented.

R49. Generated public adapter outputs MUST be refreshed through normal generation when canonical skill or asset behavior changes.

R50. Historical clean reviews remain historical evidence and MUST NOT be retroactively invalidated solely because they lack requirement-fidelity receipts.

## Inputs and outputs

Inputs:

- changed paths or review surface metadata;
- relevant spec clauses and accepted decompositions when present;
- required surface vocabulary when present;
- implementation diff or changed artifact surface;
- validator assertions and validation evidence when present;
- prior findings and review-resolution evidence when relevant;
- review stage and invocation context.

Outputs:

- applicability manifest;
- requirement-property decomposition table or accepted decomposition reference when applicable;
- property-by-surface matrix evidence for multi-surface contracts;
- requirement-fidelity receipt for applicable clean reviews;
- material findings for requirement compression or spec-quality gaps;
- calibration seed results when running review calibration;
- review-log and review-result updates under existing formal review recording rules.

## State and invariants

- The spec is the canonical comparison point for requirement-bearing review.
- Implementation and validator agreement is not sufficient proof of spec fidelity.
- Requirement-fidelity receipt state is review evidence, not a replacement for artifact lifecycle status.
- The independent-review gate and requirement-fidelity gate are additive sibling gates.
- Historical reviews remain valid historical records unless a later governing artifact explicitly requires rereview.
- `Follow-on artifacts` in lifecycle artifacts remains the place for actual downstream artifacts or terminal disposition.

## Error and boundary behavior

- Missing applicability manifest in an applicable automated review blocks clean review.
- Missing decomposition evidence in an applicable review blocks clean review.
- Unknown applicability result, reviewer override direction, not-applicable reason, trigger name, seeded-defect family, or seeded-defect type fails closed before consistency checks.
- A spec clause too vague for property extraction produces a spec-quality finding, not an implementation-compression finding.
- Missing one property on one required surface is sufficient to fail the property matrix.
- Reviewer override without justification is invalid.
- A review may record `not-applicable` only with a closed reason and supporting rationale.
- Sampling records with unknown `sampling_reason`, `rotation_trigger`, or `audit_outcome` values fail closed before consistency checks.

## Compatibility and migration

This spec applies forward to the first requirement-fidelity implementation slice. It does not retroactively migrate historical reviews, rewrite all validators, or require broad full-spec reads for small changes unrelated to normative contracts.

Existing independent adversarial review gates remain in force. Existing review stage order is unchanged. Autoprogression behavior changes only by adding requirement-fidelity receipt checks when applicability is triggered.

Rollback may disable the requirement-fidelity autoprogression gate while preserving independent review gates and already-recorded valid requirement-compression findings. Spec-derived property constants protecting active validators should remain unless the governing spec changes.

## Observability

Requirement-fidelity review evidence must expose:

- applicability result and trigger evidence;
- reviewer override and justification when present;
- relevant spec clause IDs;
- decomposition source, accepted or reviewer-authored;
- requirement properties;
- required surfaces;
- per-property and per-surface verification results;
- validator assertion comparison result;
- compressed-requirement risk result;
- not-applicable reason when used;
- material finding IDs when compression or spec-quality findings exist.

Calibration evidence should report corpus iteration, seed type, expected finding, observed finding, and recall result.

## Security and privacy

The gate must not require secrets, credentials, private network access, or side-effecting external systems. Review packets, receipts, and calibration fixtures must avoid sensitive data and machine-local paths unless they are intentionally part of a reviewed example.

Requirement-compression findings affecting security, privacy, compatibility, or release gates are material and may be blocking under this spec.

## Accessibility and UX

No end-user UI requirements apply. Contributor-facing review output must remain scan-first and must make applicability, decomposition, matrix status, and no-finding rationale easy to inspect without reading hidden reasoning.

## Performance expectations

The gate should start from affected paths, stable requirement IDs, accepted decompositions, surface vocabulary, and bounded excerpts. It should not require broad full-spec reads for changes unrelated to normative contracts.

Applicability computation and receipt validation should be deterministic and cheap enough to run during review artifact validation or targeted skill validation.

## Edge cases

EC1. A review surface changes a validator and a public skill, but no accepted decomposition exists. The reviewer authors a decomposition before implementation/validator comparison and marks it reviewer-authored.

EC2. A changed path matches the trigger set, but the reviewer believes no normative contract is affected. The manifest may override to `force-not-applicable` only with a recorded justification and closed not-applicable reason.

EC3. A path does not match the trigger set, but the changed content adds a material-finding schema enum. The category trigger makes the gate applicable.

EC4. A global validator assertion finds the missing phrase somewhere in a skill file, but one required section omits it. The review records compression because the per-surface matrix fails.

EC5. A spec defines a closed enum with seven values and the validator checks six. The review records closed-enum compression even if all implemented values pass existing tests.

EC6. A spec clause cannot be decomposed because the requirement says only "behave appropriately." The review records a spec-quality finding and routes upstream.

EC7. A clean review omits the requirement-fidelity receipt even though applicability is `applicable`. Autoprogression stops before downstream continuation.

EC8. A fixed public calibration corpus reaches 100 percent recall because reviewers memorize it. The metric is insufficient unless the corpus rotates.

EC9. A historical clean review lacks a fidelity receipt. It remains historical evidence unless a later change makes the reviewed surface current again and triggers a new applicable review.

## Non-goals

- Do not replace independent adversarial review gates.
- Do not require every review to produce a finding.
- Do not expose private chain-of-thought.
- Do not require reviewers to copy entire specs into review records.
- Do not require broad full-spec reads for every small change.
- Do not automatically parse arbitrary prose requirements in the first slice.
- Do not rewrite all existing validators in the first slice.
- Do not force code generation of all constants from specs in the first slice.
- Do not use implementation and validator agreement as sufficient proof of spec fidelity.
- Do not add finding quotas or forced-finding rules.
- Do not change workflow stage order.
- Do not automatically repair requirement-compression findings.
- Do not retroactively migrate historical reviews.
- Do not require mandatory manual-review applicability classification in the first slice.

## Acceptance criteria

AC-RFG-001. A reviewer can tell that requirement compression is distinct from review anchoring.

AC-RFG-002. A review manifest can record deterministic applicability from affected paths and category triggers.

AC-RFG-003. A reviewer override cannot silently bypass applicability.

AC-RFG-004. A relevant spec clause is decomposed into explicit properties before artifact comparison.

AC-RFG-005. An accepted decomposition is preferred over a reviewer-authored decomposition.

AC-RFG-006. A vague spec clause routes to a spec-quality finding.

AC-RFG-007. A multi-surface contract requires per-property and per-surface verification.

AC-RFG-008. Global substring checks are insufficient for multi-surface contracts.

AC-RFG-009. Validator tests for selected changed contracts use shared property-list by surface-list assertions.

AC-RFG-010. Removing one property from one required surface fails validation or review.

AC-RFG-011. Implementation and validator agreement on a compressed subset does not pass.

AC-RFG-012. The M2 missing-`recorded` case is represented as the canonical regression.

AC-RFG-013. Applicable clean automated reviews include a structurally valid requirement-fidelity receipt.

AC-RFG-014. Calibration sampling achieves at least the Phase B floor rates defined in R17 and R17a and the not-applicable receipt sampling rate defined in R45.

AC-RFG-015. The seeded-defect corpus rotates per the R44 trigger set, and each calibration record cites the `iteration_id` measured.

AC-RFG-016. Existing independent-review gate behavior remains intact.

AC-RFG-017. No finding quota or forced-finding rule is introduced.

AC-RFG-018. Historical reviews are not retroactively invalidated solely for lacking the new receipt.

AC-RFG-019. Manual reviews can voluntarily record a fidelity receipt without mandatory first-slice manual-review applicability classification.

AC-RFG-020. Steady-state sampling rates cannot drop below the R17b floors without a follow-on approved amendment.

## Planned test IDs

RFG-T017. Sample rate during Phase B is at least 10 percent for routine applicable fidelity receipts and at least 30 percent for reviewer-authored decompositions.

RFG-T018. Not-applicable receipt sampling is at least 5 percent per calibration cycle during Phase B.

RFG-T019. Corpus rotation triggers fire correctly on complete defect-set exposure, recall above 95 percent for two consecutive cycles, and scheduled two-cycle rotation.

RFG-T020. Calibration records cite the `iteration_id` measured.

RFG-T021. Steady-state sampling rates cannot drop below 5 percent baseline and 15 percent reviewer-authored decomposition floors without a follow-on approved amendment.

RFG-T022. The spec rejects unquantified soft-normative wording in `MUST` requirements unless the term is defined, quantified, or explicitly non-normative.

## Open questions

None for first-slice spec-review. Later work may decide whether to create a unified review-quality umbrella spec after the independence and fidelity gates have both been exercised.

## Next artifacts

```text
architecture assessment
architecture, if required
architecture-review, if architecture is required
plan
plan-review
test-spec
test-spec-review
implementation
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- `Manual Review Applicability for the Requirement-Fidelity Gate` proposal after Phase B of the automated pilot completes and produces at least 30 calibrated review records.

## Readiness

Approved for architecture assessment.
