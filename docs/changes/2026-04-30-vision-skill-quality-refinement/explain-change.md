# Vision Skill Quality Refinement Explain Change

## Summary

M1 refines the canonical `vision` skill and focused skill-validator assertions so the skill pushes stronger first-pass vision drafts instead of only blocking bad outputs.

Generated `.codex/skills/` and `dist/adapters/` output is intentionally deferred to M2. Root `vision.md` and README front-matter remain out of scope for this refinement.

## Source Artifacts

- Proposal: `docs/proposals/2026-04-30-vision-skill-quality-refinement.md`
- Spec: `specs/vision-skill.md` (`R19`, `R81`-`R94`, `AC13`-`AC19`)
- Test spec: `specs/vision-skill.test.md`
- Plan: `docs/plans/2026-04-30-vision-skill-quality-refinement.md`

## Diff Rationale

| Area | Change | Reason |
| --- | --- | --- |
| `scripts/test-skill-validator.py` | Added focused assertions for workflow-fit placement, drafting heuristics, consolidated edit authorization, mode-table shape, and enforceable revise-mode traceability. | The implementation surface is skill text, so tests need stable contract assertions that fail before the guidance exists. |
| `skills/vision/SKILL.md` | Moved workflow fit near the top, consolidated source-of-truth and overwrite rules into edit authorization, converted mode behavior to one table, added drafting heuristics, and made substantive revise-mode traceability explicit. | Matches the approved refinement while preserving create/revise/mirror behavior, README marker rules, and source-of-truth order. |
| Change-local evidence | Added this artifact pack during M1. | Implementation-stage changes are non-trivial, so the causal link should be durable before later generated-output and closeout milestones. |

## Scope Control

- No root `vision.md` revision is part of this refinement.
- No README front-matter content is changed by M1.
- No generated `.codex/skills/` or `dist/adapters/` files are hand-edited.
- Shared evidence-collection boilerplate extraction remains out of scope.
- Proposal, proposal-review, and governance behavior are not broadened in M1.

## Validation Evidence

- `python scripts/test-skill-validator.py` failed before the skill revision for the new M1 assertions.
- `python scripts/test-skill-validator.py` passed after the skill revision.
- `python scripts/validate-skills.py skills/vision/SKILL.md` passed.
- `python scripts/validate-skills.py` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.test.md` passed.
- `python scripts/test-change-metadata-validator.py` passed.
- `python scripts/validate-readme.py README.md --vision-markers` passed.
- `git diff --check -- specs/vision-skill.test.md scripts/test-skill-validator.py skills/vision/SKILL.md docs/plans/2026-04-30-vision-skill-quality-refinement.md docs/changes/2026-04-30-vision-skill-quality-refinement` passed.

Selector inspection passed and selected generated skill and adapter drift checks. Those checks are deferred to M2 because generated output refresh is the next milestone, not part of M1.

## Readiness

M1 targeted validation has passed. This milestone is ready for code-review before M2 generated-output refresh.
