# Broad-Smoke Safe Parallelism Explain Change

## Summary

This change adds first-slice, opt-in broad-smoke parallel execution for children that are classified as high-confidence independent, while keeping omitted `--jobs` and `--jobs 1` behavior sequential. It also records the child classification, baseline timing, preservation proof, opt-in result evidence, review records, and lifecycle metadata needed to show that the speedup changes scheduling only.

Default broad-smoke parallelism was not promoted. The recorded local opt-in run with `--jobs 4` passed and improved wall time from the M1 single-run baseline by 42061ms / 11.24%, below the proposal's 30% median target and still dominated by sequential-only children.

## Problem

Broad-smoke remained the largest measured local validation bottleneck after selector-regression optimization. The accepted direction was narrow: reduce broad-smoke wall-clock time by running independent child checks concurrently, without changing the child set, child commands, failure detection, diagnostic value, output ordering, or final broad-verification meaning.

## Decision Trail

- Proposal: `docs/proposals/2026-06-27-broad-smoke-safe-parallelism.md`
- Proposal review: approved with no material findings; open-question decisions recorded before spec.
- Spec: `specs/broad-smoke-safe-parallelism.md`
- Spec review: approved with no material findings.
- Architecture: recorded as not required because the change stays inside the existing CI wrapper and repository-owned validation scripts; no persistent worker, cache, composition framework, protocol, persistence, deployment, or trust boundary was introduced.
- Plan: `docs/plans/2026-06-27-broad-smoke-safe-parallelism.md`
- Plan milestones:
  - M1: inventory, classification freshness, and sequential timing baseline.
  - M2: opt-in parallel executor and deterministic aggregation.
  - M3: result evidence, default-promotion decision, and closeout evidence.
  - Final holistic code-review: complete branch review before explain-change and verify.
- Requirements: `R1`-`R42`
- Acceptance criteria: `AC1`-`AC24`
- Test spec: `specs/broad-smoke-safe-parallelism.test.md`

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test / evidence |
| --- | --- | --- | --- | --- |
| `scripts/ci.sh` | Added classification preflight, opt-in broad-smoke parallel scheduling for explicit `--jobs > 1`, per-child result files, deterministic aggregation, verbose grouped output, scheduler-error handling, and optional result-evidence writing through `RIGORLOOP_BROAD_SMOKE_RESULT_JSON`. | Implements scheduling-only parallelism while preserving sequential compatibility and failure evidence. | Spec `R3`-`R32`, `R36`-`R40`; M2/M3 plan | `python scripts/test-select-validation.py -k broad_smoke`; `python scripts/test-select-validation.py -k jobs`; `bash -n scripts/ci.sh`; real `--jobs 1` and `--jobs 4` broad-smoke runs |
| `scripts/validate-broad-smoke-classification.py` | Added a stdlib-only validator that reconciles the change-local classification artifact with the `scripts/ci.sh` canonical child inventory and fails closed for stale, missing, low-confidence parallel-safe, or contradictory metadata. | Makes classification freshness a validation surface before parallel execution. The PyYAML dependency was removed after review finding `CR-M1-1`. | Spec `R1`-`R12`, `R29`-`R32`, `R41`-`R42`; M1 | `python scripts/validate-broad-smoke-classification.py`; classification freshness regressions |
| `scripts/test-select-validation.py` | Added broad-smoke fixtures for child inventory, classification reconciliation, omitted `--jobs`, `--jobs 1`, explicit opt-in overlap, deterministic output, single and multiple failures, missing classification, worker crash, verbose grouping, result evidence, and baseline/result artifact shape. | Proves the behavioral contract without relying only on expensive real broad-smoke runs. | Test spec `BSP-T1`-`BSP-T12`; M1-M3 | Focused test selections through M1-M3; worker-crash regression for `CR-M2-1` |
| `scripts/validation_selection.py` | Registered broad-smoke parallelism evidence and validator paths so selected CI routes the new validation surface. | Prevents manual routing debt for the new validator and evidence artifacts. | Plan validation routing; scope-control requirements | Selected explicit CI over touched implementation and evidence paths |
| `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-child-classification.yaml` | Added JSON-compatible YAML classification for every current broad-smoke child, including eligibility, side-effect metadata, paths, resource notes, and isolation decisions. | Provides the implementation input for safe eligibility without becoming an independent child-list owner. | Spec `R1`-`R12`, `R41`-`R42`; M1 | Classification validator and freshness tests |
| `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-baseline.yaml` | Recorded a local WSL2 sequential per-child timing baseline before scheduling changes. | Establishes attribution and preserves the "measure first" contract. | Spec `R33`-`R36`; M1 | Baseline artifact shape test; recorded broad-smoke baseline run |
| `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md` | Recorded child set, command identity, output, diagnostics, `--verbose`, rollback, cache boundary, and final-verify preservation evidence. | Makes behavior preservation reviewable instead of implicit. | Spec `R5`-`R7`, `R19`-`R24`, `R36`-`R40`; M1-M3 | Lifecycle validation and selected CI |
| `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-result.yaml` | Recorded the opt-in `--jobs 4` result, child phases, durations, output sizes, delta, and promotion decision. | Shows the measured scheduling effect and why default promotion remains deferred. | Spec `R33`-`R38`, `AC22`; M3 | Real opt-in broad-smoke run passed in 332s |
| Proposal, spec, test spec, plan, review records, and `change.yaml` | Added and maintained the lifecycle artifacts for proposal acceptance, spec approval, plan/test-spec review, milestone reviews, material finding resolution, final holistic review, and this explanation. | Keeps the planned initiative auditable and aligned with repository workflow requirements. | `AGENTS.md`, `CONSTITUTION.md`, workflow contract, active plan | Review artifact validation, change metadata validation, artifact lifecycle validation |

