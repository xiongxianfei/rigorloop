# Code Review M6 R5

Review ID: code-review-m6-r5
Stage: code-review
Round: M6 R5
Reviewer: independent same-session context-reset reviewer
Target: M6 correction commit `b57fd9df`
Reviewed artifact: M6 correction commit `b57fd9df`
Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-25
Recording status: recorded
Material findings: BRF-M6-CR11
Immediate next stage: review-resolution M6

## Review context

- Invocation mode: direct isolated milestone rereview
- Independence level: `L1-same-session-context-reset`
- Review surface: commit `b57fd9df` against parent `e9f4c7b7`
- Requirement-fidelity gate: applied to `BRF-R068` through `BRF-R077`, T28, and T30
- Risk tier: elevated
- Automated independent-review gate: not required for this direct isolated invocation
- Context limitation: the reviewer shares the implementation session, intentionally reset to the actual commit, approved specification, active test specification, and current M6 plan, and does not claim blind L2 independence

## Independent risk map

### Affected behavior

- Fresh-process proposal-correction completion reconciliation.
- Consumption of the original correction capability.
- Atomic activation of replacement proposal-review authority.

### Highest-impact failure modes

- Recovery replays the proposal mutation.
- Reconstructed proposal bytes do not bind to the reviewed proposal identity.
- The original receipt completes while replacement authority is derived from unbound recovery-time input.
- Recovery output changes according to process-local or caller-supplied values.

### Changed boundaries

- `scripts/workflow_automation.py`: correction-result reconstruction and replacement capability derivation.
- `scripts/test-workflow-automation.py`: public crash-after-write recovery proof.

### Expected evidence

- The exact reviewed prefix and closed correction payload are reconstructed from durable authority and current bytes.
- The original receipt and capability settle without invoking the proposal write again.
- Historical review evidence remains unchanged.
- Every replacement-capability field is derived from durable transaction or verified repository evidence.

### Direct-inspection areas

- `_verify_applied_proposal_correction`.
- `derive_post_correction_capabilities`.
- Persisted-capability matching in `coordinate_one_stage`.
- The public proposal-correction recovery regression.

### Intentionally out-of-scope areas

- Final holistic cross-milestone review.
- `explain-change`, final `verify`, and PR handoff.
- Closed M1-M5 behavior except where M6 exposes it publicly.

### Risk classes

- Applicable: durable authority, interruption recovery, deterministic evidence, correction replay, and audit integrity.
- Not applicable: personal-data processing, cryptographic protocol design, accessibility UI, and deployed-service availability.

### Falsifiable questions

