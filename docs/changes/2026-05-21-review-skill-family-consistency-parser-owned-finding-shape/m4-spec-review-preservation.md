# M4 Spec-Review Preservation Evidence

## Scope

M4 conforms `spec-review` to the review-family asset contract by replacing `assets/review-finding.md` with `assets/material-finding.md`, updating references, and preserving spec-review result fields. It does not change spec-review judgment, review dimensions, severity values, status values, recording rules, isolation rules, stop conditions, lifecycle boundaries, downstream readiness behavior, or handoff behavior.

## Asset inventory

| Asset | Status | Evidence |
|---|---|---|
| `skills/spec-review/assets/material-finding.md` | added | Replaces the old `review-finding.md` name and contains the parser-owned field labels. |
| `skills/spec-review/assets/review-finding.md` | removed | Approved review-family asset name is `material-finding.md`. |
| `skills/spec-review/assets/review-result-skeleton.md` | conformed | Preserves result fields and makes the gate-review status vocabulary explicit. |

## Material-finding field parity

The material-finding parser-owned field block is byte-identical to `code-review` and `proposal-review`:

```text
- Finding ID: <finding ID>
- Severity: <severity>
- Location: <location>
- Evidence: <evidence>
- Required outcome: <required outcome>
- Safe resolution path: <safe resolution path>
- needs-decision rationale: <needs-decision rationale or none>
```

The `spec-review` resource map now includes the literal `Finding ID:` confirmation before linking findings from `review-log.md` or `review-resolution.md`.

## Result-skeleton field parity

| Source result field | Asset field | Preservation |
|---|---|---|
| Skill | `Skill: spec-review` | unchanged |
| Review status | `Review status: <approved | changes-requested | blocked | inconclusive>` | unchanged gate-review vocabulary; `clean-with-notes` was not introduced |
| Material findings | `Material findings:` | unchanged |
| Recording status | `Recording status:` | unchanged |
| Recording blocker | `Recording blocker:` | unchanged |
| Review record | `Review record:` | unchanged |
| Review log | `Review log:` | unchanged |
| Review resolution | `Review resolution:` | unchanged |
| Open blockers | `Open blockers:` | unchanged |
| Immediate next stage | `Immediate next stage:` | unchanged |
| Findings | `Findings` section | unchanged |
| Eventual test-spec readiness | `Eventual test-spec readiness` section | unchanged |
| Stop condition | `Stop condition` section | unchanged |

## Behavior parity

Representative spec-review behavior is unchanged:

- A clean spec-review still uses `approved` and must still report eventual test-spec readiness.
- Material findings still use `changes-requested`, detailed review records, and review-resolution when triggered.
- `blocked` and `inconclusive` retain their existing meanings.
- Requirement clarity, normative language, completeness, testability, compatibility, observability, security/privacy, non-goals, and acceptance criteria review dimensions remain in `SKILL.md`, not in assets.
- Direct or review-only spec-review invocations remain isolated by default.

## Validator proof

`scripts/test-skill-validator.py` includes a spec-review family asset test that checks:

- `skills/spec-review/SKILL.md` maps `assets/material-finding.md` and no longer references `assets/review-finding.md`;
- the old `review-finding.md` asset is removed;
- the material-finding field block matches the code-review field block;
- the result skeleton preserves `approved | changes-requested | blocked | inconclusive`;
- the result skeleton preserves `Eventual test-spec readiness`;
- the result skeleton does not introduce `clean-with-notes`.

The spec-family asset validator inventory now accepts `assets/material-finding.md` for `spec-review`, aligning the older spec-family validator with the newer review-family contract.
