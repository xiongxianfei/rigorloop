# M3 Proposal-Review Preservation Evidence

## Scope

M3 conforms existing `proposal-review` assets to the review-family contract. It does not change proposal-review judgment, review dimensions, severity values, status values, recording rules, isolation rules, stop conditions, lifecycle boundaries, or handoff behavior.

## Asset inventory

| Asset | Status | Evidence |
|---|---|---|
| `skills/proposal-review/assets/material-finding.md` | retained | Already used the parser-owned material-finding labels. |
| `skills/proposal-review/assets/review-result-skeleton.md` | conformed | Now makes the gate-review status vocabulary explicit. |

## Material-finding field parity

The material-finding parser-owned field block is byte-identical to `code-review`:

```text
- Finding ID: <finding ID>
- Severity: <severity>
- Location: <location>
- Evidence: <evidence>
- Required outcome: <required outcome>
- Safe resolution path: <safe resolution path>
- needs-decision rationale: <needs-decision rationale or none>
```

The `proposal-review` resource map now includes the literal `Finding ID:` confirmation before linking findings from `review-log.md` or `review-resolution.md`.

## Result-skeleton field parity

| Source result field | Asset field | Preservation |
|---|---|---|
| Skill | `Skill: proposal-review` | unchanged |
| Review status | `Review status: <approved | changes-requested | blocked | inconclusive>` | unchanged gate-review vocabulary; `clean-with-notes` was not introduced |
| Material findings | `Material findings:` | unchanged |
| Recording status | `Recording status:` | unchanged |
| Recording blocker | `Recording blocker:` | unchanged |
| Review record | `Review record:` | unchanged |
| Review log | `Review log:` | unchanged |
| Review resolution | `Review resolution:` | unchanged |
| Open blockers | `Open blockers:` | unchanged |
| Immediate next stage | `Immediate next stage:` | unchanged |
| Review dimensions | `Review Dimensions` section | unchanged |
| Scope preservation review | `Scope Preservation Review` section | unchanged |
| Recommended proposal edits | `Recommended Proposal Edits` section | unchanged |
| Recommendation | `Recommendation` section | unchanged |

## Behavior parity

Representative proposal-review behavior is unchanged:

- A clean proposal-review still uses `approved` and remains a gate review rather than a code-review milestone review.
- Material findings still use `changes-requested`, detailed review records, and review-resolution when triggered.
- `blocked` and `inconclusive` retain their existing meanings.
- Vision fit, scope preservation, option quality, risk, and readiness dimensions remain in `SKILL.md`, not in assets.
- Direct or review-only proposal-review invocations remain isolated by default.

## Validator proof

`scripts/test-skill-validator.py` includes a proposal-review family asset test that checks:

- `skills/proposal-review/SKILL.md` maps both assets with `COPY`;
- the resource map includes the literal `Finding ID:` confirmation;
- the material-finding field block matches the code-review field block;
- the result skeleton preserves `approved | changes-requested | blocked | inconclusive`;
- the result skeleton does not introduce `clean-with-notes`.
