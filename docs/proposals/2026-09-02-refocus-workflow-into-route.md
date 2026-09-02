# Refocus Workflow into the Route Skill

## Challenge

The current `workflow` skill combines two materially different responsibilities: routing, resuming, auditing, and automating governed work; and creating, refreshing, and consuming `docs/workflows.md`. Routing dominates ordinary use, while guide authoring is infrequent and requires separate predicates, assemblies, resources, assets, conflict handling, and path-resolution fallbacks.

This split makes ordinary routing carry concepts it rarely needs and requires agents to reconstruct deterministic project facts from lifecycle state, skill rules, and a Markdown map. RigorLoop's v3 CLI lifecycle boundary can resolve those facts structurally. Agent reasoning should instead focus on semantic questions such as blocker meaning, correction ownership, and whether work should continue or stop.

## Goals

- Rename `workflow` to `route` so the public skill name matches its primary responsibility.
- Keep semantic routing, resumption, auditing, correction routing, and bounded automation in `route`.
- Make the CLI authoritative for deterministic project-local workflow context and artifact-location resolution.
- Eliminate `docs/workflows.md` as a RigorLoop lifecycle or routing artifact and remove guide authoring from the skill.
- Reduce skill complexity and agent context without moving semantic engineering judgment into the CLI.
- Preserve stage ownership, Git-tracked engineering evidence, and fail-closed lifecycle behavior.
- Update canonical documentation, validation, and generated public packages coherently.

## Scope and non-goals

The approved direction covers the following workstreams:

| Workstream | Scope budget treatment | Boundary |
| --- | --- | --- |
| Rename `workflow` to `route` and simplify its invocation model | core to this proposal | The current package makes a clean v3 break; no current `workflow` alias is retained. |
| CLI-derived deterministic workflow context | same-slice dependency | Design defines the command and result contract before the skill removes document fallback. |
| Governed routing and bounded automation guidance | core to this proposal | Semantic ownership remains in `route`. |
| Retire `docs/workflows.md` and guide-only resources | separate implementation slice | Historical copies remain ordinary documentation without RigorLoop authority. |
| Constitution, repository guidance, validation, and documentation updates | same-slice dependency | Current source-of-truth and contributor rules must agree at cutover. |
| Generated adapters and public invocation naming | separate implementation slice | Generated output derives from canonical `skills/` sources. |
| Existing active or resumable automation records | same-slice dependency | Design must preserve or explicitly stop them without silently reinterpreting state. |

This proposal does not move semantic routing ownership into the CLI, make the CLI an autonomous workflow engine, change stage-specific artifact ownership, redesign lifecycle stages, define exact commands or schemas, select the repository configuration format, introduce a hosted service, or retain `docs/workflows.md` as a generated compatibility artifact. Exact APIs, configuration inputs, migration mechanics, implementation sequencing, and proof allocation belong to Design and Delivery.

Historical `workflow` skill archives and completed records remain historical evidence. The current v3 package adopts `route` without a public `workflow` alias; downstream Design must define clear diagnostics for obsolete invocation names and safe handling of pre-cutover automation records.

## Governing principle

> Deterministic workflow facts should be resolved by the CLI; semantic workflow routing should remain owned by the route skill.

## Proposed direction

Replace the mixed skill with three explicit responsibility boundaries:

```text
CLI
├── deterministic lifecycle and automation state
├── effective project-local workflow information
├── artifact-location resolution
└── structurally allowed lifecycle operations

route skill
├── semantic routing and blocker interpretation
├── correction ownership and workflow resumption
├── workflow auditing
├── bounded automation orchestration
└── stop or continue judgment

stage skills
└── stage-specific artifacts and judgments
```

`route` asks the CLI for authoritative structured context and then decides which structurally permitted path matches the engineering situation. The CLI answers what is structurally true and permitted; `route` decides what the evidence means and which owner should act.

Bounded automation remains in `route` because correction classification, decision-basis impact, rereview requirements, and owner-judgment stops require semantic interpretation. The CLI supplies lifecycle facts, targets, receipts, and permitted operations without autonomously choosing the engineering route.

`docs/workflows.md`, `references/workflow-guide-authoring.md`, `assets/workflows-skeleton.md`, guide-specific invocation predicates and assemblies, and workflow-map fallbacks leave the current RigorLoop contract. If deterministic resolution is unavailable, the CLI returns a structured unresolved result and `route` stops rather than guessing from filenames, chat, or memory.

Engineering artifacts—including proposals, specifications, architecture, plans, reviews, implementation evidence, verification evidence, and change state—remain Git-native and repository-owned.

## Feasibility

**Assessment: feasible.** The current skill already isolates guide authoring behind dedicated predicates, assemblies, a reference, and an asset, so that responsibility can be removed cleanly. Routing, correction, auditing, and automation are already represented separately. The repository also ships a structured lifecycle CLI that reports contract authority, current stage, package status, blockers, artifact identities, and permitted operations.

The main constraint is sequencing: the CLI must expose every deterministic workflow fact currently supplied by the guide before `route` removes its fallbacks. Design must also settle configuration inputs and the treatment of pre-cutover automation. No conceptual blocker prevents Design, but implementation must cut over canonical skill text, CLI behavior, validators, documentation, and generated packages coherently.

## Impact and major trade-offs

The change removes a human-readable workflow map and creates a stronger runtime dependency on a compatible CLI. Human-oriented CLI output must therefore remain inspectable, and CLI failure or unresolved configuration will intentionally block governed routing.

The public skill rename is a compatibility-sensitive clean break in the current v3 package. Existing released archives remain immutable, but current documentation and adapters will no longer advertise or install `workflow`. This requires aligned Constitution and contributor-guidance changes and clear obsolete-invocation diagnostics.

`route` remains a substantial reasoning skill because semantic correction routing and bounded automation stay within it. The reduction comes from removing deterministic reconstruction and guide authoring, not from removing necessary judgment.

## Decision requested

Approve the direction to rename `workflow` to `route`; keep semantic routing, resumption, auditing, correction ownership, and bounded automation in `route`; make the CLI authoritative for deterministic project-local workflow context; eliminate `docs/workflows.md` and guide-specific behavior; preserve stage ownership and Git-native engineering evidence; adopt a clean current-v3 skill-name cutover without a `workflow` alias; and update governance, documentation, validation, and generated packages coherently.

Approval authorizes Architecture and Specification to define the CLI context boundary, configuration inputs, obsolete-invocation behavior, and active-automation transition. It does not approve exact commands, schemas, configuration formats, internal implementation, delivery sequencing, verification allocation, or release mechanics.
