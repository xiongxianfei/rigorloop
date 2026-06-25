# Validation Execution Performance and Preflight Test Spec

## Status

active

## Related spec and plan

- Spec: [Validation Execution Performance and Preflight](validation-execution-performance-and-preflight.md)
- Plan: [Preflight-First and Measured Script Execution Optimization Plan](../docs/plans/2026-06-24-preflight-first-measured-script-execution-optimization.md)
- Architecture/ADRs: not applicable; architecture assessment recorded `architecture-not-required`

## Testing strategy

Unit and integration coverage focuses on `scripts/validation_selection.py`, `scripts/select-validation.py`, and `scripts/ci.sh`, because those are the contributor-facing selection and selected-CI execution surfaces for the first slice. Existing broad smoke, lifecycle, change-metadata, and review-artifact validators provide regression coverage for lifecycle evidence and workflow artifacts. Manual verification is limited to final verify sequencing and absence of self-referential hash evidence.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T1, T2 | integration | Selector preflight records run before selected checks are executed. |
| R2 | T1, T2 | integration | Git worktree, unmerged-path, and tracked-authoritative checks are represented in preflight. |
| R3 | T2, T8 | integration | Blocking selector status prevents selected CI execution. |
| R4 | T2 | integration | Blocker includes path and corrective action. |
| R5 | T7 | integration | Selected CI only runs after selector status is `ok`. |
| R6 | T8 | integration | Selector-blocked status stops selected checks. |
| R7 | T4, T5 | unit | Boundary triggers remain visible through broad-smoke and release/package check selection. |
| R8 | T6, T7, T8 | integration | Existing command catalog and exit behavior remain trusted. |
| R9 | T7 | integration | Selected CI summary records elapsed time per check. |
| R10 | T7 | integration | Selected CI records phase timing summary. |
| R11 | T9 | manual | Representative baseline records cold/warm distinction when performance evidence is gathered. |
| R12 | T3, T7 | integration | Selection output includes changed paths, selected checks, reasons, and phases. |
| R13 | T10 | manual | Shared context reduction is verified by Git-inspection count when introduced. |
| R14 | T6 | integration | Standalone selector and validator command contracts remain trusted. |
| R15 | T11 | unit | Cache status remains `not-applicable`; no closeout cache proof is introduced. |
| R16 | T11 | unit | Future cache behavior is out of first-slice implementation. |
| R17 | T12 | manual | Final verify checks committed tracked state before branch-ready. |
| R18 | T12 | manual | Same-commit evidence does not require literal self hash. |
| R19 | T13 | manual | Parallelism remains existing CI wrapper behavior; no new parallel contract is enabled. |
| R20 | T9 | manual | Performance budgets remain baseline/warning evidence. |
| R21 | T9 | manual | Timing sidecar retention is recorded before detailed sidecar rollout. |
| R22 | T7 | integration | Runtime timing is measured separately from output compactness. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T2 | Untracked governing artifact blocks with corrective action. |
| E2 | T8 | Blocked selector status prevents selected checks. |
| E3 | T4, T5 | Boundary checks remain selected for broad triggers. |
| E4 | T12 | Manual final verify evidence covers committed-state wording. |
| E5 | T3, T7 | Selector JSON and selected CI output explain selected checks and timing. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | T2 | Untracked authoritative artifact preflight. |
| EC2 | T8 | Blocking selector status stops execution. |
| EC3 | T4 | Selector and validation script changes select regression checks. |
| EC4 | T12 | Final verify manual proof. |
| EC5 | T7 | Timing output preserves command result semantics. |
| EC6 | T9 | Detailed timing sidecar policy manual check. |
| EC7 | T11 | Cache remains disabled/not-applicable. |
| EC8 | T13 | No new concurrency contract. |

## Test cases

T1. Preflight pass records Git-state checks
- Covers: R1, R2
- Level: integration
- Fixture/setup: Temporary Git repository with tracked authoritative artifact.
- Steps: Run selector in explicit mode for the tracked artifact.
- Expected result: Selector JSON includes `preflight_results` with tracked-authoritative and unmerged-path pass records.
- Failure proves: Preflight evidence is absent or not run before selected validation.
- Automation location: `scripts/test-select-validation.py`

T2. Untracked authoritative artifact blocks with action
- Covers: R1, R2, R3, R4, E1, EC1
- Level: integration
- Fixture/setup: Temporary Git repository with untracked `docs/proposals/new-proposal.md`.
- Steps: Run selector in explicit mode for the untracked proposal.
- Expected result: Status is `blocked`; blocker code is `untracked-authoritative-artifacts`; corrective action is `git add -- docs/proposals/new-proposal.md`.
- Failure proves: Cheap blockers are opaque or broad validation can proceed prematurely.
- Automation location: `scripts/test-select-validation.py`

T3. Selector JSON includes phase and cache status
- Covers: R12, E5
- Level: unit
- Fixture/setup: Explicit selector request for a tracked skill path.
- Steps: Inspect `selected_checks`.
- Expected result: Each selected check includes `phase` and `cache_status: not-applicable`.
- Failure proves: Selection explanation is incomplete.
- Automation location: `scripts/test-select-validation.py`

T4. Broad-smoke selection is boundary phase
- Covers: R7, E3, EC3
- Level: unit
- Fixture/setup: Explicit selector request with `--broad-smoke`.
- Steps: Inspect selected checks.
- Expected result: `broad_smoke.repo` has `phase: boundary`; ordinary selected checks remain `focused`.
- Failure proves: Boundary triggers are not distinguishable.
- Automation location: `scripts/test-select-validation.py`

