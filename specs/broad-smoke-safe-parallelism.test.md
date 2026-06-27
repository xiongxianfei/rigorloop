# Broad-Smoke Safe Parallelism Test Spec

## Status

draft

## Related spec and plan

- Spec: [Broad-Smoke Safe Parallelism](broad-smoke-safe-parallelism.md)
- Spec review: [spec-review-r1](../docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/spec-review-r1.md)
- Plan: [Broad-Smoke Safe Parallelism Plan](../docs/plans/2026-06-27-broad-smoke-safe-parallelism.md)
- Plan review: [plan-review-r1](../docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/plan-review-r1.md)
- Architecture/ADRs: not required; assessment recorded in [change.yaml](../docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml)

## Testing strategy

Use unit and integration tests around the validation wrapper and classification
helpers before changing broad-smoke scheduling. The first milestone proves child
inventory ownership, classification freshness, fail-closed mismatch behavior,
and timing artifact shape. The second milestone proves opt-in scheduling,
`--jobs 1` parity, deterministic aggregation, grouped diagnostics, and failure
parity with wrapper fixtures. The third milestone proves runtime evidence,
rollback, default-promotion decision behavior, and scope boundaries.

End-to-end proof uses the repository wrapper commands named in the plan:
`bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 1`,
`bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 4`, and
selected explicit validation over changed files and evidence artifacts. Manual
proof is limited to performance-environment notes and review of runtime
evidence where automation cannot make the machine variance claim.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | BSP-T1 | integration | Identifies wrapper-owned canonical child inventory before scheduling changes. |
| R2 | BSP-T1 | integration | Asserts child ID, command, canonical order, and required/optional status. |
| R3 | BSP-T2, BSP-T5 | integration | Reconciles classification before any parallel scheduling. |
| R4 | BSP-T1, BSP-T2 | contract | Ensures classification metadata is checked against, not substituted for, inventory. |
| R5 | BSP-T1, BSP-T8 | integration | Compares baseline and revised child set. |
| R6 | BSP-T1, BSP-T2, BSP-T8 | integration | Compares command identity and rejects stale classifications. |
| R7 | BSP-T6, BSP-T8 | integration | Aggregation and grouped output follow canonical order. |
| R8 | BSP-T2, BSP-T3, BSP-T5 | unit | High confidence is required for parallel eligibility. |
| R9 | BSP-T2, BSP-T3 | unit | Missing, stale, low-confidence, contradictory, or unreconciled entries are not eligible. |
| R10 | BSP-T2, BSP-T3 | unit | Unsafe side effects, shared paths, ordering, cache, cwd, and uncaptured output block eligibility. |
| R11 | BSP-T3, BSP-T11 | integration | Network-sensitive checks stay sequential unless hermetic and isolated. |
| R12 | BSP-T3, BSP-T5 | integration | Resource-heavy children are sequential or consume explicit budget. |
| R13 | BSP-T4, BSP-T5, BSP-T7 | integration | First-slice parallel mode remains opt-in until parity evidence exists. |
| R14 | BSP-T9 | contract | Default promotion is a separate acceptance state. |
| R15 | BSP-T9 | unit | Promoted default worker count uses the conservative formula or recorded safer value. |
| R16 | BSP-T4, BSP-T5 | integration | Bounded worker count is supported for parallel-enabled execution. |
| R17 | BSP-T4, BSP-T10 | e2e | `--jobs 1` gives strict sequential compatibility and rollback behavior. |
| R18 | BSP-T5 | integration | Jobs above eligible count do not change semantics. |
| R19 | BSP-T6, BSP-T7 | integration | Child stdout/stderr is captured separately. |
| R20 | BSP-T6 | integration | Parallel child output is never live-interleaved. |
| R21 | BSP-T6 | integration | Success output remains compact and deterministic. |
| R22 | BSP-T6 | integration | Verbose output is grouped and ordered by child. |
| R23 | BSP-T7 | integration | Failure output includes all required child diagnostic fields. |
| R24 | BSP-T7 | integration | First slice runs all required children and reports all required failures. |
| R25 | BSP-T10 | contract | Fail-fast remains out of scope without a separate approved contract. |
| R26 | BSP-T4, BSP-T7 | integration | All required children passing exits 0. |
| R27 | BSP-T7 | integration | Any required child failure exits nonzero. |
| R28 | BSP-T7 | integration | Scheduler errors exit nonzero. |
| R29 | BSP-T2, BSP-T7 | integration | Inventory/classification mismatch exits nonzero before parallel execution. |
| R30 | BSP-T3 | integration | Low-confidence or explicitly ineligible reconciled children can run sequentially. |
| R31 | BSP-T2 | unit | Command changes without classification updates fail freshness validation. |
| R32 | BSP-T2 | unit | Contradictory parallel-safe metadata fails validation. |
| R33 | BSP-T8 | contract | Fresh sequential per-child timing exists before behavior changes. |
| R34 | BSP-T9 | contract | Before/after runtime evidence is comparable or limitations are recorded. |
| R35 | BSP-T9 | manual | Runtime evidence records whether improvement came from scheduling, not omitted proof. |
| R36 | BSP-T8, BSP-T9 | contract | Preservation evidence covers child set, commands, order, exit behavior, diagnostics, verbose, jobs=1, final verify, and cache boundary. |
| R37 | BSP-T9 | contract | Smaller improvement records sequential-only rationale. |
| R38 | BSP-T9 | contract | No-safe-parallelism closeout records rationale and separate follow-up route. |
| R39 | BSP-T10 | contract | Final verify boundary remains actual execution evidence. |
| R40 | BSP-T10 | contract | Cache, remote cache, persistent worker, and composition remain excluded. |
| R41 | BSP-T9 | contract | Default promotion requires validator-owned or registry-owned classification. |
| R42 | BSP-T2, BSP-T12 | integration | Freshness validation fails for missing, stale, low-confidence, contradictory, and unsafe entries. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | BSP-T1, BSP-T5, BSP-T6 | Opt-in parallel mode preserves identity and canonical summary order. |
| E2 | BSP-T4 | `--jobs 1` parity covers order, exit behavior, diagnostics, and verbose grouping. |
| E3 | BSP-T2, BSP-T7 | Missing classification fails before launching parallel children. |
| E4 | BSP-T3 | Medium-confidence child remains sequential. |
| E5 | BSP-T6, BSP-T7 | Multiple parallel and sequential failures are grouped in canonical order. |
| E6 | BSP-T2 | Stale command identity fails freshness validation before parallel execution. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | BSP-T2 | No classification artifact fails reconciliation before parallel execution. |
| EC2 | BSP-T2 | Stale command identity fails freshness validation. |
| EC3 | BSP-T2 | Contradictory shared temp/write metadata fails validation. |
| EC4 | BSP-T3 | Low-confidence child is not scheduled in the parallel phase. |
| EC5 | BSP-T6, BSP-T7 | Completion order differs from canonical order; output remains canonical. |
| EC6 | BSP-T7 | Parallel and sequential-only child failures are both reported. |
| EC7 | BSP-T7 | Worker crash is reported as scheduler error and exits nonzero. |
| EC8 | BSP-T6 | Verbose output from parallel children is grouped without interleaving. |
| EC9 | BSP-T5 | `--jobs` greater than eligible count has no semantic effect. |
| EC10 | BSP-T9 | CPU count one or unavailable produces conservative worker behavior. |
| EC11 | BSP-T11 | Hermetic local network check with shared port conflict remains sequential or fails eligibility. |
| EC12 | BSP-T9 | Slower parallel result records resource-contention limitation. |
| EC13 | BSP-T9 | No safe child records no-safe-parallelism rationale. |
| EC14 | BSP-T10 | Fail-fast request is rejected or deferred as out of scope. |

