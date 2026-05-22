# Broad-Smoke and Fixture-Suite Output Compaction Plan

## Status

Plan lifecycle state: done
Terminal disposition: merged

## Purpose / big picture

Implement the approved broad-smoke and fixture-suite output compaction contract without changing validation behavior. The work extends the accepted script-output policy from the `scripts/test-select-validation.py` first slice to the broad-smoke orchestration layer and the first targeted direct-run producer, `scripts/test-change-metadata-validator.py`.

The change is presentation-only. Successful broad-smoke output should become aggregate and compact, failed broad-smoke output should remain actionable, direct producer success should become compact, and all selected commands, selected tests, exit codes, failure detection, generated artifacts, skills, adapters, JSON behavior, and selected-CI behavior must be preserved.

## Source artifacts

- Proposal: `docs/proposals/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md`
- Spec: `specs/script-output-optimization.md`
- Architecture: not-required; the approved spec scopes this to existing script-output and CI-wrapper behavior with no new persistence, deployment, security boundary, API, or long-lived architecture package.
- Test spec: `specs/script-output-optimization.test.md`, active after focused broad-smoke and `scripts/test-change-metadata-validator.py` amendment.
- Proposal reviews: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/proposal-review-r1.md`, `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/proposal-review-r2.md`
- Spec reviews: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/spec-review-r1.md`, `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/spec-review-r2.md`
- Review log: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-log.md`
- Review resolution: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-resolution.md`

## Context and orientation

`scripts/ci.sh` owns broad-smoke orchestration. The broad-smoke path currently runs child validation producers through a separate `run_check` helper that streams child stdout and stderr. This plan changes that wrapper path so broad-smoke captures child output by default, suppresses successful child output, emits an aggregate broad-smoke success summary, and prints captured child evidence on failure or under `--verbose`.

`scripts/test-change-metadata-validator.py` is the locked first direct-run producer unless the audit records owner approval for a replacement. The producer currently uses unittest-compatible invocation behavior, including accepted `--quiet` and `-q`. This plan preserves that quiet compatibility and does not add custom compact quiet formatting for this producer.

The first script-output slice is already complete. `scripts/test-select-validation.py` and selected-CI behavior are not implementation targets here except for regression proof or proven-compatible shared-interface adjustments if implementation makes them unavoidable.

The implementation must create durable evidence under `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/`, including an output-layer audit and behavior-preservation proof. The test spec amendment must make the wrapper-mode consistency invariant checkable, not just documented.

## Non-goals

- Do not change what any producer validates.
- Do not change broad-smoke check selection, command order, failure detection, or exit-code behavior.
- Do not change selected-CI behavior except for a proven-compatible shared helper or interface if implementation requires it.
- Do not add generated artifacts, skill output, adapter output, JSON support, persistent output logs, or new output storage.
- Do not rewrite every verbose unittest producer.
- Do not introduce a shared output helper unless broad-smoke and producer work would otherwise duplicate meaningful non-trivial formatting logic.
- Do not add custom compact quiet formatting to `scripts/test-change-metadata-validator.py`.
- Do not rely on producer-level `--quiet` to make broad-smoke output compact.
- Do not switch broad-smoke default success to per-child success lines without a later approved spec amendment.

## Requirements covered

- R36 through R38: M1.
- R39 through R50: M2 and M4.
- R51 through R52: M2.
- R53: M1 and M3.
- R54 through R59: M3.
- R60 through R60c: M1, M3, and M4.
- R61 through R62: M1, M3, and M4.
- R63: M2, M3, and M4.
- R64 through R65: M2, M3, and M4.
- AC15: M1.
- AC16 through AC22: M2 and M4.
- AC23 through AC27: M3 and M4.
- AC28 through AC30: M2, M3, and M4.
- AC31 through AC36: M1, M3, and M4.

## Current Handoff Summary

