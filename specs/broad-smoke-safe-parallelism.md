# Broad-Smoke Safe Parallelism

## Status

approved

## Related proposal

- Proposal: [Broad-Smoke Safe Parallelism With Deterministic Aggregation](../docs/proposals/2026-06-27-broad-smoke-safe-parallelism.md)
- Proposal review R1: [proposal-review-r1](../docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/proposal-review-r1.md)
- Prior classification evidence: [Broad-Smoke Child Classification](../docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/broad-smoke-child-classification.md)
- Parent runtime proposal: [Preflight-First Validation Runtime Optimization](../docs/proposals/2026-06-26-preflight-first-validation-runtime-optimization.md)
- Prior selector-runtime proposal: [Selector-Regression Runtime Reduction With Coverage-Preservation Proof](../docs/proposals/2026-06-27-selector-regression-runtime-reduction.md)

## Goal and context

Broad-smoke remains the largest measured local validation-runtime bottleneck after selector-regression runtime reduction. Recorded evidence places broad-smoke at about 354 seconds for 11 checks after selector work, and earlier runtime evidence placed broad-smoke at about 725 seconds before later validation-runtime improvements.

This spec defines the observable contract for reducing broad-smoke wall-clock time by scheduling independently classified child checks concurrently. It preserves the broad-smoke child set, child commands, exit behavior, deterministic aggregate output, failure diagnostics, `--verbose` behavior, and final broad-verification meaning.

The current broad-smoke child classification evidence is a prerequisite input, not sufficient by itself to enable default parallel execution. The downstream implementation must reconcile classification against the canonical child inventory and record fresh timing and preservation evidence before relying on parallel scheduling.

## Glossary

- `broad-smoke`: the repository boundary-validation command `bash scripts/ci.sh --mode broad-smoke`, including the `--skip-diff-scoped` variant used in local evidence.
- `canonical child inventory`: the authoritative list of broad-smoke child checks consumed by `scripts/ci.sh` broad-smoke execution, including child ID, command, canonical order, and required/optional status.
- `classification artifact`: repository-owned or change-local safety metadata for each broad-smoke child, including command identity, side effects, temp/output paths, ordering constraints, resource expectations, and parallel eligibility.
- `classification freshness`: proof that a child's safety classification still matches its current child ID, command, canonical order, required/optional status, side effects, temp/output paths, and resource assumptions.
- `parallel-eligible child`: a broad-smoke child with high-confidence classification showing no shared-state, ordering, temp/output, network, nested-parallelism, or resource conflict that would make concurrent execution unsafe.
- `sequential-only child`: a broad-smoke child that is missing classification, low confidence, explicitly ineligible, mutating shared state, order-dependent, resource-heavy, network-sensitive without hermetic proof, or otherwise unsafe to run concurrently.
- `deterministic aggregation`: output and summary behavior that reports child results in canonical child order regardless of completion order.
- `first-slice parallel mode`: the initial opt-in parallel broad-smoke mode used to prove parity before default enablement.
- `default promotion`: a later state in which high-confidence independent broad-smoke children run concurrently without an explicit experimental opt-in.
- `scheduler error`: an internal orchestration failure, worker crash, output capture failure, classification reconciliation failure, or impossible scheduling state.

## Examples first

Example E1: opt-in parallel execution preserves child identity
Given the canonical broad-smoke inventory contains the current child IDs, commands, order, and required/optional status
And eligible children have fresh high-confidence classification
When a contributor runs broad-smoke in opt-in parallel mode with `--jobs 4`
Then the same required child checks run as sequential broad-smoke
And the aggregate summary is reported in canonical child order.

Example E2: `--jobs 1` behaves like sequential broad-smoke
Given broad-smoke has both parallel-eligible and sequential-only children
When a contributor runs broad-smoke with `--jobs 1`
Then the command uses strict sequential compatibility
And child result order, exit behavior, failure diagnostics, and `--verbose` grouping match sequential broad-smoke.

Example E3: missing classification blocks parallel execution
Given a current broad-smoke child exists in the canonical inventory
And the classification artifact has no matching record for that child
When broad-smoke is run in a parallel-enabled mode
Then execution fails before launching parallel children
And the diagnostic identifies the missing child classification.

Example E4: low-confidence child remains sequential
Given a current broad-smoke child has classification confidence `medium`
When broad-smoke runs with `--jobs 4`
Then that child is not scheduled in the parallel phase
And it runs sequentially or remains sequential-only according to the configured execution model.

Example E5: parallel failure diagnostics are grouped
Given two parallel-eligible children fail and one sequential-only child fails
When broad-smoke completes
Then broad-smoke exits nonzero
And reports all required child failures in canonical child order
And each failure includes child ID, command, exit code or signal, duration, captured output, rerun command, and execution phase.