- Does recovery reject a current proposal that is not exactly the reviewed bytes plus the compiled payload?
- Does recovery avoid every second proposal write?
- Does fresh capability creation use only fields bound by the original receipt or effective capability?
- Can changing a recovery-only request field change durable completed state?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, `review-log.md`, `review-resolution.md`, `change.yaml`, active plan, and plan index
- Open blockers: `BRF-M6-CR11`
- Next stage: review-resolution M6
- Review status: changes-requested
- Material findings: `BRF-M6-CR11`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m6-r5.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m6-r5`
- Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M6 resolution and rereview
- Required review-resolution: yes
- Finding IDs: `BRF-M6-CR11`
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `b57fd9df` against parent `e9f4c7b7`.
- Tracked governing branch state: approved specification, approved test specification, approved architecture, accepted ADR, active M6 plan, and recorded R4 resolution.
- Direct proof: a temporary public correction transaction was interrupted after proposal replacement. Recovery reused the same prepared receipt and capability but changed only the new invocation's `derived_at` from `2026-07-22T00:01:00Z` to `2099-01-01T00:00:00Z`. The original receipt completed and the fresh proposal-review capability persisted the unbound `2099` value.
- Validation evidence challenged: the new recovery regression and ordinary proposal correction test pass, but the regression reuses the original `derived_at` and does not test whether replacement authority is invariant to recovery-only caller input.

## Diff summary

The correction reconstructs the applied proposal mutation by removing the compiled payload from current bytes, comparing the remaining prefix with the persisted reviewed proposal identity, and matching the rehashed current artifact with verified completion evidence.

It replaces invocation-local changed-path and expected-identity checks with that reconstruction, preserves rollback tracking for ordinary in-process failures, and adds public same-receipt process-loss proof with mutation-replay trapping.

## Findings

### BRF-M6-CR11 - Replacement authority still trusts an unbound recovery timestamp

Finding ID: BRF-M6-CR11
Severity: major
Location: `scripts/workflow_automation.py:2071-2085`, `scripts/workflow_automation.py:4480-4516`, and `scripts/test-workflow-automation.py:4592-4669`
Evidence: Fresh proposal-review capability derivation still uses `coordination.get("derived_at")`, a field supplied by the new resume invocation. When a persisted capability already exists, `coordinate_one_stage` validates its parent, stage, basis, path roots, mutation categories, and correction scope but does not bind the new `derived_at` argument to the persisted capability or transition key. A direct crash/recovery reproduction changed only that recovery argument from `2026-07-22T00:01:00Z` to `2099-01-01T00:00:00Z`; the same prepared receipt completed and the activated proposal-review capability stored `2099-01-01T00:00:00Z`. The new regression reuses the same request dictionary and therefore misses this process-state/caller-input dependence. The proposal bytes are now reconstructed safely, but replacement authority is not yet derived entirely from durable transaction evidence as required by the accepted `BRF-M6-CR10` outcome and T30 determinism contract.
Required outcome: Fresh proposal-review capability creation during normal completion and recovery must derive every durable field, including `derived_at`, from the original persisted capability, receipt, or another explicitly bound deterministic source; changing an unbound resume argument must not change finalized state.
Safe resolution path: Use a documented durable timestamp source such as the original correction capability's validated `derived_at`, or add an approved bound transition field if a distinct settlement time is required. Reject or ignore recovery-time `derived_at` when the capability already exists. Extend the crash-after-write regression with altered and omitted recovery timestamps and assert identical canonical state, receipt, consumed capability, and fresh capability across both resumes.
needs-decision rationale: none; the existing deterministic recovery and durable capability contracts define the required behavior.
auto_fix_class: none

## Prior finding reconciliation

| Finding | Result | Evidence |
| --- | --- | --- |
| `BRF-M6-CR10` | failed-remediation | Proposal mutation reconstruction and no-replay settlement now work, but fresh proposal-review authority still depends on the new invocation's unbound `derived_at`. Residual durable-authority nondeterminism is recorded as `BRF-M6-CR11`. |

## Requirement-fidelity result

| Contract | Result | Evidence |
| --- | --- | --- |
| `BRF-R068` through `BRF-R073`, `BRF-R075` through `BRF-R077` | pass for reviewed path | The original prepared receipt, transition key, effective capability, and verified artifact identities remain bound and settle through the sole writer. |
| `BRF-R074` | concern | Mutation and receipt reconciliation avoid stage replay, but atomic replacement authority includes one recovery-time field not bound by the original transaction. |
| T28 / T30 | block | Changing only the recovery invocation timestamp changes durable capability state, contradicting process-state and order independence. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | Receipt and mutation recovery satisfy the central no-rerun contract, but replacement authority is not fully durable-input-derived. |
| Test coverage | block | The new regression does not vary or omit recovery-only `derived_at`. |
| Edge cases | block | Fresh-process caller-input substitution changes durable state. |
| Error handling | concern | Invalid timestamp shapes fail, but any valid RFC3339 value is accepted during recovery. |
| Architecture boundaries | concern | The state writer remains sole owner, but the coordinator supplies unbound audit state to atomic capability activation. |
| Compatibility | pass | No legacy writer, alias, or migration behavior changed. |
| Security/privacy | pass | No secrets, external actions, or broader mutation authority are introduced. |
| Derived artifact currency | pass | No generated output changed. |
| Unrelated changes | pass | The diff is limited to correction recovery, its proof, and lifecycle evidence. |
| Validation evidence | block | Passing focused and broad suites do not detect the directly reproduced recovery-input nondeterminism. |

## Direct-proof gaps

- No recovery test changes or omits `derived_at` after the original capability is persisted.
- No canonical-state comparison proves replacement authority is identical across fresh-process invocation variants.

## Milestone handoff

- Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M6-CR11`
- Remaining in-scope implementation milestones: M6 resolution and rereview
- Next stage: review-resolution M6
- Final closeout readiness: not ready
- Reason: M6 has one open material finding; final holistic code review, explain-change, verify, and PR handoff remain pending.

## Isolation

This direct code-review is isolated. It records the finding and synchronized lifecycle state but does not apply the fix or start review-resolution automatically.