- Current milestone: M4. Preservation evidence and lifecycle closeout
- Current milestone state: closed
- Last reviewed milestone: M4. Preservation evidence and lifecycle closeout
- Review status: code-review M4 R2 completed clean-with-notes after `BSO-M4-CR1` review-resolution
- Remaining in-scope implementation milestones: none
- Next stage: done
- Final closeout readiness: complete
- Reason final closeout is or is not ready: M1, M2, M3, and M4 are closed after code-review, review-resolution is closed with no open findings, CI-maintenance cleared the local selector blocker, explain-change is refreshed, final local verify passed, and PR #85 merged on 2026-05-22.

## Milestones

### M0. Plan review and test-spec handoff

- Milestone state: review-requested
- Goal: Review this execution plan, then amend the focused test spec before implementation.
- Requirements: R36 through R65, AC15 through AC36.
- Files/components likely touched:
  - `docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md`
  - `docs/plan.md`
  - `specs/script-output-optimization.test.md` after plan-review
  - `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/`
- Dependencies:
  - Accepted proposal.
  - Approved spec.
  - Closed proposal-review and spec-review findings.
- Tests to add/update:
  - None in this milestone; test-spec creation is the next lifecycle stage after plan-review.
- Implementation steps:
  - Run `plan-review` on this plan.
  - If plan-review is approved or resolved, amend `specs/script-output-optimization.test.md`.
  - Ensure the test spec covers broad-smoke capture, aggregate success, failure evidence, verbose output, wrapper-mode consistency, command identity proof, producer compact output, producer verbose output, producer quiet compatibility, zero-test behavior, selected-CI regression, ordinary-validation guard, and no generated/artifact scope expansion.
- Validation commands:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md --path specs/script-output-optimization.md --path docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md --path docs/plan.md --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-log.md --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-resolution.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction`
  - `git diff --check --`
- Expected observable result: plan-review can evaluate sequencing, proof requirements, and remaining gates without relying on chat-only context.
- Commit message: `M0: plan broad-smoke output compaction`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Starting implementation before output-contract tests are specified.
- Rollback/recovery:
  - Keep implementation blocked and revise the plan, spec, or test spec before any code change if plan-review finds an uncovered contract gap.

### M1. Output-layer audit and baseline identity proof

- Milestone state: closed
- Goal: Record producer/orchestrator output layers and baseline identity evidence before changing wrapper or producer output.
- Requirements: R36 through R38, R49 through R50, R53, R60 through R62, AC15, AC21, AC27, AC31 through AC35.
- Files/components likely touched:
  - `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/script-output-layer-audit.md`
  - `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/behavior-preservation.md`
  - Optional durable command/test identity files under `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/` if the evidence is too large for the preservation matrix.
- Dependencies:
  - Approved plan-review.
  - Focused test-spec amendment approved for implementation use.
- Tests to add/update:
  - Baseline broad-smoke child command extraction proof with ordered command list plus SHA-256 hash.
  - Baseline `scripts/test-change-metadata-validator.py` selected test/check identifier list plus SHA-256 hash.
  - Baseline quiet compatibility proof for `--quiet` and `-q`.
  - Audit rows for selected-CI and broad-smoke as separate orchestrator paths.
- Implementation steps:
  - Inventory producers and orchestrators, including `scripts/test-select-validation.py`, `scripts/test-change-metadata-validator.py`, selected-CI, broad-smoke, and any other producer directly relevant to broad-smoke.
  - Record direct-run success shape, direct-run failure usefulness, orchestrator capture policy, high-use status, and first-slice treatment.
  - Pin a deterministic broad-smoke command-list extraction method before hashing. If extraction is not deterministic, stop and amend the test spec or implementation approach before claiming preservation.
  - Capture the baseline broad-smoke child command list and SHA-256 hash.
  - Capture the baseline producer selected test/check list and SHA-256 hash.
  - Record current `scripts/test-change-metadata-validator.py --quiet` and `-q` compatibility behavior.
- Validation commands:
  - `bash scripts/ci.sh --mode broad-smoke`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-change-metadata-validator.py --quiet`
  - `python scripts/test-change-metadata-validator.py -q`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`
  - `git diff --check -- docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction`
- Expected observable result: reviewers can compare post-change behavior against stable command/test identity proof rather than output shape or count-only evidence.
- Result: Implemented. Added `script-output-layer-audit.md`, `behavior-preservation.md`, `broad-smoke-child-commands-baseline.txt`, and `change-metadata-validator-tests-baseline.txt`. The audit identifies selected-CI and broad-smoke as separate orchestrator paths, keeps `scripts/test-change-metadata-validator.py` as the first targeted producer, records quiet compatibility, and records normalized baseline command/test identity hashes.
- Validation result: Passed after making the new change-local and plan artifacts visible to dirty-worktree diff selection with `git add -N`; the initial exact broad-smoke run failed because untracked new lifecycle artifacts were invisible to `git diff`, causing artifact-lifecycle validation to evaluate stale historical plan-index context instead of the active new plan context.
- Code-review result: clean-with-notes in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/code-review-m1-r1.md`; no review-resolution required.
- Commit message: `M1: audit broad-smoke output layers`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - A fragile command-list extraction method could make the preservation hash meaningless.
  - Baseline evidence could be captured after output changes.
