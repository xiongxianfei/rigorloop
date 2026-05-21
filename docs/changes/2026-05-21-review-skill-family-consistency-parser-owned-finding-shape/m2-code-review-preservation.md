# M2 Code-Review Preservation Evidence

## Scope

M2 adds review-family assets to `skills/code-review/` and updates `skills/code-review/SKILL.md` to point at those assets. It does not change code-review judgment, review dimensions, severity values, review-status values, recording rules, isolation rules, stop conditions, lifecycle boundaries, or handoff behavior.

## Asset inventory

| Asset | Status | Evidence |
|---|---|---|
| `skills/code-review/assets/material-finding.md` | added | Contains the parser-owned material-finding field labels and placeholders. |
| `skills/code-review/assets/review-result-skeleton.md` | added | Contains the code-review result block fields and preserves code-review status vocabulary. |

## Material-finding field parity

| Source obligation in `SKILL.md` | Asset field | Preservation |
|---|---|---|
| Finding ID | `Finding ID:` | unchanged label and obligation |
| Severity | `Severity:` | unchanged label and obligation |
| Location | `Location:` | unchanged label and obligation |
| Evidence | `Evidence:` | unchanged label and obligation |
| Required outcome | `Required outcome:` | unchanged label and obligation |
| Safe resolution path or needs-decision rationale | `Safe resolution path:` and `needs-decision rationale:` | unchanged safe-resolution boundary |

## Result-skeleton field parity

| Source result field | Asset field | Preservation |
|---|---|---|
| Skill | `Skill: code-review` | unchanged |
| Status | `Status: <completed | blocked | inconclusive>` | unchanged |
| Artifacts changed | `Artifacts changed:` | unchanged |
| Open blockers | `Open blockers:` | unchanged |
| Next stage | `Next stage:` | unchanged |
| Review status | `Review status: <clean-with-notes | changes-requested | blocked | inconclusive>` | unchanged; `approved` was not introduced |
| Material findings | `Material findings:` | unchanged |
| Recording status | `Recording status:` | unchanged |
| Recording blocker | `Recording blocker:` | unchanged |
| Review record | `Review record:` | unchanged |
| Review log | `Review log:` | unchanged |
| Review resolution | `Review resolution:` | unchanged |
| Reviewed milestone | `Reviewed milestone:` | unchanged |
| Milestone closeout | `Milestone closeout:` | unchanged |
| Remaining implementation milestones | `Remaining implementation milestones:` | unchanged |
| Required review-resolution | `Required review-resolution:` | unchanged |
| Finding IDs | `Finding IDs:` | unchanged |
| Verify readiness | `Verify readiness: <not-claimed>` | unchanged |

## Behavior parity

Representative code-review behavior is unchanged:

- Clean non-final milestone review still uses `clean-with-notes`, closes only the reviewed milestone, and hands off to the next implementation milestone.
- Material or required-change findings still use `changes-requested`, require detailed review recording, and route to review-resolution.
- `blocked` and `inconclusive` remain available review statuses with their existing stop behavior.
- The asset extraction does not change checklist coverage, finding severity meanings, recording status values, isolation behavior, milestone handoff semantics, or final-closeout boundaries.

## Validator proof

`scripts/test-skill-validator.py` includes a code-review family asset test that checks:

- `skills/code-review/SKILL.md` maps both assets with `COPY`;
- the material-finding asset contains parser-owned finding labels, including `Finding ID:`;
- the result skeleton preserves `clean-with-notes | changes-requested | blocked | inconclusive`;
- the result skeleton does not introduce proposal/spec `approved` status vocabulary.
