# Code Review M2 R6

Review ID: code-review-m2-r6

Stage: code-review

Round: 6

Reviewer: Codex code-review skill

Target: commit range f35604a4..dd33af42

Reviewed artifact: boundary-complete recovery correction and immutable run
`run-f6bb6b5f5d7912166d28fa37d012242f`

Reviewed milestone: M2

Status: changes-requested

Review status: changes-requested

Material findings: BFP-CR-M2-12

Immediate next stage: review-resolution

Milestone closeout: resolution-needed

Recording status: recorded

Review date: 2026-07-27

Automated review: yes

Native review status: changes-requested

Review gate outcome: stop

Independence level: L1

Author context ID: boundary-m2-recovery-implementation-r6

Reviewer context ID: boundary-m2-review-r6-reset

Context separation mechanism: fresh review phase with tracked-diff reset

Risk tier: elevated

Risk-tier triggers: durable publication transaction; interruption recovery;
immutable evidence authority; high-risk M2

Risk-tier classifier: governing-spec and changed-path triggers

Governing artifacts: specs/rigorloop-workflow.md R28y;
specs/rigorloop-workflow.test.md T51-T52;
docs/architecture/system/architecture.md;
docs/plans/2026-07-25-boundary-first-proof-modeling.md M2

Formal criteria: R28y; R28n; T51; T52; BFP-CR-M2-11

Initial packet inventory: specs/rigorloop-workflow.md@dd33af42#sha256:7d32316ec3434641ef1fc6512a03deef765a4e264a507300ddf1ab3b4215ee1d; specs/rigorloop-workflow.test.md@dd33af42#sha256:8c660c1728b189c87646f089bff3ee12c16f793c8691d26143cf2086378e23b1; docs/architecture/system/architecture.md@dd33af42#sha256:ee9cda306ac94b7f23be63f59353ae453c7792e8f7a5bda9af8ca603f007ac1d; docs/plans/2026-07-25-boundary-first-proof-modeling.md@dd33af42#sha256:906d8020134159b531a11f2890b4ecea4cf6304771e04dbd2f08978f0bd1064b; scripts/boundary_proof_behavior.py@dd33af42#sha256:542682d32ed8e51bff320cca093ba797ea03451db9c5a7c07e3ca15d3c7d8b63; scripts/test-boundary-proof.py@dd33af42#sha256:71f553c56619b4f1c71e365085fcd545ac2e19fc1c6a65804c2d5367e898dcb6

Prompt template version: code-review-template-v1

Initial packet hash: sha256:9fd98b1967ce9f37ec4d5da7576164a88f99856bb894020023e1fa50a5e5bd25

Manifest owner: orchestrator

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Affected behavior: completed-history partitioning, staged-orphan validation,
recovery authority binding, fixed control-root validation, and fresh-generation
eligibility

Highest-impact failure modes: terminal history hides a live same-run orphan;
syntactic shape substitutes for complete staged-run validity; unrelated
repository bytes grant destructive recovery; malformed control storage permits
lifecycle reinvocation

Changed boundaries: recovery-object identity versus run identity; structural
versus semantic staged validity; change-local authority containment; fixed
control-path type

Evidence expected: object-level completed-history consumption; one complete
staged-run validator shared by publication and recovery; exact change-local
authority roots; fixed-root type validation before candidate routing

Areas requiring direct inspection: `_discover_global_candidate`;
`_completed_recovery_is_valid`; `_validate_staged_run`;
`discard_interrupted_publication`; T51 property tests

Areas intentionally out of scope: M3 downstream preservation; M4 aggregation;
final explain-change, verify, PR, hosted CI, and release activation

Risk classes considered: durable-write ordering=applicable;
interruption recovery=applicable; concurrency/idempotency=applicable;
identity freshness=applicable; generated-evidence currency=applicable;
security/privacy=applicable:recovery authority containment

Falsifiable review questions: Does completed recovery remove only its own
history objects? Does staged recovery require the same complete semantic
validity as pre-publication staging? Can authority come from outside the
change-local record? Can a malformed fixed control root survive discovery?

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

Requirement-fidelity receipt: no; sibling boundary compression found

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active
  plan, and change metadata
- Open blockers: BFP-CR-M2-12
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: BFP-CR-M2-12
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m2-r6.md
- Review log: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md
- Review resolution: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Finding IDs: BFP-CR-M2-12
- Verify readiness: not-claimed

## Review inputs

- Diff: `f35604a4..dd33af42`
- Tracked governing branch state: clean at
  `dd33af422d680481181bd077a5da6b4418820ea0`
- Governing contract: R28y and R28n
- Proof map: T51 and T52
- Active plan: M2
- Direct review probes: completed-history plus same-run staging, semantically
  empty staged run, unrelated authority file, and non-directory runs root

