# Validation Runtime Follow-Through Test Spec

## Status

active

## Related spec and plan

- Spec: [Validation Runtime Follow-Through](validation-runtime-follow-through.md)
- Plan: [Preflight-First Validation Runtime Optimization Plan](../docs/plans/2026-06-26-preflight-first-validation-runtime-optimization.md)
- Proposal: [Preflight-First Validation Runtime Optimization](../docs/proposals/2026-06-26-preflight-first-validation-runtime-optimization.md)
- Prior spec: [Validation Execution Performance and Preflight](validation-execution-performance-and-preflight.md)
- Spec review: [spec-review-r1](../docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/spec-review-r1.md)
- Plan review: [plan-review-r1](../docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/plan-review-r1.md)
- Architecture/ADRs: not applicable for this slice; the approved spec and plan require architecture only if scope expands into persistent workers, shared or remote cache, cross-process protocol, or broad validator composition.

## Testing strategy

- Unit strategy: add focused selector and classifier tests in `scripts/test-select-validation.py` for selected-check identity, missing-route blockers, cache boundary metadata, and broad-smoke classification fields.
- Integration strategy: run selected CI through `bash scripts/ci.sh --mode explicit --timeout 180 --path ...` for changed scripts, specs, plan, and change-local evidence so wrapper-visible behavior, exit status, and diagnostics are covered together.
- End-to-end strategy: use milestone validation evidence for selected validation, broad-smoke baseline capture, and final verify scenario recording; do not claim branch readiness from these inner-loop proofs.
- Smoke strategy: run `python scripts/test-select-validation.py`, lifecycle validation, change metadata validation, review artifact validation, and `git diff --check` for each milestone.
- Manual strategy: manually inspect performance evidence where machine variance or expensive broad-smoke runtime prevents deterministic assertions about elapsed time.
- Contract strategy: every `MUST` requirement maps to a stable test ID or explicit manual proof, and every runtime-reduction claim requires proof-preservation evidence.
- Migration strategy: verify existing standalone commands and the existing selected-CI timeout override remain compatible; no historical timing evidence migration is required.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T1 | contract | Baseline evidence cites June 24 as upstream foundation and does not supersede it. |
| R2 | T1 | contract | Durable upstream artifact references are required in baseline evidence. |
| R3 | T2 | integration | Baseline separates selected validation, broad-smoke, and final verify scenarios. |
| R4 | T2 | manual, integration | Dominant contributors are recorded when timing output supports them; limitations are explicit. |
| R5 | T2 | contract | Fixed percentage target is rejected until baseline review. |
| R6 | T3, MP-SEL-001 | manual, integration | `selector.regression` profile exists before optimization acceptance with exact environment, commands, timing, selected-check identity, timeout behavior, and pass/fail criteria. |
| R7 | T4 | integration | Baseline and post-change selected-check identity are compared. |
| R8 | T4 | integration | Expected failing routing fixtures still fail. |
| R9 | T4 | integration | Expected passing routing fixtures still pass. |
| R10 | T4, T5 | integration | Runtime improvement alone cannot pass without identity, failure sensitivity, and diagnostics. |
| R11 | T3, T5, MP-SEL-001 | manual, contract | No-safe-reduction result records profile evidence, reason, timeout behavior, and follow-up decision. |
| R12 | T6 | integration | Known unclassified path classes produce deterministic missing-route blockers. |
| R13 | T6 | integration | Blocker output includes path, blocker ID, class when known, and corrective guidance. |
| R14 | T7 | integration | Explicit diagnostic broad-smoke does not erase selected-validation blocker. |
| R15 | T6 | integration | Required artifact/path classes need routing registration or out-of-scope rationale. |
| R16 | T8 | contract | Broad-smoke classification exists before any parallelism proposal. |
| R17 | T8 | contract | Classification records every required field. |
| R18 | T9 | integration | Classification is read-only and broad-smoke execution remains sequential. |
| R19 | T9 | integration | Broad-smoke parallel execution remains disabled in this slice. |
| R20 | T10 | integration | `cache_status` remains metadata; cache reuse and final-proof cache claims are absent. |
| R21 | T11 | contract | Broad multi-validator composition remains out of scope. |
| R22 | T11 | manual, contract | Readiness assessment is allowed only if baseline shows material repeated overhead. |
| R23 | T11 | contract | Any later composition proof starts with one validator or wrapper and preserves CLI behavior. |
| R24 | T12 | contract, manual | Final verify remains actual-run evidence against stable committed tracked state. |
| R25 | T4, T6, T9, T12 | integration, contract | Coverage, diagnostics, exit behavior, IDs, broad-smoke coverage, and rerun guidance are preserved. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T2, T3 | Baseline splits scenarios and identifies `selector.regression` or other dominant contributors when measurable. |
| E2 | T4, T5 | Selector optimization preserves identity and failure fixtures or records no-safe-reduction rationale. |
| E3 | T6, T7 | Missing selector route blocks selected validation and survives diagnostic broad-smoke. |
| E4 | T8, T9 | Broad-smoke classification is evidence only and does not change execution ordering. |
| E5 | T10, T12 | Cache status remains informational and cannot become final closeout proof. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | T3, T5 | Dominant selector runtime with no safe reduction records rationale and follow-up. |
| EC2 | T4, T5 | Faster selector run that loses a negative fixture is blocked. |
| EC3 | T6 | New generated output class without route produces missing-route blocker. |
| EC4 | T7 | Passing diagnostic broad-smoke does not convert selected validation to pass. |
| EC5 | T8 | Writing or shared-state broad-smoke child is not a parallel-safe candidate. |
| EC6 | T8 | Output-order-dependent child is not a parallel-safe candidate. |
| EC7 | T1 | PR-number-only baseline references fail evidence review. |
| EC8 | T11 | Composition readiness finding cannot authorize composition without standalone compatibility proof. |
| EC9 | T10, T12 | `cache_status` in output is not cache reuse evidence or final proof. |

