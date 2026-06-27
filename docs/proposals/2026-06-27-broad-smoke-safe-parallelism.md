# Broad-Smoke Safe Parallelism With Deterministic Aggregation

## Status

accepted

## Problem

Broad-smoke is the largest remaining measured validation-runtime bottleneck after selector-regression optimization.

The selector-regression runtime work records that the selector suite improved by changing the execution cost model while preserving the proof contract, but final verification still showed broad-smoke taking about 354 seconds for 11 checks. That retrospective recommends broad-smoke as the next optimization target, after consuming existing child-check classification evidence and auditing side effects, shared outputs, temp roots, ordering requirements, and failure diagnostics.

Earlier validation-runtime work also identified broad-smoke as a major boundary-validation cost. Broad-smoke previously took about 725 seconds, and the accepted direction was to classify child checks before enabling broad-smoke parallel execution.

The current opportunity is narrow:

```text
Run independent broad-smoke child checks concurrently
without changing what broad-smoke proves.
```

The risk is equally concrete. Broad-smoke is a boundary-validation surface. Unsafe parallelism can create shared temp-directory collisions, shared output corruption, ordering-dependent failures, interleaved diagnostics, flaky resource contention, masked child failures, or incorrect final broad-verification evidence.

The project already has the prerequisite direction: broad-smoke child classification should exist before parallelism, and only independent, side-effect-free checks should become candidates.

## Goals

- Reduce broad-smoke wall-clock time with measured before/after evidence.
- Use existing broad-smoke child classification evidence as the starting input.
- Record per-child broad-smoke timings before changing execution.
- Revalidate every child check for side effects, shared temp paths, shared output paths, current-working-directory assumptions, ordering constraints, resource conflicts, network or external dependency assumptions, nested parallelism risk, and diagnostic aggregation requirements.
- Enable parallel execution only for checks classified as independent.
- Keep non-independent checks sequential.
- Preserve the exact broad-smoke child set unless a separate contract changes it.
- Preserve deterministic aggregate output ordering.
- Preserve child exit behavior and broad-smoke exit behavior.
- Preserve captured diagnostics for failing children.
- Preserve `--verbose` behavior.
- Preserve final broad-verification semantics.
- Keep caching, persistent workers, remote cache, and broad validator composition out of scope.
- Keep rollback simple: one flag or configuration change should restore sequential execution.

## Non-goals

- Do not reduce broad-smoke runtime by removing child checks.
- Do not weaken broad-smoke coverage.
- Do not parallelize checks with unclassified or low-confidence safety evidence.
- Do not parallelize checks that mutate shared files or depend on shared output paths.
- Do not introduce validation-result caching.
- Do not use cache hits as final verification proof.
- Do not introduce a persistent validation worker.
- Do not compose unrelated validators into a new broad in-process runner.
- Do not change selector behavior.
- Do not change final verify ownership of branch readiness.
- Do not claim hosted CI or PR readiness from this proposal alone.
- Do not hide child output on failure.
- Do not allow nondeterministic output ordering.
- Do not make broad-smoke parallelism the default until sequential parity and failure parity are proven.

## Vision fit

fits the current vision

RigorLoop depends on validation evidence that is trustworthy, durable, and reviewable. Broad-smoke parallelism is acceptable only if it preserves the evidence contract while reducing avoidable wall-clock time.

This proposal supports that vision by applying the existing runtime-optimization principle:

```text
Make validation faster by reducing safe duplicate or independent waiting time,
not by doing less proof.
```

It would conflict with the vision if broad-smoke child coverage changes, a child failure is hidden, diagnostics become harder to use, output ordering becomes nondeterministic, final verify relies on stale or cache-only evidence, parallel execution introduces flakiness, or a low-confidence child is treated as safe to parallelize.

## Context

The prior runtime work deliberately deferred broad-smoke parallelism until broad-smoke children were classified. The follow-through test spec also required classification evidence for broad-smoke children and explicitly kept broad-smoke sequential in that earlier slice.

The selector-regression runtime work then showed the next measured bottleneck had shifted. Selector-regression dropped to about 36 seconds, selected-CI focused checks completed in about 50 seconds, and broad-smoke remained about 354 seconds. It recommends broad-smoke safe parallel execution as the next optimization proposal, with caching and validation context composition kept separate.

