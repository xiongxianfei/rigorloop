# Broad-Smoke Safe Parallelism Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Change ID: 2026-06-27-broad-smoke-safe-parallelism
- Owner: agent
- Start date: 2026-06-27
- Last updated: 2026-06-27
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

This plan sequences the accepted broad-smoke safe parallelism contract into reviewable implementation slices. The goal is to reduce broad-smoke wall-clock time by scheduling only independently classified child checks concurrently while preserving child identity, command identity, deterministic aggregate output, failure diagnostics, `--verbose`, `--jobs 1`, rollback, and final broad-verification semantics.

## Source artifacts

- Proposal: [Broad-Smoke Safe Parallelism With Deterministic Aggregation](../proposals/2026-06-27-broad-smoke-safe-parallelism.md)
- Spec: [Broad-Smoke Safe Parallelism](../../specs/broad-smoke-safe-parallelism.md)
- Prior classification evidence: [Broad-Smoke Child Classification](../changes/2026-06-26-preflight-first-validation-runtime-optimization/broad-smoke-child-classification.md)
- Architecture: not-required; architecture assessment recorded in [change.yaml](../changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml)
- Test spec: [Broad-Smoke Safe Parallelism Test Spec](../../specs/broad-smoke-safe-parallelism.test.md)
- Change metadata: [change.yaml](../changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml)
- Review log: [review-log.md](../changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md)
- Proposal reviews: [proposal-review-r1](../changes/2026-06-27-broad-smoke-safe-parallelism/reviews/proposal-review-r1.md), [proposal-review-r2](../changes/2026-06-27-broad-smoke-safe-parallelism/reviews/proposal-review-r2.md)
- Spec review: [spec-review-r1](../changes/2026-06-27-broad-smoke-safe-parallelism/reviews/spec-review-r1.md)
- Plan review: [plan-review-r1](../changes/2026-06-27-broad-smoke-safe-parallelism/reviews/plan-review-r1.md)
- Test-spec review: [test-spec-review-r1](../changes/2026-06-27-broad-smoke-safe-parallelism/reviews/test-spec-review-r1.md)

## Upstream status settlement

- Upstream artifact: `specs/broad-smoke-safe-parallelism.md`
- Review evidence: `docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/spec-review-r1.md`; review log has no open findings.
- Previous status: draft
- New status: approved
- Settlement result: updated
- Settlement blocker: none

## Context and orientation

The implementation surface is the repository validation wrapper and its regression tests:

- `scripts/ci.sh` owns broad-smoke execution, `run_broad_smoke`, `run_check`, output capture, `--jobs`, `--verbose`, wrapper exit behavior, and selected-check parallel infrastructure already used outside broad-smoke.
- `scripts/test-select-validation.py` owns wrapper structural tests, broad-smoke command identity assertions, selected-CI concurrency fixtures, and likely new broad-smoke parity fixtures.
- `scripts/validation_selection.py` owns selected-check catalog metadata and existing selected-check parallel safety, but broad-smoke child classification must not become an independent child-list owner.
- `docs/changes/2026-06-27-broad-smoke-safe-parallelism/` owns classification reconciliation, timing baseline/result, preservation proof, review, and validation evidence.

Current code evidence shows `scripts/ci.sh` accepts `--jobs`, selected-check execution already has bounded parallel-safe chunks, and `run_broad_smoke` still calls `run_check` sequentially for broad-smoke children. This plan should reuse existing wrapper patterns where safe, but it must not make unclassified broad-smoke children parallel-safe by default.

## Non-goals

- Do not remove broad-smoke child checks.
- Do not change broad-smoke child commands under the umbrella of scheduling.
- Do not weaken broad-smoke coverage, exit behavior, output ordering, diagnostics, or `--verbose`.
- Do not introduce validation-result caching, remote/shared caching, or cache-hit final proof.
- Do not introduce persistent validation workers.
- Do not compose broad validators into one in-process runner.
- Do not change selector behavior.
- Do not change final verify, hosted CI, branch readiness, PR readiness, or release readiness semantics.
- Do not add first-slice fail-fast behavior.

## Requirements covered

