# Code Review R3

Review ID: code-review-r3
Stage: code-review
Round: 3
Reviewer: Codex code-review skill
Target: M2 committed range `8b4a03f..HEAD`
Status: changes-requested

## Scope

Reviewed the M2 CI wrapper selector-consumption implementation against the approved selector spec, active test spec, architecture, plan milestone, committed diff, and recorded validation evidence.

## Review inputs

- Diff range: `8b4a03f..HEAD`
- Review surface: `.github/workflows/ci.yml`, `scripts/ci.sh`, `scripts/validation_selection.py`, `scripts/test-select-validation.py`, the active plan, and change metadata
- Tracked governing branch state: spec, architecture, test spec, plan, and prior review records are present in tracked branch commits
- Spec: `specs/test-layering-and-change-scoped-validation.md`
- Test spec: `specs/test-layering-and-change-scoped-validation.test.md`
- Plan milestone: `docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md` M2
- Validation evidence inspected: `python scripts/test-select-validation.py`, `bash scripts/ci.sh --mode explicit --path specs/test-layering-and-change-scoped-validation.md`, `bash scripts/ci.sh --mode explicit --path scripts/ci.sh`, and `bash scripts/ci.sh --mode broad-smoke` are recorded as passing in `change.yaml`

## Diff summary

M2 turns `scripts/ci.sh` into a selector-consuming wrapper for normal modes, keeps `--mode broad-smoke` as the non-recursive broad-smoke execution path, updates hosted CI to pass PR/main ranges into the wrapper, adds `ci-wrapper` selector classification, and extends selector regression tests for wrapper execution, blocked/fallback/malformed selector output, failing selected checks, unavailable selected commands, argument forwarding, and broad-smoke delegation.

## Findings

### CR3-F1 - Missing direct proof that selector JSON commands cannot bypass the trusted catalog

Finding ID: CR3-F1
Severity: major

Evidence: `specs/test-layering-and-change-scoped-validation.test.md` requires wrapper tests to prove command execution comes from trusted catalog data and does not use arbitrary JSON command text through `eval`. The reviewed M2 tests cover selected command success, blocked/fallback/malformed selector output, selected command failure, unavailable catalog commands, argument forwarding, and broad-smoke delegation, but no test provides selector fixture output with a known check ID and a tampered `command` value that must be rejected before execution.

Required outcome: The wrapper regression suite must directly prove that selected check commands are derived from the versioned catalog contract and that a selector payload cannot substitute arbitrary command text for a valid check ID.

Suggested safe resolution: Add a focused `scripts/test-select-validation.py` wrapper test that feeds `scripts/ci.sh` fixture JSON with a valid check ID such as `skills.validate` and a non-catalog command string, then asserts the wrapper exits nonzero with a catalog-mismatch error before running the selected check.

## Checklist coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | concern | Wrapper mode separation and non-recursive broad smoke match the spec, but the trusted-catalog execution invariant lacks direct regression proof. |
| Test coverage | concern | Existing M2 tests cover most wrapper success and failure paths but miss the explicit arbitrary JSON command rejection case from the security verification section. |
| Edge cases | pass | Blocked, fallback, malformed selector output, selected command failure, unavailable command, argument forwarding, and non-recursive broad smoke are covered. |
| Error handling | pass | The wrapper fails safely for blocked, fallback, malformed JSON, unavailable commands, and failing selected checks. |
| Architecture boundaries | pass | The wrapper consumes selector JSON and validates commands against shared catalog data without introducing a second path-selection engine. |
| Compatibility | pass | No-argument `scripts/ci.sh` preserves broad-smoke behavior for legacy local use, and hosted CI now passes explicit PR/main mode inputs. |
| Security/privacy | concern | The code has catalog validation, but the required security proof for tampered selector command text is missing. |
| Generated output drift | pass | No canonical skill or adapter source changed in M2. |
| Unrelated changes | pass | The reviewed diff is limited to M2 wrapper, selector classification, hosted CI, tests, and milestone artifacts. |
| Validation evidence | concern | Recorded commands pass, but they do not include the missing catalog-mismatch regression. |

## Recommended next stage

Enter review-resolution for `CR3-F1`, add the missing regression test, run the M2 targeted validation, and rerun `code-review` with a strictly later round.