This proposal is that focused follow-up.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Start focused broad-smoke safe-parallelism work | in scope | Recommended Direction |
| Use existing child classification evidence | in scope | Goals, Safety Classification Contract |
| Record per-child timings first | in scope | Timing Baseline |
| Classify side effects and conflicts | in scope | Safety Classification Contract |
| Parallelize only independent checks | in scope | Recommended Direction, Parallel Execution Model |
| Preserve deterministic output and exit behavior | in scope | Output and Diagnostics Contract, Exit Behavior Contract |
| Preserve final broad-verification semantics | in scope | Final Verification Boundary |
| Avoid caching or validator-composition scope creep | in scope | Non-goals, Deferred Boundaries |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Existing broad-smoke child classification review | core to this proposal | It is the prerequisite evidence for safe parallelism. |
| Per-child timing baseline | core to this proposal | Parallelism should target actual cost, not guesswork. |
| Safety classification revalidation | core to this proposal | Existing evidence should be checked before execution changes rely on it. |
| Parallel executor for eligible children | core to this proposal | This is the runtime-speed actuator. |
| Sequential fallback for ineligible children | core to this proposal | Preserves correctness for shared-state checks. |
| Deterministic result aggregation | core to this proposal | Prevents flaky output and review confusion. |
| Failure-output parity | core to this proposal | Failure evidence should stay actionable. |
| `--jobs` / worker limit behavior | same-slice dependency | Parallelism should be bounded and controllable. |
| Dry-run execution plan | first-slice candidate | Useful for review before enabling concurrency. |
| Broad-smoke child command changes | out of scope unless required for isolation | The goal is orchestration, not rewriting child checks. |
| Cache adoption | separate proposal | Requires identity and final-proof contract. |
| Broad validator composition | separate proposal | Only after broad-smoke profiling proves it is still needed. |
| Persistent worker or daemon | out of scope | Too much complexity for this slice. |

## Options Considered

### Option 1: Keep broad-smoke sequential

This is the lowest correctness risk and preserves existing behavior, but it leaves the largest remaining measured validation-runtime cost untouched and forces contributors to wait for independent checks one after another.

Rejected as the long-term direction, but retained as rollback.

### Option 2: Parallelize all broad-smoke children immediately

This has the largest potential wall-clock reduction, but it is unsafe without side-effect and resource classification. It can create flaky failures, shared output corruption, nondeterministic diagnostics, and violation of the prior safety boundary.

Rejected.

### Option 3: Add an opt-in experimental parallel mode only

This lowers default-path risk and is useful for gathering data. The downside is that if it never becomes part of the normal path, adoption will be weak and the project may split evidence into "real broad-smoke" and "fast broad-smoke."

Acceptable as a rollout step, not the final target.

### Option 4: Parallelize only high-confidence independent children with deterministic aggregation

This targets actual broad-smoke wall-clock cost, preserves sequential behavior for risky checks, keeps failure output reviewable, and is compatible with staged rollout and rollback.

Recommended.

### Option 5: Use caching or validator composition instead

These mechanisms may reduce repeated work in other paths, but they carry different identity, contract, and final-proof risks. Cache identity and final-proof boundaries are not solved here. Validator composition should be considered only after broad-smoke profiling shows it is still the bottleneck.

Deferred.

## Recommended Direction

Introduce bounded broad-smoke parallel execution in `scripts/ci.sh`.

Use the existing broad-smoke child list and classification artifact as input, then record fresh per-child timing under sequential broad-smoke, revalidate each child's independence classification, mark only independent checks as parallel-eligible, run eligible checks concurrently with bounded workers, run ineligible checks sequentially, aggregate all results in canonical child order, and preserve the same broad-smoke pass/fail semantics.

The core invariant:

```text
Parallelism changes scheduling only.
It does not change the broad-smoke child set, child command semantics,
failure detection, output contract, or final verify meaning.
```

## Expected Behavior Changes

Before this change:

```text
bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped
-> runs all broad-smoke children sequentially
-> total wall time is approximately the sum of child durations
```

