---
name: plan
description: >
  Create or revise a living execution plan after proposal, spec, and architecture are stable enough to implement. Use for multi-file, multi-component, risky, or milestone-based work that should be split into reviewable milestone slices.
---

# Living execution plan

You are turning approved behavior and architecture into a safe, reviewable implementation path.

Planning happens after the spec defines behavior and architecture defines the design direction. Do not use this skill to decide what the product should be.

## Inputs to read

Read:

- `AGENTS.md`
- `CONSTITUTION.md` if present
- `docs/plan.md` if present
- accepted proposal
- approved or reviewed feature spec
- spec-review findings
- architecture doc and ADRs when relevant
- architecture-review findings when available
- test-spec if already created
- `docs/project-map.md`
- relevant code, tests, CI, and workflows

## Output paths

Prefer:

```text
docs/plans/YYYY-MM-DD-slug.md
docs/plan.md
```

Create a new dated plan for new initiatives. Update `docs/plan.md` as the lifecycle index of active, blocked, done, and superseded plans.
For planned initiatives, `docs/plan.md` remains the lifecycle index while files under `docs/plans/` remain the plan bodies. `plan` owns creating or revising those surfaces when an initiative starts or is re-planned, not every later execution-time update.

## Required sections

1. **Status**: draft, reviewed, active, blocked, done, superseded.
2. **Purpose / big picture**: why this implementation plan exists.
3. **Source artifacts**: proposal, spec, architecture, test spec.
4. **Context and orientation**: files, modules, flows, and constraints a new contributor needs.
5. **Non-goals**: scope guardrails from proposal/spec.
6. **Requirements covered**: list requirement IDs and where they will be implemented.
7. **Milestones**: small reviewable slices.
8. **Validation plan**: commands and manual checks per milestone.
9. **Risks and recovery**: rollback, feature flags, migration recovery, idempotence.
10. **Dependencies**: internal and external sequencing constraints.
11. **Progress**: checkboxes or status per milestone.
12. **Decision log**: implementation decisions made during planning.
13. **Surprises and discoveries**: updated during implementation.
14. **Validation notes**: evidence from implementation.
15. **Outcome and retrospective**: filled after completion.

## Milestone format

Each milestone should include:

```text
M1. Title
- Goal:
- Requirements:
- Files/components likely touched:
- Dependencies:
- Tests to add/update:
- Implementation steps:
- Validation commands:
- Expected observable result:
- Commit message: `M1: <completed milestone outcome>`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
- Rollback/recovery:
```

Milestones should be small enough for one review loop and one coherent commit. A PR may contain one or more completed milestones when that is the clearest review boundary.

## Planning rules

- Derive work from spec requirements and architecture decisions.
- Do not add behavior not in the spec.
- Do not hide risky work in vague milestones.
- Do not omit validation commands.
- Keep `docs/plan.md` as an index, not a second long-form plan body.
- When planning starts a new initiative or replaces an older one, update the relevant `docs/plan.md` entry and plan body in the same planning change.
- Do not create a plan that only the current chat context can understand.
- Do not proceed to implementation until `plan-review` and `test-spec` are ready unless using the fast lane.
- If planning reveals spec or architecture gaps, update those artifacts first.

## Evidence collection efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations when inspecting large files, repeated scans, generated output, or validation output. Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

- concrete plan file path;
- updated `docs/plan.md` index when applicable;
- milestone-by-milestone plan;
- validation and recovery strategy;
- readiness statement for `plan-review` and `test-spec`.