- `R1`-`R7`: M1 canonical inventory and M2/M3 identity preservation.
- `R8`-`R12`: M1 classification validation and M2 scheduling eligibility.
- `R13`-`R18`: M2 opt-in worker behavior, `--jobs 1`, and bounded jobs semantics; M3 default-promotion decision.
- `R19`-`R24`: M2 output capture, deterministic aggregation, verbose grouping, failure diagnostics, and all-failures aggregation.
- `R25`: deferred; fail-fast remains out of scope unless a separate contract is approved.
- `R26`-`R32`: M2 exit behavior, scheduler errors, classification mismatch, stale identity, and contradictory metadata.
- `R33`-`R38`: M1 baseline timing, M3 result timing, preservation evidence, attribution, and no-safe-parallelism closeout.
- `R39`-`R42`: M1 through M3 final-verify boundary, cache/composition exclusion, validator-owned classification requirement for default promotion, and freshness validation.
- `AC1`-`AC24`: covered across M1 through M3 and downstream closeout.

## Current Handoff Summary

- Current milestone: final holistic cross-milestone review
- Current milestone state: closed
- Latest review evidence: docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-final-r1.md
- Last reviewed milestone: final holistic cross-milestone review
- Review status: approved; stage=code-review; round=r1
- Remaining in-scope implementation milestones: none
- Next stage: explain-change
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: lifecycle-gates-open, explain-change-pending, verify-pending, pr-handoff-pending — M1, M2, M3, review-resolution, and final holistic code-review are closed; explain-change, verify, and PR handoff have not completed.

## Milestones

### M1. Inventory, Classification Freshness, and Timing Baseline

- Milestone state: closed
- Goal: Establish the canonical broad-smoke child inventory, reconcile existing classification evidence, add freshness validation, and record sequential per-child timing before behavior changes.
- Requirements: `R1`-`R12`, `R31`-`R36`, `R41`-`R42`, `AC1`-`AC7`, `AC18`, `AC22`
- Files/components likely touched:
  - `scripts/ci.sh`
  - `scripts/test-select-validation.py`
  - `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-baseline.yaml`
  - `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md`
  - `docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml`
- Dependencies:
  - Plan-review approves this plan.
  - Test spec maps classification freshness, child identity, and baseline evidence obligations before implementation.
- Tests to add/update:
  - Structural test that extracts the canonical broad-smoke child inventory from the wrapper-owned source.
  - Classification reconciliation tests for missing child, stale command identity, low-confidence parallel-safe claim, contradictory metadata, and valid sequential-only classification.
  - Baseline evidence shape check where practical.
- Implementation steps:
  - Identify the authoritative broad-smoke child inventory in the wrapper or a wrapper-consumed helper.
  - Reconcile current child IDs, commands, canonical order, and required/optional status against existing classification evidence.
  - Add or update validation logic so classification freshness failures are explicit before parallel execution.
  - Record sequential per-child timing baseline using at least three runs when practical, or record variance and limitations.
  - Record initial behavior-preservation evidence for child set, command identity, order, output, failure diagnostics, `--verbose`, `--jobs 1`, final verify boundary, and cache boundary.
