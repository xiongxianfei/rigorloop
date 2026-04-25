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
```

Treat `learn` as an advice-only follow-up when a durable lesson actually emerged or another approved rule elevates it.

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
| ADR | `accepted`, `active` | `deprecated`, `superseded`, `archived`, `abandoned` |

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

Default stage order:

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
15. `code-review` in independent-review mode with a first-pass review record before any review-driven fixes.
16. `verify` to check artifact/code/test coherence.
17. `ci` when GitHub workflow automation for a material risk is missing or stale.
18. `explain-change` to summarize why the diff exists.
19. `pr` to prepare and open the pull request when ready.

Follow with `learn` only when a durable lesson actually emerged.

For ordinary non-trivial work in the full-feature lane, carry the baseline change-local pack:

- `docs/changes/<change-id>/change.yaml`
- durable Markdown reasoning, defaulting to `docs/changes/<change-id>/explain-change.md` for new work unless an approved equivalent surface already applies

Keep `review-resolution.md` and `verify-report.md` conditional. Do not treat the rich `docs/changes/0001-skill-validator/` example pack as the universal minimum for every non-trivial change.

### Review-resolution contract

- Material findings must include evidence, required outcome, and a safe resolution path or `needs-decision` rationale.
- Record first-pass material review findings before review-driven fixes when feasible; reconstructed records must say they were reconstructed.
- For non-trivial changes with material findings, use `review-resolution.md` and approved dispositions: `accepted`, `rejected`, `deferred`, `partially-accepted`, and `needs-decision`.
- `needs-decision` is not final and blocks `verify`, `explain-change`, and `pr` until resolved or explicitly deferred by an authorized owner.
- `Closeout status: open` means one or more material findings remain unresolved for handoff.
- `Closeout status: closed` means every material finding has a final disposition plus required action, rationale, follow-up, and validation evidence.
- A review outcome requiring revision still needs a later same-stage review round or explicit reviewer or owner closeout evidence; `review-resolution.md` alone is not a silent substitute for required re-review.

### Review-stage handoff versus downstream readiness

- `spec-review` may report both immediate next repository stage and eventual `test-spec` readiness, but those are different concepts.
- After approved `spec-review`, the immediate next stage is `architecture` when architecture is still required, otherwise `plan`.
- Eventual `test-spec` readiness may be `ready` or `conditionally-ready` after approved `spec-review`; `conditionally-ready` must name the remaining intermediate dependency.
- `changes-requested` and `blocked` pair with eventual `test-spec` readiness `not-ready` and return the workflow to `spec`.
- `inconclusive` pairs with eventual `test-spec` readiness `not-assessed`, records the missing-input stop condition, and leaves immediate next stage empty.
- `plan-review` remains the normal immediate handoff to `test-spec`. If implementation readiness is discussed there, it is downstream readiness rather than the handoff itself.

### Execution-stage claim ownership

- `implement` may report milestone completion, validation, blockers, readiness for `code-review`, or the next milestone, but it does not claim review findings or `branch-ready`.
- Before `implement` hands off to `code-review`, the approved slice should satisfy a `first-pass acceptable result`.
- `implement` targets the `smallest scope-complete change`, not merely the smallest diff.
- The same-slice completeness set includes in-scope requirements, required authored surfaces, required aligned surfaces, required edge cases, and the targeted validation set.
- Required edge cases come from approved artifacts, named regression cases, changed branch conditions or touched failure paths, governing tests or fixtures, and required aligned wording distinctions for the slice.
- If a required surface stays unchanged, `implement` records `unaffected with rationale` in an authoritative surface such as the active plan or required change-local artifacts.
- If missing or contradictory inputs prevent that standard, stop with a blocker instead of handing off an incomplete slice to `code-review`.
- Later review comments may still happen. A `preventable first-pass miss` is only a finding that should have been caught by the same-slice completeness set, required edge cases, or targeted validation before `code-review`.
- `code-review` may inspect staged or unstaged diffs, PR diffs, or commit ranges. If it cites governing artifacts for a clean branch-scoped conclusion, those artifacts must be confirmed in tracked governing branch state.
- Missing tracked governing authority blocks `clean-with-notes`, but it does not suppress independently supported findings from the review surface.
- Named edge cases need direct proof for clean review or `branch-ready` outcomes; code-shape inference alone is insufficient.
- `verify` owns `branch-ready`. `pr` owns `pr-body-ready` and `pr-open-ready`.
- Avoid unqualified `PR-ready` as live workflow guidance or status language.

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
- Approved fast-lane work may still omit `docs/changes/<change-id>/` when the governing workflow contract allows it.
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

## Invocation context and continuation

Classify the request into one of these contexts before deciding whether to continue:

- `workflow-managed`: the agent is carrying a change through its normal downstream stages toward completion under the active lane.
- `isolated`: the user asked for one stage result only, such as standalone `proposal-review`, `spec-review`, `architecture-review`, `code-review`, `verify`, or `explain-change`.
- `direct-pr`: the user directly invoked `pr`.

Rules:

- In v1, workflow-managed autoprogression applies only to:
  - `proposal -> proposal-review`
  - `spec -> spec-review`
  - `architecture -> architecture-review` when that review stage is the next required or default downstream step
  - full-feature execution from `implement` through `pr`
- In the full-feature lane, continue through this downstream chain unless a stop condition applies:
  - `implement -> code-review`
  - `code-review -> review-resolution -> code-review` only for first-pass `changes-requested` findings that are fixable within current approved scope
  - `code-review -> verify` only for first-pass `clean-with-notes` once the review gate is satisfied
  - `verify -> ci` when the governing workflow contract elevates `ci`; otherwise `verify -> explain-change`
  - `ci -> explain-change`
  - `explain-change -> pr`
- In workflow-managed full-feature runs, autoprogressed `code-review` must emit its first-pass review record before any review-driven fix begins.
- In workflow-managed full-feature runs, first-pass `blocked` and `inconclusive` stop instead of entering `review-resolution`.
- Direct `proposal-review`, `spec-review`, `architecture-review`, `code-review`, `verify`, and `explain-change` stay isolated by default unless the user explicitly asks for end-to-end continuation.
- Direct `pr` remains in scope and still performs the `pr` stage itself when readiness passes. Isolation only prevents downstream continuation beyond `pr`.
- Fast-lane and bugfix execution remain on the repository's existing explicit-step behavior in v1.
- Advice-only stages such as `learn` do not auto-run by default.

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

## Continuation and checkpoints

For high-impact changes, produce the artifact and clearly mark whether it is ready for the next stage.

Do not ask for redundant approval merely to enter an already-known next required or default downstream stage in a workflow-managed flow.

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

## Expected output

Always state:

- chosen lane and why;
- invocation context and why;
- current stage;
- artifacts found, created, or missing;
- next recommended skill or next automatic stage;
- blockers or assumptions;
- whether continuation happened, stopped, or is out of scope;
- whether implementation is allowed yet.
