# Broad-Smoke and Fixture-Suite Output Compaction

## Status

accepted

## Problem

The accepted script-output optimization slice made one high-noise producer and one selected-CI wrapper path quieter while preserving actionable failure evidence. That slice was intentionally narrow: `scripts/test-select-validation.py` gained compact defaults, and selected validation wrapper behavior stayed failure-focused.

The remaining output noise is a layering problem. Repository validation output can come from producers that print directly and from orchestrators that run those producers. The first slice optimized one producer and one orchestrator path, but broad-smoke still uses a separate `run_check` path in `scripts/ci.sh` that streams child stdout and stderr directly. Some child fixture suites also still use verbose defaults, including the named candidate `scripts/test-change-metadata-validator.py`.

Either layer alone is an incomplete fix. Capturing broad-smoke child output protects successful broad-smoke logs from current and future noisy children, but direct local producer runs can remain noisy. Compacting producers improves local runs and failure readability, but future broad-smoke children can still reintroduce success noise if `run_check` streams by default.

## Goals

- Extend the accepted script-output optimization direction from selected-CI to the broad-smoke orchestration path.
- Make broad-smoke quiet on success by applying an output-capture policy to `run_check`.
- Keep broad-smoke failure output actionable, including the failed check, exit reason, command, duration, and captured child output.
- Preserve selected checks, command execution, exit-code behavior, failure detection, failure evidence, and rerun behavior.
- Inventory producer and orchestrator layers together instead of auditing producers alone.
- Give compact defaults to the first confirmed high-use or high-noise direct-run producer, expected to be `scripts/test-change-metadata-validator.py`.
- Preserve `--verbose` access to full child output and full producer detail.
- Keep generated artifacts, skills, specs unrelated to this initiative, adapters, JSON behavior, and validation selection out of scope.

## Non-goals

- Do not rewrite every `unittest.main(verbosity=2)` script in this slice.
- Do not change what any producer validates.
- Do not change broad-smoke check selection.
- Do not change selected-CI behavior except for compatible shared interfaces if a later spec or plan proves they are needed.
- Do not suppress failure reasons or hide child stderr on failure.
- Do not truncate failure evidence below what maintainers need to diagnose failures.
- Do not add new `--json` support.
- Do not change generated skill output, public adapter output, or adapter installation behavior.
- Do not solve UI transcript folding; display-layer folding is outside repository-owned script behavior.
- Do not claim implementation readiness, final verification, branch readiness, or PR readiness from this proposal alone.

## Vision fit

fits the current vision

RigorLoop's vision depends on evidence that is easy to inspect, reason about, validate, and maintain. Compact success output and actionable failure output directly support that evidence discipline. This proposal extends the accepted script-output principle to every layer that can print during broad-smoke validation:

```text
Output volume should scale with the information the reader needs to act on,
not with the amount of work the program did.
```

The direction would conflict with the vision if shorter output changed selected commands, selected tests, exit codes, failure detection, or made maintainers rerun commands to understand a failure.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Continue optimization after the first script-output slice | in scope | Problem, Goals |
| Address broad-smoke noise | in scope | Goals, Recommended direction |
| Address verbose child producers | in scope | Goals, Scope budget |
| Prioritize `run_check` capture | in scope | Recommended direction |
| Audit layers, not just scripts | in scope | Goals, Testing and verification strategy |
| Keep orchestrator and producer fixes separated | in scope | Scope budget, Rollout and rollback |
| Preserve failure evidence | in scope | Goals, Non-goals, Testing and verification strategy |
| Preserve validation behavior | in scope | Goals, Non-goals |
| Avoid UI transcript folding | out of scope | Non-goals |
| Avoid blanket rewrite of all unittest scripts | out of scope | Non-goals, Scope budget |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Producer by orchestrator output-layer audit | core to this proposal | The missed gap is an unenumerated orchestration path, so the next slice needs layer evidence before implementation. |
| Broad-smoke `run_check` capture policy | first-slice candidate | It is the structural fix that prevents successful broad-smoke output from scaling with child-suite verbosity. |
| Broad-smoke success, failure, verbose, stderr, and exit-code proof | same-slice dependency | The wrapper change is only acceptable if failure evidence and child exit semantics are preserved. |
| First high-use direct-run producer compact default | first-slice candidate | The expected target, `scripts/test-change-metadata-validator.py`, improves direct local runs and captured failure readability. |
| Selected-CI regression proof | same-slice dependency | The accepted first slice should remain compatible and unchanged unless shared helper behavior requires proof. |
| Broad rewrite of all verbose unittest producers | separate implementation slice | The audit should identify priority, but blanket rewrites create review churn without being necessary for broad-smoke success compaction. |
| Shared script-output helper library | deferable follow-up | It is justified only if the wrapper and first producer would otherwise duplicate meaningful formatting logic. |
| JSON output across validation scripts | separate proposal | Machine-readable output is a broader contract than this human-readable output slice. |
| UI transcript folding | out of scope | UI folding is not repository-owned script behavior. |
| Generated skill or adapter output | out of scope | The proposal targets repository validation output, not generated release artifacts. |