## Test cases

### T1. Baseline cites durable June 24 foundation

- Covers: R1, R2, EC7
- Level: contract
- Fixture/setup: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/script-performance-baseline.yaml` plus links to the June 24 proposal, spec, plan, change ID, and timing evidence.
- Steps: Inspect the baseline evidence and assert it cites durable June 24 artifacts instead of relying only on `post-#109` or PR-number shorthand.
- Expected result: Baseline evidence is reviewable without GitHub PR archaeology and clearly treats June 24 work as upstream, not superseded.
- Failure proves: The follow-through work cannot be reviewed against stable upstream authority.
- Automation location: static assertions in `scripts/test-select-validation.py` or lifecycle/evidence validation for the baseline artifact.

### T2. Baseline distinguishes selected, broad-smoke, and final-verify scenarios

- Covers: R3, R4, R5, E1
- Level: integration
- Fixture/setup: Existing phase/timing output, June 24 timing evidence, and new change-local baseline evidence.
- Steps: Record selected validation, broad-smoke, and final verify scenarios separately; record dominant contributor when measurable; verify no fixed percentage target is introduced.
- Expected result: Evidence separates developer inner-loop cost from boundary and final-verify cost and records limitations when a contributor cannot be measured.
- Failure proves: Optimization target selection is not measurement-driven.
- Automation location: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/script-performance-baseline.yaml`; `bash scripts/ci.sh --mode explicit --timeout 180 --path ...`.

### T3. Selector-regression runtime profile exists before optimization acceptance

- Covers: R6, R11, E1, EC1
- Level: manual, integration
- Manual proof: MP-SEL-001
- Evidence artifact: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-regression-profile.md`.
- Fixture/setup: `scripts/test-select-validation.py`, timing/profiling output, and `selector-regression-profile.md`.
- Procedure: Follow `MP-SEL-001`.
- Expected result: The selector-regression profile records the measured runtime, selected checks, timeout behavior, dominant contributors or instrumentation limitations, and either a safe reduction decision or a no-safe-reduction rationale.
- Failure proves: Missing or incomplete `MP-SEL-001` evidence blocks implementation closeout because runtime changes were made before an auditable profile identified the measured bottleneck.
- Automation location: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-regression-profile.md`; `python scripts/test-select-validation.py`.

## Manual proof cases

### MP-SEL-001. Selector-regression profiling proof

- Stable proof ID: MP-SEL-001
- Covered requirements: R6, R11
- Covered test cases: T3, T5
- Owning stage: implementation milestone that changes selector-regression runtime behavior
- Owner role: implementer records evidence; code-review verifies evidence completeness
- Automation rationale:
  - Selector-regression runtime depends on machine performance, cold or warm cache behavior, Python startup/import overhead, and repository state.
  - The first slice needs a repeatable profile and preservation evidence, but it must not set a fixed runtime threshold before baseline review.
  - Therefore this proof is manual evidence with exact required steps rather than an automated pass/fail runtime budget.
- Required environment:
  - Run from repository root.
  - Use the same Python interpreter used by repository validation.
  - Record operating system, CPU class or runner name when available, Python version, and whether the run is local, CI, or containerized.
  - Record current commit or `HEAD` identity.
  - Record whether the worktree is clean or dirty and list changed files if dirty.
  - Use no network-dependent setup.
  - Use the repository-supported selected-CI timeout override when running the selected wrapper path.
- Exact profiling steps:
  1. Record the baseline selected-regression command used before optimization.
  2. Run the focused selector-regression proof command.
  3. Record total wall-clock duration.
  4. Record per-check or per-phase timing when the command output exposes it.
  5. If the command times out at the default selected-CI timeout, rerun with the documented timeout override and record both the timeout and successful run.
  6. Run a profiling command that separates selector-regression runtime from wrapper overhead when supported by the repository.
  7. Record dominant contributors when the evidence supports them.
  8. If dominant contributors cannot be determined from available instrumentation, record that limitation explicitly.
  9. Record whether a safe reduction was identified.
  10. If no safe reduction was identified, record the reason and follow-up decision.
- Minimum commands:
  ```bash
  python scripts/test-select-validation.py
  ```
  ```bash
  bash scripts/ci.sh --mode explicit --timeout 180 \
    --path scripts/validation_selection.py \
    --path scripts/test-select-validation.py
  ```
  If repository-supported profiling helpers exist, include them. If not, use a stable timing wrapper and record the exact command:
  ```bash
  /usr/bin/time -p python scripts/test-select-validation.py
  ```
- Required evidence artifact: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-regression-profile.md`
- Evidence artifact required fields:
  ```md
  ## Selector-regression profile

  - Proof ID: MP-SEL-001
  - Commit or HEAD:
  - Worktree state:
  - Environment:
  - Commands:
  - Baseline duration:
  - Timeout behavior:
  - Timeout override used:
  - Selected checks observed:
  - Dominant contributors:
  - Limitations:
  - Safe reduction identified: yes/no
  - No-safe-reduction rationale:
  - Follow-up decision:
  ```
