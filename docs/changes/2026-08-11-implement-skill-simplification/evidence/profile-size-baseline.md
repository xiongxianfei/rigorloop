# Implement Skill Profile Size Baseline

Milestone: M1
Date: 2026-08-11
Canonical baseline commit: `53df8ce2`

## Canonical resource identities

| Resource | SHA-256 | Lines | Words | UTF-8 bytes | Estimated tokens |
| --- | --- | ---: | ---: | ---: | ---: |
| `skills/implement/SKILL.md` | `b7839e959175acc05b93d3a1f4c5c612e95fcd579eb9b02551f6be40c528a301` | 395 | 3338 | 23906 | 5977 |
| `skills/implement/references/boundary-first-method-v1.md` | `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f` | 110 | 857 | 6346 | not separately reported by the existing tool |
| Total package | derived from the two rows | 505 | 4195 | 30252 | not used as a normative gate |

Token evidence uses the existing `scripts/measure-skill-tokens.py --skills-root skills` estimator. Words and UTF-8 bytes are the primary portable measurements.

## Invocation profiles before simplification

The current package has no planned, automation, or result resource split. Every valid invocation loads the same `SKILL.md`; the boundary reference is added only when its independent trigger applies.

| Profile | Always loaded policy resources | Words | UTF-8 bytes | Conditional boundary addition |
| --- | --- | ---: | ---: | --- |
| `IP0-isolated` | `skills/implement/SKILL.md` | 3338 | 23906 | +857 words / +6346 bytes only when boundary guidance is triggered |
| `IP1-planned` | `skills/implement/SKILL.md` | 3338 | 23906 | same independent addition |
| `IP2-planned-armed` | `skills/implement/SKILL.md` | 3338 | 23906 | same independent addition |

## Structural baseline

| Metric | Baseline |
| --- | ---: |
| Behaviorally significant rule rows | 24 |
| Literal compatibility rows | 18 |
| Identified duplication/procedure clusters | 7 |
| Complete inline result structures | 2 |
| Mapped resources | 1 |
| Conditional implementation references | 0 |
| Structural result assets | 0 |

The seven clusters are orientation/trigger, evidence reading, shared boundary detail, handoff guidance, claim/stop repetition, planned-milestone procedure, and automation procedure/output repetition.
