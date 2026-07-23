# Code Review: M4 R5 Capability Binding and Durable Review State

Review ID: code-review-m4-r5
Stage: code-review
Round: M4 R5
Reviewer: Codex code-review skill in isolated direct-review mode
Target: M4 correction commit `e60090d7`
Reviewed artifact: M4 correction commit `e60090d7`
Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-23
Recording status: recorded
Material findings: BRF-M4-CR11, BRF-M4-CR12
Immediate next stage: review-resolution M4

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M4-CR11` and `BRF-M4-CR12` block M4 closeout
- Next stage: review-resolution M4
- Review status: changes-requested
- Material findings: `BRF-M4-CR11`, `BRF-M4-CR12`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m4-r5.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m4-r5`
- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution and rereview, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M4-CR11`, `BRF-M4-CR12`
- Verify readiness: not-claimed

## Review Inputs

- Review surface: commit `e60090d7` against the pre-correction review commit `187d53d5`, with production code inspected before changed tests, validation notes, and the R4 review record.
- Tracked governing branch state: clean worktree at `e60090d7` before R5 review evidence was recorded.
- Governing requirements: BRF-R032-BRF-R046, BRF-R047-BRF-R066, BRF-R078-BRF-R080, BRF-R099, and BRF-R100.
- Test contract: T10-T12 and the M4 CMD15-CMD20 proof boundary.
- Architecture: immutable policy projection, exact effective-capability binding, sole state writer, prepared receipt, independent review/correction stages, and fail-closed durable validation.
- Prior review and resolution: `code-review-m4-r4.md` and `BRF-M4-CR7` through `BRF-M4-CR10`, consulted only after the blind-first code, test, and direct-probe pass.

## Blind-First Risk Map

- Affected behavior: closed proposal-correction execution, rejected-mutation rollback, durable proposal-review projection, and later-target correction-loop selection.
- Highest-impact failures: recipe text not governing bytes, rejected or escaped mutations surviving, stale correction authority driving a new review, and contradictory durable pause state being accepted.
- Changed boundaries: canonical review resolution to executable operation; proposal file to atomic replacement and rollback; verified review occurrence to durable run state; active correction capabilities to correction-loop routing.
- Expected evidence: exact operation and unsupported-recipe contrasts, callback non-execution, atomic failure and rejected-postcondition rollback, exhaustive outcome routing, exact current capability identity binding, and pause-reason consistency.
- Direct-inspection areas: `_compile_proposal_correction_operation`, `_atomic_replace_regular_file`, `coordinate_non_public_authoring_stage`, `project_proposal_review_result`, `resolve_active_proposal_correction_capability`, `finalize_transition`, and durable validator consistency.
- Intentionally out of scope: M5 implementation/verification integration, M6 public activation and compatibility cutover, final holistic review, verification, PR, and external actions.
- Applicable risk classes: authorization containment, stale authority, partial-failure recovery, durable-state integrity, review/correction independence, and proof sufficiency.
- Non-applicable risk classes: credentials, network, database, UI, deployment, and generated adapters.
- Falsifiable questions: Can a stale correction capability produce `correction-loop` for a new review? Can an active run retain a stale pause reason after an approved `continue` result? Can caller correction code execute? Can a rejected correction leave proposal bytes changed?

## Diff Summary

The correction replaces free-form proposal mutation callbacks with one closed
recipe compiler and one atomic regular-file replacement. It restores original
proposal bytes when a later postcondition rejects the transaction.

Proposal-review routing now uses one shared pure projection from the helper,
state finalizer, and validator. The finalizer can persist `correction-loop` and
records the selected correction capability ID.

The exact-operation and rollback corrections resolve the R4 mutation findings.
Two durable binding gaps remain: correction-loop selection does not bind the
candidate capability to the just-finalized review/proposal identities, and the
validator does not reject a stale run-level pause reason when the canonical
review route is non-paused.

## Prior-Finding Reconciliation

| Prior finding | R5 result | Evidence |
| --- | --- | --- |
| `BRF-M4-CR7` | resolved | The only accepted recipe compiles to an exact byte append; unsupported recipe text fails before invocation, and caller mutation code is not executed. |
| `BRF-M4-CR8` | resolved | Correction owns one atomic regular-file replacement, callback escape code cannot run, atomic replacement failure leaves no mutation, and rejected postconditions restore original bytes. |
| `BRF-M4-CR9` | failed-remediation | The shared projection rejects the reported result-field contradictions, but an active run with canonical `continue` still accepts a stale run-level `pause_reason`. The remaining defect is `BRF-M4-CR12`. |
| `BRF-M4-CR10` | failed-remediation | The transactional branch exists, but it selects an active correction capability without proving its review-record and reviewed-proposal identities match the occurrence just finalized. The remaining defect is `BRF-M4-CR11`. |

## Findings

## Finding BRF-M4-CR11

Finding ID: BRF-M4-CR11
Severity: major
Location: `scripts/validate_workflow_automation.py:130-169`; `scripts/workflow_automation_state.py:982-1005`; coverage at `scripts/test-workflow-automation.py:1429-1469`
Evidence: `resolve_active_proposal_correction_capability` considers status, kind, stage, parent status, and remaining budget, but does not compare `basis.review_record_identity` or `basis.reviewed_proposal_identity` with the review proof being finalized. The transactional positive fixture itself overwrites the review record after creating the correction capability. A direct probe persisted `routing_action: correction-loop` and selected `cap-correction-transaction` even though the capability review hash and current review hash differed; `validate_workflow_automation` returned no errors.
Required outcome: A correction-loop route must bind exactly one active correction capability whose reviewed proposal identity, review-record identity, finding evidence, parent authority, and remaining budget are current for the just-recorded review occurrence.
Safe resolution path: Make capability selection accept the verified proposal identity and canonical review-record identity as required inputs, compare them with the capability basis before returning an ID, and use the same identity-aware selector in finalization and durable validation. Replace the positive fixture with a capability derived from the exact finalized review evidence and add stale-review, stale-proposal, absent, invalid-budget, and ambiguous-capability transactional contrasts.
needs-decision rationale: none; BRF-R037, BRF-R044, BRF-R046, and BRF-R054 already require current, unique capability authority.
auto_fix_class: none

## Finding BRF-M4-CR12

Finding ID: BRF-M4-CR12
Severity: major
Location: `scripts/validate_workflow_automation.py:1401-1444`; coverage at `scripts/test-validate-workflow-automation.py:430-469`
Evidence: Durable validation compares `latest_review_result` with the shared projection and compares `run.status`, but it never validates the run-level `pause_reason`. A direct probe set an approved later-target result to `continue`, kept `run.status: active`, added `run.pause_reason: stale-blocker`, and received no validation errors. Status output can therefore report a human-decision reason that contradicts the canonical non-paused route.
Required outcome: Durable run pause evidence must be an exact projection of proposal-review routing: paused routes require the matching run-level reason, while active and completed routes must not retain one.
Safe resolution path: Extend the shared projection or its durable consistency check to compare the expected run pause reason as well as status. Add positive and negative tests for blocked, inconclusive, authorization-required, correction-loop, continue, and stop-at-target routes, including missing, wrong, and stale run-level reasons.
needs-decision rationale: none; BRF-R047, BRF-R055, BRF-R099, and BRF-R100 already require coherent durable pause reporting.
auto_fix_class: none

## Requirement Fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| BRF-R037 and BRF-R044 current capability basis | block | A review-record identity mismatch still qualifies for correction-loop routing. |
| BRF-R046 unique active stage occurrence | pass with concern | Multiple active proposal-correction occurrences fail closed, but uniqueness does not establish current identity binding. |
| BRF-R047-BRF-R058 occurrence/gate/route projection | block | Result fields and run status are canonical, but stale run-level pause evidence is accepted. |
| BRF-R060-BRF-R062 independent deterministic correction | pass | Review and correction remain separate, and the closed recipe alone determines the proposal mutation. |
| BRF-R065-BRF-R066 rollback and rereview | pass | Rejected postconditions restore bytes; successful mutation stales the old proposal identity and derives fresh review authority. |
| BRF-R078-BRF-R080 policy and isolation | pass with concern | One shared projection replaces duplicated routing, but current-capability selection remains under-bound. Public routing remains unchanged. |
| BRF-R099-BRF-R100 durable reporting | block | A stale run pause reason can contradict the tracked review projection. |

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Current capability basis and durable pause-state requirements remain incomplete. |
| Test coverage | block | The correction-loop positive fixture uses mismatched review identity, and no test checks run-level pause-reason absence or equality. |
| Edge cases | block | Direct stale-capability and stale-pause probes both pass when they must fail closed. |
| Error handling | pass | Atomic replacement failure and rejected postconditions leave original proposal bytes in place. |
| Architecture boundaries | concern | The sole state writer and shared policy projection are preserved, but the writer receives an under-bound capability selection result. |
| Compatibility | pass | Public workflow, legacy adapter, schema, and external-action surfaces are unchanged in this M4 correction. |
| Security/privacy | block | Stale executable authority can control correction routing for a different review occurrence. |
| Derived artifact currency | pass | No generated or public adapter artifact changed. |
| Unrelated changes | pass | The diff is limited to R4 corrections, tests, and lifecycle evidence. |
| Validation evidence | concern | Focused suites pass, but two direct adversarial probes expose untested accepted states. |

## Validation and Direct Proof

- `python scripts/test-workflow-automation.py -k proposal_review` passed 5 tests.
- `python scripts/test-workflow-automation.py -k proposal_correction` passed 8 tests.
- `python scripts/test-validate-workflow-automation.py` passed 55 tests.
- `git diff 187d53d5..e60090d7 --check` passed.
- Direct stale-capability probe persisted `correction-loop` with mismatched capability/current review hashes and returned no durable validation errors.
- Direct stale-pause probe accepted `run.status: active`, canonical `routing_action: continue`, and `run.pause_reason: stale-blocker`.
- Source inspection confirmed caller correction callbacks cannot run, rejected postconditions restore original proposal bytes, and public or legacy routing is unchanged.

## No-Finding Rationale

Not applicable; this review has two material findings.

## Residual Risks

Rereview must prove identity-current correction capability selection and exact
run-level pause projection. M5 and M6 remain outside this review surface.

## Milestone Handoff

- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M4-CR11` and `BRF-M4-CR12`
- Remaining in-scope implementation milestones: M4 resolution and rereview, M5, M6
- Next stage: review-resolution M4
- Final closeout readiness: not ready because M4 has two open material findings and M5-M6 remain unimplemented
- Verify readiness: not-claimed
- Isolation: this direct review performs no automatic downstream handoff