- Rollback/recovery:
  - Stop implementation until deterministic extraction is available, or amend the approved test spec to define the reliable proof route.

### M2. Broad-smoke capture and wrapper-mode consistency guard

- Milestone state: closed
- Goal: Make broad-smoke capture child stdout/stderr by default, emit aggregate success, show captured output on failure or verbose, and enforce wrapper-mode consistency.
- Requirements: R39 through R52, R63 through R65, AC16 through AC22, AC28 through AC30, AC35.
- Files/components likely touched:
  - `scripts/ci.sh`
  - Existing or new repository-owned tests selected by `specs/script-output-optimization.test.md`
  - `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/behavior-preservation.md`
  - `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/script-output-layer-audit.md` if implementation changes observed wrapper policy.
- Dependencies:
  - M1 baseline command identity proof.
  - Focused test spec includes ordinary-validation coverage or an ordinary guard for wrapper output-contract tests.
- Tests to add/update:
  - Broad-smoke default success with noisy child does not stream successful child stdout or stderr.
  - Broad-smoke default success reports one aggregate `[PASS] broad-smoke` summary with count and duration.
  - Broad-smoke default failure reports child name, command, exit code or reason, duration, and captured stdout/stderr.
  - Captured failure output either preserves combined stdout/stderr ordering or labels streams clearly.
  - Broad-smoke `--verbose` emits successful child output in stable child-check order.
  - Wrapper-mode consistency guard fails for an orchestration mode that runs validation producers without capture and without a documented exception.
  - Broad-smoke command list and wrapper exit-code behavior are unchanged.
- Implementation steps:
  - Add capture behavior to broad-smoke `run_check` without changing selected child commands.
  - Preserve child stdout/stderr evidence on failure.
  - Implement aggregate broad-smoke success reporting.
  - Keep verbose output full and stable.
  - Add or wire the wrapper-mode consistency guard through ordinary validation.
  - Update behavior-preservation evidence with post-change broad-smoke command list/hash, pass/fail exit-code proof, failure-evidence proof, and verbose-output proof.
