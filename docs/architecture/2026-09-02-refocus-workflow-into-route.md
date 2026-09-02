# Route-Focused Workflow Architecture

## Owning change record

- `docs/changes/2026-09-02-refocus-workflow-into-route/change.yaml`

## Related artifacts

- Proposal: [Refocus Workflow into the Route Skill](../proposals/2026-09-02-refocus-workflow-into-route.md)
- Specification: None yet; specification reconciliation follows this architecture.
- Plan: None yet.
- ADR: [ADR-20260902-route-context-and-skill-identity](../adr/ADR-20260902-route-context-and-skill-identity.md)

## Introduction and Goals

This architecture turns the mixed-purpose `workflow` package into a route-focused orchestration package. Deterministic project and lifecycle facts move behind a read-only CLI projection; semantic routing, correction ownership, auditing, resumption, and bounded automation remain in the renamed `route` skill. The generated `docs/workflows.md` guide and its authoring machinery are retired.

The design reduces repeated agent reconstruction while preserving stage ownership, Git-native engineering evidence, current v3 lifecycle authority, and existing active automation.

## Architecture Constraints

- `stage-owned-change-local-v3` remains the active lifecycle graph; this change does not redesign its stages.
- The lifecycle CLI may state what is structurally true or permitted but may not decide what an engineering finding means or which permitted route is correct.
- `route` may select and orchestrate a stage but may not author that stage's semantic artifact or review verdict.
- `change.yaml` remains the sole mutable governed lifecycle snapshot.
- Proposal, spec, architecture, ADR, plan, review, implementation, Verify, and PR evidence remain repository-owned.
- `skills/` remains the only authored skill source; adapter packages remain generated release output.
- Unknown configuration, paths, lifecycle values, or operation values fail closed before consistency checks.
- Current packages make a clean public rename: `route` exists and `workflow` does not.
- Stored `workflow` authority and `workflow.automation` keys remain stable protocol identifiers so v3 runs need no migration.

## Context and Scope

```text
User or automation request
          |
          v
     route skill ---------------- semantic meaning, owner, stop/continue
          |
          v
rigorloop workflow-context ------- deterministic project/change facts
          |
          +-- bundled v3 defaults
          +-- rigorloop.workflow.yaml (optional override)
          +-- lifecycle contract and change.yaml records
          +-- registered artifacts, packages, milestones, automation
          |
          v
  route-selected owning stage ---- stage-owned artifact or evidence
```

This is a repository protocol and packaged-skill change, not a new service, process, network boundary, or deployable container. A C4 diagram would add no material information beyond the authority flow above.

## Solution Strategy

1. Introduce `rigorloop workflow-context` as the sole current CLI projection for deterministic project-local routing facts.
2. Define bundled v3 workflow defaults plus an optional closed `rigorloop.workflow.yaml` repository override.
3. Rename the authored and published package to `route`, remove guide-only resources and assemblies, and preserve only routing and automation resources selected by progressive disclosure.
4. Remove `docs/workflows.md` from authority, validation, authoring, discovery, templates, and current documentation.
5. Preserve the stable lifecycle `workflow` authority token and `workflow.automation` persistence namespace while changing user-facing skill identity to `route`.
6. Migrate all current consumers and generated packages coherently, with deterministic stale-install diagnostics and no current alias.

## Building Block View

### Workflow-context command

`rigorloop workflow-context [--change <change-id>] [--format human|json]` is a read-only top-level command adjacent to the lifecycle command family.

Project phase, without `--change`, returns:

- result schema and command identity;
- effective lifecycle contract and activation authority;
- configuration source, version, and normalized placement summary;
- active governed-change candidates with bounded stage/status facts;
- deterministic blockers such as malformed configuration or selection ambiguity.

Change phase, with `--change`, additionally returns:

- exact lifecycle revision and current stage;
- registered artifact IDs, kinds, owners, paths, identities, and evidence state;
- resolved location for each known stage-owned output;
- approved/incomplete package, milestone, review, and blocker projections;
- immediate structurally permitted operations and route-required operations;
- current bounded-automation target, occurrence, status, and receipts when present.

The command does not accept a mutation request. It does not infer user intent or select among multiple changes, owners, findings, or routes. Human and JSON renderers consume the same normalized result. Diagnostics use stable codes and repository-relative paths and remain useful without reading `docs/workflows.md`.

### Project workflow configuration

