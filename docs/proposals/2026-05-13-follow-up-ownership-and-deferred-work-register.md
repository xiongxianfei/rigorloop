# Follow-Up Ownership and Deferred Work Register

## Status

accepted

## Problem

RigorLoop changes often discover work that should not be done immediately:

- future release packaging improvements;
- later token-cost optimization;
- example migration follow-ups;
- validator hardening;
- documentation cleanup;
- recurring process risks;
- future architecture or workflow improvements.

Today, future items can appear in many places:

```text
proposal follow-ons
plan notes
change.yaml
explain-change
learn sessions
project-map risk areas
chat
PR comments
```

This creates confusion:

```text
Where should deferred work live?
Which skill owns it?
Should project-map track it?
How does a future agent find it without searching many artifacts?
```

`project-map` is not the right owner. Its purpose is orientation: describe current repository structure, boundaries, runtime flow, tests, CI, risks, and open questions. It should describe what exists today, not become a project backlog.

RigorLoop needs a simple, durable follow-up ownership rule.

## Goals

- Define where deferred and future work should be recorded.
- Keep `project-map` focused on orientation, not backlog ownership.
- Make `docs/workflows.md` the user-facing guide for follow-up placement.
- Keep current-change follow-ups near the active change.
- Provide an optional central register for follow-ups not owned by an active change.
- Keep skills concise and avoid repeated follow-up rules in every skill.
- Make future work discoverable without broad searches across many authoritative documents.
- Preserve RigorLoop's artifact-owns-truth model.

## Non-goals

- Do not create a new workflow stage.
- Do not create a new skill unless later evidence proves one is needed.
- Do not turn `project-map` into a backlog.
- Do not require every minor note to become a tracked follow-up.
- Do not force all deferred items into one global file when an active plan or change artifact already owns them.
- Do not replace proposals, plans, learn sessions, or release reports.
- Do not change workflow stage order.
- Do not add heavy semantic validation in the first slice.

## Vision fit

fits the current vision

This proposal strengthens RigorLoop's goal of making AI-assisted software work reconstructable from durable artifacts while keeping skills concise and reducing token-wasting searches.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Decide who owns deferred or future work | in scope | Recommended direction, Follow-up ownership rules |
| Decide whether `project-map` owns deferred work | in scope; answer is no | Problem, Recommended direction, Project-map risks |
| Keep rules simple and concise | in scope | Goals, Skill guidance |
| Avoid broad searches for follow-ups | in scope | Goals, `docs/workflows.md` responsibility |
| Generate a proposal artifact | in scope | This document |

## Context

The current `project-map` skill creates architecture visibility for humans and agents. Its required sections include repository layout, runtime flow, data flow, test map, CI/release map, risk areas, and open questions. It says the map should describe what exists today and should not invent future design.

The current public adapter migration proposal contains many future or deferred items: adapter artifact migration, example relocation, artifact-location guidance, token-cost measurement, and release packaging work. Those items belong to proposals, plans, release reports, or follow-up registers, not to `project-map`.

The project artifact-location guide proposal already establishes the right pattern: `docs/workflows.md` should tell users and agents where artifacts go, while exact shapes live in specs and examples live in `docs/examples`.

## Options considered

### Option 1: Let `project-map` own future work

Advantages:

- One document can collect risks and open questions.
- It is useful for repository orientation.

Disadvantages:

- It blurs current-state mapping with future backlog tracking.
- It makes architecture orientation stale and noisy.
- It encourages agents to scan the project map for work items.
- It conflicts with the `project-map` skill's purpose: describe what exists today.

### Option 2: Keep follow-ups only inside active plans and change artifacts

Advantages:

- Follow-ups stay near the work that created them.
- No new artifact is needed.
- It is good for current-change scope.

Disadvantages:

- Cross-change or long-term follow-ups can be hard to find.
- Once a plan closes, future work may become buried.
- Maintainers may need one project-level view.

### Option 3: Use action-owning artifacts plus an optional central follow-up register

Advantages:

- Current-change follow-ups stay in active change artifacts.
- Long-term unowned follow-ups have one durable home.
- `project-map` remains an orientation artifact.
- `docs/workflows.md` can explain the routing.
- Future agents avoid broad searches.

Disadvantages:

- It adds one possible document: `docs/follow-ups.md`.
- It requires guidance to avoid duplicating every small follow-up.

## Recommended direction

Choose Option 3.

Use this ownership model:

```text
Current change follow-up:
  active plan, change.yaml, review-resolution, explain-change, or release report

Future standalone initiative:
  proposal

Future implementation sequence:
  plan

Repeated durable lesson:
  learn

Repository orientation risk:
  project-map risk/open question only

Unowned cross-change future work:
  docs/follow-ups.md, only when the register creation and admission rules are met

Placement guidance:
  docs/workflows.md

Routing owner:
  workflow skill
```

## Follow-up ownership rules

### Current-change follow-ups

If a follow-up belongs to the active change, record it in the current change's durable artifacts.

Preferred locations:

```text
docs/plans/<plan>.md
docs/changes/<change-id>/change.yaml
docs/changes/<change-id>/review-resolution.md
docs/changes/<change-id>/explain-change.md
docs/reports/<area>/
```

Examples:

```text
A review finding needs later validation:
  review-resolution.md

A release report discovers future adapter packaging work:
  release report + docs/follow-ups.md only if the item is accepted, cross-change, and otherwise unowned

A plan defers a milestone:
  active plan

An explain-change notes a future cleanup:
  explain-change + docs/follow-ups.md only if it must survive beyond the change and is otherwise unowned
```

### Proposal-worthy follow-ups

If the future work changes product direction, workflow policy, release packaging, public skill behavior, architecture, or source-of-truth ownership, create or schedule a proposal.

Examples:

```text
Public adapter archive migration
Downstream status settlement extension
Single authored source steady-state cleanup
```

### Learn-worthy follow-ups

If the follow-up comes from a repeated failure, incident, or durable lesson, use `learn`.

Do not use `learn` as a general backlog.

Learn sessions may identify follow-ups, but they do not own general backlog execution.

Use this routing:

```text
Learn follow-up tied to the current change:
  active plan or change artifacts

Learn follow-up requiring new policy, workflow, skill, or architecture direction:
  proposal

Learn follow-up that is real, cross-change, and unowned:
  docs/follow-ups.md, with the learn session as the source
```

### Project-map risks

`project-map` may record:

```text
risk areas
unclear ownership
missing tests
architecture open questions
```

But it should not own execution follow-ups.

A project-map risk becomes a follow-up only when it has a concrete action, owner stage, and source rationale.

Otherwise it remains an orientation note in `project-map`.

If a project-map risk meets that threshold, route it to:

```text
proposal
plan
docs/follow-ups.md entry
```

### Cross-change follow-ups

If the follow-up is real, cross-change, not owned by an active change, and meets the register admission criteria, record it in:

```text
docs/follow-ups.md
```

This file is a lightweight project-wide register, not a full backlog system.

## Central register creation rule

`docs/follow-ups.md` is created only when at least one accepted follow-up is real, cross-change, and not already owned by an active plan, change artifact, review-resolution, release report, proposal, or learn session.

If no such item exists, the first implementation slice updates `docs/workflows.md` and skill guidance only. It does not create an empty register.

## Follow-up register admission criteria

A `docs/follow-ups.md` entry is allowed only when all are true:

- the item is not already owned by an active plan, change artifact, review-resolution, release report, proposal, or learn session;
- the item has a durable source artifact or review-visible source;
- the item has an owner stage or owning artifact type;
- the item has a concrete next action;
- the item is expected to matter beyond the current change.

Do not add chat-only, vague, or speculative notes to `docs/follow-ups.md`.

## Proposed `docs/follow-ups.md` shape

```md
# Follow-ups

This file tracks deferred work that is not owned by an active plan, change, review-resolution, release report, or learn session.

Do not use this file for normal active milestone tracking.

## Open follow-ups

| ID | Title | Source | Owner stage | Owner surface | Status | Next action |
|---|---|---|---|---|---|---|
| FU-001 | Publish adapter archives | docs/proposals/... | plan | docs/plans/<planned-path>.md | open | create release packaging plan |

## Closed follow-ups

| ID | Title | Closed by | Notes |
|---|---|---|---|
```

Allowed status values:

```text
open
planned
done
superseded
deferred
blocked
```

