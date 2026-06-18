# RigorLoop Guide System Optimization and Source-of-Truth Alignment

## Status

accepted

## Problem

RigorLoop now has many guide-like surfaces:

- `README.md`
- `VISION.md`
- `CONSTITUTION.md`
- `AGENTS.md`
- `docs/workflows.md`
- `docs/project-map.md`
- `docs/plan.md`
- `docs/changes/<change-id>/`
- `docs/learn/sessions/`
- `skills/*/SKILL.md`
- package README surfaces
- release docs

These artifacts are individually useful, but the overall guide system is becoming harder to reason about. A contributor or adopter can reasonably ask:

- Where do I start?
- Which guide is authoritative?
- Where does this artifact go?
- Which skill owns this artifact?
- Which file tells me current work state?
- Which file explains durable workflow policy?
- Which guide applies in a customer project?

Recent workflow and placement work already shows the problem. The `workflow` skill says it creates or refreshes the project-local workflow guide and artifact-location map, while the owning stage skill still authors artifact content. Plan-placement work clarified that `docs/plan.md` is the global plan index, while the exact detailed plan-body location remains owned by the workflow artifact-location contract. Proposal-review placement work clarified that formal review records belong under `docs/changes/<change-id>/reviews/`, and that live placement rules belong in `docs/workflows.md`, not only in a learn session.

The underlying issue is that RigorLoop has strong artifacts, but its guides need a clearer system: which guide answers which question, what each guide may own, and how drift is detected.

This is not only documentation polish. Guides affect routing, onboarding, skill use, contribution, artifact placement, and verification. A stale or ambiguous guide can cause artifacts to be written to the wrong place or users to rely on the wrong source of truth.

## Goals

- Define a coherent guide system for RigorLoop.
- Clarify which guide answers which user question.
- Separate orientation guides from normative contracts.
- Make `README.md` a landing page, not a full manual.
- Make `docs/workflows.md` the project-local workflow and artifact-location map.
- Make `docs/project-map.md` the repository orientation map.
- Keep `VISION.md` and `CONSTITUTION.md` as durable source-of-truth artifacts.
- Keep `docs/plan.md` as a bounded live-work index, not a long-form guide.
- Keep stage skills self-contained for skill-only adopters.
- Add a guide ownership matrix and drift checks.
- Prevent guide duplication from becoming a second source of truth.
- Preserve RigorLoop's artifact-first workflow and lifecycle semantics.

## Non-goals

- Do not rewrite every guide in one slice.
- Do not change lifecycle stage order.
- Do not change artifact content schemas.
- Do not change skill behavior except guide references and source-of-truth wording where needed.
- Do not make `README.md` the authoritative source for workflow rules.
- Do not make `docs/workflows.md` the only source for skill-only adopters.
- Do not make learn sessions live routing authority.
- Do not migrate historical artifacts in this proposal.
- Do not add a new CLI scaffold.
- Do not hand-edit generated adapter output.
- Do not treat guide cleanup as verification, branch readiness, or PR readiness.

## Vision fit

fits the current vision

RigorLoop's value is traceable, resumable, reviewable AI-assisted work. That depends on guides that make the artifact system understandable without making the guide layer itself a new source of ambiguity.

