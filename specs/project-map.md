# Project Map Skill Contract

## Status

approved

## Related proposal

- [Evidence-Bound and Incremental `project-map` Skill](../docs/proposals/2026-06-23-evidence-bound-incremental-project-map.md)

## Review evidence

- [Spec-review R1](../docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/spec-review-r1.md)

## Goal and context

This spec defines the contract for the `project-map` skill as a current-state repository orientation tool. A project map helps humans and agents understand what exists in a repository, where important boundaries are, how runtime and data flows are currently evidenced, where tests and CI live, and what is unknown.

The `project-map` skill is not an architecture-design skill, backlog, plan, validation gate, or replacement for direct source inspection. Its job is to describe current repository reality with cited evidence, visible inference, bounded freshness, and explicit gaps.

This spec is specific to `project-map` behavior. Generic published-skill metadata, resource-map, generated-output, and adapter-parity rules remain owned by `specs/skill-contract.md`.

## Glossary

- `project map`: A repository orientation artifact, normally `docs/project-map.md` or `docs/project-map/<area>.md`, produced or refreshed by the `project-map` skill.
- `root map`: The repository-level project map that remains the entry point when area maps exist.
- `area map`: A project map for a durable subsystem, package group, service, application, data platform, infrastructure subsystem, ownership area, or domain.
- `map status`: The freshness status recorded in a project map: `current`, `partial`, or `stale`.
- `observed`: A claim supported by inspected repository evidence.
- `inferred`: A reasonable conclusion not directly declared by inspected source-of-truth evidence.
- `unknown`: A conclusion the inspected evidence cannot safely support.
- `material claim`: A current-state claim a downstream agent could use to choose a module, trust a boundary, select tests, assess runtime or data flow, or decide whether a map is safe to rely on.
- `configured command`: A command found in a manifest, workflow, script, or documented configuration.
- `executed command`: A command actually run during the mapping session with its result recorded.
- `correction note`: A refresh-result note that records a prior map claim was wrong at its recorded baseline, not merely stale because repository state later changed.
- `current-state evidence`: Source, runtime configuration, build/package manifests, schemas, tests, CI workflows, current-state documentation, or generated output with a known canonical source.
- `intent artifact`: A proposal, spec, architecture plan, ADR, or execution plan that may describe desired or planned behavior but does not prove current implementation.

## Examples first

### Example E1: root map records current repository state

Given no suitable repository-level project map exists
When `project-map` creates a root map
Then the map records metadata including scope, baseline, last-reviewed date, coverage, exclusions, parent map, known gaps, and map status
And the map includes all required structural sections
And material current-state claims cite repository paths.

### Example E2: area map is registered from the root map

Given a repository has a durable subsystem whose root-map section would exceed roughly one screen of content
When `project-map` creates an area map for that subsystem
Then the area map records `Parent map`
And the root map links the area map in an area-map registration table
And the root and area maps identify any overlap and avoid contradictory detailed descriptions.

### Example E3: intent artifacts do not prove current behavior

Given an accepted proposal describes a future package boundary
And the current source does not implement that boundary
When `project-map` describes the repository
Then it describes the current source as current state
And it may cite the proposal only as planned or expected state
And it records the discrepancy as a risk or open question rather than silently reconciling the two.

### Example E4: commands are separated by evidence

Given a package manifest configures `npm test`
And the mapping session does not run `npm test`
When `project-map` writes the test map
Then it records `npm test` as a configured command
And it does not claim the command passed, works, or was executed.

### Example E5: dirty working tree baseline is auditable

Given Git is available
And the working tree has uncommitted changes in inspected files
When `project-map` creates or refreshes a map
Then the map records the baseline as `<sha>+dirty`
And it lists the inspected uncommitted paths.

### Example E6: prior map was wrong, not stale

Given an existing map claimed that `src/server.ts` registered all routes
And a refresh finds that this was false at the previous map baseline
When the refreshed map corrects the route-flow section
Then the refresh result includes a correction note naming the affected section, the corrected claim, and the evidence path
And the map status remains one of `current`, `partial`, or `stale`.

## Requirements

### Skill role and claim boundaries

R1. The `project-map` skill MUST describe current repository orientation and MUST NOT design future architecture, approve future architecture, claim implementation readiness, claim review approval, claim validation success, claim branch readiness, claim PR readiness, or claim final lifecycle closeout.

R2. The `project-map` skill MUST preserve customer-project operation by using project-local guidance when present and portable defaults when safe, and it MUST NOT require RigorLoop repository-internal files in customer projects.