## Test cases

### BSP-T1. Canonical Broad-Smoke Inventory and Identity

- Covers: R1, R2, R4, R5, R6, E1
- Level: integration
- Fixture/setup: Wrapper-owned broad-smoke inventory or helper fixture with current child IDs, commands, order, and required/optional status.
- Steps: Extract the canonical inventory, compare it to the wrapper execution source, and assert classification data is not accepted as an independent child list.
- Expected result: Inventory contains every broad-smoke child with stable identity fields, and child set/order/commands are the source used by broad-smoke execution.
- Failure proves: Broad-smoke scheduling could run a different child set or allow classification metadata to own execution identity.
- Automation location: `scripts/test-select-validation.py -k broad_smoke`

### BSP-T2. Classification Reconciliation and Freshness Failures

- Covers: R3, R4, R6, R8, R9, R10, R29, R31, R32, R42, E3, E6, EC1, EC2, EC3
- Level: unit
- Fixture/setup: Classification fixtures for missing artifact, missing child, stale command, low-confidence parallel-safe claim, contradictory parallel-safe metadata, and valid high-confidence independent metadata.
- Steps: Run freshness validation against the canonical inventory for each fixture.
- Expected result: Missing, stale, low-confidence parallel-safe, contradictory, or unreconciled fixtures fail closed with explicit diagnostics before parallel execution.
- Failure proves: Unknown or stale broad-smoke checks could be treated as parallel-safe by accident.
- Automation location: `scripts/test-select-validation.py -k broad_smoke`