After this change:

```text
bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped
-> runs independent children concurrently
-> runs non-independent children sequentially
-> reports results in deterministic configured order
-> preserves broad-smoke pass/fail behavior and diagnostics
```

The child inventory and command identity should remain unchanged unless a separate accepted contract changes them. Execution evidence should record which children ran in the parallel phase and which remained sequential.

## Architecture Impact

| Surface | Impact |
| --- | --- |
| `scripts/ci.sh` | Add bounded parallel scheduling for eligible broad-smoke children. |
| Broad-smoke child inventory | Should be explicit and reconciled with classification evidence. |
| Broad-smoke classification artifact | Becomes implementation input and should remain current. |
| `scripts/test-select-validation.py` or CI wrapper tests | Add ordering, failure, `jobs=1`, and parallel-path tests. |
| Change-local performance evidence | Add per-child timing and before/after result evidence. |
| Final verify evidence | Still records actual broad-smoke execution and branch-readiness boundaries. |
| Cache / validation composition | No change. |
| Runtime application code | No change. |

Architecture is not expected unless implementation introduces a persistent worker, shared cache, remote cache, new cross-process protocol, or broad validator composition framework. That matches the earlier validation-runtime boundary.

## Safety Classification Contract

Each broad-smoke child should have a stable classification record. Recommended fields:

```yaml
check_id:
command:
current_order:
estimated_duration_ms:
classification:
  parallel_candidate: true | false
  confidence: high | medium | low
  reason:
side_effects:
  mutates_tracked_files: true | false
  mutates_generated_files: true | false
  writes_shared_temp: true | false
  writes_shared_output: true | false
  changes_cwd_assumptions: true | false
  relies_on_command_order: true | false
  network_sensitive: true | false
  uses_shared_cache: true | false
  starts_nested_parallelism: true | false
  cpu_intensity: low | medium | high
  io_intensity: low | medium | high
  diagnostic_order_sensitive: true | false
paths:
  read_paths:
  write_paths:
  temp_roots:
  shared_outputs:
isolation_plan:
  temp_root_strategy:
  output_capture_strategy:
  environment_strategy:
  cwd_strategy:
result:
  eligible_for_parallelism: true | false
```

A child should be parallel-eligible only when classification confidence is high, it does not mutate tracked files or shared generated outputs, it does not rely on shared temp/output paths, it has no ordering dependency or global current-working-directory side effect, it has no unsafe shared cache path, failure output can be captured per child, and its resource use will not starve sibling checks.

Low-confidence classification should mean sequential execution.

## Timing Baseline

Before any execution behavior changes, the downstream change should record a fresh sequential baseline:

```text
docs/changes/<change-id>/broad-smoke-parallelism-baseline.yaml
```

Recommended fields:

```yaml
scenario: broad-smoke-sequential-baseline
command: bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped
environment:
  os:
  shell:
  cpu_class:
  local_or_ci:
  runner:
repository_state:
  head:
  worktree_state:
children:
  - check_id:
    command:
    order:
    duration_ms:
    result:
    output_bytes:
total_duration_ms:
slowest_children:
classification_artifact:
notes:
```

Use at least three sequential runs where practical. If machine variance is high, record paired same-environment runs and limitations. Do not set a hard numeric speed target until this baseline is reviewed.

## Parallel Execution Model

The downstream spec should choose the exact model based on current child dependencies.

One likely model:

```text
1. preflight
2. parallel-eligible broad-smoke children
3. sequential-only broad-smoke children
```

If broad-smoke semantics require original order for some checks, use safe windows instead:

```text
1. run prefix sequential children until first parallel-safe window
2. run parallel-safe window
3. aggregate results in canonical order
4. continue sequential children
```

Worker behavior should add or reuse a bounded option:

```bash
bash scripts/ci.sh --mode broad-smoke --jobs <n>
```

Rules to settle downstream:

- Default worker count should be conservative.
- Minimum workers should be one.
- `--jobs 1` should be behaviorally equivalent to sequential broad-smoke.
- `--jobs` greater than eligible child count should not change semantics.
- Resource-heavy children may reserve more than one worker slot or remain sequential.
- If the existing selected-CI `--jobs` behavior can be reused safely, reuse it.

