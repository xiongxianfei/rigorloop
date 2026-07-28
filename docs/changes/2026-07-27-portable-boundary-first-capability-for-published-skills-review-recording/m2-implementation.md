# M2 implementation evidence

## Result

- Milestone: PBF-M2
- Status: review-requested
- Scope: governed lifecycle skill behavior
- Next stage: code-review M2

## Implementation

Each governed lifecycle skill now maps the same skill-local
`references/boundary-first-method-v1.md` with a stage-specific `READ`
condition. Each skill owns only its PBF-R043 responsibility and PBF-R064 stop
behavior; the shared reference remains free of stage approval, placement, and
handoff policy.

Semantic-gap fixtures cover missing ownership, example-only behavior,
undecidable applicability, coupled milestones, stale contract IDs, helper-only
proof, mutation without proof, escaped boundary paths, and stale verification
evidence. These fixtures assert that the owning skill supplies the semantic
response and never delegate semantic completeness to structural validation.

The existing spec-family and review-family asset checks now allow exactly the
approved boundary-first reference for governed consumers. Other packaged
non-asset resources remain invalid, and ordinary resource-map validation still
requires the literal `READ` verb, a trigger condition, and a present local
file.

## Test-first evidence

Before implementation,
`python scripts/test-skill-validator.py -k BoundaryFirstLifecycleSkillTests`
failed for all ten missing skill mappings and the absent semantic fixture.
After implementation, both focused tests pass.

## Validation

| Command | Result |
| --- | --- |
| `python scripts/test-skill-validator.py -k BoundaryFirstLifecycleSkillTests` | pass; 2 tests |
| `python scripts/validate-skills.py` | pass; 24 skill files |
| `python scripts/test-skill-validator.py` | pass; 261 tests |
| `python scripts/build-skills.py --check` | pass; temporary generated output validated |
| `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py skills scripts/fixtures/boundary-first/semantic/review-cases.json` | pass |

## Handoff

M2 is ready for independent code-review against the approved spec, plan, test
spec, actual diff, and this validation evidence. M3 remains blocked until M2
review closes.