T5. Release or package boundary selection remains broad
- Covers: R7, E3
- Level: unit
- Fixture/setup: Existing release/package selector fixtures.
- Steps: Run selector tests for release and adapter paths.
- Expected result: Boundary checks remain selected when authoritative triggers apply.
- Failure proves: Optimization removed required broad proof.
- Automation location: `scripts/test-select-validation.py`

T6. Trusted command catalog compatibility remains intact
- Covers: R8, R14
- Level: integration
- Fixture/setup: Existing selected-CI command mismatch fixture.
- Steps: Run CI wrapper with tampered selector command.
- Expected result: CI rejects selector command mismatch and does not execute tampered command.
- Failure proves: Optimized selection weakened trusted command execution.
- Automation location: `scripts/test-select-validation.py`

T7. Selected CI records per-check and per-phase timing
- Covers: R9, R10, R12, R22, E5, EC5
- Level: integration
- Fixture/setup: CI wrapper selected-check fixture.
- Steps: Run selected CI.
- Expected result: Output includes selected check summary with elapsed time and phase timing summary without emitting hidden success output by default.
- Failure proves: Timing evidence is missing or output semantics regressed.
- Automation location: `scripts/test-select-validation.py`

T8. Blocked selector prevents selected check execution
- Covers: R3, R6, E2, EC2
- Level: integration
- Fixture/setup: Selector fixture with `status: blocked`.
- Steps: Run selected CI.
- Expected result: CI reports selector blocker and does not run selected checks.
- Failure proves: Focused/boundary execution can proceed after a blocker.
- Automation location: `scripts/test-select-validation.py`

T9. Performance baseline evidence is recorded before budgets
- Covers: R11, R20, R21, EC6
- Level: manual
- Fixture/setup: Representative final-verify workflow.
- Steps: Record cold/warm timing, subprocess count, Git inspection count, and sidecar retention policy.
- Expected result: Baseline/warning evidence exists; no hard performance budget gate is introduced.
- Failure proves: Performance claims are unsupported.
- Automation location: manual proof in change-local evidence.

T10. Shared context reduces repeated repository inspection
- Covers: R13
- Level: manual
- Fixture/setup: Representative composed validation bundle.
- Steps: Compare Git inspection count before and after shared immutable context introduction.
- Expected result: Count decreases or the change records why no safe reduction was available.
- Failure proves: Shared-context milestone did not reduce duplicate work or record why.
- Automation location: manual proof in change-local evidence.

T11. Cache remains disabled for first slice
- Covers: R15, R16, EC7
- Level: unit
- Fixture/setup: Selector JSON and selected CI output.
- Steps: Inspect selected check metadata.
- Expected result: `cache_status` is `not-applicable`; no final closeout cache hit is accepted as proof.
- Failure proves: First slice introduced unsafe result reuse.
- Automation location: `scripts/test-select-validation.py`

T12. Final verify uses stable committed-state evidence
- Covers: R17, R18, E4, EC4
- Level: manual
- Fixture/setup: Final verify stage.
- Steps: Inspect explain-change, verify report, current `HEAD`, and worktree state.
- Expected result: Branch readiness is tied to current committed state; same-commit evidence avoids literal mutable final commit hash requirements.
- Failure proves: Final verify evidence can become stale or self-invalidating.
- Automation location: final `verify` evidence.

T13. No new parallel validation contract is enabled
- Covers: R19, EC8
- Level: manual
- Fixture/setup: Selected CI wrapper and proposal follow-up list.
- Steps: Inspect diff and selected-CI behavior.
- Expected result: Existing bounded selected-CI concurrency is preserved, but no new parallel validation contract is introduced for preflight-first optimization.
- Failure proves: First slice introduced unreviewed concurrency behavior.
- Automation location: code review and final verify.

## Fixtures and data

Temporary Git repositories in `scripts/test-select-validation.py` exercise tracked and untracked authoritative artifact states. Existing selected-CI fixture payloads exercise blocked selectors, command mismatch, parallel-safe grouping, failures, timeouts, and output handling.

## Mocking/stubbing policy

Use temporary Git repositories and stub child scripts for shell-wrapper tests. Do not mock selector result parsing where command trust or preflight output is under test.

## Migration or compatibility tests

Existing selected-CI fixtures remain compatibility tests for command catalog trust, output shape, timeout behavior, and parallel-safe grouping. Standalone selector CLI JSON remains backward-compatible with additive fields.

## Observability verification

Automated tests verify selected check reasons, phase metadata, preflight results, elapsed times, and phase timing summary output.

## Security/privacy verification

Trusted command mismatch tests verify selector JSON cannot substitute arbitrary command text. Evidence must not include secrets or private keys.

## Performance checks

Automated tests prove timing fields exist. Representative runtime improvement is measured manually during implementation and final verify because wall-clock budgets are machine-sensitive.

## Manual QA checklist

- Confirm no cache hit is used as final closeout proof.
- Confirm no new parallel validation contract is enabled.
- Confirm final verify evidence uses current committed state and stable wording.
- Confirm detailed timing sidecar retention is recorded before sidecar rollout.

## What not to test and why

- Do not test remote/shared cache behavior; it is out of scope.
- Do not test a new process pool or concurrency scheduler; first-slice parallel expansion is out of scope.
- Do not test hosted CI redesign; local selected-CI behavior is the target.

## Uncovered gaps

None for the first implementation slice. Caching, parallel check execution, hosted-CI reuse, and persistent workers require separate specs or follow-up proposals.

## Next artifacts

- implement
- code-review
- explain-change
- verify

## Follow-on artifacts

None yet

## Readiness

Active; implementation milestones are closed and final lifecycle verification remains pending.
