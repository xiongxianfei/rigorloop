# Test and CI Speed Optimization Explain Change

## Summary

This change adds bounded parallel execution for selector-selected CI checks while keeping the selector, wrapper, and hosted workflow boundaries intact.

M1 adds the metadata and command-line contract needed before parallel execution is possible: the catalog records explicit `parallel_safe` metadata, exposes `is_parallel_safe_check`, and `scripts/ci.sh` accepts `--jobs`, `--timeout`, `--fail-fast`, and `--verbose` without changing existing selector arguments.

M2 replaces ad hoc selected-check execution with a deterministic result model: each selected check gets captured stdout/stderr, stable summary rows, failed-output sections, optional successful output under `--verbose`, timeout handling, and distinct failure attribution for nonzero exits, signals, unavailable commands, and timeouts.

M3 adds the bounded scheduler: consecutive allowlisted checks run concurrently up to the configured job cap, non-allowlisted checks run alone, default execution runs to completion, and `--fail-fast` stops only queued work while preserving final status for already-started checks.

M4 documents the wrapper flags in contributor workflow guidance, proves hosted CI remains a thin matrix-free caller of `scripts/ci.sh`, and records final six-script plus broad-smoke proof. Code-review and verify are complete; this explanation closes the durable rationale and hands the branch to PR preparation.

## Problem

The repository already had several independent validation scripts, but selected-check execution was sequential and the proposal was at risk of becoming larger than needed. The selected direction was deliberately narrow: run reviewed safe checks in parallel inside `scripts/ci.sh`, keep non-reviewed checks serial, keep logs deterministic, and defer hosted matrix fan-out, caching, distributed execution, and sandboxing.

## Decision Trail

- Exploration option selected: simple script-level bounded parallelism first, with hosted matrix fan-out deferred until measurement shows single-runner parallelism is not enough.
- Proposal: `docs/proposals/2026-05-04-test-and-ci-speed-optimization.md`
- Spec: `specs/test-and-ci-speed-optimization.md`
- Test spec: `specs/test-and-ci-speed-optimization.test.md`
- Plan: `docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
- Requirements covered: `R1`-`R20`, with M4 specifically covering `R9`, `R10`, `R15`, `R17`-`R20`, and `AC1`-`AC9`.
- Architecture/ADR decision: no architecture update was needed because the existing selector/wrapper boundary already models the design. The selector still decides what to run; the wrapper decides how to execute selected checks; hosted CI stays a thin caller.
- Plan milestones: M1 metadata and flags, M2 deterministic sequential result model, M3 bounded scheduling, M4 contributor guidance and final proof.

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `scripts/validation_selection.py` | Adds `parallel_safe` catalog metadata and marks only reviewed regression check IDs safe. | Encodes independence by allowlist instead of parallel-by-default. | Spec `R4`-`R5`, plan M1 | `python scripts/test-select-validation.py`; six-script `--jobs 6` proof |
| `scripts/ci.sh` | Parses `--jobs`, `--timeout`, `--fail-fast`, and `--verbose`; implements captured result execution, timeout handling, failure attribution, stable summaries, and bounded scheduling. | Keeps execution policy in the wrapper and preserves selector ownership. | Spec `R1`-`R3`, `R6`-`R14`, `R16`, `R20`; plan M1-M3 | Selector regression suite; selected wrapper proofs; direct broad smoke |
| `scripts/test-select-validation.py` | Adds regression coverage for catalog metadata, wrapper flags, deterministic reporting, output isolation, timeout/signal/unavailable-command reporting, bounded scheduling, fail-fast, workflow guidance, and hosted CI boundaries. | Tests the contract at the selector/wrapper boundary without adding test-only production commands. | Test spec `T1`-`T19` | Red/green `python scripts/test-select-validation.py`; final 55-test pass |
| `docs/workflows.md` | Documents `--jobs`, `--jobs 1`, `--timeout`, `--fail-fast`, `--verbose`, and the matrix-free hosted-CI boundary. | Makes the completed wrapper behavior discoverable while preserving deferred non-goals. | Spec `R17`-`R20`; test spec `T17` | `test_workflow_guidance_aligns_with_validation_layering_contract`; hosted CI inspection |
| `.github/workflows/ci.yml` | Unchanged. | The existing workflow already delegates PR and main validation to `scripts/ci.sh`; changing it would exceed the first slice. | Spec `R17`-`R19`, `AC9` | `test_hosted_ci_remains_thin_and_matrix_free`; grep inspection |
| `docs/changes/2026-05-04-test-and-ci-speed-optimization/` | Maintains change metadata, review records, review resolution, and this explanation. | Satisfies the non-trivial change-local artifact pack and keeps review/verify evidence durable. | Governance docs-change baseline | Change metadata, review artifact, and lifecycle validation |
| `docs/plans/2026-05-04-test-and-ci-speed-optimization.md` and `docs/plan.md` | Records milestone progress, review/verify/explain-change completion, validation notes, and next-stage readiness. | Keeps the active plan and plan index aligned with actual stage state. | Plan file policy and verify lifecycle rules | Artifact lifecycle validation and selected wrapper proof |

## Tests Added Or Changed

- `T1` / catalog metadata: proves the initial safe set is explicit and unknown checks are unsafe by default.
- `T2` / wrapper CLI contract: proves `--jobs`, `--timeout`, `--fail-fast`, and `--verbose` are accepted by the wrapper and not forwarded incorrectly to the selector.
- `T3`-`T5` / invalid inputs and sequential fallback: prove invalid execution flags fail before checks start and `--jobs 1` remains deterministic.
- `T6`-`T9` / bounded scheduler: prove allowlisted concurrency, non-allowlisted isolation, default run-to-completion, and `--fail-fast` queued cancellation.
- `T10`-`T14` / output and failure attribution: prove stable summaries, per-check output isolation, successful-output verbosity, timeouts, signal kills, unknown IDs, and unavailable commands.
- `T15` / broad smoke: proves `broad_smoke.repo` preserves non-recursive broad-smoke behavior and avoids a selected-check outer timeout.
- `T17` / hosted CI boundary: proves contributor guidance exists and `.github/workflows/ci.yml` does not add matrix axes, hardcoded check IDs, selector duplication, cache setup, distributed execution, or sandbox setup.
- `T18` / real six-script proof: proves the initial reviewed regression candidates pass under `--jobs 6`.
- `T19` / safety evidence: ties the allowlist to recorded inspection evidence.

These are boundary-level tests because the risk sits at repository validation orchestration, not inside one pure function.

## Verification Evidence

- `python scripts/test-select-validation.py`
  - Passed after each milestone; final M4 focused suite passed with 55 tests.
- `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path scripts/test-adapter-distribution.py --path scripts/test-change-metadata-validator.py --path scripts/test-review-artifact-validator.py --path scripts/test-select-validation.py --path scripts/test-artifact-lifecycle-validator.py --jobs 6`
  - Passed selected checks `skills.regression`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.regression`, `artifact_lifecycle.regression`, `change_metadata.regression`, and `selector.regression`.