Each entry should include:

```text
ID
title
source artifact
owner stage
owner surface
status
next action
```

`Owner surface` may be:

```text
proposal
plan
release report
review-resolution
learn session
specific artifact path
undecided
```

If `Owner surface` is `undecided`, the next action should be to choose the owner, not to implement the work.

## Follow-up status values

- `open`: accepted follow-up exists but is not yet owned by an active plan, proposal, release plan, or other action-owning artifact.
- `planned`: follow-up is now owned by a proposal, plan, release plan, or other action-owning artifact.
- `blocked`: follow-up cannot proceed until a named decision, dependency, or artifact exists.
- `done`: follow-up was completed and links to the closing artifact.
- `superseded`: follow-up was replaced by another artifact or decision.
- `deferred`: follow-up remains valid but is intentionally postponed; it includes a reason and revisit condition.

Closed follow-ups must link to the artifact or decision that closed them.

## `docs/workflows.md` responsibility

Add a concise section:

```md
## Follow-up ownership

Record follow-ups where they can be acted on.

| Follow-up type | Owner |
|---|---|
| Active implementation follow-up | active plan |
| Review finding follow-up | review-resolution.md |
| Change closeout follow-up | explain-change.md or change.yaml |
| Release follow-up | release report or release plan |
| Repeated lesson | learn |
| Architecture risk/open question | project-map risk section |
| Unowned cross-change future work | docs/follow-ups.md, only when register rules are met |
| New direction or policy change | proposal |
```

Add:

```md
`project-map` may identify risks and open questions, but it does not own deferred execution.
```

## `workflow` skill responsibility

Update `workflow` to route follow-ups.

`workflow` should:

```text
- decide where a follow-up belongs;
- create or refresh docs/workflows.md follow-up ownership guidance;
- route proposal-worthy follow-ups to proposal;
- route implementation follow-ups to plan;
- route repeated lessons to learn;
- route unowned cross-change items to docs/follow-ups.md only when the register creation and admission rules are met.
```

`workflow` should not:

```text
- maintain a backlog inside project-map;
- create detailed plans for every follow-up;
- turn every minor note into tracked future work;
- replace proposal, plan, learn, or review-resolution.
```

## Skill guidance

Public skills should use a short shared rule:

```md
Record future work in the artifact that can act on it.

Use:

- active plan for current implementation follow-ups;
- review-resolution for review findings;
- explain-change or change.yaml for change closeout follow-ups;
- release report or release plan for release follow-ups;
- learn for repeated lessons;
- proposal for new direction or policy;
- docs/follow-ups.md only for real cross-change follow-ups that are not already owned by another durable artifact.

Do not use project-map as the follow-up backlog.
```

Do not paste long follow-up tables into every skill.

## Expected behavior changes

Before:

```text
Future work may be scattered across chat, plans, project-map risks, release reports, and proposals.
```

After:

```text
Workflow routes follow-ups to the artifact that owns action.
```

Before:

```text
project-map may be tempting as a general future-work bucket.
```

After:

```text
project-map remains current-state orientation and may only surface risks/open questions.
```

Before:

```text
agents may broad-search many documents to find deferred work.
```

After:

```text
docs/workflows.md explains follow-up ownership and docs/follow-ups.md holds only accepted unowned cross-change items that meet admission criteria.
```

## Architecture impact

No runtime architecture change.

This is a workflow documentation and skill-routing improvement.

Affected surfaces may include:

```text
docs/workflows.md
skills/workflow/SKILL.md
docs/follow-ups.md
skills/project-map/SKILL.md
selected stage skills if shared follow-up wording is added
```

`project-map` may need a small clarification that risks and open questions are orientation notes and do not own deferred execution.

No `templates/shared/` block should be introduced in the first implementation slice. The first slice needs concise wording in only two skills, so a shared block would add abstraction before repetition is proven.

## Testing and verification strategy