## Context

The accepted [RigorLoop Script Output Optimization](2026-05-21-script-output-optimization.md) proposal and approved `specs/script-output-optimization.md` define the first output-shaping slice around `scripts/test-select-validation.py` and the selected validation wrapper boundary. That spec already establishes the key invariant: output optimization is presentation-only and does not change validation coverage, selected checks, failure detection, or exit-code semantics.

The current `scripts/ci.sh` broad-smoke path has a separate `run_check` helper that prints the label, prints the command, executes the command directly, and then prints a blank line. Because the child process is not captured by that path, any successful child that emits verbose output can flood broad-smoke logs. `scripts/test-change-metadata-validator.py` is one named producer candidate because it is run by broad-smoke and is likely useful as a direct maintainer command.

This proposal treats the next slice as a coordinated wrapper-plus-producer output UX improvement, not a validation semantics change.

## Options considered

### Option 1: Do nothing

Leave broad-smoke and remaining producer scripts unchanged.

Pros:

- No implementation risk.
- Existing logs remain familiar.
- No new output-shape tests are needed.

Cons:

- Broad-smoke success output remains vulnerable to noisy children.
- Direct local producer runs remain verbose.
- The first slice's output policy stays inconsistent across orchestrator paths.

### Option 2: Optimize only child producers

Convert high-noise direct-run producers such as `scripts/test-change-metadata-validator.py` to compact defaults.

Pros:

- Improves direct local runs.
- Makes captured failure output easier to read later.
- Keeps orchestrator behavior unchanged.

Cons:

- Broad-smoke remains structurally vulnerable to any future noisy producer.
- Every producer has to be individually disciplined to protect broad-smoke success logs.
- A newly verbose child can reintroduce success noise.

### Option 3: Optimize only broad-smoke `run_check`

Make broad-smoke capture child output and show it only on failure or under `--verbose`.

Pros:

- Highest leverage for successful broad-smoke logs.
- Prevents future verbose children from flooding broad-smoke success output.
- Aligns broad-smoke with the selected-CI failure-focused policy.

Cons:

- Direct local producer runs remain noisy.
- Failure output from still-verbose producers can remain large.
- Producer-specific direct-run contracts remain inconsistent.

### Option 4: Coordinated wrapper capture plus one high-use producer

Apply broad-smoke `run_check` capture first, then compact the first confirmed high-use or high-noise direct-run producer.

Pros:

- Fixes the structural orchestrator gap.
- Improves direct-run behavior for a named producer candidate.
- Keeps scope bounded.
- Separates wrapper behavior risk from producer formatting risk.
- Creates a reusable pattern for later producer conversions.

Cons:

- Touches both wrapper and producer surfaces.
- Requires behavior-preservation proof for two layers.
- Requires a producer by orchestrator audit instead of a script-only audit.

## Recommended direction

Choose Option 4.

The next slice should first inventory every output layer that matters for broad-smoke and selected-CI. It should then apply a broad-smoke `run_check` capture policy so successful child stdout and stderr are not streamed by default. Captured child output should be emitted for failures and for successful checks under `--verbose`.

The first producer cleanup should remain targeted. The producer should default to one compact success summary, keep actionable failure detail, preserve full detail under `--verbose`, and avoid treating zero executed tests as a successful run unless an explicit mode documents zero as valid.

The wrapper-mode consistency invariant should be enforced by the downstream spec or test spec: repository-owned orchestration modes that run validation producers should use the same capture-on-success, show-on-failure-or-verbose policy unless the governing spec records a deliberate exception. The proof should include a check that every `scripts/ci.sh` orchestration mode that runs validation producers either uses the capture policy or carries a documented exception.