Even if checks finish out of order, output order should follow the canonical broad-smoke child order. Summaries, final status, failing child identification, captured diagnostics, and verbose output should be deterministic and grouped by child. Child output should not interleave.

## Output and Diagnostics Contract

Default success output should remain compact. If per-child summaries are already part of the current contract, they should remain in canonical order.

On failure, output should include the failing check ID, command, exit code or signal, duration, captured stdout/stderr for the failing child, rerun command, and whether the failure occurred in the parallel or sequential phase. Parallelism should not truncate diagnostics below the current failure-actionability level.

`--verbose` should display captured child output grouped and ordered by child. Parallel execution should not stream child output live in a way that interleaves logs.

## Exit Behavior Contract

The broad-smoke wrapper should preserve exit behavior:

- all children pass -> broad-smoke exits `0`;
- any required child fails -> broad-smoke exits nonzero;
- internal scheduling error -> broad-smoke exits nonzero;
- parallel worker crash -> broad-smoke exits nonzero;
- `--jobs 1` -> same result as sequential;
- missing classification -> fail before parallel execution or run sequentially, depending on downstream spec decision.

Recommended first-slice decision:

```text
If classification is missing or low-confidence, run that child sequentially.
If the child inventory itself cannot be reconciled with classification evidence,
fail before parallel execution.
```

## Final Verification Boundary

This proposal changes broad-smoke scheduling, not final verification ownership.

Final verify still uses actual commands, records real execution evidence, uses stable committed state for branch readiness, does not rely on cache-only proof, and does not infer hosted CI or PR readiness from local broad-smoke alone.

The previous validation-runtime proposal explicitly kept final verify distinct and based on actual execution evidence against stable committed state. This proposal preserves that boundary.

## Testing and Verification Strategy

The downstream spec and test spec should cover:

| Check ID | What is verified |
| --- | --- |
| `BSP-001` | Every broad-smoke child has a classification entry. |
| `BSP-002` | Every broad-smoke child has a fresh sequential timing record. |
| `BSP-003` | Low-confidence or missing classifications do not run in parallel. |
| `BSP-004` | Children with tracked-file or shared-output writes remain sequential. |
| `BSP-005` | Children with ordering constraints remain sequential or keep required order. |
| `BSP-006` | `--jobs 1` is equivalent to sequential broad-smoke. |
| `BSP-007` | Parallel-eligible children run concurrently when `--jobs > 1`. |
| `BSP-008` | Aggregate output is ordered by canonical child order, not completion order. |
| `BSP-009` | Failing child diagnostics are captured and attached to the correct child. |
| `BSP-010` | `--verbose` prints grouped child output without interleaving. |
| `BSP-011` | A child failure still makes broad-smoke fail. |
| `BSP-012` | Multiple failures are all reported, or reported according to a documented fail-fast policy. |
| `BSP-013` | Worker crash or scheduler error fails broad-smoke. |
| `BSP-014` | Parallel execution does not mutate shared temp/output paths in fixtures. |
| `BSP-015` | Broad-smoke child set is unchanged unless an approved contract changes it. |
| `BSP-016` | Final verify still records actual-run broad-smoke evidence. |
| `BSP-017` | Cache status remains non-authoritative for final proof. |
| `BSP-018` | Measured runtime improves, or a no-safe-parallelism rationale is recorded. |

Behavior-preservation evidence should be recorded in:

```text
docs/changes/<change-id>/broad-smoke-parallelism-preservation.md
```

The preservation matrix should compare baseline and revised proof for child set, child commands, exit behavior, failure diagnostics, output order, `--verbose`, `--jobs 1`, final verify, and cache boundary.

Performance evidence should be recorded in:

```text
docs/changes/<change-id>/broad-smoke-parallelism-baseline.yaml
docs/changes/<change-id>/broad-smoke-parallelism-result.yaml
```

Use paired baseline and revised runs in the same environment. Prefer the median of at least three runs when practical.