## Diff summary

The correction introduces exact recovery basis/state validation, stricter
working and staged tree checks, active recovery blocking, constrained malformed
temporary-basis cleanup, publisher-active diagnostics, direct regressions, and
a fresh immutable run.

The implementation still classifies some boundaries by run ID or shallow shape
instead of by complete object state and semantic validity.

## Requirement-property decomposition

| R28y property | Direct observation | Result |
| --- | --- | --- |
| Completed history removes only its valid recovery history objects | a same-run `.prepared-<run>` root is erased when `completed_ids` is subtracted from the run-ID set | fail |
| Staging recovery validates the complete staged run | an exact-field manifest with empty events, snapshots, inventories, transport, and fake references is accepted and recovered | fail |
| Recovery authority is a change-local review or owner decision | an unrelated repository-root Markdown file authorizes and completes recovery | fail |
| Fixed control roots have exact object kinds before routing | a regular file at `runs` is accepted by global discovery | fail |

## Finding

### BFP-CR-M2-12 - Recovery classification still substitutes run IDs and shallow shape for closed object validity

Finding ID: BFP-CR-M2-12

Prior finding reconciliation: failed-remediation

Severity: blocker

Auto-fix class: declared-safe

Location:

- `scripts/boundary_proof_behavior.py`, `_discover_global_candidate`
- `scripts/boundary_proof_behavior.py`, `_completed_recovery_is_valid`
- `scripts/boundary_proof_behavior.py`, `_validate_staged_run`
- `scripts/boundary_proof_behavior.py`, `discard_interrupted_publication`
- `scripts/test-boundary-proof.py`, T51 recovery proof

Evidence:

- A completed lease-only recovery plus `.prepared-<same-run>` returns no active
  candidate.
- A syntactically complete but semantically empty staged run completes
  discard-and-regenerate recovery.
- `unrelated-owner-note.md` outside the change record is accepted as
  authorization evidence.
- A regular file at `evidence/simple-change/runs` does not fail global
  discovery.

Required outcome: Make global discovery and recovery operate on validated
object-level state, use one complete staged-run validity projection, constrain
authority to exact change-local review/decision surfaces, and reject malformed
fixed roots before routing.

Safe resolution path:

- Inputs: R28y global ordering, completed-history predicate, complete staged-run
  contract, authorization evidence locality, and fixed namespace.
- Outputs: typed object inventory rather than run-ID subtraction; complete
  staged payload validation shared with publication; closed authority path
  predicate; fixed-root type checks; direct sibling regressions.
- Allowed paths: M2 harness/tests/evidence, validation notes, review resolution,
  and active-plan state.
- Forbidden paths: M3/M4 behavior, release activation, external actions,
  PR/deployment surfaces, and unrelated refactors.
- Acceptance criteria: all four R6 probes reject before unauthorized mutation
  or lifecycle invocation; valid completed histories remain inert beside
  different-run candidates; valid stale staging remains recoverable without
  adopting bytes; focused and canonical validation pass.
- Required validation: complete boundary-proof suite; direct R6 regressions;
  canonical regeneration because harness identity changes; skill/build,
  metadata, review, lifecycle, and diff checks.

No owner decision is required because R28y already defines these boundaries.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Four closed R28y boundaries remain executable escapes. |
| Test coverage | block | The 93-test suite omits the reproduced sibling states. |
| Edge cases | block | Same-run active objects, empty staged semantics, authority locality, and fixed-root types are unproved. |
| Error handling | block | Invalid state can reach durable recovery or fresh-generation eligibility. |
| Architecture boundaries | concern | Typed nested validators exist, but global classification remains run-ID based. |
| Compatibility | pass | Opaque v1 and unsupported v2 behavior are unaffected. |
| Security/privacy | block | Destructive recovery accepts authority outside the change-local decision record. |
| Derived artifact currency | concern | The current run passes but does not exercise the failing branches. |
| Unrelated changes | pass | The reviewed slice remains within M2. |
| Validation evidence | block | Passing checks do not include the four direct R6 probes. |

## Prior finding reconciliation

- `BFP-CR-M2-11`: failed-remediation; its four named probes are fixed, but
  sibling members of the same recovery classes still escape.
- `BFP-CR-M2-12`: new residual finding for the independently reproduced
  object-validity and authority-containment gaps.

## Handoff

M2 remains `resolution-needed`.
Enter review resolution for `BFP-CR-M2-12`, add the direct sibling regressions,
replace run-ID/shallow classification with closed object-level validity, and
rerun code review.
M3, final closeout, verify, and PR handoff remain blocked.
