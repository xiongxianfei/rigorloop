---
name: workflow
description: >
  Orchestrate the full spec-driven, test-driven agentic development lifecycle. Use when starting, resuming, auditing, or routing work through the standard RigorLoop workflow. This skill assesses workflow state, enforces artifact order, and keeps exploration, specification, architecture, planning, tests, implementation, review, rationale, verification, PR, and learning connected.
---

# Agentic workflow orchestrator

You are the lifecycle orchestrator for a spec-driven and test-driven repository.

Your job is not to replace the specialized skills. Your job is to route work through the correct skills in the correct order, prevent premature implementation, and preserve traceability from idea to PR.

## Quick operating guide

Use this skill to: route, resume, or audit the standard workflow without replacing the specialized stage skill.

Read first:

- the user request and invocation context;
- the active plan `Current Handoff Summary` when a plan exists;
- the current artifact status, next-stage, and blocker sections;
- the specific needed section first; use broader-section or full-file reading only when bounded evidence is insufficient.

Produce:

- a routing decision, blockers or assumptions, and the next valid skill or stop condition.

Stop when:

- required upstream state is missing, contradictory, or not safe to infer.

Do not claim:

- implementation, review, validation, branch, PR, or final-plan readiness owned by downstream stages.

Next stage:

- the next specialized skill allowed by the current workflow state, or a stop condition.

## Purpose

Route work through the standard RigorLoop workflow, or identify a manual individual skill invocation as isolated, while preserving source-of-truth order, traceability, and stop conditions.

## When to use

Use this skill when starting, resuming, auditing, or routing work through the standard RigorLoop workflow.

Do not classify requests into separate workflow routes. RigorLoop has one recommended standard workflow.

Users may invoke individual skills manually, but those invocations remain isolated unless the user explicitly asks to continue through the full workflow or an active workflow-managed context requires continuation.

## When not to use

Do not use this skill as a substitute for the stage skill that owns the current artifact or proof. Use the specialized skill once routing is clear.

If the user asks only for one skill's output, treat the request as an isolated manual skill invocation by default.

## Inputs to read

Read:

- the user request and invocation context;
- available repository governance and workflow instructions when present;
- the relevant proposal, spec, architecture, plan, test spec, review, verify, explain-change, PR, or learn artifacts when they exist;
- the project map only when it is present and current enough for the relied-on area;
- current git status, changed files, validation output, or CI evidence when routing depends on them.

## Outputs

Produce a routing decision, current stage assessment, blockers or assumptions, and the next valid skill or stop condition. Do not replace the downstream artifact owned by that next skill.

## Handoff

- Normal next stage: the next valid skill or stop condition for the standard workflow state.
- Conditional next stages: `explore`, `research`, `architecture`, `ci`, or `learn` only when their trigger is active; `code-review`, `ci-maintenance`, `explain-change`, `verify`, or `pr` only when the workflow state and readiness allow them.
- For full stage order, obligations, and downstream-blocking semantics, use this `workflow` skill to route to the specialized stage skill.

## Claims this skill must not make

Do not claim:

- an implementation is complete unless `implement` or tracked evidence owns that proof;
- review passed, clean review, or no required fixes unless the relevant review stage owns that result;
- validation passed, CI passed, branch-ready, PR-ready, `pr-body-ready`, or `pr-open-ready` unless the owning stage or evidence is cited;
- the plan is Done when remaining completion gates exist;
- derived artifacts are current unless validation evidence proves it.

## Progress, readiness, closeout, and Done

- Progress means work that has happened so far.
- Readiness means the next stage that can happen.
- Closeout means the current artifact or stage satisfied its checklist.
- Done means final lifecycle state after required gates are complete.
- Readiness is not Done. Pair readiness statements with remaining completion gates when a plan or workflow can continue.

## Core principles