This proposal is falsified if README becomes longer but less useful, `docs/workflows.md` and skill defaults disagree, users still cannot tell which guide owns which question, guides restate specs and drift from them, learn sessions are used as live routing authority, a customer project cannot use installed skills without RigorLoop repo internals, or validators cannot detect guide/source-of-truth drift.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize RigorLoop guides. | in scope | Goals, Recommended Direction |
| Make guides easier to use. | in scope | Guide taxonomy, README contract |
| Clarify artifact placement. | in scope | Workflow guide contract |
| Keep workflow skill responsible for `docs/workflows.md`. | in scope | Guide taxonomy, Recommended Direction |
| Avoid guide/source-of-truth drift. | in scope | Testing and Verification Strategy |
| Preserve skill-only portability. | in scope | Stage-skill guide boundary |
| Avoid broad behavior change. | in scope | Non-goals |
| Avoid historical migration. | out of scope | Non-goals, Follow-on Artifacts |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Guide taxonomy | core to this proposal | The system needs a clear map of guide types. |
| Guide ownership matrix | core to this proposal | Every guide needs an owner and allowed content boundary. |
| README guide index | first-slice candidate | High-value onboarding improvement. |
| `docs/workflows.md` guide contract | core to this proposal | Artifact placement and workflow routing depend on it. |
| `docs/project-map.md` guide contract | first-slice candidate | Useful for repository orientation. |
| `docs/plan.md` bounded index wording | first-slice candidate | Prevents the plan index from becoming a guide or manual. |
| Stage-skill guide references | same-slice dependency | Skills must not contradict guide source-rank when touched by the first slice. |
| Drift validation | core to this proposal | Dual guide surfaces need checks. |
| Full guide rewrite | separate implementation slice | Too broad for the first pass. |
| Historical artifact migration | separate proposal | Different risk and validation surface. |
| Docs website | deferable follow-up | Larger adoption surface, not required first. |
| Generated guide tooling | deferable follow-up | Useful only after the guide structure is stable. |

## Context

The current workflow guidance already contains the right high-level boundary:

- the `workflow` skill creates or refreshes `docs/workflows.md`;
- the guide tells users where artifacts go;
- the owning stage skill still authors its own artifact content.

That boundary should become the core guide-system principle.

Recent placement work also shows why the guide system needs stronger structure. Plan placement confusion was resolved by distinguishing `docs/plan.md` as the index from detailed plan-body placement, with the exact plan-body path left to the workflow artifact-location contract. Proposal-review placement confusion was resolved by routing formal review files under `docs/changes/<change-id>/reviews/`.

The guide system should make those answers obvious without requiring users to inspect learn sessions or remember previous conversations.

## Options Considered

### Option 1: Do nothing

Pros:

- No implementation risk.

Cons:

- Guide drift continues.
- Users keep asking placement and routing questions.
- Learn sessions remain too tempting as hidden guide authority.

Rejected.

### Option 2: Optimize README only

Pros:

- Improves first-contact adoption.

Cons:

- Does not fix workflow-map ambiguity.
- Does not clarify guide ownership.
- Does not prevent drift.

Rejected as insufficient.

### Option 3: Optimize `docs/workflows.md` only

Pros:

- Fixes the artifact-routing surface.

Cons:

- README, project map, plan index, and skill-guide boundaries remain unclear.
- Does not create full guide-system ownership.

Rejected as incomplete.

### Option 4: Define guide taxonomy, ownership, and drift checks

Pros:

- Clarifies the whole guide system.
- Keeps each guide focused.
- Preserves the source-of-truth hierarchy.
- Makes future guide changes testable.

Cons:

- Requires multiple guide surfaces to be reviewed.
- Needs careful first-slice boundary.

Recommended.

## Relationship to Workflow Artifact-Location Map Work

This proposal optimizes the guide system broadly. It does not independently settle exact artifact path policy when that policy is owned by the workflow artifact-location map contract.

The workflow artifact-location map contract owns exact artifact registry semantics, including plan-body path, review-record path, PR handoff path, and registry validation. This guide-system proposal owns guide taxonomy, guide ownership, guide indexes, and source-of-truth alignment across README, `VISION.md`, `CONSTITUTION.md`, `docs/workflows.md`, `docs/project-map.md`, `docs/plan.md`, learn sessions, and stage skills.

If both changes proceed, the workflow artifact-location map spec should settle the exact `docs/workflows.md` registry contract first, or be incorporated as the workflow-guide subsection of the guide-system spec.

## Recommended Direction

Use a source-ranked guide system:

1. `VISION.md` owns durable why.
2. `CONSTITUTION.md` owns governance and source-of-truth policy.
3. `docs/workflows.md` owns project-local workflow and artifact-location map.
4. `docs/project-map.md` owns repository orientation.
5. `docs/plan.md` owns live work index.
6. Stage skills own stage behavior and portable defaults.
7. Specs and schemas own exact artifact contracts.
8. Learn sessions explain history, not live routing.

The governing rule is:

> Guides should orient and route. Specs, schemas, and skills should own enforceable contracts. Validators should detect drift.

### Guide taxonomy

| Guide class | Example | Purpose | Should contain | Should not contain |
| --- | --- | --- | --- | --- |
| Landing guide | `README.md` | First-contact orientation | What it is, why it matters, quick start, links | Full workflow contract |
| Vision guide | `VISION.md` | Durable project why | Values, product direction, core principles | Operational routing details |
| Governance guide | `CONSTITUTION.md` | Source-of-truth and rules | Authority, lifecycle governance, safety boundaries | Detailed per-stage templates |
| Workflow guide | `docs/workflows.md` | Project-local lifecycle and artifact map | Stage order, artifact paths, source rank | Full artifact schemas |
| Project map | `docs/project-map.md` | Repo orientation | Components, boundaries, key files, ownership | Workflow policy |
| Plan index | `docs/plan.md` | Current live work index | Active, blocked, and recent done status | Detailed milestone journal |
| Change pack | `docs/changes/<change-id>/` | Per-change evidence | Metadata, reviews, plan evidence, validation, rationale | Global guide content |
| Learn sessions | `docs/learn/sessions/` | Historical learning evidence | Observations, classification, routing rationale | Live routing authority |
| Skill guide | `skills/*/SKILL.md` | Installed operating contract | When to use, how to execute, output expectations | Repo-internal-only assumptions |
| Release guide | `docs/releases/*` | Release evidence and process | Publish evidence, smoke results, recovery notes | General workflow tutorial |

### Guide ownership matrix

Add or maintain a guide ownership matrix in `docs/workflows.md`, because it already owns project-local workflow guidance.

Suggested matrix:

| Question | Primary guide | Secondary source | Owner |
| --- | --- | --- | --- |
| Why does this project exist? | `VISION.md` | README summary | `vision` / `proposal` |
| What rules govern source of truth? | `CONSTITUTION.md` | `docs/workflows.md` summary | `constitution` |
| Where does an artifact go? | `docs/workflows.md` | stage skill portable default | `workflow` |
| What does this repo contain? | `docs/project-map.md` | README links | `project-map` |
| What work is active? | `docs/plan.md` | active plan body or change pack | `plan` |
| What happened in one change? | `docs/changes/<change-id>/` | `docs/plan.md` index | relevant stage skills |
| How do I perform one stage? | `skills/<stage>/SKILL.md` | workflow guide | owning stage skill |
| Why did a rule change? | learn session or proposal | spec or workflow guide | `learn` / `proposal` |

### README optimization

`README.md` should answer:

- What is RigorLoop?
- Who is it for?
- Why should I care?
- How do I start?
- Where do I go next?

README should remain a landing guide, not the full workflow manual. It should include a compact "Where to go next" guide index that links to `VISION.md`, `CONSTITUTION.md`, `docs/workflows.md`, `docs/project-map.md`, `docs/plan.md`, and installed stage skills where relevant.

### `docs/workflows.md` optimization

`docs/workflows.md` should identify itself as the project-local workflow guide and artifact-location map.

It owns stage order summaries, stage obligations summaries, artifact location map, source-rank rules, guide ownership matrix, customization rules, and migration notes.

It should not own proposal schema, spec schema, review finding schema, validation internals, or full stage instructions.

Recommended top-level structure:

- Status
- Source rank
- Guide ownership
- Lifecycle graph
- Stage obligations
- Artifact location map
- Review record placement
- Plan surfaces
- Customization rules
- Migration notes

### `docs/project-map.md` optimization

`docs/project-map.md` should answer:

- What is in this repository?
- Where are the important components?
- What boundaries matter?
- Where should an agent look first?

It should not answer where every lifecycle artifact goes, what the stage order is, or the current milestone state. Those belong in `docs/workflows.md` and `docs/plan.md`.

Recommended sections are overview, major directories, key commands, runtime boundaries, generated artifacts, validation surfaces, ownership or maintainers, and known external dependencies.

### `docs/plan.md` optimization

`docs/plan.md` should remain a bounded live-work index. It should answer what is active, what is blocked, what is next, and what recently completed.