- Validation commands:
  - `bash scripts/ci.sh --mode broad-smoke`
  - `bash scripts/ci.sh --mode broad-smoke --verbose`
  - `python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --jobs 1`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`
  - `git diff --check -- scripts/ci.sh docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction`
- Expected observable result: successful broad-smoke logs are aggregate and do not include child success output, while failures and verbose runs retain full evidence.
- Result: Implemented. `scripts/ci.sh` broad-smoke `run_check` now captures combined child stdout/stderr, suppresses successful child output by default, emits one aggregate `[PASS] broad-smoke` summary, prints captured output on failure, preserves full successful child output under `--verbose`, and keeps broad-smoke command identity unchanged.
- Tests/proof added first: Added broad-smoke default-success, failure-evidence, verbose-output, and wrapper-mode consistency guard tests to `scripts/test-select-validation.py`; the focused `python scripts/test-select-validation.py --verbose -k broad_smoke` run failed before implementation and passed after implementation.
- Validation result: Passed targeted M2 validation. `bash scripts/ci.sh --mode broad-smoke` passed with one aggregate `[PASS] broad-smoke: 12 checks passed in 134s` line; `bash scripts/ci.sh --mode broad-smoke --verbose` passed with full captured child output; `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/behavior-preservation.md --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml --path docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md --path docs/plan.md --path specs/script-output-optimization.md --path specs/script-output-optimization.test.md --jobs 1` passed selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- Code-review result: changes-requested in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/code-review-m2-r1.md`; `BSO-M2-CR1` required broadening the wrapper-mode consistency guard beyond a `run_check` body check.
- Review-resolution result: Implemented for `BSO-M2-CR1`. The guard now keeps the helper-level `run_check()` capture assertion, verifies mode dispatch policy, documents the selected-CI exception with reason/spec/test references, scans `run_*` orchestration functions for direct validation producer calls outside `run_check`, allows command-array construction, and fails direct bare `"$@"` streaming outside `run_check`. Added negative fixtures for a new direct-streaming validation mode and direct bare `"$@"` streaming mode.
- Code-review recheck result: clean-with-notes in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/code-review-m2-r2.md`; M2 is closed and M3 is next.
- Commit message: `M2: capture broad-smoke child output`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Capturing output could accidentally lose stderr, change stdout/stderr ordering, or mask child exit behavior.
  - A broad wrapper edit could change selected commands.
- Rollback/recovery:
  - Revert the broad-smoke capture patch independently while keeping tests and baseline evidence, then reimplement through a smaller `run_check` change.

### M3. First producer compact default and verbose compatibility

- Milestone state: closed
- Goal: Make `scripts/test-change-metadata-validator.py` compact by default, preserve full detail under `--verbose` and `-v`, preserve unittest-compatible `--quiet` and `-q`, and record selected-test identity proof.
- Requirements: R53 through R65, AC23 through AC36.
- Files/components likely touched:
  - `scripts/test-change-metadata-validator.py`
  - Existing or new repository-owned tests selected by `specs/script-output-optimization.test.md`
  - `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/behavior-preservation.md`
  - `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/script-output-layer-audit.md` if producer observations change.
- Dependencies:
  - M1 baseline selected test/check identity proof.
  - M2 broad-smoke capture closed or explicitly deferred by plan-review-approved replan.
  - Focused test spec includes ordinary-validation coverage or an ordinary guard for producer output-contract tests.
- Tests to add/update:
  - Default success prints one `[PASS] test-change-metadata-validator` summary with nonzero passed count and duration.
  - Default success hides individual passing tests.
  - Default failure includes `[FAIL]` summary, failed test names, messages, and locations when available.
  - Default failure collapses passing detail into counts.
  - `--verbose` and `-v` preserve full pass/check detail.
  - `--quiet` and `-q` remain accepted and preserve current unittest-compatible quiet behavior.
  - Zero executed tests fail unless an explicit audit/list/dry-run mode documents zero selection as allowed.
  - Selected test/check identifier list and pass/fail exit codes remain unchanged.
- Implementation steps:
  - Add the smallest producer-local output adapter needed for compact default and verbose behavior.
  - Preserve existing `--quiet` and `-q` compatibility instead of converting those flags into unsupported usage or custom compact quiet formatting.
  - Do not rely on producer quiet mode for broad-smoke compaction.
  - Update behavior-preservation evidence with post-change selected test/check list/hash, pass/fail exit proof, verbose proof, quiet compatibility proof, and failure-evidence proof.
- Validation commands:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-change-metadata-validator.py --verbose`
  - `python scripts/test-change-metadata-validator.py -v`
  - `python scripts/test-change-metadata-validator.py --quiet`
  - `python scripts/test-change-metadata-validator.py -q`
  - `bash scripts/ci.sh --mode explicit --path scripts/test-change-metadata-validator.py --jobs 1`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`
  - `git diff --check -- scripts/test-change-metadata-validator.py docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction`
- Expected observable result: direct producer success is compact by default, verbose keeps previous detail available, quiet compatibility is preserved, and selected test/check identity is unchanged.
- Result: Implemented. `scripts/test-change-metadata-validator.py` now uses a producer-local runner with compact default success/failure output, full unittest detail under `--verbose` and `-v`, preserved unittest-compatible `--quiet` and `-q`, zero-test failure handling, and a dynamic failure fixture for output-contract proof without changing the normal selected-test identity.
- Tests/proof added first: Added subprocess output-contract tests to `scripts/test-select-validation.py` for producer default success, default failure, verbose detail, quiet compatibility, and zero selected tests. The focused `python scripts/test-select-validation.py --verbose -k change_metadata_validator` run failed before the producer runner change and passed after implementation.
- Validation result: Passed M3 validation. `python scripts/test-change-metadata-validator.py` emitted one compact `[PASS] test-change-metadata-validator: 18 passed ...` line and exited `0`; `--verbose` and `-v` preserved full unittest detail; `--quiet` and `-q` exited `0` with no stdout and normal unittest quiet summary on stderr; the dynamic failing fixture exited `1` with `[FAIL]` summary, failed test name, assertion, file location, and rerun command; zero selected tests exited `1`; post-M3 selected-test hash matched baseline `fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e`; `python scripts/test-select-validation.py` passed 82 tests; selected explicit CI over `scripts/test-change-metadata-validator.py` and `scripts/test-select-validation.py` passed selected `change_metadata.regression` and `selector.regression`.
- Code-review result: changes-requested in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/code-review-m3-r1.md`; `BSO-M3-CR1` requires the recorded producer selected-test identity extraction method to remain replayable after M3, and `BSO-M3-CR2` requires `change.yaml` to list the primary M3 producer file.
- Review-resolution result: Implemented for `BSO-M3-CR1` and `BSO-M3-CR2`. The audit and behavior-preservation evidence now use a replayable selected-test identity extraction method that registers the module in `sys.modules` before `exec_module()`, and `change.yaml` now lists `scripts/test-change-metadata-validator.py` in `changed_files`.
- Code-review recheck result: clean-with-notes in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/code-review-m3-r2.md`; M3 is closed and M4 is next.
- Commit message: `M3: compact change metadata validator output`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Replacing unittest runner behavior could skip tests or change CLI compatibility.
  - Quiet compatibility could be accidentally tightened beyond the approved spec.
- Rollback/recovery:
  - Revert producer output formatting independently from broad-smoke capture, keep the failing output-contract tests, and reimplement around the existing unittest runner semantics.

### M4. Preservation evidence and lifecycle closeout

- Milestone state: closed
- Goal: Close the implementation slice with behavior-preservation proof, selected-CI regression evidence, ordinary-validation coverage evidence, and lifecycle state synchronization.
- Requirements: R49 through R50, R62 through R65, AC21, AC27 through AC30, AC35 through AC36.
- Files/components likely touched:
  - `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/behavior-preservation.md`
  - `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/script-output-layer-audit.md`
  - `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`
  - `docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md`
  - `docs/plan.md`
- Dependencies:
  - M2 and M3 closed after code-review.
  - Any material review findings resolved and re-reviewed.
- Tests to add/update:
  - No new behavior tests unless closeout exposes a proof gap.
  - Preservation matrix rows for broad-smoke child commands, broad-smoke pass/fail exit behavior, broad-smoke failure evidence, broad-smoke verbose output, producer selected tests/checks, producer pass/fail exit behavior, producer failure evidence, producer verbose output, producer quiet compatibility, selected-CI behavior, ordinary-validation guard, and no generated/artifact scope expansion.
- Implementation steps:
  - Recompute and record broad-smoke command-list hash and producer selected-test/check hash.
  - Record selected-CI regression evidence.
  - Record that output-contract tests run in ordinary validation or that an ordinary guard fails when they fail.
  - Record no generated artifacts, skills, adapters, JSON support, validation selection logic, or validation coverage changed.
  - Synchronize `docs/plan.md`, this plan, and `change.yaml` before final closeout gates.
- Validation commands:
  - `python scripts/test-script-output.py` if present after the focused test-spec amendment, otherwise the repository-owned output-contract command named by the test spec
  - `python scripts/test-select-validation.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-change-metadata-validator.py --verbose`
  - `python scripts/test-change-metadata-validator.py --quiet`
  - `python scripts/test-change-metadata-validator.py -q`
  - `bash scripts/ci.sh --mode broad-smoke`
  - `bash scripts/ci.sh --mode broad-smoke --verbose`
  - `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-change-metadata-validator.py --path scripts/test-select-validation.py --jobs 1`
  - `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-change-metadata-validator.py --path scripts/test-select-validation.py --path specs/script-output-optimization.md --path specs/script-output-optimization.test.md --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml --path docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md --path docs/plan.md --jobs 1`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md --path specs/script-output-optimization.md --path specs/script-output-optimization.test.md --path docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md --path docs/plan.md --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-log.md --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-resolution.md`
  - `git diff --check --`