- Validation commands:
  - `python scripts/test-select-validation.py -k broad_smoke`
  - `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 1`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/broad-smoke-safe-parallelism.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml`
  - `git diff --check -- scripts docs/changes/2026-06-27-broad-smoke-safe-parallelism specs/broad-smoke-safe-parallelism.md docs/plans/2026-06-27-broad-smoke-safe-parallelism.md docs/plan.md`
- Expected observable result: Child inventory and classification freshness are explicit, stale or unsafe classifications fail closed, and baseline evidence exists before scheduling changes.
- Commit message: `M1: record broad-smoke inventory and baseline`
- Milestone closeout:
  - targeted validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Existing classification evidence may be too coarse for default promotion.
  - Per-child timing may be noisy on local hardware.
- Rollback/recovery:
  - Keep useful classification findings; revert only behavior-affecting validation changes if they over-block.
  - Record no-safe-parallelism if no child can be classified safely.

### M2. Opt-In Parallel Executor and Deterministic Aggregation

- Milestone state: closed
- Goal: Add opt-in bounded broad-smoke parallel scheduling for high-confidence eligible children while preserving sequential fallback, `--jobs 1` parity, deterministic aggregation, and failure-output parity.
- Requirements: `R3`-`R32`, `R36`-`R40`, `AC5`-`AC21`, `AC23`
- Files/components likely touched:
  - `scripts/ci.sh`
  - `scripts/test-select-validation.py`
  - `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md`
  - `docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml`
- Dependencies:
  - M1 classification freshness and baseline evidence complete.
  - Test spec defines opt-in trigger behavior and failure fixtures.
- Tests to add/update:
  - `--jobs 1` sequential parity.
  - Explicit `--jobs > 1` broad-smoke opt-in path.
  - Parallel-eligible children run concurrently when safe.
  - Low-confidence and sequential-only children do not run in parallel.
  - Deterministic aggregate output ordered by canonical child order.
  - Single failure, multiple failures, parallel child failure, sequential-only child failure, scheduler/internal error, and verbose failure output.
  - No interleaved child logs.
- Implementation steps:
  - Add broad-smoke scheduling that runs only high-confidence eligible children concurrently.
  - Keep broad-smoke sequential when `--jobs 1` is used.
  - Treat omitted broad-smoke worker count as sequential until default-promotion evidence is approved.
  - Capture child output separately and aggregate summaries, verbose output, and failures in canonical order.
  - Make classification mismatch, stale command identity, contradictory metadata, worker crash, and scheduler errors fail nonzero.
  - Record preservation evidence for all affected behavior surfaces.
- Validation commands:
  - `python scripts/test-select-validation.py -k broad_smoke`
  - `python scripts/test-select-validation.py -k jobs`
  - `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 1`
  - `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml`
- Expected observable result: First-slice parallel broad-smoke is available only through explicit opt-in, preserves all required diagnostics and exit behavior, and leaves unsafe children sequential.
- Commit message: `M2: add opt-in broad-smoke parallel scheduling`
- Milestone closeout:
  - targeted validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Parallel output could become nondeterministic.
  - A child classified as safe may still contend for CPU, IO, ports, or temp roots.
  - Scheduler failures could mask child failures.
- Rollback/recovery:
  - Force broad-smoke `--jobs 1` behavior.
  - Disable opt-in parallel scheduling while keeping classification and aggregation tests that remain useful.
  - Reclassify risky children as sequential-only.

### M3. Performance Result, Default-Promotion Decision, and Closeout Evidence

- Milestone state: closed
- Goal: Record before/after runtime evidence, decide whether default promotion is justified, and close with measured scheduling improvement or no-safe-parallelism evidence.
- Requirements: `R13`-`R18`, `R33`-`R42`, `AC8`-`AC24`
- Files/components likely touched:
  - `scripts/ci.sh`
  - `scripts/test-select-validation.py`
  - `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-result.yaml`
  - `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md`
  - `docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml`
  - `docs/plans/2026-06-27-broad-smoke-safe-parallelism.md`
- Dependencies:
  - M2 opt-in executor complete and reviewed.
  - Paired baseline and revised timing can be compared, or limitations are recorded.
- Tests to add/update:
  - Default-promotion behavior when approved, or explicit opt-in retention when default promotion is not justified.
  - Conservative default worker calculation after promotion, if promoted.
  - Regression that rollback to sequential broad-smoke remains available and tested.
  - Evidence checks for runtime result and preservation artifact shape where practical.
- Implementation steps:
  - Run paired opt-in broad-smoke timing in the same environment as the baseline where practical.
  - Record `broad-smoke-parallelism-result.yaml` with jobs, phases, child durations, output sizes, delta, preservation results, variance, low-confidence children, and sequential-only children.
  - Decide whether to promote high-confidence independent children to default parallel execution.
  - If promoting, ensure classification is validator-owned or registry-owned and checked against canonical inventory.
  - If not promoting, keep opt-in behavior and record the reason.
  - If no child is safe to parallelize, record no-safe-parallelism and route follow-up to child isolation, validator composition, or cache adoption as a separate proposal.
- Validation commands:
  - `python scripts/test-select-validation.py -k broad_smoke`
  - `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 1`
  - `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 4`
  - `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-baseline.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-result.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-27-broad-smoke-safe-parallelism`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/broad-smoke-safe-parallelism.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml`
  - `git diff --check -- scripts docs/changes/2026-06-27-broad-smoke-safe-parallelism specs/broad-smoke-safe-parallelism.md docs/plans/2026-06-27-broad-smoke-safe-parallelism.md docs/plan.md`
