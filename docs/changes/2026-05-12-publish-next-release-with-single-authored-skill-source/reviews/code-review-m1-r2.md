# Code Review M1 R2

Review ID: code-review-m1-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: M1. Release gate validates public output, not `.codex/skills/`
Reviewed artifact: committed M1 diff `4eb0521`
Review date: 2026-05-13
Recording status: recorded
Status: clean-with-notes

## Review inputs

- Diff/review surface: committed diff `4eb0521` for M1 implementation and governing artifacts.
- Prior review: `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/reviews/code-review-m1-r1.md`
- Active plan: `docs/plans/2026-05-13-publish-next-release-with-single-authored-skill-source.md`
- Spec: `specs/publish-next-release-with-single-authored-skill-source.md`
- Test spec: `specs/publish-next-release-with-single-authored-skill-source.test.md`
- Architecture: `docs/architecture/system/architecture.md`
- Validation evidence recorded in the active plan and change metadata.
- Direct review checks run:
  - `git show -- scripts/release-verify.sh scripts/validate-release.py scripts/adapter_distribution.py scripts/test-adapter-distribution.py`
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_release_verify_script_supports_v0_1_1 AdapterDistributionTests.test_v0_1_1_release_validation_accepts_ignored_untracked_codex_skills AdapterDistributionTests.test_v0_1_1_release_validation_rejects_tracked_codex_skills AdapterDistributionTests.test_v0_1_1_release_validation_rejects_unignored_codex_skills AdapterDistributionTests.test_v2_final_release_validation_requires_changed_surface_input`
  - `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.1`
  - `python scripts/validate-release.py --version v0.1.1`
  - `git ls-files -- .codex/skills/`
  - `git check-ignore -v .codex/skills/proposal/SKILL.md`

## Diff summary

- `scripts/release-verify.sh` removes `python scripts/build-skills.py --check` from required `v0.1.1` release evidence and keeps it for other release versions.
- `scripts/adapter_distribution.py` adds `v0.1.1` release validation for `.codex/skills/` ignored/untracked state without generating or structurally validating `.codex/skills/`.
- `scripts/validate-release.py` treats a no-argument CLI invocation as an explicit empty changed-surface context while direct helper validation still rejects missing context.
- `scripts/test-adapter-distribution.py` adds regression coverage for the v0.1.1 release gate and `.codex/skills/` ignored/untracked pass/fail behavior.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | pass | R7-R19 and R32-R35 are covered by the release gate, structured release validation, and token-cost preservation tests. |
| Test coverage | pass | Focused tests directly prove v0.1.1 omits `build-skills.py --check`, accepts ignored/untracked `.codex/skills/`, rejects tracked or unignored `.codex/skills/`, and preserves direct helper changed-surface enforcement. |
| Edge cases | pass | EC3 and EC4 have direct positive and negative tests; the no-argument CLI behavior is covered through `python scripts/validate-release.py --version v0.1.1`. |
| Error handling | pass | Git helper failures do not crash release validation, and unignored or tracked local runtime state returns actionable validation errors. |
| Architecture boundaries | pass | The release gate proves public adapter output and only checks local Codex runtime tracked-state absence, matching the transition-release architecture. |
| Compatibility | pass | Historical release gates still require `build-skills.py --check`; v0.1.1 keeps canonical skills, adapter drift, adapter validation, token-cost validation, and release metadata validation. |
| Security/privacy | pass | The change does not print generated skill bodies or local `.codex/skills/` contents as release evidence. |
| Derived artifact currency | pass | No generated adapter or skill output changed; release validation still checks tracked public adapter drift. |
| Unrelated changes | pass | The reviewed code diff is scoped to the M1 release-gate and release-validation behavior plus required lifecycle artifacts. |
| Validation evidence | pass | M1 full targeted validation and rerun focused checks passed. |

## No-finding rationale

The committed M1 implementation removes the privileged local Codex mirror check from the `v0.1.1` release gate while preserving all required public release proof: canonical skill validation, public adapter drift and structure validation, token-cost metadata validation, release metadata validation, release notes checks through structured validation, and `.codex/skills/` ignored/untracked state. The tests directly cover the named edge cases and preserve the direct helper behavior that requires changed-surface context for final v2 token-cost release validation.

## Residual risks

- M2 still needs to update release docs and adapter install guidance, so this clean review closes only M1.
- M3 still needs final release evidence validation before any PR or release readiness claim.

## Review outcome

- First-pass review status: clean-with-notes
- Material findings: none
- Required review-resolution: not required
- Reviewed milestone: M1
- Milestone state after review: closed
- Remaining implementation milestones: M2 planned, M3 planned
- Next stage: implement M2
- Final closeout readiness: not ready because M2-M3 are not implemented or reviewed
