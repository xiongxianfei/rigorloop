# Code Review M2 R10

Review ID: code-review-m2-r10

Stage: code-review

Round: 10

Reviewer: Codex code-review skill

Target: M2 correction-authority implementation through `928355ac`

Reviewed artifact: implementation diff `e2bd25b6..928355ac`

Reviewed milestone: M2

Status: changes-requested

Review status: changes-requested

Material findings: BFP-CR-M2-16, BFP-CR-M2-17

Immediate next stage: review-resolution

Milestone closeout: resolution-needed

Recording status: recorded

Review date: 2026-07-27

Automated review: yes

Native review status: changes-requested

Review gate outcome: stop

Independence level: L1

Author context ID: boundary-m2-correction-authority-r10

Reviewer context ID: boundary-m2-review-r10-reset

Context separation mechanism: blind-first diff and governing-clause pass before
validation summaries and prior findings

Risk tier: elevated

Risk-tier triggers: mutation authority, terminal recovery, immutable generated
evidence, and comparison oracle

Risk-tier classifier: governing-spec, mutation-authority, recovery, and
generated-evidence triggers

Governing artifacts: `specs/rigorloop-workflow.md` R28y;
`specs/rigorloop-workflow.test.md` T52;
`docs/plans/2026-07-25-boundary-first-proof-modeling.md` M2

Formal criteria: exact correction eligibility, durable owner-decision stop,
discard/equal-input recovery, request-only child input, post-observation
expectation comparison

Initial packet inventory: specs/rigorloop-workflow.md@928355ac#sha256:7b035049f01e8e197809e79dbfb7f8481a2c61f63fc3bf992116544a4250c819; specs/rigorloop-workflow.test.md@928355ac#sha256:431e30ef05ff2720e77a589b48ac2794d79d76878f17c8dbe6be335d165d8f87; docs/plans/2026-07-25-boundary-first-proof-modeling.md@928355ac#sha256:bf48ca3fb18a04ea775ca7ade2fc088b9f805b53c563027aff588a1f46b5ec8a; scripts/boundary_proof_behavior.py@928355ac#sha256:f92d04b40d43f5221d939e76a0c33a1b2b05a76a6afc0f9dfe08214e90794824; scripts/test-boundary-proof.py@928355ac#sha256:27ec697f978c0545ee4906c5701b6b5c5a4379d7449a71aff3fb7f924b3df04d

Prompt template version: code-review-template-v1

Initial packet hash: sha256:68d68c74f6cf22edab9fcb536f2680630f8c473e57e35d5150ab98974cdc84a6

Manifest owner: orchestrator

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

## Independent risk map

Affected behavior: correction authority derivation, terminal stop persistence,
discard recovery, scenario comparison, and immutable-run validation

Highest-impact failure modes: owner-decision evidence is lost or unrecoverable;
a required negative boundary passes without proof; expected results steer child
invocation; stale authority enters attempt 2

Changed boundaries: review outcome versus executable correction authority;
working versus staged publication; authoritative request versus parent-only
expectations

Evidence expected: exact retained stop package, recovery/equal-input
transaction tests, complete finding-field mutation matrix, request capture,
and all branch/role expectation contrasts

Areas requiring direct inspection: `_write_correction_stop`,
`_working_tree_identity`, `_completed_correction_stop_input_identities`,
generation branches, scenario comparison, and T52 tests

Areas intentionally out of scope: M3, M4, final holistic review, final verify,
PR, and release activation

Risk classes considered: authorization=applicable; recovery=applicable;
generated evidence=applicable; requirement fidelity=applicable; oracle
independence=applicable; external deployment=not-applicable

Falsifiable review questions: Can an owner-decision stop be recovered
immediately? Does every T52 named contrast fail when seeded? Can changing only
expectation fields change any pre-comparison request or event bytes?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, change metadata, and plan handoff
- Open blockers: BFP-CR-M2-16, BFP-CR-M2-17
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: BFP-CR-M2-16, BFP-CR-M2-17
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m2-r10.md
- Review log: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md
- Review resolution: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Finding IDs: BFP-CR-M2-16, BFP-CR-M2-17
- Verify readiness: not-claimed

## Findings

## Finding BFP-CR-M2-16

Finding ID: BFP-CR-M2-16

Prior finding reconciliation: new

Severity: blocker

Auto-fix class: declared-safe

Location: `scripts/boundary_proof_behavior.py:6553`,
  `scripts/boundary_proof_behavior.py:5848`

