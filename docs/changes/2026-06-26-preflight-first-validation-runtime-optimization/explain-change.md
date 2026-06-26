# Explain Change: Preflight-First Validation Runtime Optimization

## Summary

This change records the approved validation-runtime follow-through as a measurement and proof-preservation slice. It does not make validation faster by removing proof. It records current runtime evidence, preserves selector-regression coverage, strengthens deterministic missing-route diagnostics, and inventories broad-smoke child checks before any future parallelism decision.

The implementation touches only selector routing/diagnostic code, selector regression tests, lifecycle artifacts, and plan/change state. Broad-smoke execution remains sequential. Cache reuse, broad validator composition, final verify, branch readiness, PR readiness, and hosted CI success remain unclaimed.

## Problem

The accepted June 24 validation work added preflight-first timing and phase metadata, but the follow-on evidence showed two distinct cost profiles:

- developer inner-loop selected validation cost, especially `selector.regression`;
- boundary and PR-readiness cost, especially broad-smoke.

The approved June 26 proposal chose a narrow next slice: use the existing instrumentation, profile the selected-validation bottleneck, preserve selector behavior, make unregistered changed evidence paths block deterministically, and classify broad-smoke children before any concurrency work.

## Decision Trail

| Decision point | Decision | Source |
| --- | --- | --- |
| Relationship to prior work | Treat this as a post-implementation follow-on to the accepted June 24 preflight-first work, not a supersession. | `docs/proposals/2026-06-26-preflight-first-validation-runtime-optimization.md` |
| Main implementation target | Profile and preserve `selector.regression` before attempting runtime changes. | `specs/validation-runtime-follow-through.md` R6-R11; plan M1-M2 |
| Missing-route behavior | Keep unregistered deterministic change evidence as a selected-validation blocker and add clearer class/guidance fields. | R12-R15; plan M2 |
| Broad-smoke boundary | Produce read-only child classification evidence and keep broad-smoke execution unchanged. | R16-R19; plan M3 |
| Cache boundary | Keep `cache_status: not-applicable` as metadata only; do not enable cache reuse or final cache proof. | R20 |
| Composition boundary | Do not introduce broad in-process validator composition in this slice. | R21-R23 |
| Final verification boundary | Do not claim final verify, branch readiness, PR readiness, or CI readiness from inner-loop evidence. | R24-R25 |
| Architecture | No architecture artifact was required because no persistent worker, remote/shared cache, cross-process protocol, or broad composition framework was introduced. | active plan source artifacts |
| Milestone sequence | M1 baseline/profile, M2 selector preservation and missing-route blockers, M3 broad-smoke child classification. | `docs/plans/2026-06-26-preflight-first-validation-runtime-optimization.md` |
| Review outcome | M1, M2, M3, and final holistic code review completed with no material findings. | `reviews/code-review-r1.md` through `reviews/code-review-r4.md` |

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `scripts/validation_selection.py` | Registered `selector-regression-profile.md` as change evidence routed to `artifact_lifecycle.validate`. | M1 evidence must not appear as unregistered manual-routing debt once the selector profile is an approved evidence artifact. | R6, R20, R25; plan M1 | `test_registered_change_evidence_routes_without_manual_debt` coverage; M1 selected validation |
| `scripts/validation_selection.py` | Registered `broad-smoke-child-classification.md` under command-output change evidence routed to `artifact_lifecycle.validate`. | M3 classification is an approved change-local evidence artifact and should be lifecycle-validated rather than treated as missing selector routing. | R16-R19, R25; plan M3 | `test_registered_change_evidence_routes_without_manual_debt`; selected explicit validation including the classification artifact |
| `scripts/validation_selection.py` | Added `path_class`, `affected_class`, and selector-routing language to unregistered evidence debt diagnostics. | Missing selector routes needed deterministic, reviewable blocker details without falling through to broad-smoke as a substitute. | R12-R15; plan M2 | `test_unregistered_change_evidence_produces_registration_debt`; `test_diagnostic_broad_smoke_does_not_erase_missing_route_blocker` |
| `scripts/test-select-validation.py` | Added selector-preservation selected-check identity coverage. | Runtime work cannot be accepted if `selector.regression` coverage is reduced or selected-check identity changes silently. | R7-R10, R25; test spec T4 | `test_selector_preservation_surface_keeps_selected_check_identity`; `selector-preservation.md` |
| `scripts/test-select-validation.py` | Extended unregistered evidence tests to assert class fields and reroute guidance. | The missing-route blocker contract requires actionable diagnostics, not only a generic blocked status. | R12-R14; test spec T6 | `python scripts/test-select-validation.py -k unregistered_change_evidence` |
| `scripts/test-select-validation.py` | Added diagnostic broad-smoke coverage proving an explicit broad-smoke request does not erase the missing-route blocker. | Broad-smoke may be diagnostic evidence, but it must not convert an unclassified path into a clean selected-validation result. | R15; test spec T7 | `python scripts/test-select-validation.py -k diagnostic_broad_smoke` |
| `scripts/test-select-validation.py` | Added broad-smoke child extraction and classification parser helpers. | M3 needed static proof that the classification artifact covers the actual `run_broad_smoke` child list. | R16-R18; test spec T8 | `test_broad_smoke_child_classification_covers_ci_children` |
| `scripts/test-select-validation.py` | Added broad-smoke classification guardrails for unsafe candidate claims. | Side-effecting, shared-output, or low-confidence children must not be treated as already approved for parallel execution. | R17-R19; test spec T8-T9 | `test_broad_smoke_classification_blocks_unsafe_candidate_claims` |
| `scripts/test-select-validation.py` | Added proof that broad-smoke remains sequential and does not use `parallel_safe`, `ThreadPoolExecutor`, or backgrounded `run_check` calls in this slice. | The approved scope allowed classification only, not broad-smoke parallel execution. | R19; plan M3 non-goal | `test_broad_smoke_classification_keeps_runtime_sequential` |
| `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/script-performance-baseline.yaml` | Recorded baseline timing and timeout behavior for selected validation, selector calculation, selected wrapper, broad-smoke reference evidence, and final-verify boundary. | The proposal required measurement before choosing optimization targets or setting numeric goals. | R1-R6, R24; plan M1 | M1 profile commands and selected wrapper timeout evidence |
| `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-regression-profile.md` | Recorded `MP-SEL-001` environment, commands, timing, timeout behavior, dominant contributors, limitations, and no-safe-reduction decision. | Test-spec review required an auditable manual profile proof before implementation handoff. | R6, R11; test spec T3 and `MP-SEL-001` | `test-spec-review-r2` and `test-spec-review-r3` approved the proof map |
| `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-preservation.md` | Recorded selected-check identity, failure-sensitivity, missing-route, diagnostic broad-smoke, and no-safe-reduction evidence. | M2 needed durable proof that selected validation stayed complete while runtime reduction was not safely available. | R7-R15, R25; plan M2 | M2 targeted selector tests and full selector regression |
| `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/broad-smoke-child-classification.md` | Inventoried broad-smoke child checks with read/write behavior, temp roots, shared outputs, network use, resource expectations, ordering risk, failure-output dependency, candidate status, and confidence. | Broad-smoke is the larger wall-clock cost, but safe parallelism requires child classification first. | R16-R19; plan M3 | M3 classification tests and selected validation |
| `docs/proposals/2026-06-26-preflight-first-validation-runtime-optimization.md` | Recorded the accepted follow-on proposal and normalized status to accepted after proposal review. | Downstream spec, plan, and implementation needed a durable accepted direction. | workflow lifecycle contract | proposal-review R1 and R2 |
| `specs/validation-runtime-follow-through.md` | Defined R1-R25 for baseline evidence, selector preservation, missing-route blockers, broad-smoke classification, cache/composition boundaries, and final verify boundaries. | Implementation needed contract-level requirements before coding. | spec-review R1 | spec-review R1 approved with no material findings |
| `specs/validation-runtime-follow-through.test.md` | Mapped requirements and edge cases to T1-T12, including manual proof `MP-SEL-001`. | Test-spec review found the manual selector profile proof needed exact procedure and pass/fail criteria before implementation. | test-spec-review R1 finding `TSR1-F1` | `review-resolution.md`; test-spec-review R2 and R3 |
| `docs/plans/2026-06-26-preflight-first-validation-runtime-optimization.md` | Created and updated the living plan through M1-M3, code reviews, and current handoff. | The work needed milestone sequencing and state synchronization across lifecycle surfaces. | plan-review R1 | plan state and review records |
| `docs/plan.md` | Added the active plan entry and updated its next stage. | Repository workflow requires active planned work to be visible in the bounded plan index. | AGENTS plan file policy | artifact lifecycle validation |
| `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/*.md` | Recorded proposal, spec, plan, test-spec, milestone code reviews, and final holistic code review. | Formal reviews require durable review evidence. | AGENTS review recording rules | review artifact validation |
| `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/review-log.md` | Indexed all formal review events and finding state. | Review discovery and closeout require a durable log. | AGENTS review recording rules | review artifact validation |
| `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/review-resolution.md` | Closed `TSR1-F1` and recorded no-material review closeouts. | The material test-spec-review finding had to be resolved and re-reviewed before implementation. | AGENTS material finding rules | review artifact closeout validation |
| `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/change.yaml` | Tracked artifacts, requirements, changed files, review status, and validation evidence. | Change-local metadata keeps lifecycle evidence discoverable for final verify and PR handoff. | AGENTS baseline artifact pack | change metadata validation |