- Expected observable result: final code-review and downstream `explain-change`, `verify`, and `pr` gates have durable evidence that the output compaction is presentation-only.
- Result: Implemented. Added final post-M4 broad-smoke child-command identity evidence and producer selected-test identity evidence. Updated `behavior-preservation.md` and `script-output-layer-audit.md` with M4 final proof, selected-CI regression proof, ordinary-validation coverage proof, and out-of-scope surface proof.
- Tests/proof added first: Recomputed final identity hashes before lifecycle state handoff. `broad-smoke-child-commands-post-m4.txt` matches the M1 baseline hash `8b1e4d0d7f36fccc0b7d0e2fa3ad5efedc39f7f41f935bb117c8c9f6eda9565f`; `change-metadata-validator-tests-post-m4.txt` matches the M1 baseline hash `fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e`. The replayable producer extraction also returned count `18` and the same hash.
- Validation result: Passed M4 validation. `scripts/test-script-output.py` is absent, so M4 used the repository-owned output-contract command named by the test spec: `python scripts/test-select-validation.py`, which passed 82 tests. Direct producer default, verbose, quiet, and `-q` runs passed. Default broad-smoke passed with one aggregate `[PASS] broad-smoke: 12 checks passed ...` line; verbose broad-smoke passed and emitted captured child output. Selected explicit CI passed for wrapper/producer/selector paths and for the expanded M4 path set, selecting `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression` where applicable. Review-artifact closeout, change metadata validation, artifact lifecycle validation, and patch hygiene passed.
- Code-review result: changes-requested in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/code-review-m4-r1.md`; `BSO-M4-CR1` requires M4 lifecycle state to be synchronized across the active plan before M4 can close.
- Review-resolution result: Implemented for `BSO-M4-CR1`. The active plan Current Handoff Summary and M4 milestone body both record M4 as `resolution-needed`; `docs/plan.md`, `change.yaml`, `review-log.md`, and `review-resolution.md` are synchronized for the M4 review-resolution state. M4 is not marked closed and must return to code-review.
- Code-review recheck result: clean-with-notes in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/code-review-m4-r2.md`; M4 is closed and final closeout starts with `explain-change`.
- Commit message: `M4: close broad-smoke output evidence`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Closeout could claim behavior preservation from output appearance instead of stable command/test identity.
  - Lifecycle state could diverge between `docs/plan.md`, this plan, and `change.yaml`.
