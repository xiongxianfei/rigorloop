# Code Review M2 R3

Review ID: code-review-m2-r3

Stage: code-review

Round: 3

Reviewer: Codex code-review skill with context-separated independent reviewer

Target: commit range d1496c87..e522a808

Reviewed artifact: capability-bound M2 implementation and current failed-generation evidence

Status: blocked

Review status: blocked

Reviewed milestone: M2

Material findings: BFP-CR-M2-9

Immediate next stage: spec

Milestone closeout: resolution-needed

Recording status: recorded

Review date: 2026-07-27

Context separation mechanism: separate-agent

## Evidence reviewed

- Approved R28y contract, R53 spec review, and current proof map.
- Active M2 plan, current implementation diff, focused tests, and
  `validation-m2.md`.
- Fresh capability-bound v3 preflight and failed canonical generation.
- Exact scenario, comparison candidates, stage-envelope transport, and
  normalized oracle comparison code.

## Finding

### BFP-CR-M2-9 - Exact oracle equality conflicts with independent stage ownership

Finding ID: BFP-CR-M2-9

Severity: blocker

Auto-fix class: none

Location:

- `specs/rigorloop-workflow.md`, R28y candidate-oracle comparison
- `scripts/boundary_proof_behavior.py`, fresh feature and proof-map comparison
- `tests/fixtures/boundary-proof/simple-change/scenario.json`

Evidence:

- R28y requires equality across every normalized field, including stable IDs,
  boundary rows, rationales, examples, interactions, proof decomposition, and
  test-case IDs.
- The same contract requires each stage-owning skill to author every semantic
  byte independently.
- The scenario fixes R1-R4 behavior but does not authoritatively determine one
  stable-ID vocabulary, every non-applicability rationale, row ownership,
  interaction selection, or proof grouping.
- Fresh runs therefore reject structurally closed and independently reviewable
  alternatives unless they reproduce the hidden candidate decomposition.
- The implementation cannot expose the candidate as an input without violating
  its comparison-only role, and it cannot weaken comparison locally without
  violating the approved spec.

Required outcome: Define which fields are exact scenario invariants and which
are stage-owned modeling choices assessed through structural validity and
independent review.

Safe resolution: Amend R28y so comparison oracles enforce exact requested
behavior and closed structural invariants without demanding one golden
modeling decomposition. If exact decomposition is genuinely required instead,
move the complete decomposition into declared authoritative stage input and
stop describing it as comparison-only. Add a dedicated structural-oracle
mismatch diagnostic rather than routing this failure through
`unexpected-prohibited-event`.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Exact-oracle equality and independent semantic authorship are contradictory for the current input. |
| Test coverage | pass | 64 focused tests pass, including exact runtime projection, handler, retry, and publication contrasts. |
| Edge cases | concern | Golden-decomposition variance is not represented as a first-class diagnostic. |
| Error handling | pass | Generation fails before staging or publication and preserves the prior pointer. |
| Architecture boundaries | pass | Parent-only materialization and capability-bound preflight remain intact. |
| Compatibility | pass | Registered v1 remains opaque and v2 remains unsupported. |
| Security/privacy | pass | Bounded evidence contains no secret or raw private-runtime values. |
| Derived artifact currency | block | No current v3 immutable run can be published until the contract conflict is resolved. |
| Unrelated changes | pass | The reviewed slice remains within M2 runtime, harness, skill, fixture, and evidence scope. |
| Validation evidence | pass | Focused tests, compilation, skill validation, and diff integrity pass; canonical generation fails closed. |

## Prior finding reconciliation

`BFP-CR-M2-1`, `BFP-CR-M2-7`, and `BFP-CR-M2-8` remain open because their
current closeout requires a successful fresh canonical run and immutable
evidence. No separate material defect was found in the runtime projection,
capability-bound preflight, evidence-first retry coordinator, or publication
transaction.

## Handoff

- Review result: blocked.
- Milestone state: resolution-needed.
- Immediate next stage: focused R28y spec revision, then spec-review and
  downstream architecture/plan/test-spec synchronization only where affected.
- M3, final verification, and PR handoff remain blocked.
