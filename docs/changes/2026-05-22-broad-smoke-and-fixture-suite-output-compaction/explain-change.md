# Broad-Smoke and Fixture-Suite Output Compaction Explanation

## Summary

This change makes successful repository validation output shorter without changing what validation runs. It fixes the remaining script-output noise at two layers:

- the broad-smoke orchestrator now captures child output and prints one aggregate success line by default;
- the first targeted direct-run producer, `scripts/test-change-metadata-validator.py`, now uses compact default success and failure output while preserving verbose and quiet compatibility.

The change also records durable audit, identity, behavior-preservation, review, and lifecycle evidence so reviewers can verify that selected commands, selected tests, exit codes, failure evidence, selected-CI behavior, and out-of-scope generated surfaces were preserved. A final CI-maintenance fix routes those new deterministic evidence files through selected validation so local and PR CI do not require manual routing.

## Problem

The first script-output optimization slice made `scripts/test-select-validation.py` compact and kept the selected-CI wrapper failure-focused. Broad-smoke still had its own `run_check` path in `scripts/ci.sh` that streamed child stdout and stderr directly, so any noisy passing child could flood successful broad-smoke logs.

The accepted proposal framed this as a layer problem: producers print directly, and orchestrators print while running producers. Fixing only one layer would leave the other able to reintroduce noisy success output.

## Decision Trail

The accepted proposal chose the coordinated slice:

1. audit producer and orchestrator output layers;
2. make broad-smoke `run_check` capture successful child output and show child output on failure or `--verbose`;
3. compact the first targeted direct-run producer, locked to `scripts/test-change-metadata-validator.py`;
4. record behavior-preservation and lifecycle evidence.

The approved spec added requirements R36 through R65 and acceptance criteria AC15 through AC36. The focused test spec operationalized them as TSRO-015 through TSRO-027.

No architecture artifact was created because the active plan records this as a presentation-only wrapper/producer formatting change with no new persistence, API, deployment, security boundary, or long-lived design package.

Implementation followed four plan milestones:

- M1: output-layer audit and baseline identity proof;
- M2: broad-smoke wrapper capture;
- M3: compact `scripts/test-change-metadata-validator.py` default output;
- M4: final preservation evidence and lifecycle closeout.

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `scripts/ci.sh` | Changed broad-smoke `run_check` to capture combined child stdout/stderr, print captured output on failure, print captured successful output only under `--verbose`, and emit one aggregate `[PASS] broad-smoke` line. | Satisfies the orchestrator-layer fix for R39 through R49 and AC16 through AC21. | Proposal option 4; spec R39-R49; plan M2. | `python scripts/test-select-validation.py`; `bash scripts/ci.sh --mode broad-smoke`; `bash scripts/ci.sh --mode broad-smoke --verbose`; `broad-smoke-child-commands-post-m2.txt`; `broad-smoke-child-commands-post-m4.txt`. |
| `scripts/test-change-metadata-validator.py` | Replaced the default `unittest.main(verbosity=2)` entrypoint with a scoped runner supporting compact default output, actionable failure summaries, `--verbose` / `-v`, existing unittest-compatible `--quiet` / `-q`, `-k` filtering, zero-test failure, and an opt-in failure fixture. | Satisfies first-producer compaction while preserving compatibility and selected-test identity. | Spec R53-R62 and R60-R60c; plan M3; spec-review `SRO-BSO-SR1`. | Producer subprocess tests in `scripts/test-select-validation.py`; direct producer commands; `change-metadata-validator-tests-post-m3.txt`; `change-metadata-validator-tests-post-m4.txt`. |
| `scripts/test-select-validation.py` | Added broad-smoke fixture workspaces, wrapper-mode consistency guard checks, negative fixtures for direct streaming, and subprocess tests for the producer default, failure, verbose, quiet, and zero-test behavior. | Ensures output contracts run in ordinary validation and prevents future wrapper divergence. | Spec R51-R52, R63; test spec TSRO-017 through TSRO-024. | `python scripts/test-select-validation.py`; focused M2/M3 runs recorded in `change.yaml`. |
| `scripts/validation_selection.py` and selector tests in `scripts/test-select-validation.py` | Classified `script-output-layer-audit.md`, broad-smoke command identity files, and change-metadata-validator selected-test identity files as change-local lifecycle artifacts. | Final local CI found these deterministic evidence files were valid but lacked a v1 selector route, producing `manual-routing-required`. They now route to `artifact_lifecycle.validate`. | CI-maintenance triggered by verify; learn session `2026-05-22-change-local-selector-routing`. | `python scripts/test-select-validation.py`; `bash scripts/ci.sh --mode local --jobs 1`. |
| `specs/script-output-optimization.md` | Added broad-smoke and first-producer requirements, examples, quiet compatibility contract, non-goals, acceptance criteria, and future quiet-formatting boundary. | Makes the new wrapper and producer behavior contract-level and resolves the spec-review quiet compatibility defect. | Proposal review findings `BSO-PR1` through `BSO-PR4`; spec review `SRO-BSO-SR1`. | Spec-review R2 approved; lifecycle validation passed. |
| `specs/script-output-optimization.test.md` | Added TSRO-015 through TSRO-027 covering audit evidence, command/test identity proof, broad-smoke output, wrapper consistency, producer output, quiet compatibility, ordinary-validation guard, selected-CI regression, and final smoke validation. | Turns the accepted spec into concrete proof obligations before implementation. | Active plan M0 and owner-approved test-spec amendment. | Plan-review R1 approved; owner approved the test spec for implementation. |
| `docs/changes/.../script-output-layer-audit.md` | Added the producer/orchestrator matrix, selected-CI and broad-smoke path separation, first-producer decision, and post-M2/M3/M4 updates. | Documents every layer that can print and prevents repeating the first-slice blind spot. | Spec R36-R38; test spec TSRO-015. | M1 code-review clean; final M4 evidence update. |
| `docs/changes/.../behavior-preservation.md` | Added baseline and post-change matrices for broad-smoke command identity, producer selected-test identity, pass/fail evidence, verbose behavior, quiet compatibility, selected-CI behavior, and out-of-scope surfaces. | Proves shorter output is presentation-only rather than a validation selection change. | Spec R49-R50, R62-R65; test spec TSRO-016, TSRO-024, TSRO-026, TSRO-027. | Matching SHA-256 hashes: broad-smoke `8b1e4d0d7f36fccc0b7d0e2fa3ad5efedc39f7f41f935bb117c8c9f6eda9565f`; producer `fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e`. |
| `docs/changes/.../*commands*.txt` and `*tests*.txt` | Added baseline, post-M2, post-M3, and post-M4 identity files. | Provides stable replayable proof for command and selected-test identity. | Proposal `Behavior-preservation proof`; spec R50 and R62. | `sha256sum` evidence recorded in `change.yaml`. |
| `docs/proposals/...`, `docs/plans/...`, `docs/plan.md`, `docs/changes/.../change.yaml`, `review-log.md`, `review-resolution.md`, and review records | Added and maintained lifecycle artifacts, review records, review resolutions, validation evidence, and plan state through M1-M4. | Required by the workflow for a planned, non-trivial, reviewable change. | `CONSTITUTION.md`, `AGENTS.md`, active plan, and formal review rules. | Review-artifact validation and change metadata validation passed after M4 R2. |

## Tests Added Or Changed

The main automated test surface is `scripts/test-select-validation.py`:

- TSRO-017: broad-smoke success captures child output and prints one aggregate summary.
- TSRO-018: broad-smoke failure includes failed child identity, command, exit status, duration, and captured output.
- TSRO-019: broad-smoke `--verbose` emits successful child output in stable order.
- TSRO-020: wrapper-mode consistency guard checks current `scripts/ci.sh` and fails on direct-streaming validation modes or bare `"$@"` streaming outside `run_check`.
- TSRO-021: `scripts/test-change-metadata-validator.py` default success and failure output is compact and actionable.
- TSRO-022: producer `--verbose` and `-v` preserve full unittest detail.
- TSRO-023: producer `--quiet` and `-q` remain accepted and keep existing unittest-compatible quiet behavior.
- TSRO-024: zero selected tests fail and producer selected-test identity is proven by ordered identifiers plus SHA-256.

