# Test and CI Speed Optimization

## Status

- accepted

## Problem

RigorLoop's selector already decides which validation checks should run, and `scripts/ci.sh` already executes them. The immediate slowdown is that independent checks run serially even when they could safely run together.

The change should not become a broad CI redesign. The narrow problem is to add bounded parallel execution for reviewed safe checks inside the wrapper while preserving selector ownership, deterministic output, and existing validation semantics.

## Goals

- Reduce local validation wall-clock time by running independent checks in parallel.
- Keep `scripts/select-validation.py` responsible for what runs.
- Keep `scripts/ci.sh` responsible for how selected checks execute.
- Make parallel safety explicit through a reviewed allowlist.
- Preserve nonzero exit behavior, failure attribution, and readable logs.
- Keep hosted matrix, caching, runner changes, and distributed execution out of the first slice.

## Non-goals

- Weakening required validation or skipping selected checks.
- Running all checks in parallel by default.
- Moving path or check selection into GitHub Actions YAML.
- Adding persistent result caching, dependency caching, or input hashing.
- Adding per-check sandboxing, cgroups, containers, distributed workers, or advanced scheduling.
- Changing generated-output sync behavior.

## Vision fit

fits the current vision

This fits RigorLoop's focus on reviewable validation evidence. The proposal changes execution shape, not proof requirements or source-of-truth boundaries.

## Context

`CONSTITUTION.md` requires repository-owned validation logic and thin GitHub Actions wrappers. The accepted validation contract already says the selector is the source of truth and `scripts/ci.sh` is the wrapper.

The repository currently has six test scripts:

- `scripts/test-adapter-distribution.py`
- `scripts/test-artifact-lifecycle-validator.py`
- `scripts/test-change-metadata-validator.py`
- `scripts/test-review-artifact-validator.py`
- `scripts/test-select-validation.py`
- `scripts/test-skill-validator.py`

Those six scripts were inspected for shared writes and then run concurrently with `xargs -P6`; the concurrent run passed. That makes them good initial candidates, but still not something to parallelize by assumption.

The current hosted CI is one job that checks out the repository, sets up Python, and calls `scripts/ci.sh`. Hosted matrix fan-out can be considered later if one-runner parallelism still leaves a meaningful hosted wall-clock bottleneck.

## Options considered

### Option 1: Keep serial execution

This is lowest risk but leaves obvious local speedup unused.

### Option 2: Parallelize every selected check by default

This is simple, but unsafe. A newly selected check that writes shared generated output, mutates Git state, or uses a fixed external resource could become flaky.

### Option 3: Add GitHub Actions matrix first

This gives job isolation, but repeats checkout and setup, risks duplicating routing in workflow YAML, and is likely worse for short checks.

### Option 4: Add bounded wrapper parallelism with a safe-check allowlist

This improves local wall-clock time while keeping selection in repo-owned scripts. It fails safely: a forgotten allowlist entry runs sequentially instead of racing.

## Recommended direction

Choose Option 4.

Add bounded parallel execution to `scripts/ci.sh` for check IDs that are explicitly marked parallel-safe. Checks not on the allowlist run sequentially even when parallelism is enabled.

A check is parallel-safe only if it reads repository files without writing tracked paths, writes only to a process-unique scratch directory, holds no shared external resource such as a fixed port or global Git config mutation, and writes output only to its own stdout/stderr streams.

The first slice should:

- add `--jobs N`;
- make `--jobs 1` explicit sequential execution;
- default local jobs to CPU count minus one, with a floor of one;
- reject `--jobs 0`, invalid values, and unlimited fan-out;
- start the allowlist with the six inspected `scripts/test-*.py` checks;
- wait for all started checks to finish by default;
- add optional `--fail-fast`, but not as the default;
- add a 60-second per-check timeout, with `--timeout` to override;
- capture stdout and stderr per check, without interleaving live logs;
- print a stable summary table in selector order with check ID, status, exit reason, and elapsed time;
- print full output for failed checks, and hide successful logs unless `--verbose` is set;
- report nonzero exits, signal kills, unavailable commands, and per-check timeouts distinctly;
- measure elapsed time from process start to process exit, not queue time.

The 60-second timeout is sized to the current work, not a generic category. A recent broad-smoke run completed the whole wrapper, selector overhead, checkout/setup-equivalent local work, and eleven checks in well under one minute. A 60-second per-check limit gives several times the observed slow-check headroom while still killing hangs quickly enough to keep local iteration useful.

Timeouts should apply at the leaf check level. Recursive wrapper checks such as `broad_smoke.repo` should not need a special outer timeout when their leaf checks are already bounded. If a future check legitimately needs more time, callers can use `--timeout 300`, or the catalog can add a reviewed per-check override for that recurring case.

Hosted CI should not add matrix fan-out in this slice. If hosted CI later uses matrix execution, the matrix axis should come from stable check IDs emitted by repo-owned scripts, and each matrix job should call the same wrapper with a single-check form such as `--check-id <id>`.

