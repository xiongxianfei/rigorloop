# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M1. Release gate validates public output, not `.codex/skills/`
Reviewed artifact: local diff for `scripts/release-verify.sh`, `scripts/validate-release.py`, `scripts/adapter_distribution.py`, and `scripts/test-adapter-distribution.py`
Review date: 2026-05-13
Recording status: recorded
Status: inconclusive

## Review inputs

- Diff/review surface: unstaged local diff for M1 implementation files.
- Active plan: `docs/plans/2026-05-13-publish-next-release-with-single-authored-skill-source.md`
- Spec: `specs/publish-next-release-with-single-authored-skill-source.md`
- Test spec: `specs/publish-next-release-with-single-authored-skill-source.test.md`
- Architecture: `docs/architecture/system/architecture.md`
- Validation evidence recorded in the active plan and change metadata.
- Direct review checks run:
  - `git ls-files -- .codex/skills/`
  - `git check-ignore -v .codex/skills/proposal/SKILL.md`
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_release_verify_script_supports_v0_1_1 AdapterDistributionTests.test_v0_1_1_release_validation_accepts_ignored_untracked_codex_skills AdapterDistributionTests.test_v0_1_1_release_validation_rejects_tracked_codex_skills AdapterDistributionTests.test_v0_1_1_release_validation_rejects_unignored_codex_skills AdapterDistributionTests.test_v2_final_release_validation_requires_changed_surface_input`
  - `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.1`

## Diff summary

- `scripts/release-verify.sh` removes `python scripts/build-skills.py --check` from required `v0.1.1` release evidence while preserving it for other release versions.
- `scripts/adapter_distribution.py` adds structured `.codex/skills/` ignored/untracked validation for `v0.1.1` release metadata validation.
- `scripts/validate-release.py` passes an explicit empty changed-surface context when the maintainer-facing CLI is invoked without changed-path arguments.
- `scripts/test-adapter-distribution.py` adds direct regression tests for the `v0.1.1` release gate and `.codex/skills/` ignored/untracked checks.

## Findings

No implementation-code material findings were identified in the inspected M1 diff.

## Blocking evidence issue

The review cannot return `clean-with-notes` because the governing proposal, spec, test spec, active plan, and change-local records for this workflow are still untracked in the local Git worktree. The code-review skill permits local-only governing artifacts as background, but missing tracked governing authority blocks a clean branch-scoped conclusion.

Required outcome: add or commit the governing artifacts and M1 implementation state so a rerun can make a branch-scoped clean review conclusion.

Safe resolution path: track the already-created governing artifacts and M1 implementation files, then rerun `code-review M1` against the tracked branch state. No product, spec, architecture, or scope decision is required.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | concern | The inspected code aligns with R7-R19 and R32-R35, but governing artifacts are untracked so the review cannot close branch-scoped alignment. |
| Test coverage | pass | Focused tests cover v0.1.1 release-gate omission of `build-skills.py --check`, `.codex/skills/` ignored/untracked pass/fail cases, and direct helper changed-surface enforcement. |
| Edge cases | pass | EC3 and EC4 are directly covered by ignored/untracked and tracked `.codex/skills/` tests; the direct helper missing-context edge remains covered. |
| Error handling | pass | Git command failures in `.codex/skills/` state helpers fall back without crashing and surface ignored-state failure where appropriate. |
| Architecture boundaries | concern | The code follows the public-adapter release boundary, but clean architecture compliance depends on untracked architecture/spec artifacts becoming tracked. |
| Compatibility | pass | Historical release gates retain `build-skills.py --check`; v0.1.1 dry-run keeps canonical skills, adapter drift, adapter validation, token-cost validation, and release metadata validation. |
| Security/privacy | pass | The change checks local runtime tracked/ignored state and does not print skill bodies or local `.codex/skills/` contents as evidence. |
| Derived artifact currency | pass | No generated adapter or skill output was changed by M1; release validation still checks tracked public adapter drift. |
| Unrelated changes | concern | The review target includes only M1 code files, but the branch also has untracked lifecycle artifacts from earlier stages that must be tracked before clean branch-scoped review. |
| Validation evidence | pass | Plan-recorded M1 command pack passed, and focused review commands reran successfully. |

## No-finding rationale for implementation diff

The inspected M1 implementation removes the local Codex mirror generation check from required `v0.1.1` release evidence while keeping canonical skill validation, public adapter drift validation, adapter structural validation, token-cost validation, and release metadata validation in the release gate. The structured validator checks only `.codex/skills/` ignored/untracked state for `v0.1.1`, which matches the approved boundary that `.codex/skills/` is local runtime state rather than release output.

## Review outcome

- First-pass review status: inconclusive
- Material findings: none
- Required review-resolution: no review-resolution yet; rerun code-review after tracked governing state is available
- Reviewed milestone: M1
- Milestone state after review: review-requested
- Remaining implementation milestones: M1 review-requested, M2 planned, M3 planned
- Next stage: track or commit governing artifacts and rerun `code-review M1`
- Final closeout readiness: not ready because M1 is not clean-reviewed and M2-M3 are not implemented or reviewed