- `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path .github/workflows/ci.yml --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md`
  - Passed and selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
- `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path .github/workflows/ci.yml --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --jobs 2`
  - Passed the selected checks, including `broad_smoke.repo`.
- `bash scripts/ci.sh --mode broad-smoke`
  - Passed direct broad smoke.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Passed with both material review findings closed.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml`
  - Passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md`
  - Passed.
- `git diff --check -- docs/workflows.md .github/workflows/ci.yml scripts/test-select-validation.py docs/plan.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Passed.
- `rg -n '[[:blank:]]$|\\t' docs/workflows.md scripts/test-select-validation.py docs/plan.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Returned no matches.

CI status: local repository CI proof passed. Hosted CI was not observed.

## Review Resolution Summary

Two material code-review findings were recorded and accepted in `docs/changes/2026-05-04-test-and-ci-speed-optimization/review-resolution.md`:

- `CR1-F1`: stale plan-index state was corrected.
- `CR2-F1`: missing M2 proof was fixed by adding large-output isolation coverage and a default-timeout constant assertion.

`review-resolution.md` is at `Closeout status: closed`, `review-log.md` lists no open findings, and final direct M4 code-review returned `clean-with-notes` with no blocking or required-change findings.

## Alternatives Rejected

- GitHub Actions matrix fan-out: deferred because the first slice should prove script-level parallelism before multiplying hosted checkouts and setup cost.
- Persistent caching or input-hash skip logic: deferred because caching has separate correctness questions around invalidation and freshness.
- Distributed execution or per-check sandboxing: out of scope for a six-check bounded local scheduler.
- Parallel-by-default with an exclusion list: rejected in favor of an explicit allowlist because forgetting to mark a check safe only leaves performance on the table, while forgetting to mark a check unsafe can create intermittent races.
- A new CI runner module: not added because the existing wrapper could hold the scheduler without creating a new architecture boundary.

## Scope Control

The selector remains the source of selected checks, hosted CI remains a thin wrapper, existing modes and arguments keep their meaning, and generated outputs were not hand-edited. Non-allowlisted checks still run serially even when `--jobs` is greater than one.

## Risks And Follow-Ups

- A future allowlisted check could gain hidden shared state; recovery is to remove its check ID from the allowlist and rerun with `--jobs 1`.
- Local resource pressure can still happen on small machines; contributors can use `--jobs 1` or a lower explicit cap.
- Hosted CI may later need matrix fan-out if single-runner wall-clock remains high; that should be a separate measured proposal that consumes stable check IDs from repository-owned scripts.
- Hosted CI has not been observed in this local verify/explain-change run.

## PR Handoff

- Summary: adds bounded parallel selected-check execution, deterministic reporting, fail-fast support, workflow guidance, and hosted-CI boundary proof.
- Tests: selector regression suite, selected wrapper proof, direct broad smoke, review closeout validation, change metadata validation, artifact lifecycle validation, diff check, and whitespace scan passed.
- Reviewer focus: scheduler boundaries for allowlisted versus non-allowlisted checks, `broad_smoke.repo` timeout behavior, and confirmation that hosted CI remains matrix-free.
- Readiness: M1-M4, code-review, verify, and explain-change are complete. The next stage is `pr`; direct `$explain-change` stops before opening or preparing the PR.