## Tests Added Or Changed

| Test ID or surface | What it proves | Why this level is appropriate |
| --- | --- | --- |
| T1-T2 | Baseline evidence exists and uses durable upstream references instead of PR shorthand. | Change-local evidence is the right proof level for runtime measurements and prior-artifact lineage. |
| T3 / `MP-SEL-001` | Selector-regression profiling evidence records environment, commands, timing, selected checks, timeout behavior, limitations, and decision. | Manual proof is appropriate because runtime depends on machine state and should not become a fixed budget before baseline review. |
| T4 | Selected-check identity remains stable for selector-preservation changes. | Unit-level selector tests catch accidental coverage removal deterministically. |
| T5 | A no-safe-reduction outcome is allowed only with profile evidence and rationale. | Evidence review is appropriate because the outcome is a measured decision, not a pure code branch. |
| T6 | Unregistered deterministic change evidence blocks with class details and next action. | Unit-level selector tests are appropriate for deterministic routing diagnostics. |
| T7 | Diagnostic broad-smoke does not erase the missing-route blocker. | Unit-level selector tests cover the important boundary without running broad-smoke. |
| T8 | Broad-smoke child classification covers every child discovered from `run_broad_smoke` and includes required fields. | Static tests are appropriate because M3 is a read-only classification slice. |
| T9 | Broad-smoke execution remains sequential and unsafe children are not approved for parallelism. | Static tests are appropriate to prove no concurrency behavior was enabled. |
| T10 | Cache remains metadata-only and no cache reuse is introduced. | Existing selected-check metadata plus scope review is sufficient for this non-goal. |
| T11 | Broad validator composition remains deferred. | Scope review is appropriate because no composition code was introduced. |
| T12 | Final verify remains separate from inner-loop validation. | Workflow and review evidence are appropriate because final verify is a downstream stage. |