R3. The normalized `project-map` skill MUST include frontmatter `version`, `schema-version`, a portable routing `description`, and `argument-hint`.

R4. The normalized `project-map` skill MUST include a workflow-role block or the approved equivalent required by `specs/skill-contract.md`.

R5. If the selected workflow-role stage label is not already allowed by the governing skill contract, implementation MUST either reuse an approved equivalent label or amend the governing skill contract before relying on a new label.

### Operating modes and result output

R6. The skill MUST classify each invocation as `create`, `refresh`, `area`, or `audit` before broad repository reading.

R7. A `create` invocation MUST create a root map or approved area map only when no suitable map exists for the requested scope.

R8. A `refresh` invocation MUST update affected map sections and metadata when relevant repository state has changed.

R9. An `area` invocation MUST create or update an area map only for a durable repository boundary.

R10. An `audit` invocation MUST report whether a map is current, partial, stale, incomplete, contradictory, or otherwise unsafe to rely on, and MUST NOT rewrite map artifacts unless the user requested edits.

R11. The skill output MUST include a result block that reports skill, status, mode, map scope, artifacts changed, freshness result, correction note, open blockers, and immediate next stage.

### Artifact placement

R12. The portable root-map path MUST be `docs/project-map.md`.

R13. The portable area-map path pattern MUST be `docs/project-map/<area>.md`.

R14. Artifact placement MUST use this lookup order unless higher-priority project guidance conflicts: explicit user path, current artifact metadata or active workflow context, `docs/workflows.md` artifact map, portable default, then block on unresolved ambiguity.

R15. `project-map` MUST own project-map content, while workflow routing and project-local placement policy remain owned by workflow guidance.

### Map metadata and freshness

R16. Every root or area map MUST begin with a `Map metadata` section.

R17. `Map metadata` MUST record map status, scope, baseline, last-reviewed date, coverage, exclusions, parent map, and known gaps.

R18. Map status MUST use only `current`, `partial`, or `stale`.

R19. A map MUST NOT claim `current` merely because the skill successfully produced or refreshed the document.

R20. A `current` map status MUST mean relevant cited surfaces were inspected and no known material gap remains.

R21. A `partial` map status MUST mean the scope is intentionally bounded or important evidence was unavailable.

R22. A `stale` map status MUST mean a cited or relied-on surface is known to have materially changed.

R23. When Git is available, a map baseline MUST include a commit SHA or ref and the last-reviewed date.

R24. When Git is available and inspected files include uncommitted changes, the baseline MUST record `<sha>+dirty` and list the inspected uncommitted paths.

R25. When Git is unavailable, the baseline MUST record the last-reviewed date and a clear evidence baseline, such as inspected archive, workspace, or supplied path set.

R26. Refresh triggers MUST include changes to top-level or package boundaries, runtime entry points, public module interfaces, service-to-service calls, storage models, schemas, migrations, build/package manifests, test layout or commands, CI/release/deployment/infrastructure configuration, generated-source ownership, ownership boundaries, external integrations, and files cited by the map in a way that changes the map conclusion.

R27. Unrelated repository changes MUST NOT automatically make every map stale.

R28. If refresh discovers a previous map claim was wrong at its recorded baseline, the refresh result MUST include a correction note that identifies the affected section, corrected claim, and evidence path.

R29. Correction notes MUST NOT introduce a fourth first-slice map status.

### Evidence and source ranking

R30. The skill MUST distinguish `observed`, `inferred`, and `unknown` evidence classes.

R31. An observed claim MUST cite inspected repository evidence.

R32. An inferred claim MUST be visibly labeled as inference when the conclusion is not directly declared by inspected source-of-truth evidence.

R33. An unknown MUST be recorded under `Open questions` rather than guessed.

R34. Material current-state claims MUST cite at least one repository path.

R35. Directory names alone MUST NOT be treated as sufficient evidence for a material claim when file content could change the conclusion.

R36. Material-claim guidance MUST include examples that distinguish material claims from incidental statements.

R37. A repository-wide architecture pattern MUST be described as an observed architecture rule only when an explicit project rule states it or multiple independent examples consistently demonstrate it.

R38. A single example MUST be described as an observed instance rather than a repository-wide rule.

R39. For current-state claims, the skill MUST prefer evidence in this order: executable source and runtime configuration; build/package manifests and schemas; tests and CI workflows; explicit current-state project documentation; generated output with a known canonical source; directory and file names alone.