### BSP-T3. Sequential-Only Eligibility Cases

- Covers: R8, R9, R10, R11, R12, R30, E4, EC4, EC11
- Level: integration
- Fixture/setup: Broad-smoke fixture inventory containing low-confidence, mutating, shared-output, order-dependent, network-sensitive, and resource-heavy children.
- Steps: Build the execution plan with `--jobs 4` and inspect each child's scheduled phase and worker budget.
- Expected result: Unsafe, low-confidence, non-hermetic network-sensitive, and resource-heavy children are sequential-only or require an explicit larger worker budget.
- Failure proves: The scheduler is allowing unsafe children into the parallel phase.
- Automation location: `scripts/test-select-validation.py -k broad_smoke`

### BSP-T4. `--jobs 1` Sequential Compatibility

- Covers: R13, R16, R17, R26, E2
- Level: e2e
- Fixture/setup: Broad-smoke fixture or real wrapper run with both eligible and sequential-only children.
- Steps: Run broad-smoke with `--jobs 1`, compare result order, exit behavior, diagnostics, and verbose grouping to strict sequential broad-smoke.
- Expected result: `--jobs 1` behaves as sequential broad-smoke and exits 0 when all required children pass.
- Failure proves: Rollback/sequential compatibility is broken.
- Automation location: `python scripts/test-select-validation.py -k broad_smoke`; `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 1`

### BSP-T5. Opt-In Parallel Scheduling and Worker Bounds

- Covers: R3, R8, R12, R13, R16, R18, E1, EC9
- Level: integration
- Fixture/setup: Execution-plan fixture with high-confidence eligible children, sequential-only children, and `--jobs` values `2`, `4`, and greater than eligible child count.
- Steps: Run the scheduler in opt-in parallel mode and inspect launched phases, worker count, and scheduled child commands.
- Expected result: Only eligible children run in parallel, worker count is bounded, sequential-only children remain sequential, and excess jobs do not change child semantics.
- Failure proves: Opt-in broad-smoke parallelism is either unbounded or changes the proof contract.
- Automation location: `scripts/test-select-validation.py -k jobs`; `scripts/test-select-validation.py -k broad_smoke`

### BSP-T6. Deterministic Aggregation and Verbose Grouping

- Covers: R7, R19, R20, R21, R22, R36, E1, E5, EC5, EC8
- Level: integration
- Fixture/setup: Parallel children with controlled completion order different from canonical order and stdout/stderr payloads for default and verbose modes.
- Steps: Run the aggregate formatter for success and verbose outputs after out-of-order child completion.
- Expected result: Default success output is compact and deterministic; verbose and grouped output is ordered by canonical child order with no interleaved child logs.
- Failure proves: Parallel scheduling makes broad-smoke output nondeterministic or less reviewable.
- Automation location: `scripts/test-select-validation.py -k broad_smoke`

