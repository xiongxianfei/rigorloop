# Skill Readability and Self-Containment Token Baseline

## Scope

Baseline static token measurement for the pilot pair before any `proposal` or `proposal-review` skill rewrite.

Measured command:

```sh
python scripts/measure-skill-tokens.py
```

Measurement date: 2026-05-18

Token estimate: approximate local estimate from `scripts/measure-skill-tokens.py`.

## Pilot baseline

| Skill | Path | Baseline bytes | Baseline lines | Baseline estimated tokens |
|---|---|---:|---:|---:|
| proposal | `skills/proposal/SKILL.md` | 12758 | 254 | 3189 |
| proposal-review | `skills/proposal-review/SKILL.md` | 13020 | 296 | 3255 |

## Thresholds for after-change comparison

| Skill | Zero-regression target | +5% tolerance ceiling | +10% hard cap |
|---|---:|---:|---:|
| proposal | 3189 | 3348 | 3508 |
| proposal-review | 3255 | 3417 | 3580 |

## M1 status

No pilot skill body was rewritten in M1. This report is the baseline for M2 and M3 comparisons.

M2 must record after-change token counts for the pilot pair before rollout evidence is accepted.
