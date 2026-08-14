# Project Map Skill Contract

## Owning change record

`docs/changes/2026-08-14-project-map-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

- [Evidence-Bound and Incremental `project-map` Skill](../docs/proposals/2026-06-23-evidence-bound-incremental-project-map.md)
- [Project-Map Skill Simplification](../docs/proposals/2026-08-14-project-map-skill-simplification.md)

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
- `operation`: One of `create`, `refresh`, or `audit`, selected from the requested action and resolved target state.
- `map scope`: Either `repository` or `area:<slug>`.
- `map coordination context`: Evidence that area-map discovery, registration, parent/child identity, overlap, contradiction, or missing-area handling applies.
- `semantic classification`: One of six operation/scope combinations; it describes behavior rather than loaded resources.
- `procedural assembly`: The resources loaded for an invocation: `PMA0-simple-root-create` or `PMA1-maintenance-or-coordinated`.
- `area-creation transaction`: The identity-bound creation of one area map followed by its exact root registration, with registration as the commit point.
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

### Example E7: create cannot replace an existing map

Given the resolved repository map already exists
When the user requests `create`
Then the operation stops and requires explicit `refresh`
And a complete rewrite remains a refresh strategy.

### Example E8: audit remains read-only

Given an existing area map is audited and a correctable defect is found
When the user requests correction after the audit
Then the audit finishes without mutation
And correction begins a new refresh operation with current target and evidence resolution.

### Example E9: simple root creation omits conditional procedure safely

Given the root target is absent
And the bounded coordination preflight finds no configured area locations, area files, registrations, request-supplied coordination, or active-change references
When the root map is created
Then assembly `PMA0-simple-root-create` loads `SKILL.md` and the skeleton only.

### Example E10: late coordination discovery changes only the assembly

Given root creation begins as `create + repository`
When a known area-map location reveals an existing area map
Then `map_coordination_context` becomes true
And assembly changes to `PMA1-maintenance-or-coordinated` before dependent judgment or writes
And operation and scope remain unchanged.

### Example E11: area creation commits through root registration

Given one valid root map exists and the area target and registration are absent
When area creation writes and validates the area map
And the root identity remains current
Then the exact root registration is written last as the commit point
And both reciprocal identities are validated.

### Example E12: interrupted area creation reconciles exact state only

Given an area file exists without root registration after interruption
When its root, area, path, parent, baseline, and expected registration identities match the original attempt
Then retry may validate the area and complete only the registration
But a mismatched or ambiguous file is not adopted.

## Requirements

### Skill role and claim boundaries

R1. The `project-map` skill MUST describe current repository orientation and MUST NOT design future architecture, approve future architecture, claim implementation readiness, claim review approval, claim validation success, claim branch readiness, claim PR readiness, or claim final lifecycle closeout.

R2. The `project-map` skill MUST preserve customer-project operation by using project-local guidance when present and portable defaults when safe, and it MUST NOT require RigorLoop repository-internal files in customer projects.

R3. The normalized `project-map` skill MUST include frontmatter `version`, `schema-version`, a portable routing `description`, and `argument-hint`.

R4. The normalized `project-map` skill MUST include a workflow-role block or the approved equivalent required by `specs/skill-contract.md`.

R5. If the selected workflow-role stage label is not already allowed by the governing skill contract, implementation MUST either reuse an approved equivalent label or amend the governing skill contract before relying on a new label.

### Operations, scopes, assemblies, and result output

R6. The skill MUST classify operation as exactly `create`, `refresh`, or `audit` and map scope as exactly `repository` or `area:<slug>` before broad repository reading.

R7. `create` MUST be permitted only when exactly one resolved target map is absent, and an existing target MUST stop with an explicit `refresh` requirement.

R8. `refresh` MUST be permitted only when exactly one target map exists and is resolvable, and an absent target MUST stop and route to `create`.

R9. A complete rewrite of an existing map MUST remain a `refresh` strategy and MUST NOT be performed through `create`.

R10. `audit` MUST always be read-only; an absent target MUST produce a `missing-map` finding, and a later correction request MUST begin a separately classified refresh with current target and evidence resolution.

R11. The skill output MUST include a result block that reports skill, status, `Operation`, `Map scope`, artifacts changed, freshness result, correction note, open blockers, and immediate next stage, and new results MUST NOT emit the legacy `Mode` field.

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

### Simplified package and progressive disclosure

R85. The canonical `project-map` package MUST contain `SKILL.md`, `references/map-maintenance-and-area-coordination.md`, and `assets/project-map-skeleton.md`, with no additional result or policy asset introduced by this change.

R86. `SKILL.md` MUST remain self-sufficient for purpose, routing, placement, target resolution, operation and scope classification, coordination preflight, map-status meanings, baseline truthfulness, evidence classes, source ranking, command truthfulness, universal map and reliance invariants, stops, claims, resource triggers, and next-stage behavior.

R87. The conditional reference MUST own detailed refresh-trigger comparison, affected-section selection, correction notes, audit procedure, root registration, parent/child rules, overlap ownership, contradiction and missing-area handling, previous/current baseline comparison, changed-path targeting, and interrupted maintenance or coordination recovery.

R88. The conditional reference MUST NOT redefine universal evidence meanings, source ranking, command authority, map statuses, claim boundaries, stops, downstream ownership, or asset structure.

R89. The skeleton MUST be the sole owner of metadata labels, required section order, root registration table headers, evidence-trail table headers, placeholders, and insertion locations.

R90. `SKILL.md` MUST NOT duplicate the complete required-output or metadata-label inventory owned by the skeleton.

R91. The skeleton MUST remain policy-free and MUST NOT determine evidence adequacy, freshness, operation applicability, coordination context, authority, claims, or handoff.

R92. The `Area maps` section MUST be emitted only for a root map with registered area maps and MUST be omitted for an area map or a root map with no registered areas.

### Coordination preflight and procedural assemblies

R93. Before classifying repository root creation as uncoordinated, the skill MUST inspect project-local workflow guidance for customized paths, the canonical or configured root path, canonical or configured area directories, existing root registrations when present, known area files, request-supplied coordination evidence, and directly referenced project-map paths in active change context when applicable.

R94. The coordination preflight MUST remain bounded to known project-map ownership surfaces and MUST NOT require a broad repository content scan merely to prove absence.

R95. No known coordination evidence MUST select uncoordinated behavior; discovered coordination evidence MUST require the conditional reference; unavailable, conflicting, or ambiguous known surfaces MUST require reference-owned resolution or stop when the reference is unavailable.

R96. `map_coordination_context` MUST be true for every area scope and whenever evidence identifies an existing, proposed, missing, or orphaned area map, root registration, parent/child identity, overlap ownership, or root/area contradiction handling.

R97. The six semantic classifications MUST be the Cartesian set of the three operations and two scope kinds, but procedural loading MUST use only `PMA0-simple-root-create` and `PMA1-maintenance-or-coordinated`.

R98. `PMA0-simple-root-create` MUST apply only to `create + repository + coordination=false` and MUST load `SKILL.md` plus the skeleton when writing.

R99. `PMA1-maintenance-or-coordinated` MUST apply to every refresh, every audit, every area scope, and every root create with coordination and MUST load `SKILL.md` plus the conditional reference and the skeleton when writing.

R100. Late coordination discovery during root creation MUST change the loaded assembly to `PMA1` before dependent judgment or writes without changing operation or scope.

R101. A missing, unreadable, escaped, contradictory, or mixed-version required reference MUST stop dependent work without reconstructing its procedure from memory.

### Area-map creation transaction

R102. Area creation MUST require one existing structurally valid root map and MUST NOT create the root map implicitly.

R103. When the root map is absent, area creation MUST stop, route to repository root creation, and require a new area-creation attempt after the root exists.

R104. An area-creation attempt MUST bind the root path and content identity, area slug and normalized path, area parent/root identity, current evidence baseline, and expected root registration row before writing.

R105. Area creation MUST confirm both the area target and expected registration are absent before its first write.

R106. Area creation MUST prepare and validate complete area content, write the area map first, re-read and revalidate the root identity and relevant registration state, then write the exact root registration last as the transaction commit point.

R107. After commit, area creation MUST validate both artifacts and their reciprocal identity fields.

R108. A retry MAY complete only missing registration when the existing area file and complete original transaction identities match; it MUST NOT adopt a file whose identity or evidence basis differs.

R109. A dangling registration, conflicting path or parent, changed root identity, multiple candidate files or rows, stale basis, or ambiguous state MUST stop without implicit adoption or overwrite.

R110. When both artifacts already match the expected identities, an identical retry MUST return idempotent success without another write.

R111. Audit MAY identify any partial area/root transaction state but MUST remain read-only; repair requires separately resolved refresh or correction authority.

### Compatibility, preservation, and measurement

R112. New invocation results MUST use `Operation: create | refresh | audit` and `Map scope: repository | area:<slug>` and MUST NOT emit legacy `Mode`.

R113. Legacy `create` MUST map to `create + repository`; legacy `refresh` and `audit` MUST use their operation plus one explicitly resolved scope; legacy `area` MUST require one explicitly resolved operation and `area:<slug>` or stop.

R114. Existing project-map artifacts MUST remain readable and MUST NOT be rewritten solely for the result-contract or package migration.

R115. Normative and parser/package literal dependencies MUST be preserved or migrated atomically, test-only incidental assertions MUST be updated instead of owning prose, and historical forms MUST remain only where they prove compatibility.

R116. Acceptance MUST report LF-normalized UTF-8 bytes and Unicode whitespace-separated words for `SKILL.md`, the reference, the asset, `PMA0`, `PMA1`, representative outputs, and the total package, and both procedural assemblies MUST decrease unless an independently approved semantic-preservation exception identifies the exact reason.

R117. Acceptance MUST use deterministic structure, static contract scenarios, semantic review, and canonical/generated/archive/install parity and MUST NOT execute a target-agent runtime or add a permanent tokenizer, prose-quality, or simplicity validator.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64, R65, R66, R67, R68, R69, R70, R71, R72, R73, R74, R75, R76, R77, R78, R79, R80, R81, R82, R83, R84, R85, R86, R87, R88, R89, R90, R91, R92, R93, R94, R95, R96, R97, R98, R99, R100, R101, R102, R103, R104, R105, R106, R107, R108, R109, R110, R111, R112, R113, R114, R115, R116, R117

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R6, R7, R8, R9, R10, R11, R93, R94, R95, R96, R97, R98, R99, R100, R112, R113 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R7, R8, R9, R10, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R102, R103, R104, R105, R106, R107, R108, R109, R110, R111 | BND-STATE-001 | - |
| identity-authority | applicable | R10, R14, R15, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R102, R103, R104, R105, R106, R107, R108, R109, R110, R111 | BND-AUTH-001 | - |
| composition-path | applicable | R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64, R65, R85, R86, R87, R88, R89, R90, R91, R92, R93, R94, R95, R96, R97, R98, R99, R100, R101 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R100, R104, R105, R106, R107, R108, R109, R110, R111 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R57, R95, R101, R108, R109, R110, R111 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R81, R82, R83, R84, R112, R113, R114, R115, R116, R117 | BND-COMPAT-001 | - |
| external-environment | applicable | R23, R24, R25, R42, R43, R44, R45, R46, R47, R48, R93, R94, R95 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R6, R7, R8, R9, R10, R11, R93, R94, R95, R96, R97, R98, R99, R100, R112, R113 | create/refresh/audit; repository/area; coordination true/false/ambiguous; legacy forms | Exactly one operation, scope, target, and assembly are resolved before dependent work. | Valid inputs classify; missing or ambiguous identity stops; legacy ambiguity stops. | R6 |
| BND-STATE-001 | state-lifecycle | R7, R8, R9, R10, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R102, R103, R104, R105, R106, R107, R108, R109, R110, R111 | target absent/existing; map current/partial/stale; area transaction absent/partial/committed/conflicting | Create never replaces; refresh requires existing target; audit is read-only; registration is the area commit point. | Create, refresh, finding, idempotent success, or explicit stop. | R7 |
| BND-AUTH-001 | identity-authority | R10, R14, R15, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R102, R103, R104, R105, R106, R107, R108, R109, R110, R111 | observed/inferred/unknown; read-only inspection; explicit map write; command go-ahead; matching or stale identities | Evidence authority stays explicit; loading resources grants no authority; only resolved targets and matching identities may be written. | Supported claim, labeled inference, visible unknown, authorized read/write, or authority blocker. | R30 |
| BND-COMPOSE-001 | composition-path | R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64, R65, R85, R86, R87, R88, R89, R90, R91, R92, R93, R94, R95, R96, R97, R98, R99, R100, R101 | root/area maps; common/reference assembly; skeleton insertion; overlapping maps | Root remains entry point; one policy owner and one structural owner; coordinated paths load the reference. | Simple root create uses PMA0; maintenance or coordination uses PMA1; contradiction blocks clean result. | R85 |
| BND-TEMPORAL-001 | temporal-retry | R100, R104, R105, R106, R107, R108, R109, R110, R111 | late loading; first attempt; interruption after area write; concurrent root change; identical retry | Operation and scope stay stable; registration commits last; retries bind the original complete identity. | Late load, registration completion, idempotent success, or stop without overwrite. | R106 |
| BND-RECOVERY-001 | failure-recovery | R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R57, R95, R101, R108, R109, R110, R111 | missing evidence/resource; wrong prior map; orphan file; dangling row; conflict; ambiguity | Unknowns remain visible; procedure is not reconstructed; unrelated state is not adopted. | Partial/stale status, correction note, routed repair, or fail-closed stop. | R101 |
| BND-COMPAT-001 | compatibility-migration | R81, R82, R83, R84, R112, R113, R114, R115, R116, R117 | old Mode results; new Operation/Map scope results; existing maps; mixed package resources | New output is write-new; historical maps remain readable; canonical and derived packages retain parity. | Deterministic mapping, historical readability, atomic migration, rollback, or stop. | R112 |
| BND-ENV-001 | external-environment | R23, R24, R25, R42, R43, R44, R45, R46, R47, R48, R93, R94, R95 | Git available/unavailable/dirty; filesystem paths available/ambiguous; network or execution requested | Evidence baseline is truthful; known ownership surfaces are bounded; risky commands need go-ahead. | SHA, SHA+dirty, alternate evidence baseline, configured-only command, executed result, or stop. | R24 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R6, R7, R8, R9, R10, R112, R113 | BND-INPUT-001, BND-STATE-001, BND-COMPAT-001 | A legacy or explicit operation conflicts with current target existence. | Stop without implicit operation conversion; identify create or refresh as the required new operation. |
| INT-002 | R93, R94, R95, R96, R97, R98, R99, R100, R101 | BND-INPUT-001, BND-COMPOSE-001, BND-RECOVERY-001, BND-ENV-001 | Incomplete or late coordination evidence could omit required procedure. | Check known surfaces, switch to PMA1 before dependent work, or stop when resolution resources are unavailable. |
| INT-003 | R102, R103, R104, R105, R106, R107, R108, R109, R110, R111 | BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001 | Area write interruption or concurrent root mutation could create orphaned or incorrect registration state. | Register last only against the unchanged root; reconcile exact matching state and reject every mismatch. |
| INT-004 | R23, R24, R25, R26, R27, R28, R29, R87, R116 | BND-STATE-001, BND-RECOVERY-001, BND-ENV-001 | A dirty baseline or previously wrong claim could be mistaken for ordinary staleness during refresh. | Report SHA+dirty universally and use reference-owned comparison to emit the correct correction or freshness result. |
| INT-005 | R85, R86, R87, R88, R89, R90, R91, R101, R112, R113, R114, R115, R116, R117 | BND-COMPOSE-001, BND-COMPAT-001, BND-RECOVERY-001 | New literals or a missing packaged reference could produce mixed contract behavior. | Migrate real consumers atomically, validate parity, and stop rather than combine mixed resources. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R58, R61, R62 | BND-COMPOSE-001 | - | - |
| E2 | illustration | R49, R51, R52, R53 | BND-COMPOSE-001 | - | - |
| E3 | illustration | R30, R31, R32, R40, R41 | BND-AUTH-001 | - | - |
| E4 | illustration | R42, R43, R44, R45, R46, R47, R48 | BND-AUTH-001, BND-ENV-001 | - | - |
| E5 | illustration | R23, R24, R25 | BND-STATE-001, BND-ENV-001 | - | - |
| E6 | illustration | R26, R27, R28, R29 | BND-STATE-001, BND-RECOVERY-001 | - | - |
| E7 | illustration | R7, R8, R9 | BND-INPUT-001, BND-STATE-001 | - | - |
| E8 | illustration | R10, R111 | BND-STATE-001, BND-AUTH-001 | - | - |
| E9 | illustration | R93, R94, R95 | BND-INPUT-001, BND-COMPOSE-001, BND-ENV-001 | - | - |
| E10 | illustration | R100 | BND-INPUT-001, BND-COMPOSE-001, BND-TEMPORAL-001 | - | - |
| E11 | illustration | R104, R105, R106, R107 | BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001 | - | - |
| E12 | illustration | R108, R109, R110, R111 | BND-TEMPORAL-001, BND-RECOVERY-001 | - | - |

## Inputs and outputs

Inputs:

- User orientation request, area request, refresh request, or audit request.
- Project-local guidance such as `AGENTS.md`, `CONSTITUTION.md`, `docs/workflows.md`, `docs/project-map.md`, specs, ADRs, README files, build manifests, package manifests, schemas, tests, CI workflows, deployment files, infrastructure files, source files, and generated output with known canonical sources.
- Existing root or area maps when present.

Outputs:

- Created, refreshed, or audited project-map artifact.
- Result block with operation, status, map scope, artifacts changed, freshness result, correction note, blockers, and next stage.
- For formal repository work, validation evidence and change-local artifacts required by the active workflow stage.

## State and invariants

- A project map is a living reference, not a source-of-truth override.
- Source code, runtime configuration, schemas, build manifests, tests, and CI remain stronger evidence of current behavior than the map.
- Intent artifacts can describe planned or required behavior but do not prove current implementation.
- Root maps remain the repository-level entry point when area maps exist.
- Area maps provide bounded depth for durable repository boundaries.
- Unknowns remain visible rather than being silently guessed.
- The skeleton asset owns output structure, while `SKILL.md` owns evidence, freshness, source-rank, claim-boundary, and handoff policy.
- Operation selection is bound to target existence, while procedural assembly selection is bound to operation, scope, and coordination evidence.
- Area creation is committed only by the exact root registration written after a validated area file.

## Error and boundary behavior

- If artifact placement cannot be resolved by explicit path, metadata, workflow guidance, or portable default, the skill MUST block instead of guessing.
- If required evidence is unavailable, the map MUST use `partial` status or record unknowns rather than claiming current.
- If overlapping maps contradict each other, the skill MUST block a clean refresh result and name the contradiction.
- If a cited path no longer exists, downstream reliance on that claim is unsafe until source inspection or map refresh resolves the gap.
- If a user requests runtime, network, build, or test execution without sufficient safety context, the skill MUST ask for go-ahead before executing those commands.
- If create targets an existing map or refresh targets an absent map, the skill MUST stop and identify the required operation without silently reclassifying it.
- If known coordination surfaces are unavailable, conflicting, or ambiguous, the skill MUST load reference-owned resolution procedure or stop when it is unavailable.
- If an area transaction observes an orphan, dangling registration, changed root, stale basis, conflict, or ambiguity, it MUST stop without implicit adoption or overwrite.

## Compatibility and migration

- Existing project maps remain valid historical artifacts but do not automatically satisfy the revised contract until refreshed.
- This change does not require automatic migration of existing customer or repository maps.
- The revised skill and skeleton must remain portable to customer projects without requiring RigorLoop repository internals.
- Generated adapter output must be rebuilt from canonical skill source; generated public adapter skill bodies must not be hand-edited.
- If `orientation` is not an accepted workflow-role stage value, the implementation must reuse an approved equivalent or amend the governing skill contract before publishing the new role block.
- New invocation results use `Operation` and `Map scope`; old map artifacts remain readable and are not rewritten solely to adopt the new result contract.
- Real parser and package consumers of legacy `Mode` migrate atomically, while historical fixtures may retain the old form only to prove compatibility.

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
- Loaded-context measurement must distinguish semantic classifications from the two procedural assemblies and must report total package size separately.

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

EC13. Create targets an existing map: stop and require refresh.

EC14. Refresh targets an absent map: stop and route to create.

EC15. Audit targets an absent map: emit `missing-map` without mutation.

EC16. Root creation discovers an area map after initial classification: load PMA1 before dependent work without changing operation or scope.

EC17. Coordination paths are configured but unavailable: require reference-owned resolution or stop.

EC18. Area creation has no root map: stop and route to root creation without implicitly creating it.

EC19. Area file exists without registration after interruption: complete registration only when every bound identity matches.

EC20. Root changes after area-file write: stop without overwriting or adopting the changed root.

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
| AC-PMAP-003 | The skill supports three operations and repository or area scope as independent axes. |
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
| AC-PMAP-023 | Create applies only to absent targets, refresh applies only to existing targets, and full rewrites remain refreshes. |
| AC-PMAP-024 | Audit is always read-only, including missing-map and post-audit correction paths. |
| AC-PMAP-025 | New results emit `Operation` and `Map scope` and omit legacy `Mode`. |
| AC-PMAP-026 | Root creation omits the reference only after the bounded seven-surface coordination preflight. |
| AC-PMAP-027 | Ambiguous or unavailable known coordination surfaces cannot be treated as no coordination. |
| AC-PMAP-028 | Six semantic classifications remain separate from PMA0 and PMA1 procedural assemblies. |
| AC-PMAP-029 | Late coordination discovery loads PMA1 before dependent judgment or writes. |
| AC-PMAP-030 | Missing or mixed required resources fail closed without remembered reconstruction. |
| AC-PMAP-031 | The skeleton is the sole structural owner and does not own evidence or lifecycle policy. |
| AC-PMAP-032 | Area creation requires one existing valid root and never creates it implicitly. |
| AC-PMAP-033 | Area creation binds complete root, area, path, parent, baseline, and registration identities. |
| AC-PMAP-034 | Area content is validated before root registration, and registration is the commit point. |
| AC-PMAP-035 | Exact matching partial area state is recoverable and mismatched, dangling, stale, conflicting, or ambiguous state stops. |
| AC-PMAP-036 | Existing maps remain readable without automatic rewriting. |
| AC-PMAP-037 | Legacy result consumers migrate according to their normative, parser, incidental, obsolete, or historical classification. |
| AC-PMAP-038 | Both PMA0 and PMA1 loaded words and bytes decrease unless an independently approved semantic-preservation exception applies. |
| AC-PMAP-039 | Common-path and total-package measurements are reported separately. |
| AC-PMAP-040 | Static proof covers all applicable boundaries and selected interactions without target-agent execution. |
| AC-PMAP-041 | Canonical, generated, archived, and installed resources retain required parity. |

## Open questions

None.

## Next artifacts

```text
spec-review
architecture assessment
architecture
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

Ready for independent `spec-review`. This revision does not claim spec approval, architecture completion, planning readiness, implementation readiness, verification, branch readiness, or PR readiness.