Example E6: stale command identity blocks classification freshness
Given a classified broad-smoke child command changes
And the classification artifact is not updated to match the new command identity
When classification freshness validation runs
Then validation fails before parallel execution
And the child is not treated as parallel-safe by accident.

## Requirements

R1. The canonical child inventory MUST be identified before broad-smoke parallel execution is implemented.

R2. The canonical child inventory MUST include child ID, command, canonical order, and required/optional status for every broad-smoke child.

R3. The classification artifact MUST be validated against the canonical child inventory before any child is scheduled in parallel.

R4. The classification artifact MUST NOT become an independent owner of the broad-smoke child list.

R5. Broad-smoke parallelism MUST preserve the canonical child set unless a separate approved contract changes the child set.

R6. Broad-smoke parallelism MUST preserve child command identity unless a separate approved contract changes a child command.

R7. Broad-smoke parallelism MUST preserve canonical child order for aggregate summaries and grouped output.

R8. A child MUST NOT be parallel-eligible unless its classification confidence is high.

R9. A child MUST NOT be parallel-eligible when classification is missing, stale, low-confidence, contradictory, or unreconciled with the canonical child inventory.

R10. A child MUST NOT be parallel-eligible when it mutates tracked files, mutates shared generated outputs, writes shared temp paths, writes shared output paths, depends on command order, changes global current-working-directory assumptions, uses unsafe shared cache paths, or has uncaptured failure output.

R11. Network-sensitive children MUST remain sequential unless classification proves they are fully hermetic and isolated with local fixtures or stubs, no credentials, no external mutable state, no shared port conflict, no hidden environment dependency, deterministic timeout behavior, and isolated temp/output roots.

R12. Resource-heavy children MUST remain sequential or consume an explicit larger worker budget when parallel scheduling would starve sibling checks.

R13. The first-slice parallel mode MUST be opt-in until `--jobs 1` parity, deterministic aggregation, failure-output parity, and classification reconciliation pass review.

R14. Default promotion MUST be a separate acceptance state from first-slice opt-in parallel mode.

R15. After default promotion, the default worker count SHOULD be `min(4, eligible_child_count, max(1, cpu_count - 1))` unless a downstream plan records a safer repository-specific value.

R16. Broad-smoke MUST support a bounded worker count option for parallel-enabled execution.

R17. `--jobs 1` MUST provide strict sequential compatibility for broad-smoke execution.

R18. A `--jobs` value greater than the eligible child count MUST NOT change child semantics.

R19. Parallel execution MUST capture each child stdout/stderr separately.

R20. Parallel execution MUST NOT stream child output in a way that interleaves logs.

R21. Successful default output MUST remain compact and deterministic.

R22. `--verbose` output MUST include child output grouped by child and ordered by canonical child order.

R23. On failure, broad-smoke output MUST include child ID, command, exit code or signal, duration, captured stdout/stderr, rerun command, and whether the child ran in the parallel or sequential phase.

R24. The first slice MUST run all required broad-smoke children and aggregate all required child failures instead of fail-fast.

R25. A later fail-fast mode MUST require a separate approved contract before it can change first-slice behavior.

R26. Broad-smoke MUST exit `0` when all required children pass.

R27. Broad-smoke MUST exit nonzero when any required child fails.

R28. Broad-smoke MUST exit nonzero when a scheduler error occurs.

R29. Broad-smoke MUST exit nonzero before parallel execution when the canonical child inventory and classification artifact cannot be reconciled.

R30. Low-confidence or explicitly ineligible children MAY run sequentially when the inventory and classification artifact otherwise reconcile.

R31. A child command change without updated classification MUST fail classification freshness validation before parallel execution.

R32. A child marked parallel-safe with contradictory side-effect, write path, temp path, current-working-directory, network, cache, or ordering metadata MUST fail classification validation.

R33. The implementation MUST record fresh sequential per-child timing evidence before execution behavior changes.

R34. The implementation MUST record before/after broad-smoke runtime evidence under comparable environment conditions or record measurement limitations.

R35. Runtime evidence SHOULD use the median of at least three paired same-environment runs when practical.

R36. The implementation MUST record behavior-preservation evidence for child set, child commands, canonical order, required/optional status, exit behavior, failure diagnostics, output order, `--verbose`, `--jobs 1`, final verify boundary, and cache boundary.

R37. Runtime improvement MUST be attributed to scheduling independent work concurrently, not omitting checks, changing commands, weakening diagnostics, or changing final verification semantics.

R38. If no child is safe to parallelize, the change MAY close only with a no-safe-parallelism rationale that names the next optimization target.

