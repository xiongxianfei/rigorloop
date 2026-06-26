# ADR-20260626-requirement-fidelity-gate: Requirement-Fidelity Gate for Spec-Canonical Reviews

## Status

accepted

## Context

The independent adversarial review gates make workflow-managed automated reviews procedurally independent: fresh context, neutral packets, blind-first risk formation, staged evidence release, risk-tiered escalation, and clean-review sufficiency receipts. The M2 `test-spec-review` miss showed a separate failure mode: a reviewer can be independent and still compare implementation wording to validator assertions instead of decomposing the governing spec clause.

The observed compression pattern was:

```text
spec requires A + B + C
implementation carries A + B
validator checks A + B
review confirms implementation and validator agree
```

This is a durable architecture decision because it changes automated review packet shape, applicability evidence, review-result evidence, validator assertion structure, calibration fixtures, autoprogression handoff eligibility, and the relationship between the independent-review gate and spec-canonical comparison.

## Decision

Add a requirement-fidelity gate as an additive sibling to the independent adversarial review gate for formal automated reviews whose deterministic applicability check evaluates to `applicable`.

The workflow or pre-review stage owns the applicability boundary:

```text
affected paths
matched path triggers
matched category triggers
applicability result
reviewer override direction
override justification
review stage
```

The reviewer owns the spec-canonical comparison boundary:

```text
relevant spec clauses
accepted or reviewer-authored decomposition
requirement properties
required surfaces
property-by-surface verification
validator assertion comparison
compressed-requirement risk result
requirement-fidelity receipt or material finding
```

Applicable review packets present relevant spec clauses before implementation diffs, validator assertions, validation evidence, and prior findings. Accepted decompositions are preferred. If no accepted decomposition exists, the reviewer authors one before comparing artifacts to each other. Multi-surface contracts are checked property by property and surface by surface; global substring checks are insufficient when independent property or surface checks are possible.

Validator pilots use spec-derived property-list by surface-list assertion matrices for changed requirements that introduce closed enums, required fields, required surfaces, cross-section `MUST` requirements, or recent compression findings. Shared constants identify the normative source clause and include negative fixtures or equivalent proof for missing-property failures.

Calibration adds the `requirement-compression` seeded-defect family. Phase B sampling has numeric floors for applicable receipts, reviewer-authored decompositions, and `not-applicable` receipts. Seeded compression-defect recall is measured against named rotating corpus iterations.

When both the independent-review contract and requirement-fidelity contract apply, autoprogression uses AND semantics: both passing receipts are required before workflow-managed continuation. The requirement-fidelity gate can be disabled as a rollback lever without removing valid compression findings or the independent-review gate.

No hosted service, database, external control plane, deployment target, or network dependency is introduced.

## Alternatives considered

### Keep only independent adversarial review gates

Rejected because independence addresses anchoring and author-context leakage, not whether the reviewer preserved the full normative property set from the spec.

### Leave applicability to reviewer discretion

Rejected because silently classifying an applicable diff as not applicable repeats the same failure mode at the gate-selection layer. Applicability starts from deterministic path and category triggers, with recorded reviewer override only.

### Generate all requirement properties from specs immediately

Rejected for the first slice because arbitrary prose extraction is too broad and brittle. Reviewer-authored decompositions and spec-derived constants provide a reviewable first slice, with logged decompositions available for later automation work.

### Require a finding or seeded failure in every review

Rejected because finding quotas optimize for noise rather than requirement fidelity. Clean reviews remain valid when the manifest, decomposition, matrix, validator comparison, and receipt are structurally sufficient.

## Consequences

- Automated review evidence becomes more expensive because applicable clean reviews must carry applicability manifests, decomposition evidence, property matrices, validator comparison, and requirement-fidelity receipts.
- Reviewers have a canonical comparison point: the governing spec clause, not implementation/validator agreement.
- Validators for selected multi-surface or closed-list contracts become less likely to encode only a hand-copied subset because tests iterate over shared property and surface lists.
- Clean automated handoff becomes stricter: missing decomposition, free-form `not-applicable`, validator-only comparison, or an incomplete property matrix blocks continuation when applicability is `applicable`.
- Calibration must distinguish requirement-compression recall from generic review independence metrics, using rotating corpus iterations to reduce fixture memorization.
- Manual reviews remain compatible: they may voluntarily record fidelity receipts, but mandatory manual-review applicability classification is out of first-slice scope.
- Historical clean reviews remain historical evidence and are not retroactively invalidated solely because they lack requirement-fidelity receipts.
- Implementation must preserve existing independent-review fixtures and behavior while adding requirement-fidelity checks.

## Follow-up

- Architecture-review this ADR and the canonical architecture package update.
- Author the matching test specification for requirement-fidelity requirements, examples, acceptance criteria, and RFG check IDs.
- Plan implementation of applicability manifests, packet ordering evidence, decomposition tables, property matrices, receipt validation, validator constants, negative fixtures, seeded compression defects, calibration sampling records, and generated adapter updates.
- Keep manual-review applicability as a follow-on proposal after Phase B produces at least 30 calibrated review records.
