# Skill Readability Behavior-Parity Report

## Scope

- Change: `2026-05-18-skill-readability-self-containment`
- Milestone: M3
- Date: 2026-05-18
- Baseline commit: `837b3e0` after M1 and before the M2 pilot rewrite
- Rewritten source: current `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md`

## Method

This pilot uses manual contract comparison rather than live LLM execution, as allowed by the active test spec. I compared the baseline skill text with the rewritten pilot text on the same representative synthetic inputs and classified observable differences as `equivalent`, `improvement`, or `regression`.

Representative inputs:

- `proposal`: author a proposal for optimizing installed skill readability and self-containment while preserving the priority order quality, clarity, then token cost.
- `proposal-review`: review the revised skill readability and self-containment proposal.

## Comparison

| Skill | Compared behavior | Classification | Notes |
|---|---|---|---|
| `proposal` | Required proposal sections, status values, Vision fit values, standing artifact gates, scope preservation, scope budget, evidence access, artifact placement, and readiness handoff | equivalent | Required output obligations and stop conditions are preserved. |
| `proposal` | Scanability of sections, closed enums, workflow role, rule scope, and output shape | improvement | The rewrite adds a workflow role block, fenced enum blocks, tables, and a fenced fillable skeleton. |
| `proposal-review` | Review dimensions, material-finding fields, review status values, Vision fit review, scope-preservation review, recording behavior, isolation, and downstream handoff boundaries | equivalent | Formal review obligations and result fields are preserved. |
| `proposal-review` | Scanability of review dimensions, enum values, role, rule scope, and result shape | improvement | The rewrite adds a workflow role block, fenced enum blocks, tables, and a fenced result skeleton. |

## Regression Check

| Regression class | Result |
|---|---|
| Missed required proposal section | none found |
| Changed proposal status or Vision fit enum membership | none found |
| Weakened standing artifact gate | none found |
| Weakened scope-preservation rule | none found |
| Missed material review finding requirement | none found |
| Changed review status, dimension result, or recording status enum membership | none found |
| Weakened formal review recording or review-resolution boundary | none found |
| Weakened handoff or stop condition | none found |

## Result

Behavior parity passed for the pilot pair. Observed differences are classified as `equivalent` or `improvement`; no `regression` classification remains.