R39. Final verify semantics MUST remain unchanged; broad-smoke parallelism MUST NOT claim branch readiness, PR readiness, hosted CI success, or cache-only proof.

R40. The implementation MUST NOT introduce validation-result caching, remote/shared caching, persistent validation workers, or broad validator composition.

R41. If parallel broad-smoke becomes default, classification MUST become a validator-owned or registry-owned artifact checked against the canonical child inventory.

R42. Classification freshness validation MUST fail when a current child has no classification, when a child command changes without classification update, when a low-confidence child is marked parallel-safe, or when classification metadata contradicts parallel eligibility.

## Inputs and outputs

Inputs include the broad-smoke command, `--skip-diff-scoped`, `--jobs`, `--verbose`, canonical child inventory, classification artifact, child commands, child IDs, canonical order, required/optional status, child stdout/stderr, child exit codes or signals, child durations, repository state, environment metadata, CPU count, temp/output path metadata, and baseline timing evidence.

Outputs include broad-smoke exit code, aggregate summary, grouped child output, failure diagnostics, rerun commands, execution phase metadata, classification validation diagnostics, scheduler diagnostics, timing baseline, runtime result evidence, and behavior-preservation evidence.

## State and invariants

- Parallelism changes scheduling only.
- The canonical child inventory owns child identity; classification metadata does not independently define the child set.
- A child is parallel-safe only when high-confidence classification and freshness validation agree.
- Unknown, stale, contradictory, low-confidence, shared-state, order-dependent, or non-hermetic network-sensitive children are not parallel-eligible.
- Aggregate output remains deterministic in canonical child order.
- Child failure diagnostics remain attached to the correct child.
- `--jobs 1` remains the strict sequential compatibility path.
- First-slice parallel mode and default promotion are separate states.
- Broad-smoke remains actual execution evidence, not cache-only proof.

## Error and boundary behavior

- Missing classification for a current child blocks parallel execution.
- Stale classification caused by child command identity changes blocks parallel execution.
- Contradictory classification metadata blocks parallel execution.
- Low-confidence or explicitly ineligible classification keeps a child sequential when inventory reconciliation otherwise succeeds.
- Scheduler errors, worker crashes, output capture failures, impossible worker budgets, and child process launch failures make broad-smoke exit nonzero.
- Multiple child failures are aggregated in canonical child order in the first slice.
- Network-sensitive checks without full hermetic proof remain sequential.
- Resource-heavy checks remain sequential or use explicit worker-budget treatment.
- Runtime variance does not invalidate the feature by itself, but evidence must record limitations and avoid unsupported speed claims.

## Compatibility and migration

Existing sequential broad-smoke behavior remains available through `--jobs 1` and rollback configuration. First-slice parallel execution is opt-in. Default promotion is a later acceptance state after parity and failure-output evidence pass review.

Existing child commands, child IDs, and canonical order remain compatible unless a separate approved contract changes them. Historical broad-smoke evidence does not need migration, but new parallelism evidence should use change-local timing and preservation artifacts.

Rollback sets broad-smoke worker count to `1` or disables parallel scheduling while preserving classification and timing evidence. Runtime improvement must not be claimed after rollback.

## Observability

Broad-smoke parallelism evidence must be reviewable from tracked or change-local artifacts.

The baseline timing evidence records scenario, command, environment, repository state, child IDs, commands, order, per-child duration, result, output size, total duration, slowest children, classification artifact, and limitations.

The result evidence records baseline and revised durations, jobs value, child phase, per-child durations, output sizes, delta, preservation results, variance, low-confidence children, and sequential-only children.

Classification validation diagnostics identify missing classifications, stale command identities, contradictory fields, low-confidence parallel-safe claims, and inventory/classification mismatches.

## Security and privacy

Broad-smoke output capture and timing evidence must not commit secrets, credentials, tokens, private keys, or machine-local debug artifacts. Network-sensitive children remain sequential unless fully hermetic and isolated. Parallel scheduling must not expose environment variables, credentials, or temporary outputs across child boundaries.

## Accessibility and UX

No graphical or web UI accessibility impact. Command-line output remains readable and deterministic. Failure diagnostics should be easier to review because child output is grouped and ordered, not interleaved by process completion.

## Performance expectations

The primary success target is at least a 30 percent median wall-clock reduction for broad-smoke in a comparable environment while preserving child set, child commands, exit behavior, diagnostics, output order, `--verbose`, `--jobs 1`, and final verify semantics.

A smaller measured reduction is acceptable when only a subset of high-confidence children is safe to parallelize and the evidence records why remaining children are sequential.

