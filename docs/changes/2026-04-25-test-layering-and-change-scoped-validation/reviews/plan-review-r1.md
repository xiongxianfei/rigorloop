# Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review skill
Target: docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md
Status: revise

## Scope

Reviewed the execution plan against the approved spec, approved architecture, accepted proposal, current review-resolution state, and repository governance.

## Dimension Results

| Dimension | Result | Notes |
| --- | --- | --- |
| Self-contained context | pass | The plan names source artifacts, dependencies, current repository context, and active change-local records. |
| Source alignment | pass | Milestones map to the approved selector, wrapper, broad-smoke, manual-proof, and generated-output requirements. |
| Milestone size | pass | The four milestones are reviewable and split by selector, wrapper, workflow guidance, and closeout. |
| Sequencing | pass | Selector core precedes wrapper adoption; workflow guidance follows real selector and wrapper behavior. |
| Scope discipline | pass | Non-goals protect broad-smoke coverage, runtime/app test selection, release-only smoke, and undefined fallback behavior. |
| Validation quality | concern | Negative-path checks are listed as raw validation commands even though the contract requires nonzero exit codes. |
| TDD readiness | concern | The plan identifies selector and wrapper regression tests, but the negative-path pass/fail harness is not explicit. |
| Risk coverage | pass | Rollback and recovery are named for selector gaps, wrapper regression, broad-smoke attribution, manual proof, and generated output. |
| Architecture alignment | pass | The plan follows the approved selector module, wrapper boundary, trigger-source model, manual-proof ownership, and v1 unclassified blocking decisions. |
| Operational readiness | pass | CI wrapper behavior, broad-smoke handoff, generated adapters, and final lifecycle closeout are included. |
| Plan maintainability | pass | Progress, decisions, discoveries, validation notes, and milestone closeout fields are present. |

## Findings

### PR1-F1: Negative validation commands are not wrapped as passing assertions

Finding ID: PR1-F1

Evidence: The plan lists `python scripts/select-validation.py --mode explicit --path experimental/runtime/example.txt` as an M1 validation command. The approved spec requires blocked selector results to exit with code `2` (`specs/test-layering-and-change-scoped-validation.md:232`-`236`) and the approved architecture requires unclassified paths to return `blocked` with `unclassified-path` (`docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md:227`-`234`). The M2 validation list similarly includes `bash scripts/ci.sh --mode explicit --path experimental/runtime/example.txt` as an expected blocking failure. As written, these milestone validation lists mix passing checks with commands that should return nonzero, so a maintainer cannot run the listed commands as a reliable pass/fail gate.

Required outcome: Negative-path behavior must be validated through a command or test harness that exits `0` when the expected nonzero selector or wrapper result is observed, and fails otherwise.

Suggested resolution: Move the unclassified-path selector and wrapper assertions into `python scripts/test-select-validation.py`, or add a small explicit shell/Python harness that captures exit code, stdout JSON, and `unclassified-path` details. Keep raw `select-validation.py` and `ci.sh` examples for manual inspection only if they are labeled as expected nonzero demonstrations rather than milestone pass commands.

## Recommendation

Revise the plan before `test-spec`. The fix should make negative-path validation commands executable as a reliable milestone gate, then rerun `plan-review`.
