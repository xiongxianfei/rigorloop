# Workflow Guide Skeleton Asset and Source-of-Truth Alignment

## Status

accepted

## Problem

The `workflow` skill is responsible for creating or refreshing a project-local workflow guide at `docs/workflows.md`.
That guide is the project-local artifact-location map and should answer where artifacts go, how workflow stages route, which skill owns each artifact, and how project-local placement overrides portable skill defaults.

The current `workflow` skill says it creates or refreshes `docs/workflows.md`, but the skill directory does not ship a copy-and-fill skeleton for that guide.
The existing workflow artifact-location map spec already expects `docs/workflows.md` to contain a registry, source-rank rules, placement tables, and ambiguity handling.

This leaves a source-of-truth gap:

```text
workflow skill:
  owns creation/refresh behavior

docs/workflows.md:
  should have a stable structure

current packaged skill:
  has no skeleton to copy
```

Agents may recreate the workflow guide inconsistently, omit required sections, duplicate long placement guidance across stage skills, or produce a project-local workflow map that drifts from the approved registry contract.

## Goals

- Add a packaged workflow-guide skeleton asset to the `workflow` skill.
- Make `docs/workflows.md` creation consistent in customer projects.
- Keep the guide structure stable, reviewable, and validator-friendly.
- Preserve the source-of-truth layering: specs own normative requirements; `workflow` owns guide creation and refresh behavior; `docs/workflows.md` owns project-local routing and artifact placement; stage skills own artifact content and portable defaults.
- Avoid duplicated long artifact-placement guidance across stage skills.
- Add a `Resource map` entry in `skills/workflow/SKILL.md`.
- Add validation proving the skeleton exists, is packaged, and stays aligned with workflow-map requirements.
- Preserve customer-project portability.
- Avoid turning the skeleton into hidden policy.

## Non-goals

- Do not change the standard workflow order.
- Do not change artifact content schemas.
- Do not make the workflow skill author proposals, specs, plans, reviews, ADRs, verification reports, or PR handoff content.
- Do not remove stage-skill portable defaults.
- Do not make `docs/workflows.md` the only source for skill-only adopters.
- Do not move existing artifacts or migrate historical workflow guides.
- Do not duplicate the full workflow-map contract in every stage skill.
- Do not hide lifecycle transition policy inside the skeleton asset.
- Do not hand-edit generated adapter output.
- Do not create a CLI scaffold in this proposal.

## Vision fit

fits the current vision

RigorLoop exists to make AI-assisted software work traceable, resumable, and reviewable in Git.
Artifact traceability fails when a user or agent cannot determine where an artifact goes, which skill owns it, what the next valid stage is, or what should block downstream progress.

This proposal strengthens the existing traceability model by giving the workflow skill a packaged structure for the project-local workflow guide it already owns.

## Context

The accepted workflow-map model already treats `docs/workflows.md` as the project-local workflow and artifact-location guide.
The workflow skill creates or refreshes that guide, while stage skills create their own artifacts using explicit user paths, active metadata, project-local workflow guidance, or portable defaults.

A learn session on `2026-07-05` observed that the workflow guide creation responsibility lacks a packaged skeleton asset.
It recommended a three-layer contract:

| Layer | Owns | Must not own |
| --- | --- | --- |
| Workflow spec / workflow-map spec | Normative requirements, required registry fields, validation semantics, source-rank contract | Project-specific values for every customer repo |
| `skills/workflow/SKILL.md` | When to create or refresh `docs/workflows.md`, conflict handling, blocking behavior, resource map | Full copied guide structure or hidden artifact schema |
| `assets/workflows-skeleton.md` | Headings, registry shape, table scaffolds, placeholders, short fill hints | Lifecycle policy, stage semantics, review rules, enum policy |
| Project `docs/workflows.md` | Project-local artifact placement, source rank, routing tables, concise operational guidance | Stage artifact content schemas |
| Stage skills | Artifact content, portable defaults, stage-specific stop conditions | Long project-local path tables |

The existing project workflow guide also states that learn sessions are historical rationale, not live routing authority, unless the current rule is promoted into a guide, approved spec, schema, or owning skill.
This proposal is the owner-seeking step that promotes the learn observation into a reviewable direction.

## Options Considered

### Option 1: Keep the workflow skill without a skeleton

This has no implementation cost and keeps current prose short.
It leaves agents to recreate `docs/workflows.md` structure from memory, making customer guides incomplete or inconsistent and giving validators no packaged template to check.

Rejected.

### Option 2: Put the full guide structure inline in `SKILL.md`

This keeps everything visible in one file.
It would make `SKILL.md` long and noisy, mix policy with structure, and increase drift risk.

Rejected.

### Option 3: Add a workflow skeleton asset with hidden policy

