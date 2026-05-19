# Code Review M1 R2: Assets-First Progressive Disclosure Pilot

Review ID: code-review-m1-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: commits e70545d6c3e75cd33d8b0d5437f9ca88d0363a85 and 7e36d2805ab3db800f84db40c1d0906c54282fc6
Status: clean-with-notes
Reviewed artifact: M1. Asset Contract Validation And Test Spec Support
Review date: 2026-05-19
Recording status: recorded

## Result

- Skill: code-review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/reviews/code-review-m1-r2.md
- Review log: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/review-log.md
- Review resolution: not-required
- Open blockers: none
- Immediate next stage: implement M2

## Review inputs

- Diff/review surface: M1 implementation commit `e70545d6c3e75cd33d8b0d5437f9ca88d0363a85` and APD-CR1 resolution commit `7e36d2805ab3db800f84db40c1d0906c54282fc6`.
- Tracked governing branch state: proposal, approved spec amendment, approved test-spec amendment, active plan, M1 implementation, APD-CR1 review record, review-resolution, and M1 rerun handoff are tracked.
- Governing artifacts: `specs/skill-contract.md` R37-R45, `specs/skill-contract.test.md` T33-T34, and `docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md` M1.
- Validation evidence: active plan and change metadata record passing M1 commands after APD-CR1 resolution, including `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, change metadata validation, review artifact validation, artifact lifecycle validation, `git diff --check --`, and selected CI checks.

## Diff summary

M1 adds deterministic validator support and fixtures for the assets-first `plan` pilot. The APD-CR1 follow-up adds `tests/fixtures/skills/published-design/plan-assets-missing-resource-map-entry/`, a `name: plan` fixture with exactly the approved four assets where `assets/decision-log-row.md` is intentionally omitted from the `Resource map`. `scripts/test-skill-validator.py` now asserts that this fixture fails with the omitted asset path named in the error. Lifecycle evidence was updated to mark APD-CR1 resolved and return M1 to code-review.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | The reviewed M1 surface implements deterministic proof for R37-R39 and R42-R43 without changing the real `skills/plan` body or adding real assets before M2. |
| Test coverage | pass | `scripts/test-skill-validator.py` includes positive plan asset coverage plus negative cases for exact count, metadata, non-normative status, non-`COPY`, missing fields, missing resource-map entry, placeholders, root dependency, fingerprint mismatch, and section-set mismatch. |
| Edge cases | pass | APD-CR1 is directly covered: the new fixture has all four approved assets and omits only `assets/decision-log-row.md` from the `Resource map`; the assertion checks that the omitted path is reported. |
| Error handling | pass | Validator failure paths produce stable path-specific errors for malformed or unmapped assets while allowing flat `plan` before M2. |
| Architecture boundaries | pass | The change stays within static validator/test fixtures and lifecycle evidence; adapter roots, lockfiles, CLI behavior, generated adapter output, and real `skills/plan` assets are untouched in M1. |
| Compatibility | pass | `_validate_plan_asset_pilot` activates only for `name: plan` with an `assets/` directory, preserving existing flat skill validation before M2. |
| Security/privacy | pass | The fixture and tests introduce no secrets or private data, and root dependency rejection remains covered. |
| Derived artifact currency | pass | No generated public adapter outputs are hand-edited; generated packaging proof remains M3 scope. |
| Unrelated changes | pass | The reviewed commits are limited to the lifecycle packet, validator/test support, plan-asset fixtures, and APD-CR1 review-resolution evidence. |
| Validation evidence | pass | M1 evidence names the targeted commands and selected CI check IDs after APD-CR1 resolution. |

## No-finding rationale

The APD-CR1 proof gap is closed by a plan-specific fixture and assertion that exercise the exact missing resource-map-entry case required by T34 and M1. The full M1 validator fixture set now distinguishes valid packaged `plan` assets from missing, unmapped, malformed, or drifted assets without broad semantic scoring or changes to real skill assets.

## Residual risks

M2 still needs to apply the asset split to real `skills/plan` and prove common-path reduction. M3 still owns adapter packaging, token, behavior-parity, and historical coverage proof.

## Milestone handoff

- Reviewed milestone: M1. Asset Contract Validation And Test Spec Support
- Review status: clean-with-notes
- Milestone state after review: closed
- Required review-resolution: no
- Remaining in-scope implementation milestones: M2, M3
- Next stage: implement M2
- Final closeout readiness: not ready; M2 and M3 remain unimplemented, and explain-change, verify, and PR handoff have not run.
