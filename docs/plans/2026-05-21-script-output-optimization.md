# Script Output Optimization

- Status: active
- Owner: maintainer
- Start date: 2026-05-21
- Last updated: 2026-05-21
- Related proposal: `docs/proposals/2026-05-21-script-output-optimization.md`
- Related spec: `specs/script-output-optimization.md`
- Related architecture: `docs/architecture/system/architecture.md`
- Supersedes: none

## Purpose / big picture

This plan sequences the approved script-output optimization contract into reviewable implementation slices. The work makes `scripts/test-select-validation.py` quiet and count-bearing on success, specific on failure, explicit about `--verbose` and `--quiet`, and backed by behavior-preservation evidence.

The change is presentation-only. It must not change selected checks, validation behavior, failure detection, or exit-code semantics except for the approved zero-test safety boundary.

## Source artifacts

- Proposal: `docs/proposals/2026-05-21-script-output-optimization.md`
- Spec: `specs/script-output-optimization.md`
- Architecture: `docs/architecture/system/architecture.md`
- Test spec: `specs/script-output-optimization.test.md`
- Proposal reviews: `docs/changes/2026-05-21-script-output-optimization/reviews/proposal-review-r1.md`, `docs/changes/2026-05-21-script-output-optimization/reviews/proposal-review-r2.md`
- Spec reviews: `docs/changes/2026-05-21-script-output-optimization/reviews/spec-review-r1.md`, `docs/changes/2026-05-21-script-output-optimization/reviews/spec-review-r2.md`
- Architecture review: `docs/changes/2026-05-21-script-output-optimization/reviews/architecture-review-r1.md`
- Review log: `docs/changes/2026-05-21-script-output-optimization/review-log.md`
- Review resolution: `docs/changes/2026-05-21-script-output-optimization/review-resolution.md`

## Context and orientation

`scripts/test-select-validation.py` is both the first-slice target and a repository-owned regression test runner for validation selection and CI wrapper behavior. It currently emits detailed passing output that this change must preserve behind `--verbose`.

`scripts/ci.sh` is already governed by `specs/test-and-ci-speed-optimization.md`: it hides successful child-check output by default, exposes it with wrapper `--verbose`, and surfaces failed child output with stable check identity. This plan treats `scripts/ci.sh` as conditional. It is touched only if the audit or runner change proves a minimal wrapper adjustment is needed to preserve the approved quiet-success and loud-failure contract.

The implementation must create durable first-slice evidence under `docs/changes/2026-05-21-script-output-optimization/`, including the script-output audit and a behavior-preservation matrix. No generated adapter output, public skill file, workflow spec, selector logic, or broad CI-log standardization belongs in this slice.

## Non-goals

- Do not change what any script validates.
- Do not change selected-check logic, validation-selection logic, or failure detection.
- Do not remove required validation or repair evidence.
- Do not add new JSON support.
- Do not introduce a common script-output helper library.
- Do not rewrite all repository scripts.
- Do not hand-edit generated adapter output or public skill files.
- Do not broaden `scripts/ci.sh` beyond the minimal wrapper boundary allowed by the spec.

## Requirements covered

- R1 through R8: M2, M3
- R9 through R15d: M2, M3
- R16 through R18: M2, M3
- R19 through R22: M2, M3
- R23 through R24: M1, M2, M3
- R25 through R26: M1
- R27: M2, M3
- R28 through R31: M1, M4 when triggered
- R32 through R34: M1, M3, M4 when triggered, M5
- R35: M2, M3, M4 when triggered
- AC1 through AC11: M1 through M3 and M5
- AC12 through AC13: M1 and M4 when triggered
- AC14: all milestones

## Current Handoff Summary

- Current milestone: Final closeout
- Current milestone state: pr-open-hosted-ci-pending
- Last reviewed milestone: M5. Lifecycle evidence and closeout handoff
- Review status: `code-review-ci-routing-r1` closed the selector-routing maintenance fix with no material findings
- Remaining in-scope implementation milestones: none
- Next stage: hosted CI and human review on PR #83
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: all implementation milestones are closed, review-resolution is closed, explain-change is current, final local verify passed, and PR #83 is open; hosted CI and human review remain pending.

## Milestones

### M0. Plan review and test-spec handoff

- Milestone state: closed
- Goal: Review this execution plan, then create the focused test spec required before implementation.
- Requirements: proposal proof route, R35, AC1 through AC14
- Files/components likely touched:
  - `docs/plans/2026-05-21-script-output-optimization.md`
  - `docs/plan.md`
  - `specs/script-output-optimization.test.md` after plan-review
  - `docs/changes/2026-05-21-script-output-optimization/`
- Dependencies:
  - Accepted proposal.
  - Approved spec.
  - Approved architecture review.
- Tests to add/update:
  - None in this milestone; test-spec creation is the next lifecycle stage after plan-review.
- Implementation steps:
  - Run plan-review on this plan.
  - If plan-review is clean or resolved, create `specs/script-output-optimization.test.md`.
  - Keep test-spec focused on output shape, flag boundaries, zero-test safety, rerun behavior, JSON deferral, behavior preservation, and conditional CI wrapper behavior.
