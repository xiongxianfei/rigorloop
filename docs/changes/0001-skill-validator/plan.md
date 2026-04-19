# 0001 Skill Validator Plan

## Source plan

The implementation source of truth is the active plan at `../../plans/2026-04-19-rigorloop-first-release-implementation.md`.

M1 aligned contributor guidance first. The core validator feature then shipped through M2-M6.

## Milestone map

| Milestone | Commits | Outcome |
| --- | --- | --- |
| `M2` | `44a8eaf`, `7d82242` | added `schemas/`, change-metadata fixtures, and `scripts/validate-change-metadata.py` |
| `M3` | `ca0f214` | normalized canonical `skills/` and added skill-validator fixtures |
| `M4` | `8347d73`, `972a11a` | implemented skill validation, deterministic generation, and the missing-`SKILL.md` regression fix |
| `M5` | `4f4a9ec` | replaced template CI with repo-owned structural checks and aligned contributor docs |
| `M6` | current milestone | published the change-local artifact pack and linked it from `README.md` |

## Key execution choices

- keep schema shape in `schemas/` and executable validation rules in `scripts/`
- delay `.codex/skills/` sync until canonical `skills/` is stable enough for one deliberate regeneration
- summarize top-level approved artifacts here instead of copying them verbatim