It should not contain full milestone journals, long review summaries, detailed implementation plans, or complete historical transcripts.

### Plan-location boundary

This proposal does not independently settle the canonical detailed change-plan path.

The guide-system work should align with the approved workflow artifact-location contract. If the workflow-map contract adopts `docs/changes/<change-id>/plan.md` for new workflow-managed change plans, this proposal updates guides to reflect that. If the contract preserves `docs/plans/YYYY-MM-DD-slug.md`, this proposal preserves that path.

The implementation should not leave `docs/plans/*.md` and `docs/changes/<change-id>/plan.md` as competing canonical locations for the same workflow-managed plan role.

### Learn-session optimization

Learn sessions should explain historical observations and lessons. They should not be treated as live guide rules.

If a learn session changes how users should route artifacts, update the owning guide or contract. Do not leave the rule only in learn.

| Observation | Correct live owner |
| --- | --- |
| Plan placement rule | `docs/workflows.md` / workflow spec |
| Review record placement rule | `docs/workflows.md` / review placement spec |
| Repeated mistake pattern | `docs/learn/topics/*` or relevant skill |
| Validation blind spot | spec, test spec, or validator |

### Stage-skill guide boundary

Stage skills are also guides. They are the installed operating manuals for each stage.

Each stage skill should include when to use, what it owns, artifact placement portable default, source-rank behavior, output expectations, stop conditions, and claim boundaries.

Stage skills should not duplicate the full project-local workflow guide.

Recommended shared wording:

```md
Use the project-local workflow guide when present. If absent, use this skill's
portable default. Block when placement remains ambiguous.
```

This preserves customer-project portability while allowing `docs/workflows.md` customization.

## Expected Behavior Changes

The proposed change is expected to make guide routing more predictable without changing workflow stage order, artifact schemas, lifecycle status semantics, validation semantics, or PR readiness claims.

After implementation, a new contributor should be able to use README for orientation, `docs/workflows.md` for workflow and artifact placement, `docs/project-map.md` for repository structure, `docs/plan.md` for current work, stage skills for stage execution, and learn sessions for historical rationale.

Skill-only adopters should continue to have portable stage defaults when a project-local workflow guide is absent.

## Architecture Impact

The change affects documentation architecture and validation surfaces rather than runtime architecture.

Expected touched areas:

- public and contributor-facing guides: `README.md`, `docs/workflows.md`, `docs/project-map.md`, and `docs/plan.md`;
- canonical skill sources under `skills/`, especially `workflow`, only where guide-generation or placement wording contradicts the guide system;
- validation scripts and fixtures if guide drift checks are added;
- downstream spec and test-spec artifacts that define the guide ownership and drift-check contract.

No deployed runtime, storage model, adapter command surface, lifecycle stage order, artifact schema, or generated adapter output change is proposed for the first slice.

## Validation Ownership Boundary

First-slice guide checks span multiple artifact classes. Use a focused guide-system validator or guide-validation module for cross-guide consistency, and keep skill-only checks in `validate-skills.py`.

Cross-guide checks include README guide index links, workflow-guide registry presence, project-map scope, plan-index boundary, learn-session non-authority, and guide/source-of-truth drift.

Do not put README, project-map, plan-index, learn-session, and constitution checks into the skill validator unless they directly check packaged skill content.

Recommended ownership split:

| Check type | Owner |
| --- | --- |
| Skill frontmatter, resource maps, portable-default wording | `validate-skills.py` |
| `docs/workflows.md` registry/table consistency | workflow-map validator or guide validator |
| README guide index links | guide validator or link checker |
| `docs/project-map.md` scope boundary | guide validator |
| `docs/plan.md` bounded-index shape | plan-index validator or guide validator |
| Learn sessions not live authority | guide validator / content fixture |
| Generated adapter inclusion | adapter validation |

## Testing and Verification Strategy

Use phased guide-system validation.

Phase 1 checks:

| Check ID | What is verified |
| --- | --- |
| `GUIDE-001` | `README.md` links to primary guides without duplicating their contracts. |
| `GUIDE-002` | `docs/workflows.md` includes guide ownership and artifact-location sections. |
| `GUIDE-003` | `docs/workflows.md` distinguishes guide ownership from stage-skill content ownership. |
| `GUIDE-004` | `docs/project-map.md` does not own workflow stage order. |
| `GUIDE-005` | `docs/plan.md` remains a bounded index. |
| `GUIDE-006` | Learn sessions are not cited as live routing authority. |
| `GUIDE-007` | Stage-skill placement text does not contradict `docs/workflows.md`. |
| `GUIDE-008` | Workflow skill default paths match `docs/workflows.md`. |

Phase 2 checks:

| Check ID | What is verified |
| --- | --- |
| `GUIDE-009` | Guide links are valid. |
| `GUIDE-010` | README Quick Start does not drift from package CLI contract. |
| `GUIDE-011` | `VISION.md` and README positioning do not conflict. |
| `GUIDE-012` | `CONSTITUTION.md` and `docs/workflows.md` do not conflict on artifact placement. |
| `GUIDE-013` | Generated adapters include updated skill guide content if affected. |

First-slice proof should also include:

- behavior-preservation evidence under `docs/changes/<change-id>/behavior-preservation.md`;
- cold-read evidence under `docs/changes/<change-id>/guide-cold-read.md`;
- targeted validation through the repository-owned explicit-path CI wrapper for touched guides, skills, scripts, fixtures, specs, and change-local artifacts.

## Rollout and Rollback

Rollout:

1. Accept this proposal.
2. Write or amend the spec for guide ownership and workflow-map contract.
3. Write the test spec for guide drift checks.
4. Update `workflow` skill guide-generation instructions where needed.
5. Update `docs/workflows.md` structure.
6. Add README guide index.
7. Add or update project-map and plan-index boundary text only where needed.
8. Add drift validation.
9. Record cold-read proof.
10. Code-review and verify.

Rollback:

- Revert guide wording if it creates source-of-truth confusion.
- Revert validation checks if they overfit prose.
- Keep the guide ownership matrix only if it remains accurate.
- Do not move historical artifacts during rollback.
- Do not modify stage skill behavior unless the rollback also restores matching guide paths.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Guides become too long. | Use guide index and concise ownership tables. |
| README duplicates contracts. | README links out instead of restating rules. |
| `docs/workflows.md` becomes too rigid. | Allow project-local customization, but require it to be recorded. |
| Stage skills and workflow map drift. | Add validation. |
| Learn sessions become hidden authority. | State that live rules should be promoted to owning guides or specs. |
| Customer projects lack the full guide set. | Stage skills keep portable defaults and block on ambiguity. |
| Validators overfit prose. | Validate stable headings, links, artifact types, and paths. |

## Acceptance Criteria