- Validation commands:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-script-output-optimization.md --path specs/script-output-optimization.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization`
  - `git diff --check --`
- Expected observable result: plan-review has enough self-contained context to approve or challenge sequencing, and test-spec has a clear downstream boundary.
- Commit message: `M0: plan script output optimization`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Starting implementation before the focused test spec exists.
- Rollback/recovery:
  - Keep implementation blocked and revise the plan or spec before test-spec if plan-review finds an uncovered contract gap.

### M1. Audit and baseline preservation evidence

- Milestone state: closed
- Goal: Record the first-slice audit and baseline behavior evidence before changing runner output.
- Requirements: R23, R24, R25, R26, R28 through R34, AC9 through AC14
- Files/components likely touched:
  - `docs/changes/2026-05-21-script-output-optimization/script-output-audit.md`
  - `docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md`
  - `scripts/test-select-validation.py` only for tests if the approved test spec calls for baseline fixtures in the runner itself
- Dependencies:
  - Approved plan-review.
  - Approved focused test spec.
- Tests to add/update:
  - Baseline proof entries for pass exit code, failure exit code, selected tests/checks, failure detection, failure evidence, verbose-equivalent full pass output, quiet failure behavior once implemented, and CI semantics if `scripts/ci.sh` is later touched.
  - Audit entries for `scripts/test-select-validation.py`, `scripts/ci.sh`, and any candidate script inspected only to justify non-inclusion.
- Implementation steps:
  - Create the script-output audit with the fields required by R26.
  - Capture the current default output shape, current success-line count, failure usefulness, and first-slice treatment.
  - Record whether `scripts/ci.sh` already satisfies the wrapper portion after the runner change, or why M4 remains conditionally needed.
  - Record current JSON support status for touched scripts so the first slice can prove JSON deferral or preservation.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/ci.sh --verbose`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml`
  - `git diff --check -- docs/changes/2026-05-21-script-output-optimization`
- Expected observable result: the audit identifies `scripts/test-select-validation.py` as the implementation target, records conditional `scripts/ci.sh` treatment, and preserves a baseline against which presentation-only behavior can be reviewed.
- Result: Implemented. Added `script-output-audit.md` and `behavior-preservation.md` with baseline runner, JSON, failure, and wrapper evidence. No production code changed in M1.
- Review result: `code-review-m1-r1` requested changes for `SRO-M1-CR1`; selected tests/checks baseline proof is count-only and must be made durable before M1 closes.
- Resolution result: Added `selected-tests-baseline.txt`, recorded the selected-set hash in `behavior-preservation.md`, and updated the selected tests/checks row to reference the durable list and hash. No production code changed.
- Re-review result: `code-review-m1-r2` clean-with-notes; M1 closed.
- Commit message: `M1: audit script output baseline`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Baseline evidence could accidentally rely on the noisy output after it is changed.
- Rollback/recovery:
  - Recreate baseline evidence from the prior commit or stop implementation until the missing proof is reconstructed.

### M2. Output contract tests

- Milestone state: closed
- Goal: Add focused output-shape and preservation tests before changing the runner implementation.
- Requirements: R1 through R24, R27, R32 through R35, AC1 through AC11
- Files/components likely touched:
  - `scripts/test-select-validation.py`
  - `specs/script-output-optimization.test.md`
  - `docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md`
- Dependencies:
  - M1 audit and baseline evidence.
  - Approved focused test spec.
- Tests to add/update:
  - Default success: one `[PASS]` line with suite name, nonzero count, and duration; no individual passing checks.
  - Default failure: `[FAIL]` summary plus failed names, messages, locations when available, and collapsed passing detail.
  - `--verbose` / `-v`: full pass/check detail remains available.
  - `--quiet` / `-q`: success writes no stdout or stderr; failure still emits actionable diagnostics.
  - `--verbose --quiet`: nonzero usage error before test selection or execution, stderr names both flags, stdout empty, no summaries.
  - Zero executed tests: failure unless an explicit mode permits zero selection.
  - Rerun command: emitted only for reliable exact filters; omitted or broadened when reliability cannot be proven.
  - JSON: no new `--json`; existing JSON preserved only if present.
- Implementation steps:
  - Add failing tests or fixtures in the smallest local harness that can prove the approved contract.
  - Ensure tests can detect accidental changes to selected tests/checks and exit codes, not only output text.
  - Keep assertions stable around status words, counts, names, and failure fields while avoiding brittle exact duration values.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/script-output-optimization.md --path specs/script-output-optimization.test.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml`
  - `git diff --check -- scripts/test-select-validation.py specs/script-output-optimization.test.md docs/changes/2026-05-21-script-output-optimization docs/plans/2026-05-21-script-output-optimization.md docs/plan.md`
- Expected observable result: tests fail for the old noisy default output and pass only when the approved output contract and preservation checks are satisfied.
- Result: Implemented. Added `ScriptOutputContractTests` and `ScriptOutputFixtureTests` in `scripts/test-select-validation.py`. Required formatter contract cases are excluded from ordinary M2 validation and run as explicit pre-M3 red-test proof through `python scripts/test-select-validation.py ScriptOutputContractTests`. JSON deferral, verbose compatibility, and unreliable-rerun guard tests pass now.
- Review result: `code-review-m2-r1` requested changes for `SRO-M2-CR1`; expected-failure decorators mask required output-contract failures in normal validation.
- Resolution result: Removed expected-failure masking, split ordinary validation from explicit red-test proof, added a default guard against expected-failure masking, and recorded `output-contract-red-test.md`.
- Re-review result: `code-review-m2-r2` closed M2 with no material findings.
- Aligned surface note: `behavior-preservation.md` records the intentional M2 test-suite extension and preserves the M1 selected-test baseline for M3 comparison.
- Commit message: `M2: add script output contract tests`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Tests could overfit exact formatting and make harmless duration or message changes hard to maintain.
- Rollback/recovery:
  - Narrow assertions to spec-owned fields and preserve explicit behavior checks for selection, exit code, and failure evidence.

### M3. Test-select-validation output shaping

- Milestone state: closed
- Goal: Implement the approved default, verbose, quiet, conflict-flag, zero-test, rerun, and JSON-deferral behavior in `scripts/test-select-validation.py`.
- Requirements: R1 through R24, R27, R32 through R35, AC1 through AC11, AC14
- Files/components likely touched:
  - `scripts/test-select-validation.py`
  - `docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md`
  - `docs/changes/2026-05-21-script-output-optimization/script-output-audit.md`
  - `docs/plans/2026-05-21-script-output-optimization.md`
- Dependencies:
  - M2 output contract tests.
- Tests to add/update:
  - Update or add implementation-adjacent tests as needed to make M2 tests pass without weakening them.