Primary success is at least a 30 percent median wall-clock reduction for broad-smoke in a comparable environment while preserving child set, exit behavior, diagnostics, and final verify semantics. A smaller measured reduction is acceptable if the first slice parallelizes only a subset of high-confidence children and records why remaining children are sequential.

If no child is safe to parallelize, record a no-safe-parallelism rationale and route the next optimization target to validator composition, child isolation, or cache adoption as a separate proposal.

## Rollout and Rollback

Rollout:

1. Reconcile existing broad-smoke classification evidence against the current `scripts/ci.sh` broad-smoke child inventory.
2. Record missing, stale, or low-confidence classifications.
3. Record per-child sequential timing without changing execution behavior.
4. Add bounded parallel scheduling behind an explicit flag or conservative default, depending on review outcome.
5. Add `--jobs 1` equivalence, deterministic aggregation, and failure-output tests.
6. Enable parallel execution by default only for high-confidence independent children, or keep it opt-in if review evidence shows risk.
7. Record before/after performance evidence and final actual-run evidence.
8. Decide whether remaining runtime warrants child isolation work, validation context composition, cache-aware inner-loop follow-up, or no further optimization.

Rollback:

- Set broad-smoke worker count to `1`.
- Disable parallel scheduling while preserving classification and timing evidence.
- Restore sequential broad-smoke execution order.
- Keep deterministic aggregation tests if they remain useful for wrapper safety.
- Do not delete broad-smoke classification evidence.
- Do not claim performance improvement after rollback.
- Preserve child-safety findings for a future isolation slice.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Parallelism creates flaky broad-smoke failures | Parallelize only high-confidence independent children; keep sequential fallback. |
| Child output interleaves | Capture output per child and aggregate in canonical order. |
| Shared temp/output paths collide | Require classification and unique temp-root proof. |
| Resource contention makes runtime worse | Record CPU/IO intensity and bound workers conservatively. |
| A child mutates tracked or generated files | Keep it sequential or block until isolated. |
| Missing classification is treated as safe | Fail or run sequential; never parallelize unknowns. |
| `--jobs 1` diverges from sequential | Add equivalence fixtures. |
| Failure output becomes less actionable | Preserve captured diagnostics and rerun commands. |
| Runtime improves by skipping checks | Preserve child inventory and command identity. |
| Final verify semantics weaken | Final verify remains actual-run evidence against stable state. |
| Broad-smoke parallelism hides selector-routing gaps | Selected-routing blockers remain independent; broad-smoke cannot erase them. |

## Deferred Boundaries

In scope for the first slice:

```text
classification reconciliation
per-child broad-smoke timing baseline
parallel-safe eligibility rules
bounded worker execution for eligible children
deterministic aggregation
failure-output parity
jobs=1 equivalence
before/after runtime evidence
behavior-preservation proof
```

Out of scope:

```text
cache adoption
remote/shared cache
persistent validation worker
broad validator composition
changing broad-smoke child commands
removing broad-smoke children
hosted CI redesign
final verify ownership changes
PR readiness changes
```

## Acceptance Criteria

| ID | Criterion |
| --- | --- |
| `AC-BSP-001` | Existing broad-smoke child classification is reviewed before execution changes. |
| `AC-BSP-002` | Every current broad-smoke child has fresh per-child timing evidence. |
| `AC-BSP-003` | Every current broad-smoke child has a safety classification. |
| `AC-BSP-004` | Only high-confidence independent children run in parallel. |
| `AC-BSP-005` | Low-confidence, shared-state, ordering-dependent, or mutating children remain sequential. |
| `AC-BSP-006` | `--jobs 1` preserves sequential broad-smoke behavior. |
| `AC-BSP-007` | Parallel output is aggregated in deterministic broad-smoke child order. |
| `AC-BSP-008` | Failing-child diagnostics remain captured and actionable. |
| `AC-BSP-009` | Broad-smoke child set and command identity are preserved. |
| `AC-BSP-010` | Broad-smoke exit behavior is preserved. |
| `AC-BSP-011` | `--verbose` behavior is preserved without interleaved logs. |
| `AC-BSP-012` | Final verify still uses actual broad-smoke execution evidence. |
| `AC-BSP-013` | No cache, remote cache, persistent worker, or validator composition is introduced. |
| `AC-BSP-014` | Runtime improvement is measured and attributed to parallel scheduling, or no-safe-parallelism evidence is recorded. |
| `AC-BSP-015` | Rollback to sequential broad-smoke is available and tested. |
| `AC-BSP-016` | The canonical broad-smoke child inventory is identified and classification is validated against it. |
| `AC-BSP-017` | A child command change without updated classification fails the classification freshness check. |
| `AC-BSP-018` | First-slice parallel mode is opt-in until `--jobs 1` parity, deterministic aggregation, and failure-output parity pass review. |
| `AC-BSP-019` | The first slice reports all required child failures rather than fail-fast. |

