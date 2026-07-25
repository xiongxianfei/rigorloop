# Code Review M6 R4

Review ID: code-review-m6-r4
Stage: code-review
Round: M6 R4
Reviewer: independent same-session context-reset reviewer
Target: M6 correction commit `d59bd2b1`
Reviewed artifact: M6 correction commit `d59bd2b1`
Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-25
Recording status: recorded
Material findings: BRF-M6-CR10
Immediate next stage: review-resolution M6

## Review context

- Invocation mode: direct isolated milestone rereview
- Independence level: `L1-same-session-context-reset`
- Review surface: commit `d59bd2b1` against parent `bf42662d`
- Requirement-fidelity gate: applied to `BRF-R068` through `BRF-R077`, T28, and T30
- Risk tier: elevated
- Automated independent-review gate: not required for this direct isolated invocation
- Context limitation: the reviewer shares the implementation session, intentionally reset to the actual commit, approved specification, active test specification, and current M6 plan, and does not claim blind L2 independence

## Independent risk map

### Affected behavior

- Durable pause and reactivation at the verification authorization boundary.
- Evidence-first recovery of public prepared transitions.
- Composed deterministic proof for interruption and correction scenarios.

### Highest-impact failure modes

- Recovery succeeds only for ordinary artifact stages but strands correction transitions whose completion has stage-specific side effects.
- A restarted coordinator silently depends on state that existed only in the lost process.
- Valid completion evidence leaves the run paused with an active capability and prepared receipt.
- A passing named interruption fixture overstates recovery coverage across stage families.

### Changed boundaries

- `scripts/workflow_automation.py`: public resume and prepared-transition recovery.
- `scripts/workflow_automation_state.py`: durable run pause.
- `scripts/test-workflow-automation.py`: T28/T30 public composition proof.

### Expected evidence

- Missing verification authority durably pauses and later repository-backed authorization reactivates the run.
- Recovery retains the original transition key, receipt, and effective capability.
- Stage-specific post-completion work can be reconstructed from durable basis and verified repository evidence after process loss.
- No stage mutation is repeated when valid completion evidence already exists.

### Direct-inspection areas

- `resume_public_run`.
- `coordinate_one_stage`.
- Proposal-correction invocation and fresh-rereview capability derivation.
- The interruption branch of `test_public_composition_is_deterministic_and_order_independent`.

### Intentionally out-of-scope areas

- Final holistic cross-milestone review.
- `explain-change`, final `verify`, and PR handoff.
- Closed M1-M5 behavior except where M6 exposes it publicly.

### Risk classes

- Applicable: authorization integrity, durable state, process interruption, correction containment, recovery idempotency, and proof fidelity.
- Not applicable: personal-data processing, cryptographic protocol design, accessibility UI, and deployed-service availability.

### Falsifiable questions

