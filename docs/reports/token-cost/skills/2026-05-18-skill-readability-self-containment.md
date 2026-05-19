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

## M3 after-change measurement

Measured command:

```sh
python scripts/measure-skill-tokens.py
```

Measurement date: 2026-05-18

| Skill | Baseline estimated tokens | After-change estimated tokens | Delta | Delta % | +5% tolerance | +10% hard cap |
|---|---:|---:|---:|---:|---|---|
| proposal | 3189 | 3345 | +156 | +4.89% | within ceiling 3348 | below hard cap 3508 |
| proposal-review | 3255 | 3417 | +162 | +4.98% | within ceiling 3417 | below hard cap 3580 |

## M3 status

The pilot pair remains within the accepted +5% tolerance and below the +10% hard cap. The accepted increases are tied to readability and self-containment gains: workflow role blocks, fenced closed enums, tabulated contracts, labeled workflow-wide rules, and fenced output skeletons are now present in the installed skill text.

Behavior-parity and cold-read evidence in the change-local pack records no quality or clarity regression. Token cost remains subordinate to output quality and clarity under the approved spec.
