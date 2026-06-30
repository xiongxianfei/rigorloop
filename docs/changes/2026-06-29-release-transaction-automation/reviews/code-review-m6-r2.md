# Code Review M6 R2

Review ID: code-review-m6-r2
Stage: code-review
Round: M6 R2
Reviewer: Codex code-review skill
Target: M6 resolution commit `c8d63893`
Reviewed artifact: M6 review-resolution diff `c8d63893`
Reviewed milestone: M6. Published evidence closeout and behavior preservation
Status: clean-with-notes
Review status: clean-with-notes
Review date: 2026-06-29
Recording status: recorded
Material findings: None
Immediate next stage: explain-change

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m6-r2.md, docs/changes/2026-06-29-release-transaction-automation/review-log.md, docs/changes/2026-06-29-release-transaction-automation/review-resolution.md, docs/plans/2026-06-29-release-transaction-automation.md, docs/plan.md, docs/changes/2026-06-29-release-transaction-automation/change.yaml
- Open blockers: none
- Next stage: explain-change
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m6-r2.md
- Review log: docs/changes/2026-06-29-release-transaction-automation/review-log.md
- Review resolution: docs/changes/2026-06-29-release-transaction-automation/review-resolution.md#code-review-m6-r2
- Reviewed milestone: M6. Published evidence closeout and behavior preservation
- Milestone closeout: closed
- Remaining implementation milestones: none
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review Inputs

- Diff range: `HEAD^..HEAD` at `c8d63893`.
- Review surface: `scripts/close-release-publication.py`, `scripts/release_transaction.py`, `scripts/test-release-transaction.py`, M6 review-resolution lifecycle updates, active plan M6 state, and change metadata.
- Governing spec: `specs/release-transaction-automation.md` requirements `R31` through `R38`, plus `R43` and `R44`.
- Test spec: `specs/release-transaction-automation.test.md` `RTA-T018`, `RTA-T020`, `RTA-T021`, and `RTA-T023`.
- Active plan milestone: `docs/plans/2026-06-29-release-transaction-automation.md` M6.
- Prior finding under rereview: `CR-RTA-M6-F1`.
- Validation evidence inspected: `python scripts/test-release-transaction.py` passed with 84 tests; `python scripts/close-release-publication.py --help` passed; Python compilation passed; release-verify dry-run passed; selector validation selected adapter/release regression while blocked on known release transaction script manual routing; selected adapter/release regression passed; lifecycle, review artifact, change metadata, and whitespace validation passed.

## Diff Summary

The M6 resolution changes closeout from local public-evidence-file ownership to provider-owned public evidence collection. Default `close_release_publication` now rejects manually supplied evidence unless explicit fixture mode is enabled, collects GitHub release assets, npm registry metadata, npm tarball metadata, public version smoke, and public target init smoke through a provider, validates the normalized evidence, and writes published `npm-publication.md` only after validation. The CLI exposes `--fixture-mode --fixture-public-evidence` for tests/imports and no longer presents local evidence as a routine closeout proof source. Tests now use a recording provider to assert required provider calls and failure behavior.

## Findings

No blocking or required-change findings.

## Prior Finding Reconciliation

`CR-RTA-M6-F1` is resolved. `close_release_publication` rejects `public_evidence` in default mode at `scripts/release_transaction.py:659` through `scripts/release_transaction.py:666`, and default mode calls `_collect_public_release_evidence` with a closeout provider at `scripts/release_transaction.py:667` through `scripts/release_transaction.py:676`. `_collect_public_release_evidence` requests GitHub assets and npm metadata before public smoke at `scripts/release_transaction.py:731` through `scripts/release_transaction.py:755`. It runs exact `npx @xiongxianfei/rigorloop@0.3.5 version` and `npx @xiongxianfei/rigorloop@0.3.5 init <target>` command shapes without `-y`.