## Validation Evidence Available Before Final Verify

Key validation already recorded in `change.yaml` and the active plan:

- `/usr/bin/time -p python scripts/test-select-validation.py` passed 103 tests for the M1 baseline with suite time 142.65 seconds and `time` real 135.04 seconds.
- `/usr/bin/time -p python scripts/select-validation.py --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --json` passed selected `selector.regression` calculation evidence with real time 1.18 seconds.
- `/usr/bin/time -p bash scripts/ci.sh --mode explicit --timeout 180 ...` timed out in selected wrapper execution after 180.12 seconds, as recorded in the M1 profile.
- `/usr/bin/time -p bash scripts/ci.sh --mode explicit --timeout 300 ...` passed the selected-wrapper selector-regression proof with `selector.regression` at 273.28 seconds in M1 and 142.54 seconds in M2.
- `python scripts/test-select-validation.py -k selector_preservation_surface` passed.
- `python scripts/test-select-validation.py -k unregistered_change_evidence` passed.
- `python scripts/test-select-validation.py -k diagnostic_broad_smoke` passed.
- `python scripts/test-select-validation.py -k broad_smoke_classification` passed.
- `python scripts/test-select-validation.py -k broad_smoke_child_classification` first failed before the M3 classification artifact existed, then passed after the artifact was added.
- `/usr/bin/time -p python scripts/test-select-validation.py` passed 108 tests after M3 with suite time 260.64 seconds and `time` real 248.35 seconds.
- `/usr/bin/time -p bash scripts/ci.sh --mode explicit --timeout 180 --path scripts/ci.sh --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/broad-smoke-child-classification.md` passed selected checks with `artifact_lifecycle.validate` at 0.28 seconds and `selector.regression` at 174.54 seconds.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/change.yaml` passed during each implementation milestone.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-26-preflight-first-validation-runtime-optimization` passed.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-26-preflight-first-validation-runtime-optimization` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed for the touched implementation, lifecycle, and review artifacts during each implementation milestone.
- `git diff --check -- ...` passed for touched implementation, lifecycle, plan, and spec surfaces.
- `code-review-r4` completed final holistic cross-milestone review with no material findings.

This is not final verification. The `verify` stage still owns final artifact-code-test coherence, branch state, and readiness checks.

## Review Resolution Summary

Review resolution is closed in `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/review-resolution.md`.

- Material findings resolved: 1.
- Unresolved findings: 0.
- Dispositions: `TSR1-F1` accepted and resolved.
- Later reviews: test-spec-review R2/R3 and code-review R1/R2/R3/R4 had no material findings.

`TSR1-F1` was a manual-proof adequacy defect in the test spec. The resolution added `MP-SEL-001`, linked it from R6, R11, T3, and the manual QA checklist, and required exact environment, commands, evidence artifact, pass/fail conditions, and rerun conditions for selector-regression profiling.

## Alternatives Rejected

- Optimize broad-smoke first: rejected for this slice because broad-smoke is the larger wall-clock cost but safe parallelism requires child side-effect, scratch-root, output-order, and resource classification first.
- Enable broad-smoke parallelism immediately: rejected because it could change semantics or hide failure output without child classification.
- Enable local or shared cache reuse: rejected because cache identity and final-proof boundaries need a separate proposal and test coverage.
- Compose broad validators in-process: rejected because composition can grow into a large refactor; this slice only records evidence and leaves readiness assessment to a later measured decision.
- Remove or narrow selector-regression coverage for speed: rejected because the core invariant forbids faster validation through less proof.
- Treat diagnostic broad-smoke as a replacement for selector routing: rejected because unclassified changed paths must remain visible blockers.

## Scope Control

Preserved non-goals:

- no broad-smoke parallel execution;
- no local, remote, or shared cache enablement;
- no cache hit treated as final proof;
- no broad in-process validator composition;
- no persistent validation worker;
- no final verify, branch-readiness, PR-readiness, or hosted-CI claim;
- no weakening of selected routing or broad-smoke coverage;
- no hidden failure output or changed broad-smoke ordering.

## Risks And Follow-Ups

- Runtime measurements are local and machine-dependent, so they should guide the next bottleneck decision rather than become fixed pass/fail budgets.
- `selector.regression` remains expensive; M2 records no safe reduction identified with the available profile rather than forcing an unsafe optimization.
- Broad-smoke remains the largest known wall-clock cost. The classification artifact is a prerequisite for a later broad-smoke parallelism proposal or implementation slice, not approval to parallelize now.
- Cache support remains deferred until complete input identity, malformed-cache behavior, and final-verify exclusion are specified and tested.
- Final `verify` still needs to confirm artifact-code-test coherence, lifecycle state, branch state, and readiness. PR handoff remains incomplete until after verification.

## Readiness

All in-scope implementation milestones are closed and code-reviewed. Required review-resolution is closed. This explanation records the durable rationale needed before final verification.

Next stage after this artifact is recorded: `verify`.