The test level is appropriate because the changed behavior is command-line output and wrapper orchestration. Subprocess tests exercise the same entrypoints maintainers and CI use instead of only unit-testing formatter helpers.

## Validation Evidence Available Before Final Verify

Recorded validation includes:

- `python scripts/test-select-validation.py`
- `python scripts/test-change-metadata-validator.py`
- `python scripts/test-change-metadata-validator.py --verbose`
- `python scripts/test-change-metadata-validator.py --quiet`
- `python scripts/test-change-metadata-validator.py -q`
- `bash scripts/ci.sh --mode broad-smoke`
- `bash scripts/ci.sh --mode broad-smoke --verbose`
- selected explicit CI over `scripts/ci.sh`, `scripts/test-change-metadata-validator.py`, `scripts/test-select-validation.py`, the spec, test spec, plan, plan index, and change metadata
- `bash scripts/ci.sh --mode local --jobs 1`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `git diff --check --`

The active plan and `change.yaml` contain the full command history and results. Final `verify` has not run yet.

## Review Resolution Summary

Formal review evidence is recorded under `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/`.

Review-resolution status is closed. The review log has 12 review entries and no open findings. Material findings resolved:

- proposal-review R1: 4 accepted and resolved findings (`BSO-PR1` through `BSO-PR4`);
- spec-review R1: 1 accepted and resolved finding (`SRO-BSO-SR1`);
- code-review M2 R1: 1 accepted and resolved finding (`BSO-M2-CR1`);
- code-review M3 R1: 2 accepted and resolved findings (`BSO-M3-CR1`, `BSO-M3-CR2`);
- code-review M4 R1: 1 accepted and resolved finding (`BSO-M4-CR1`).

The final milestone review, code-review M4 R2, closed M4 with `clean-with-notes`.

## Alternatives Rejected

- Producer-only compaction was rejected because broad-smoke could still stream future noisy children.
- Broad-smoke-only compaction was rejected because direct maintainer runs of the named producer would remain verbose.
- Rewriting every verbose unittest producer was rejected as unnecessary churn for this slice.
- Per-child broad-smoke success lines were rejected in favor of one aggregate line because per-child success still grows with the amount of work.
- Custom compact quiet formatting for `scripts/test-change-metadata-validator.py` was rejected after spec review found `--quiet` and `-q` were already accepted unittest-compatible invocations.
- A shared output helper library was deferred because this slice did not need enough duplicated formatting logic to justify a new abstraction.

## Scope Control

The change does not intentionally alter:

- validation selection behavior, except for the CI-maintenance selector route that classifies the new change-local evidence files for deterministic local/PR validation;
- broad-smoke child command selection or order;
- producer selected-test identity;
- selected-CI behavior;
- generated skill output;
- adapter output or adapter installation behavior;
- JSON support;
- UI transcript folding.

The recorded hashes prove broad-smoke child command identity and producer selected-test identity did not change.

## Risks And Follow-Ups

Remaining risks before final verify:

- final verify may still find stale lifecycle state or a validation gap across the full branch;
- hosted CI has not been claimed;
- PR readiness has not been claimed.

Follow-ups intentionally left out of this slice:

- broader compact defaults for other verbose producers identified by the audit;
- a shared script-output helper if multiple future producers need the same formatter;
- JSON output across validation scripts;
- broader CI log standardization if other wrappers diverge later.

## Current Readiness

All implementation milestones are closed after code review, CI-maintenance has cleared the local selector blocker, and this explanation records the rationale for the actual diff. The active plan's next stage is `verify`.

This artifact does not claim final verification, branch readiness, PR readiness, or hosted CI status.
