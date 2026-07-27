# Code Review M2 R7

Review ID: code-review-m2-r7

Stage: code-review

Round: 7

Reviewer: Codex code-review skill

Target: commit range 6779e383..f38a5aa2

Reviewed artifact: object-complete recovery correction and immutable run
`run-7c219a9daabd04402fa8345812f74b33`

Reviewed milestone: M2

Status: changes-requested

Review status: changes-requested

Material findings: BFP-CR-M2-13

Immediate next stage: review-resolution

Milestone closeout: resolution-needed

Recording status: recorded

Review date: 2026-07-27

Automated review: yes

Native review status: changes-requested

Review gate outcome: stop

Independence level: L1

Author context ID: boundary-m2-object-validity-implementation-r7

Reviewer context ID: boundary-m2-review-r7-reset

Context separation mechanism: fresh review phase with tracked-diff reset

Risk tier: elevated

Risk-tier triggers: durable destructive recovery; authority binding; immutable
evidence; high-risk M2

Risk-tier classifier: governing-spec and changed-path triggers

Governing artifacts: specs/rigorloop-workflow.md R28y;
specs/rigorloop-workflow.test.md T51-T52;
docs/architecture/system/architecture.md;
docs/plans/2026-07-25-boundary-first-proof-modeling.md M2

Formal criteria: R28y; T51-MANUAL-RECOVERY; BFP-CR-M2-12

Initial packet inventory: specs/rigorloop-workflow.md@f38a5aa2#sha256:7d32316ec3434641ef1fc6512a03deef765a4e264a507300ddf1ab3b4215ee1d; specs/rigorloop-workflow.test.md@f38a5aa2#sha256:8c660c1728b189c87646f089bff3ee12c16f793c8691d26143cf2086378e23b1; docs/architecture/system/architecture.md@f38a5aa2#sha256:ee9cda306ac94b7f23be63f59353ae453c7792e8f7a5bda9af8ca603f007ac1d; docs/plans/2026-07-25-boundary-first-proof-modeling.md@f38a5aa2#sha256:a4c719766aa97cec49deb7182cbe813b2654108623d7dd0098e41685a0f9a898; scripts/boundary_proof_behavior.py@f38a5aa2#sha256:9cc5566fce205147ff99d216af4a371525d404cf67cf5d98de59bf139067f945; scripts/test-boundary-proof.py@f38a5aa2#sha256:42343f316decb38ae8698158214f195ccbda3954e14f201a4f2ebc5d3da82940

Prompt template version: code-review-template-v1

Initial packet hash: sha256:45c77e20f5e85a49ff60f1f06b1a262f9b3283fe8efbc4f3aa24f811ed93f2d8

Manifest owner: orchestrator

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Affected behavior: recovery authority classification and exact recovery
authorization

Highest-impact failure modes: an arbitrary change-local Markdown artifact
authorizes destructive orphan detachment and regeneration

Changed boundaries: path containment versus semantic decision authority

Evidence expected: a closed review/owner-decision classifier and content bound
to the selected run, publisher, input, action, and authorized actor

Areas requiring direct inspection: `_validate_recovery_basis`;
`discard_interrupted_publication`; T51 manual-recovery fixtures

Areas intentionally out of scope: M3 downstream preservation; M4 aggregation;
final explain-change, verify, PR, hosted CI, and release activation

Risk classes considered: durable-write ordering=applicable;
interruption recovery=applicable; concurrency/idempotency=applicable;
identity freshness=applicable; security/privacy=applicable:destructive recovery
authority

Falsifiable review questions: Can a Markdown file under the change root that is
neither a review nor an owner decision authorize recovery?

Clean-review sufficiency receipt: no

Requirement-fidelity gate: required

Requirement-fidelity applicability: applicable

Requirement-fidelity affected paths: scripts/boundary_proof_behavior.py;
scripts/test-boundary-proof.py

Requirement-fidelity matched path triggers: specs/

Requirement-fidelity matched category triggers: workflow routing contracts

Requirement-fidelity review stage: code-review

Requirement-fidelity packet order: spec clause > decomposition > expected
surfaces > implementation diff > validator assertions > validation evidence >
prior findings

Requirement-property decomposition evidence: present below

Requirement-fidelity receipt: no; authority type and authorization content are
compressed into path suffix and containment

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active
  plan, and change metadata
- Open blockers: BFP-CR-M2-13
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: BFP-CR-M2-13
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m2-r7.md
- Review log: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md
- Review resolution: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Finding IDs: BFP-CR-M2-13
- Verify readiness: not-claimed

## Requirement-property decomposition

| R28y property | Direct observation | Result |
| --- | --- | --- |
| Completed history consumes only exact validated objects | same-run active staging remains visible and fails closed | pass |
| Recoverable staging is semantically complete | empty and malformed correction traces reject | pass |
| Fixed control roots have exact object kinds | non-directory `runs` rejects | pass |
| Authority is a current change-local review or owner decision authorizing the exact recovery | any current `.md` below the change root satisfies `_validate_recovery_basis`, regardless of artifact class or contents | fail |

## Finding

### BFP-CR-M2-13 - Recovery authority is location-bound but not decision-bound

Finding ID: BFP-CR-M2-13

Prior finding reconciliation: partial-remediation

Severity: blocker

Auto-fix class: declared-safe

Location:

- `scripts/boundary_proof_behavior.py`, `_validate_recovery_basis`
- `scripts/boundary_proof_behavior.py`, `discard_interrupted_publication`
- `scripts/test-boundary-proof.py`, T51 manual-recovery proof

Evidence:

- `_validate_recovery_basis` accepts every regular, current `.md` reference
  below `docs/changes/<change-id>/`.
- It does not classify the reference as a formal review or owner-decision
  artifact.
- It does not prove the referenced decision authorizes the selected `run_id`,
  `publisher_instance_id`, `input_set_identity`,
  `discard-and-regenerate` action, or `authorized_by` value.
- Therefore a validation note, plan-like note, or unrelated review inside the
  selected change record can authorize destructive recovery.

Required outcome: Accept only a closed change-local recovery-decision artifact
whose parsed authorization binds the exact recovery subject and action, while
preserving identity freshness and immutable recovery-basis binding.

Safe resolution path:

- Inputs: R28y exact recovery authority, selected lease, and recovery-basis
  schema.
- Outputs: one closed owner-decision schema and parser, exact subject/action
  equality checks before mutation, valid/invalid authority fixtures, and
  canonical regeneration.
- Allowed paths: M2 harness/tests/evidence, a change-local recovery decision,
  validation notes, review resolution, and active-plan state.
- Forbidden paths: broad Markdown heuristics, M3/M4 behavior, release
  activation, external actions, PR/deployment surfaces, and unrelated
  refactors.
- Acceptance criteria: arbitrary change-local Markdown rejects; wrong run,
  publisher, input, action, actor, schema, or extra/missing field rejects;
  current exact decision passes; stale decision identity rejects; focused and
  canonical validation pass.
- Required validation: complete boundary-proof suite; direct authority
  mutation matrix; canonical regeneration because the harness and input set
  change; skill/build, metadata, review, lifecycle, and diff checks.

No owner decision about product behavior is required because R28y already
defines exact recovery authorization.

## Prior finding reconciliation

- `BFP-CR-M2-12`: resolved for object-level history consumption, complete
  staged validation, and fixed-root kinds. Its authority-containment outcome
  is only partially remediated and is continued as `BFP-CR-M2-13`.

## Handoff

M2 remains `resolution-needed`.

Implement the closed recovery-decision schema and direct mutation matrix,
regenerate canonical evidence, then run `code-review-m2-r8`.