### BSP-T7. Failure Parity and Scheduler Errors

- Covers: R13, R19, R23, R24, R26, R27, R28, R29, E3, E5, EC5, EC6, EC7
- Level: integration
- Fixture/setup: Failure fixtures for one child failure, multiple child failures, parallel child failure, sequential-only child failure, inventory/classification mismatch, and worker crash.
- Steps: Run broad-smoke wrapper fixtures in opt-in parallel mode and inspect exit code and diagnostics.
- Expected result: All required failures are reported in canonical order with child ID, command, exit code or signal, duration, captured stdout/stderr, rerun command, and execution phase; scheduler errors exit nonzero.
- Failure proves: Parallelism hides failures, degrades diagnostics, or masks scheduler errors.
- Automation location: `scripts/test-select-validation.py -k broad_smoke`

### BSP-T8. Baseline Timing and Preservation Evidence Shape

- Covers: R5, R6, R7, R33, R36, AC3, AC18
- Level: contract
- Fixture/setup: `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-baseline.yaml` and preservation artifact fixture.
- Steps: Validate required baseline fields and preservation matrix entries for child set, commands, output order, exit behavior, failure diagnostics, `--verbose`, `--jobs 1`, final verify, and cache boundary.
- Expected result: Baseline evidence exists before execution behavior changes and preservation evidence names all required surfaces.
- Failure proves: Runtime attribution or behavior-preservation proof is incomplete.
- Automation location: selected explicit CI over evidence artifacts where practical; manual review for timing-run count and variance notes.

### BSP-T9. Runtime Result, Promotion Decision, and No-Safe-Parallelism Evidence

- Covers: R14, R15, R34, R35, R37, R38, R41, EC10, EC12, EC13
- Level: contract
- Fixture/setup: `broad-smoke-parallelism-result.yaml`, default-promotion decision record, and no-safe-parallelism fixture when applicable.
- Steps: Validate result fields, comparable-environment notes, child phases, duration delta, variance, sequential-only rationale, and default-promotion classification ownership when promotion is chosen.
- Expected result: Performance claims are attributed to scheduling; slower, partial, or no-safe-parallelism outcomes are recorded without weakening proof.
- Failure proves: The change is claiming runtime value without sufficient evidence or promoting default behavior without durable classification ownership.
- Automation location: selected explicit CI over result and preservation artifacts; manual review for environment comparability.

### BSP-T10. Rollback, Compatibility, and Scope Boundaries

- Covers: R17, R25, R39, R40, AC20, AC21, AC23, EC14
- Level: contract
- Fixture/setup: Wrapper option fixture and artifact review of changed files.
- Steps: Verify `--jobs 1` remains available as rollback, fail-fast is not introduced in the first slice, final verify remains actual-run evidence, and no cache, persistent worker, remote cache, composition, selector, hosted CI, PR readiness, or branch-readiness behavior is added.
- Expected result: Rollback exists and the implementation stays within the approved scope.
- Failure proves: The implementation has expanded beyond scheduling-only broad-smoke parallelism.
- Automation location: `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py`; code review and final verify.

### BSP-T11. Network and Security Isolation

- Covers: R11, EC11
- Level: integration
- Fixture/setup: Network-sensitive child fixture using local hermetic stub metadata, and a conflicting shared-port variant.
- Steps: Evaluate parallel eligibility for isolated and shared-port variants.
- Expected result: Only fully hermetic, isolated, deterministic, credential-free network fixtures can be eligible; shared port conflict remains sequential or fails eligibility.
- Failure proves: Network-sensitive checks could contend for mutable external or local resources in parallel.
- Automation location: `scripts/test-select-validation.py -k broad_smoke`

### BSP-T12. Lifecycle and Metadata Consistency