The CLI begins with versioned bundled defaults for every supported artifact kind and external surface. An optional repository-root `rigorloop.workflow.yaml` may override supported locations. Its schema has:

- `schema_version` from a closed supported set;
- `artifact_locations`, keyed by closed artifact kind;
- for each entry, exactly one supported repository-relative path template or structured non-path surface;
- optional bounded ownership metadata only when it agrees with the lifecycle's closed stage owner.

Templates may use only documented variables such as `<change-id>`, `<date>`, `<slug>`, and `<review-round>`, and only where the artifact kind supplies them. Resolution normalizes paths inside the repository and rejects escape, absolute, symlink-dependent, ambiguous, incomplete, duplicate, and conflicting values. The CLI reports effective value and provenance (`bundled-default` or `repository-override`). It never parses workflow policy from prose.

### Route skill package

The current package is:

```text
skills/route/
├── SKILL.md
└── references/
    ├── governed-lifecycle-routing.md
    ├── bounded-workflow-automation.md
    └── boundary-first-method-v1.md
```

The exact final disclosure split may consolidate a reference when measured content no longer warrants it, but the package contains no guide authoring reference, workflow-guide skeleton, guide predicate, guide assembly, or `docs/workflows.md` fallback.

`SKILL.md` owns invocation classification, source precedence, semantic route judgment, stage ownership, isolation, stop/continue claims, and resource triggers. Governed routing loads authoritative CLI context. Automation loads the automation reference only for an armed, resumable, status, cancellation, or bootstrap invocation. Portable direct use without governed CLI context may use an explicit user target or a safe published portable default, but it cannot claim governed lifecycle state or project-local customization.

### Lifecycle compatibility boundary

The public package name changes, not the v3 stage graph or stored schema. `route` supplies `stage_authority: workflow` for workflow-owned lifecycle operations. Existing `workflow.automation` state is interpreted unchanged and becomes resumable by `route`; occurrence, target, budgets, receipts, and authorization identity stay exact.

Current adapter manifests, generated archives, installer metadata, skill indexes, and documentation name `route`. Validation rejects a current package containing both names, only `workflow`, or guide-only resources. Upgrade and installation diagnostics identify `workflow -> route`. Historical release archives and Git history remain immutable.

### Governed artifact ownership

The CLI resolves locations and structural permission only. The selected stage skill writes its own artifact and asks the lifecycle CLI to register or settle it. Route writes only workflow-owned request/evidence surfaces and never uses location resolution to acquire another stage's authority.

## Runtime View

### Start or resume routing

1. Route classifies the user's request as portable, governed, or bounded automation intent.
2. For governed work it calls project-phase `workflow-context` if exact change identity is not already authoritative.
3. If several candidates remain, route uses explicit user intent and semantic evidence to select one; unresolved ambiguity stops.
4. Route calls change-phase context for the exact identity.
5. It interprets blockers and engineering meaning, chooses one structurally allowed owning stage or stops, and invokes that stage without authoring its artifact.

### Correction routing

The CLI exposes current findings, settled packages, active correction state, and legal operations. Route decides whether a finding belongs to proposal, spec, architecture, plan, implementation, review, CI, or external evidence. It then submits the existing workflow-authorized correction operation. The CLI validates the choice but never originates it.

### Active automation after rename

Route reads the existing `workflow.automation` projection, proves the exact occurrence and target, and resumes with unchanged receipts and budgets. No state rewrite occurs merely to rename the skill. A stale installed `workflow` package cannot continue under a current adapter manifest and is directed to install/use `route`.

### Configuration failure

Malformed, unknown, escaped, contradictory, or incomplete configuration returns a deterministic blocker with the offending repository-relative config path and no guessed fallback. Route surfaces the blocker and stops; it does not reconstruct paths from deleted Markdown or memory.

### Guide retirement

Implementation removes the current `docs/workflows.md` file and its canonical references in the same coherent package migration. If a downstream repository retains that filename, current CLI and route ignore it. It remains ordinary documentation with no RigorLoop authority.

## Deployment View

The capability ships in the existing Node package and generated adapter archives. It adds no service, daemon, database, network dependency, credential, or telemetry. The release unit includes CLI code, bundled defaults, optional config schema, route skill, validators, docs, fixtures, adapter manifests, and release metadata.

Activation is atomic at the release-package level: current supported packages must agree on `route`, CLI context version, configuration schema, and absence of workflow-guide resources. Before publication rollback restores the prior coherent package. After users create repository configuration or resume through the new package, recovery is a corrective release; historical archives remain unchanged.

