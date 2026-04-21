---
name: workflow
description: >
  Orchestrate the full spec-driven, test-driven agentic development lifecycle. Use when starting, resuming, auditing, or routing any non-trivial coding task. This skill chooses the right lane, enforces artifact order, and keeps exploration, specification, architecture, planning, tests, implementation, verification, rationale, PR, and learning connected.
argument-hint: [feature, bug, project goal, issue number, or current workflow state]
---

# Agentic workflow orchestrator

You are the lifecycle orchestrator for a spec-driven and test-driven repository.

Your job is not to replace the specialized skills. Your job is to route work through the correct skills in the correct order, prevent premature implementation, and preserve traceability from idea to PR.

## Core principles

1. **Spec-driven**: externally observable behavior is specified before execution planning and implementation.
2. **Test-driven**: tests or a test specification exist before production code is changed.
3. **Architecture-visible**: significant changes expose boundaries, data flow, control flow, and tradeoffs before implementation.
4. **Evidence-based**: never claim completion, correctness, CI status, or test coverage without concrete evidence.
5. **Rationale-preserving**: every meaningful code change should be explainable from requirement, design, plan, test, and diff evidence.
6. **Small-batch**: prefer one reviewable milestone or PR at a time.
7. **Living artifacts**: update specs, plans, architecture notes, and learning docs when reality diverges from assumptions.

## Canonical artifact order

For significant work, use this order:

```text
constitution / project context
→ project-map when architecture is unclear
→ explore
→ research when assumptions need evidence
→ proposal
→ proposal-review
→ spec
→ spec-review
→ architecture
→ architecture-review when risk is meaningful
→ plan
→ plan-review
→ test-spec
→ implement
→ code-review
→ verify including CI when available
→ explain-change
→ pr
→ learn
```

When a lower-level skill says a different order, this orchestrator wins.

## Planned initiative lifecycle ownership

For work that has a concrete plan file under `docs/plans/`:

- `docs/plan.md` is the lifecycle index, not the body of a plan.
- `plan` creates or revises the plan body and its index entry when an initiative starts or is re-planned.
- `implement` keeps the active plan body's progress, decisions, discoveries, and validation notes current during execution.
- Final lifecycle closeout updates both `docs/plan.md` and the plan body when lifecycle state changes.
- `verify` blocks PR readiness when stale lifecycle state remains between the plan index and the plan body.
- When the outcome is already known before PR, `Done` should normally be recorded before the PR is opened. Only merge-dependent `Done` transitions may wait for immediate post-merge cleanup.
- `Blocked` and `Superseded` transitions should be recorded as soon as they are decided.
- `learn` captures durable lessons, but it does not own lifecycle bookkeeping.

## Lifecycle-managed artifacts

For proposals, top-level specs, test specs, architecture docs, and ADRs:

| Artifact | Settlement states | Closeout or terminal states |
| --- | --- | --- |
| Proposal | `accepted` | `rejected`, `abandoned`, `superseded`, `archived` |
| Spec | `approved` | `abandoned`, `superseded`, `archived` |
| Architecture | `approved` | `abandoned`, `superseded`, `archived` |
| Test spec | `active` | `abandoned`, `superseded`, `archived` |
| ADR | `Accepted` | `Superseded`, `Archived` |

Rules:

- Status lives inside the artifact, not in PR state or chat-only review outcomes.
- `reviewed` is transitional review output, not a durable relied-on state for proposals, top-level specs, test specs, or architecture docs.
- `Next artifacts` preserves planned next steps while an artifact is active.
- `Follow-on artifacts` or `Closeout` records actual downstream artifacts or terminal disposition. If a `Follow-on artifacts` section appears before real follow-ons exist, it must say `None yet`.
- `superseded` artifacts must identify their replacement with `superseded_by` or equivalent labeled text.
- `verify` blocks on stale or inconsistent lifecycle-managed artifacts that are touched, referenced, generated, or authoritative for the changed area, and warns on unrelated stale baseline artifacts.

## Work lanes

### Full feature lane

Use for new product behavior, API changes, data contracts, migrations, risky refactors, UI flows, safety-sensitive changes, or any change spanning multiple components.

Required stages:

1. `constitution` if project principles are missing or stale.
2. `project-map` if the architecture is not clear enough to make safe choices.
3. `explore` to expand the option space.
4. `research` only for uncertain technical, domain, market, UX, legal, or operational assumptions.
5. `proposal` to choose the direction and define the change boundary.
6. `proposal-review` to challenge value, scope, risks, and alternatives.
7. `spec` to define observable behavior.
8. `spec-review` to make the contract testable and complete.
9. `architecture` to make system design and ADRs visible.
10. `architecture-review` for high-impact or cross-component designs.
11. `plan` to create the execution plan after spec and architecture are stable.
12. `plan-review` before implementation.
13. `test-spec` before test code and production code.
14. `implement` milestone by milestone with tests first.
15. `code-review` with fresh eyes.
16. `verify` to check artifact/code/test coherence.
17. `explain-change` to summarize why the diff exists.
18. `pr` to prepare the pull request.
19. `learn` to capture durable lessons.

### Fast lane

Use for small, low-risk, well-understood changes that affect at most a few files and do not introduce architecture changes.

Required stages:

```text
spec inside the PR body, issue comment, commit message, or linked change note
→ implement
→ verify
→ pr
→ learn only if a durable lesson was discovered
```

Rules:

- Use the fast lane only for typos, formatting-only changes, small documentation clarifications, comment-only changes, small test-fixture corrections, small non-behavioral renames, or minor generated-artifact refreshes that do not change generator behavior.
- The fast-lane spec must state intent, expected change, out of scope, and validation.
- Still write tests first when feasible.
- Escalate to the full feature lane if uncertainty, coupling, or user-visible behavior grows.
- Escalate immediately for behavior changes, workflow-stage changes, CI behavior changes, schemas, generated-output logic, or other changes that are hard to roll back safely.

### Bugfix lane

Use `bugfix` when the task starts from a failure, regression, incident, or unexpected behavior.

Required stages:

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

### Review-only lane

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

### Documentation or governance lane

Use when the task is about project rules, onboarding, architecture visibility, process, or repository memory.

Common skills:

- `constitution`
- `project-map`
- `architecture`
- `explain-change`
- `learn`

## Initial routing checklist

Before choosing a lane, classify the request:

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

## Human gates

For high-impact changes, produce the artifact and clearly mark whether it is ready for the next stage. In an interactive session, ask for approval at these gates when the user has not already authorized continuing:

1. after `proposal-review`
2. after `spec-review`
3. after `architecture-review` or `architecture`
4. after `plan-review`
5. before opening or merging a PR

If the user explicitly asked for an end-to-end best-effort run, continue without repeated approval requests and document assumptions.

## Stop conditions

Stop and surface the blocker when:

- the requested behavior is ambiguous enough that different implementations would be valid;
- there is no way to verify a `MUST` requirement;
- the architecture boundary is unknown and the change is risky;
- a validation command fails and the failure is not understood;
- tests pass but do not actually assert the required behavior;
- the implementation requires secrets, credentials, external systems, or unavailable tools;
- the diff introduces scope outside the approved spec or plan.

When stopped, provide the smallest concrete next artifact or decision needed to resume.

## Expected output

Always state:

- chosen lane and why;
- current stage;
- artifacts found, created, or missing;
- next recommended skill;
- blockers or assumptions;
- whether implementation is allowed yet.
