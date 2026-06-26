# Requirement-Fidelity Gate for Spec-Canonical Reviews

## Status

accepted

## Problem

The recent M2 `test-spec-review` evidence wording miss exposed a review failure that the independent adversarial review gates were not designed to catch.

The proximate failure was requirement compression:

```text
Spec R26 required:
  approved + current + recorded

Implementation taught:
  approved + current

Validator asserted:
  approved + current

Reviewer compared:
  implementation <-> validator

Result:
  agreement found, but the spec-required "recorded" property was missed.
```

The learn session captured this as a review miss involving `specs/test-spec-review-gate.md` R26, `skills/implement/SKILL.md`, `scripts/test-skill-validator.py`, and affected code-review rounds.

The important distinction is that the independence gates address anchoring, not requirement compression. They make the reviewer more independent from authoring context, require fresh review context, separate discovery from prior-finding reconciliation, and add clean-review sufficiency evidence.

Those mechanisms are necessary, but they do not guarantee that the reviewer's comparison point is the full spec. A reviewer can be fresh, adversarial, and unanchored, yet still compare:

```text
implementation surface
<-> validator assertion
```

instead of comparing both against:

```text
normative spec clause
```

The recurring defect pattern is:

```text
Spec says A + B + C.
Implementation, validator, or public skill surface carries only A + B.
Review confirms implementation and validator agree.
The missing C is not rediscovered.
```

This is a distinct review-quality failure mode:

```text
review independence without requirement fidelity
```

## Goals

- Add a review-process layer that prevents normative requirements from being compressed during implementation, validation, or review.
- Require reviewers to decompose relevant spec clauses into explicit requirement properties before checking artifacts.
- Make the spec, not the implementation, validator, or prior review, the canonical comparison point.
- Require multi-surface contracts to be checked property by property across every required surface.
- Encourage validators to use spec-derived property lists or constants instead of hand-listed phrase checks.
- Add compression defects to the seeded review-calibration corpus.
- Preserve the existing independent adversarial review gates.
- Avoid finding quotas or artificial review failures.
- Make clean reviews stronger by requiring a requirement-property fidelity receipt when the review surface implements or validates normative spec clauses.
- Reduce repeated "subset of spec enumeration" misses across skills, validators, review artifacts, and workflow contracts.
- Make applicability determination deterministic enough that reviewers do not silently skip the gate on a diff that should trigger it.

## Non-goals

- Do not replace the independent adversarial review gates.
- Do not require every review to produce a finding.
- Do not expose private chain-of-thought.
- Do not require reviewers to copy entire specs into review records.
- Do not require broad full-spec reads for every small change.
- Do not make validators parse arbitrary prose requirements automatically in the first slice.
- Do not require all existing historical tests to be rewritten immediately.
- Do not force code generation of all constants from specs in the first slice.
- Do not treat implementation and validator agreement as sufficient proof of spec fidelity.
- Do not allow review calibration to optimize for finding count.
- Do not change workflow stage order or autoprogression profiles in this proposal.
- Do not automatically repair requirement-compression findings.

## Vision fit

fits the current vision

RigorLoop's core value is traceable, reviewable, human-understandable AI-assisted work. That depends on requirements remaining intact as they move through:

```text
spec -> test spec -> skill guidance -> implementation -> validators -> review
```

This proposal strengthens that chain by making requirement projection explicit and auditable. It fits the project vision because it improves reviewability, traceability, durable evidence, and human inspection of AI-assisted changes.

The proposal is falsified if:

```text
- reviewers still compare implementation only to validator assertions;
- a spec clause with A+B+C can be implemented as A+B and reviewed cleanly;
- multi-surface contracts are checked with one global substring assertion;
- clean reviews lack evidence that normative properties were decomposed;
- seeded compression defects are missed by calibrated review fixtures;
- the process creates boilerplate without improving defect detection.
```

## Context

The independent adversarial review gates proposal is still valuable. It addresses:

```text
author-context leakage
autoprogression outcome pressure
validation-result anchoring
fix-confirmation-only rereviews
missing clean-review sufficiency evidence
```

It does not fully address whether the reviewer has decomposed the spec clause before comparing artifacts. The M2 miss supplies concrete evidence of that adjacent failure mode.

This proposal should therefore be framed as a sibling layer:

```text
Review independence:
  Is the reviewer cognitively and procedurally independent?

Requirement fidelity:
  Is the reviewer comparing every artifact to the complete normative spec?
```

Both are required for trustworthy automated review.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Explain why independence gates missed the issue | in scope | Problem, Context |
| Add a follow-on mechanism for requirement compression | in scope | Recommended Direction |
| Use spec-derived enumerations or constants | in scope | Recommended Direction, Testing and Verification Strategy |
| Add requirement-property decomposition to review | in scope | Recommended Direction |
| Add compression defects to calibration corpus | in scope | Recommended Direction, Testing and Verification Strategy |
| Preserve independence gates | in scope | Non-goals, Context |
| Keep review critical and independent | in scope | Context, Recommended Direction |
| Avoid treating the gates as broken | in scope | Context, Decision Log |
| Make this a focused follow-on proposal | in scope | Scope budget, Rollout and Rollback |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Requirement-property decomposition phase | core to this proposal | Directly addresses compression misses. |
| Spec-canonical evidence packet ordering | core to this proposal | Reduces implementation and validator anchoring. |
| Multi-surface contract review case | core to this proposal | Compression misses are likely when one requirement is repeated across surfaces. |
| Spec-derived property constants for validators | first-slice candidate | High leverage; can start with selected requirements. |
| Deterministic applicability manifest | core to this proposal | Prevents the gate from depending only on reviewer discretion. |
| Authoritative decomposition annex support | first-slice candidate | Reduces the chance that reviewer-authored decomposition is itself compressed. |
| Seeded compression-defect corpus | core to this proposal | Calibrates whether reviewers catch this defect family. |
| Clean-review sufficiency receipt extension | same-slice dependency | Clean reviews need evidence that fidelity checks happened. |
| Code-review pilot | first-slice candidate | The M2 miss occurred in code review. |
| Spec-review and plan-review adoption | separate implementation slice | Broaden after the code-review pilot proves the pattern. |
| Full automatic extraction of properties from specs | deferable follow-up | Useful later, but too broad for the first slice. |
| Rewrite of all existing validators | out of scope | Start with changed or high-risk requirement families. |
| Finding quota or forced-failure policy | rejected option | Would incentivize noise. |

## Options Considered

| Option | Summary | Tradeoff |
| --- | --- | --- |
| Keep only the independent adversarial review gates | Preserve the current follow-on gate design without adding a requirement-fidelity layer. | Lowest process change, but it leaves the observed A+B+C to A+B compression failure mode unaddressed. |
| Add a requirement-fidelity gate for applicable reviews | Require spec-canonical packet ordering, requirement-property decomposition, multi-surface matrices, validator property lists, and compression-defect calibration for requirement-bearing review surfaces. | Best match for the failure mode, with bounded added review evidence. |
| Add requirement-fidelity guidance but leave applicability entirely to reviewer judgment | Tell reviewers when to apply the gate without deterministic affected-path support. | Rejected because misclassifying an applicable diff as not applicable is the same failure family at the gate-selection layer. |
| Generate requirement properties automatically from specs immediately | Build automation that extracts properties from arbitrary prose requirements and feeds validators or review packets. | Potentially useful later, but too broad and brittle for a first slice. |
| Use finding quotas or forced-failure calibration | Require reviews to produce findings or optimize for finding count. | Rejected because it rewards noise instead of fidelity and can reduce trust in clean reviews. |

## Recommended Direction

Add a Requirement-Fidelity Gate to automated reviews and high-risk manual reviews.

The gate has five parts:

```text
1. spec-canonical packet ordering
2. requirement-property decomposition
3. multi-surface property matrix
4. spec-derived validator assertions
5. compression-defect calibration
```

The first implementation slice should pilot the gate in `code-review`, especially for validator, skill, workflow, and review-recording changes.

When both the independent-review contract and the requirement-fidelity contract apply, autoprogression should use AND semantics: both receipts pass before the workflow continues. Requirement fidelity strengthens the comparison reference; it does not substitute for independent review.

### Applicability determination

Applicability should be computed deterministically before review from the affected-path set and recorded in the review manifest by the orchestrator or a pre-review skill invocation. The reviewer receives the applicability result as review input, not as an unstructured question to answer from scratch.

The first-slice allowlist should cover paths and change categories that can project normative requirements, including:

```text
skills/
scripts/*validator*
scripts/validate-*
schemas/
specs/
templates/
docs/workflows.md
docs/changes/**/reviews/
docs/changes/**/review-*.md
```

It should also cover the category triggers below when the changed path alone is not enough:

```text
spec-derived validators
skill instructions derived from specs
review-recording contracts
workflow routing contracts
closed enums
multi-surface public skill guidance
artifact lifecycle validators
metadata validators
generated-output or package parity validators
autoprogression gates
material-finding schemas
```

Reviewer override is allowed only when the manifest records the computed result, the override direction, and a bounded justification.

### Requirement-property decomposition

When a review surface claims to implement, validate, teach, or preserve a normative spec clause, the reviewer first decomposes that clause into explicit properties.

Example:

```text
Spec R26:
  implement skill requires test-spec-review evidence to be approved, current,
  and recorded before implementation.

Requirement properties:
  P1: approved
  P2: current
  P3: recorded
```

The review then checks each required property against each required surface.

When an authoritative decomposition exists in a spec annex or other governing artifact, the review should use it instead of re-authoring a fresh decomposition. When the reviewer authors the decomposition, the review record should identify it as reviewer-authored and make that review eligible for higher calibration sampling than reviews that reference an accepted decomposition.

If a cited spec clause is too vague to decompose into properties, the review should record a spec-quality finding against the spec rather than silently passing the implementation. That finding is distinct from an implementation-compression finding because the governing requirement itself is not yet reviewable.

Applicable reviews record a decomposition receipt similar to:

```md
## Requirement-property decomposition

| Spec clause | Requirement property | Required surfaces | Verified? | Evidence |
| --- | --- | --- | ---: | --- |
| R26 | approved | implement workflow role, inputs, default evidence, stop condition, validator assertions | yes/no | paths / checks |
| R26 | current | implement workflow role, inputs, default evidence, stop condition, validator assertions | yes/no | paths / checks |
| R26 | recorded | implement workflow role, inputs, default evidence, stop condition, validator assertions | yes/no | paths / checks |
```

For small changes unrelated to normative contracts, the review may record:

```text
Requirement-property decomposition: not applicable
Reason: <bounded reason>
```

The bounded reason should come from a closed set in the spec amendment, initially:

```text
change unrelated to normative contracts
decomposition already accepted upstream and unchanged
surfaces covered by spec-derived constants exercised in tests
```

For requirement-fidelity reviews, the initial review packet should present:

1. Relevant spec clauses.
2. Accepted requirement-property decomposition, if one exists.
3. Required artifact surfaces.
4. Implementation diff.
5. Validator assertions.
6. Validation evidence.
7. Prior findings.

If no decomposition exists yet, the reviewer creates one before inspecting implementation or validator details.

For multi-surface contracts:

```text
global substring checks are insufficient.
per-surface property checks are required.
```

When a spec clause is multi-surface, the spec should name the required surfaces from a closed vocabulary defined either in that spec or in a project-wide skill-section taxonomy. Surface identifiers such as `workflow_role`, `inputs`, `default_evidence`, and `pre_implementation_stop_condition` should not be invented independently by each reviewer.

Validators and tests should derive multi-surface assertions from a single property list:

```python
# Source: specs/test-spec-review-gate.md R26
R26_REQUIRED_EVIDENCE_PROPERTIES = (
    "approved",
    "current",
    "recorded",
)

R26_TAUGHT_IN_IMPLEMENT_SURFACES = (
    "workflow_role",
    "inputs",
    "default_evidence",
    "pre_implementation_stop_condition",
)
```

The key pattern is:

```text
one property list
x
one surface list
=
complete assertion matrix
```

Use spec-derived constants when a requirement contains:

```text
closed enum
evidence-property list
required-field list
required-surface list
multi-stage workflow condition
multi-target package/install parity rule
multi-adapter target list
review result vocabulary
resource class mapping
```

First-slice selection criteria should include every changed requirement that:

```text
introduces a closed enum
names a required-fields list
names a required-surfaces list
uses MUST across more than one section
produced a compression-class finding in the prior 90 days
```

This keeps "selected contracts" from becoming a discretionary deferral bucket.

Every constant should identify the normative source, for example:

```python
# Source: specs/test-spec-review-gate.md R26
```

At implementation time, the applicability trigger list and seeded-defect class list in this proposal should also become spec-derived constants with tests asserting their content. Those lists are themselves requirement-bearing enumerations and should not rely on hand-copied subsets.

Add a new seeded-defect family:

```text
requirement-compression
```

Required seed types include:

| Seed type | Example |
| --- | --- |
| A+B+C compressed to A+B | Spec requires approved/current/recorded; surface omits recorded. |
| N surfaces compressed to N-1 | Requirement taught in four public surfaces; one surface omits it. |
| Closed enum compressed | Spec has seven enum values; validator checks six. |
| Normative verbs compressed | Spec says require, reject, and record; implementation only requires and rejects. |
| Multi-surface asymmetry | Surface 1 is complete; surface 2 weakens the contract. |
| Validator mirrors implementation | Validator asserts the same shortened phrase as implementation. |

The M2 `approved + current` versus `approved + current + recorded` case should become the canonical seed for this class.

For applicable clean reviews, add a requirement-fidelity receipt similar to:

```md
## Requirement-fidelity receipt

- Relevant spec clauses decomposed: <yes/no/not-applicable>
- Property matrix complete: <yes/no/not-applicable>
- Multi-surface contracts identified: <yes/no/not-applicable>
- Validator assertions checked against spec: <yes/no/not-applicable>
- Compressed requirement risk: <none found | finding IDs | not applicable>
- No-finding rationale: <bounded rationale>
```

Receipt validation should be structural, not only assertion-based. A `yes` value requires the same record to include a decomposition table that cites at least one property for each cited spec clause. A `not-applicable` value requires a non-empty reason from the closed reason set. Missing tables, empty reasons, and free-form opt-out reasons should block the clean-review path when the deterministic applicability manifest marks the gate applicable.

Requirement compression should be a material finding when it affects required evidence, review or lifecycle gating, workflow routing, validation correctness, published skill behavior, test coverage obligations, package/install integrity, security, privacy, compatibility, or release gates.

Suggested finding title format:

```text
<surface> compresses <spec clause> by omitting <property>
```

Default severity should be `major`. Use `blocking` when the compressed property protects an implementation start gate, verification gate, review recording gate, security gate, compatibility gate, or release gate.

## Expected Behavior Changes

Before:

```text
reviewer compares implementation phrase to validator phrase
implementation and validator agree
review passes
```

After:

```text
reviewer decomposes spec clause into properties
reviewer checks each property against each required surface
validator tests iterate over spec-derived property list
omitted property fails review or validation
```

Before:

```text
A clean review says tests passed and no material issues found.
```

After:

```text
A clean review shows the spec clauses decomposed, surfaces checked,
and why no compression was found.
```

## Architecture Impact