R40. Intent artifacts MUST NOT be treated as proof that intended behavior exists in current implementation.

R41. When intent artifacts conflict with implementation, the map MUST describe implementation as current state, cite the intent artifact only as planned or expected state, and record the discrepancy as a risk or open question.

### Commands and runtime evidence

R42. The skill MUST distinguish configured commands from executed commands.

R43. The map MUST NOT state that a configured command works, passes, or was executed unless it was actually run during the mapping session.

R44. Executed commands MUST be recorded with their exit code in the map's evidence trail or equivalent evidence section.

R45. Read-only inspection commands such as `git log`, `ls`, test discovery commands, `--dry-run`, and `--help` MAY be run when useful for orientation.

R46. Commands that mutate state, hit the network, or run the actual test or build suite MUST require user go-ahead before execution.

R47. Runtime and data-flow statements MUST identify whether the flow was statically traced, demonstrated by tests, observed through execution, or partially inferred.

R48. The skill MUST NOT imply runtime observation when only static source inspection occurred.

### Root and area maps

R49. When any area map exists, the root map MUST remain the repository-level entry point.

R50. The root map MUST include repository-wide overview, major boundaries, major entry points, shared test and CI surfaces, external boundaries, links to area maps, and scope/freshness summary for each area map.

R51. Every area map MUST be linked from the root map.

R52. The root-map area registration MUST use a stable Markdown table with columns for area, map, scope, baseline, freshness, and known gaps.

R53. An area map MUST name its parent map.

R54. Area maps MUST be based on durable repository boundaries, not only on the fact that one current feature touches a directory.

R55. The skill MUST NOT create an area map until the root-map section for that area would exceed roughly one screen of content, unless the area has its own deploy, release, ownership, package, domain, or data lifecycle.

R56. When two maps overlap, each map MUST name the overlap, one map MUST own the detailed description, and the other map SHOULD link rather than duplicate.

R57. Contradictions between overlapping maps MUST block a clean refresh result.

### Required map structure and packaged skeleton

R58. Root and area maps MUST include these structural sections: `Map metadata`, `Purpose and scope`, `System overview`, `Repository layout`, `Runtime flow`, `Data flow`, `External boundaries`, `Test map`, `CI and release map`, `Architecture rules observed`, `Risk areas`, and `Open questions`.

R59. Root maps SHOULD include `Area maps` when area maps exist.

R60. A required section with no applicable observed content MUST say `Not observed in the mapped scope.` and include a short rationale.

R61. The `project-map` skill MUST ship a packaged skeleton asset at `skills/project-map/assets/project-map-skeleton.md`.

R62. The `project-map` skill MUST include a `Resource map` entry that uses `COPY` for `assets/project-map-skeleton.md` when creating a new root or area project map.

R63. The skeleton asset MAY contain headings, metadata fields, table headers, placeholders, and short fill instructions.

R64. The skeleton asset MUST NOT own evidence-ranking rules, inference policy, refresh triggers, future-design prohibitions, handoff rules, or claim boundaries.

R65. Produced maps MUST NOT contain unfilled skeleton placeholders.

### Diagrams

R66. Mermaid diagrams MAY be used only when they clarify runtime flow, data flow, module/service boundaries, deployment boundaries, or external integrations.

R67. Every diagram node MUST correspond to an observed repository component or an explicitly marked external actor.

R68. Diagrams MUST cite supporting files for material nodes or edges.

R69. Inferred diagram edges MUST be labeled as inferred.

R70. Diagrams MUST NOT include decorative layers or present planned components as deployed.

R71. Detailed area diagrams SHOULD live in the owning area map rather than the root map.

### Downstream reliance and handoff

R72. Downstream skills MAY use a current map to locate likely modules and entry points, find tests and CI, identify known boundaries, decide which source files need direct inspection, and recognize known gaps.

R73. Downstream skills MUST inspect source directly when the relevant map is stale or partial, the change crosses an unreviewed area, map evidence conflicts with current code, architecture or security decisions depend on exact behavior, cited paths no longer exist, or the relevant claim is inferred or unknown.

R74. The skill MUST recommend a next stage from `explore`, `proposal`, `architecture`, `workflow`, or `none` based on the map result.

R75. The skill MUST NOT automatically start a downstream stage during an isolated invocation.

R76. Risks and open questions recorded by `project-map` MUST NOT become execution commitments automatically.