- Rollback/recovery:
  - Stop final closeout, reopen the specific milestone with the missing proof, and rerun code-review after evidence is corrected.

## Validation plan

- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction`: validate review recording and resolved findings.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`: validate change metadata.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`: validate touched lifecycle artifacts.
- `python scripts/test-select-validation.py`: preserve first-slice runner behavior and ordinary output-contract coverage.
- `python scripts/test-change-metadata-validator.py`: prove default producer behavior and selected-test coverage.
- `python scripts/test-change-metadata-validator.py --verbose`: prove producer full-detail escape hatch.
- `python scripts/test-change-metadata-validator.py --quiet`: preserve existing quiet compatibility.
- `python scripts/test-change-metadata-validator.py -q`: preserve existing quiet alias compatibility.
- `bash scripts/ci.sh --mode broad-smoke`: prove default broad-smoke aggregate success and selected child command behavior.
- `bash scripts/ci.sh --mode broad-smoke --verbose`: prove successful child output remains available under verbose mode.
- `bash scripts/ci.sh --mode explicit --path ... --jobs 1`: prove selected-CI behavior does not regress for touched paths.
- `bash scripts/ci.sh --mode explicit --path ... --jobs 1`: run selected checks for changed files.
- `git diff --check --`: catch whitespace and patch hygiene issues.

## Risks and recovery

- Risk: Broad-smoke capture hides stderr or changes stdout/stderr ordering needed for diagnosis.
  - Recovery: Use combined capture that preserves emitted order, or label separated stdout/stderr streams clearly as required by R47.
- Risk: Broad-smoke selected child commands change while output becomes shorter.
  - Recovery: Treat command-list hash drift as blocking unless the spec is amended and owner-approved.
- Risk: Producer compacting changes selected tests or unittest CLI compatibility.
  - Recovery: Treat selected-test hash drift, pass/fail exit-code drift, or `--quiet`/`-q` compatibility drift as blocking and revert producer formatting independently.
- Risk: Wrapper-mode consistency is documented but not enforced.
  - Recovery: Keep M2 open until an ordinary validation guard checks each `scripts/ci.sh` orchestration mode that runs validation producers or records an approved exception.
- Risk: Output-contract tests are added but excluded from ordinary validation.
  - Recovery: Keep the relevant milestone open until ordinary validation runs those tests or an ordinary guard fails when they fail.
- Risk: Selected-CI regresses through a shared helper or `scripts/ci.sh` change.
  - Recovery: Stop closeout, restore selected-CI behavior, and add regression proof before re-review.

## Dependencies

- Proposal is accepted.
- Spec is approved after spec-review R2.
- `review-resolution.md` is closed and `review-log.md` has no open findings.
- Plan-review must approve or resolve this plan before test-spec amendment.
- Focused test-spec amendment must exist and be approved for implementation use before code changes.
- M1 baseline evidence must precede M2 and M3 implementation changes.
- M2 broad-smoke capture should close before M3 producer formatting unless plan-review approves a replan.

## Progress

- 2026-05-22: Proposal accepted after proposal-review R2.
- 2026-05-22: Spec approved after spec-review R2, including the corrected quiet compatibility contract for `scripts/test-change-metadata-validator.py`.
- 2026-05-22: Plan created. Upstream status settlement result: not-needed; proposal and spec already carry accepted/approved statuses with durable review evidence.
- 2026-05-22: Plan-review R1 approved this plan with no material findings.
- 2026-05-22: Focused test-spec amendment added TSRO-015 through TSRO-027 for broad-smoke capture, wrapper-mode consistency, producer compaction, quiet compatibility, identity proof, ordinary-validation guard, selected-CI regression, and final smoke coverage.
- 2026-05-22: Owner approved the active focused test-spec amendment for implementation use.
- 2026-05-22: M1 implemented output-layer audit and baseline identity proof; milestone is ready for code-review.
- 2026-05-22: M1 code-review R1 completed clean-with-notes; M1 is closed and M2 is next.
- 2026-05-22: M2 implementation started.
- 2026-05-22: M2 implemented broad-smoke capture and wrapper-mode consistency tests; milestone is ready for code-review.
- 2026-05-22: M2 code-review R1 requested changes for `BSO-M2-CR1`; M2 is in review-resolution.
- 2026-05-22: M2 review-resolution implemented `BSO-M2-CR1`; milestone is ready for code-review recheck.
- 2026-05-22: M2 code-review R2 completed clean-with-notes after `BSO-M2-CR1` resolution; M2 is closed and M3 is next.
- 2026-05-22: M3 implementation started.
- 2026-05-22: M3 implemented compact default producer output and is ready for code-review.
- 2026-05-22: M3 code-review R1 requested changes for `BSO-M3-CR1` and `BSO-M3-CR2`; M3 is in review-resolution.
- 2026-05-22: M3 review-resolution implemented `BSO-M3-CR1` and `BSO-M3-CR2`; milestone is ready for code-review recheck.
- 2026-05-22: M3 code-review R2 completed clean-with-notes after `BSO-M3-CR1` and `BSO-M3-CR2` resolution; M3 is closed and M4 is next.
- 2026-05-22: M4 implemented final preservation evidence and lifecycle state synchronization; milestone is ready for code-review.
- 2026-05-22: M4 code-review R1 requested changes for `BSO-M4-CR1`; M4 is in review-resolution.
- 2026-05-22: M4 review-resolution implemented `BSO-M4-CR1`; M4 remains not closed and is ready for code-review recheck.
- 2026-05-22: M4 code-review R2 completed clean-with-notes after `BSO-M4-CR1` resolution; all implementation milestones are closed and final closeout starts with `explain-change`.
- 2026-05-22: Explain-change recorded under `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/explain-change.md`; next stage is `verify`.
- 2026-05-22: CI-maintenance fixed local/PR selector routing for the new change-local evidence files, refreshed explain-change, and reran local selected CI; next stage remains `verify`.
- 2026-05-22: Final local verify passed, including selector regression, producer default/verbose/quiet compatibility, identity hashes, local and explicit selected CI, broad-smoke default and verbose runs, review-artifact closeout, change metadata, artifact lifecycle, and patch hygiene. Next stage is `pr`.
- 2026-05-22: PR #85 opened for hosted CI and human review.
- 2026-05-22: PR #85 merged; lifecycle state updated to done.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-22 | No separate architecture artifact for this slice. | The approved spec scopes the change to existing script-output and CI-wrapper behavior with no new long-lived design boundary. | Create an architecture package for a presentation-only wrapper/producer formatting change. |
| 2026-05-22 | M1 records command/test identity baselines before output changes. | Stable hashes are required to prove presentation-only preservation. | Use output shape, counts, or post-change reconstruction as the only proof. |
| 2026-05-22 | M2 implements broad-smoke capture before M3 producer formatting. | Orchestrator capture is the structural fix for broad-smoke success noise and prevents future noisy children from flooding logs. | Start with producer formatting only. |
| 2026-05-22 | Preserve producer `--quiet` and `-q` compatibility without custom compact quiet formatting. | Spec-review found these invocations are already accepted; changing them would add compatibility risk outside the slice. | Treat quiet as unsupported or impose `test-select-validation.py` quiet semantics here. |
| 2026-05-22 | Use normalized command templates for broad-smoke command identity baseline. | The runtime adapter output directory, changed review roots, and lifecycle explicit paths are intentionally dynamic, so hashing raw runtime command output would be unstable. | Hash temp paths and dirty-worktree-specific path lists. |

## Surprises and discoveries

- `bash scripts/ci.sh --mode broad-smoke` uses tracked dirty-worktree diff paths for artifact-lifecycle scope. New untracked lifecycle artifacts must be made visible to `git diff` before the exact broad-smoke command validates the active new plan context.
- The earlier plan text named `bash scripts/ci.sh --mode selected --jobs 1`, but `selected` is not a supported `scripts/ci.sh` mode. The repository-owned selected-CI proof surface is explicit, local, PR, main, or release mode; M2 uses explicit path-scoped selected CI.
- `bash scripts/ci.sh --mode local --jobs 1` reported `manual-routing-required` for new deterministic change-local evidence files. Final CI-maintenance classified those evidence file classes as change-local lifecycle artifacts and reran local selected CI successfully.

## Validation notes

- Plan authoring validation recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`.
- Test-spec authoring validation recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`.
- M1 validation recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`.
- M2 validation recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`.
- M2 `BSO-M2-CR1` review-resolution validation recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`.
- M2 code-review R2 recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/code-review-m2-r2.md`.
- M3 validation recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`.
- M3 code-review R1 recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/code-review-m3-r1.md`; review-resolution validation is recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`.
- M3 code-review R2 recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/code-review-m3-r2.md`.
- M4 validation recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`.
- Explain-change recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/explain-change.md`.
- Final CI-maintenance selector-routing validation recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`.
- Final verify validation recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`.

## Outcome and retrospective

- PR #85 merged on 2026-05-22.

## Readiness

- See `Current Handoff Summary`.
- PR #85 merged; Done is claimed.
