# M1 Rule Ownership and Baseline Evidence

Milestone: M1
Date: 2026-08-10
Status: implementation-complete; review pending

## Scope

The ledger accounts for all current `code-review` headings and the seven R11 duplication clusters before canonical prose moves. The scenario fixture covers all seven R16 modes, and the negative fixture uses the unknown `moved-somewhere` disposition.

## Baseline

| Metric | Baseline |
| --- | ---: |
| `SKILL.md` lines | 518 |
| `SKILL.md` words | 4514 |
| `SKILL.md` estimated tokens | 8160 |
| Conditional automation reference words | 0 |
| Conditional automation reference estimated tokens | 0 |
| Total package words | 5569 |
| Total package estimated tokens | 10116 |
| Duplicated rule clusters | 7 |
| Inline templates | 1 |
| Mapped resources | 3 |

Token estimates use `scripts/measure-skill-tokens.py`. Package totals include canonical `SKILL.md`, the boundary reference, and both assets.

## Completeness and aligned surfaces

- Canonical `skills/code-review/` is intentionally unchanged in M1 because the ledger must precede prose movement.
- Existing skill and adapter validators are unaffected in M1 because no package resource or generated output changed.
- No rule uses `removed-obsolete-with-approved-contract-change`; no upstream contract change is required.

## Handoff

M1 is ready for independent code review after the exact ledger/fixture proof and lifecycle checks pass. This evidence does not close the milestone or claim downstream readiness.
