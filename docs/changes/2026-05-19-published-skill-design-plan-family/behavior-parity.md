# Published Skill Design Plan Family Behavior Parity

Change: `2026-05-19-published-skill-design-plan-family`
Milestone: M1 scaffold
Date: 2026-05-19
Scope: `skills/plan/SKILL.md`, `skills/plan-review/SKILL.md`

## Purpose

Define representative parity cases for the M3 `plan` and `plan-review` rewrites.
M1 records the baseline expectations and token estimates. M3 must update this
file with final parity results after skill-body edits.

## Token baseline

Measured with:

```bash
python scripts/measure-skill-tokens.py --skills-root skills
```

| Skill | Baseline bytes | Baseline lines | Baseline estimated tokens | M3 result |
|---|---:|---:|---:|---|
| `plan` | 14070 | 303 | 3518 | pending |
| `plan-review` | 6529 | 165 | 1631 | pending |

## Representative `plan` parity cases

| Case ID | Input shape | Baseline expected behavior | M3 parity requirement |
|---|---|---|---|
| PLAN-P1 | Approved proposal/spec with no architecture needed, user asks for an execution plan. | Create or revise a concrete plan under `docs/plans/`, update `docs/plan.md` when starting/replanning, include milestones, validation, recovery, dependencies, progress, decisions, validation notes, outcome, and readiness. | Same artifact ownership and required sections remain intact. |
| PLAN-P2 | Upstream spec status is stale but clean spec-review evidence exists. | Settle only lifecycle/status/readiness/follow-on/closeout metadata using explicit mappings; block on missing, contradictory, or unmapped evidence. | Same settlement discipline remains intact. |
| PLAN-P3 | User asks to start implementation while planning. | Do not implement; produce plan and hand off to `plan-review` / `test-spec` sequence. | Same no-implementation and stage-order boundary remains intact. |
| PLAN-P4 | Milestone-based plan is created or revised. | Include allowed milestone states and `Current Handoff Summary` fields; keep final closeout not ready while implementation milestones remain. | Same active-state ownership remains intact. |
| PLAN-P5 | User asks whether the plan is Done after plan authoring. | State readiness, not Done; list remaining gates. | Same readiness-vs-Done boundary remains intact. |

## Representative `plan-review` parity cases

| Case ID | Input shape | Baseline expected behavior | M3 parity requirement |
|---|---|---|---|
| PRV-P1 | Concrete plan is scoped, sequenced, and verifiable. | Return approved review status, no material findings, record clean receipt and review log, no empty review-resolution, immediate next stage `test-spec`. | Same clean review and handoff behavior remains intact. |
| PRV-P2 | Plan milestone is too vague or missing validation commands. | Return material finding with severity, location, evidence, required outcome, and safe resolution path. | Same finding shape remains intact. |
| PRV-P3 | Review evidence cannot be written. | Report `Recording status: blocked` with blocker and smallest next action. | Same blocked-recording behavior remains intact. |
| PRV-P4 | Direct isolated review has material findings. | State no automatic downstream handoff, list finding IDs, required record path, record-before-fixing or reconstruction status, and owner-decision status. | Same isolation/recording boundary remains intact. |
| PRV-P5 | User asks plan-review to review implementation code. | Treat as competing `code-review` scope, not plan-review. | Same near-miss boundary remains intact. |

## Evidence required in M3

M3 must update this file with:

- after-change token estimates for `plan` and `plan-review`;
- final parity result for each case above;
- confirmation that material review status, finding format, recording
  obligations, stop conditions, validation obligations, plan-state ownership,
  and claim boundaries were not weakened.

## M1 conclusion

The parity baseline is sufficient for M2 and M3 to proceed. No final parity
claim is made in M1 because no skill-body rewrite has happened yet.