## Crosscutting Concepts

### Authority

CLI owns deterministic interpretation and guarded mutation. Route owns semantic selection and continuation. Stage skills own their artifacts. Review peers own verdicts. The stable `workflow` authority token names the lifecycle role, not a public package.

### Traceability

Context paths and identities point to Git-tracked proposal, design, Delivery, review, implementation, and verification evidence. The context projection is derived and does not become a second durable state store.

### Determinism and freshness

Every change-phase result binds the current lifecycle revision and exact artifact identities. A mutation uses the existing optimistic-concurrency request boundary. Re-reading context is required after mutation or observed drift.

### Security and privacy

Configuration and output use repository-relative paths and bounded identifiers. Absolute paths, path escape, symlink traversal, secrets, environment dumps, credentials, and arbitrary executable configuration are rejected or omitted.

### Progressive disclosure and token economy

The project phase is bounded, the change phase returns normalized facts once, and specialized automation guidance loads only when triggered. Route no longer reads a generated workflow guide or searches multiple files to reconstruct deterministic placement.

### Validation

Deterministic validation owns schema, vocabulary, path safety, source provenance, result shape, package inventory, generated parity, and stale-name diagnostics. Semantic review owns whether route selected the correct stage and whether package guidance preserves authority.

## Architecture Decisions

- [ADR-20260902 Route Context and Skill Identity](../adr/ADR-20260902-route-context-and-skill-identity.md) — adopts the two-phase read-only context projection, bundled defaults plus optional `rigorloop.workflow.yaml`, a clean public skill rename, and stable stored workflow protocol names.
- [ADR-20260824 Governed Lifecycle CLI Transaction Boundary](../adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md) — retained for state interpretation, semantic mutation, freshness, and transaction ownership.
- [ADR-20260825 Workflow-Routed Correction and Artifact Ownership](../adr/ADR-20260825-workflow-routed-correction-and-artifact-ownership.md) — retained; `route` exercises the workflow authority and the CLI validates but does not select corrections.

## Quality Requirements

| Quality | Scenario | Measure |
| --- | --- | --- |
| correctness | several changes are active | project context returns candidates and no chosen change; route must select or stop |
| safety | config contains an unknown kind or escaped path | explicit failure occurs before fallback or lifecycle interpretation |
| continuity | v3 automation was armed before the rename | route resumes the same occurrence without lifecycle migration or receipt loss |
| efficiency | governed route context is requested | one bounded CLI result replaces workflow-guide parsing and repository path guessing |
| explainability | a human requests context | output names effective sources, stage, blockers, allowed operations, and resolved paths |
| package coherence | adapters are generated or installed | exactly `route` and its mapped resources exist; stale `workflow` inventory is diagnosed |
| authority | two transitions are structurally allowed | CLI reports both; route alone chooses the semantically correct one |

## Risks and Technical Debt

- A dedicated config file adds one repository surface. Closed schema, optional use, bundled defaults, and provenance output keep it bounded.
- The stable `workflow` authority token may initially look inconsistent with the `route` name. Documentation must explicitly distinguish protocol role from public package identity; renaming stored values is deferred until it has independent value.
- Hosts may reject `$workflow` before RigorLoop can render its own diagnostic. Install/upgrade diagnostics and release migration notes provide the deterministic supported path, while no alias avoids indefinite dual naming.
- CLI context could grow into a semantic router. Contract tests must prove it reports candidates and permissions without choosing correction ownership or next-stage meaning.
- Removing `docs/workflows.md` invalidates several earlier current contracts. Implementation must amend or supersede their current clauses coherently rather than leaving contradictory validation active.

## Glossary

- **Route:** the public skill that owns semantic workflow routing and bounded orchestration.
- **Workflow authority:** the stable lifecycle protocol role used by route-owned mutations.
- **Workflow context:** a read-only CLI projection of deterministic project and selected-change facts.
- **Bundled default:** a versioned artifact-location rule shipped with the CLI.
- **Repository override:** an optional supported value in root `rigorloop.workflow.yaml`.
- **Portable mode:** skill use without a governed CLI context; it grants no governed lifecycle claim.

## Next artifacts

- Specification reconciliation.
- Design Review of this architecture, the ADR, and the specification as one exact package.

## Follow-on artifacts

- None yet.

## Readiness

The architecture and ADR are ready for specification reconciliation. They do not authorize implementation until the exact Design package is approved.
