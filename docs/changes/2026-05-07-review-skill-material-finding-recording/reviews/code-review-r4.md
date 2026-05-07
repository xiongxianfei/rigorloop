# Code Review R4

Review ID: code-review-r4
Stage: code-review
Round: 4
Reviewer: Owner PR review
Target: shared formal review skill `Isolation and Recording` guidance in PR #32
Status: changes-requested

## Review inputs

- PR: https://github.com/xiongxianfei/rigorloop/pull/32
- User review request: simplify the shared `Isolation and Recording` skill description.
- Canonical shared block: `templates/shared/review-isolation-and-recording.md`
- Copied skill blocks: `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md`, `skills/architecture-review/SKILL.md`, `skills/plan-review/SKILL.md`, and `skills/code-review/SKILL.md`
- Static proof: `scripts/test-skill-validator.py`

## Findings

### CR4-F1 - Shared review recording block is too verbose for skill guidance

Finding ID: CR4-F1
Severity: major
Evidence: `templates/shared/review-isolation-and-recording.md` includes an internal `specs/rigorloop-workflow.md` reference, a long tracked-artifact definition, an operational shortcut paragraph, duplicate resolution-gate wording, and explicit next-action enum strings. The same verbose block is copied into all five formal review skills and generated outputs.
Required outcome: Simplify the shared skill-facing wording while preserving the active rule that isolation controls handoff, every material finding requires change-local review files, material findings need evidence/outcome/resolution or decision rationale, clean reviews stay lightweight, and isolated material-review output names the required recording surface.
Safe resolution: Replace the canonical shared block with the concise owner-provided wording, using "before fixing" instead of "review-driven edits"; update the static assertions and any aligned spec/test wording that requires the old verbose skill text; recopy the block into all five formal review skills; regenerate `.codex/skills/` and `dist/adapters/`; then rerun selected validation.

## Checklist coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | changes requested | The approved rule remains valid, but the skill-facing description should be concise enough to use reliably. |
| Test coverage | changes requested | Static assertions currently pin verbose wording and must be updated with the concise contract. |
| Generated output drift | changes requested | Canonical skill edits require generated Codex skill and adapter refresh. |
| Validation evidence | pending | Validation must run after the block, tests, copied skills, and generated outputs are updated. |

## Recommended next stage

Record this finding before fixing, then update the shared block and rerun selected validation.
