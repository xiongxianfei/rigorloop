# Learn Session: Selector-Regression Runtime Reduction Retrospective

## Status

- Status: recorded
- Date: 2026-06-27
- Trigger type: explicit maintainer request
- Trigger: `$learn` request to summarize the selector-regression runtime-reduction experience, explain why the result improved significantly, and outline the next optimization direction.
- Session path: `docs/learn/sessions/2026-06-27-selector-regression-runtime-reduction-retrospective.md`

## Frame

Scope:

- Selector-regression runtime-reduction change for `2026-06-27-selector-regression-runtime-reduction`.
- PR #115 status as observed after maintainer reported merge.
- Runtime, preservation, review, verify, and plan evidence created by the change.
- Next optimization direction after this completed selector-regression slice.

Evidence in scope:

- `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-profile.md`
- `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-baseline.yaml`
- `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-result.yaml`
- `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md`
- `docs/changes/2026-06-27-selector-regression-runtime-reduction/verify-report.md`
- `docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/code-review-r3.md`
- `docs/plans/2026-06-27-selector-regression-runtime-reduction.md`
- `gh pr view 115 --json number,state,mergedAt,mergeCommit,baseRefName,headRefName,statusCheckRollup,url`

Explicit exclusions:

- No new workflow policy is created by this session.
- No topic file is updated; the observations are useful, but this session does not need a new durable topic entry.
- No plan closeout, branch readiness, PR readiness, or CI readiness is claimed by this learn record.
- No broad-smoke parallelism, validation cache, persistent worker, or validator-composition implementation is proposed as already approved.

Prior learnings reviewed:

- `docs/learn/sessions/2026-06-26-zero-runtime-improvement-root-cause.md`: the prior runtime slice produced 0% feature-caused improvement because it added readiness and evidence infrastructure, not a runtime-speed actuator.
- `docs/learn/sessions/2026-06-26-validation-runtime-speed-best-practices.md`: safe runtime optimization order is to measure first, run cheap preconditions, select the smallest complete check set, avoid duplicate parsing/process startup, reuse only under complete identity, parallelize only independent work, and keep final broad verification separate.
- `docs/learn/sessions/2026-06-24-verify-repetition-cost.md`: repeated expensive validation before stable state creates avoidable cost; scoped validation and durable evidence should be sequenced carefully.
- `docs/learn/topics/ci-selector-routing.md`: new change-local evidence classes need deterministic selector routes.
- `docs/learn/topics/workflow-stage-order.md`: workflow stage order matters when proof artifacts depend on approved contracts.

## Observations

### O1 - The improvement came from a real runtime-speed actuator

Evidence:

- The previous runtime follow-through slice had no speed actuator; this selector slice targeted a concrete repeated-work mechanism.
- Baseline median for `python scripts/test-select-validation.py` was `164.73s` with 109 tests.
- Revised median was `36.23s` with 111 tests.
- The recorded reduction was `78.01%`.

Observation:

The significant improvement was possible because this slice changed the execution cost model, not the proof contract. It removed repeated repository-state discovery from pure selector cases while preserving selected-check identity, missing-route blockers, command-boundary coverage, cache-boundary behavior, broad-smoke classification, and final-verify boundaries.

### O2 - Profiling found multiplicative duplicate work inside one selector path

Evidence:

- Grouped profiling identified `ValidationSelectionTests` as the dominant bucket.
- Per-test timing found `test_first_slice_representative_categories_route_or_block_safely` spent about `105.804s` repeating repository preflight discovery across pure selector table rows.
- Reusing a frozen `RepositoryPreflightContext` for the same repository root reduced the representative table to `real 1.05s`.
- The implementation added an identity guard so a cached preflight context raises if used with a different repository root.

Observation:

The selector-regression suite had a high-leverage repeated cost: the same repository facts were rediscovered many times inside cases that only needed stable selector inputs. This is why the result could improve dramatically without deleting tests. The optimization was safe because reuse was bound to complete repository identity and guarded against cross-root misuse.

### O3 - Preservation evidence made the speed claim credible

Evidence:

- The default command still ran the complete selector-regression path.
- Test count increased from 109 to 111 after adding preservation and duration-regression coverage.
- `selector-regression-runtime-result.yaml` records `selected_identity_preserved: true`, `failure_sensitivity_preserved: true`, `behavioral_selector_identity_preserved: true`, `cli_boundary_subprocess_coverage_preserved: true`, `cache_boundary_preserved: true`, and `broad_smoke_classification_preserved: true`.
- The selected-CI explicit check passed without the prior timeout override.

Observation:

The improvement is defensible because the suite got faster while retaining the ordinary command path and adding coverage. Runtime reduction was attributed to less duplicate work rather than less validation.

### O4 - Timing exposed an adjacent defect that was worth fixing in-slice

Evidence:

- The first M3 revised timing attempt exposed `test_broad_smoke_verbose_prints_successful_child_output_in_order` failing on a negative broad-smoke elapsed value.
- The implementation replaced Bash `$SECONDS` duration math in `scripts/ci.sh` with explicit epoch-second helpers and a negative clamp.
- A regression test, `test_ci_wrapper_duration_reporting_does_not_use_bash_seconds`, was added.

Observation:

Performance evidence collection can reveal correctness bugs in validation output. Fixing the duration-reporting defect was justified because it affected the default command evidence path, while broad-smoke execution order and parallelism remained out of scope.

### O5 - Broad-smoke is now the next measured optimization target

Evidence:

- Final verify recorded `python scripts/test-select-validation.py` passing 111 tests in `36.99s`.
- Final verify recorded selected-CI focused checks completing in `50.37s`.
- Final verify recorded `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped` passing 11 checks in `354s`.
- The plan already deferred broad-smoke parallelism, validation caching, and broad validator composition to separate approved work.

Observation:

After selector-regression duplication was removed, broad-smoke dominates remaining wall time. The next optimization should target broad-smoke only after consuming the child-check classification and auditing side effects, shared outputs, temp roots, ordering requirements, and failure diagnostics.

### O6 - The merged PR is not yet evidence that the change reached main

Evidence:

- PR #115 was observed as merged with merge commit `730916f5e9ccf5b01104d97e681b7cbc9e9fe492`.
- PR #115 merged into `proposal/preflight-first-validation-runtime-optimization`, not `main`.
- PR #114, the earlier stacked-base PR into `main`, had already merged before PR #115.
- The PR #115 merge commit was not observed as an ancestor of `origin/main`.

Observation:

The selector-regression work is merged into its stacked base, but the change still needs an integration path to `main`. That should be handled by a follow-up PR from the stacked base branch to `main`, or by cherry-picking the selector-regression commits to a fresh main-based branch.

## Why The Result Improved Significantly

The baseline was not slow because every selector scenario required a fresh heavyweight command boundary. It was slow because pure selector tests repeatedly recomputed repository state inside table-driven coverage. Once profiling identified that repeated preflight discovery, the implementation could reuse a frozen repository context for the same root and keep subprocess tests only where command-boundary behavior was actually under test.

That moved the dominant case from about `105.804s` to `real 1.05s`, and the full default selector-regression command from a `164.73s` median to a `36.23s` median. The suite also added tests, so the improvement came from reducing duplicate work rather than removing proof.

## What To Do Next

Recommended next sequence:

1. Get the selector-regression change onto `main`.
   - PR #115 merged into its stacked base, but not into `main`.
   - Use either a follow-up PR from `proposal/preflight-first-validation-runtime-optimization` to `main` or a fresh main-based cherry-pick branch.

2. Start a focused broad-smoke safe-parallelism proposal.
   - Use the existing broad-smoke child classification evidence as the input.
   - Record per-child broad-smoke timings before changing execution.
   - Classify each child check for side effects, shared temp/output paths, cwd assumptions, ordering constraints, and resource conflicts.
   - Parallelize only checks classified as independent.
   - Preserve deterministic aggregate output, exit behavior, captured diagnostics, and final broad verification semantics.

3. Keep caching separate.
   - Cache adoption should wait for complete command/input/policy identity and normal-command-path integration.
   - Cache hits should remain excluded from final closeout proof unless a separate accepted contract changes that boundary.

4. Consider validation context composition only after broad-smoke profiling.
   - If startup/import/repository discovery remains dominant after safe broad-smoke parallelism, propose shared validation context composition.
   - Do not introduce persistent workers or cross-process protocols unless profiling proves the complexity is worth it.

5. Add a PR-stack hygiene follow-up if this repeats.
   - The stacked-branch merge outcome shows a process risk: a PR can merge into a base branch that has already merged to `main`.
   - If this recurs, route a separate proposal or workflow update to make the PR handoff check verify that the selected base branch still reaches the intended integration target.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | none | explicit `$learn` request | The session records the evidence-backed result; no new policy is needed. |
| O2 | observation | observation | candidate future runtime-optimization guidance | explicit `$learn` request | The pattern reinforces prior best-practice guidance about identity-safe reuse, but this session does not need a topic update. |
| O3 | observation | observation | none | explicit `$learn` request | Preservation evidence explains why the speed claim is credible. |
| O4 | observation | observation | none | explicit `$learn` request | The adjacent duration bug was handled inside the implementation and does not require a new follow-up. |
| O5 | direction | direction | future broad-smoke parallelism proposal | explicit `$learn` request | The next optimization target is clear, but broad-smoke parallelism still needs its own approved artifact. |
| O6 | process-follow-up | process-follow-up | follow-up PR or cherry-pick path to `main` | explicit `$learn` request | This is a concrete integration follow-up, not a learn-owned lifecycle closeout. |

## Route

- Topic updates: none.
- Authoritative artifact updates: none.
- Follow-up proposals opened by this session: none.
- Recommended process follow-up: ensure PR #115's merged content reaches `main`.
- Recommended optimization follow-up: propose broad-smoke safe parallel execution using child-check side-effect classification and fresh timing evidence.

## Validation

- `python scripts/select-validation.py --mode explicit --path docs/learn/sessions/2026-06-27-selector-regression-runtime-reduction-retrospective.md`: passed; selected `guide_system.validate`.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/learn/sessions/2026-06-27-selector-regression-runtime-reduction-retrospective.md`: passed; no artifact lifecycle files required validation for this path.
- `git diff --check -- docs/learn/sessions/2026-06-27-selector-regression-runtime-reduction-retrospective.md`: passed.
- `python scripts/validate-guide-system.py`: passed.
