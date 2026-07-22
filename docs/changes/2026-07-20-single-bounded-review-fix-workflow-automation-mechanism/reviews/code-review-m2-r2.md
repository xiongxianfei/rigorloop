# Code Review M2 R2

Review ID: code-review-m2-r2
Stage: code-review
Round: M2 R2
Reviewer: Codex code-review skill with context-isolated blind-first reviewer
Target: M2 correction commit `f41506ef`
Reviewed artifact: M2 correction commit `f41506ef`
Reviewed milestone: M2. Sole State Writer, Prepared Receipts, and Recovery
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-22
Recording status: recorded
Material findings: BRF-M2-CR5, BRF-M2-CR6
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, `review-log.md`, `review-resolution.md`, the active plan and plan index, and `change.yaml`
- Open blockers: none
- Next stage: review-resolution M2
- Review status: changes-requested
- Material findings: BRF-M2-CR5, BRF-M2-CR6
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m2-r2.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m2-r2`
- Reviewed milestone: M2. Sole State Writer, Prepared Receipts, and Recovery
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2 resolution needed, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: BRF-M2-CR5, BRF-M2-CR6
- Verify readiness: not-claimed

## Review Inputs

- Diff range: `6bfb02e5..f41506ef`.
- Tracked governing branch state: branch `proposal/single-bounded-review-fix-automation`, clean at review start.
- Governing spec: `specs/single-bounded-review-fix-workflow-automation.md`, especially `BRF-R068`-`BRF-R077`.
- Test spec: `specs/single-bounded-review-fix-workflow-automation.test.md`, especially T14, T15, and T29.
- Architecture and ADR: the accepted sole-writer, immutable policy, canonical state-read, and capability-bound receipt boundaries.
- Active plan: M2 in `review-requested` state with M3-M6 remaining.
- Prior findings and implementation validation were withheld until after the blind-first risk map was recorded.

## Risk Map

The blind-first pass prioritized durable receipt identity, retry authority, cancellation reconciliation, query fail-closed behavior, compatibility of the required receipt projection, deterministic proof quality, and recovery call-site completeness.
Its falsifiable questions included whether canonical read recomputes transition-key integrity, whether all three retry families use valid persisted states, whether cancellation retains the original receipt binding, and whether malformed automation can reach any bounded query projection.
M3-M6 orchestration, public routing, adapters, external actions, release behavior, and final holistic review remain out of scope.

## Diff Summary

The correction resolves receipt lookup by persisted transition ID, derives retry decisions from the immutable registry, adds the retry projection to key computation, validates query state before projection, and adds repeat/reverse T29 scenarios.
`BRF-M2-CR1`, `BRF-M2-CR3`, and `BRF-M2-CR4` are resolved.
`BRF-M2-CR2` is classified as failed-remediation because canonical read does not validate the computed transition key and the claimed all-family proof uses invalid states.

## Findings

## Finding BRF-M2-CR5

Finding ID: BRF-M2-CR5
- Severity: major
- Location: `scripts/workflow_automation_state.py:98-113`, `scripts/workflow_automation_state.py:200-269`, `scripts/validate_workflow_automation.py:1064-1163`
- Evidence: Preparation checks `transition_key == compute_transition_key(receipt)`, but canonical read only requires a non-empty key and never recomputes it. A direct review reproduction changed an otherwise-valid prepared receipt's expected postcondition while retaining its old key. `validate_workflow_automation` returned no errors, the key differed from `compute_transition_key`, and recovery accepted matching completion evidence with `RecoveryDecision(action='reconcile-completed', invoke_stage=False, reason='completion-evidence-valid')`. This rediscovered the transition-key-binding portion of `BRF-M2-CR2`, so that prior remediation is `failed-remediation`.
- Required outcome: Every persisted prepared or completed receipt accepted by canonical read, status projection, or recovery must have a transition key equal to the deterministic key computed from its immutable operation inputs.
- Safe resolution path: Put transition-key computation in a dependency-safe shared helper or validate it at the state-reader boundary; fail closed with a stable error before projection or recovery. Add prepared and completed tampered-key tests through `WorkflowAutomationStateStore.read()`, recovery, and query status.
- needs-decision rationale: none

## Finding BRF-M2-CR6

Finding ID: BRF-M2-CR6
- Severity: major
- Location: `scripts/test-workflow-automation-state.py:165-189`
- Evidence: The all-three retry-family test changes only the stage name and capability kind on a proposal-review fixture, then calls the recovery evaluator directly. Canonical validation reports eight errors for the architecture-assessment case and sixteen for implement, including wrong basis, parent bounds, predecessor, and missing milestone occurrence/identity; only proposal-review is valid. Independently constructed validator-valid states produce the expected retry and manual-recovery decisions, so this is a proof failure rather than a demonstrated production decision error. T15 and the `BRF-M2-CR2` resolution require valid prepared receipts under every retry policy.
- Required outcome: Directly prove all three retry-policy families with complete validator-valid persisted automation states passing through the canonical read boundary, plus mismatch rejection.
- Safe resolution path: Extend the existing post-proposal and next-milestone fixture builders with correct parent scope, basis, predecessor/input identities, and milestone occurrence; persist and read each fixture through `WorkflowAutomationStateStore` before asserting recovery decisions.
- needs-decision rationale: none

## Prior Finding Reconciliation

| Finding | Result | Evidence |
| --- | --- | --- |
| `BRF-M2-CR1` | resolved | Recovery looks up the persisted mapping entry by transition ID, validates its embedded identity, and requires it to be the sole prepared receipt. |
| `BRF-M2-CR2` | failed-remediation | Registry-owned retry decisions are present, but persisted transition-key integrity and valid all-family proof remain incomplete in `BRF-M2-CR5` and `BRF-M2-CR6`. |
| `BRF-M2-CR3` | resolved | T29 repeats and reverses fresh-root transition and migration scenarios and compares receipt, key, migration, recovery, canonical-byte, temporary-file, and root-teardown evidence. |
| `BRF-M2-CR4` | resolved | Unified query loading uses the canonical validated read and rejects four malformed closed-vocabulary families without byte mutation. |

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `BRF-M2-CR5` leaves deterministic receipt identity unenforced after persistence. |
| Test coverage | block | `BRF-M2-CR6` does not prove two retry families through valid canonical state. |
| Edge cases | block | Persisted key drift reaches recovery; invalid-state retry fixtures bypass canonical validation. |
| Error handling | concern | Query closed-vocabulary failures are corrected, but stale transition-key input is not rejected. |
| Architecture boundaries | block | Canonical read does not enforce the deterministic receipt identity required by the state boundary. |
| Compatibility | pass | No public writer or adapter changed, and no tracked unified run predates this non-public M2 format. |
| Security/privacy | pass | No secret, external action, or credential surface changed. |
| Derived artifact currency | pass | No generated adapter or derived public artifact changed. |
| Unrelated changes | pass | The correction diff remains scoped to M2 code, tests, and lifecycle evidence. |
| Validation evidence | concern | CMD4-CMD9 pass, but direct adversarial reproductions demonstrate that the selected assertions are insufficient. |

## No-Finding Rationale

Not applicable; two material findings are recorded.

## Validation

- `python scripts/test-change-metadata-validator.py`: 53 passed.
- Direct change-metadata validation passed.
- `python scripts/test-workflow-automation-state.py`: 27 passed.
- Receipt-selected automation validator: 17 passed.
- Migration-selected automation validator: 3 passed.
- `python scripts/test-query-change-record.py`: 18 passed.
- Python compilation and commit-range diff checks passed.
- Direct stale-key reproduction was accepted by validation and recovery.
- Direct retry-fixture validation proved architecture-assessment and implement cases were not canonical valid states.

## Milestone Handoff

- Reviewed milestone: M2. Sole State Writer, Prepared Receipts, and Recovery
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M2-CR5` and `BRF-M2-CR6`
- Remaining in-scope implementation milestones: M2 resolution needed, M3, M4, M5, M6
- Next stage: review-resolution M2
- Final closeout readiness: not ready because M2 has two open findings and M3-M6 plus final closeout remain.

## Recommended Next Stage

This direct review remains isolated: no correction or downstream implementation was performed.
Enter review-resolution for `BRF-M2-CR5` and `BRF-M2-CR6`, return M2 to `review-requested` after targeted validation, and rerun M2 code review before starting M3.