- Covers: R42, workflow handoff, artifact consistency
- Level: contract
- Fixture/setup: Change metadata, plan, spec, test spec, and review records for this change.
- Steps: Run metadata, review, lifecycle, selected explicit CI, and diff hygiene commands over the lifecycle-managed artifacts.
- Expected result: Lifecycle state points to `test-spec-review`, authoritative artifacts are valid, and no review findings are left unrecorded.
- Failure proves: The workflow state is stale or cannot safely route to the next gate.
- Automation location: `python scripts/validate-change-metadata.py docs/changes/2026-06-27-broad-smoke-safe-parallelism/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`; `bash scripts/ci.sh --mode explicit ...`; `git diff --check -- ...`

## Fixtures and data

- Canonical child inventory fixture derived from the wrapper-owned broad-smoke child source.
- Classification fixtures for high-confidence independent, low-confidence, explicit sequential-only, missing child, stale command, contradictory metadata, shared temp/output, cwd/order-dependent, unsafe cache, network-sensitive, and resource-heavy children.
- Scheduler fixtures with controlled child duration, stdout/stderr payloads, exit codes, signals, and worker crash behavior.
- Timing evidence artifacts:
  - `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-baseline.yaml`
  - `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-result.yaml`
  - `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md`

## Mocking/stubbing policy

Use fixtures for child commands, child output, failures, timing, and worker
crashes so tests are deterministic and fast. Do not mock away the scheduler
decision logic, classification reconciliation, aggregate formatter, exit-code
selection, or wrapper command parsing under test. Network-sensitive behavior
must use local hermetic stubs only; no test should require credentials or
external mutable services.

## Migration or compatibility tests

- `--jobs 1` is the compatibility and rollback path and must match sequential broad-smoke behavior.
- First-slice parallel mode remains opt-in; default promotion is tested only when a later milestone records the promotion decision.
- Existing broad-smoke child set, command identity, canonical order, required/optional status, output contract, exit behavior, and final verify boundary are preservation surfaces.

## Observability verification

Failure diagnostics must include child ID, command, exit code or signal,
duration, captured stdout/stderr, rerun command, and execution phase. Verbose
output must show full child output grouped in canonical child order. Runtime
artifacts must record baseline and parallel child durations, result, output
bytes, phase, delta, variance notes, low-confidence children, and
sequential-only children.

## Security/privacy verification

The scheduler must not run network-sensitive children concurrently unless
metadata proves local hermetic fixtures or stubs, no credentials, no external
mutable state, no shared port conflict, no hidden environment dependency,
deterministic timeout behavior, and isolated temp/output roots. Tests should
assert no cache, remote cache, persistent worker, new cross-process protocol, or
validator composition is introduced by this change.

## Performance checks

Record fresh sequential per-child timing before behavior changes. Record paired
before/after broad-smoke runtime evidence under comparable conditions where
practical, preferably median of at least three runs. If variance is high,
parallelism is slower, or no child is safe, record limitations and rationale
instead of claiming success.

## Manual QA checklist

- Review baseline and result artifacts for comparable environment notes and variance limitations.
- Review preservation evidence for child set, command identity, output order, diagnostics, `--verbose`, `--jobs 1`, final verify, and cache boundary.
- Confirm default promotion, if chosen, cites validator-owned or registry-owned classification.
- Confirm no-safe-parallelism or partial-improvement rationale is recorded when applicable.

## What not to test and why

- Do not test validation-result caching, remote/shared cache, or cache-hit final proof; these are explicit non-goals.
- Do not test persistent workers or broad validator composition; they require separate proposals.
- Do not test selector behavior changes, hosted CI redesign, PR readiness, branch readiness, or release readiness; this change is local broad-smoke scheduling.
- Do not test child-command rewrites as part of parallelism; command changes require a separate approved contract.
- Do not test fail-fast as first-slice behavior; first-slice broad-smoke must aggregate all required failures.

## Uncovered gaps

None. The approved spec and plan provide enough contract and sequencing context
for implementation tests after `test-spec-review`.

## Next artifacts

```text
test-spec-review
implementation
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet.

## Readiness

Ready for `test-spec-review`. This artifact defines the proof map only; it does
not authorize implementation until test-spec-review completes.