## Tests Added Or Changed

- `BSP-T1`: proves the canonical broad-smoke inventory and command identity are extractable from `scripts/ci.sh`.
- `BSP-T2`: proves classification reconciliation fails for stale command identity and contradictory parallel-safe metadata.
- `BSP-T3`: proves sequential-only and unsafe classifications do not become parallel-eligible.
- `BSP-T4`: proves `--jobs 1` remains strict sequential compatibility.
- `BSP-T5`: proves explicit `--jobs > 1` can overlap eligible children and obey worker bounds.
- `BSP-T6`: proves output aggregation and verbose output are grouped and canonical-order deterministic.
- `BSP-T7`: proves failure parity for single failure, multiple failures, missing classification, and worker/scheduler errors.
- `BSP-T8`: proves baseline and preservation evidence shape.
- `BSP-T9`: proves result evidence records child phases and supports the promotion decision.
- `BSP-T10`-`BSP-T12`: prove rollback, scope boundaries, network/security classification behavior, and lifecycle consistency through artifact and selected-CI checks.

## Validation Evidence Available Before Final Verify

- `python scripts/validate-broad-smoke-classification.py`
- `python scripts/test-select-validation.py -k broad_smoke`
- `python scripts/test-select-validation.py -k jobs`
- `python scripts/test-select-validation.py -k result_evidence`
- `python scripts/test-select-validation.py -k worker_crash`
- `bash -n scripts/ci.sh`
- `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 1`
- `RIGORLOOP_BROAD_SMOKE_RESULT_JSON=docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-result.yaml bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 4`
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-27-broad-smoke-safe-parallelism`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-27-broad-smoke-safe-parallelism`
- `python scripts/validate-change-metadata.py docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `bash scripts/ci.sh --mode explicit --path ...`
- `git diff --check -- ...`

The final `verify` stage still owns the final readiness verdict. Hosted CI status is not observed in this environment.

## Review Resolution Summary

Two material code-review findings were recorded and resolved:

- `CR-M1-1`: accepted and resolved by removing the undeclared PyYAML dependency from the classification validation path.
- `CR-M2-1`: accepted and resolved by registering expected child result slots and failing closed on missing or incomplete worker result metadata.

The review-resolution record is closed at `docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md`. Final holistic code-review completed clean-with-notes with no material findings at `docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-final-r1.md`.

## Alternatives Rejected

- Parallelize all broad-smoke children immediately: rejected because unclassified or shared-state checks could corrupt outputs, interleave diagnostics, or hide failures.
- Promote parallel broad-smoke to default in this slice: rejected because the single local result showed 11.24% improvement, below the 30% median target, and dominant children remain sequential-only.
- Use caching, remote cache, persistent workers, or validator composition: rejected as separate proposals with different identity, proof, and ownership risks.
- Change broad-smoke child commands to make more work parallel-safe: rejected as outside the scheduling-only first slice.
- Fail fast on the first child failure: rejected because first-slice broad-smoke must preserve all-failures diagnostic value.

## Scope Control

- The broad-smoke child set and command identity are preserved.
- Omitted `--jobs` and `--jobs 1` keep sequential broad-smoke behavior.
- Unsafe, low-confidence, stale, contradictory, network-sensitive, or sequential-only children do not run in parallel.
- Output and verbose diagnostics are captured per child and aggregated in canonical child order.
- Broad-smoke still exits nonzero for child failures, scheduler errors, and classification mismatch before parallel launch.
- Final verify, hosted CI, branch readiness, PR readiness, cache proof, persistent workers, validator composition, and selector behavior are unchanged.

## Risks And Follow-Ups

- Runtime improvement is modest because `broad_smoke.adapters.regression` and `broad_smoke.artifact_lifecycle.scoped` dominate the run and remain sequential-only.
- The timing evidence is a single local WSL2 baseline/result pair, not a three-run median. The artifacts record that limitation.
- If default promotion is reconsidered, classification should become a validator-owned or registry-owned artifact and the promotion should go through a separate acceptance state.
- Higher future gains likely require child isolation, validator composition, or cache-aware inner-loop work as separate proposals.

## Readiness

`explain-change` is complete for this initiative. The next workflow stage is `verify`.