| Surface | Impact |
| --- | --- |
| Independent review gates | Add a requirement-fidelity phase and receipt. |
| Code-review skill | Pilot decomposition and spec-canonical packet ordering. |
| Review-result skeletons | Add requirement-fidelity receipt when applicable. |
| Material-finding guidance | Add requirement-compression finding pattern. |
| Skill-validator tests | Use spec-derived property constants for selected multi-surface contracts. |
| Test-spec guidance | Add compression-defect fixtures. |
| Workflow autoprogression | Require a valid fidelity receipt before automatic continuation when applicable. |
| Calibration corpus | Add requirement-compression seeded defects. |
| Existing validators | No broad rewrite; update selected touched surfaces first. |

No runtime service, deployment boundary, persistence engine, or external API is introduced.

Architecture is not expected unless implementation introduces new orchestration state, generated packet manifests, or cross-process review services.

## Testing and Verification Strategy

Likely proof points:

| Check ID | What is verified |
| --- | --- |
| `RFG-001` | A relevant spec clause is decomposed before implementation or validator comparison. |
| `RFG-002` | Decomposition lists every normative property in the clause. |
| `RFG-003` | Multi-surface contracts identify every required surface. |
| `RFG-004` | A missing property on one surface fails review. |
| `RFG-005` | A global substring check is insufficient for multi-surface contracts. |
| `RFG-006` | Validator tests use a shared property list for selected contracts. |
| `RFG-007` | Removing one property from one surface fails a targeted test. |
| `RFG-008` | Validator and implementation agreeing on a compressed subset still fails. |
| `RFG-008a` | The M2 `approved + current` without `recorded` case is the canonical regression for validator and implementation agreement on a compressed subset. |
| `RFG-009` | Requirement-fidelity receipt is required for applicable clean automated reviews. |
| `RFG-010` | Requirement-fidelity receipt may be `not-applicable` only with a bounded reason from the closed reason set. |
| `RFG-011` | Seeded A+B+C to A+B compression is detected. |
| `RFG-012` | Seeded N-surface to N-1 surface compression is detected. |
| `RFG-013` | Closed-enum compression is detected. |
| `RFG-014` | Spec-canonical packet ordering is recorded in the review manifest or review evidence. |
| `RFG-014a` | The relevant spec clause section appears first in the manifest's evidence enumeration for requirement-fidelity reviews. |
| `RFG-015` | Validation evidence is not treated as the canonical source of the requirement. |
| `RFG-016` | Existing independent-review gates still pass their original fixtures. |
| `RFG-017` | Deterministic affected-path applicability is recorded before reviewer override. |
| `RFG-018` | Reviewer applicability override requires a recorded direction and justification. |
| `RFG-019` | Vague spec clauses route to spec-quality findings rather than silent pass. |
| `RFG-020` | Multi-surface review uses a closed surface vocabulary instead of reviewer-invented labels. |
| `RFG-021` | Applicability trigger and seeded-defect lists are protected by constants or equivalent closed-list tests. |

Create behavior-preservation evidence under the eventual change-local artifact pack:

```text
docs/changes/<change-id>/behavior-preservation.md
```

Required matrix:

| Surface | Baseline | Revised proof | Result |
| --- | --- | --- | --- |
| Review independence | Fresh context and blind-first review | Unchanged plus requirement-fidelity phase | strengthened |
| Clean review | Sufficiency receipt | Adds requirement-fidelity receipt when applicable | strengthened |
| Validator tests | Hand-listed assertions allowed | Spec-derived matrices for selected contracts | strengthened |
| Spec review | Spec is governing contract | Explicitly canonical comparison point | clarified |
| Existing workflows | Same stage order | Unchanged | preserved |
| Autoprogression | Gates on clean review | Gates on clean review plus fidelity receipt when applicable | strengthened |
| Historical reviews | Remain valid evidence | No migration | preserved |

Evaluate after the first 10 applicable reviews or 30 calendar days, whichever gives better evidence.

Target outcomes:

```text
zero repeated A+B+C -> A+B compression escapes
100% of applicable clean code reviews include fidelity receipts
100% seeded compression-defect recall in each iteration of a rotating pilot corpus
zero validator pilots using one global substring for a multi-surface contract
at least one property-list x surface-list assertion replacing a prior compressed assertion
```

A finding produced by the new gate is a success signal, not a regression.

## Rollout and Rollback

Rollout should proceed as bounded phases rather than a repo-wide rewrite:

| Phase | Scope |
| --- | --- |
| Contract and review-protocol amendment | Amend the independent adversarial review gate spec, add deterministic applicability recording, add requirement-property decomposition, add spec-canonical packet ordering, add fidelity receipt fields, and add the requirement-compression seeded-defect class. |
| Code-review pilot | Update `code-review` guidance, add A+B+C to A+B fixtures, add multi-surface examples, and require the fidelity receipt for automated code-review when specs are implemented or validators are changed. |
| Validator assertion pilot | Select one recent high-value requirement family, such as the `test-spec-review` evidence gate, and replace hand-listed phrase checks with property-list by surface-list assertions using the first-slice selection criteria. |
| Calibration | Add rotating seeded compression defects to review calibration, measure recall against baseline, sample `not-applicable` receipts, and update review guidance from misses. |
| Review-family expansion | Apply to `spec-review`, `plan-review`, `architecture-review`, and proposal-review only after the code-review pilot proves the pattern. |

Rollback:

- Disable the requirement-fidelity autoprogression gate while preserving independent review gates.
- Keep the seeded corpus for manual calibration.
- Restore prior review-result skeletons only if receipt requirements create unacceptable false positives.
- Do not delete valid requirement-compression findings.
- Do not remove spec-derived property constants once they protect active validators unless the governing spec changes.
- Preserve historical review records without retroactive migration.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Review records become too verbose | Require decomposition only for relevant normative clauses. |
| Reviewers copy spec text without thinking | Require property lists and surface matrices, not full text dumps. |
| Property extraction is inconsistent | Start with reviewer-authored decomposition, then codify constants for repeated contracts. |
| Reviewer-authored decomposition is itself compressed | Prefer authoritative decomposition annexes when present and increase calibration sampling for reviewer-authored decompositions. |
| Constants drift from specs | Annotate source clauses and review constants when specs change. |
| Validator overfits words | Prefer property labels and surface-specific tests; use exact text only when wording is itself normative. |
| Clean reviews become boilerplate | Calibrate with seeded compression defects and sample receipts. |
| `not-applicable` becomes an easy exit | Use deterministic applicability manifests, closed not-applicable reasons, override justification, and periodic sampling. |
| Surface labels drift between reviewers | Define required multi-surface vocabulary in the governing spec or a project-wide skill-section taxonomy. |
| Too many surfaces are marked required | Let specs define required surfaces; review blocks ambiguity. |
| Automation slows down | Apply only to spec-derived or multi-surface changes, not every small diff. |
| Reviewer still anchors on implementation | Enforce spec-canonical packet ordering. |

## Open Questions

### 1. Should requirement-property decomposition be mandatory for every review?

Candidate:

```text
No. Require it when the review surface implements, validates, teaches, or
projects a normative spec clause.

Applicability should be computed deterministically from affected paths and
closed category triggers, recorded in the review manifest, and shown to the
reviewer as an input. Reviewer override requires recorded justification.
Periodically sample not-applicable receipts to audit misclassification.
```

### 2. Should properties be generated automatically from specs?

Candidate:

```text
No in the first slice. Start with reviewer-authored decomposition and
spec-annotated constants for repeated contracts.

Record each reviewer-authored decomposition keyed to the source spec clause.
That corpus becomes input for a follow-on automation proposal and an empirical
baseline for whether generated decomposition would match human review.
```

### 3. Should the decomposition table live in every review record?

Candidate:

```text
Only when applicable. Otherwise require a brief not-applicable reason from a
closed reason set.
```

### 4. Should validators use exact words or semantic property IDs?

