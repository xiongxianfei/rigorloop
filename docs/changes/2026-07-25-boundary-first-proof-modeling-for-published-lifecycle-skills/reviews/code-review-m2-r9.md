# Code Review M2 R9

Review ID: code-review-m2-r9

Stage: code-review

Round: 9

Reviewer: Codex code-review skill

Target: immutable run `run-8f095d95abb863dbcbd642fe61abd65e`

Reviewed artifact: immutable run
`run-8f095d95abb863dbcbd642fe61abd65e`

Reviewed milestone: M2

Status: changes-requested

Review status: changes-requested

Material findings: BFP-CR-M2-15

Immediate next stage: spec

Milestone closeout: resolution-needed

Recording status: recorded

Review date: 2026-07-27

Automated review: yes

Native review status: changes-requested

Review gate outcome: stop

Independence level: L1

Author context ID: boundary-m2-canonical-run-r9

Reviewer context ID: boundary-m2-review-r9-reset

Context separation mechanism: fresh review phase with tracked-evidence reset

Risk tier: elevated

Risk-tier triggers: canonical behavior evidence; comparison oracle; high-risk
M2

Risk-tier classifier: governing-spec and fresh-behavior-evidence triggers

Governing artifacts: specs/rigorloop-workflow.md R28y;
specs/rigorloop-workflow.test.md T52;
tests/fixtures/boundary-proof/simple-change/scenario.json

Formal criteria: R28y scenario comparison-only expectations; T52

Initial packet inventory: specs/rigorloop-workflow.md@e1072df7#sha256:7d32316ec3434641ef1fc6512a03deef765a4e264a507300ddf1ab3b4215ee1d; specs/rigorloop-workflow.test.md@e1072df7#sha256:8c660c1728b189c87646f089bff3ee12c16f793c8691d26143cf2086378e23b1; tests/fixtures/boundary-proof/simple-change/scenario.json@e1072df7#sha256:9b3d8fb361795fdc96140e13bfd34d52a73969e863e12e04418fda832c520415; docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/runs/run-8f095d95abb863dbcbd642fe61abd65e/manifest.json@e1072df7#sha256:fd38b39b23e5a7ae8448fd7dd6c03cb87b19b7737b1596f3d93f396a271f81b7

Prompt template version: code-review-template-v1

Initial packet hash: sha256:6f45e209b26ad15f9283d2a0c21f5b543824f6f1ba5e209d55effe330a34ad80

Manifest owner: orchestrator

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Affected behavior: comparison-only expected branch and corrected-role
validation

Highest-impact failure modes: canonical evidence reports pass for an observed
trace that contradicts the fixture’s declared expectation

Changed boundaries: scenario shape validation versus observed-result
comparison

Evidence expected: derived observed branch/role, exact comparison after event
derivation, and mismatch regressions proving no invocation influence

Areas requiring direct inspection: `_scenario`; `_generate_behavior_locked`;
`_validate_run`; T52 expectation contrasts

Areas intentionally out of scope: the correction-authority spec amendment,
M3, M4, final verification, PR, and release activation

Risk classes considered: canonical evidence=applicable; comparison
oracle=applicable; generated-evidence currency=applicable

Falsifiable review questions: Does changing only `expected_branch` or
`corrected_role` change invocation? Does a mismatch fail only after the
observed trace is derived?

Clean-review sufficiency receipt: no

Requirement-fidelity gate: required

Requirement-fidelity applicability: applicable

Requirement-fidelity affected paths: scripts/boundary_proof_behavior.py;
scripts/test-boundary-proof.py

Requirement-fidelity matched path triggers: specs/

Requirement-fidelity matched category triggers: workflow routing contracts

Requirement-fidelity review stage: code-review

Requirement-fidelity packet order: spec clause > scenario bytes > observed
manifest > implementation > tests

Requirement-property decomposition evidence: present below

Requirement-fidelity receipt: no; expectation shape and expectation comparison
are collapsed

## Result

- Skill: code-review
- Status: completed
- Open blockers: BFP-CR-M2-14, BFP-CR-M2-15
- Next stage: spec
- Review status: changes-requested
- Material findings: BFP-CR-M2-15
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m2-r9.md
- Review log: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md
- Review resolution: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Finding IDs: BFP-CR-M2-15
- Verify readiness: not-claimed

## Finding

### BFP-CR-M2-15 - Scenario expectations are parsed but never compared

Finding ID: BFP-CR-M2-15

Prior finding reconciliation: new

Severity: blocker

Auto-fix class: declared-safe

Location:

- `scripts/boundary_proof_behavior.py`, `_scenario`
- `scripts/boundary_proof_behavior.py`, `_generate_behavior_locked`
- `scripts/boundary_proof_behavior.py`, `_validate_run`
- `scripts/test-boundary-proof.py`, T52

Evidence:

- The current scenario declares `expected_branch: zero-correction` and
  `corrected_role: null`.
- The current immutable manifest contains `spec#2` and one completed
  feature-spec correction.
- Generation and validation both return pass with correction-cycle count one.
- Code reads the expectation fields only for shape consistency; no later path
  compares them with the derived trace.

Required outcome: Derive the observed branch and corrected role solely from
the completed event trace, then compare them exactly with the scenario
expectations after invocation and before publication/validation success.

Safe resolution path:

- Add one pure observed-expectation projection.
- Use it in both staged/current validation and generation before publication.
- Prove changing only expectations does not change requests, invocations,
  events, diagnostics, or outputs.
- Prove mismatched branch and role fail closed after derivation.
- Clarify the canonical scenario request so its expected zero-correction
  branch does not depend on an undefined Unicode classification.

## Prior finding reconciliation

- `BFP-CR-M2-14`: remains open and owns the spec correction-authority gap.
- `BFP-CR-M2-15`: new implementation gap; the governing expectation contract
  is already explicit.

## Handoff

Complete the focused correction-authority spec revision first, synchronize its
downstream projections, then fix this comparison defect in the same M2
implementation correction.
