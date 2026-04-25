# Code Review R1

Review ID: code-review-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: HEAD commit 03a8884 (M1: add validation selector)
Status: changes-requested

## Scope

Reviewed the M1 selector implementation against the approved spec, approved architecture, active plan, active test spec, actual `HEAD^..HEAD` diff, and recorded validation evidence.

## Review inputs

- Diff range: `HEAD^..HEAD`
- Review surface: M1 selector scripts, selector regression tests, and change-local artifacts in commit `03a8884`
- Tracked governing branch state: spec, architecture, plan, test spec, and existing review records are tracked in `HEAD`
- Spec: `specs/test-layering-and-change-scoped-validation.md`
- Test spec: `specs/test-layering-and-change-scoped-validation.test.md`
- Architecture: `docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md`
- Plan milestone: `docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md` M1
- Validation evidence inspected: `python scripts/test-select-validation.py` passed; direct selector probe for `docs/releases/release-notes.md` returned `status: "ok"` and exit `0`

## Diff summary

M1 adds `scripts/validation_selection.py`, `scripts/select-validation.py`, and `scripts/test-select-validation.py`. The selector defines the v1 check catalog, mode handling, changed-path discovery, first-slice path classification, affected roots, release version inference, broad-smoke source attribution, JSON rendering, and v1 blocking behavior for unclassified paths. The change also adds the proposal, spec, architecture, test spec, plan, and change-local review artifacts for this initiative.

## Findings

### CR1-F1: Ambiguous release paths are accepted with a fake release version

Finding ID: CR1-F1
Severity: blocker

Evidence: The approved spec requires the selector to block when a release version cannot be inferred (`specs/test-layering-and-change-scoped-validation.md:369` and `specs/test-layering-and-change-scoped-validation.md:371`). The active test spec names this edge case as EC4 and routes it to T8/T9 (`specs/test-layering-and-change-scoped-validation.test.md:69`, `specs/test-layering-and-change-scoped-validation.test.md:229`). However, `python scripts/select-validation.py --mode explicit --path docs/releases/release-notes.md` returned exit `0`, `status: "ok"`, and selected `release.validate` with command `python scripts/validate-release.py --version release-notes.md`. In the implementation, `_path_category` classifies every `docs/releases/` path as `release`, and `_release_version_from_path` returns `parts[2]` even when the path is a direct file under `docs/releases/` (`scripts/validation_selection.py:648`, `scripts/validation_selection.py:693`).

Required outcome: A release path without an inferable `docs/releases/<version>/...` version must not produce an `ok` selector result or a `release.validate` command with a file name as the version. In v1, it must return a blocking result requiring manual routing because no conservative fallback set is defined.

Suggested resolution: Add a regression test for an ambiguous release path such as `docs/releases/release-notes.md` expecting exit `2`, `status: "blocked"`, and a release-version/manual-routing blocking result. Then tighten release version inference so only paths nested under `docs/releases/<version>/...` can infer a version, and rerun `python scripts/test-select-validation.py`.

### CR1-F2: M1 tests do not directly prove required valid PR/main modes and first-slice category coverage

Finding ID: CR1-F2
Severity: major

Evidence: The test spec requires valid selector invocations for `pr` and `main` mode with `--base` and `--head` (`specs/test-layering-and-change-scoped-validation.test.md:102`) and requires representative first-slice category coverage for generated adapters, generated `.codex/skills`, workflow summaries, governance files, schemas, and validation/generation scripts (`specs/test-layering-and-change-scoped-validation.test.md:187`, `specs/test-layering-and-change-scoped-validation.test.md:206`, `specs/test-layering-and-change-scoped-validation.test.md:254`). The committed test file only invokes `pr` for the missing-input error case (`scripts/test-select-validation.py:138`) and has no valid `--mode main` coverage. It also lacks representative assertions for `dist/adapters/**`, `.codex/skills/**`, `docs/workflows.md`, `CONSTITUTION.md`, and `schemas/**`; the category tests currently cover a skill path, change metadata, one review/lifecycle/release bundle, selector and one validator script, `AGENTS.md`, release mode, local mode, and outside-path normalization (`scripts/test-select-validation.py:112`, `scripts/test-select-validation.py:171`, `scripts/test-select-validation.py:193`, `scripts/test-select-validation.py:211`, `scripts/test-select-validation.py:219`, `scripts/test-select-validation.py:251`, `scripts/test-select-validation.py:266`, `scripts/test-select-validation.py:284`).

Required outcome: Named selector edge cases and first-slice categories from the M1 test spec need direct proof from targeted tests before this milestone can receive a clean code-review result.

Suggested resolution: Add compact table-driven selector tests for the missing representative categories, including generated adapter output and generated `.codex/skills` paths. Add a small temporary Git range fixture that invokes valid `pr` and `main` modes with `--base` and `--head`, proves they use the same selector module, and asserts `main` records the authoritative broad-smoke mode source.

## Checklist coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | block | CR1-F1 violates R12a by accepting a release path with no inferable version. |
| Test coverage | concern | CR1-F2 leaves named T2/T6/T7/T9 coverage without direct proof. |
| Edge cases | block | EC4 fails in the direct selector probe; EC11/EC12 lack direct valid-mode proof. |
| Error handling | concern | Ambiguous release input is treated as an `ok` release validation rather than a blocking state. |
| Architecture boundaries | pass | The implementation keeps routing in `validation_selection.py` and the CLI wrapper thin. |
| Compatibility | concern | Contributors can receive misleading release validation commands for ambiguous release paths. |
| Security/privacy | pass | No secrets, credentials, network use, or unsafe logging were found in the reviewed diff. |
| Generated output drift | pass | M1 does not change canonical shipped skill guidance or generated adapter output. |
| Unrelated changes | pass | The diff is scoped to M1 selector implementation and its lifecycle artifacts. |
| Validation evidence | concern | `python scripts/test-select-validation.py` passes, but it does not catch CR1-F1 or directly cover CR1-F2. |

## Recommended next stage

Stop after this isolated code review. Resolve CR1-F1 and CR1-F2 in the implementation, update `review-resolution.md` with accepted actions and validation evidence, then rerun `code-review` with a strictly later round.