Candidate:

```text
Use semantic property IDs where possible. Use exact words only when exact
wording is itself part of the public contract.

Public contract wording includes stage names, review outcome values, error
message strings downstream tools match against, configuration keys read from
files, and command-line flags. It does not include prose descriptions,
comments, or rationale unless a governing artifact makes the exact wording
normative.
```

### 5. Should compression findings be auto-fixable?

Candidate:

```text
Usually no.

A missing property may require wording, validator, and spec/test-spec changes.
Treat it as requiring review-resolution unless the reviewer explicitly declares
a deterministic safe resolution path under the separate auto-fix contract.

A compression finding qualifies as mechanical only when the missing property's
phrasing is uniquely determined by the spec text and the fix is to insert that
exact phrase into identified surfaces with no other changes.
```

### 6. Who triggers the applicability check, and how is it recorded?

Candidate:

```text
The orchestrator or a pre-review skill invocation runs a deterministic
applicability check against the affected paths, records the result in the
review manifest, and presents it to the reviewer as a fact. Reviewer override
is allowed only with documented justification in the manifest.
```

### 7. Is a unified review-quality umbrella spec needed soon?

Candidate:

```text
Maybe, but not in this slice. Flag the risk during proposal-review: the
independence gate and requirement-fidelity gate should remain sibling layers
now, while a future umbrella may improve the mental model if review-quality
contracts continue to grow.
```

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-26 | Treat requirement compression as a distinct review failure mode. | The M2 learn session showed implementation and validator agreement could still omit the `recorded` property from R26; independence gates solve anchoring, not complete spec projection. | Declare independence gates ineffective. |
| 2026-06-26 | Add requirement-property decomposition before artifact comparison. | Reviewers need an explicit property list before checking implementation. | Continue relying on free-form adversarial review. |
| 2026-06-26 | Make the spec the canonical comparison point. | Implementation and validators can agree on the same compressed subset. | Compare implementation only to validator. |
| 2026-06-26 | Require per-surface checks for multi-surface contracts. | Global substring assertions miss weakened surfaces. | One global phrase check. |
| 2026-06-26 | Add compression defects to calibration. | Review-quality metrics need to measure this failure family. | Keep current seeded corpus unchanged. |
| 2026-06-26 | Avoid finding quotas. | The goal is fidelity, not more findings. | Require at least one finding per review. |
| 2026-06-26 | Make applicability deterministic with justified override. | Reviewer discretion alone can skip the gate on the same requirement-bearing surfaces the gate is meant to protect. | Leave applicability as an unstructured reviewer judgment. |
| 2026-06-26 | Prefer authoritative decomposition when available. | Reviewer-authored decomposition can itself compress the spec clause. | Let the same reviewer always create and verify the decomposition. |

## Next Artifacts

```text
review-independence / requirement-fidelity spec amendment
formal review recording amendment, if receipt fields need schema support
spec-review
test-spec amendment
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

Architecture is not expected unless the implementation introduces new orchestration state, generated packet manifests, or cross-process review services.

Potential later follow-on proposals after this proposal is reviewed:

- Proposal for automatic spec-property extraction from structured requirements.
- Proposal for review packet manifest hashing and immutable phase receipts.
- Proposal for all-review-family requirement-fidelity rollout.
- Proposal for validator-generation helpers from property/surface matrices.
- Proposal for review-quality reporting that includes compression-defect recall.

## Follow-on Artifacts

- [Requirement-Fidelity Gate for Spec-Canonical Reviews spec](../../specs/requirement-fidelity-gate.md)

## Readiness

Accepted after clean recorded `proposal-review`; follow-on spec has been authored.

Core invariant:

```text
A review is not spec-faithful merely because implementation and validator agree.

For every relevant normative clause, the reviewer must know the full set of
properties the spec requires, the surfaces that must carry them, and whether
each surface preserves each property.

The spec is the reference. Everything else is a projection that must be checked
against it.
```