## Open-question resolutions

- Parallel execution starts opt-in. Default parallel broad-smoke is a later promotion after parity and failure-output evidence pass.
- Default worker count after promotion is conservative: `min(4, eligible_child_count, max(1, cpu_count - 1))`.
- Missing classification or stale command identity fails before parallel execution. Low-confidence or ineligible children run sequentially.
- Fail-fast is out of scope for the first slice; run all broad-smoke children and aggregate all failures.
- Network-sensitive checks remain sequential unless they are fully hermetic and isolated.
- If parallel broad-smoke becomes default, classification must become a validator-owned or registry-owned artifact checked against the canonical broad-smoke child inventory.

## Open Questions

### 1. Should parallel broad-smoke be opt-in first or default immediately?

Candidate answer: opt in first for one implementation slice. Promote to default only after `--jobs 1` parity, deterministic aggregation, and failure-output parity pass clean review.

### 2. What should the default worker count be?

Candidate answer: use a conservative default such as `min(4, eligible_child_count, CPU count - 1)`. Allow override through `--jobs`. Use `--jobs 1` for strict sequential compatibility.

### 3. What should happen when classification is missing?

Candidate answer: if the child inventory and classification artifact disagree, fail before parallel execution. If an individual child is classified but low-confidence or ineligible, run it sequentially.

### 4. Should fail-fast be allowed?

Candidate answer: no in the first slice. Run all required children and aggregate all failures to preserve broad-smoke diagnostic value. Consider fail-fast later only as an explicit opt-in.

### 5. Should network-sensitive checks ever run in parallel?

Candidate answer: no in the first slice unless classification proves they use independent fixtures, no credentials, no external mutable state, and deterministic local network stubs.

### 6. Should broad-smoke classification become a validator-owned artifact?

Candidate answer: yes if broad-smoke parallelism becomes default. The classification should remain current when child commands change.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-27 | Target broad-smoke after selector-regression. | Broad-smoke now dominates remaining measured wall time. | Continue optimizing selector path first. |
| 2026-06-27 | Use child classification as input. | Prior work established classification as prerequisite to concurrency. | Parallelize immediately. |
| 2026-06-27 | Record per-child timing before scheduling changes. | Runtime attribution needs fresh baseline evidence. | Compare only total broad-smoke time. |
| 2026-06-27 | Parallelize only high-confidence independent children. | Boundary validation should stay deterministic. | Parallelize all children. |
| 2026-06-27 | Preserve deterministic aggregate output. | Review evidence should stay readable and stable. | Print children in completion order. |
| 2026-06-27 | Keep caching and composition separate. | They have separate identity and ownership risks. | Bundle all speed mechanisms. |

## Next Artifacts

```text
proposal-review
spec: broad-smoke safe parallel execution
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

Architecture is not expected unless the implementation introduces a persistent worker, shared or remote cache, broad validator composition framework, or new cross-process protocol.

## Follow-on Artifacts

- Proposal review: [proposal-review-r1](../changes/2026-06-27-broad-smoke-safe-parallelism/reviews/proposal-review-r1.md)
- Review log: [review-log](../changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md)
- Spec: [Broad-Smoke Safe Parallelism](../../specs/broad-smoke-safe-parallelism.md)

## Readiness

Ready for specification.

## Core Invariant

```text
Broad-smoke may run faster only by scheduling independent checks concurrently.

It must still run the same required checks, produce deterministic aggregate
evidence, preserve failure diagnostics and exit behavior, and retain final
broad-verification semantics.
```