R77. Actionable follow-up work MUST be routed through the appropriate owner surface, such as proposal, plan, learn, review resolution, release evidence, or `docs/follow-ups.md`, according to project workflow guidance.

### Validation and rollout scope

R78. The first implementation slice MUST validate the skill contract, skeleton asset, generated adapter inclusion, and a small representative output set.

R79. The first implementation slice MUST NOT require a full project-map fixture suite before concrete drift evidence exists.

R80. A dedicated project-map artifact validator MUST NOT be added in the first slice unless concrete structural drift has already appeared in two or more produced maps.

R81. Generated adapters MUST include the revised `project-map` skill and skeleton asset.

R82. Existing project maps MUST NOT be automatically migrated by this change.

R83. Behavior-preservation evidence MUST cover the orientation-only role, current-state focus, eleven-section structure, material path citations, observation/inference split, narrow-area support, risk routing, handoff behavior, and customer-project mode.

R84. Cold-read proof MUST include at least a small repository, a monorepo or multi-service fixture, and an intentionally stale map, unless the plan explicitly defers one with rationale accepted before implementation.

## Inputs and outputs

Inputs:

- User orientation request, area request, refresh request, or audit request.
- Project-local guidance such as `AGENTS.md`, `CONSTITUTION.md`, `docs/workflows.md`, `docs/project-map.md`, specs, ADRs, README files, build manifests, package manifests, schemas, tests, CI workflows, deployment files, infrastructure files, source files, and generated output with known canonical sources.
- Existing root or area maps when present.

Outputs:

- Created, refreshed, or audited project-map artifact.
- Result block with mode, status, map scope, artifacts changed, freshness result, correction note, blockers, and next stage.
- For formal repository work, validation evidence and change-local artifacts required by the active workflow stage.

## State and invariants

- A project map is a living reference, not a source-of-truth override.
- Source code, runtime configuration, schemas, build manifests, tests, and CI remain stronger evidence of current behavior than the map.
- Intent artifacts can describe planned or required behavior but do not prove current implementation.
- Root maps remain the repository-level entry point when area maps exist.
- Area maps provide bounded depth for durable repository boundaries.
- Unknowns remain visible rather than being silently guessed.
- The skeleton asset owns output structure, while `SKILL.md` owns evidence, freshness, source-rank, claim-boundary, and handoff policy.

## Error and boundary behavior

- If artifact placement cannot be resolved by explicit path, metadata, workflow guidance, or portable default, the skill MUST block instead of guessing.
- If required evidence is unavailable, the map MUST use `partial` status or record unknowns rather than claiming current.
- If overlapping maps contradict each other, the skill MUST block a clean refresh result and name the contradiction.
- If a cited path no longer exists, downstream reliance on that claim is unsafe until source inspection or map refresh resolves the gap.
- If a user requests runtime, network, build, or test execution without sufficient safety context, the skill MUST ask for go-ahead before executing those commands.

## Compatibility and migration

- Existing project maps remain valid historical artifacts but do not automatically satisfy the revised contract until refreshed.
- This change does not require automatic migration of existing customer or repository maps.
- The revised skill and skeleton must remain portable to customer projects without requiring RigorLoop repository internals.
- Generated adapter output must be rebuilt from canonical skill source; generated public adapter skill bodies must not be hand-edited.
- If `orientation` is not an accepted workflow-role stage value, the implementation must reuse an approved equivalent or amend the governing skill contract before publishing the new role block.

## Observability

- Produced maps expose their own evidence through metadata, cited paths, evidence labels, configured/executed command distinction, executed command exit codes, known gaps, open questions, and correction notes.
- Reviewers can observe compliance through the map artifact, skeleton asset, skill text, representative output fixtures, behavior-preservation evidence, generated adapter proof, and cold-read proof.
- No telemetry, remote scanning, or external indexing is introduced by this spec.

## Security and privacy

- The skill must not require secrets, credentials, private tokens, or private keys.
- The skill must not commit machine-local paths or host-specific command workarounds unless intentionally part of a reviewed example with rationale.
- Network commands require user go-ahead before execution.
- The skill must not expose RigorLoop maintainer-only paths as customer-project requirements in published skill text.

## Accessibility and UX

No end-user UI is introduced. The map and skeleton are Markdown artifacts. Headings, tables, examples, and result blocks should remain scannable for human reviewers and agents.

## Performance expectations

- The skill should use bounded evidence before broad reads.
- The skill must not require reading every repository file.
- The root map should remain concise and stable across unrelated changes.
- Area maps should be used to avoid unbounded root-map growth when durable boundaries justify the split.
- Validation should target stable metadata, headings, resource maps, generated adapter inclusion, and representative outputs rather than broad natural-language scoring.