- Expected observable result: Broad-smoke has measured opt-in parallel performance evidence and either a justified default-promotion change or an explicit decision to remain opt-in/no-safe-parallelism.
- Commit message: `M3: record broad-smoke parallelism result`
- Milestone closeout:
  - targeted validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Runtime improvement may be smaller than the target because few children are safe to parallelize.
  - Default promotion could be premature if classification ownership is not durable.
  - Broad-smoke may remain dominated by one sequential-only child.
- Rollback/recovery:
  - Keep opt-in only or force `--jobs 1`.
  - Preserve timing and classification evidence for child isolation or future composition work.
  - Record the next optimization target without weakening broad-smoke proof.

### final holistic cross-milestone review

- Milestone state: closed
- Goal: Review the complete M1-M3 implementation and evidence set before entering explain-change and verify.
- Requirements: all in-scope requirements `R1`-`R42` and `AC1`-`AC24`.
- Files/components likely touched: none unless review finds a blocking issue.
- Dependencies:
  - M1, M2, and M3 implementation milestones are closed.
  - Review-resolution is closed with no open findings.
- Tests to add/update: none expected; this is a review gate over the complete implementation and evidence surface.
- Validation commands:
  - Review the complete branch diff and recorded validation evidence.
  - Run lifecycle and review artifact validation after recording the final holistic review.
- Expected observable result: A clean final holistic code-review record or recorded material findings before explain-change.
- Commit message: `final review: record broad-smoke holistic code review`
- Milestone closeout:
  - final holistic code-review recorded
  - no open material findings
  - handoff to explain-change
- Risks:
  - Cross-milestone evidence could drift even when individual milestones passed.
- Rollback/recovery:
  - Route any material finding through review-resolution before explain-change or verify.

## Validation plan