- Does missing verification authority persist the exact required pause without creating a capability or receipt?
- Can public resume reconcile a prepared `spec` transition without reinvoking the stage?
- Can public resume reconcile a prepared proposal-correction transition after process loss using only durable state and verified completion evidence?
- Does recovery preserve the original transition and capability without silently deriving replacement authority?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, `review-log.md`, `review-resolution.md`, `change.yaml`, active plan, and plan index
- Open blockers: `BRF-M6-CR10`
- Next stage: review-resolution M6
- Review status: changes-requested
- Material findings: `BRF-M6-CR10`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m6-r4.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m6-r4`
- Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M6 resolution and rereview
- Required review-resolution: yes
- Finding IDs: `BRF-M6-CR10`
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `d59bd2b1` against parent `bf42662d`.
- Tracked governing branch state: approved specification, approved test specification, approved architecture, accepted ADR, active M6 plan, and recorded R3 resolution.
- Direct proof: a temporary public proposal-correction run was interrupted after the atomic proposal replacement but before receipt finalization. The original receipt remained `prepared` and its effective capability remained `active`. A fresh public resume supplied valid repository-backed completion evidence for the same receipt and capability, but failed with `proposal correction paused: mutation escaped effective capability`; the durable run became paused while the receipt and capability remained prepared/active.
- Validation evidence challenged: the implementation reports 71 passing engine tests and T30 now proves same-receipt recovery for `spec`, but the interruption branch does not exercise correction recovery or any post-completion callback that must be reconstructed after restart.

## Diff summary

The correction adds a sole-writer durable pause for missing verification authority and reactivates the run after later repository-backed authorization.

It also teaches the one-stage coordinator to find one existing prepared receipt, validate its immutable transition and capability binding, inspect supplied completion evidence, reconcile the original receipt without stage reinvocation, or reuse it for a policy-permitted retry.

The T30 interruption scenario now leaves a `spec` receipt prepared across a simulated process loss and resumes that same transition under the controlled environment.

## Findings

### BRF-M6-CR10 - Proposal-correction recovery depends on transient state from the lost invocation

Finding ID: BRF-M6-CR10
Severity: blocker
Location: `scripts/workflow_automation.py:1890-1894`, `scripts/workflow_automation.py:1942-1959`, `scripts/workflow_automation.py:1973-2016`, `scripts/workflow_automation.py:4532-4547`, and `scripts/test-workflow-automation.py:1797-1968`
Evidence: `derive_post_correction_capabilities` requires `actual_changed_paths` and `expected_proposal_identity_after`, but those closure variables are populated only by `invoke_bounded_proposal_correction` in the original process. Recovery correctly skips stage reinvocation and calls the newly constructed post-completion callback with verified durable proof; its closure therefore still contains the defaults `frozenset()` and `None`. A direct public reproduction interrupted immediately after the atomic proposal replacement, confirmed the same receipt remained `prepared` and the same capability `active`, then resumed with valid completion evidence for that exact proposal identity. Recovery failed with `proposal correction paused: mutation escaped effective capability`, leaving the run paused, receipt prepared, and capability active. This violates the universal `BRF-R074` requirement that a prepared transition with valid completion evidence reconcile without rerunning the stage. The new T30 interruption fixture covers only `stage="spec"`, whose recovery has no stage-specific post-completion derivation, so its passing result cannot detect this boundary.
Required outcome: Every stage that supports prepared-transition recovery must reconstruct completion validation and post-completion authority effects entirely from durable receipt/capability basis, current repository evidence, and verified completion proof; proposal-correction recovery must complete the original receipt and activate exactly one fresh proposal-review capability without repeating the correction mutation.
Safe resolution path: Refactor proposal-correction post-completion derivation into a restart-safe stage operation that deterministically recomputes the compiled correction result, affected path set, and expected proposal identity from the persisted correction capability and current artifact bytes, or persist any irreducible operation projection before mutation. Add a public crash-after-proposal-write regression that recreates the coordinator, supplies independently serialized completion evidence, asserts zero mutation reinvocation, finalizes the same receipt/capability, and activates the fresh rereview capability atomically. Audit other `post_completion_capabilities` users for the same transient-state dependency.
needs-decision rationale: none; `BRF-R068` through `BRF-R077` already require evidence-first, same-receipt, no-rerun recovery.
auto_fix_class: none

## Prior finding reconciliation

| Finding | Result | Evidence |
| --- | --- | --- |
| `BRF-M6-CR8` | resolved | The zero-parent verification path now writes `run.status: paused` with `verification-authorization-required`; the direct regression asserts no capability or receipt and later repository-backed authorization reactivates the run. |
| `BRF-M6-CR9` | failed-remediation | The original prepared receipt is now recovered for the simple `spec` fixture and status/state observations are controlled, but the public correction path still cannot recover its own prepared transition after process loss. Residual restart-safety failure is recorded as `BRF-M6-CR10`. |

## Requirement-fidelity result

| Contract | Result | Evidence |
| --- | --- | --- |
| `BRF-R043e` | pass | Missing verification authority now durably pauses with the exact reason and later concrete authorization reactivates the run. |
| `BRF-R068` through `BRF-R073`, `BRF-R075` through `BRF-R077` | pass for reviewed generic path | Prepared receipt selection, transition-key/capability binding, evidence-first decision, retry-policy handling, and same-receipt finalization are present in the generic coordinator. |
| `BRF-R074` | block | Proposal correction has valid completion evidence but cannot reconcile after restart because its post-completion checks require lost in-memory variables. |
| T28 / T30 | block | T30 directly proves simple `spec` recovery but not recovery of the public correction transaction included in the composed mechanism. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `BRF-M6-CR10` violates the universal valid-evidence reconciliation requirement. |
| Test coverage | block | The only process-interruption recovery case uses `spec` and misses stage-specific post-completion effects. |
| Edge cases | block | Process loss after correction mutation but before finalization is a named recovery boundary and fails directly. |
| Error handling | block | Valid completion evidence strands a prepared receipt and active correction capability behind a paused run. |
| Architecture boundaries | concern | The sole writer and effective-capability binding are preserved, but executable recovery still depends on coordinator-local state rather than durable evidence. |
| Compatibility | pass | The reviewed correction does not re-enable legacy writers or remove compatibility aliases. |
| Security/privacy | pass | No external action or sensitive-data surface is introduced by this correction. |
| Derived artifact currency | pass | No generated adapter output is hand-edited in the reviewed correction. |
| Unrelated changes | pass | The diff is limited to the two R3 corrections, their proof, and lifecycle state. |
| Validation evidence | block | Passing engine and composed tests do not cover the directly failing correction-recovery contrast. |

## Direct-proof gaps

- No test interrupts proposal correction after its artifact write and resumes through a freshly constructed coordinator.
- No test proves that correction post-completion capability activation is derivable without invocation-local variables.
- No restart audit covers other stage-specific post-completion hooks.

## Milestone handoff

- Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M6-CR10`
- Remaining in-scope implementation milestones: M6 resolution and rereview
- Next stage: review-resolution M6
- Final closeout readiness: not ready
- Reason: M6 has one open material finding; final holistic code review, explain-change, verify, and PR handoff remain pending.

## Isolation

This direct code-review is isolated. It records the finding and synchronized lifecycle state but does not apply the fix or start review-resolution automatically.