This would be easy for agents to copy.
It would also hide lifecycle semantics in an asset, create a second policy owner, and make review and validation harder.

Rejected.

### Option 4: Add a structural skeleton asset and keep rules in specs and skill text

This matches the existing asset-design pattern, gives agents a stable structure, keeps source-of-truth layering clean, preserves stage-skill portability, and supports deterministic validation.

Recommended.

## Recommended Direction

Add one new structural asset:

```text
skills/workflow/assets/workflows-skeleton.md
```

Map it from `skills/workflow/SKILL.md` with a `COPY` entry in a `Resource map` section.
The asset should be a copy-and-fill structure for creating a new project-local `docs/workflows.md` or fully rewriting a stale workflow guide.

The skeleton should include metadata comments and stable sections for:

- status;
- source rank;
- lifecycle graph;
- stage obligations;
- `artifact_locations` YAML registry;
- human-readable artifact location table;
- review record placement;
- plan surfaces;
- guide ownership;
- customization rules;
- migration notes;
- validation notes.

The skeleton should stay structural.
Normative lifecycle policy, stage semantics, review approval rules, and artifact content schemas should remain in approved specs, schemas, `docs/workflows.md`, and owning stage skills.

## Expected Behavior Changes

- When adopting RigorLoop in a customer project, the workflow skill can create `docs/workflows.md` from a packaged skeleton instead of agent memory.
- Workflow guides have stable sections and tables.
- Stage skills can rely on concise project-guide lookup wording instead of duplicating long placement tables.
- Validators can check skeleton presence and registry/table alignment.
- Generated adapters include the skeleton asset when they package the workflow skill.
- The workflow skill remains an orchestrator and map creator, not the author of every lifecycle artifact.
- Existing `docs/workflows.md` files are not automatically migrated.

## Architecture Impact

| Surface | Expected impact |
| --- | --- |
| `skills/workflow/SKILL.md` | Add a `Resource map` and concise skeleton usage rules. |
| `skills/workflow/assets/workflows-skeleton.md` | New packaged structural asset. |
| Workflow-map spec | Amend with skeleton contract expectations. |
| Skill validation | Check resource map and asset presence. |
| Workflow-map validation | Continue owning registry/table consistency, with extension or composition for skeleton checks. |
| Guide-system validation | Compose workflow-map validation rather than duplicating registry checks. |
| Stage skills | No broad rewrite; only remove directly conflicting duplicated placement prose. |
| Generated skill mirror and adapters | Include the asset when the workflow skill is packaged. |
| Historical `docs/workflows.md` | No automatic migration. |

## Testing and Verification Strategy

Add deterministic validation for the skeleton and its packaging boundary:

| Check | Proof target |
| --- | --- |
| Skeleton existence | `skills/workflow/assets/workflows-skeleton.md` exists. |
| Resource map | `skills/workflow/SKILL.md` maps the skeleton with `COPY`. |
| Metadata | Skeleton includes required metadata comments. |
| Required sections | Skeleton includes source rank, lifecycle graph, artifact registry, artifact table, review placement, plan surfaces, customization, migration, and validation notes. |
| Registry and table coverage | Workflow-map validation checks required artifact types and registry/table consistency. |
| Validator layering | Guide-system validation composes workflow-map validation instead of duplicating the registry contract. |
| Stage-skill boundary | Directly affected stage skills retain concise lookup wording and portable defaults. |
| Generated output | Build and adapter validation prove the asset is included when packaged. |

Candidate negative fixtures should cover missing skeleton, missing resource-map entry, missing required skeleton sections, mismatched registry/table entries, and packaged output that omits the asset.

## Rollout and Rollback

Rollout should proceed through the standard workflow after proposal review:

```text
spec or spec amendment
spec-review
architecture assessment
plan
plan-review
test-spec
test-spec-review when required
implementation
code-review
explain-change
verify
pr
```

The downstream implementation should update canonical authored sources first, then prove generated outputs through repository-owned build and validation scripts.
It should not hand-edit generated adapter output.

Rollback should remove the resource-map entry and skeleton asset together, remove or disable skeleton-specific validation, and restore prior workflow skill wording.
Workflow-map registry validation should remain if it is independently valid.
Historical `docs/workflows.md` files should not be rewritten as part of rollback.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Skeleton becomes hidden policy | Keep lifecycle rules in specs and concise skill instructions; keep the asset structural. |
| Workflow skill becomes too large | Move full structure to the asset and keep `SKILL.md` concise. |
| Stage skills duplicate the full guide | Keep stage skills to lookup rules and portable defaults. |
| Validator duplicates registry ownership | Compose or extend the workflow-map validator rather than cloning registry checks. |
| Customer projects need customization | Include customization and migration sections in the skeleton. |
| Historical guides drift | Make the change forward-looking; require explicit refresh or migration for existing guides. |
| Asset packaging fails | Add generated skill and adapter packaging checks. |