| ID | Criterion |
| --- | --- |
| `AC-GUIDE-001` | The guide taxonomy defines each major guide surface and its purpose. |
| `AC-GUIDE-002` | `README.md` includes a guide index or equivalent "where to go next" section. |
| `AC-GUIDE-003` | `docs/workflows.md` identifies itself as the project-local workflow and artifact-location map. |
| `AC-GUIDE-004` | `docs/workflows.md` includes guide ownership or source-rank guidance. |
| `AC-GUIDE-005` | `docs/project-map.md` is scoped to repository orientation, not workflow policy. |
| `AC-GUIDE-006` | `docs/plan.md` remains the live plan index, not a detailed plan body. |
| `AC-GUIDE-007` | Learn sessions are not treated as live routing authority. |
| `AC-GUIDE-008` | Stage-skill portable defaults remain available for skill-only adopters. |
| `AC-GUIDE-009` | Drift checks detect contradiction between workflow map and stage-skill placement text. |
| `AC-GUIDE-010` | No lifecycle order, artifact schema, validation semantics, or readiness claim changes. |
| `AC-GUIDE-011` | Cold-read proof shows a new contributor can find the right guide for common questions. |
| `AC-GUIDE-012` | The proposal declares its relationship to the workflow artifact-location map contract. |
| `AC-GUIDE-013` | The proposal does not leave `docs/plans/*.md` and `docs/changes/<change-id>/plan.md` as competing canonical detailed plan locations. |
| `AC-GUIDE-014` | The proposal defines which validator owns cross-guide drift checks. |
| `AC-GUIDE-015` | `validate-skills.py` is not expanded to own non-skill guide checks unless those checks directly concern packaged skill content. |
| `AC-GUIDE-016` | If `docs/workflows.md` uses both YAML and Markdown tables, validation treats one representation as canonical and checks the other for consistency. |
| `AC-GUIDE-017` | Historical guide inconsistencies do not trigger artifact migration in this slice. |
| `AC-GUIDE-REG-001` | `docs/workflows.md` has a canonical machine-checkable registry when drift validation is in scope. |
| `AC-GUIDE-REG-002` | Markdown guide tables do not contradict the canonical registry. |
| `AC-GUIDE-SKILL-001` | Only directly contradictory stage-skill placement text is changed in the first slice. |
| `AC-GUIDE-SKILL-002` | Stage-skill portable defaults remain available when no project-local workflow guide exists. |
| `AC-GUIDE-VAL-001` | The proposal identifies which validator owns cross-guide consistency checks. |
| `AC-GUIDE-VAL-002` | `validate-skills.py` is not expanded to own README, project-map, plan-index, learn-session, or constitution checks unless those checks directly concern packaged skill content. |
| `AC-GUIDE-MIG-001` | Existing inconsistencies are recorded as baseline drift, not automatically migrated. |
| `AC-GUIDE-MIG-002` | Historical artifact or guide migration is out of scope for the first slice unless separately approved. |

## Behavior-Preservation Proof Target

Create `docs/changes/<change-id>/behavior-preservation.md` during implementation.

Required matrix:

| Surface | Baseline | New proof | Preservation |
| --- | --- | --- | --- |
| README | Landing guide plus deep links | Guide index added | strengthened |
| `VISION.md` | Durable why | Unchanged or linked | preserved |
| `CONSTITUTION.md` | Governance | No conflicting guide claim | preserved |
| `docs/workflows.md` | Workflow guide | Structured guide ownership and artifact map | strengthened |
| `docs/project-map.md` | Repo orientation | Boundary clarified | strengthened |
| `docs/plan.md` | Live index | Index-only boundary preserved | preserved |
| Stage skills | Portable defaults | No contradiction with workflow map | preserved |
| Learn sessions | Historical record | Not live routing authority | clarified |

## Cold-Read Proof Target

Create `docs/changes/<change-id>/guide-cold-read.md` during implementation.

Ask a reviewer to answer using only the guide system:

1. Where do I start?
2. Where does a proposal go?
3. Where does a formal review record go?
4. What is `docs/plan.md` for?
5. Where do I find the detailed plan for one workflow-managed change?
6. Which guide explains repository structure?
7. Which guide explains governance?
8. Which file is live routing authority?
9. Which files are historical rationale only?

Pass condition:

The reviewer can answer without prior chat context or learn-session archaeology.

## Open Questions

The proposal-review open questions are resolved as follows.

### Dedicated guide index

Do not add `docs/guides.md` in the first slice.

Use README for first-contact guide navigation and `docs/workflows.md` for project-local guide ownership and source-rank rules.

Add `docs/guides.md` only if the guide index grows beyond what README and `docs/workflows.md` can carry without becoming noisy.

### Workflow guide registry

When drift validation is in scope, `docs/workflows.md` includes a canonical fenced YAML registry plus human-readable Markdown projections.

The YAML registry is the validator source of truth. Markdown tables are reader projections and must not contradict the YAML registry.

Example:

```yaml
artifact_locations:
  proposal:
    owner: proposal
    path: docs/proposals/YYYY-MM-DD-slug.md
  change_plan:
    owner: plan
    path: docs/changes/<change-id>/plan.md
  proposal_review:
    owner: proposal-review
    path: docs/changes/<change-id>/reviews/proposal-review-r<n>.md
```

This example is illustrative and does not settle the plan-location dependency by itself.

### Stage-skill edits

Edit stage skills in this slice only when their placement text directly contradicts the approved workflow guide, source-rank model, or artifact-location registry.

