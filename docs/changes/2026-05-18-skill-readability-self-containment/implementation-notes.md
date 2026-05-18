# Skill Readability and Self-Containment Implementation Notes

## M1. Static validator foundations and baseline evidence

M1 adds the first opt-in static validation foundation for the skill readability contract without rewriting `proposal` or `proposal-review`.

### Tests first

Added failing fixture tests for `schema-version: skill-readability-v1` skills before implementing validator support:

- valid opt-in readability fixture;
- missing workflow role block;
- invalid workflow role `stage`;
- missing output skeleton;
- required unavailable internal reference;
- duplicate closed enum block.

The first run of `python scripts/test-skill-validator.py` failed on the new readability tests as expected before validator implementation.

### Implementation

- Added opt-in readability validation in `scripts/skill_validation.py`.
- The checks run only when a skill declares `schema-version: skill-readability-v1`, so current canonical skills remain valid until the M2 rewrite opts the pilot pair into the contract.
- Added focused fixture coverage under `tests/fixtures/skills/skill-readability/`.
- Recorded the pilot token baseline in `docs/reports/token-cost/skills/2026-05-18-skill-readability-self-containment.md`.

### Scope boundary

M1 did not rewrite `skills/proposal/SKILL.md` or `skills/proposal-review/SKILL.md`. M2 owns the pilot skill text rewrite and generated adapter validation.