Direct proof exists in `scripts/test-release-transaction.py:1321` through `scripts/test-release-transaction.py:1443`, covering GitHub asset lookup, npm metadata lookup, public version smoke, all target init smoke commands, manual evidence rejection in default mode, unavailable npm evidence, failed public `npx` smoke, and provider-value provenance. Fixture/import mode remains explicit through `scripts/test-release-transaction.py:1445` through `scripts/test-release-transaction.py:1518`.

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | pass | `R32` and `R33` are now implemented through provider-owned GitHub/npm/npx collection before published evidence is written. `R34` command strings use `npx ... version` and `npx ... init <target>` without `-y`. |
| Test coverage | pass | Provider-call tests directly prove GitHub, npm, version smoke, and per-target init smoke are requested. Negative tests cover unavailable GitHub/npm/smoke evidence, manual evidence rejection, `npx -y`, raw tree hash, and missing target evidence. |
| Edge cases | pass | Default mode cannot use a manually authored local evidence file. Fixture mode is explicit. Missing provider evidence and smoke failure return errors before writes. Historical `v0.3.4` evidence remains unchanged. |
| Error handling | pass | Public evidence collection failures raise/return closeout errors and avoid writing published evidence. `--check` remains non-writing. Published evidence validation still rejects invalid command/hash/target shapes. |
| Architecture boundaries | pass | Release transaction helpers own evidence normalization and validation; the CLI remains a thin wrapper; tests use stub providers instead of live GitHub/npm/npx. |
| Compatibility | pass | Historical evidence is not rewritten, `release-verify.sh` is unchanged, and published evidence validation remains inherited through `validate-release.py`. |
| Security/privacy | pass | No secrets or credentials are added. Public command outputs are summarized rather than persisted wholesale. |
| Derived artifact currency | pass | Plan, plan index, review log, review-resolution, and change metadata were synchronized after the resolution. Behavior-preservation evidence remains in scope and validates through lifecycle checks. |
| Unrelated changes | pass | The diff is scoped to M6 closeout ownership, tests, and lifecycle state. |
| Validation evidence | pass | Focused release transaction tests, CLI help, Python compilation, release-verify dry-run, selector-selected adapter regression, lifecycle validation, review artifact validation, change metadata validation, and whitespace validation are recorded. Selector manual-routing debt is unchanged and does not hide the selected regression result. |

## No-Finding Rationale

The resolution addresses the exact trust-boundary defect from M6 R1 without weakening the release gate or relying on manually supplied local evidence in routine closeout. Default closeout now owns public metadata collection and fresh public smoke, tests prove those provider calls directly, and failure paths avoid writing published evidence. The remaining selector manual-routing limitation is pre-existing validation-selection debt and is paired with the selected adapter/release regression that passed.

## Residual Risks

The production provider performs live GitHub asset downloads and public `npx` execution during real closeout, so real release closeout can still fail on external availability or maintainer machine tooling. That is expected release-owned behavior under `R37`, not a unit-test requirement. Selector routing for release transaction scripts remains a known follow-up outside M6.

## Validation

- Reviewed implementation evidence: `python scripts/test-release-transaction.py` passed with 84 tests.
- Reviewed implementation evidence: `python scripts/close-release-publication.py --help` passed.
- Reviewed implementation evidence: `python -m py_compile scripts/release_transaction.py scripts/test-release-transaction.py scripts/close-release-publication.py scripts/validate-release.py` passed.
- Reviewed implementation evidence: `RELEASE_VERIFY_DRY_RUN=1 RELEASE_OUTPUT_DIR=/tmp/rigorloop-release-output RELEASE_COMMIT=fixture-commit bash scripts/release-verify.sh v0.3.5` passed.
- Reviewed implementation evidence: selector validation selected adapter/release regression while blocked on known release transaction script manual routing.
- Reviewed implementation evidence: selected adapter/release regression passed.
- Reviewed implementation evidence: lifecycle validation, review artifact validation, change metadata validation, and `git diff --check --` passed.

## Recommended Next Stage

Close M6 and proceed to `explain-change`. Do not claim verify readiness, PR readiness, release readiness, or final closeout completion from this review alone.