- Pass condition:
  - Evidence artifact exists.
  - Evidence names `MP-SEL-001`.
  - Evidence records environment, commands, timing, selected checks, and timeout behavior.
  - Evidence records dominant contributors or an explicit instrumentation limitation.
  - Evidence records either a safe reduction or a no-safe-reduction rationale.
  - Evidence records a timeout or follow-up decision when applicable.
  - Reviewer can replay or understand the profiling route without asking the implementer for missing context.
- Failure condition:
  - Evidence artifact is missing.
  - Evidence omits environment, commands, timing, selected checks, or timeout behavior.
  - Evidence says profiling was performed but does not name the command.
  - Evidence claims runtime improvement without selected-check preservation.
  - Evidence claims no-safe-reduction without rationale.
  - Evidence requires reviewer inference to determine what was measured.
- Rerun condition:
  - Selector-regression implementation changes.
  - Selector selected-check identity changes.
  - Timeout behavior changes.
  - Profiling command or wrapper behavior changes.
  - Review finds the evidence incomplete.

### T4. Selector preservation proves identity and fixture sensitivity

- Covers: R7, R8, R9, R10, R25, E2, EC2
- Level: integration
- Fixture/setup: Positive and negative selector routing fixtures in `scripts/test-select-validation.py` plus `selector-preservation.md`.
- Steps: Capture baseline selected-check identity, run post-change identity comparison, assert expected-fail fixtures still fail, assert expected-pass fixtures still pass, and compare diagnostic IDs/rerun guidance.
- Expected result: Selector proof is preserved across any runtime change.
- Failure proves: Faster selector validation came from reduced coverage or weakened diagnostics.
- Automation location: `python scripts/test-select-validation.py`; `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-preservation.md`.