Evidence: `_write_correction_stop` writes only `correction-stop.json` after
  the stage workspace has already been destroyed by its temporary-directory
  scope. `_working_tree_identity` accepts a correction stop only when it can
  find a matching retained review record and log below
  `boundary-proof-workspace-*`. A real owner-decision stop therefore produces
  a working root that its only permitted discard recovery cannot validate.
  The accepted review event, record, log, resolution, bundle, and normalized
  projection required by R28y are not durably retained.
Required outcome: Materialize and fsync one closed, lease-bound correction
  stop evidence package containing the accepted event, record, log,
  resolution, bundle, projection, and identities before raising the terminal
  diagnostic; validate that exact package during working-tree recovery.
Safe resolution path: Add one parent-authored stop-evidence materializer fed
  only by validated stage outputs, define a closed path/schema set, bind it to
  the existing receipt, and add end-to-end owner-stop plus discard-recovery
  tests for both review stages and malformed/symlink/special-file contrasts.
needs-decision rationale: none

Auto-fix recipe: implement the exact R28y retained-evidence contract in
  `scripts/boundary_proof_behavior.py` and its focused tests; do not alter
  published skills, scenario semantics, M3, or M4.
Required validation: `python scripts/test-boundary-proof.py`;
  `python scripts/boundary_proof_behavior.py validate --change-id
  2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills`

## Finding BFP-CR-M2-17

Finding ID: BFP-CR-M2-17

Prior finding reconciliation: new

Severity: major

Auto-fix class: declared-safe

Location: `scripts/test-boundary-proof.py:3294-3444`

Evidence: the new tests cover one complete automatic finding, one
  owner-decision finding, one empty field, two receipt mutations, one assembled
  path rejection, and one expectation mismatch. T52 requires every finding
  label mutation, unknown values, all nonempty owner-decision subsets,
  terminal nonpublication, exact discard crash boundaries, equal-input
  pre-allocation rejection, unequal-input restart, request-only byte
  invariance, and every compatible/incompatible observed branch-role pair.
  Those named proof obligations have no direct tests.
Required outcome: Add direct, named, deterministic tests that cover every
  T52 contrast and demonstrate the proof obligations independently of the
  successful canonical run.
Safe resolution path: Use table-driven pure/helper tests for closed parsing
  and comparison matrices, plus bounded temporary-repository transaction tests
  for stop persistence, recovery, equal-input rejection, and request capture.
  Keep the live canonical run as integration evidence rather than a substitute
  for contrast proof.
needs-decision rationale: none

Auto-fix recipe: implement the exact T52 named proof matrix in
  `scripts/test-boundary-proof.py`, adding minimal helper seams only where
  needed for deterministic observation; do not widen runtime behavior.
Required validation: `python scripts/test-boundary-proof.py`

## Prior finding reconciliation

- BFP-CR-M2-14: resolved by the identity-bound correction eligibility and
  owner-decision branch, subject to BFP-CR-M2-16 durability correction.
- BFP-CR-M2-15: resolved; generation and immutable validation derive observed
  branch/role and compare the parent-only expectations after event assembly.
- BFP-CR-M2-16: new-finding.
- BFP-CR-M2-17: new-finding.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | R28y retained stop evidence is not implemented. |
| Test coverage | block | T52 named contrast matrix is materially compressed. |
| Edge cases | block | Owner-stop recovery and equal-input boundaries lack direct proof. |
| Error handling | block | The terminal state cannot pass its own recovery validator. |
| Architecture boundaries | pass | Parent remains the only materializer and child input remains request-only. |
| Compatibility | pass | Existing public skills and generated adapters are unchanged. |
| Security/privacy | pass | No credential or network authority is widened. |
| Derived artifact currency | pass | `run-b6114d…` and `current.json` validate for the zero-correction branch. |
| Unrelated changes | pass | The reviewed implementation is scoped to R57/R29/R22/R26. |
| Validation evidence | concern | Commands pass, but selected tests do not satisfy the approved proof map. |

## Requirement-fidelity receipt

Requirement fidelity is applicable and does not pass. R28y’s retained-evidence
properties are absent from the owner-stop surface, and T52’s direct contrast
properties are absent from the test surface. Passing the current 104 tests
does not establish those properties.

## Handoff

M2 moves to `resolution-needed`. Both findings are deterministic and within
approved scope, so workflow-managed review-resolution may apply the declared
safe recipes and must rerun code review. M3, final closeout, explain-change,
verify, and PR remain blocked.