- Implementation steps:
  - Add argument parsing for `--verbose` / `-v` and `--quiet` / `-q`.
  - Reject combined `--verbose --quiet` before test selection or execution.
  - Capture test results and duration without changing the selected test set.
  - Print one `[PASS]` summary line in default success mode.
  - Print `[FAIL]` summary plus failure details in default and quiet failure modes.
  - Print no stdout or stderr for quiet success.
  - Keep full pass/check listing available through verbose mode.
  - Fail zero executed tests unless an explicit allowed mode exists.
  - Generate scoped rerun commands only when the script can prove a reliable exact filter and safe quoting; otherwise omit or print a safe broader command.
  - Preserve JSON absence or existing JSON behavior.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/test-select-validation.py --verbose`
  - `python scripts/test-select-validation.py --quiet`
  - `python scripts/test-select-validation.py --verbose --quiet`
  - `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --jobs 1 --verbose`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml`
  - `git diff --check --`
- Expected observable result: local default runner success is one `[PASS]` line, verbose exposes the previous full pass detail, quiet success is silent, failures remain actionable, and behavior-preservation evidence proves selection and exit-code semantics are unchanged.
- Result: Implemented. Added a script-local unittest runner adapter that parses `--verbose` / `-v`, `--quiet` / `-q`, `-k`, and explicit test names, rejects conflicting output flags before loading tests, captures result and duration for compact default/quiet output, preserves full unittest pass-list output under verbose mode, fails zero-test runs, omits scoped rerun commands for unreliable loader failures, and keeps `--json` unsupported.
- Evidence updates: `behavior-preservation.md` now records M3 new proof for `scripts/test-select-validation.py`; `script-output-audit.md` records post-change observations; `output-contract-red-test.md` records the red-test command passing after M3.
- Aligned surface note: `scripts/ci.sh` remains untouched in M3. M4 still owns the conditional wrapper no-code/patch decision.
- Review result: `code-review-m3-r1` requested changes for `SRO-M3-CR1`; the required output-contract tests still run only through an explicit command and are excluded from ordinary post-M3 validation.
- Resolution result: Removed the `load_tests` exclusion so `ScriptOutputContractTests` run in ordinary validation. `python scripts/test-select-validation.py` now runs `73` tests, including all `10` output-contract acceptance tests. The explicit output-contract command remains a focused diagnostic rerun.
- Re-review result: `code-review-m3-r2` closed M3 with no material findings.
- Commit message: `M3: shape test-select-validation output`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Replacing runner mechanics could accidentally skip tests or change failure detection.
  - Quiet mode could accidentally hide usage or failure diagnostics.
- Rollback/recovery:
  - Revert the formatter and flag parsing while keeping tests as the contract, then reimplement through a smaller result-reporting adapter around the existing runner logic.

### M4. Conditional CI wrapper preservation

- Milestone state: closed
- Goal: Make no `scripts/ci.sh` change unless M1 or M3 proves the wrapper must be adjusted to preserve quiet-success and loud-failure behavior.
- Requirements: R28 through R31, R32 through R35 when wrapper is touched, AC12 through AC14
- Files/components likely touched:
  - `scripts/ci.sh` only if triggered
  - `scripts/test-select-validation.py` for wrapper tests if triggered
  - `docs/changes/2026-05-21-script-output-optimization/script-output-audit.md`
  - `docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md`
- Dependencies:
  - M1 audit result.
  - M3 runner output behavior.
- Tests to add/update:
  - If untouched: record no-change evidence showing existing wrapper success hiding, wrapper `--verbose`, failed child output, stable check status, and selected-check semantics remain correct.
  - If touched: tests proving successful child output remains hidden by default, exposed with wrapper `--verbose`, and failed child output includes check ID, status, exit reason, elapsed runtime, and command information.
- Implementation steps:
  - Evaluate post-M3 wrapper behavior through selected explicit paths.
  - If no wrapper gap exists, record M4 as no-code closed with evidence.
  - If a wrapper gap exists, make the smallest `scripts/ci.sh` patch and preserve existing wrapper modes, selected-check coverage, and child-process exit behavior.
- Validation commands:
  - `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/ci.sh --jobs 1`
  - `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/ci.sh --jobs 1 --verbose`
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml`
  - `git diff --check --`
- Expected observable result: CI wrapper behavior is either unchanged with recorded proof or minimally patched with tests that preserve selected-check execution semantics and failure evidence.
- Result: Implemented as a no-code milestone. Post-M3 wrapper proof shows `scripts/ci.sh` still hides successful child output by default, exposes successful child output with wrapper `--verbose`, preserves `selector.regression` selected-check semantics, and has existing focused regression coverage for failed child output expansion. No wrapper patch was triggered.
- Review result: `code-review-m4-r1` closed M4 with no material findings.
- Commit message: `M4: preserve CI wrapper output boundary`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Conditional wrapper work could expand into broad CI log standardization.
- Rollback/recovery:
  - Revert wrapper edits first and keep runner-local output improvements if they still satisfy the spec.

### M5. Lifecycle evidence and closeout handoff

- Milestone state: closed
- Goal: Complete behavior-preservation evidence, lifecycle state, and final handoff surfaces after all in-scope implementation milestones are reviewed.
- Requirements: R25 through R35, AC10 through AC14
- Files/components likely touched:
  - `docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md`
  - `docs/changes/2026-05-21-script-output-optimization/explain-change.md` in the later explain-change stage
  - `docs/changes/2026-05-21-script-output-optimization/change.yaml`
  - `docs/plans/2026-05-21-script-output-optimization.md`
  - `docs/plan.md`
- Dependencies:
  - M1 through M4 closed or M4 explicitly closed as not-triggered.
  - Required code-review and review-resolution closeout.
- Tests to add/update:
  - None unless review finds a gap. This milestone records and validates final evidence rather than adding new runtime behavior.
- Implementation steps:
  - Update the behavior-preservation matrix for every touched script.
  - Update `change.yaml` artifacts, validation, changed files, and review status.
  - Run selected validation through `scripts/ci.sh`.
  - Keep this plan and `docs/plan.md` synchronized before final closeout.
  - Hand off to `explain-change`, then `verify`, then `pr` only after implementation milestones and reviews are closed.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/ci.sh --path specs/script-output-optimization.md --path specs/script-output-optimization.test.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/changes/2026-05-21-script-output-optimization/script-output-audit.md --path docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-script-output-optimization.md --path specs/script-output-optimization.md --path specs/script-output-optimization.test.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md`
  - `git diff --check --`