Persistent caching remains out of scope. It needs its own correctness rules for inputs, invalidation, and freshness.

## Expected behavior changes

- Local users can run safe selected checks concurrently through `scripts/ci.sh`.
- Unsafe or unclassified checks keep serial behavior.
- A failing parallel run still reports all started check results by default.
- Wrapper output becomes deterministic and failure-focused instead of interleaved.
- CI workflow YAML remains a thin caller of repository scripts.

## Architecture impact

The change is contained to validation execution orchestration.

Likely affected surfaces:

- `specs/test-and-ci-speed-optimization.md`
- `specs/test-and-ci-speed-optimization.test.md`
- `docs/workflows.md`
- `scripts/ci.sh`
- `scripts/test-select-validation.py`
- `scripts/validation_selection.py` for per-check metadata such as parallel-safety and any future per-check timeout override

No service, database, persistent cache, generated adapter layout, or hosted runner topology change is required in the first slice.

Configuration should stay with the code that owns the decision:

| Configuration kind | Location |
| --- | --- |
| Per-check command, paths, version, and parallel-safety | `scripts/validation_selection.py` check catalog |
| Selector decision rules | `scripts/validation_selection.py` and `scripts/select-validation.py` |
| Wrapper defaults such as `--jobs` and `--timeout` | top-level constants in `scripts/ci.sh` |
| Invocation overrides | command-line flags |
| Test fixtures | environment variables, following the existing fixture pattern |
| Hosted CI environment | `.github/workflows/ci.yml` |

## Testing and verification strategy

The spec should require tests for:

- parallel-safe allowlist behavior;
- `--jobs 1` sequential behavior;
- `--jobs N` running allowlisted checks concurrently while non-allowlisted checks stay serial;
- run-to-completion behavior when one check fails;
- optional `--fail-fast`;
- stable summary and failed-output ordering;
- separate stdout/stderr capture;
- invalid job values, invalid timeout values, unknown check IDs, unavailable commands, nonzero exit, signal kill, and timeout reporting.

Verification should include a concurrent run of the six initial `scripts/test-*.py` scripts and selector-selected proof for touched files. Broad smoke remains governed by existing triggers.

## Rollout and rollback

Roll out by adding wrapper support, enabling only the initial reviewed allowlist, and documenting `--jobs 1` as the escape hatch for suspected races.

Rollback is straightforward: run with `--jobs 1`, remove a check ID from the allowlist, or revert the wrapper change. Matrix and caching are not part of this rollout.

## Risks and mitigations

- Risk: a check marked safe has hidden shared state.
  Mitigation: require allowlist review and keep `--jobs 1`.

- Risk: logs become unreadable.
  Mitigation: buffer per-check output and print stable summaries plus failed logs.

- Risk: parallelism hides other failures through early exit.
  Mitigation: default to run-to-completion; make fail-fast opt-in.

- Risk: local machines become overloaded.
  Mitigation: bounded CPU-count-minus-one default, explicit override, and no unlimited mode.

- Risk: hosted matrix duplicates selector logic.
  Mitigation: defer matrix and require repo-owned check IDs before any hosted fan-out.

## Open questions

- Should JSON summary output be included in the first implementation slice or deferred until hosted matrix orchestration needs it?

This does not block proposal review.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-04 | Use bounded script-level parallelism with an explicit parallel-safe allowlist as the first slice. | It is the smallest useful speed improvement and preserves selector, wrapper, and workflow boundaries. | Serial-only execution; parallel-by-default execution. |
| 2026-05-04 | Defer GitHub Actions matrix execution and caching. | Matrix and caching have different cost and correctness tradeoffs and should be justified after wrapper parallelism is proven. | Matrix-first CI redesign; persistent result caching; dependency caching in this slice. |
| 2026-05-04 | Use a 60-second default per-check timeout with `--timeout` override. | Current validation checks are short enough that 60 seconds gives practical headroom while still detecting hangs quickly. | Generic multi-minute timeout defaults; no timeout in the first slice. |

## Next artifacts

- Proposal review after this substantive revision.
- `specs/test-and-ci-speed-optimization.md`.
- `specs/test-and-ci-speed-optimization.test.md`.
- Architecture update or ADR only if the spec changes selector metadata ownership, wrapper boundaries, or hosted CI topology.
- Execution plan after the spec and test spec settle.

## Follow-on artifacts

- `proposal-review`: approved with no material findings after the bounded-parallelism revision.
- `specs/test-and-ci-speed-optimization.md`.
- `specs/test-and-ci-speed-optimization.test.md`.
- `docs/plans/2026-05-04-test-and-ci-speed-optimization.md`.

## Readiness

Accepted. The proposal is intentionally scoped to bounded wrapper parallelism; matrix and caching are deferred. Follow-on spec, active test spec, and execution plan exist; implementation is next.
