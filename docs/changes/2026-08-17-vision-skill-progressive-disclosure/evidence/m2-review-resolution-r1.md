# M2 Review Resolution R1

Finding: `VIS-M2-CR1`
Disposition: accepted
Status: resolved pending independent rereview

## Correction

- The universal vision contract now requires the complete governed operation manifest to be persisted in authorized change-local authoring evidence before the first target write when the existing evidence model supports the contract.
- If that model cannot support the contract, the skill stops and requires architecture before planning.
- A zero-write sync skip now records unchanged canonical vision and skipped README targets with equal prior and intended identities.
- A zero-write skip now requires no changed files and prohibits synchronization and marker-validity claims.
- Focused assertions fail if any of these clauses disappear.

The correction reuses existing Markdown authoring evidence and introduces no persistence surface, parsed schema, lifecycle state, or authority owner.

## Validation

| Command | Result |
| --- | --- |
| `python scripts/validate-skills.py skills/vision/SKILL.md` | pass |
| `python scripts/test-skill-validator.py VisionSkillProgressiveDisclosureTests` | pass; 6 tests |
| `python scripts/test-skill-validator.py` | pass; 408 tests, 16 skipped |
| `python scripts/test-build-skills.py` | pass; 7 tests |
| `python scripts/build-skills.py --check` | pass |
| `python scripts/validate-change-metadata.py docs/changes/2026-08-17-vision-skill-progressive-disclosure/change.yaml` | pass |

The largest loaded procedural assembly is 2,057 words and 15,735 bytes, below the 2,268-word and 15,845-byte baseline.