Suggested checks:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
git diff --check --
```

If `docs/follow-ups.md` is added, include lightweight validation for the register.

Initial validation should check:

```text
- required headings exist;
- the open table has required columns;
- each open entry has ID, title, source, owner stage, owner surface, status, and next action;
- status is one of the allowed values.
```

Do not add semantic validation in the first slice.

If canonical skills change and generated outputs are still tracked for the release:

```bash
python scripts/build-adapters.py --check
python scripts/validate-adapters.py
```

## Acceptance criteria

- `docs/workflows.md` contains the follow-up ownership table.
- `workflow` contains concise follow-up routing wording.
- `project-map` contains concise "not a backlog" boundary wording.
- No `templates/shared/` block is introduced in the first slice.
- Skill wording does not duplicate the full follow-up ownership table.
- `docs/follow-ups.md` is not created unless at least one accepted unowned cross-change follow-up meets the creation and admission rules.

## Rollout and rollback

Rollout:

```text
M1 - Workflow guidance
  Add follow-up ownership section to docs/workflows.md.
  Update workflow skill to route follow-ups.
  Update project-map skill to say risks/open questions do not own execution.
  Do not introduce a templates/shared block.

M2 - Optional central register, only if needed
  Add docs/follow-ups.md only if at least one accepted unowned cross-change follow-up needs a home.
  Seed only currently accepted/deferred items that are not already owned by active artifacts.
  Add minimal validation for the register.

M3 - Project-map clarification
  Refine project-map guidance if M1's clarification needs follow-up detail.
  Route actionable risks to proposal, plan, learn, or follow-ups.

M4 - Validation and generated output
  Add static skill checks if needed.
  Regenerate public skill/adapters if canonical skills changed.
  Validate.
```

Rollback:

```text
If docs/follow-ups.md creates noise:
  remove the central register
  keep follow-up ownership guidance in docs/workflows.md
  route open items back to their active plans/proposals/reports

If project-map becomes too constrained:
  restore its risk/open-question section
  keep the rule that actionable execution belongs elsewhere
```

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| `docs/follow-ups.md` becomes a dumping ground | Require source, owner stage, owner surface, status, next action, and admission criteria |
| Follow-ups are duplicated across artifacts | Prefer the action-owning artifact; use `docs/follow-ups.md` only when unowned |
| Project-map loses useful risk notes | Keep risk/open-question sections, but route action elsewhere |
| Skills get longer | Use direct concise wording in workflow and project-map only; do not introduce a shared block until repetition is proven |
| Future agents still broad-search | Put the ownership table in `docs/workflows.md` |

## Shared wording decision

The first implementation slice will not introduce a `templates/shared/` block.

The follow-up ownership rule lives in `docs/workflows.md`.

`workflow` and `project-map` receive short, direct wording only.

A shared template may be proposed later only if three or more skills require the same concise operational text and duplication becomes a measured maintenance problem.

## Decision log

| Date | Decision | Reason |
|---|---|---|
| 2026-05-13 | Do not make `project-map` own deferred work. | `project-map` is repository orientation, not backlog ownership. |
| 2026-05-13 | Let `workflow` own follow-up routing guidance. | `workflow` owns routing and the user-facing workflow guide. |
| 2026-05-13 | Use action-owning artifacts first. | Deferred work should live where it can be acted on. |
| 2026-05-13 | Add optional `docs/follow-ups.md` for unowned cross-change work. | Some future items are real but not tied to an active change. |
| 2026-05-13 | Do not create an empty `docs/follow-ups.md`. | The register should exist only when at least one accepted unowned cross-change follow-up needs a home. |
| 2026-05-13 | Require owner surface, status definitions, and minimal validation when the register exists. | A durable register needs enough structure to stay actionable without becoming a heavy backlog system. |
| 2026-05-13 | Do not introduce a `templates/shared/` block in the first slice. | Only `workflow` and `project-map` need wording now; `docs/workflows.md` owns the policy. |

## Next artifacts

```text
proposal-review
spec only if workflow/follow-up ownership needs normative contract
plan
test-spec
implement
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- [Follow-up Ownership and Deferred Work Register spec](../../specs/follow-up-ownership-and-deferred-work-register.md)

## Readiness

Accepted after proposal-review approval and post-review maintainer decision on shared wording. Actual downstream artifacts are recorded in `Follow-on artifacts`.

## Core invariant

```text
Project-map orients.
Workflow routes.
Action-owning artifacts track work.
docs/follow-ups.md holds only unowned cross-change future work.
Do not create an empty docs/follow-ups.md.
No shared template until repetition is proven.
```
