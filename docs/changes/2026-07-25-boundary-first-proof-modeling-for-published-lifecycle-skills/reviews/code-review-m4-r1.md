# Code Review M4 R1

Review ID: code-review-m4-r1

Stage: code-review

Round: 1

Reviewer: Codex code-review skill

Target: M4 implementation at `2a4d4fe0`

Reviewed artifact: implementation diff `f5757ac7..2a4d4fe0`

Reviewed milestone: M4

Status: changes-requested

Review status: changes-requested

Material findings: BFP-CR-M4-1

Immediate next stage: review-resolution

Milestone closeout: resolution-needed

Recording status: recorded

Review date: 2026-07-27

Automated review: yes

Native review status: changes-requested

Review gate outcome: stop

Independence level: L1

Author context ID: boundary-m4-implementation

Reviewer context ID: boundary-m4-review-r1-reset

Context separation mechanism: blind-first diff and report-schema inspection
before relying on the M4 validation summary

Risk tier: elevated

Risk-tier triggers: generated evidence, public adapter parity, release
activation semantics, selector routing, and final capability aggregation

Risk-tier classifier: generated-evidence, requirement-fidelity, release, and
validation triggers

Governing artifacts: `specs/rigorloop-workflow.md` R28n-R28p, R28y-R28z;
`specs/rigorloop-workflow.test.md` T46, T47, T54;
`docs/plans/2026-07-25-boundary-first-proof-modeling.md` M4

Formal criteria: fresh closed-operation execution, exact typed result and
dependency identities, complete report projection, reconstruction-only
validation, four-surface parity, exact selector routing, and release
non-activation

Initial packet inventory: specs/rigorloop-workflow.md@2a4d4fe0#sha256:7b035049f01e8e197809e79dbfb7f8481a2c61f63fc3bf992116544a4250c819; specs/rigorloop-workflow.test.md@2a4d4fe0#sha256:431e30ef05ff2720e77a589b48ac2794d79d76878f17c8dbe6be335d165d8f87; scripts/boundary_proof_model.py@2a4d4fe0#sha256:3cacfd008630fa61c78f5ce481c9842d3addcc6b21f0d9d3dc3b14a488dc60dc; scripts/validate-boundary-proof.py@2a4d4fe0#sha256:25a85a24cacac49cce350ec7f14d30fc028e40d499761cfd5a75b3cb041f3961; scripts/test-boundary-proof.py@2a4d4fe0#sha256:8d5b8916b64feb67be16c7f69d43bfae0249b50a194641a52fe3dd3b4eaefc2d; docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md@2a4d4fe0#sha256:89fe2ff1a7c3476b207425da764765252a0793c4dbff5337263d15b019210589

Prompt template version: code-review-template-v1

Initial packet hash: sha256:2a4d4fe02a4d4fe02a4d4fe02a4d4fe02a4d4fe02a4d4fe02a4d4fe02a4d4fe0

Manifest owner: orchestrator

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

## Independent risk map

Affected behavior: report generation, operation ownership, dependency
identity binding, canonical reconstruction, selector execution, adapter
parity, and release activation proof.

Highest-impact failure modes: asserted pass rows, omitted registry operations,
stale dependency identities, partial parity, or a report that validates
without reproducing current evidence.

Changed boundaries: typed operation results versus report projections;
deterministic validation versus lifecycle reinvocation; current candidate
evidence versus immutable published release history.

Evidence expected: all closed operations, exact ordered dependencies,
current input/output references, reconstruction equality, contrast tests,
four-surface parity, and non-activation proof.

Areas requiring direct inspection: report schema, operation builder,
capability aggregation, validation mode, selector routing, adapter parity,
activation fixtures, and current generated evidence.

Areas intentionally out of scope: release activation, publication, deployment,
PR creation, and progressive-disclosure resumption.

Risk classes considered: authorization=not-applicable; generated
evidence=applicable; validation=applicable; requirement fidelity=applicable;
release=applicable

Falsifiable review questions: Can a report row claim pass without a current
typed operation result, or can a dependency identity be changed without
invalidating canonical validation?

## Result

- Skill: code-review
- Status: completed
- Open blockers: BFP-CR-M4-1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: BFP-CR-M4-1
- Recording status: recorded
- Reviewed milestone: M4
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4
- Required review-resolution: open
- Verify readiness: not-claimed

## Review findings

Finding ID: BFP-CR-M4-1

Severity: major

Location: `scripts/boundary_proof_model.py` capability-report schema and
`scripts/validate-boundary-proof.py` report generation/validation

Evidence: The committed report omits the required `support` and
`simple_change` projections and the per-row `diagnostic_id`,
`operation_identity`, `dependency_results`, and `observations`. Generation
marks workflow, skill, traceability, preservation, parity, and aggregate rows
as `pass` directly instead of freshly executing and serializing the closed
R28y operation graph. Validation checks only the older aggregate shape and
current evidence references; it does not reconstruct operation identities,
direct dependency order, or report-row round trips.

Required outcome: Implement the complete R28y typed operation-result contract,
derive every production row from freshly executed operation owners, serialize
the complete support/simple-change/check/preservation/parity/fixture
projection, and make validation independently reconstruct and compare the
canonical report without lifecycle reinvocation. Add fail-closed tests for
missing, duplicate, reordered, stale, substituted, and round-trip-mismatched
operation/dependency data.

Safe resolution path: Add one immutable closed operation registry and typed
result validator in the boundary model, centralize result construction and
projection in the report writer, reconstruct deterministic operations plus
the validated current immutable behavior run during validation, then
regenerate the canonical report.

## Validation evidence

The submitted suites pass, but they validate the obsolete report projection.
They do not resolve the current R28y schema and operation-ownership mismatch.

## Handoff

M4 remains open in resolution-needed state. Resolve BFP-CR-M4-1 and rerun M4
code review before final holistic review or verification.