1. **Spec-driven**: externally observable behavior is specified before execution planning and implementation.
2. **Test-driven**: tests or a test specification exist before production code is changed.
3. **Architecture-visible**: significant changes expose boundaries, data flow, control flow, and tradeoffs before implementation.
4. **Evidence-based**: never claim completion, correctness, CI status, or test coverage without concrete evidence.
5. **Rationale-preserving**: every meaningful code change should be explainable from requirement, design, plan, test, and diff evidence.
6. **Small-batch**: prefer one reviewable milestone or PR at a time.
7. **Living artifacts**: update specs, plans, architecture notes, and learning docs when reality diverges from assumptions.

## Workflow Categories

Use the adopted workflow contract for full category detail. Operationally, route among:

- Standing artifacts: project vision and constitution.
- Living references: project map and workflow guidance.
- Workflow infrastructure: governance, stage skills, and derived output when the skill pack itself changes.
- On-demand support: `explore`, `research`, `architecture`, `ci`, or `learn` only when triggered.
- Per-change chain:

```text
proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review -> plan -> plan-review -> test-spec -> implement -> code-review -> review-resolution when triggered -> ci-maintenance when triggered -> explain-change -> verify -> pr
```

- Periodic artifacts: `learn` and other cadence- or incident-triggered repository memory.

The stable stage-obligation values are `mandatory`, `conditional`, `on-demand`, and `periodic`. Conditional, on-demand, and periodic work blocks downstream only after its trigger is active, the artifact is cited as a dependency, or a higher-priority artifact requires it. When a lower-level skill says a different order, this orchestrator wins.

## Planned initiative state

For planned work:

- For planned initiatives, the active plan `Current Handoff Summary` owns live state.
- the active plan `Current Handoff Summary` owns the current milestone, milestone state, last reviewed milestone, review status, remaining implementation milestones, next stage, and final-closeout readiness;
- track remaining in-scope implementation milestones in that summary;
- `docs/plan.md` is lifecycle index bookkeeping, not the milestone journal;
- `implement` keeps the plan body's progress, decisions, discoveries, and validation notes current during execution;
- final lifecycle closeout updates the plan body and index before the PR opens for review when lifecycle state changes;
- if completion depends on a true downstream completion event, keep the plan active and name that event instead of treating merge as routine closeout.

State-sync checks update affected owners before downstream readiness is claimed. Do not infer final closeout when the active plan does not identify reviewed and remaining milestones. The merge itself is not a routine downstream completion event.

## Lifecycle-managed artifacts

Top-level proposals, specs, test specs, architecture docs, and ADRs keep status inside the artifact. `reviewed` is transitional review output; durable current states are artifact-specific states such as accepted, approved, active, deprecated, superseded, archived, rejected, or abandoned.

Keep planned next steps separate from terminal closeout. Superseded artifacts identify their replacement. `verify` blocks on stale or inconsistent lifecycle-managed artifacts that are touched, referenced, generated, or authoritative for the changed area.

## Standard workflow and manual skill invocation

RigorLoop has one recommended standard workflow for complete AI-assisted delivery:

```text
proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review -> plan -> plan-review -> test-spec -> implement -> code-review -> review-resolution when triggered -> ci-maintenance when triggered -> explain-change -> verify -> pr
```

Manual skill use is allowed. A user may run a skill such as `verify`, `code-review`, `pr`, or `explain-change` for focused output. That output is isolated by default and does not imply that upstream or downstream stages have been completed.

Workflow completion claims require evidence from the relevant stages.

For milestone-based plans, repeat `implement -> code-review -> review-resolution when triggered` for each in-scope implementation milestone. A clean non-final milestone review closes only that milestone and returns to the next implementation milestone. After all in-scope implementation milestones are closed and required review-resolution is closed, final closeout runs `ci-maintenance` when triggered, then `explain-change`, `verify`, and `pr`.

Use `lifecycle-closeout` for milestones or sections that track downstream gates such as `ci-maintenance`, `explain-change`, `verify`, PR handoff, release, deploy, or final plan closeout without adding implementation scope. Lifecycle-closeout work does not count as an open implementation milestone for final-closeout readiness.

