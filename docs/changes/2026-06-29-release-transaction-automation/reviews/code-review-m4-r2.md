# Code Review M4 R2

Review ID: code-review-m4-r2
Stage: code-review
Round: M4 R2
Reviewer: Codex code-review skill
Target: M4 resolution commit `8ebd0eb6`
Reviewed artifact: M4 review-resolution diff `8ebd0eb6`
Reviewed milestone: M4. Release preflight command
Status: clean-with-notes
Review status: clean-with-notes
Review date: 2026-06-29
Recording status: recorded
Material findings: None
Immediate next stage: implement M5

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m4-r2.md, docs/changes/2026-06-29-release-transaction-automation/review-log.md, docs/changes/2026-06-29-release-transaction-automation/review-resolution.md, docs/plans/2026-06-29-release-transaction-automation.md, docs/plan.md, docs/changes/2026-06-29-release-transaction-automation/change.yaml
- Open blockers: none
- Next stage: implement M5
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m4-r2.md
- Review log: docs/changes/2026-06-29-release-transaction-automation/review-log.md
- Review resolution: docs/changes/2026-06-29-release-transaction-automation/review-resolution.md#code-review-m4-r2
- Reviewed milestone: M4. Release preflight command
- Milestone closeout: closed
- Remaining implementation milestones: M5, M6
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review Inputs

- Diff range: `HEAD^..HEAD` at `8ebd0eb6`.
- Review surface: `scripts/release_transaction.py`, `scripts/release-preflight.py`, `scripts/test-release-transaction.py`, M4 review-resolution lifecycle updates, and M4 validation evidence.
- Governing spec: `specs/release-transaction-automation.md` requirements `R18`-`R27`.
- Test spec: `specs/release-transaction-automation.test.md` `RTA-T011` through `RTA-T015`.
- Active plan milestone: `docs/plans/2026-06-29-release-transaction-automation.md` M4.
- Prior findings under rereview: `CR-RTA-M4-F1`, `CR-RTA-M4-F2`.
- Validation spot checks run during rereview: `python scripts/test-release-transaction.py`, `python scripts/release-preflight.py --help`, and `python -m py_compile scripts/release_transaction.py scripts/test-release-transaction.py scripts/prepare-release.py scripts/release-preflight.py`.

## Diff Summary

The M4 resolution adds default Git changed-file discovery for the release preflight CLI, keeps explicit `--changed-file` as a deterministic override, and fails clearly when changed files cannot be derived outside a Git working tree. It also adds direct M4 preflight tests for malformed profile, incomplete profile, missing required local input, non-Git CLI invocation without explicit changed files, and default CLI discovery of a changed unauthorized current-version literal.

## Findings

No blocking or required-change findings.

## Prior Finding Reconciliation

`CR-RTA-M4-F1` is resolved. The default CLI path now calls `discover_changed_files(root)` when `--changed-file` is absent in `scripts/release-preflight.py:43` through `scripts/release-preflight.py:53`, then passes those files into `release_preflight` at `scripts/release-preflight.py:54` through `scripts/release-preflight.py:59`. `discover_changed_files` uses Git staged, unstaged tracked, and untracked path discovery in `scripts/release_transaction.py:335` through `scripts/release_transaction.py:367`. Direct proof exists in `test_release_preflight_cli_discovers_changed_unauthorized_literal` at `scripts/test-release-transaction.py:729` through `scripts/test-release-transaction.py:775`, and the non-Git failure path is covered at `scripts/test-release-transaction.py:600` through `scripts/test-release-transaction.py:620`.

`CR-RTA-M4-F2` is resolved. Direct preflight-path negative tests now cover malformed profile at `scripts/test-release-transaction.py:628` through `scripts/test-release-transaction.py:638`, incomplete profile at `scripts/test-release-transaction.py:640` through `scripts/test-release-transaction.py:645`, and missing required local input at `scripts/test-release-transaction.py:647` through `scripts/test-release-transaction.py:656`.

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | pass | The preferred Python CLI remains `python scripts/release-preflight.py <tag>` and now derives changed files by default, satisfying `R18` and `R22`. The preflight path continues to check profile/package/pending evidence/tag/output/local-input surfaces required by `R21`. |
| Test coverage | pass | `python scripts/test-release-transaction.py` now runs 50 tests and directly covers both prior M4 findings plus existing clean/idempotent, package mismatch, metadata pointer, pending evidence, dirty output, local tag, remote tag, and helper literal-audit cases. |
| Edge cases | pass | Non-Git roots without explicit changed files fail clearly, explicit changed-file input remains supported, and malformed/incomplete/missing-input cases are direct preflight tests rather than lower-level profile-loader inference only. |
| Error handling | pass | Git discovery failures raise `ReleasePreflightChangedFilesError` and the CLI reports a clear failure before running release checks. Missing local metadata input diagnostics name the missing path. |
| Architecture boundaries | pass | The patch stays within M4 preflight tooling and tests. It does not introduce M5/M6 release gate parity, timing, CI, publication closeout, or public smoke behavior. |
| Compatibility | pass | Existing explicit `--changed-file` fixture behavior is preserved while the documented default command becomes stronger. CLI output adds diagnostic changed-file source and changed-file list lines. |
| Security/privacy | pass | No secrets, credentials, publication actions, package publication, or public smoke are introduced. Git commands inspect local working-tree state only. |
| Derived artifact currency | pass | Preflight remains side-effect-light; the clean fixture idempotency test still compares file contents before and after preflight. |
| Unrelated changes | pass | The implementation diff is scoped to preflight changed-file discovery, M4 regression tests, and lifecycle metadata. |
| Validation evidence | pass | Rereview spot checks passed for focused tests, CLI help, and Python compilation. Selector validation remains known manual-routing debt and is recorded as blocked with tracked-artifact preflights passing. |

## No-Finding Rationale

The resolution directly fixes the prior default-CLI blind spot and the named preflight proof gaps without broadening release behavior. The tests exercise the user-facing CLI path for Git-discovered changed files and the explicit failure path when discovery is unavailable, and they add direct preflight coverage for the named malformed/incomplete/missing-input cases. The implementation remains a cheap local/profile/schema gate and does not touch release publication, CI parity, timing, or full release verification behavior.

## Residual Risks

Selector routing still lacks deterministic checks for the release transaction scripts and static fixture directories, so selector validation remains a known manual-routing limitation rather than a M4 behavior blocker. M5 and M6 remain unimplemented and unreviewed.

## Validation

- `python scripts/test-release-transaction.py` passed during rereview: 50 tests.
- `python scripts/release-preflight.py --help` passed.
- `python -m py_compile scripts/release_transaction.py scripts/test-release-transaction.py scripts/prepare-release.py scripts/release-preflight.py` passed.

## Recommended Next Stage

Close M4 and proceed to `implement M5` for full release gate parity and timing evidence.