- `python scripts/validate-review-artifacts.py docs/changes/2026-06-27-broad-smoke-safe-parallelism`: review record structure.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-27-broad-smoke-safe-parallelism`: review closeout consistency.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml`: change metadata validity.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-27-broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml`: lifecycle artifact consistency.
- `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-06-27-broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml`: selected CI over authoring artifacts.
- `git diff --check -- docs/proposals/2026-06-27-broad-smoke-safe-parallelism.md specs/broad-smoke-safe-parallelism.md docs/plans/2026-06-27-broad-smoke-safe-parallelism.md docs/plan.md docs/changes/2026-06-27-broad-smoke-safe-parallelism`: patch hygiene.

## Risks and recovery

- Risk: broad-smoke child classification is stale or too coarse.
  - Recovery: fail closed, keep children sequential, and update classification before scheduling.
- Risk: parallel execution creates nondeterministic output.
  - Recovery: aggregate captured output by canonical child order and keep live streaming disabled.
- Risk: worker crashes or scheduler errors hide child failures.
  - Recovery: treat scheduler errors as broad-smoke failures and report already captured child diagnostics.
- Risk: resource contention makes broad-smoke slower.
  - Recovery: reduce worker count, mark resource-heavy children sequential, or keep opt-in only.
- Risk: no child is safely parallelizable.
  - Recovery: record no-safe-parallelism and route follow-up to child isolation, validator composition, or cache adoption as separate work.

## Dependencies

- Accepted proposal and approved spec.
- Clean recorded spec-review.
- Architecture assessment recorded as `architecture-not-required`.
- Plan-review approval before test-spec.
- Test-spec drafted and test-spec-review approved before implementation.
- Broad-smoke baseline and classification evidence before scheduling behavior changes.

## Progress

- 2026-06-27: Proposal accepted, proposal-review R1/R2 recorded, spec approved, architecture assessment recorded as not required, and plan authored for plan-review.
- 2026-06-27: Plan-review R1 approved the plan with no material findings; test spec drafted for test-spec-review.
- 2026-06-27: Test-spec-review R1 approved the proof map with no material findings and allowed implementation handoff.
- 2026-06-27: M1 implemented classification freshness validation, change-local classification evidence, sequential baseline timing, and preservation evidence; M1 is ready for code-review.
- 2026-06-27: Code-review M1 R1 requested changes for `CR-M1-1`, an undeclared PyYAML dependency in the M1 validation path.
- 2026-06-27: Resolved `CR-M1-1` by removing the PyYAML dependency and parsing JSON-compatible YAML artifacts with the Python standard library.
- 2026-06-27: Code-review M1 R2 completed clean-with-notes, closed M1, and handed off to M2 implementation.
- 2026-06-27: M2 implemented explicit `--jobs > 1` broad-smoke opt-in scheduling with classification preflight, bounded parallel windows, sequential fallback for ineligible children, per-child output capture, deterministic aggregation, all-failure reporting, and controlled missing-classification diagnostics. M2 is ready for code-review.
- 2026-06-27: Code-review M2 R1 requested changes for `CR-M2-1`, a scheduler-error gap where a missing worker result could be skipped and produce incomplete broad-smoke evidence.
- 2026-06-27: Resolved `CR-M2-1` by registering expected child result slots before launch, failing closed on missing or incomplete result metadata, and adding a worker-crash regression.
- 2026-06-27: Code-review M2 R2 completed clean-with-notes, closed M2, and handed off to M3 implementation.
- 2026-06-27: M3 recorded opt-in broad-smoke runtime evidence from `--jobs 4`: 332s total, 42061ms / 11.24% faster than the M1 single-run baseline. Default promotion remains deferred; first-slice parallelism stays opt-in.
- 2026-06-27: Code-review M3 R1 completed clean-with-notes and closed M3; next stage is final holistic cross-milestone code-review.
- 2026-06-27: Final holistic code-review completed clean-with-notes across the complete M1-M3 diff; next stage is explain-change.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-27 | Use three implementation milestones. | Baseline/classification, opt-in scheduling, and promotion/evidence have different risk and review surfaces. | Bundle all work in one implementation slice. |
| 2026-06-27 | Record architecture assessment as not required. | The work stays within existing validation wrapper behavior and does not introduce a persistent worker, cache, composition framework, new protocol, persistence, deployment, or trust boundary. | Produce an architecture package for wrapper-only scheduling. |
| 2026-06-27 | Keep first-slice broad-smoke parallelism opt-in. | The spec requires parity and failure-output evidence before default promotion. | Enable default parallel broad-smoke immediately. |
| 2026-06-27 | Keep broad-smoke runtime sequential in M1. | M1 records freshness and timing evidence before scheduling behavior changes. | Introduce scheduling changes before baseline evidence. |
| 2026-06-27 | Keep omitted broad-smoke `--jobs` sequential in M2. | The spec separates first-slice opt-in parallelism from default promotion, so default worker calculation remains selected-CI-only until M3 decision evidence exists. | Treat computed default jobs as broad-smoke opt-in. |
| 2026-06-27 | Do not promote broad-smoke parallelism to default in M3. | The measured single-run reduction is 11.24%, below the 30% median target, and dominant children remain sequential-only. | Enable default parallel broad-smoke immediately. |

## Surprises and discoveries

- Current `scripts/ci.sh` already supports `--jobs` and selected-check parallel-safe chunks, but broad-smoke still calls `run_check` sequentially.
- M1 measured `broad_smoke.adapters.regression` at `173108ms` and `broad_smoke.artifact_lifecycle.scoped` at `149434ms`; these dominate the sequential baseline.
- M2 can prove broad-smoke child overlap with fixture child scripts and active counters without running expensive real child commands in parallel before M3 runtime evidence.
- M3 opt-in runtime improved wall time but remained dominated by sequential-only adapter regression and scoped artifact-lifecycle checks.

## Validation notes

- Plan-review validation passed before test-spec authoring.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml` passed after test-spec authoring.
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-27-broad-smoke-safe-parallelism` passed after test-spec authoring.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-27-broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.test.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/proposal-review-r1.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/proposal-review-r2.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/spec-review-r1.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/plan-review-r1.md` passed after test-spec authoring.
- `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-06-27-broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.test.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/proposal-review-r1.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/proposal-review-r2.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/spec-review-r1.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/plan-review-r1.md` passed after staging the new authoritative test spec.
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-27-broad-smoke-safe-parallelism` passed after test-spec-review.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-27-broad-smoke-safe-parallelism` passed after test-spec-review.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-27-broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.test.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/proposal-review-r1.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/proposal-review-r2.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/spec-review-r1.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/plan-review-r1.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/test-spec-review-r1.md` passed after test-spec-review.
- `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-06-27-broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.test.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/proposal-review-r1.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/proposal-review-r2.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/spec-review-r1.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/plan-review-r1.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/test-spec-review-r1.md` passed after test-spec-review.
- `python scripts/validate-broad-smoke-classification.py` passed for M1.
- `python scripts/test-select-validation.py -k broad_smoke` passed for M1 (`17 passed in 3.90s`).
- Sequential per-child timing run passed for M1 and recorded `374061ms` total child time in `broad-smoke-parallelism-baseline.yaml`.
- `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 1` passed for M1 (`[PASS] broad-smoke: 11 checks passed in 365s`).
- `bash scripts/ci.sh --mode explicit --path scripts/validate-broad-smoke-classification.py --path scripts/test-select-validation.py --path scripts/validation_selection.py --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-child-classification.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-baseline.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path specs/broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.test.md` passed for M1 selected CI.
- `python scripts/validate-broad-smoke-classification.py` passed after `CR-M1-1` resolution.
- `python scripts/test-select-validation.py -k broad_smoke` passed after `CR-M1-1` resolution (`17 passed in 3.85s`).
- `python scripts/test-select-validation.py -k registered_change_evidence` passed after `CR-M1-1` resolution (`5 passed in 0.14s`).
- `rg -n "^import yaml|from yaml|yaml\\.safe" scripts docs/changes/2026-06-27-broad-smoke-safe-parallelism` returned no matches after `CR-M1-1` resolution.
- `bash scripts/ci.sh --mode explicit --path scripts/validate-broad-smoke-classification.py --path scripts/test-select-validation.py --path scripts/validation_selection.py --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-child-classification.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-baseline.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m1-r1.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path specs/broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.test.md` passed after `CR-M1-1` resolution.
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-27-broad-smoke-safe-parallelism` passed after code-review M1 R2.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-27-broad-smoke-safe-parallelism` passed after code-review M1 R2.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml` passed after code-review M1 R2.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-27-broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.test.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/proposal-review-r1.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/proposal-review-r2.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/spec-review-r1.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/plan-review-r1.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/test-spec-review-r1.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m1-r1.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m1-r2.md` passed after code-review M1 R2.
- `git diff --check -- scripts docs/changes/2026-06-27-broad-smoke-safe-parallelism specs/broad-smoke-safe-parallelism.md specs/broad-smoke-safe-parallelism.test.md docs/plans/2026-06-27-broad-smoke-safe-parallelism.md docs/plan.md` passed after code-review M1 R2.
- `bash scripts/ci.sh --mode explicit --path scripts/validate-broad-smoke-classification.py --path scripts/test-select-validation.py --path scripts/validation_selection.py --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-child-classification.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-baseline.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m1-r1.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m1-r2.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path specs/broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.test.md` passed after code-review M1 R2.
- `python scripts/validate-broad-smoke-classification.py` passed for M2.
- `python scripts/test-select-validation.py -k broad_smoke` passed for M2 (`23 passed in 7.02s`).
- `python scripts/test-select-validation.py -k jobs` passed for M2 (`5 passed in 3.93s`).
- `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 1` passed for M2 rollback compatibility (`[PASS] broad-smoke: 11 checks passed in 352s`).
- `bash -n scripts/ci.sh` passed for M2.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml` passed for M2.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.test.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md` passed for M2.
- `git diff --check -- scripts docs/changes/2026-06-27-broad-smoke-safe-parallelism specs/broad-smoke-safe-parallelism.md specs/broad-smoke-safe-parallelism.test.md docs/plans/2026-06-27-broad-smoke-safe-parallelism.md docs/plan.md` passed for M2.
- `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path scripts/validate-broad-smoke-classification.py --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path specs/broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.test.md` passed for M2 selected CI.
- `python scripts/test-select-validation.py -k worker_crash` passed after `CR-M2-1` resolution (`1 passed in 0.23s`).
- `python scripts/test-select-validation.py -k broad_smoke` passed after `CR-M2-1` resolution (`24 passed in 7.37s`).
- `python scripts/test-select-validation.py -k jobs` passed after `CR-M2-1` resolution (`5 passed in 3.94s`).
- `bash -n scripts/ci.sh` passed after `CR-M2-1` resolution.
- `python scripts/validate-broad-smoke-classification.py` passed after `CR-M2-1` resolution.
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-27-broad-smoke-safe-parallelism` passed after `CR-M2-1` resolution.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-27-broad-smoke-safe-parallelism` passed after `CR-M2-1` resolution.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml` passed after `CR-M2-1` resolution.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m2-r1.md` passed after `CR-M2-1` resolution.
- `git diff --check -- scripts docs/changes/2026-06-27-broad-smoke-safe-parallelism docs/plans/2026-06-27-broad-smoke-safe-parallelism.md docs/plan.md` passed after `CR-M2-1` resolution.
- `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path scripts/validate-broad-smoke-classification.py --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m2-r1.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md` passed after `CR-M2-1` resolution.
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-27-broad-smoke-safe-parallelism` passed after code-review M2 R2.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-27-broad-smoke-safe-parallelism` passed after code-review M2 R2.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml` passed after code-review M2 R2.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m2-r2.md` passed after code-review M2 R2.
- `bash scripts/ci.sh --mode explicit --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m2-r2.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md` passed after code-review M2 R2.
- `python scripts/test-select-validation.py -k result_evidence` failed before M3 implementation because no result artifact was written.
- `python scripts/test-select-validation.py -k result_evidence` passed after M3 result writer implementation (`1 passed in 0.24s`).
- `python scripts/test-select-validation.py -k broad_smoke` passed for M3 (`25 passed in 7.53s`).
- `python scripts/test-select-validation.py -k jobs` passed for M3 (`5 passed in 3.95s`).
- `bash -n scripts/ci.sh` passed for M3.
- `RIGORLOOP_BROAD_SMOKE_RESULT_JSON=docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-result.yaml bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 4` passed for M3 (`[PASS] broad-smoke: 11 checks passed in 332s`).
- `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 1` passed for M3 rollback compatibility (`[PASS] broad-smoke: 11 checks passed in 353s`).
- `python scripts/test-select-validation.py -k broad_smoke` passed after result sanitization (`25 passed in 7.52s`).
- `python scripts/test-select-validation.py -k jobs` passed after result sanitization (`5 passed in 3.97s`).
- `python -m json.tool docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-result.yaml >/dev/null` passed for M3.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml` passed for M3.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.test.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-baseline.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-result.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md` passed for M3.
- `git diff --check -- scripts docs/changes/2026-06-27-broad-smoke-safe-parallelism specs/broad-smoke-safe-parallelism.md specs/broad-smoke-safe-parallelism.test.md docs/plans/2026-06-27-broad-smoke-safe-parallelism.md docs/plan.md` passed for M3.
- `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-baseline.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-result.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path specs/broad-smoke-safe-parallelism.md --path specs/broad-smoke-safe-parallelism.test.md` passed for M3 selected CI.
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-27-broad-smoke-safe-parallelism` passed after code-review M3 R1.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-27-broad-smoke-safe-parallelism` passed after code-review M3 R1.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml` passed after code-review M3 R1.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m3-r1.md` passed after code-review M3 R1.
- `bash scripts/ci.sh --mode explicit --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m3-r1.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md` passed after code-review M3 R1.
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-27-broad-smoke-safe-parallelism` passed after final holistic code-review.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-27-broad-smoke-safe-parallelism` passed after final holistic code-review.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml` passed after final holistic code-review.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-final-r1.md` passed after final holistic code-review.
- `bash scripts/ci.sh --mode explicit --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md --path docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-final-r1.md --path docs/plans/2026-06-27-broad-smoke-safe-parallelism.md --path docs/plan.md` passed after final holistic code-review.

## Outcome and retrospective

- Pending. Keep this section final-only while the plan is active.

## Readiness

- See `Current Handoff Summary`.