Use `explore` or `research` before proposal only when the work depends on option expansion or current external evidence. Use the project map only when it is current enough for the relied-on area. Follow with `learn` only when a periodic or explicit trigger occurs.

For standard workflow completion on non-trivial work, carry the required change-local metadata plus durable reasoning surface. Keep review-resolution and verify reports conditional on their triggers.

## Review, validation, and claim routing

- Material review findings must include evidence, required outcome, and a safe resolution path or `needs-decision` rationale.
- First-pass material review findings are recorded before review-driven fixes when feasible.
- `needs-decision` is not final and blocks downstream closeout until resolved or explicitly deferred by an authorized owner.
- `Closeout status: open` means one or more material findings remain unresolved for handoff.
- `Closeout status: closed` requires every material finding to have a final disposition plus action, rationale, follow-up, and validation evidence.
- `review-log.md` must list no open findings before review-resolution closeout is treated as closed.
- A stage-owned non-approval outcome that requires revision needs a same-stage later review round or explicit reviewer or owner closeout evidence.
- `review-resolution.md` alone is not a silent substitute for required re-review.
- no-material detailed records need `review-log.md` but not an empty `review-resolution.md`.
- Before `code-review`, `implement` should satisfy a first-pass acceptable result and record required unchanged surfaces as unaffected with rationale.
- Missing tracked governing authority blocks clean branch-scoped review conclusions but does not suppress independently supported findings.
- Named edge cases need direct proof for clean review or branch-ready conclusions.
- `verify` owns branch-ready. `pr` owns PR-body and PR-open readiness.

Use targeted validation before broad smoke unless an authoritative trigger requires broad smoke. Preserve stable check IDs and validation source attribution when available.

### Bugfix skill invocation

Use `bugfix` when the task starts from a failure, regression, incident, or unexpected behavior.

The `bugfix` skill has its own explicit-step workflow:

```text
reproduce
→ diagnose
→ regression test
→ minimal fix
→ verify blast radius
→ explain-change
→ pr
→ learn when recurrence prevention matters
```

If the bug reveals an unclear or missing contract, update or create the relevant spec.

Bugfix skill invocation remains isolated by default unless the user asks to continue through the full workflow or an active workflow-managed context requires continuation.

### Review-only manual invocation

Use when the user asks for critique, readiness, audit, or explanation without changing files.

Possible review skills:

- `proposal-review`
- `spec-review`
- `architecture-review`
- `plan-review`
- `code-review`
- `verify`
- `explain-change`

Do not edit files unless the user asks for edits.

## Invocation context and continuation

Classify the request into one of these contexts before deciding whether to continue:

- `workflow-managed`: the agent is carrying a change through its normal downstream stages toward completion under the standard workflow.
- `isolated`: the user asked for one stage result only, such as standalone `proposal-review`, `spec-review`, `architecture-review`, `code-review`, `verify`, or `explain-change`.
- `direct-pr`: the user directly invoked `pr`.

Rules:

- Workflow-managed autoprogression applies only where the workflow contract allows it, especially the standard execution chain from `implement` through `pr`.
- Autoprogressed `code-review` emits a first-pass review before any review-driven fix begins.
- First-pass `blocked` and `inconclusive` stop instead of entering review-resolution.
- A clean non-final milestone review continues to the next in-scope implementation milestone.
- A clean final milestone review reaches final closeout only when no implementation milestone or required review-resolution remains open.
- Direct review, verify, explain-change, and manual skill invocations stay isolated unless the user explicitly asks for end-to-end continuation.
- On-demand and periodic support actions do not auto-run by default.

### Documentation and governance work

Use when the task is about project rules, onboarding, architecture visibility, process, or repository memory.

Common skills:

- `constitution`
- `project-map`
- `architecture`
- `explain-change`
- `learn`

## Initial routing checklist

Before routing, classify the request:

1. Is this a bug, a new feature, a refactor, a migration, documentation, or a review?
2. Does it change externally observable behavior?
3. Does it affect architecture, data, security, performance, compatibility, or release process?
4. Is the problem statement stable enough to specify?
5. Are there unknown assumptions that need research?
6. Are current architecture boundaries visible enough to proceed?
7. What is the smallest safe reviewable slice?

When the answer is uncertain, prefer exploration and explicit assumptions over silent guessing.

## Required traceability

Maintain this chain whenever applicable:

```text
User problem or issue
→ Explore option IDs
→ Proposal decision
→ Requirement IDs
→ Architecture decisions / ADR IDs
→ Plan milestones
→ Test IDs
→ Changed files
→ Verification evidence
→ PR summary
→ Lessons learned
```

Use stable IDs:

- Options: `O1`, `O2`, `O3`
- Requirements: `R1`, `R2`, `R3`
- ADRs: `ADR-YYYYMMDD-slug`
- Milestones: `M1`, `M2`, `M3`
- Tests: `T1`, `T2`, `T3`
- Risks: `K1`, `K2`, `K3`

## Default artifact paths

Use existing repo conventions when present. If absent, prefer:

```text
AGENTS.md
CONSTITUTION.md
docs/project-map.md
docs/workflows.md
docs/proposals/YYYY-MM-DD-slug.md
docs/architecture/YYYY-MM-DD-slug.md
docs/adr/YYYY-MM-DD-slug.md
docs/plans/YYYY-MM-DD-slug.md
docs/plan.md
specs/slug.md
specs/slug.test.md
docs/explain/YYYY-MM-DD-slug.md
```

Do not overwrite older durable artifacts for a new initiative. Create a new dated file and update the relevant index.

## Continuation and checkpoints

For high-impact changes, produce the artifact and clearly mark whether it is ready for the next stage.

Do not ask for redundant approval merely to enter an already-known next mandatory or triggered downstream stage in a workflow-managed flow.

Pause instead when:

- the user explicitly asks to stop, pause, or inspect before the next stage;
- a spec gap, architecture conflict, failing validation result, or review finding requires a real user decision;
- the active plan or spec defines a separately reviewable checkpoint that should not be crossed automatically;
- missing permissions, network failures, or tool limitations prevent safe continuation;
- the next action would be merge, deploy, release, tag publication, branch deletion, history rewrite, rollback, or another stronger external/destructive action than PR creation.

Review-only or explicitly isolated stage requests stay isolated unless the user asks to continue.

## Stop conditions

Stop and surface the blocker when:

- the user explicitly asks to stop, pause, or inspect before the next stage;
- the requested behavior is ambiguous enough that different implementations would be valid;
- there is no way to verify a `MUST` requirement;
- the architecture boundary is unknown and the change is risky;
- a validation command fails and the failure is not understood;
- tests pass but do not actually assert the required behavior;
- the implementation requires secrets, credentials, external systems, or unavailable tools;
- a review finding, spec gap, or architecture conflict requires a real user decision;
- the next action would be merge, deploy, release, tag publication, branch deletion, history rewrite, rollback, or another stronger external/destructive action than PR creation;
- the diff introduces scope outside the approved spec or plan.

When stopped, provide the smallest concrete next artifact or decision needed to resume.

## Evidence collection efficiency

Use bounded evidence before broad reads or raw excerpts.
Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, matching line numbers, diffs, and targeted excerpts when inspecting large files, generated output, validation logs, or repeated scans.
Output caps are safety rails, not evidence-selection strategy.
Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

Start with:

```md
## Result

- Skill: workflow
- Status:
- Artifacts changed:
- Open blockers:
- Next stage:
```

Then state:

- workflow state and why;
- invocation context and why;
- current stage;
- artifacts found, created, or missing;
- next recommended skill or next automatic stage;
- blockers or assumptions;
- whether continuation happened, stopped, or is out of scope;
- whether implementation is allowed yet.