## Edge cases

EC1. Git unavailable: the map records date plus evidence baseline instead of SHA.

EC2. Dirty working tree: the map records `<sha>+dirty` and inspected uncommitted paths.

EC3. Existing map has outdated cited source: affected map is stale until refreshed.

EC4. Existing map was wrong at baseline: refresh records a correction note.

EC5. Single-directory feature request: area map is not created unless a durable boundary and split floor are met.

EC6. Directory name suggests ownership but contents contradict it: contents win and the directory-name inference is not written as observed fact.

EC7. Configured test command found but not run: command is recorded as configured only.

EC8. Static source trace only: runtime flow is labeled statically traced or partially inferred, not observed through execution.

EC9. Future spec describes a planned service: map does not present the service as deployed unless current source/config proves it.

EC10. Root and area maps overlap: one map owns detail and the other links.

EC11. Required section has no evidence in scope: section says `Not observed in the mapped scope.` with rationale.

EC12. Produced output still contains skeleton placeholders: output is invalid for representative proof.

## Non-goals

- Do not turn `project-map` into an architecture-design skill.
- Do not propose future module boundaries or implementation changes.
- Do not turn the map into a backlog, plan, or follow-up registry.
- Do not require runtime instrumentation for every map.
- Do not require reading every repository file.
- Do not require every repository to have every map section populated with substantive content.
- Do not add an area map for every feature or directory.
- Do not make `docs/project-map.md` authoritative over source code, build configuration, schemas, or runtime configuration.
- Do not use proposals, plans, or unimplemented specs as proof of current behavior.
- Do not add decorative diagrams.
- Do not duplicate the complete workflow guide in the project map.
- Do not add remote scanning, telemetry, or external indexing.
- Do not hand-edit generated adapter output.
- Do not add automatic dependency graph generation in this slice.
- Do not add runtime tracing in this slice.
- Do not add a dedicated project-map artifact validator before the drift threshold is met.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC-PMAP-001 | `project-map` remains an observation and orientation skill. |
| AC-PMAP-002 | The skill explicitly prohibits presenting future design as current state. |
| AC-PMAP-003 | The skill supports `create`, `refresh`, `area`, and `audit` modes. |
| AC-PMAP-004 | Produced maps include scope, baseline, coverage, last-reviewed date, and known gaps. |
| AC-PMAP-005 | Dirty Git baselines record `<sha>+dirty` and inspected uncommitted paths. |
| AC-PMAP-006 | Important current-state claims cite repository paths. |
| AC-PMAP-007 | Inferences are explicitly distinguishable from observations. |
| AC-PMAP-008 | Unknowns are recorded rather than guessed. |
| AC-PMAP-009 | Root maps register all area maps in a stable Markdown table. |
| AC-PMAP-010 | Area maps are based on durable repository boundaries and the split floor, not one feature request. |
| AC-PMAP-011 | Plans, proposals, and unimplemented specs are not treated as current implementation evidence. |
| AC-PMAP-012 | Configured and executed commands are distinguished. |
| AC-PMAP-013 | Executed commands are recorded with exit codes. |
| AC-PMAP-014 | Stale or partial maps cannot support unqualified downstream reliance. |
| AC-PMAP-015 | Refreshes that correct a previously wrong map section include a correction note. |
| AC-PMAP-016 | The full output skeleton is packaged and mapped with `COPY`. |
| AC-PMAP-017 | The skeleton contains no hidden evidence, routing, or future-design policy. |
| AC-PMAP-018 | Risks and open questions do not become execution commitments automatically. |
| AC-PMAP-019 | Existing project maps are not automatically migrated. |
| AC-PMAP-020 | Generated adapters include the revised skill and skeleton. |
| AC-PMAP-021 | Representative outputs preserve the existing eleven-section coverage and contain no unfilled placeholders. |
| AC-PMAP-022 | The first slice validates contract, skeleton, generated adapter inclusion, and a small representative output set without requiring a full fixture suite. |

## Open questions

None.

## Next artifacts

```text
architecture-review
plan
plan-review
test-spec
implementation
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- Spec-review: [Spec-review R1](../docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/spec-review-r1.md)
- Architecture update: [Canonical system architecture](../docs/architecture/system/architecture.md)

## Readiness

Approved after clean spec-review. Architecture update recorded; ready for `architecture-review`.
