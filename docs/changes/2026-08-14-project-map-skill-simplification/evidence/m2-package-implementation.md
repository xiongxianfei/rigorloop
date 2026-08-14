# M2 Package Implementation

## Result

- Milestone: M2
- Status: implementation-complete
- Canonical package: `SKILL.md`, one conditional reference, and one structural skeleton
- Simple assembly: `PMA0-simple-root-create`
- Conditional assembly: `PMA1-maintenance-or-coordinated`

The canonical skill now classifies operation and scope independently, binds create and refresh to target existence, keeps audit read-only, performs the seven-surface coordination preflight, and fails closed when required conditional procedure is unavailable. The new reference owns refresh, audit, root/area coordination, area creation, commit ordering, and exact retry recovery. The existing skeleton remains the only structural asset.

The first focused run preceded the package edit and failed with four contract failures plus one missing-reference error. After the atomic package and validator update, all six focused tests pass. Compatibility fixtures now use `Operation` and `Map scope`; the validator no longer treats `area` as an operation or requires the skill body to duplicate skeleton-owned structure.

## Validation

- CMD2, `python scripts/validate-skills.py skills/project-map/SKILL.md`: passed.
- CMD3, `python scripts/test-skill-validator.py ProjectMapSkillSimplificationTests`: passed, 6 tests.
- CMD4, `python scripts/test-skill-validator.py`: passed, 336 tests with 16 skips.
- CMD5, `python scripts/test-build-skills.py`: passed, 7 tests.
- CMD6, `python scripts/build-skills.py --check`: passed.
- CMD9, `python scripts/validate-boundary-first.py --check --path specs/project-map.md`: passed.
- `git diff --check`: passed.

## Profile checkpoint

LF-normalized portable word and byte accounting will be finalized in M3. The current canonical files already establish that `PMA0` is materially smaller and `PMA1` is smaller than the 2,297-word and 15,545-byte baseline:

| Surface | Words | UTF-8 bytes |
| --- | ---: | ---: |
| `SKILL.md` / `PMA0` procedure | 1,610 | 11,727 |
| Conditional reference | 525 | 3,800 |
| `PMA1` procedure | 2,135 | 15,527 |

## Handoff

Ready for independent M2 `code-review`. This evidence does not claim generated adapter parity, final semantic closeout, verification, or PR readiness.
