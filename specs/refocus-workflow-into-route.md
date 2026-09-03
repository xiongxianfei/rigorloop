# Refocus Workflow into Route

## Owning change record

`docs/changes/2026-09-02-refocus-workflow-into-route/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

[Refocus Workflow into the Route Skill](../docs/proposals/2026-09-02-refocus-workflow-into-route.md)

## Goal and context

RigorLoop must expose one `route` skill for semantic workflow routing, resumption, audit, correction ownership, and bounded automation. Deterministic project-local workflow facts must come from a read-only CLI context projection instead of agent reconstruction or `docs/workflows.md`. The rename must preserve current v3 stage ownership and active automation while removing guide authoring and the old public skill name.

## Glossary

- **Route:** the public skill that interprets engineering meaning and selects or orchestrates the next owning stage.
- **Workflow authority:** the stable lifecycle protocol role used by route-owned operations; its stored value remains `workflow`.
- **Workflow context:** the read-only CLI projection of deterministic project facts and, when selected, exact change facts.
- **Project phase:** context without an exact change, used to expose candidates and configuration.
- **Change phase:** context for one explicit change, used to expose current lifecycle, artifacts, paths, blockers, operations, and automation.
- **Bundled default:** a versioned artifact-location rule shipped with the CLI.
- **Repository override:** a supported project-local configuration value in `rigorloop.workflow.yaml`.
- **Semantic routing:** judgment about what a request or finding means and which structurally permitted owner should act.
- **Portable mode:** skill use without authoritative governed CLI context; it grants no governed lifecycle claim.

## Examples first

Example E1: Route resumes one exact governed change
Given a user identifies an active change
When route requests change-phase workflow context
Then the CLI returns its exact stage, artifacts, blockers, permitted operations, and automation state, and route selects the semantically correct permitted next action

Example E2: Several active changes are not silently selected
Given project-phase context finds several active governed changes
When no explicit request disambiguates them
Then the CLI returns bounded candidates, route reports selection ambiguity, and neither component chooses or mutates a change

Example E3: Architecture finding routes semantically
Given the CLI reports that returning to spec or architecture is structurally permitted
And a review finding concerns a technical boundary rather than required behavior
When route evaluates the finding
Then route selects architecture ownership; the CLI did not originate that semantic decision

Example E4: Repository override resolves a custom path
Given `rigorloop.workflow.yaml` contains a valid supported path template for formal reviews
When workflow context resolves a review output for an exact change and round
Then it returns the normalized repository-relative path and `repository-override` provenance

Example E5: Invalid configuration fails closed
Given repository configuration contains an unknown artifact kind or a path escaping the repository
When workflow context loads it
Then it returns a deterministic configuration blocker and does not fall back to prose, filename guessing, prior chat, or memory

Example E6: Existing automation resumes after rename
Given a v3 change has active `workflow.automation` state created before the package rename
When the current route skill resumes it
Then the same target, occurrence, budgets, and receipts remain authoritative without rewriting the lifecycle record

Example E7: Old skill invocation has no alias
Given the current adapter inventory contains `route` and no `workflow` package
When installation or upgrade detects an obsolete current `workflow` package or request
Then it identifies `route` as the replacement and does not install or execute a compatibility alias

Example E8: Historical workflow guide is ignored
Given a repository still contains an old `docs/workflows.md`
When current route resolves governed workflow information
Then CLI context remains authoritative and the historical document does not affect paths, stages, permissions, or routing

Example E9: Stage ownership remains intact
Given route selects specification as the next owner
When work continues
Then the spec skill authors and registers specification content; route does not write it merely because it chose the stage

Example E10: Route package resources migrate coherently
Given the current canonical route package is generated for a supported adapter
When package validation checks its invocation assemblies and mapped resources
Then routing and conditional automation resources are present, guide-only resources are absent, and a missing or mixed required resource blocks use

Example E11: Portable placement does not claim governed authority
Given a direct portable invocation has no governed CLI context
When an explicit safe artifact path or published portable default is available
Then the owning stage may use it subject to safety and governance constraints but does not claim project-local governed placement

## Requirements

| ID | Requirement |
| --- | --- |
| RT-R1 | Current authored and published skill inventories MUST contain one public `route` skill and MUST NOT contain a current `workflow` skill, alias, or tombstone package. |
| RT-R2 | Route MUST own semantic workflow routing, resumption, auditing, correction ownership, bounded automation orchestration, target handling, and stop-or-continue judgment. |
| RT-R3 | Route MUST NOT author, approve, settle, or repair another stage's semantic artifact merely because it selected that stage. |
| RT-R4 | Proposal, specification, architecture, ADR, plan, review, implementation, Verify, and PR evidence ownership MUST remain unchanged. |
| RT-R5 | The v3 lifecycle stage graph and current stage-transition semantics MUST remain unchanged by the skill rename. |
| RT-R6 | The CLI MUST expose a read-only `rigorloop workflow-context` command with versioned human and JSON results derived from one normalized result model. |
| RT-R7 | Project-phase workflow context MUST return the effective lifecycle contract, configuration provenance, bounded active-change candidates, and deterministic selection or configuration blockers without selecting a change. |
| RT-R8 | Change-phase workflow context MUST require one exact change identity and return its current lifecycle revision, stage, artifact identities and evidence states, resolved artifact locations, package and milestone projections, blockers, structurally permitted operations, and bounded automation projection. |
| RT-R9 | Workflow context MUST NOT mutate repository state, classify user intent, select correction ownership, choose among candidates, or decide which structurally permitted transition is semantically correct. |
| RT-R10 | Route MUST consume workflow context for governed deterministic facts and MUST NOT independently reconstruct those facts from repository prose, filename conventions, prior chat, remembered state, or guessed paths. |
| RT-R11 | When exact change identity is not already authoritative, route MUST use project-phase context before change-phase context and MUST stop if explicit user intent and current evidence cannot resolve several candidates. |
| RT-R12 | Route MUST treat a current lifecycle revision returned by change-phase context as stale after any lifecycle mutation or observed identity drift and MUST refresh before another dependent operation. |
| RT-R13 | The CLI MUST derive effective artifact-location configuration from versioned bundled v3 defaults followed by an optional repository-root `rigorloop.workflow.yaml` override. |
| RT-R14 | `rigorloop.workflow.yaml` MUST use a closed schema version and a closed `artifact_locations` map keyed only by supported artifact kinds. |
| RT-R15 | Each configured artifact location MUST contain exactly one supported repository-relative path template or structured non-path surface; unknown keys, kinds, placement forms, or template variables MUST fail closed. |
| RT-R16 | Path resolution MUST reject absolute paths, repository escape, symlink-dependent traversal, incomplete variables, duplicate effective ownership, ambiguous results, and conflicts with lifecycle or stage ownership. |
| RT-R17 | Workflow context MUST report each effective configured value with `bundled-default` or `repository-override` provenance and MUST identify the repository-relative source of a configuration blocker. |
| RT-R18 | Explicit user artifact identity or path MAY be supplied as request input but MUST remain subordinate to governance, schema, ownership, security, and repository-containment constraints. |
| RT-R19 | `docs/workflows.md` MUST NOT be created, refreshed, required, parsed, or consulted by current RigorLoop routing, placement, lifecycle, validation, installation, or release behavior. |
| RT-R20 | A retained historical `docs/workflows.md` MUST be treated as ordinary documentation without RigorLoop lifecycle or routing authority and MUST require no migration. |
| RT-R21 | The route package MUST remove workflow-guide authoring behavior, guide-specific invocation predicates and assemblies, `references/workflow-guide-authoring.md`, `assets/workflows-skeleton.md`, and every workflow-map fallback. |
| RT-R22 | Route invocation classification MUST cover portable routing, governed routing, automation command, active or resumable automation, automation bootstrap, automation status, and cancellation without a guide-authoring dimension. |
| RT-R23 | Route MUST load governed routing guidance only when governed routing is applicable and automation guidance only for an armed, resumable, bootstrap, status, or cancellation automation context. |
| RT-R24 | Missing, unreadable, contradictory, or mixed-version required route resources MUST stop the affected operation without remembered or invented reconstruction. |
| RT-R25 | In portable mode, route or a stage skill MAY use an explicit safe target or its published portable default, but MUST NOT claim governed lifecycle state or project-local customization without authoritative CLI context. |
| RT-R26 | Route MUST continue to use the stable lifecycle `stage_authority: workflow` role for workflow-owned mutations; that token MUST NOT be interpreted as a current public skill identity. |
| RT-R27 | Existing `workflow.automation` stored state MUST remain readable and resumable by route without rewriting change records solely for the rename. |
| RT-R28 | Resuming existing automation MUST preserve exact target, occurrence, authorization identity, budgets, receipts, pause/cancel state, and lifecycle revision safeguards. |
| RT-R29 | Current user-facing skill names, commands, examples, documentation, manifests, and release metadata MUST use `route` except where explicitly documenting the stable protocol token, stored namespace, historical evidence, or migration from the old name. |
| RT-R30 | Installer, upgrade, and validation paths MUST detect an obsolete current `workflow` package or request, identify `route` as its replacement, and reject mixed inventories containing both current names. |
| RT-R31 | Historical release archives and completed historical workflow artifacts MUST remain immutable and MUST NOT be rewritten to use the new name. |
| RT-R32 | `skills/` MUST remain the only authored skill source; current generated adapters MUST reproduce the route package and its mapped resources without hand-edited generated source. |
| RT-R33 | Current governance, workflow specs, architecture, skills, schemas, validators, fixtures, docs, adapter metadata, and release validation MUST remove authoritative `docs/workflows.md` and current `workflow`-skill dependencies coherently. |
| RT-R34 | Every new closed vocabulary introduced for workflow context, configuration, skill identity, placement, or outcome MUST reject unknown values before consistency checks and MUST have a direct unknown-value regression test. |
| RT-R35 | Human workflow-context output MUST make effective sources, selection state, current stage, blockers, permitted operations, and resolved locations understandable without inspecting JSON or `docs/workflows.md`. |
| RT-R36 | Workflow-context output and diagnostics MUST use repository-relative paths and bounded identifiers and MUST NOT expose secrets, credentials, private environment dumps, or machine-local absolute paths. |
| RT-R37 | Current package validation MUST prove the CLI remains structural by demonstrating that multiple candidates or permitted transitions are reported without a semantic choice. |
| RT-R38 | Current package validation MUST prove that workflow context is read-only and that failure, ambiguity, retry, and identical reads leave governed files byte-identical. |

## Important scenarios

- A review finding can structurally route to more than one upstream stage; CLI reports allowed routes and route chooses from engineering meaning.
- A custom path uses `<review-round>` where no round exists; configuration resolution blocks instead of emitting an incomplete path.
- A repository has no override file; bundled defaults resolve current supported artifact locations and provenance remains explicit.
- A repository has a valid old workflow guide and a conflicting valid config override; the CLI uses the config override and ignores the guide.
- A stale adapter contains both `workflow` and `route`; validation rejects the mixed inventory.
- A current route invocation resumes automation whose persisted owner namespace is `workflow.automation`; no migration occurs.
- A direct portable stage invocation has no CLI or config; its safe portable default may be used without claiming governed placement.
- The CLI reports `advance-stage` as permitted, but a semantic blocker means route stops rather than advancing.

## Acceptance conditions

- Current skill discovery exposes `route`, not `workflow`.
- One bounded CLI call exposes deterministic project facts and one exact change call exposes deterministic change facts.
- Route owns semantic selection and the CLI demonstrably does not.
- Valid repository configuration overrides bundled defaults; invalid or ambiguous configuration blocks without prose fallback.
- Current routing never reads or requires `docs/workflows.md`.
- Existing v3 automation resumes unchanged through route.
- Stage skills continue to own their artifacts and reviews.
- Current adapters, docs, validators, and release metadata agree on the new identity and removed guide surface.

## Inputs and outputs

Project-phase inputs are repository identity, bundled defaults, optional `rigorloop.workflow.yaml`, lifecycle activation data, and discoverable governed change records. Its output is one read-only context result containing effective configuration and bounded candidates or blockers.

Change-phase inputs additionally include one exact change ID and its current governed evidence. Its output is one read-only result containing the current lifecycle revision, stage, resolved locations, artifact/package/milestone/blocker/operation state, and automation projection.

Route inputs are the user's request, authoritative context results, and relevant engineering evidence. Its output is one semantic route, stage invocation, automation action, audit result, or explicit stop. It does not output another stage's artifact or verdict.

## State and invariants

- `change.yaml` remains the only mutable governed lifecycle snapshot.
- Workflow context is a derived projection and never a second state store.
- The optional repository configuration owns only supported deterministic project values, not lifecycle state or semantic policy.
- `route` is the sole current public skill identity; `workflow` remains only a documented protocol token, stored namespace, or historical name.
- Structural permission never implies semantic correctness.
- A resolved path never transfers artifact authority.
- Active automation identity survives the rename unchanged.
- Historical documents and archives never regain current authority through fallback.

## Error and boundary behavior

- No repository or unsupported configuration schema: return an explicit blocker and do not guess.
- Several active changes without authoritative disambiguation: return candidates and stop without selection.
- Missing exact change: return not-found without falling back to another change.
- Unknown configuration or result vocabulary: fail before consistency interpretation.
- Unsafe or ambiguous path: report the config source and offending artifact kind without emitting an authorized output path.
- Stale lifecycle revision: refresh change-phase context before dependent mutation.
- Semantic ambiguity despite structural permission: route stops for owner input.
- Missing route resource: stop the affected route or automation action.
- Obsolete current package: identify `route` replacement and require coherent installation.
- Dependency or filesystem read failure: return bounded failure and leave governed state byte-identical.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: RT-R1, RT-R2, RT-R3, RT-R4, RT-R5, RT-R6, RT-R7, RT-R8, RT-R9, RT-R10, RT-R11, RT-R12, RT-R13, RT-R14, RT-R15, RT-R16, RT-R17, RT-R18, RT-R19, RT-R20, RT-R21, RT-R22, RT-R23, RT-R24, RT-R25, RT-R26, RT-R27, RT-R28, RT-R29, RT-R30, RT-R31, RT-R32, RT-R33, RT-R34, RT-R35, RT-R36, RT-R37, RT-R38

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | RT-R6, RT-R7, RT-R8, RT-R11, RT-R13, RT-R14, RT-R15, RT-R16, RT-R17, RT-R18 | BND-INPUT-001 | - |
| state-lifecycle | applicable | RT-R5, RT-R7, RT-R8, RT-R12, RT-R19, RT-R20, RT-R27, RT-R28, RT-R31, RT-R38 | BND-STATE-001 | - |
| identity-authority | applicable | RT-R1, RT-R2, RT-R3, RT-R4, RT-R8, RT-R9, RT-R10, RT-R18, RT-R25, RT-R26, RT-R29, RT-R30 | BND-AUTH-001 | - |
| composition-path | applicable | RT-R6, RT-R10, RT-R13, RT-R19, RT-R21, RT-R22, RT-R23, RT-R24, RT-R32, RT-R33 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | RT-R12, RT-R27, RT-R28, RT-R31, RT-R38 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | RT-R11, RT-R15, RT-R16, RT-R17, RT-R24, RT-R30, RT-R34, RT-R38 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | RT-R1, RT-R19, RT-R20, RT-R21, RT-R26, RT-R27, RT-R29, RT-R30, RT-R31, RT-R33 | BND-COMPAT-001 | - |
| external-environment | applicable | RT-R13, RT-R16, RT-R24, RT-R32, RT-R35, RT-R36, RT-R38 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | RT-R6, RT-R7, RT-R8, RT-R11, RT-R13, RT-R14, RT-R15, RT-R16, RT-R17, RT-R18 | no or exact change; absent, valid, unknown, malformed, unsafe, conflicting, or ambiguous config; bundled or overridden value | Inputs use closed schemas and safe repository-relative identities; project phase never selects a candidate. | Exact valid input yields bounded context; unsupported, unsafe, or ambiguous input blocks without fallback. | RT-R15 |
| BND-STATE-001 | state-lifecycle | RT-R5, RT-R7, RT-R8, RT-R12, RT-R19, RT-R20, RT-R27, RT-R28, RT-R31, RT-R38 | current or stale context; inactive, active, paused, cancelled, complete, or resumable automation; current or historical guide/package | Derived context never mutates state; current revision is required for dependent mutation; history grants no current authority. | Current state supports routing judgment; stale state refreshes; historical surfaces are ignored. | RT-R12 |
| BND-AUTH-001 | identity-authority | RT-R1, RT-R2, RT-R3, RT-R4, RT-R8, RT-R9, RT-R10, RT-R18, RT-R25, RT-R26, RT-R29, RT-R30 | route skill, workflow protocol role, CLI structural owner, stage owner, current or obsolete package | CLI reports; route judges; stage owner authors; resolved location or permission never transfers authority. | Correct owner acts; ambiguity or obsolete identity stops with bounded guidance. | RT-R3 |
| BND-COMPOSE-001 | composition-path | RT-R6, RT-R10, RT-R13, RT-R19, RT-R21, RT-R22, RT-R23, RT-R24, RT-R32, RT-R33 | defaults to override to context to route to stage; canonical route package to generated adapter; governed or portable path | Current governed routing composes through CLI context and never through the retired guide; generated packages mirror canonical source. | Coherent composition routes; missing resource or mixed surface blocks. | RT-R10 |
| BND-TEMPORAL-001 | temporal-retry | RT-R12, RT-R27, RT-R28, RT-R31, RT-R38 | first read, identical reread, mutation, stale reread, active-run resume, retry, historical read | Reads are non-mutating; mutation stales prior context; rename alone does not change automation occurrence. | Identical reads are stable; stale context refreshes; active automation resumes exactly. | RT-R28 |
| BND-RECOVERY-001 | failure-recovery | RT-R11, RT-R15, RT-R16, RT-R17, RT-R24, RT-R30, RT-R34, RT-R38 | ambiguity, config failure, resource failure, stale install, correction, retry | Failure leaves governed state byte-identical and cannot trigger guessed fallback or partial semantic action. | Owner/configuration correction followed by a fresh read may recover; unresolved failure stops. | RT-R38 |
| BND-COMPAT-001 | compatibility-migration | RT-R1, RT-R19, RT-R20, RT-R21, RT-R26, RT-R27, RT-R29, RT-R30, RT-R31, RT-R33 | current route package, obsolete workflow package, mixed package, historical archive, old guide, stable stored protocol names | One current public name; no guide authority; historical evidence immutable; stored v3 automation remains readable. | Coherent route package operates; obsolete or mixed current package rejects; history remains non-authoritative. | RT-R30 |
| BND-ENV-001 | external-environment | RT-R13, RT-R16, RT-R24, RT-R32, RT-R35, RT-R36, RT-R38 | missing repository, absent config, filesystem failure, symlink, generated adapter, human or JSON output | No network/service dependency; paths remain contained; diagnostics omit host-private data; generated output derives from canonical source. | Safe local context succeeds; unavailable or unsafe environment blocks without mutation. | RT-R36 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | RT-R7, RT-R9, RT-R11, RT-R37 | BND-INPUT-001, BND-AUTH-001 | Several candidates or transitions cause the CLI to make a semantic choice. | CLI reports bounded alternatives; route selects from user intent and engineering evidence or stops. |
| INT-002 | RT-R13, RT-R15, RT-R16, RT-R19 | BND-INPUT-001, BND-COMPOSE-001, BND-RECOVERY-001 | Invalid configuration silently falls back to the retired guide or guessed defaults. | Invalid effective configuration blocks with provenance and no prose fallback. |
| INT-003 | RT-R1, RT-R26, RT-R27, RT-R28, RT-R30 | BND-AUTH-001, BND-TEMPORAL-001, BND-COMPAT-001 | Public rename invalidates stable authority or active automation, or dual names gain current authority. | Route is the sole public skill; stored workflow role/state stays exact and resumes without alias or migration. |
| INT-004 | RT-R3, RT-R8, RT-R10, RT-R18 | BND-AUTH-001, BND-COMPOSE-001 | CLI path resolution or route selection is treated as authority to author another stage's artifact. | The stage owner alone authors and registers its content; route and CLI retain bounded roles. |
| INT-005 | RT-R12, RT-R24, RT-R38 | BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001 | A failed read or later mutation leaves route acting on stale or partial context. | Failed reads are non-mutating; any mutation/drift requires a complete fresh context before dependent action. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | RT-R2, RT-R8, RT-R10 | BND-AUTH-001, BND-COMPOSE-001 | - | - |
| E2 | illustration | RT-R7, RT-R9, RT-R11 | BND-INPUT-001, BND-AUTH-001 | - | - |
| E3 | illustration | RT-R2, RT-R9, RT-R37 | BND-AUTH-001 | - | - |
| E4 | illustration | RT-R13, RT-R15, RT-R17 | BND-INPUT-001, BND-COMPOSE-001 | - | - |
| E5 | illustration | RT-R15, RT-R16, RT-R19 | BND-INPUT-001, BND-RECOVERY-001 | - | - |
| E6 | illustration | RT-R26, RT-R27, RT-R28 | BND-TEMPORAL-001, BND-COMPAT-001 | - | - |
| E7 | illustration | RT-R1, RT-R29, RT-R30 | BND-AUTH-001, BND-COMPAT-001 | - | - |
| E8 | illustration | RT-R19, RT-R20 | BND-COMPOSE-001, BND-COMPAT-001 | - | - |
| E9 | illustration | RT-R3, RT-R4 | BND-AUTH-001 | - | - |
| E10 | illustration | RT-R21, RT-R22, RT-R23, RT-R24, RT-R32, RT-R33 | BND-COMPOSE-001, BND-RECOVERY-001, BND-ENV-001 | - | - |
| E11 | illustration | RT-R18, RT-R25 | BND-INPUT-001, BND-AUTH-001 | - | - |

## Compatibility and migration

The release makes one clean current-package transition from `workflow` to `route`. Canonical skills and every current generated adapter contain route only. Upgrade and validation paths diagnose an obsolete current workflow installation and direct users to route; no compatibility skill is published.

Stored v3 lifecycle authority `workflow` and `workflow.automation` remain valid and require no record migration. Historical releases, completed changes, and historical workflow guides remain unchanged. Current tooling ignores any retained guide. Earlier specifications that assign current authority to `docs/workflows.md` or the public workflow skill are superseded for current packages by this specification and must be marked or amended coherently during implementation.

## Observability

Human and JSON context results expose configuration version and provenance, candidate or selected change identity, lifecycle revision, stage, artifact and evidence state, resolved locations, package/milestone/automation state, blockers, permitted operations, and claim limits. Stable diagnostics distinguish selection ambiguity, unsupported config, unknown vocabulary, unsafe path, stale context, obsolete skill identity, and mixed package state.

No telemetry service, external database, background process, or network observation is introduced.

## Security and privacy

The configuration language is data-only and cannot execute commands or interpolate environment values. Paths are normalized inside the repository. Results use repository-relative paths and bounded IDs and omit credentials, tokens, secrets, usernames, hostnames, absolute paths, and unrelated file content.

## Accessibility and UX

Human output is text-first and states the selected or ambiguous identity, current stage, configuration provenance, blockers, permitted operations, and next structural options directly. Users do not need to interpret JSON or a removed Markdown guide. Migration documentation states the single replacement invocation `$route`.

## Performance expectations

Project context performs one bounded scan of supported change records and one bounded configuration load. Change context reads the selected record and its registered evidence surfaces. It performs no repository-wide semantic search, Git-history scan, network request, or unbounded prose parsing. Correctness takes precedence over a fixed latency target.

## Edge cases

EC1. The override file is absent: bundled defaults are valid and explicitly identified.

EC2. The override file is empty or has an unsupported schema: context blocks rather than treating it as absent.

EC3. Two path templates normalize to conflicting owned output for one operation: resolution blocks.

EC4. A symlink inside a configured path leaves the repository: path validation blocks.

EC5. The explicit change is complete and another change is active: change phase returns the explicit change and does not silently substitute the active one.

EC6. Existing automation is paused: route may report or resume it under existing authorization; rename does not change pause state.

EC7. A host receives `$workflow` but resolves skills before CLI execution: the host may report unavailable; supported install/upgrade diagnostics and migration docs identify `$route` without publishing an alias.

EC8. A historical document uses “workflow skill” descriptively: it is not rewritten; current-package validation distinguishes historical surfaces from current inventory claims.

EC9. Route context says an artifact path is valid but an owning stage rejects content: stage ownership wins and route cannot override it.

EC10. A context read is interrupted: no lifecycle or configuration file is changed and the caller must perform a complete fresh read.

## Non-goals

- Moving semantic routing, blocker interpretation, or correction ownership into the CLI.
- Changing lifecycle stages or another stage's artifact contract.
- Renaming stored workflow authority or automation namespaces in this change.
- Building an autonomous workflow engine, daemon, hosted service, or external state store.
- Inferring project semantics from filenames or making configuration executable.
- Preserving `docs/workflows.md` as generated compatibility output.
- Rewriting historical archives, changes, or ordinary project documentation.
- Defining future configuration beyond the first closed artifact-location surface.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| RT-AC1 | Current canonical and generated skill inventories contain route and no workflow alias or guide-only resource. |
| RT-AC2 | Project-phase context reports configuration and bounded candidates without choosing among them or mutating files. |
| RT-AC3 | Change-phase context reports the exact deterministic lifecycle, location, package, operation, and automation facts for one selected change. |
| RT-AC4 | Route selects semantic ownership from CLI facts while CLI tests prove it does not make that selection. |
| RT-AC5 | Valid repository overrides resolve with provenance; unknown, unsafe, incomplete, conflicting, and ambiguous values fail closed with regression coverage. |
| RT-AC6 | Current routing and validation succeed without `docs/workflows.md` and ignore a retained historical copy. |
| RT-AC7 | An existing active, paused, or resumable v3 automation occurrence remains exact and usable through route without lifecycle migration. |
| RT-AC8 | Stage artifact ownership, registration, review, and settlement boundaries remain unchanged. |
| RT-AC9 | Obsolete or mixed current workflow packages are diagnosed, route is identified as replacement, and no alias is installed. |
| RT-AC10 | Human output is sufficient to inspect effective workflow facts without JSON or a generated guide. |
| RT-AC11 | Unknown closed values fail before consistency checks and each new vocabulary has an unknown-value regression test. |
| RT-AC12 | Repository lifecycle, skill, resource, adapter, explicit-path, docs, and release validation pass for the coherent route package. |

## Open questions

None. Exact internal module names, serialized JSON field order beyond the versioned public schema, delivery milestones, test commands, and release commands belong to Delivery planning.

## Next artifacts

- Design Review with `docs/architecture/2026-09-02-refocus-workflow-into-route.md` and `docs/adr/ADR-20260902-route-context-and-skill-identity.md`.
- Execution plan after approved Design Review.

## Follow-on artifacts

None yet

## Readiness

Ready for Design Review reconciliation with the architecture and ADR. This specification does not authorize implementation until the exact Design package is approved.