The recommended broad-smoke success-output candidate is an aggregate success summary, such as `[PASS] broad-smoke: N checks passed in <duration>s`, with per-child lines shown only for non-pass children or under `--verbose`. If the downstream spec or plan chooses one line per passing child instead, it should record why that growth with child count is still acceptable for broad-smoke.

## First producer decision

The first targeted producer is `scripts/test-change-metadata-validator.py`.

The output-layer audit may recommend a different producer only if it records:

- the alternative producer;
- why it has higher direct-run or failure-readability value;
- whether broad-smoke runs it;
- owner approval to replace the default target.

Without that recorded decision, implementation should target `scripts/test-change-metadata-validator.py`.

## Producer verbosity decision

The downstream plan must decide one of these routes for the first targeted producer:

1. implement default, `--verbose`, and `--quiet` behavior;
2. implement default and `--verbose` only, and explicitly record that `--quiet` is out of scope for this producer.

If `--quiet` is implemented, quiet success writes no stdout or stderr, and quiet failure still prints actionable failure details.

If both `--verbose` and `--quiet` are accepted by the producer, combined use should follow the existing script-output conflict rule: reject with a nonzero usage error before running checks.

The recommended first-slice route is default and `--verbose` behavior, with `--quiet` added only if the focused test-spec amendment explicitly owns that mode.

## Expected behavior changes

- Broad-smoke success output becomes compact and wrapper-owned. The recommended shape is one aggregate success summary, with per-child lines reserved for non-pass children or `--verbose`.
- Broad-smoke no longer streams successful child stdout or stderr by default.
- Broad-smoke failure output includes the failed child name, exit code or exit reason, command, duration, and captured output.
- Broad-smoke `--verbose` preserves full child output, including successful child output.
- The first targeted producer becomes compact when run directly.
- The first targeted producer keeps actionable failure output and full verbose detail.
- Validation selection, command execution, exit codes, failure detection, generated artifacts, skills, adapters, and selected-CI behavior remain unchanged unless a later approved artifact explicitly broadens scope.

## Architecture impact

| Surface | Expected impact |
| --- | --- |
| `scripts/ci.sh` broad-smoke `run_check` | Add capture-on-success and show-on-failure-or-verbose behavior for broad-smoke child checks. |
| Broad-smoke tests | Add output-shape coverage for success, failure, verbose mode, stderr handling, and child exit semantics. |
| Wrapper-mode consistency guard | Add spec or test-spec coverage that checks every `scripts/ci.sh` orchestration mode running validation producers uses capture-on-success/show-on-failure-or-verbose behavior or documents an exception. |
| First producer script | Add or adapt compact default output and verbosity tiers for the confirmed producer. |
| `specs/script-output-optimization.md` | Amend only if the existing approved contract does not already cover broad-smoke and direct-run producer expansion. |
| `specs/script-output-optimization.test.md` | Add focused coverage for broad-smoke wrapper behavior and the first targeted producer. |
| Change-local evidence | Add a producer by orchestrator audit and behavior-preservation evidence for selected commands, selected tests, exit codes, and failure evidence. |
| CI behavior | Reduce success noise while preserving failure evidence and exit behavior. |
| Generated artifacts, skills, adapters | No expected change. |

## Proof route

This proposal requires a focused test-spec amendment for broad-smoke wrapper behavior and the first targeted producer.

A spec amendment is required if the existing `script-output-optimization` contract does not already define:

- broad-smoke `run_check` capture-on-success behavior;
- show-on-failure-or-verbose behavior;
- wrapper-mode consistency across selected-CI and broad-smoke;
- direct-run producer compact default behavior beyond `test-select-validation.py`;
- behavior-preservation proof for selected child commands and selected tests.

Implementation must not begin until the plan names one approved route:

1. existing spec plus focused test-spec amendment is sufficient;
2. spec amendment plus focused test-spec amendment packet is approved.

The recommended route is a focused test-spec amendment, with a spec amendment likely unless the existing spec already covers broad-smoke and the targeted direct-run producer.

## Behavior-preservation proof

Implementation must record a preservation matrix:

| Surface | Baseline proof | Post-change proof | Required result |
| --- | --- | --- | --- |
| broad-smoke child commands | ordered command list plus SHA-256 hash | ordered command list plus SHA-256 hash | unchanged |
| broad-smoke pass exit code | passing fixture | passing fixture | unchanged |
| broad-smoke fail exit code | failing fixture | failing fixture | unchanged |
| broad-smoke failure evidence | baseline failed child output | captured failed child output | same or more actionable |
| broad-smoke verbose output | baseline streamed child output | verbose captured child output | full detail preserved |
| targeted producer selected tests/checks | ordered identifier list plus SHA-256 hash | ordered identifier list plus SHA-256 hash | unchanged |
| targeted producer pass/fail exit codes | pass/fail fixtures | pass/fail fixtures | unchanged |
| selected-CI behavior | baseline selected-CI command/output | post-change command/output | unchanged |

## Ordinary-validation guard

Post-implementation ordinary validation must exercise the new output-contract tests or include an ordinary guard that fails when those tests fail.

Focused output-contract commands may remain as diagnostics, but they should not be the only proof.

## Testing and verification strategy

Expected proof should include:

- An output-layer audit at `docs/changes/<change-id>/script-output-layer-audit.md` that names producers, direct-run success shape, direct-run failure usefulness, orchestrators, capture policy, high-use status, and first-slice treatment.
- Broad-smoke tests proving default success does not stream child stdout or stderr and still reports compact child-check summaries.
- Broad-smoke failure tests proving the failed child name, exit code or exit reason, command, duration, stderr/stdout evidence, and rerun guidance where safe.
- Broad-smoke verbose tests proving full captured child output is available for successful checks.
- A wrapper-mode consistency check proving each `scripts/ci.sh` orchestration mode that runs validation producers uses capture-on-success/show-on-failure-or-verbose behavior or has a documented exception.
- Captured failure-output proof showing stdout/stderr ordering is preserved when feasible, or clearly labeled if stdout and stderr are captured separately.
- Behavior-preservation evidence showing broad-smoke selected child commands and child exit-code behavior are unchanged.
- Producer direct-run tests for compact success, actionable failure, verbose full detail, quiet behavior where applicable, and zero-test behavior.
- Selected-CI regression proof showing the first slice does not regress.
- Changed-path proof that generated artifacts, skills, adapters, JSON support, and validation-selection logic did not change.

Suggested validation commands for the downstream plan or test spec to confirm or adjust:

```bash
python scripts/test-select-validation.py
python scripts/test-change-metadata-validator.py
python scripts/test-change-metadata-validator.py --verbose
python scripts/test-change-metadata-validator.py --quiet
bash scripts/ci.sh --mode broad-smoke
bash scripts/ci.sh --mode broad-smoke --verbose
bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-change-metadata-validator.py --path scripts/test-select-validation.py
git diff --check --
```

If repository-owned command names or supported flags differ when the test spec is amended, the test spec and plan should name the exact commands to run.

## Rollout and rollback

Roll out through the normal workflow after proposal review. The next authoring step should decide whether the approved `script-output-optimization` spec already covers the broad-smoke and producer-layer behavior or whether a focused spec amendment is needed. A focused test-spec amendment is expected either way.

The downstream plan should keep wrapper capture and producer formatting as separately reviewable work items. The wrapper capture work should precede producer formatting because it protects broad-smoke success logs from every child producer. Evidence closeout should compare before and after command lists, test lists where applicable, exit codes, failure output, verbose output, and selected-CI behavior.