### T5. Unsafe selector optimization is rejected or explained

- Covers: R10, R11, EC1, EC2
- Level: integration
- Fixture/setup: A negative fixture or review evidence representing lower elapsed time with lost selected-check identity, lost failure sensitivity, or missing diagnostics.
- Steps: Assert the optimization cannot be accepted solely on elapsed time; assert no-safe-reduction evidence records profile, reason, and timeout or follow-up decision.
- Expected result: The accepted result is either preserved optimization or documented no-safe-reduction.
- Failure proves: Performance work can silently trade away proof.
- Automation location: `scripts/test-select-validation.py`; change-local selector profile and preservation evidence.

### T6. Missing selector routes block deterministically

- Covers: R12, R13, R15, R25, E3, EC3
- Level: integration
- Fixture/setup: Changed-path fixtures for lifecycle evidence classes, validator fixture classes, guide artifact classes, generated output classes, and release evidence classes.
- Steps: Run selected validation with a known path class that lacks routing; assert blocker ID, path, class when known, and corrective guidance are emitted; assert out-of-scope rationale is required when routing is intentionally absent.
- Expected result: Selected validation blocks with deterministic missing-route diagnostics.
- Failure proves: New path classes can silently fall through or be treated as clean.
- Automation location: `scripts/test-select-validation.py`; `scripts/validation_selection.py`.

### T7. Diagnostic broad-smoke cannot erase missing-route blocker

- Covers: R14, E3, EC4
- Level: integration
- Fixture/setup: Missing-route selected-validation fixture plus explicit diagnostic broad-smoke request.
- Steps: Trigger missing-route blocker, request diagnostic broad-smoke, and assert selected-validation result remains blocked even if diagnostic broad-smoke passes.
- Expected result: Diagnostic broad-smoke adds evidence but does not convert the selected result to pass.
- Failure proves: Broad-smoke can hide selector-routing incompleteness.
- Automation location: `scripts/test-select-validation.py`; `bash scripts/ci.sh --mode explicit --timeout 180 --path ...`.

### T8. Broad-smoke child classification is complete

