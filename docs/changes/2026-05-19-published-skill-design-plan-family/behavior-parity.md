# Published Skill Design Plan Family Behavior Parity

Change: `2026-05-19-published-skill-design-plan-family`
Milestone: M3 final
Date: 2026-05-19
Scope: `skills/plan/SKILL.md`, `skills/plan-review/SKILL.md`

## Purpose

Record representative parity results for the M3 `plan` and `plan-review`
rewrites.

## Token baseline

Measured with:

```bash
python scripts/measure-skill-tokens.py --skills-root skills
```

| Skill | Baseline bytes | Baseline lines | Baseline estimated tokens | M3 bytes | M3 lines | M3 estimated tokens | Token delta | Delta percent | M3 result |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `plan` | 14070 | 303 | 3518 | 15447 | 317 | 3862 | +344 | +9.78% | within +10% hard cap |
| `plan-review` | 6529 | 165 | 1631 | 7183 | 157 | 1794 | +163 | +9.99% | within +10% hard cap |

## Representative `plan` parity cases

| Case ID | Input shape | Baseline expected behavior | M3 result |
|---|---|---|---|
| PLAN-P1 | Approved proposal/spec with no architecture needed, user asks for an execution plan. | Create or revise a concrete plan under `docs/plans/`, update `docs/plan.md` when starting/replanning, include milestones, validation, recovery, dependencies, progress, decisions, validation notes, outcome, and readiness. | Preserved by output paths, required sections, outputs, and output skeleton. |
| PLAN-P2 | Upstream spec status is stale but clean spec-review evidence exists. | Settle only lifecycle/status/readiness/follow-on/closeout metadata using explicit mappings; block on missing, contradictory, or unmapped evidence. | Preserved by upstream status settlement. |
| PLAN-P3 | User asks to start implementation while planning. | Do not implement; produce plan and hand off to `plan-review` / `test-spec` sequence. | Preserved by description, handoff, claims, and planning rules. |
| PLAN-P4 | Milestone-based plan is created or revised. | Include allowed milestone states and `Current Handoff Summary` fields; keep final closeout not ready while implementation milestones remain. | Preserved by milestone-aware plans. |
| PLAN-P5 | User asks whether the plan is Done after plan authoring. | State readiness, not Done; list remaining gates. | Preserved by progress/readiness/Done wording and output skeleton. |

## Representative `plan-review` parity cases

| Case ID | Input shape | Baseline expected behavior | M3 result |
|---|---|---|---|
| PRV-P1 | Concrete plan is scoped, sequenced, and verifiable. | Return approved review status, no material findings, record clean receipt and review log, no empty review-resolution, immediate next stage `test-spec`. | Preserved by Isolation and Recording plus output skeleton. |
| PRV-P2 | Plan milestone is too vague or missing validation commands. | Return material finding with severity, location, evidence, required outcome, and safe resolution path. | Preserved by Material findings and output skeleton. |
| PRV-P3 | Review evidence cannot be written. | Report `Recording status: blocked` with blocker and smallest next action. | Preserved by Isolation and Recording and output skeleton. |
| PRV-P4 | Direct isolated review has material findings. | State no automatic downstream handoff, list finding IDs, required record path, record-before-fixing or reconstruction status, and owner-decision status. | Preserved by Isolation and Recording. |
| PRV-P5 | User asks plan-review to review implementation code. | Treat as competing `code-review` scope, not plan-review. | Preserved by description and workflow role claim boundary. |

## M3 Final Parity Statement

No lifecycle behavior weakening was found. Material review status, finding
format, recording obligations, stop conditions, validation obligations,
plan-state ownership, and claim boundaries remain intact. The only behavior
change is improved published-skill routing, explicit workflow-role metadata,
and compact output skeletons required by the skill contract.