- Expected observable result: all in-scope milestones are closed, behavior preservation is durable, lifecycle artifacts are synchronized, and the change is ready for explain-change rather than final verification or PR yet.
- Result: Implemented. Added final preservation and scope proof to `behavior-preservation.md`, synchronized change metadata and lifecycle handoff state, and kept `explain-change` for the next downstream stage rather than creating it early.
- Review result: `code-review-m5-r1` closed M5 with no material findings.
- Commit message: `M5: close script output evidence`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Plan/index state could drift from implementation reality.
- Rollback/recovery:
  - Update the plan and change metadata to the last reviewed milestone state before any downstream handoff.

## Validation plan

- `python scripts/test-select-validation.py`: primary regression suite and output-contract proof surface.
- `python scripts/test-select-validation.py --verbose`: proves full pass/check detail remains available after default output is compacted.
- `python scripts/test-select-validation.py --quiet`: proves quiet success emits no stdout or stderr.
- `python scripts/test-select-validation.py --verbose --quiet`: proves conflicting output flags fail before test selection or execution.
- `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/ci.sh --jobs 1`: proves selected wrapper behavior around the touched runner and conditional wrapper boundary.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml`: validates change metadata after each lifecycle update.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization`: validates review evidence and finding closeout.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`: validates touched lifecycle artifacts without relying on unrelated dirty worktree state.
- `git diff --check --`: catches whitespace and patch hygiene issues.

## Risks and recovery

- Risk: output tests pass while selected tests or failure detection changed.
  - Recovery: require behavior-preservation matrix evidence for selected tests/checks, exit codes, failure detection, and failure evidence before code-review closeout.
- Risk: quiet mode hides failure reasons or usage diagnostics.
  - Recovery: keep quiet-success silence scoped only to successful outcomes; tests must cover quiet failure and conflicting-flag diagnostics.
- Risk: a scoped rerun command is misleading.
  - Recovery: omit scoped rerun or print only a safe broader command unless exact filter and safe quoting are proven.
- Risk: `scripts/ci.sh` work expands beyond the first-slice boundary.
  - Recovery: close M4 as no-code when wrapper proof is sufficient; if a patch is needed, make the smallest wrapper preservation edit and reject broad log-standardization changes.
- Risk: the implementation adds JSON or helper-library work because the formatter logic repeats.
  - Recovery: keep JSON and helper extraction deferred follow-ons unless a later approved artifact expands scope.

## Dependencies

- Plan-review must approve this plan before test-spec.
- Focused test spec must be approved before implementation.
- M1 baseline evidence must exist before M3 changes runner presentation.
- M4 is conditional and depends on the M1 audit plus M3 post-change wrapper proof.
- Code-review must close each implemented milestone before moving to the next milestone or final closeout.

## Progress

- 2026-05-21: accepted proposal recorded and proposal-review material findings resolved.
- 2026-05-21: approved spec recorded after resolving quiet-mode and conflicting-flag ambiguities.
- 2026-05-21: canonical architecture update reviewed and approved with no material findings.
- 2026-05-21: execution plan created; no implementation started.
- 2026-05-21: plan-review-r1 approved the plan with no material findings.
- 2026-05-21: active test spec created at `specs/script-output-optimization.test.md` and user-approved for implementation use; implementation is ready to start at M1.
- 2026-05-21: M1 implemented by adding the script-output audit and baseline behavior-preservation matrix; no production code changed.
- 2026-05-21: M1 code-review found `SRO-M1-CR1`; behavior-preservation selected tests/checks proof is count-only and needs resolution before M1 can close.
- 2026-05-21: `SRO-M1-CR1` resolved by adding `selected-tests-baseline.txt` with 62 ordered unittest identifiers and selected-set hash `sha256:af470dd836f5b1b44c702be35206934f77621a1477d88cafae923e50a7f492bd`; M1 is ready for code-review rerun.
- 2026-05-21: `code-review-m1-r2` closed M1 cleanly with no material findings; M2 is the next implementation milestone.
- 2026-05-21: M2 implemented output-contract tests in `scripts/test-select-validation.py`; 7 formatter-dependent cases are expected failures until M3 implements output shaping.
- 2026-05-21: M2 code-review found `SRO-M2-CR1`; expected-failure decorators mask required output-contract failures and need resolution before M2 can close.
- 2026-05-21: `SRO-M2-CR1` resolved by removing expected-failure masking, adding explicit red-test proof at `output-contract-red-test.md`, and keeping ordinary M2 validation separate from the pre-M3 red-test command.
- 2026-05-21: `code-review-m2-r2` closed M2 cleanly with no material findings; M3 is the next implementation milestone.
- 2026-05-21: M3 implemented `scripts/test-select-validation.py` output shaping and moved to code-review.
- 2026-05-21: M3 code-review found `SRO-M3-CR1`; output-contract tests must become part of ordinary post-M3 validation or an equivalent default-suite guard before M3 can close.
- 2026-05-21: `SRO-M3-CR1` resolved by removing the `load_tests` exclusion and recording the updated ordinary selected-test list/hash.
- 2026-05-21: `code-review-m3-r2` closed M3 cleanly with no material findings; M4 conditional CI wrapper preservation is the next implementation milestone.
- 2026-05-21: M4 recorded no-code wrapper-preservation evidence; `scripts/ci.sh` remains unchanged and M4 is ready for code-review.
- 2026-05-21: `code-review-m4-r1` closed M4 cleanly with no material findings; M5 lifecycle evidence and closeout handoff is the next implementation milestone.
- 2026-05-21: M5 recorded final behavior-preservation and scope-boundary evidence and is ready for code-review.
- 2026-05-21: `code-review-m5-r1` closed M5 cleanly with no material findings; explain-change is the next stage.
- 2026-05-21: Explain-change recorded the decision trail, diff rationale, tests, validation evidence, review-resolution summary, scope controls, risks, and verify handoff.
- 2026-05-21: Verify found PR-mode CI blocked by four change-local evidence files classified as `change-local-unsupported`; a narrow selector-routing maintenance fix routed those files to `artifact_lifecycle.validate`.
- 2026-05-21: `code-review-ci-routing-r1` closed the selector-routing maintenance fix cleanly with no material findings; explain-change needs refresh before final verify.
- 2026-05-21: Explain-change refreshed the durable rationale to include the selector-routing maintenance fix and its clean review.
- 2026-05-21: Final local verify passed; branch-ready evidence is recorded and the next stage is PR handoff.
- 2026-05-21: PR #83 opened for hosted CI and human review.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-21 | Sequence audit and baseline preservation before runner changes. | The change is presentation-only, so baseline evidence is needed to prove selection, failure detection, and exit codes are unchanged. | Change runner output first and reconstruct proof later. |
| 2026-05-21 | Keep `scripts/ci.sh` as conditional M4. | The approved spec allows wrapper edits only when audit or runner behavior proves they are needed. | Include broad wrapper rewrite in the first implementation milestone. |
| 2026-05-21 | Require test-spec before implementation. | The approved proposal and spec introduce observable output modes that need concrete tests before code changes. | Let implementation define test shape opportunistically. |

## Surprises and discoveries

- Existing architecture records `scripts/ci.sh` as already summary-first and failure-focused, with successful check output available through wrapper `--verbose`.
- The change root already contains formal review records, so `change.yaml` is part of the required non-trivial change-local evidence pack.

## Validation notes

- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed after plan authoring: 5 reviews, 7 findings, 5 log entries, 7 resolution entries.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-script-output-optimization.md --path specs/script-output-optimization.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md` passed after plan authoring: 3 artifact files validated.
- `git diff --check --` passed after plan authoring.
- `python scripts/select-validation.py --mode explicit ...` selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate` with no unclassified paths.
- `bash scripts/ci.sh --mode explicit ... --jobs 1` passed the selected checks: `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed after test-spec authoring.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-script-output-optimization.md --path specs/script-output-optimization.md --path specs/script-output-optimization.test.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/changes/2026-05-21-script-output-optimization/reviews/plan-review-r1.md` passed after test-spec authoring: 4 artifact files validated.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed after test-spec authoring: 6 reviews, 7 findings, 6 log entries, 7 resolution entries.
- `python scripts/select-validation.py --mode explicit ...` selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate` with no unclassified paths after test-spec authoring.
- `bash scripts/ci.sh --mode explicit ... --jobs 1` passed the selected checks after test-spec authoring: `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- `git diff --check --` passed after test-spec authoring.
- M1 baseline `python scripts/test-select-validation.py`: exit `0`, stdout `0` lines, stderr `67` lines, ran `62` tests.
- M1 baseline `python scripts/test-select-validation.py --verbose`: exit `0`, stdout `0` lines, stderr `67` lines, ran `62` tests.
- M1 baseline `python scripts/test-select-validation.py --json`: exit `2`; `--json` is currently unsupported.
- M1 baseline `python scripts/test-select-validation.py NoSuchTest`: exit `1`, stdout `0` lines, stderr `11` lines, failure evidence includes failed identifier and error message.
- M1 baseline `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/ci.sh`: exit `0`, selected `selector.regression`, stdout `10` lines, successful child output hidden by default.
- M1 baseline `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/ci.sh --verbose`: exit `0`, selected `selector.regression`, stdout `81` lines, successful child output exposed.
- M1 validation `python scripts/test-select-validation.py` passed: 62 tests.
- M1 validation `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/ci.sh --verbose` passed: selected `selector.regression`.
- M1 validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- M1 validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/script-output-audit.md --path docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md --path specs/script-output-optimization.test.md --path specs/script-output-optimization.md` passed: 4 artifact files validated.
- M1 selector inspection with `script-output-audit.md` included blocked that path as `change-local-unsupported`; it had no unclassified paths. Manual M1 routing for `script-output-audit.md` is `git diff --check -- docs/changes/2026-05-21-script-output-optimization/script-output-audit.md`, which passed.
- M1 selected validation excluding the manually routed audit path passed: selected `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- Code-review M1 R1 recording validation `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-21-script-output-optimization` passed: 7 reviews, 8 findings, 7 log entries, 8 resolution entries. Review-resolution remains open because `SRO-M1-CR1` is unresolved.
- Code-review M1 R1 recording validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- Code-review M1 R1 recording validation `git diff --check --` passed.
- Code-review M1 R1 recording validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/changes/2026-05-21-script-output-optimization/reviews/code-review-m1-r1.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed: 4 artifact files validated.
- Code-review M1 R1 selected validation passed: selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- `SRO-M1-CR1` hash verification command confirmed `selected-tests-baseline.txt` has 62 lines, one trailing newline, and `sha256:af470dd836f5b1b44c702be35206934f77621a1477d88cafae923e50a7f492bd`.
- `SRO-M1-CR1` validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- `SRO-M1-CR1` validation `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed: 7 reviews, 8 findings, 7 log entries, 8 resolution entries.
- `SRO-M1-CR1` validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/script-output-audit.md --path docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md --path docs/changes/2026-05-21-script-output-optimization/selected-tests-baseline.txt --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed: 4 artifact files validated.
- `SRO-M1-CR1` validation `git diff --check --` passed.
- `SRO-M1-CR1` selector inspection with `script-output-audit.md` and `selected-tests-baseline.txt` included blocked those paths as `change-local-unsupported`; it had no unclassified paths. Manual routing for those supporting evidence files is `git diff --check -- docs/changes/2026-05-21-script-output-optimization/script-output-audit.md docs/changes/2026-05-21-script-output-optimization/selected-tests-baseline.txt`, which passed.
- `SRO-M1-CR1` selected validation excluding manually routed evidence files passed: selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- `SRO-M1-CR1` validation `python scripts/test-select-validation.py` passed: 62 tests.
- Code-review M1 R2 validation `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed: 8 reviews, 8 findings, 8 log entries, 8 resolution entries.
- Code-review M1 R2 validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- Code-review M1 R2 validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md --path docs/changes/2026-05-21-script-output-optimization/selected-tests-baseline.txt --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/changes/2026-05-21-script-output-optimization/reviews/code-review-m1-r2.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed: 4 artifact files validated.
- Code-review M1 R2 validation `git diff --check --` passed.
- Code-review M1 R2 selected CI with `selected-tests-baseline.txt` included blocked that file as `change-local-unsupported`; manual route `git diff --check -- docs/changes/2026-05-21-script-output-optimization/selected-tests-baseline.txt` passed.
- Code-review M1 R2 selected CI excluding the manually routed evidence file passed: selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- M2 validation `python scripts/test-select-validation.py` passed: 72 tests, 7 expected failures.
- M2 validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/script-output-optimization.md --path specs/script-output-optimization.test.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml` passed: 4 artifact files validated.
- M2 validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- M2 selector inspection for `scripts/test-select-validation.py`, active plan, plan index, and change metadata selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- M2 validation `git diff --check -- scripts/test-select-validation.py specs/script-output-optimization.test.md docs/changes/2026-05-21-script-output-optimization docs/plans/2026-05-21-script-output-optimization.md docs/plan.md` passed.
- M2 selected CI `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md --jobs 1` passed: selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- Code-review M2 R1 recording validation `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-21-script-output-optimization` passed: 9 reviews, 9 findings, 9 log entries, 9 resolution entries. Review-resolution remains open because `SRO-M2-CR1` is unresolved.
- Code-review M2 R1 recording validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- Code-review M2 R1 recording validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/changes/2026-05-21-script-output-optimization/reviews/code-review-m2-r1.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed: 4 artifact files validated.
- Code-review M2 R1 recording validation `git diff --check --` passed.
- Code-review M2 R1 selected CI passed: selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- `SRO-M2-CR1` validation `python scripts/test-select-validation.py` passed: 63 tests.
- `SRO-M2-CR1` red-test proof `python scripts/test-select-validation.py ScriptOutputContractTests` exited nonzero before M3 with `FAILED (failures=9)`.
- `SRO-M2-CR1` validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- `SRO-M2-CR1` validation `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed: 9 reviews, 9 findings, 9 log entries, 9 resolution entries.
- `SRO-M2-CR1` validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/output-contract-red-test.md --path docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed: 4 artifact files validated.
- `SRO-M2-CR1` validation `git diff --check --` passed.
- `SRO-M2-CR1` selector inspection with `output-contract-red-test.md` included blocked that file as `change-local-unsupported`; it had no unclassified paths. Manual route `git diff --check -- docs/changes/2026-05-21-script-output-optimization/output-contract-red-test.md` passed.
- `SRO-M2-CR1` selected CI excluding the manually routed red-test evidence file passed: selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- Code-review M2 R2 recorded no material findings and closed M2.
- Code-review M2 R2 recording validation `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed: 10 reviews, 9 findings, 10 log entries, 9 resolution entries.
- Code-review M2 R2 recording validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- Code-review M2 R2 recording validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/changes/2026-05-21-script-output-optimization/reviews/code-review-m2-r2.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed: 4 artifact files validated.
- Code-review M2 R2 recording validation `git diff --check --` passed.
- Code-review M2 R2 selected CI passed: selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- M3 validation `python scripts/test-select-validation.py` passed: `[PASS] test-select-validation: 63 passed ...`.
- M3 validation `python scripts/test-select-validation.py ScriptOutputContractTests` passed: `[PASS] test-select-validation: 10 passed ...`.
- M3 validation `python scripts/test-select-validation.py --verbose` passed and emitted full unittest pass-list output for 63 tests.
- M3 validation `python scripts/test-select-validation.py --quiet` passed with exit `0`, `0` stdout bytes, and `0` stderr bytes.
- M3 validation `python scripts/test-select-validation.py --verbose --quiet` exited `2`, wrote `0` stdout bytes, and named both flags in stderr.
- M3 validation `python scripts/test-select-validation.py --json` exited `2` with `unrecognized arguments: --json`.
- M3 validation `python scripts/test-select-validation.py -k definitely_no_script_output_tests` exited `1` with zero-test `[FAIL]` output.
- M3 validation `python scripts/test-select-validation.py --quiet ScriptOutputFixtureTests.fixture_contract_failure` exited `1` with `[FAIL]`, failure name, assertion message, file location, and scoped rerun command.
- M3 validation `python scripts/test-select-validation.py NoSuchTest` exited `1` with `[FAIL]` and no scoped `-k "NoSuchTest"` rerun command.
- M3 selected-test proof from `python scripts/test-select-validation.py --verbose` recorded `63` ordered identifiers with SHA-256 `sha256:425feac0e0ea777c474032b954e6aa375b0f9d2986d82b9fd7053ac119e5a104`.
- M3 selected CI `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --jobs 1 --verbose` passed: selected `selector.regression` and exposed child `[PASS]` output in wrapper verbose mode.
- M3 validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- M3 validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/script-output-audit.md --path docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md --path docs/changes/2026-05-21-script-output-optimization/output-contract-red-test.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed: 4 artifact files validated.
- M3 validation `git diff --check --` passed.
- M3 selector inspection with `script-output-audit.md` and `output-contract-red-test.md` included blocked those files as `change-local-unsupported`; it had no unclassified paths. Manual route `git diff --check -- docs/changes/2026-05-21-script-output-optimization/script-output-audit.md docs/changes/2026-05-21-script-output-optimization/output-contract-red-test.md` passed.
- M3 selected CI excluding manually routed evidence files passed: selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- Code-review M3 R1 found `SRO-M3-CR1`; `ScriptOutputContractTests` are still excluded from ordinary post-M3 validation and must be routed into ordinary validation or an equivalent default-suite guard before M3 can close.
- Code-review M3 R1 recording validation `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-21-script-output-optimization` passed: 11 reviews, 10 findings, 11 log entries, 10 resolution entries.
- Code-review M3 R1 recording validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- Code-review M3 R1 recording validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/changes/2026-05-21-script-output-optimization/reviews/code-review-m3-r1.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed: 4 artifact files validated.
- Code-review M3 R1 recording validation `git diff --check --` passed.
- Code-review M3 R1 selected CI passed: selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- `SRO-M3-CR1` validation `python scripts/test-select-validation.py` passed: `[PASS] test-select-validation: 73 passed ...`; ordinary validation now includes `10` `ScriptOutputContractTests`.
- `SRO-M3-CR1` validation `python scripts/test-select-validation.py ScriptOutputContractTests` passed: `[PASS] test-select-validation: 10 passed ...`.
- `SRO-M3-CR1` selected-test proof from `python scripts/test-select-validation.py --verbose` recorded `73` ordered identifiers with SHA-256 `sha256:878bd8dfce24e987ee50ab36d686f54e8d821bf4a5b11fe831d381c57d164047`.
- `SRO-M3-CR1` validation `python scripts/test-select-validation.py --quiet` passed with exit `0`, `0` stdout bytes, and `0` stderr bytes.
- `SRO-M3-CR1` validation `python scripts/test-select-validation.py --verbose --quiet` exited `2`, wrote `0` stdout bytes, and named both flags in stderr.
- `SRO-M3-CR1` validation `python scripts/test-select-validation.py --json` exited `2` with `unrecognized arguments: --json`.
- `SRO-M3-CR1` validation `python scripts/test-select-validation.py -k definitely_no_script_output_tests` exited `1` with zero-test `[FAIL]` output.
- `SRO-M3-CR1` validation `python scripts/test-select-validation.py --quiet ScriptOutputFixtureTests.fixture_contract_failure` exited `1` with `[FAIL]`, failure name, assertion message, file location, and scoped rerun command.
- `SRO-M3-CR1` validation `python scripts/test-select-validation.py NoSuchTest` exited `1` with `[FAIL]` and no scoped `-k "NoSuchTest"` rerun command.
- `SRO-M3-CR1` validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- `SRO-M3-CR1` validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md --path docs/changes/2026-05-21-script-output-optimization/script-output-audit.md --path docs/changes/2026-05-21-script-output-optimization/output-contract-red-test.md --path docs/changes/2026-05-21-script-output-optimization/selected-tests-m3.txt --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed: 4 artifact files validated.
- `SRO-M3-CR1` validation `git diff --check --` passed.
- `SRO-M3-CR1` selector inspection with `script-output-audit.md`, `output-contract-red-test.md`, and `selected-tests-m3.txt` included blocked those files as `change-local-unsupported`; it had no unclassified paths. Manual route `git diff --check -- docs/changes/2026-05-21-script-output-optimization/script-output-audit.md docs/changes/2026-05-21-script-output-optimization/output-contract-red-test.md docs/changes/2026-05-21-script-output-optimization/selected-tests-m3.txt` passed.
- `SRO-M3-CR1` selected CI excluding manually routed evidence files passed: selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- Code-review M3 R2 recorded no material findings and closed M3.
- Code-review M3 R2 recording validation `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed: 12 reviews, 10 findings, 12 log entries, 10 resolution entries.
- Code-review M3 R2 recording validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- Code-review M3 R2 recording validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/changes/2026-05-21-script-output-optimization/reviews/code-review-m3-r2.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed: 4 artifact files validated.
- Code-review M3 R2 recording validation `git diff --check --` passed.
- Code-review M3 R2 selected CI passed: selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- M4 proof `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/ci.sh --jobs 1` passed: 10 stdout lines, selected `selector.regression`, child output hidden by default.
- M4 proof `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/ci.sh --jobs 1 --verbose` passed: 15 stdout lines, selected `selector.regression`, child `[PASS] test-select-validation: 73 passed ...` output exposed under `Selected check output`.
- M4 focused wrapper regression proof `python scripts/test-select-validation.py ValidationSelectionTests.test_ci_wrapper_jobs_one_uses_stable_summary_and_hides_success_output ValidationSelectionTests.test_ci_wrapper_run_to_completion_reports_failed_output_after_summary ValidationSelectionTests.test_ci_wrapper_verbose_prints_successful_output_in_stable_order` passed: 3 tests.
- M4 validation `python scripts/test-select-validation.py` passed: `[PASS] test-select-validation: 73 passed ...`.
- M4 validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- M4 validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/script-output-audit.md --path docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed: 4 artifact files validated.
- M4 validation `git diff --check --` passed.
- M4 selector inspection with `script-output-audit.md` included blocked that path as `change-local-unsupported`; it had no unclassified paths. Manual route `git diff --check -- docs/changes/2026-05-21-script-output-optimization/script-output-audit.md` passed.
- M4 selected CI excluding the manually routed audit path passed: selected `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- Code-review M4 R1 recorded no material findings and closed M4.
- Code-review M4 R1 recording validation `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed: 13 reviews, 10 findings, 13 log entries, 10 resolution entries.
- Code-review M4 R1 recording validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- Code-review M4 R1 recording validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/changes/2026-05-21-script-output-optimization/reviews/code-review-m4-r1.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed: 4 artifact files validated.
- Code-review M4 R1 recording validation `git diff --check --` passed.
- Code-review M4 R1 selected CI passed: selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- M5 final evidence updated `behavior-preservation.md` with final preservation and scope-boundary proof.
- M5 validation `python scripts/test-select-validation.py` passed: `[PASS] test-select-validation: 73 passed ...`.
- M5 validation `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed: 13 reviews, 10 findings, 13 log entries, 10 resolution entries.
- M5 validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- M5 validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-script-output-optimization.md --path specs/script-output-optimization.md --path specs/script-output-optimization.test.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md` passed: 4 artifact files validated.
- M5 validation `git diff --check --` passed.
- M5 selected CI with `script-output-audit.md` included blocked that path as `change-local-unsupported`; it had no unclassified paths and selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`. Manual route `git diff --check -- docs/changes/2026-05-21-script-output-optimization/script-output-audit.md` passed.
- M5 selected CI excluding the manually routed audit path passed: selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- Code-review M5 R1 recorded no material findings and closed M5.
- Code-review M5 R1 recording validation `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed: 14 reviews, 10 findings, 14 log entries, 10 resolution entries.
- Code-review M5 R1 recording validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- Code-review M5 R1 recording validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/changes/2026-05-21-script-output-optimization/reviews/code-review-m5-r1.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed: 4 artifact files validated.
- Code-review M5 R1 recording validation `git diff --check --` passed.
- Code-review M5 R1 selected CI passed: selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- Explain-change added `docs/changes/2026-05-21-script-output-optimization/explain-change.md` and synchronized the active plan and change metadata for verify handoff.
- Explain-change validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- Explain-change validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/explain-change.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed: 4 artifact files validated.
- Explain-change validation `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed: 14 reviews, 10 findings, 14 log entries, 10 resolution entries.
- Explain-change validation `git diff --check --` passed.
- Explain-change selected CI passed: selected `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- Verify rerun after explain-change found PR-mode CI blocked on `output-contract-red-test.md`, `script-output-audit.md`, `selected-tests-baseline.txt`, and `selected-tests-m3.txt` as `change-local-unsupported`.
- Selector-routing maintenance added those four evidence filenames to `change-local-lifecycle` routing and added selector regression fixture coverage.
- Selector-routing maintenance validation `python scripts/test-select-validation.py` passed: `[PASS] test-select-validation: 73 passed ...`.
- Selector-routing maintenance validation `bash scripts/ci.sh --mode pr --base $(git merge-base HEAD main) --head HEAD --jobs 1` passed: selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- Selector-routing maintenance validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- Selector-routing maintenance validation `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed before review recording: 14 reviews, 10 findings, 14 log entries, 10 resolution entries.
- Selector-routing maintenance validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-script-output-optimization.md --path specs/script-output-optimization.md --path specs/script-output-optimization.test.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md --path docs/changes/2026-05-21-script-output-optimization/explain-change.md` passed.
- Selector-routing maintenance validation `git diff --check --` passed.
- Code-review CI routing R1 recorded no material findings and closed the selector-routing maintenance fix.
- Code-review CI routing R1 recording validation `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed: 15 reviews, 10 findings, 15 log entries, 10 resolution entries.
- Code-review CI routing R1 recording validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- Code-review CI routing R1 recording validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/changes/2026-05-21-script-output-optimization/reviews/code-review-ci-routing-r1.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed: 4 artifact files validated.
- Code-review CI routing R1 recording validation `git diff --check --` passed.
- Code-review CI routing R1 selected CI passed: selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- Explain-change refresh updated `explain-change.md` with the selector-routing maintenance rationale, review outcome, validation evidence, scope-control correction, and remaining risks.
- Explain-change refresh validation `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- Explain-change refresh validation `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-21-script-output-optimization/explain-change.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md` passed: 4 artifact files validated.
- Explain-change refresh validation `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed: 15 reviews, 10 findings, 15 log entries, 10 resolution entries.
- Explain-change refresh validation `git diff --check --` passed.
- Explain-change refresh selected CI passed: selected `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- Final verify `python scripts/test-select-validation.py` passed: `[PASS] test-select-validation: 73 passed ...`.
- Final verify `python scripts/test-select-validation.py ScriptOutputContractTests` passed: `[PASS] test-select-validation: 10 passed ...`.
- Final verify `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-script-output-optimization` passed: 15 reviews, 10 findings, 15 log entries, 10 resolution entries.
- Final verify `python scripts/validate-change-metadata.py docs/changes/2026-05-21-script-output-optimization/change.yaml` passed.
- Final verify `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-script-output-optimization.md --path specs/script-output-optimization.md --path specs/script-output-optimization.test.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-21-script-output-optimization.md --path docs/plan.md --path docs/changes/2026-05-21-script-output-optimization/change.yaml --path docs/changes/2026-05-21-script-output-optimization/review-log.md --path docs/changes/2026-05-21-script-output-optimization/review-resolution.md --path docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md --path docs/changes/2026-05-21-script-output-optimization/explain-change.md` passed.
- Final verify `git diff --check --` passed.
- Final verify selected-test hash check passed for `selected-tests-baseline.txt` count `62` / `sha256:af470dd836f5b1b44c702be35206934f77621a1477d88cafae923e50a7f492bd` and `selected-tests-m3.txt` count `73` / `sha256:878bd8dfce24e987ee50ab36d686f54e8d821bf4a5b11fe831d381c57d164047`.
- Final verify `bash scripts/ci.sh --mode pr --base $(git merge-base HEAD main) --head HEAD --jobs 1` passed: selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- Final verify direct edge checks passed for quiet success silence, conflicting `--verbose --quiet`, zero-test failure, quiet failure details and rerun, JSON deferral, and no misleading `NoSuchTest` scoped rerun.
- Final verify `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 1` passed. It emitted unrelated baseline warnings for older draft proposal artifacts, then completed with `CI broad smoke checks passed`.

## Outcome and retrospective

- Not started. This section remains final-only while implementation and downstream gates are open.

## Readiness

- See `Current Handoff Summary`.
- Ready for PR handoff. Readiness is not Done; PR handoff and hosted CI remain open.
