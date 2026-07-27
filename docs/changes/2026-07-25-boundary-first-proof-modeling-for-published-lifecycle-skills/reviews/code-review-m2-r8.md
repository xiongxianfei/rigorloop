# Code Review M2 R8

Review ID: code-review-m2-r8

Stage: code-review

Round: 8

Reviewer: Codex code-review skill

Target: commit range c1d916f0..3f77e1de

Reviewed artifact: decision-bound recovery correction and immutable run
`run-8f095d95abb863dbcbd642fe61abd65e`

Reviewed milestone: M2

Status: blocked

Review status: blocked

Material findings: BFP-CR-M2-14

Immediate next stage: spec

Milestone closeout: resolution-needed

Recording status: recorded

Review date: 2026-07-27

Automated review: yes

Native review status: blocked

Review gate outcome: blocked

Independence level: L1

Author context ID: boundary-m2-decision-authority-implementation-r8

Reviewer context ID: boundary-m2-review-r8-reset

Context separation mechanism: fresh review phase with tracked-diff reset

Risk tier: elevated

Risk-tier triggers: automatic artifact mutation; owner-decision boundary;
formal review routing; high-risk M2

Risk-tier classifier: governing-spec and fresh-behavior-evidence triggers

Governing artifacts: specs/rigorloop-workflow.md R12 and R28y;
specs/rigorloop-workflow.test.md T51-T52;
docs/plans/2026-07-25-boundary-first-proof-modeling.md M2

Formal criteria: R12 finding authority; R28y correction grammar;
T51-MANUAL-RECOVERY; BFP-CR-M2-13

Initial packet inventory: specs/rigorloop-workflow.md@3f77e1de#sha256:7d32316ec3434641ef1fc6512a03deef765a4e264a507300ddf1ab3b4215ee1d; specs/rigorloop-workflow.test.md@3f77e1de#sha256:8c660c1728b189c87646f089bff3ee12c16f793c8691d26143cf2086378e23b1; docs/plans/2026-07-25-boundary-first-proof-modeling.md@3f77e1de#sha256:85d916ccd9f85f144fd5de6109d2be19241cdb643dc5ff79c6f89caaf178ee48; scripts/boundary_proof_behavior.py@3f77e1de#sha256:e82ff29c7a6c7093d64d23ad0e479d9085b979f0f9008e80690374d015aa8902; scripts/test-boundary-proof.py@3f77e1de#sha256:33b05e1f462e7e6f492e6d36e5409dc8cc2aa7f7468e265441cd94c8ee2b0b5a; docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/runs/run-8f095d95abb863dbcbd642fe61abd65e/artifacts/review-evidence/spec-review-attempt-1-record.md@3f77e1de#sha256:077dc473e42e32e27bc31ab61ed831618edca423a7fee9d9122ef7ec6f01acc5

Prompt template version: code-review-template-v1

Initial packet hash: sha256:d4c8ea0f21263252805502103948067d76a01a0f3e79cc1122d08c9bc85c11b2

Manifest owner: orchestrator

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Affected behavior: review-finding correction authorization and owner-decision
routing

Highest-impact failure modes: a formal review that explicitly requires an
owner decision is silently converted into automatic mutation authority

Changed boundaries: `changes-requested` outcome versus correction eligibility;
review occurrence versus mutation authority

Evidence expected: closed correction-eligibility state, exact owner-decision
branch, no mutation before authority, and trace/evaluator proof

Areas requiring direct inspection: R28y allowed branches;
`_generate_behavior_locked`; `_review_payload_from_markdown`; immutable run
review and correction evidence

Areas intentionally out of scope: M3 downstream preservation; M4 aggregation;
final explain-change, verify, PR, hosted CI, and release activation

Risk classes considered: authorization=applicable; workflow routing=applicable;
identity freshness=applicable; generated-evidence currency=applicable

Falsifiable review questions: Does `changes-requested` prove correction
authority? Can a recorded `needs-decision` finding reach authoring attempt 2
without a separate owner decision?

Clean-review sufficiency receipt: no

Requirement-fidelity gate: required

Requirement-fidelity applicability: applicable

Requirement-fidelity affected paths: specs/rigorloop-workflow.md;
scripts/boundary_proof_behavior.py

Requirement-fidelity matched path triggers: specs/

Requirement-fidelity matched category triggers: workflow routing contracts

Requirement-fidelity review stage: code-review

Requirement-fidelity packet order: spec clause > trace grammar > fresh
behavior evidence > implementation diff > validator assertions > prior
findings

Requirement-property decomposition evidence: present below

Requirement-fidelity receipt: no; review outcome and correction authority are
collapsed

## Result

- Skill: code-review
- Status: completed
- Open blockers: BFP-CR-M2-14
- Next stage: spec
- Review status: blocked
- Material findings: BFP-CR-M2-14
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m2-r8.md
- Review log: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md
- Review resolution: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Finding IDs: BFP-CR-M2-14
- Verify readiness: not-claimed

## Requirement-property decomposition

| Property | Direct observation | Result |
| --- | --- | --- |
| Recovery decision binds exact destructive action | complete decision mutation matrix and 100-test suite pass | pass |
| Arbitrary change-local evidence cannot authorize recovery | unrelated Markdown and wrong decision path reject | pass |
| Active recovery cannot rebind authority | decision byte drift rejects on resume | pass |
| Review nonapproval is distinct from correction authority | every initial `changes-requested` result enters attempt 2 | fail |
| Owner-decision findings pause before mutation | generated review says owner confirmation is required, then `spec#2` mutates automatically | fail |

## Finding

### BFP-CR-M2-14 - Changes-requested is incorrectly treated as correction authority

Finding ID: BFP-CR-M2-14

Prior finding reconciliation: new

Severity: blocker

Auto-fix class: needs-decision

Location:

- `specs/rigorloop-workflow.md`, R28y allowed correction branches
- `scripts/boundary_proof_behavior.py`, `_generate_behavior_locked`
- immutable run `run-8f095d95abb863dbcbd642fe61abd65e`,
  `spec-review-attempt-1-record.md` and `spec#2`

Evidence:

- The formal review records
  `needs-decision rationale: The specification owner must choose...`.
- It also states that owner confirmation is required before revision.
- `_generate_behavior_locked` treats the `changes-requested` outcome alone as
  authorization and tells the authoring stage the finding “is authorized.”
- R28y permits the correction branch but has no distinct correction
  eligibility field or owner-decision pause/resume branch.

Required outcome: Separate review outcome from effective correction authority.
Define a closed correction-eligibility projection, an exact owner-decision
record and trace branch when required, and fail closed before authoring attempt
2 when authority is absent or stale.

Safe resolution path:

- Amend R28y and its proof map before implementation.
- Preserve review occurrence and findings regardless of eligibility.
- Permit automatic correction only for explicitly correction-eligible
  findings within the bounded correction budget.
- Require a separate exact owner decision for `needs-decision`, bind it to the
  reviewed artifact identity and finding set, and record it as an input to
  authoring attempt 2.
- Add missing, stale, wrong-finding, wrong-artifact, mixed-eligibility, and
  valid-decision contrast proofs.
- Synchronize architecture/plan/test-spec only where the approved contract
  changes their owned projection.

## Prior finding reconciliation

- `BFP-CR-M2-13`: resolved. Exact decision path, schema, subject, action,
  actor, freshness, and resume binding are directly proved.
- `BFP-CR-M2-14`: new spec-blocking authority-model finding from fresh
  behavior evidence.

## Handoff

M2 remains `resolution-needed`.

Revise and review the correction-authority contract before changing the
harness or regenerating canonical evidence.
