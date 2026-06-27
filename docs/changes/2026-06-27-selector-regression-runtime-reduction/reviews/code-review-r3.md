# Code Review R3: M3 Runtime Result and Closeout Evidence

Review ID: code-review-r3
Stage: code-review
Round: 3
Reviewer: Codex code-review skill
Target: M3. Runtime Result and Closeout Evidence
Reviewed artifact: commit `152bd4e0`
Reviewed commit: `152bd4e0`
Review date: 2026-06-27
Recording status: recorded
Status: clean-with-notes
Review status: clean-with-notes
Material findings: none

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/code-review-r3.md
- Open blockers: none
- Next stage: final closeout
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/code-review-r3.md
- Review log: docs/changes/2026-06-27-selector-regression-runtime-reduction/review-log.md
- Review resolution: docs/changes/2026-06-27-selector-regression-runtime-reduction/review-resolution.md#code-review-r3
- Reviewed milestone: M3. Runtime Result and Closeout Evidence
- Milestone closeout: closed
- Remaining implementation milestones: none
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: commit `152bd4e0`
- Cumulative implementation surface: commits `68913fbe`, `158994be`, and `152bd4e0`
- Governing spec: `specs/selector-regression-runtime-reduction.md`
- Test spec: `specs/selector-regression-runtime-reduction.test.md`
- Active plan: `docs/plans/2026-06-27-selector-regression-runtime-reduction.md`
- M3 evidence: `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-result.yaml`, `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md`, and `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-profile.md`
- Relevant implementation files: `scripts/ci.sh`, `scripts/test-select-validation.py`
- Validation evidence inspected: M3 validation notes in the active plan and change metadata, runtime-result YAML, preservation evidence, actual diff, and tracked commit history.

## Diff Summary

M3 records revised selector-regression runtime evidence with three passing same-environment runs. The result records a baseline median of `164.73s`, a revised median of `36.23s`, a `78.01%` median reduction, 111 revised tests, selected-check identity `artifact_lifecycle.validate` plus `selector.regression`, and selected-CI execution under the default timeout without the prior override.

During revised timing, the default selector-regression command exposed a negative broad-smoke elapsed output. The implementation replaces Bash `$SECONDS` duration math in `scripts/ci.sh` with explicit epoch-second helpers that clamp negative elapsed values to zero, and adds `test_ci_wrapper_duration_reporting_does_not_use_bash_seconds` plus targeted broad-smoke output checks. Preservation evidence records the approved test-structure delta and keeps final verify, branch readiness, PR readiness, hosted CI, cache, worker, broad validator composition, and broad-smoke parallelism out of scope.

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | M3 satisfies `R5`-`R7`, `R21`, and `R24`-`R27` by recording revised runtime, median comparison, timeout behavior, limitations, and preservation result. It respects `R18`, `R19`, and `R28` by not enabling broad-smoke parallelism, caching, workers, composition, final verify, branch-readiness, PR-readiness, or hosted-CI claims. |
| Test coverage | pass | The new duration regression guard covers the `$SECONDS` failure mode exposed during timing, and targeted broad-smoke success, verbose, and failure-output tests passed after the fix. Full revised `python scripts/test-select-validation.py` evidence passed three times with 111 tests. |
| Edge cases | pass | EC4 is handled by same-environment median evidence with local WSL2 limitations recorded. EC6 remains covered by broad-smoke classification tests. EC8 is recorded through selected-CI execution without the timeout override. EC10 remains covered by retained wrapper and broad-smoke diagnostic output tests. |
| Error handling | pass | `elapsed_seconds_since` clamps negative elapsed values to `0`, preserving diagnostic output instead of emitting impossible negative durations when shell timing state is unreliable. Existing command failure output still includes label, exit code, command, captured output, and rerun text. |
| Architecture boundaries | pass | The diff does not add persistent workers, validation-result caching, remote/shared caches, broad validator composition, new cross-process protocols, or broad-smoke parallel execution. |
| Compatibility | pass | The default selector-regression command remains `python scripts/test-select-validation.py`. Selected-CI explicit mode passed both without a timeout override and with `--timeout 300`, selecting `artifact_lifecycle.validate` and `selector.regression`. |
| Security/privacy | pass | Runtime and preservation evidence record local environment and command data needed for reproducibility; no secrets, credentials, tokens, or private keys are introduced. |
| Derived artifact currency | pass | Plan body, plan index, change metadata, runtime result, preservation evidence, and profile evidence were synchronized for M3 review-requested state before this review. |
| Unrelated changes | pass | The functional diff is limited to duration diagnostics needed for the selector-regression command to pass reliably during M3 runtime evidence, plus M3 evidence and lifecycle bookkeeping. |
| Validation evidence | pass | M3 validation evidence includes targeted duration and broad-smoke tests, three full revised timing runs, selected-CI explicit proof with and without timeout override, focused selector validation, review artifact validation, change metadata validation, artifact lifecycle validation, and diff hygiene. |

## No-Finding Rationale

The reviewed M3 diff closes the runtime-evidence milestone without reducing selector-regression coverage. The revised default command has more tests than baseline, selected-check identity is preserved for the touched M3 path set, and the runtime result attributes improvement to the M2 duplicate preflight reduction rather than deleted proof. The additional duration fix is justified by a real default-command failure discovered during M3 timing and is covered by direct regression tests.

## Residual Risks

Runtime evidence remains local WSL2 evidence and is not hosted CI proof. The duration helper uses second-resolution wall-clock time and clamps negative elapsed values; that is sufficient for current wrapper diagnostics, but it is not a monotonic high-resolution timer. This review does not claim final verification, branch readiness, PR readiness, hosted CI success, or PR handoff readiness.

## Handoff

M3 is closed after clean code review, and no in-scope implementation milestones remain. Because this is a direct isolated `code-review` invocation, this review records the handoff only; it does not automatically start final closeout. The next lifecycle stage is `explain-change`, followed later by `verify` and PR handoff when those stages are explicitly run.