## Open Questions

None.

The authoring questions raised during proposal drafting are resolved in the decision log.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-05 | Propose a workflow-guide skeleton asset. | The workflow skill owns a substantial structured artifact and needs a copy-and-fill starting point. | Agents recreate guide ad hoc. |
| 2026-07-05 | Keep the skeleton structural. | Avoid hidden lifecycle policy in assets. | Put full workflow policy in the asset. |
| 2026-07-05 | Keep stage skills concise. | Detailed project-local placement belongs in `docs/workflows.md`; stage skills own content and portable defaults. | Duplicate path tables across skills. |
| 2026-07-05 | Validate skeleton/package parity. | Packaged public skills must include referenced assets. | Trust packaging implicitly. |
| 2026-07-05 | Do not migrate existing guides automatically. | Historical migration is separate from adding a skeleton. | Reflow all existing workflow guides. |
| 2026-07-05 | Name the asset `assets/workflows-skeleton.md`. | The name mirrors the target artifact `docs/workflows.md`. | `assets/workflow-guide-skeleton.md`. |
| 2026-07-05 | Include both YAML registry and Markdown table structure. | YAML is the validator-oriented registry shape; Markdown is the human-readable projection. | YAML-only or Markdown-only skeleton. |
| 2026-07-05 | Amend the existing workflow artifact-location map spec if it can own the skeleton contract cleanly. | The existing spec already owns `docs/workflows.md` structure and registry behavior. | Create a new spec by default. |

## Initial Intent Preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Add a packaged workflow-guide skeleton asset to the workflow skill. | in scope | Goals, Recommended Direction |
| Make `docs/workflows.md` creation consistent and validator-friendly. | in scope | Problem, Expected Behavior Changes, Testing and Verification Strategy |
| Preserve source-of-truth layering between specs, workflow skill, guide, and stage skills. | in scope | Goals, Context, Recommended Direction |
| Avoid duplicated long artifact-placement guidance across stage skills. | in scope | Goals, Non-goals, Risks and Mitigations |
| Add a `Resource map` entry in `skills/workflow/SKILL.md`. | in scope | Goals, Recommended Direction, Testing and Verification Strategy |
| Add validation for skeleton existence, packaging, and registry alignment. | in scope | Goals, Testing and Verification Strategy |
| Preserve customer-project portability. | in scope | Goals, Expected Behavior Changes, Risks and Mitigations |
| Avoid hidden lifecycle policy in the skeleton. | in scope | Non-goals, Recommended Direction, Risks and Mitigations |
| Do not change workflow order, schemas, or historical guide placement. | in scope | Non-goals, Expected Behavior Changes, Rollout and Rollback |
| Include detailed downstream implementation milestones. | rejected option | Rollout and Rollback |

## Scope Budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Workflow-map spec amendment | core to this proposal | The skeleton contract needs an approved normative owner. |
| Workflow skill resource map and concise guide-creation behavior | core to this proposal | The workflow skill owns guide creation and refresh. |
| Skeleton asset content | core to this proposal | This is the primary change proposed. |
| Validator checks for skeleton/resource-map presence | core to this proposal | The proposal requires deterministic proof that the asset exists and is referenced. |
| Registry/table consistency validation | same-slice dependency | The skeleton must stay aligned with the existing workflow-map contract. |
| Generated skill and adapter packaging proof | same-slice dependency | Referenced assets must ship when the workflow skill is packaged. |
| Broad stage-skill rewrites | out of scope | Stage skills should only change when directly contradictory. |
| Historical `docs/workflows.md` migration | separate proposal | Migration policy is distinct from adding a forward-looking skeleton. |
| CLI scaffold for guide creation | out of scope | The proposal intentionally adds a packaged asset, not a new CLI. |

## Next Artifacts

```text
proposal-review
spec or spec amendment: workflow guide skeleton contract
spec-review
architecture assessment
plan
plan-review
test-spec
test-spec-review, if required by current workflow
implementation
code-review
explain-change
verify
pr
```

## Follow-on Artifacts

- Proposal review R1: [proposal-review-r1](../changes/2026-07-05-workflow-guide-skeleton-asset/reviews/proposal-review-r1.md)
- Review log: [review-log](../changes/2026-07-05-workflow-guide-skeleton-asset/review-log.md)
- Review closeout: [review-resolution](../changes/2026-07-05-workflow-guide-skeleton-asset/review-resolution.md)

## Readiness

Accepted after clean recorded `proposal-review`.
Ready for a focused spec amendment to `specs/workflow-skill-artifact-location-map.md` before downstream implementation planning.