- Covers: R16, R17, E4, EC5, EC6
- Level: contract
- Fixture/setup: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/broad-smoke-child-classification.md` and broad-smoke child inventory from `scripts/ci.sh`.
- Steps: Assert every broad-smoke child records check ID, command, read/write behavior, temporary roots, shared outputs, network use, CPU/I/O expectations, nested parallelism risk, output-order risk, failure-output dependency, candidate status, and confidence.
- Expected result: Classification is complete, and low-confidence, writing, shared-state, network-sensitive, or output-order-dependent checks are not marked as parallel-safe candidates.
- Failure proves: Later parallelism would be based on incomplete safety evidence.
- Automation location: static tests in `scripts/test-select-validation.py`; classification artifact review.

### T9. Broad-smoke remains sequential and unchanged

- Covers: R18, R19, R25, E4
- Level: integration
- Fixture/setup: Existing broad-smoke wrapper tests and new classification checks.
- Steps: Assert this slice does not add broad-smoke concurrency, does not change broad-smoke ordering, and does not change failure output aggregation; verify parallel execution remains disabled without later approved artifact.
- Expected result: Broad-smoke classification does not change broad-smoke runtime behavior.
- Failure proves: Classification accidentally became an execution change.
- Automation location: `scripts/test-select-validation.py`; `scripts/ci.sh`.

### T10. Cache status remains boundary metadata

- Covers: R20, E5, EC9
- Level: integration
- Fixture/setup: Selected-validation output containing `cache_status: not-applicable`.
- Steps: Assert `cache_status` remains informational, no cache reuse is enabled, failed or unknown cache state cannot pass, and no final proof references cache hits.
- Expected result: Cache metadata exists only as a boundary marker.
- Failure proves: The slice introduced cache behavior or final-proof cache reliance.
- Automation location: `scripts/test-select-validation.py`; selected CI output assertions.

### T11. Validator composition remains deferred

- Covers: R21, R22, R23, EC8
- Level: contract
- Fixture/setup: Baseline/profile evidence and plan/change-local follow-up notes.
- Steps: Assert no broad multi-validator in-process runner is introduced; if repeated startup/import/parsing is material, record readiness assessment only; assert any future proof-of-concept is limited to one validator or wrapper and preserves standalone CLI behavior.
- Expected result: Composition remains out of scope unless a later approved artifact authorizes it.
- Failure proves: The first slice expanded into broad composition without proof.
- Automation location: `git diff --name-only`; change-local evidence review; selected CI for unchanged standalone CLI behavior where touched.

### T12. Final verify and compatibility boundaries are preserved

- Covers: R24, R25, E5, EC9
- Level: contract
- Fixture/setup: Prior validation execution spec, current plan, selected CI output, standalone command behavior, and final verify guidance.
- Steps: Assert selected-validation speedups do not claim branch readiness, PR readiness, hosted CI success, or final closeout; assert final verify remains actual-run evidence against stable committed tracked state; assert standalone commands keep exit codes, failure detection, diagnostics, IDs, and rerun guidance.
- Expected result: Inner-loop optimization does not weaken final verify or existing command compatibility.
- Failure proves: Runtime work crossed into readiness claims or broke standalone behavior.
- Automation location: lifecycle validation, selected CI, manual final evidence review before verify.

## Milestone coverage map

| Milestone | Covered by | Notes |
| --- | --- | --- |
| M1 Baseline and Selector Regression Profile | T1, T2, T3, T10, T11, T12 | Baseline, profile, cache boundary, composition deferral, and final-verify boundary. |
| M2 Selector Preservation and Missing-Route Blockers | T4, T5, T6, T7, T10, T12 | Selector identity, failure sensitivity, missing-route diagnostics, diagnostic broad-smoke boundary, cache, and final-verify boundary. |
| M3 Broad-Smoke Child Classification | T8, T9, T10, T11, T12 | Classification completeness, sequential broad-smoke behavior, cache boundary, composition boundary, and final-verify boundary. |

## Fixtures and data

- `docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/script-performance-baseline.yaml` for upstream timing context.
- `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/script-performance-baseline.yaml` for follow-through baseline evidence.
- `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-regression-profile.md` for selector profile evidence.
- `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-preservation.md` for identity and failure-sensitivity proof.
- `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/broad-smoke-child-classification.md` for broad-smoke classification.
- Existing and new fixtures in `scripts/test-select-validation.py` for routing, selector identity, broad-smoke wrapper behavior, selected-CI output, and cache status.

## Mocking/stubbing policy

Use temporary repositories and fixture workspaces for selector and CI wrapper behavior. Stub expensive broad-smoke child commands when testing wrapper ordering, output aggregation, and classification shape. Do not stub selected-check identity comparison, missing-route classification, or final evidence files being validated. Do not use network-dependent tests.

## Migration or compatibility tests

- Existing standalone commands remain supported: `python scripts/test-select-validation.py`, selected `bash scripts/ci.sh --mode explicit --timeout 180 --path ...`, and direct lifecycle validators.
- Existing selected-CI timeout override remains available while `selector.regression` is profiled.
- Existing broad-smoke output order and failure behavior remain compatible because this slice keeps broad-smoke sequential.
- No historical timing evidence migration is required; new evidence links to historical evidence.

## Observability verification

- Baseline evidence records scenario, command, selected checks when applicable, phase duration, dominant contributor when measurable, and limitations.
- Selector-regression evidence records before/after profile shape, selected-check identity comparison, failure-sensitivity results, and diagnostics preservation.
- Missing-route diagnostics expose path, blocker ID, class when known, and corrective action.
- Broad-smoke classification records every R17 field.
- Validation output preserves exit behavior, diagnostic IDs, failure details, and rerun guidance.

## Security/privacy verification

- Evidence artifacts must not record secrets, credentials, tokens, private keys, or machine-local debug paths unless intentionally part of a reviewed fixture.
- Broad-smoke classification identifies network use when present.
- Temporary workspaces must not persist private machine paths in tracked evidence.

## Performance checks

- M1 records baseline timing before optimization.
- M2 records before/after selector profile or no-safe-reduction rationale.
- M3 records classification evidence only; it does not claim broad-smoke runtime reduction.
- Numeric percentage targets remain out of scope until baseline evidence is reviewed downstream.

## Manual QA checklist

- [ ] `MP-SEL-001` evidence artifact exists.
- [ ] Evidence records environment and repository state.
- [ ] Evidence records exact profiling commands.
- [ ] Evidence records baseline runtime and timeout behavior.
- [ ] Evidence records selected checks observed.
- [ ] Evidence records dominant contributors or instrumentation limitations.
- [ ] Evidence records safe-reduction or no-safe-reduction decision.
- [ ] Evidence links any follow-up when no safe reduction is available.
- [ ] Reviewer can replay or inspect the proof without implementation context.
- Confirm baseline evidence separates selected validation, broad-smoke, and final verify.
- Confirm selector profile evidence exists before accepting runtime changes.
- Confirm any runtime improvement includes selected-check identity and failure-sensitivity proof.
- Confirm broad-smoke classification is not worded as permission to parallelize.
- Confirm no artifact claims branch readiness, PR readiness, hosted CI success, or final closeout from inner-loop validation.

## What not to test and why

- Do not test broad-smoke parallel execution; it is explicitly out of scope for this slice.
- Do not test local, remote, or shared cache reuse; this slice only preserves cache metadata boundaries.
- Do not test broad multi-validator composition; readiness assessment is evidence-only unless a later artifact authorizes composition.
- Do not assert a fixed percentage runtime improvement; the spec forbids setting one before baseline review.
- Do not use snapshots as the only proof for diagnostics; behavior-specific assertions must cover IDs, paths, classes, and guidance.

## Uncovered gaps

None. Every R1-R25 requirement, E1-E5 example, and EC1-EC9 edge case is mapped to test or manual proof.

## Next artifacts

- test-spec-review
- implementation
- code-review
- explain-change
- verify
- pr

## Follow-on artifacts

- Test-spec-review R1: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/test-spec-review-r1.md`
- Test-spec-review R2: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/test-spec-review-r2.md`

## Readiness

Approved by `test-spec-review-r2` for implementation handoff. This test spec defines the proof surface only; it does not claim implementation, validation, branch readiness, or PR readiness.