Do not bulk-edit lifecycle skills for style, symmetry, or wording cleanup alone.

Stage skills must continue to carry portable defaults for customer projects that do not have `docs/workflows.md`.

Likely first-slice candidates are `workflow`; `plan` if plan placement text conflicts; `proposal-review` and `spec-review` if formal review placement conflicts; and `code-review`, `verify`, or `pr` only if their evidence paths conflict.

### Validation ownership

Use `validate-skills.py` only for skill-file checks.

Use a dedicated guide-system validator, or an artifact-lifecycle guide-system mode, for cross-guide checks such as README guide index links, workflow-guide registry consistency, project-map scope, plan-index boundary, learn-session non-authority, and guide/source-of-truth drift.

Do not place non-skill guide checks in `validate-skills.py` unless they directly inspect packaged skill content.

### Baseline drift and migration

Existing guide inconsistencies are recorded as baseline drift.

This proposal does not migrate historical artifacts and does not relocate existing guide or change artifacts.

Forward changes must align with the approved guide system. Historical migration requires a separate proposal or plan with preservation proof, rollback behavior, and validation.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-18 | Treat guides as a system, not isolated files. | Placement and routing questions cross guide boundaries. | README-only cleanup. |
| 2026-06-18 | Keep README as landing guide. | First-contact users need orientation, not full contracts. | Full README manual. |
| 2026-06-18 | Keep `docs/workflows.md` as workflow map. | It is the right owner for artifact placement and routing. | Stage-only path rules. |
| 2026-06-18 | Keep stage-skill portable defaults. | Skill-only adopters may not have the project guide. | Workflow-guide-only routing. |
| 2026-06-18 | Add drift validation. | Dual-layer guide systems drift without checks. | Manual review only. |
| 2026-06-18 | Do not settle detailed plan-body path in this proposal. | That exact path belongs to the workflow artifact-location map contract. | Competing plan locations in guide-system proposal. |
| 2026-06-18 | Use split validation ownership for guide checks. | Cross-guide checks span non-skill artifacts and should not over-expand `validate-skills.py`. | Put all guide checks in skill validation. |
| 2026-06-18 | Do not add `docs/guides.md` in the first slice. | A new guide before ownership is stable risks creating another drift surface. | Dedicated guide index now. |
| 2026-06-18 | Use a canonical YAML registry with Markdown projections when drift validation is in scope. | Deterministic checks need a machine-checkable source, while readers still need tables. | Markdown-only registry; YAML-only guide. |
| 2026-06-18 | Edit stage skills only for direct contradiction in the first slice. | Portable stage defaults should remain stable and the change should avoid broad style churn. | Broad stage-skill wording pass. |
| 2026-06-18 | Treat existing guide inconsistencies as baseline drift instead of automatic migration triggers. | Historical migration has different risk and proof requirements. | Incidental migration during guide alignment. |

## Next Artifacts

- proposal-review
- spec: RigorLoop guide system and source-of-truth alignment
- spec-review
- test-spec
- plan
- plan-review
- implementation
- code-review
- explain-change
- verify
- pr

A spec is recommended because this proposal defines guide ownership and source-of-truth hierarchy across multiple durable artifacts.

## Follow-on Artifacts

- Proposal review: `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/proposal-review-r1.md`
- Spec: `specs/guide-system-source-of-truth-alignment.md`

## Readiness

Accepted after proposal-review. Ready for spec authoring and spec-review.

The remaining key dependency before spec is the plan-location relationship with the workflow artifact-location map work. Downstream work should not leave `docs/plans/*.md` and `docs/changes/<change-id>/plan.md` as competing canonical locations for the same workflow-managed plan role.

Core invariant:

Each guide should answer one kind of question well.

README orients. `VISION.md` explains why. `CONSTITUTION.md` governs. `docs/workflows.md` routes and maps artifacts. `docs/project-map.md` orients to the repository. `docs/plan.md` shows live work. Stage skills tell the agent how to do one stage. Learn sessions explain history, not live routing.

The guide system is optimized when a new user can find the right answer without chat history, duplicated contracts, or hidden source-of-truth drift.