Rollback can revert broad-smoke capture independently if wrapper failures become ambiguous. Producer formatting can be reverted independently if direct-run output regresses. Rollback should preserve accurate audit evidence and should not change validation selection, exit-code semantics, generated artifacts, skills, adapters, or unrelated specs.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| `run_check` hides failure details. | Failure output includes captured stdout and stderr, command, exit reason, and check identity. |
| `run_check` changes child exit semantics. | Behavior-preservation evidence records pass and fail exit-code behavior. |
| Captured stderr disappears or is mislabeled. | Tests cover child stderr and failure output labeling. |
| Failure output remains too large. | First producer compaction improves captured failure readability; bounded tailing can be a later decision only if evidence remains sufficient. |
| Future producers reintroduce success noise. | Broad-smoke wrapper capture makes future success output quiet by default. |
| Direct local runs remain noisy. | Audit-driven producer cleanup starts with the highest-value direct-run producer and routes later producers as follow-up slices. |
| Blanket producer rewrites cause churn. | This proposal scopes producer cleanup to the first confirmed high-use or high-noise candidate. |
| Wrapper modes diverge again. | Downstream spec or test-spec coverage should enforce wrapper-mode capture consistency through a guard over `scripts/ci.sh` orchestration paths, allowing only documented exceptions. |
| UI transcript still appears noisy. | UI transcript folding remains out of scope and should be handled by a separate display-layer proposal if needed. |

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-BSO-001` | Output-layer audit maps producers, orchestrators, capture policy, and first-slice treatment. |
| `AC-BSO-002` | Broad-smoke `run_check` captures child stdout and stderr by default. |
| `AC-BSO-003` | Broad-smoke success does not stream successful child output. |
| `AC-BSO-004` | Broad-smoke success reports an aggregate summary by default, or records an approved reason for per-child success lines. |
| `AC-BSO-005` | Broad-smoke failure reports child name, command, exit code, duration, and captured stdout/stderr. |
| `AC-BSO-006` | Broad-smoke `--verbose` emits full captured output for successful children. |
| `AC-BSO-007` | Broad-smoke selected child command list and exit-code behavior are unchanged. |
| `AC-BSO-008` | The first targeted producer has compact direct-run success output. |
| `AC-BSO-009` | The first targeted producer preserves actionable failure output. |
| `AC-BSO-010` | The first targeted producer preserves full detail under `--verbose`. |
| `AC-BSO-011` | Quiet behavior is either implemented and tested, or explicitly out of scope for the producer. |
| `AC-BSO-012` | Output-contract tests run in ordinary post-implementation validation or are guarded by ordinary validation. |
| `AC-BSO-013` | Selected-CI behavior does not regress. |
| `AC-BSO-014` | No generated artifacts, skills, adapters, JSON support, or validation selection changes are introduced. |
| `AC-BSO-015` | Wrapper-mode consistency is checked for every `scripts/ci.sh` orchestration mode that runs validation producers, with documented exceptions required for any non-capturing path. |

## Open questions

No proposal-level open questions remain.

The spec, test-spec, or plan still need to settle the exact broad-smoke command-list extraction method, the selected-test identifier extraction method for `scripts/test-change-metadata-validator.py`, whether captured failure output preserves interleaved stdout/stderr ordering or labels streams separately, and whether `--quiet` is owned by the first producer slice.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-22 | Treat remaining output noise as a layer problem. | The first slice optimized one producer and one orchestrator path; broad-smoke is a separate orchestrator. | Treat the first slice as simply incomplete. |
| 2026-05-22 | Prioritize broad-smoke `run_check` capture. | Orchestrator capture is the durable guarantee for every child run by broad-smoke. | Start with blanket producer rewrites. |
| 2026-05-22 | Require a producer by orchestrator audit. | The previous audit model did not enumerate every orchestration path that can print. | Rank producers only. |
| 2026-05-22 | Keep producer cleanup targeted. | Wrapper capture reduces broad-smoke urgency; direct-run value and failure readability should determine producer priority. | Rewrite every verbose unittest script. |
| 2026-05-22 | Keep UI transcript folding out of scope. | Repository-owned script behavior and UI display behavior are different layers. | Fix display-layer folding in this proposal. |
| 2026-05-22 | Lock the default first producer to `scripts/test-change-metadata-validator.py`. | Proposal-review R1 found the producer target too soft for planning. | Let the audit replace the target without recorded approval. |
| 2026-05-22 | Require focused test-spec amendment before implementation. | Broad-smoke is a new output layer and needs explicit proof coverage. | Let planning proceed with a conditional proof route. |
| 2026-05-22 | Require stable command/test identity proof. | Prior script-output work showed count-only proof can miss selected-test drift. | Rely only on output-shape comparison. |
| 2026-05-22 | Make wrapper-mode consistency checkable. | The original divergence happened because the capture policy was not enforced across orchestration paths. | Leave wrapper-mode consistency as prose only. |
| 2026-05-22 | Seed aggregate broad-smoke success as the recommended candidate. | Aggregate success output stays constant-size as child count grows, while per-child success lines still grow with work. | Treat aggregate and per-child success output as equally preferred. |

## Next artifacts

- `proposal-review`
- Focused `specs/script-output-optimization.test.md` amendment for broad-smoke and the first targeted producer
- Spec amendment if the existing `script-output-optimization` contract is insufficient for broad-smoke and producer-layer behavior
- Plan and plan-review
- Implementation, code-review, explain-change, verify, and PR handoff after downstream artifacts are approved

## Follow-on artifacts

- `specs/script-output-optimization.md`

## Readiness

Accepted after `proposal-review-r2`; downstream spec amendment created at `specs/script-output-optimization.md`.
