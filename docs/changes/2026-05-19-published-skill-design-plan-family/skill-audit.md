# Published Skill Design Plan Family Skill Audit

Change: `2026-05-19-published-skill-design-plan-family`
Milestone: M1
Date: 2026-05-19
Scope: `skills/plan/SKILL.md`, `skills/plan-review/SKILL.md`

## Purpose

Audit `plan` and `plan-review` before validator or skill-body changes rely on
the evidence. This file records existence justification, published-skill design
gaps, deterministic validation implications, and follow-on boundaries.

## Summary

| Skill | Existence result | Primary value | M3 rewrite needed | Merge/retire candidate |
|---|---|---|---:|---:|
| `plan` | keep | Durable plan artifact contract, milestone sequencing, state ownership, validation/recovery planning, readiness boundary | yes | no |
| `plan-review` | keep | Formal lifecycle review gate, review dimension contract, material finding shape, durable recording, downstream handoff boundary | yes | no |

Both skills earn their existence. Neither should be merged, retired, renamed, or
changed in ownership in this slice.

## Audit categories

| Category | `plan` | `plan-review` | M1 result |
|---|---|---|---|
| description routing gap | partial | partial | M3 should tighten near misses and competing-skill boundaries. |
| missing near-miss boundary | yes | yes | Add boundaries against `spec`, `test-spec`, `implement`, `code-review`, `verify`, and `pr` where relevant. |
| body contains hidden trigger logic | partial | partial | Body `When to use` / purpose sections contain useful scope guidance; essential selection logic should remain in `description` after M3. |
| missing workflow role | yes | yes | Both are lifecycle skills and need explicit `Workflow role` blocks under R30. |
| missing output template | no | no | Both have compact expected output/result skeletons; M3 should preserve or compact them. |
| unavailable internal dependency | no material blocker | no material blocker | Both use project-local wording and portable path lookup. M3 should preserve customer-project portability. |
| resource map missing | not applicable | not applicable | Neither ships packaged `references/`, `scripts/`, or `assets/` resources. |
| validation over-applied | no | no | Validation guidance is stage-appropriate. |
| validation under-specified | partial | partial | M3 should keep exact validation/result expectations visible without expanding into broad semantic scoring. |
| generic skill candidate | no | no | Both encode specialized lifecycle workflow that the base model would not perform reliably unaided. |
| script candidate | no | no | No repeated deterministic helper belongs in the skill package for this slice. |
| reference split candidate | possible for `plan` | no | `plan` is long; M3 may move rare detail only if packaged resources are introduced with a resource map, but this slice should prefer body compaction first. |
| example/counterexample candidate | possible | possible | Tiny examples may help output skeleton clarity; long examples are out of scope. |
| token-cost risk | yes | moderate | Baseline tokens are recorded below; M3 should avoid body growth. |

## Skill: `plan`

### Existence gate

`plan` should be kept because it encodes:

- durable artifact contract for concrete plan files and `docs/plan.md` index updates;
- repeatable lifecycle procedure for turning approved specs into reviewable milestones;
- stage contract for current handoff summaries and milestone states;
- validation and recovery planning that the base model often omits;
- trust boundaries around readiness, Done, final closeout, branch readiness, and PR readiness.

### Current strengths

- Frontmatter description is concise and under the 1024-character limit.
- Body contains substantial execution procedure for upstream status settlement, plan placement, milestone format, milestone states, current handoff summaries, validation, and stop conditions.
- The skill explicitly separates `docs/plan.md` as an index from concrete plan bodies.
- The skill preserves readiness-vs-Done and final-closeout boundaries.
- The skill includes a compact expected output block.

### Gaps to address in M3

- Add an explicit `Workflow role` block stating lifecycle role, input, output/status, and downstream claims it must not make.
- Tighten `description` so routing is clear from frontmatter, including near misses for product direction, spec authoring, test-spec authoring, implementation, review, verification, and PR handoff.
- Keep body scope guidance after load, but do not rely on body-only trigger logic.
- Compact or clarify rare detail only if behavior-preservation evidence shows the essential rules remain.
- Preserve upstream status settlement, plan-body/index ownership, milestone-state vocabulary, current handoff summary ownership, and readiness-vs-Done language.

## Skill: `plan-review`

### Existence gate

`plan-review` should be kept because it encodes:

- formal lifecycle review gate for execution plans before implementation;
- repeatable review dimension contract covering scope, sequencing, dependencies, validation, risk, and maintainability;
- material finding shape with evidence, required outcome, and safe resolution;
- review recording obligations and clean/material review artifact behavior;
- downstream handoff boundary that preserves `test-spec` as the immediate next stage.

### Current strengths

- Frontmatter description is concise and under the 1024-character limit.
- Review dimensions are explicit and reviewable.
- Material finding requirements are concrete.
- Formal review recording guidance is strong and matches workflow governance.
- The expected result block is compact and stage-specific.

### Gaps to address in M3

- Add an explicit `Workflow role` block stating the review stage, received artifact, produced review status/evidence, and downstream claims it must not make.
- Tighten `description` with near misses for implementation review, spec review, final verification, and PR readiness.
- Preserve clean review receipt behavior, detailed review record triggers, material finding shape, blocked recording behavior, and isolated-review handoff semantics.
- Preserve `test-spec` as the immediate next stage on approval and keep implementation readiness as downstream readiness only.

## Token baseline

Measured with:

```bash
python scripts/measure-skill-tokens.py --skills-root skills
```

| Skill | Bytes | Lines | Estimated tokens |
|---|---:|---:|---:|
| `plan` | 14070 | 303 | 3518 |
| `plan-review` | 6529 | 165 | 1631 |

## Deterministic validator implications

M1 did not identify a production validator gap that must be fixed before M3.
M2 should still add or reuse deterministic tests for this plan-family evidence
shape if needed, especially:

- evidence files exist for audit, routing coverage, behavior preservation, and behavior parity;
- plan-family scope remains limited to `skills/plan/SKILL.md` and `skills/plan-review/SKILL.md`;
- no runtime model-selection or broad semantic prose scoring is introduced;
- token baseline evidence is present before M3.

Production validator changes are conditional. If M2 finds the existing validator
already covers the deterministic requirements, record that no-change result
instead of adding brittle wording checks.

## Merge/retire candidates

None.

## M1 result

M1 evidence supports proceeding to M2. The M3 rewrite should be scoped to
routing, workflow role, execution-body clarity, output skeleton preservation,
and behavior-preservation/parity updates for `plan` and `plan-review`.
