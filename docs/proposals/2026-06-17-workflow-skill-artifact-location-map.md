# Workflow Skill Artifact-Location Map

## Status

accepted

## Problem

The `workflow` skill owns a high-leverage routing contract: it creates or refreshes the project-local workflow guide and routes work through the standard RigorLoop lifecycle. Current guidance already says `docs/workflows.md` tells users where artifacts go, while stage skills own the actual artifact content.

Recent usage exposed that artifact placement questions are still easy to ask and easy to answer inconsistently.

Two examples show the problem:

- A maintainer asked why detailed plans are not generated under `docs/plan/`. The corrected repository-standard answer is that `docs/plan.md` is the global plan index and concrete execution plan bodies live under `docs/plans/YYYY-MM-DD-slug.md`.
- A maintainer asked why proposal review files were not generated under `docs/changes/`. Later workflow-map work moved review files under `docs/changes/<change-id>/reviews/`.

These are not isolated documentation questions. They show that the workflow skill needs to be more deterministic about generating and maintaining `docs/workflows.md`.

There was also a live drift risk between earlier discussion and current repository guidance. `CONSTITUTION.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, and the `plan` skill describe concrete plan bodies under `docs/plans/YYYY-MM-DD-slug.md`. This proposal follows that repository practice as the forward contract and treats `docs/changes/<change-id>/` as the change-local evidence pack for metadata, reviews, review resolution, explain-change, verify, and PR handoff evidence.

The optimization should not make `docs/workflows.md` a vague guide that skills may or may not follow. It should make `docs/workflows.md` the project-local artifact-location map, generated or refreshed by the workflow skill, with explicit ownership boundaries and validation against stage-skill portable defaults.

## Goals

- Optimize the `workflow` skill so it reliably creates and refreshes `docs/workflows.md`.
- Make `docs/workflows.md` the project-local artifact-location map used for workflow-managed artifact placement.
- Keep owning stage skills responsible for artifact content and stage-specific rules.
- Remove placement ambiguity for proposals, specs, test specs, architecture, ADRs, plans, reviews, verification, PR handoff, and learn records.
- Align the workflow skill's default artifact paths with the project-local workflow map.
- Encode `docs/plan.md` as the plan index, `docs/plans/YYYY-MM-DD-slug.md` as the detailed workflow-managed plan body, and `docs/changes/<change-id>/reviews/` as the formal review-record location.
- Define a deterministic artifact registry shape inside `docs/workflows.md`.
- Add validation that detects drift between the workflow skill, `docs/workflows.md`, stage-skill placement sections, and generated adapter output when the workflow skill is packaged.
- Preserve skill-only portability: when a customer project lacks `docs/workflows.md`, stage skills still provide portable defaults and block on ambiguity instead of requiring RigorLoop repository internals.

## Non-goals

- Do not change the lifecycle stage order.
- Do not make the workflow skill author proposals, specs, plans, reviews, schemas, verification reports, or PR handoff content.
- Do not move existing artifacts in this proposal.
- Do not redefine proposal, spec, plan, review, verify, PR, or learn content schemas.
- Do not remove stage-skill portable defaults.
- Do not make `docs/workflows.md` override explicit user paths, current artifact metadata, governing specs, safety constraints, or schema constraints.
- Do not rely on learn sessions as live routing authority.
- Do not introduce a new CLI scaffold in this slice.
- Do not hand-edit generated adapter output.
- Do not migrate existing `docs/plans/*.md` files in the first slice.

## Vision fit

fits the current vision

RigorLoop depends on durable, traceable artifacts. Artifact traceability fails when users or agents cannot answer where an artifact goes, who owns it, or what the next valid stage is. This proposal strengthens the workflow skill as the lifecycle routing and artifact-location authority without changing downstream artifact semantics.

The proposal would be falsified if `docs/workflows.md` and workflow skill defaults disagree, plan placement remains valid in multiple competing locations for the same workflow-managed purpose, review placement remains ambiguous, stage skills infer placement from chat or learn sessions, customer projects become dependent on RigorLoop repository-internal docs, or the workflow guide starts hiding rules that belong in stage skills.

## Context

Accepted artifact-placement work already established a dual-layer model:

```text
workflow skill:
  creates or refreshes docs/workflows.md

docs/workflows.md:
  project-local workflow and artifact-location guide

stage skills:
  create their own artifacts using explicit user paths, active metadata,
  project-local workflow guidance, or portable defaults

specs and schemas:
  define exact artifact shapes and validation rules
```

That model supports project-local customization and customer-project portability, but it now needs stronger synchronization. Current `docs/workflows.md` includes an artifact-location source rank and an artifact-locations table. It also lists detailed plan bodies under `docs/plans/YYYY-MM-DD-slug.md`, which this proposal preserves as the repository-standard plan-body location.

This proposal resolves the plan-placement ambiguity by preserving the repository-standard split: detailed workflow-managed plan bodies use `docs/plans/YYYY-MM-DD-slug.md`; `docs/plan.md` remains the global plan index; `docs/changes/<change-id>/` remains the change-local evidence pack.

## Options Considered

### Option 1: Leave the workflow skill as a narrative router

This is the smallest change and preserves current behavior. It is insufficient because placement ambiguity continues, `docs/workflows.md` can drift from skill defaults, and users keep asking where artifacts go.

### Option 2: Make `docs/workflows.md` the only artifact-location source

This centralizes placement in one place, but it breaks skill-only adopter portability, leaves stage skills underspecified when the guide is absent, and conflicts with installed-skill self-containment.

### Option 3: Put all placement rules only in stage skills

This helps skill-only adopters, but project-specific customization becomes difficult, cross-skill consistency is hard to validate, and changing one path requires many skill edits.

### Option 4: Use dual-layer placement

Stage skills carry portable defaults, the workflow skill generates the project-local `docs/workflows.md` map, and the project-local map customizes placement when present and safe.

This preserves portability, supports customization, keeps workflow paths reviewable in one map, and allows drift validation. The tradeoff is that synchronization checks become necessary.

## Recommended Direction

Choose Option 4.

Optimize the workflow skill as a project-local workflow-map generator and routing gatekeeper, not as a replacement for specialized stage skills.

The governing model should be:

```text
The workflow skill owns the project-local artifact-location map.
The stage skill owns the artifact content.
The project-local map customizes placement.
The stage skill portable default protects skill-only adopters.
```

`docs/workflows.md` should use a predictable structure with at least these sections:

- status and owner metadata;
- source-rank rules;
- lifecycle graph;
- stage obligations;
- artifact-location map;
- review-record placement;
- plan surfaces;
- customization rules;
- migration notes.

The artifact-location map should include one canonical path per artifact type. It should cover proposals, proposal reviews, specs, spec reviews, test specs, architecture, ADRs, plan index, change plan, change metadata, code review, review log, review resolution, explain-change, verify report, PR handoff, and learn sessions.

The workflow skill should document formal lifecycle evidence as change-pack-first, while keeping detailed plan bodies under `docs/plans/`:

```text
For formal workflow-managed lifecycle recording, create or identify
docs/changes/<change-id>/ before recording reviews, change metadata,
review log, review resolution, explain-change, verify, or PR handoff evidence.
```

Isolated manual reviews remain possible. If the user asks for review-only advice and no formal recording is requested, the skill should not create lifecycle artifacts unless explicitly asked.

Artifact placement should use this source rank:

```text
1. explicit user path or explicit change ID
2. existing active artifact metadata
3. existing change metadata, if workflow-managed
4. docs/workflows.md project-local artifact map
5. stage-skill portable default
6. stop and ask or request workflow-map update
```

The forward plan-surface model is:

| Surface | Path | Purpose |
|---|---|---|
| Plan index | `docs/plan.md` | Small global index of active, blocked, and recent work. |
| Plan body | `docs/plans/YYYY-MM-DD-slug.md` | Detailed execution plan for one workflow-managed planned initiative. |
| Change metadata | `docs/changes/<change-id>/change.yaml` | Metadata and validation ledger. |

Existing `docs/plans/*.md` files remain valid plan bodies in this slice. They are not migrated into change packs.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Optimize the `workflow` skill's `docs/workflows.md` generation. | in scope | Goals, Recommended Direction |
| Make `docs/workflows.md` the project-local artifact-location map. | in scope | Goals, Recommended Direction |
| Preserve stage-skill ownership of artifact content. | in scope | Goals, Recommended Direction |
| Remove ambiguity across proposals, specs, plans, reviews, verification, PR, and learn records. | in scope | Goals, Recommended Direction |
| Align workflow skill defaults with the workflow map. | in scope | Goals, Testing and Verification Strategy |
| Encode `docs/plan.md` as plan index and `docs/plans/YYYY-MM-DD-slug.md` as detailed plan body. | in scope | Goals, Recommended Direction, Plan-location Decision |
| Route formal review records under `docs/changes/<change-id>/reviews/`. | in scope | Goals, Recommended Direction |
| Add drift validation across workflow skill, workflow guide, stage skills, and adapters. | in scope | Goals, Testing and Verification Strategy |
| Preserve customer-project portability and stage-skill portable defaults. | in scope | Goals, Non-goals, Recommended Direction |
| Avoid using learn sessions as live placement authority. | in scope | Non-goals, Expected Behavior Changes |
| Avoid moving existing artifacts in this proposal. | in scope | Non-goals, Rollout and Rollback |
| Add a CLI scaffold. | out of scope | Non-goals |

## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| Workflow skill artifact-map generation behavior. | core to this proposal | This is the central direction choice. |
| `docs/workflows.md` structured artifact-location map. | core to this proposal | The proposal changes the project-local map contract. |
| Source-rank and unknown-artifact blocking rules. | core to this proposal | These rules prevent hidden inference. |
| Plan-surface split between `docs/plan.md`, `docs/plans/`, and `docs/changes/<change-id>/` evidence packs. | core to this proposal | The proposal now chooses the repository-standard plan-location contract. |
| Review-record placement under `docs/changes/<change-id>/reviews/`. | first-slice candidate | The proposal preserves the recent change-pack review-recording direction. |
| Workflow/stage-skill drift validation. | first-slice candidate | Dual-layer placement needs deterministic synchronization checks. |
| Generated adapter proof. | same-slice dependency | Public workflow skill packaging should reflect the canonical skill change. |
| Historical artifact migration. | separate proposal | This proposal defines forward behavior; migration has different risk and validation needs. |
| CLI scaffold for creating change packs. | separate proposal | Useful later, but explicitly outside this slice. |

## Expected Behavior Changes

- The workflow skill creates or refreshes `docs/workflows.md` using a stable, reviewable structure.
- `docs/workflows.md` functions as the project-local artifact-location map for workflow-managed artifact placement.
- Stage skills continue to own their artifact content and carry portable defaults for skill-only adopters.
- Formal lifecycle evidence uses a change-pack-first model when the workflow-managed artifact map requires it.
- Unknown artifact types block instead of falling back to inferred paths.
- Placement decisions no longer depend on learn sessions, prior chat, or undocumented repository habit.
- Validation can detect drift between the workflow skill, project workflow map, directly relevant stage-skill placement sections, and generated adapter output.
- Lifecycle stage order and downstream readiness claims remain unchanged.

## Architecture Impact

The change affects workflow-governance surfaces and public skill behavior:

- `skills/workflow/SKILL.md` or the canonical authored workflow skill source;
- `CONSTITUTION.md`, only if a future edit makes its plan-body guidance stale or inconsistent;
- `docs/workflows.md`;
- related stage skills when their portable default placement text directly contradicts the refreshed map;
- validation scripts that inspect skill text, workflow-map structure, and generated adapter output;
- generated adapter release output, through normal generation rather than hand edits.

It does not require a runtime architecture change. The architectural concern is source-of-truth layering: `docs/workflows.md` becomes the project-local placement map, stage skills remain portable content owners, and specs or schemas keep exact artifact shapes.

## Plan-location Decision

Forward workflow-managed detailed plan bodies use:

```text
docs/plans/YYYY-MM-DD-slug.md
```

`docs/plan.md` remains the global plan index.

Existing `docs/plans/*.md` files remain valid plan bodies in this slice and are not migrated into change packs.

`docs/changes/<change-id>/` remains the change-local evidence pack and is not the canonical home for detailed plan bodies. The downstream spec must preserve this repository-standard split and update only directly contradictory placement text.

## Workflow Map Representation

`docs/workflows.md` contains both:

1. a canonical fenced YAML artifact registry for validators;
2. human-readable Markdown tables for users.

The YAML registry is the validator source of truth. The Markdown tables must not contradict it.

Candidate registry shape:

```yaml
artifact_locations:
  proposal:
    owner: proposal
    path: docs/proposals/<change-id>.md
  change_plan:
    owner: plan
    path: docs/plans/YYYY-MM-DD-slug.md
  review_record:
    owner: review-skills
    path: docs/changes/<change-id>/reviews/<stage>-r<n>.md
```

Validators should parse the YAML registry for deterministic checks and verify that the human-readable artifact-location tables agree with the registry.

## Stage-Skill Edit Policy

The first implementation slice should edit stage skills only when their placement text directly contradicts the approved workflow map or source-rank model.

Required first-slice candidates:

- `workflow`;
- `plan`, if its default plan-body path conflicts;
- `proposal-review`, if formal review path text conflicts;
- `spec-review`, if formal review path text conflicts.

Other lifecycle skills should not be bulk-edited for stylistic consistency. They should change in the first slice only when validation or direct inspection finds contradictory placement text.

## Testing and Verification Strategy

The implementation should add deterministic checks, either in existing skill validation, artifact lifecycle validation, or a focused workflow-map validator.

Candidate checks:

| Check ID | What is verified |
|---|---|
| `WFO-001` | The workflow skill has normalized published-skill frontmatter when the skill contract requires it. |
| `WFO-002` | The workflow skill states it creates or refreshes `docs/workflows.md`. |
| `WFO-003` | The workflow skill distinguishes map ownership from artifact-content ownership. |
| `WFO-004` | `docs/workflows.md` contains a structured artifact-location map. |
| `WFO-005` | Each mapped artifact type has exactly one canonical path. |
| `WFO-006` | Plan index and detailed plan body are distinct: `docs/plan.md` and `docs/plans/YYYY-MM-DD-slug.md`. |
| `WFO-007` | Formal review records route under `docs/changes/<change-id>/reviews/`. |
| `WFO-008` | Workflow skill default paths match `docs/workflows.md`. |
| `WFO-009` | Stage skills do not contradict `docs/workflows.md` for default placement. |
| `WFO-010` | Unknown artifact types block instead of using inferred paths. |
| `WFO-011` | Learn sessions are not treated as live placement authority. |
| `WFO-012` | Generated adapters include the updated workflow skill when packaged. |
| `WFO-013` | The Markdown artifact-location table does not contradict the canonical YAML registry. |

Cold-read proof should answer:

- Where does a proposal-review record go?
- Where does a workflow-managed change plan go?
- What is `docs/plan.md` for?

## Acceptance Criteria

| ID | Criterion |
|---|---|
| `AC-WFO-001` | The workflow skill clearly states it creates or refreshes `docs/workflows.md`. |
| `AC-WFO-002` | The workflow skill states that `docs/workflows.md` is the project-local artifact-location map. |
| `AC-WFO-003` | The workflow skill states that owning stage skills still author artifact content. |
| `AC-WFO-004` | `docs/workflows.md` has a structured artifact-location map. |
| `AC-WFO-005` | Every artifact type has exactly one canonical project-local path. |
| `AC-WFO-006` | `docs/plan.md` is documented only as the plan index. |
| `AC-WFO-007` | Detailed workflow-managed plan bodies are documented under `docs/plans/YYYY-MM-DD-slug.md`. |
| `AC-WFO-008` | Formal review records are documented under `docs/changes/<change-id>/reviews/`. |
| `AC-WFO-009` | Workflow skill default paths match the generated `docs/workflows.md`. |
| `AC-WFO-010` | Unknown artifact types block rather than infer a path. |
| `AC-WFO-011` | Customer projects without `docs/workflows.md` can still rely on stage-skill portable defaults or get a clear blocker. |
| `AC-WFO-012` | Validation detects drift between `workflow` skill, `docs/workflows.md`, and key stage-skill placement sections. |
| `AC-WFO-013` | No lifecycle order, artifact content schema, or downstream readiness claim changes. |
| `AC-WFO-014` | The proposal chooses one forward canonical location for workflow-managed change plans. |
| `AC-WFO-015` | The downstream spec preserves the repository-standard `docs/plans/` plan-body contract in `CONSTITUTION.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, and the `plan` skill. |
| `AC-WFO-016` | Existing `docs/plans/*.md` files are not migrated in this slice. |
| `AC-WFO-017` | `docs/workflows.md` has a canonical machine-checkable artifact registry. |
| `AC-WFO-018` | Markdown artifact-location tables do not contradict the canonical registry. |
| `AC-WFO-019` | Only directly contradictory stage-skill placement text is changed in the first slice. |

## Rollout and Rollback

Roll out through the standard lifecycle:

```text
proposal-review
spec
spec-review
test-spec
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

The first implementation slice should update canonical skill and workflow-map sources, then add drift validation. Generated adapters should be refreshed through the repository-owned generation path if the workflow skill ships publicly.

Rollback should revert the workflow skill and `docs/workflows.md` map changes together. If validation has already shipped, rollback should either remove the new checks or update fixtures so checks continue to match the restored artifact-location contract.

Historical artifact migration is intentionally not part of this rollout. Existing `docs/plans/*.md` files already live at the canonical plan-body location and do not move.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Over-centralizing placement in `docs/workflows.md` weakens installed skill self-containment. | Keep stage-skill portable defaults and source-rank fallback. |
| Workflow skill becomes too large. | Use a compact structured template for `docs/workflows.md`; keep exact schemas and validation details in specs and validators. |
| A future implementation accidentally reintroduces `docs/changes/<change-id>/plan.md` as the plan-body location. | Validation checks reject stale plan-body placement text that contradicts the repository-standard `docs/plans/` contract. |
| Path changes break existing artifacts. | Define forward behavior in this proposal; handle historical migration separately. |
| Validators overfit prose wording. | Validate stable headings, tables, artifact types, and paths rather than paragraphs. |
| Customer projects want different layouts. | Support explicit workflow-map customization, but require customization to be recorded in `docs/workflows.md`. |
| Learn sessions contradict current rules. | Treat learn sessions as rationale and history only; live routing belongs in `docs/workflows.md`, specs, schemas, or stage skills. |

## Open Questions

None blocking before spec.

Settled answers from proposal review:

- `docs/workflows.md` uses both a canonical fenced YAML artifact registry and human-readable Markdown tables.
- Formal workflow-managed recording requires a change pack. If a change ID is explicit or already present in metadata, create or refresh `docs/changes/<change-id>/`; if no change ID exists, stop and request one or route to the stage that creates it.
- Existing `docs/plans/*.md` files remain valid plan bodies in this slice and are not migrated.
- Stage skills are edited in the first slice only when their placement text directly contradicts the approved workflow map or source-rank model.
- `docs/workflows.md` is generated-or-refreshed tracked documentation. It is maintained by the workflow skill but remains a reviewable repository edit, not disposable generated output.
- This proposal adopts `docs/plans/YYYY-MM-DD-slug.md` for detailed workflow-managed plan bodies and does not require changing `CONSTITUTION.md` away from its current plan-body contract.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-06-17 | Propose optimizing the workflow skill as a project-local artifact-map generator. | Placement confusion shows the map should be explicit and maintained. | Leave workflow skill as a narrative router. |
| 2026-06-17 | Preserve stage-skill portable defaults. | Skill-only adopters may not have `docs/workflows.md`. | Make workflow guide the only source. |
| 2026-06-18 | Adopt `docs/plans/YYYY-MM-DD-slug.md` as the canonical detailed plan-body location. | The repository's existing `CONSTITUTION.md`, workflow guide, workflow spec, and plan skill treat `docs/plans/` as best-practice plan-body placement, and the owner explicitly required preserving that practice. | Move detailed plan bodies into `docs/changes/<change-id>/plan.md`. |
| 2026-06-17 | Add drift validation as part of the recommended direction. | Dual-layer placement can drift unless checked. | Manual review only. |
| 2026-06-17 | Use a canonical YAML registry plus synchronized Markdown tables in `docs/workflows.md`. | Validators need deterministic structure and users need a readable guide. | Markdown-only or YAML-only workflow-map representation. |
| 2026-06-17 | Edit only directly contradictory stage-skill placement text in the first slice. | This keeps the change bounded while closing real drift. | Bulk-edit all lifecycle skills for stylistic consistency. |

## Next Artifacts

```text
spec-review
test-spec
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

The downstream spec should encode the settled plan-location decision and define the validation contract for the workflow map.

## Follow-on Artifacts

- proposal-review R1: [docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r1.md](../changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r1.md)
- proposal-review R2: [docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r2.md](../changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r2.md)
- spec: [specs/workflow-skill-artifact-location-map.md](../../specs/workflow-skill-artifact-location-map.md)

## Readiness

Accepted after proposal-review R2. Downstream spec drafted at `specs/workflow-skill-artifact-location-map.md`.
