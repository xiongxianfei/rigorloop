# Code Review M3 R2

Review ID: code-review-m3-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M3 commits through `fc700873`
Reviewed artifact: M3 commits through `fc700873`
Reviewed milestone: M3. `prepare-release` pending artifact generation
Status: clean-with-notes
Review status: clean-with-notes
Review date: 2026-06-29
Recording status: recorded
Material findings: none
Immediate next stage: implement M4

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m3-r2.md, docs/changes/2026-06-29-release-transaction-automation/review-log.md, docs/plans/2026-06-29-release-transaction-automation.md, docs/plan.md, docs/changes/2026-06-29-release-transaction-automation/change.yaml
- Open blockers: none
- Next stage: implement M4
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m3-r2.md
- Review log: docs/changes/2026-06-29-release-transaction-automation/review-log.md
- Review resolution: not-required
- Reviewed milestone: M3. `prepare-release` pending artifact generation
- Milestone closeout: closed
- Remaining implementation milestones: M4, M5, M6
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review Inputs

- Diff range: M3 commits through `fc700873`, including `1c494c68`, `ee939607`, and the `CR-RTA-M3-F1` resolution commit `fc700873`.
- Review surface: `scripts/release_transaction.py`, `scripts/prepare-release.py`, `scripts/test-release-transaction.py`, active plan M3 state, review log, review-resolution evidence, and recorded validation evidence.
- Tracked governing branch state: approved proposal, approved spec, approved architecture/ADR, approved test spec, active plan, change metadata, closed M1, closed M2, code-review-m3-r1, and the M3 review-resolution commit are tracked through `fc700873`.
- Governing spec: `specs/release-transaction-automation.md` requirements `R8`-`R17`, `R43`, `R44`; acceptance criteria `AC2`-`AC5`, `AC18`.
- Test spec: `specs/release-transaction-automation.test.md` `RTA-T005` through `RTA-T010`.
- Plan milestone: `docs/plans/2026-06-29-release-transaction-automation.md` M3.
- Prior finding: `CR-RTA-M3-F1` in `docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m3-r1.md`.
- Review-resolution evidence: `docs/changes/2026-06-29-release-transaction-automation/review-resolution.md#code-review-m3-r1`.
- Validation evidence challenged: `python scripts/test-release-transaction.py`, `python scripts/prepare-release.py --help`, Python compilation, selector manual-routing result, change metadata validation, lifecycle explicit-path validation, review artifact validation, and whitespace validation.
- Validation spot checks run during review: `python scripts/test-release-transaction.py`, `python scripts/prepare-release.py --help`, `python -m py_compile scripts/release_transaction.py scripts/test-release-transaction.py scripts/prepare-release.py`, `git diff --check --`, and a temporary generated fixture with an explicit `<pending command>` placeholder.

## Diff Summary

M3 adds the fixture-safe `prepare-release` generator and CLI wrapper, plus the `CR-RTA-M3-F1` resolution. The resolution replaces global npm-publication substring checks with structured target-bound validation. It extracts the generated YAML block, validates each expected target independently, rejects missing, duplicate, and unknown targets, checks target-specific command, npm version, result, and closeout-blocked values, and compares the Markdown table projection against the canonical YAML target data. Tests add temporary generated-repository mutations for published target result, `npx -y`, missing target, duplicate target, unknown target, and table/YAML projection mismatch.

## Findings

No blocking or required-change findings.

## Prior Finding Closeout

| Finding ID | R2 result | Evidence |
| --- | --- | --- |
| `CR-RTA-M3-F1` | resolved | `scripts/release_transaction.py` now routes npm-publication validation through `_validate_pending_npm_publication`, `_parse_pending_target_init_smoke`, `_validate_pending_target_rows`, and `_validate_pending_table_projection`; `scripts/test-release-transaction.py` adds direct negative tests for target result `published`, `npx -y`, missing target, duplicate target, unknown target, and table projection mismatch; `python scripts/test-release-transaction.py` passed with 34 tests. |

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | pass | M3 remains scoped to `prepare-release` pending artifact generation and pending evidence validation for `R8`-`R17`; no preflight, closeout, CI, publication, or full-gate behavior is introduced. |
| Test coverage | pass | Tests prove idempotent generation, exact touched paths, release-note narrative preservation, historical evidence immutability, check mode, no external actions, happy-path pending evidence, and the named negative pending-evidence cases from `CR-RTA-M3-F1`. |
| Edge cases | pass | Missing, duplicate, and unknown targets fail; one target's published result cannot be masked by another target; `npx -y` fails; table/YAML mismatch fails; a reviewer spot check confirmed `<pending command>` fails with target-specific diagnostics. |
| Error handling | pass | Pending evidence diagnostics name the file, target, and invalid field or projection mismatch. Missing YAML blocks, missing tables, malformed target fields, and unsupported target rows produce errors rather than silent acceptance. |
| Architecture boundaries | pass | The implementation keeps release transaction helper logic in `scripts/release_transaction.py` with a thin CLI wrapper; it does not add dependencies or rewrite the existing full release validator. |
| Compatibility | pass | Existing release verification and publication boundaries remain unchanged; generated pending evidence keeps the existing YAML-plus-table shape while making YAML canonical for validation. |
| Security/privacy | pass | The reviewed diff adds no secrets, credentials, network calls, npm registry reads, GitHub release calls, tags, pushes, or publication actions. |
| Derived artifact currency | pass | Temporary generated repositories are used for fixture-safe proof. The plan records that no static `tests/fixtures/release-transaction/evidence` files were added because generated temp fixtures own this M3 proof. |
| Unrelated changes | pass | The reviewed diff is scoped to M3 pending-evidence validation, tests, review-resolution state, and lifecycle handoff updates. |
| Validation evidence | pass | Focused tests, CLI help, Python compilation, change metadata validation, lifecycle explicit-path validation, review artifact validation, and whitespace validation passed. Selector output still reports known manual-routing/unclassified fixture-path limits, with `python scripts/test-release-transaction.py` owning M3 proof per the plan. |

## No-Finding Rationale

The reviewed implementation now binds pending npm-publication validation to each target instead of relying on global fragments, and direct tests cover the failure modes that caused `CR-RTA-M3-F1`. The generated happy path still validates, human-authored release notes and historical evidence remain protected by the existing M3 tests, and the change does not cross into M4-M6 release automation behavior.

## Residual Risks

M4-M6 remain unimplemented and unreviewed. The selector still has manual-routing debt for release transaction scripts and no static fixture classification for `tests/fixtures/release-transaction/evidence`; this does not block M3 because the approved M3 proof uses generated temporary repositories and the focused release transaction test suite.

## Recommended Next Stage

Close M3 and proceed to `implement M4`. This review does not claim final closeout, verify readiness, branch readiness, PR readiness, CI success, or M4-M6 readiness.
