# Code Review R2

Review ID: code-review-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M2 commit `9b71164785140837d1098543aebc320f6ea7cf87`
Status: changes-requested
Review date: 2026-05-05

## Scope

Reviewed the M2 implementation for test and CI speed optimization against the approved spec, active test spec, active implementation plan, change-local evidence, actual committed diff, and recorded validation evidence.

## Review inputs

- Diff range: `HEAD^..HEAD` at `9b71164785140837d1098543aebc320f6ea7cf87`.
- Review surface: `scripts/ci.sh`, `scripts/test-select-validation.py`, the active spec/test-spec/plan, plan index, change metadata, and M2 explain-change evidence.
- Tracked governing branch state: `CONSTITUTION.md`, `AGENTS.md`, `specs/test-and-ci-speed-optimization.md`, `specs/test-and-ci-speed-optimization.test.md`, `docs/plans/2026-05-04-test-and-ci-speed-optimization.md`, `docs/plan.md`, and `docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml` are present in the reviewed branch state.
- Architecture / ADR: no architecture update required because M2 preserves the existing selector, catalog, wrapper, and hosted CI boundaries.
- Validation evidence: M2 red/green `python scripts/test-select-validation.py`, focused wrapper proof, selector-selected inspection, wrapper-selected validation including `broad_smoke.repo`, change metadata validation, artifact lifecycle validation, and diff/whitespace checks are recorded in the active plan and change metadata.

## Diff summary

M2 replaces direct selected-check execution with an internal `CheckPlan`/`CheckResult` model. Selected checks now execute through captured stdout/stderr buffers, produce stable summary rows, hide successful output unless `--verbose` is supplied, report failed output after the summary, enforce per-check timeouts, distinguish ordinary exits, signal kills, timeouts, and unavailable commands, and preserve the non-recursive `broad_smoke.repo` delegation boundary.

## Findings

### CR2-F1: M2 records T11/T12 coverage without direct proof for two named edge cases

Finding ID: CR2-F1

Evidence: The test spec requires `T11` to cover decode failures and large-output isolation, including a fake script that emits enough output to exercise the capture path and assertions that one check's output does not appear inside another check's report section. The M2 tests added in `scripts/test-select-validation.py` cover invalid UTF-8 output but do not add the large-output two-check isolation branch. The test spec also requires `T12` to prove the default 60-second timeout either by using an omitted-timeout long-running check or by using a shorter override while separately asserting the default constant is 60. The M2 timeout test uses `--timeout 1` but does not assert the default constant.

Required outcome: Add direct proof for the missing M2 evidence, or narrow the M2 evidence claims so they do not claim completed `T11`/`T12` coverage. The preferred resolution is to add focused tests because both gaps are small and within the approved M2 scope.

Safe resolution: Extend `scripts/test-select-validation.py` with a large-output per-check isolation assertion and a default timeout constant assertion, rerun the focused selector regression suite, rerun selector-selected validation for the touched test/review/change artifacts, and update the active plan plus change metadata with the new validation evidence.

## Checklist coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | concern | Runner behavior matches the M2 subset, but `R8c`/`EC8` and `R3a` proof are incomplete while M2 evidence claims the corresponding tests. |
| Test coverage | concern | `T11` invalid-byte coverage exists, and `T12` timeout override coverage exists, but large-output isolation and the default 60-second timeout constant are not directly proved. |
| Edge cases | concern | Named edge cases `EC8` and default-timeout proof from `T12` are actionable proof gaps. |
| Error handling | pass | Nonzero exit, unavailable command, timeout override, and signal-kill behavior have focused tests. |
| Architecture boundaries | pass | Execution behavior remains in `scripts/ci.sh`; selector trust remains through `catalog_command`; no new module boundary is introduced. |
| Compatibility | pass | Existing modes and selector-facing arguments remain unchanged; `broad_smoke.repo` remains non-recursive. |
| Security/privacy | pass | No secrets, external services, network behavior, or tracked output capture paths are introduced. |
| Generated output drift | pass | No generated outputs are touched. |
| Unrelated changes | pass | The reviewed M2 diff is scoped to wrapper/test/evidence surfaces. |
| Validation evidence | concern | Recorded validation is credible for the implemented runner path but lacks the two direct proof points above. |

## Recommended next stage

Enter review-resolution for CR2-F1, then rerun `code-review`.
