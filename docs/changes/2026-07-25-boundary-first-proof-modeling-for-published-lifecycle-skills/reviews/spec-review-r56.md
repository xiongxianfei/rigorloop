# Boundary-First Proof Modeling Spec Review R56

Review ID: spec-review-r56
Stage: spec-review
Round: 56
Reviewer: Codex spec-review skill with tracked-artifact context reset
Target: specs/rigorloop-workflow.md
Reviewed artifact: correction-authority amendment at 36903a62
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR56-1, BFP-SR56-2
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready
Architecture assessment: architecture-required
Recording status: recorded
Review date: 2026-07-27
Context separation mechanism: tracked-artifact and governing-contract reset

Reviewed commit: `36903a627df602655e055f984663a04170c96a68`

Reviewed spec identity:
`sha256:e3933c5dfdf65b24035f67ef1cd5626d4373d4249335e8896cb85b1253bbc24e`

## Result

Changes requested.

The amendment correctly separates review occurrence from correction authority
and safely rejects future-contingent in-run owner decisions. Two closed
contracts remain implicit: the exact finding projection used to derive
eligibility, and the diagnostic/recovery result when authority is absent.

## Review dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | block |
| normative language | pass |
| completeness | block |
| testability | block |
| examples | concern |
| compatibility | concern |
| observability | block |
| security/privacy | pass |
| non-goals | pass |
| acceptance criteria | block |

## Material findings

### BFP-SR56-1 — Correction eligibility has no exact parsed finding contract

Finding ID: BFP-SR56-1

Severity: blocking

Evidence:

The amendment names four Markdown labels and an exact `none` value, but does
not define finding boundaries, whitespace normalization, multiplicity,
duplicate labels, stable Finding ID binding, or how the bundle proves the
eligibility result came from the same reviewed record.

Required outcome:

Define one closed normalized finding projection, exact per-finding fields,
stable-ID uniqueness, normalization rules, and a deterministic aggregate
formula bound to the review-record identity.

Safe resolution path:

Add the projection to R28y, include its identity or complete normalized value
in the review bundle, and require unknown, duplicate, missing, empty, or
record-mismatched values to fail before eligibility routing.

needs-decision rationale: none

### BFP-SR56-2 — Authorization-required termination is outside the closed diagnostic and recovery model

Finding ID: BFP-SR56-2

Severity: blocking

Evidence:

`correction-authorization-required` is introduced as a terminal diagnostic,
but the spec does not assign its phase, result vocabulary, persisted evidence,
working-root outcome, retry rule, or relationship to manual
discard-and-regenerate recovery. Implementations could pause, fail, publish a
failed run, abandon a live lease, or reinvoke stages.

Required outcome:

Bind the diagnostic to the closed phase/result model and define the exact
nonpublication, retained evidence, lease/orphan, recovery, retry, and fresh-run
behavior.

Safe resolution path:

Classify the diagnostic as an in-turn non-retryable stop, persist the complete
review evidence in the lease-bound working root, permit only existing
explicitly authorized discard-and-regenerate recovery, forbid stage
reinvocation and immutable publication, and require a changed input identity
before a fresh run.

needs-decision rationale: none

## Routing

- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: the eligibility parser and authorization-required terminal
  state are not yet executable without architectural or implementation
  guessing.

## Handoff

Revise only the focused R28y correction-authority contract, then rerun
spec-review.
