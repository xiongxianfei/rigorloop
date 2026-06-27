# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: User-provided proposal-review result
Target: docs/proposals/2026-06-27-broad-smoke-safe-parallelism.md
Status: approved
Original review source: User-provided proposal-review result dated 2026-06-27.
Material findings: none
Scope-preservation result: pass
Immediate next stage: normalize proposal status to `accepted`, then write the broad-smoke safe-parallelism spec.
Automatic downstream handoff: none

## Result

- Skill: proposal-review
- Review status: approved
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md
- Review resolution: docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md#proposal-review-r1
- Open blockers: none
- Immediate next stage: normalize proposal status to `accepted`, then write the broad-smoke safe-parallelism spec

## Material Findings

No material findings.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Broad-smoke is correctly identified as the next measured bottleneck after selector-regression optimization. |
| User value | pass | Reduces final and boundary validation wait time without weakening evidence. |
| Option diversity | pass | Considers sequential status quo, all-parallel, opt-in, high-confidence-only, caching, and composition. |
| Decision rationale | pass | High-confidence-only parallelism follows from the broad-smoke risk profile. |
| Scope control | pass | Cache, persistent workers, validator composition, hosted CI redesign, and PR readiness stay out of scope. |
| Architecture awareness | pass | No service, cache, daemon, or protocol is introduced. |
| Testability | pass | `--jobs 1`, deterministic aggregation, failure-output parity, and classification freshness are testable. |
| Risk honesty | pass | Names flaky failures, interleaved output, shared temp paths, resource contention, and child omission risk. |
| Rollout realism | pass | Baseline, opt-in executor, default promotion, and final verify are sequenced. |
| Readiness for spec | pass | Open questions have safe candidate answers and can be normalized directly. |

## Scope Preservation Review

- Scope-preservation result: pass.

The review found that the proposal preserves the user's goals: start focused broad-smoke safe-parallelism work, use existing child classification evidence, record per-child timings first, classify side effects and conflicts, parallelize only independent checks, preserve deterministic output and exit behavior, preserve final broad-verification semantics, and avoid caching or validator-composition scope creep.

## Clean Review Receipt

The review approved the proposal with no material findings. It specifically found that the proposal:

- correctly selects broad-smoke as the next runtime target after selector-regression optimization;
- preserves the safety boundary that broad-smoke parallelism may change scheduling only, not check identity, output semantics, failure detection, or final broad-verification meaning;
- requires existing child-classification evidence as input, fresh per-child timings, side-effect and resource-conflict classification, deterministic aggregation, and sequential fallback for unsafe checks;
- keeps final verification, hosted CI, PR readiness, cache adoption, persistent workers, and broad validator composition outside the proposal.

## Non-Blocking Spec Directives

The downstream spec should:

- define the canonical broad-smoke child inventory owner;
- require child-command identity preservation for child ID, command, canonical order, and required/optional status;
- keep opt-in parallel mode and default enablement as separate gates;
- add failure-parity fixtures for single child failure, multiple child failures, parallel child failure, sequential-only child failure, scheduler/internal error, verbose failure output, and `--jobs 1` parity;
- treat classification freshness as a validation surface.

## Open-Question Decisions

- Parallel broad-smoke starts opt-in. Default enablement is a later promotion after `--jobs 1` parity, deterministic aggregation, failure-output parity, and classification reconciliation pass review.
- Default worker count after promotion is conservative: `min(4, eligible_child_count, max(1, cpu_count - 1))`.
- Missing classification or stale command identity fails before parallel execution. Low-confidence or explicitly ineligible classifications run sequentially.
- Fail-fast is out of scope for the first slice; run all required broad-smoke children and aggregate all failures.
- Network-sensitive checks remain sequential unless fully hermetic and isolated.
- If parallel broad-smoke becomes default, classification becomes validator-owned or registry-owned and is checked against the canonical child inventory.

## Blocking Questions

None.

## Recommended Proposal Edits

- Add open-question resolutions.
- Add acceptance criteria for canonical inventory ownership, classification freshness, opt-in-first rollout, and full failure aggregation.
- Normalize proposal status from `draft` to `accepted`.

## Recommendation

- Recommendation: approved. The proposal is ready for status normalization and the broad-smoke safe-parallelism spec. This review is isolated and does not automatically start downstream work.
