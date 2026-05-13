# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M3. Release evidence and final validation pack
Reviewed artifact: committed M3 diff `0c90340`
Review date: 2026-05-13
Recording status: recorded
Status: clean-with-notes

## Review inputs

- Diff/review surface: committed M3 implementation diff `0c90340`.
- Active plan: `docs/plans/2026-05-13-publish-next-release-with-single-authored-skill-source.md`
- Spec: `specs/publish-next-release-with-single-authored-skill-source.md`
- Test spec: `specs/publish-next-release-with-single-authored-skill-source.test.md`
- Prior milestone reviews: `code-review-m1-r2`, `code-review-m2-r2`
- Direct review checks run:
  - `git show --stat --oneline 0c90340`
  - `git show --unified=80 --format=short 0c90340 -- scripts/test-skill-validator.py docs/plans/2026-05-13-publish-next-release-with-single-authored-skill-source.md docs/plan.md docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/change.yaml`
  - `rg -n "T12|build-skills.py --check|Regenerate it with|generated local Codex runtime|\\.codex/skills" specs/publish-next-release-with-single-authored-skill-source.test.md docs/plans/2026-05-13-publish-next-release-with-single-authored-skill-source.md scripts/test-skill-validator.py docs/workflows.md README.md AGENTS.md CONSTITUTION.md`
  - `git ls-files -- .codex/skills/`
  - `git check-ignore -v .codex/skills/proposal/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`
  - `python scripts/validate-release.py --version v0.1.1`
  - `bash scripts/release-verify.sh v0.1.1`

## Diff summary

- `scripts/test-skill-validator.py` was updated so stale contributor-doc expectations no longer require `.codex/skills/` generated-output or direct local-regeneration wording.
- The same validator now asserts active local Codex setup wording through public Codex adapter output and rejects the stale `Regenerate it with python scripts/build-skills.py` and generated local Codex runtime phrases on contributor surfaces.
- The active plan, plan index, and change metadata record the M3 final validation pack, including the full release gate passing without `.codex/skills/` generation as release evidence.
- No skill body, generated public adapter package, release metadata, token-cost report, or adapter manifest changed in M3.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | pass | M3 preserves R1-R35 by validating canonical skills, tracked public adapter output, release notes, token-cost metadata, and ignored/untracked `.codex/skills/` state without adding `.codex/skills/` generation as release evidence. |
| Test coverage | pass | `python scripts/test-skill-validator.py`, `python scripts/test-adapter-distribution.py`, adapter drift validation, adapter validation, token-cost validation, structured release validation, and the full release gate all passed. |
| Edge cases | pass | Direct proof covers ignored/untracked `.codex/skills/`, no `.codex/skills/` release generation, public Codex adapter token-cost source, no required archives, and tracked public adapter output currency. |
| Error handling | pass | Existing release and token-cost validators still reject tracked/unignored `.codex/skills/`, invalid token-cost metadata, stale adapter output, and stale release-note claims through the tested suites. |
| Architecture boundaries | pass | The release evidence remains on canonical `skills/` and public `dist/adapters/` output; `.codex/skills/` remains local runtime state. |
| Compatibility | pass | `dist/adapters/` remains the public install path and `python scripts/validate-adapters.py --version 0.1.1` passed for Codex, Claude Code, and opencode packages. |
| Security/privacy | pass | The release gate validates security-related adapter and release metadata checks and does not publish local `.codex/skills/` contents. |
| Derived artifact currency | pass | `python scripts/build-adapters.py --version 0.1.1 --check` reported generated adapter output in sync; no generated adapter files changed. |
| Unrelated changes | pass | The M3 diff is scoped to stale validator expectations and lifecycle evidence/state updates. |
| Validation evidence | pass | Full `bash scripts/release-verify.sh v0.1.1` passed during review. |

## No-finding rationale

The M3 slice does the narrow evidence-pack work required by the approved plan. It keeps `.codex/skills/` out of release evidence, updates stale validator expectations that contradicted the M2 contract, and proves release readiness through the public adapter path. The full maintainer-facing release gate passed during review and did not require `.codex/skills/` generation.

## Residual risks

- This review does not publish, tag, merge, or deploy the release; publication remains outside the plan.
- Final lifecycle closeout still needs `explain-change`, `verify`, and `pr` handoff.

## Review outcome

- First-pass review status: clean-with-notes
- Material findings: none
- Required review-resolution: none
- Reviewed milestone: M3
- Milestone state after review: closed
- Remaining implementation milestones: none
- Next stage: final closeout, starting with `explain-change` unless a separate CI-maintenance trigger is identified
- Final closeout readiness: ready for final closeout; not PR-ready until downstream gates complete