No runtime improvement is acceptable when it comes from omitted child checks, changed child commands, weaker failure diagnostics, nondeterministic output, cache-only proof, or weakened final verification semantics.

## Edge cases

EC1. A child exists in the canonical inventory with no classification.

EC2. A child command changes after classification and classification freshness is not updated.

EC3. A child is marked parallel-safe while its metadata declares a shared temp path.

EC4. A low-confidence child is present while broad-smoke runs with `--jobs 4`.

EC5. Two parallel-eligible children fail in different completion order from canonical order.

EC6. One parallel-eligible child and one sequential-only child fail in the same run.

EC7. A scheduler worker crashes after launching one child.

EC8. `--verbose` is used while several parallel children produce output.

EC9. `--jobs` exceeds the eligible child count.

EC10. CPU count is one or unavailable.

EC11. A network-sensitive child uses local hermetic fixtures but shares a port with another child.

EC12. The measured parallel run is slower than sequential because of resource contention.

EC13. No child is safe to parallelize after classification reconciliation.

EC14. A contributor requests fail-fast during the first slice.

## Non-goals

- Do not remove broad-smoke child checks.
- Do not change broad-smoke child commands under the umbrella of scheduling.
- Do not weaken broad-smoke coverage.
- Do not make unclassified, stale, low-confidence, contradictory, shared-state, or order-dependent checks parallel-safe.
- Do not introduce validation-result caching, remote/shared caching, or cache-hit final proof.
- Do not introduce persistent validation workers.
- Do not compose broad validators into one in-process runner.
- Do not change selector behavior.
- Do not change final verify, hosted CI, branch readiness, PR readiness, or release readiness semantics.
- Do not add first-slice fail-fast behavior.
- Do not stream interleaved child logs.
- Do not claim runtime improvement when preservation evidence fails or after rollback.

## Acceptance criteria

AC1. The canonical broad-smoke child inventory is identified with child ID, command, canonical order, and required/optional status.

AC2. Existing broad-smoke child classification evidence is reconciled against the current canonical inventory.

AC3. Every current broad-smoke child has fresh per-child sequential timing evidence before execution behavior changes.

AC4. Every current broad-smoke child has a safety classification.

AC5. Classification freshness validation fails for missing classifications, stale command identity, low-confidence parallel-safe claims, and contradictory parallel-safe metadata.

AC6. Only high-confidence independent children run in parallel.

AC7. Low-confidence, shared-state, ordering-dependent, mutating, stale, contradictory, or non-hermetic network-sensitive children remain sequential or block parallel execution as specified.

AC8. First-slice parallel mode is opt-in until `--jobs 1` parity, deterministic aggregation, failure-output parity, and classification reconciliation pass review.

AC9. Default promotion is recorded as a separate acceptance state from opt-in parallel mode.

AC10. `--jobs 1` preserves sequential broad-smoke behavior.

AC11. `--jobs` greater than eligible child count has no semantic effect.

AC12. Parallel output is aggregated in deterministic broad-smoke child order.

AC13. Successful default output remains compact and deterministic.

AC14. `--verbose` output is grouped by child and ordered by canonical child order.

AC15. Single-child failure diagnostics remain captured and actionable.

AC16. Multiple child failures are all reported in the first slice.

AC17. Parallel-child failure, sequential-only-child failure, scheduler/internal error, verbose failure output, and `--jobs 1` parity are covered by tests or proof fixtures.

AC18. Broad-smoke child set, child commands, canonical order, and required/optional status are preserved or a separate approved contract is cited.

AC19. Broad-smoke exit behavior is preserved.

AC20. Final verify still uses actual broad-smoke execution evidence and does not rely on cache-only proof.

AC21. No cache, remote cache, persistent worker, broad validator composition, selector behavior, hosted CI, PR readiness, branch readiness, or final verify behavior change is introduced.

AC22. Runtime improvement is measured and attributed to parallel scheduling, or no-safe-parallelism evidence is recorded.

AC23. Rollback to sequential broad-smoke is available and tested.

AC24. If parallel broad-smoke becomes default, classification is validator-owned or registry-owned and checked against the canonical child inventory.

## Open questions

None. Proposal-review resolved the proposal open questions for specification.

## Next artifacts

```text
spec-review
test-spec
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

Architecture is not expected unless implementation introduces a persistent worker, shared or remote cache, broad validator composition framework, or new cross-process protocol.

## Follow-on artifacts

- Spec review: `docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/spec-review-r1.md`
- Plan: `docs/plans/2026-06-27-broad-smoke-safe-parallelism.md`
- Plan review: `docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/plan-review-r1.md`
- Test spec: `specs/broad-smoke-safe-parallelism.test.md`

## Readiness

Approved for planning and test-spec authoring.
