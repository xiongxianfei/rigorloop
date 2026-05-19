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

## M2. Pilot skill rewrite and generated-output proof

M2 rewrites only the pilot pair, `proposal` and `proposal-review`, to opt into the readability contract and prove generated output remains derived from canonical skill source.

### Tests first

Added `test_skill_readability_pilot_pair_opts_into_contract` before editing the pilot skills. The focused test failed as expected because the canonical pilot pair did not yet declare `schema-version: skill-readability-v1`, `## Workflow role`, or `## Output skeleton`.

### Implementation

- Added `version: "1.0.0"` and `schema-version: skill-readability-v1` to both pilot skill front matter.
- Added `## Workflow role` blocks with required role fields.
- Reworked long proposal and review contracts into tables where the content has named fields, required sections, review dimensions, or classifications.
- Added authoritative `Closed enum:` blocks for proposal status, Vision fit, scope treatment, review statuses, review dimension results, and recording-related values.
- Added fenced output skeletons near the bottom of both skills.
- Labeled workflow-wide and skill-local rules where the distinction affects user behavior.
- Preserved existing regression-tested wording for artifact placement, stage evidence access, scope preservation, Vision fit, and formal review recording.

### Generated-output proof

Generated skill validation passed from canonical `skills/` source. Temporary adapter archives were built and validated with `v0.1.5`, matching `dist/adapters/manifest.yaml` after PR #68 merged:

- `/tmp/rigorloop-skill-readability-adapters/rigorloop-adapter-codex-v0.1.5.zip`
- `/tmp/rigorloop-skill-readability-adapters/rigorloop-adapter-claude-v0.1.5.zip`
- `/tmp/rigorloop-skill-readability-adapters/rigorloop-adapter-opencode-v0.1.5.zip`

No generated adapter body was hand-edited.

## M3. Cold-read, behavior parity, token comparison, and rollout handoff

M3 records the pilot proof needed before extending the readability contract beyond `proposal` and `proposal-review`.

### Evidence

- Cold-read evidence: `docs/changes/2026-05-18-skill-readability-self-containment/cold-read-report.md`
- Behavior-parity evidence: `docs/changes/2026-05-18-skill-readability-self-containment/behavior-parity-report.md`
- Token comparison: `docs/reports/token-cost/skills/2026-05-18-skill-readability-self-containment.md`

### Result

- Built and validated temporary `v0.1.5` adapter archives from canonical source.
- Inspected installed Codex adapter skill output under `/tmp/rigorloop-skill-readability-cold-read/codex/.agents/skills/`.
- Classified behavior differences for the pilot pair as `equivalent` or `improvement`; no `regression` remains.
- Reduced the pilot skill text until after-change token counts stayed within the +5% tolerance and below the +10% hard cap.
- Kept the remaining R30 skills as follow-on rollout work under the accepted contract, with no exclusions recorded in this milestone.

### Review-resolution fix

Accepted `SRSC-M3-CR1` and removed repeated closed enum value lists after the authoritative fenced enum blocks in `proposal` and `proposal-review`. Updated the stale validator assertions so they check the authoritative enum/reference pattern instead of requiring duplicated backticked prose values.
