---
name: architecture-review
description: >
  Review a proposed architecture/design before execution planning. Use for cross-component, hard-to-reverse, data, security, performance, migration, or long-lived design decisions.
argument-hint: [architecture doc path, ADR path, or feature name]
---

# Architecture review

This entrypoint is pre-cutover only. At consolidated-gates cutover, `design-review` replaces it as progression authority over the exact architecture/specification/ADR package. Historical Architecture Review evidence remains readable but this skill is not an alias for Design Review.

Act as an independent staff-level reviewer. Challenge safety, explainability, specification alignment, and readiness without editing the reviewed artifacts.

## Workflow role

Review the exact architecture subject and write only authorized review evidence and settlement state. Workflow owns routing. Do not claim authoring, workflow continuation, plan readiness, implementation readiness, verification, branch readiness, or PR readiness.

## Inputs and evidence

Read the exact target and the governing spec and review, architecture assessment, accepted decision basis, architecture method, repository revision, canonical package, diagrams, ADRs, project map, research, interfaces, schemas, and legacy evidence needed for the selected surface. Use summary and stable-ID first reasoning; prefer check IDs, requirement IDs, file paths, and line citations.

Tracked authority is required for a clean formal result. Missing authority may support a finding; use `inconclusive` only when it prevents both a credible clean result and an actionable finding.

## When full-file read is required

Read the full file when the whole file is the review target, package consistency is in scope, bounded searches disagree, context changes the conclusion, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Review surface

Select exactly one surface before judgment:

- `canonical-architecture-update`: exact canonical package, diagrams, ADRs, and spec alignment.
- `ADR`: one durable decision and its canonical linkage.
- `no-architecture-impact-rationale`: exact rationale credibility; packaging, data or generated-output flow, deployment, adapters, cross-cutting quality, security, or durable decisions normally defeat no-impact.
- `proposal-or-spec-gap`: unresolved direction or behavior routed to its owning proposal or spec stage.

Do not invent an artifact for a record-only surface. Unknown, mixed, or ambiguous surface evidence stops before dependent judgment or mutation.

## Universal judgment

Check behavior and non-goals, impact, ownership, coupling, data, interfaces, runtime and failure handling, deployment, migration, compatibility, security, privacy, performance, operations, testability, complexity, durable decisions, and planning readiness. Load the package method for detailed C4, arc42, diagram, package, and ADR checks.

Use one status for the complete subject: `approved`, `changes-requested`, `blocked`, or `inconclusive`. Do not partially approve a combined subject; an unchanged `review-required` target remains unsettled.

Severity is exactly `blocker`, `material`, or `minor`. Every finding includes Finding, Location, Severity, and Recommendation. A material finding also includes stable Finding ID, Evidence, Required outcome, and Safe resolution path or a `needs-decision` rationale. Name affected target IDs. Every blocker scope is `review-occurrence`, `target-set`, or `target:<artifact-id>`; occurrence blockers permit no settlement.

## Loading and authority

Classify recording mode as `none`, `advisory-durable`, or `formal-lifecycle`; artifact settlement as `none` or `exact-target-set`; and execution as `manual` or `workflow-managed-automated`.

Only these combinations are valid: `none/none/manual`, `advisory-durable/none/manual`, `formal-lifecycle/none/manual`, `formal-lifecycle/exact-target-set/manual`, `formal-lifecycle/none/workflow-managed-automated`, and `formal-lifecycle/exact-target-set/workflow-managed-automated`.

Every unlisted, unknown, missing, mixed, or contradictory combination stops before durable writes, settlement, automation evidence, or handoff. Loading grants no authority. Manual execution remains isolated; workflow-managed automated execution returns control to workflow without routing.

Direct or review-only `architecture-review` requests remain isolated by default. Direct or review-only requests remain isolated by default. Durable recording applies to every formal review, explicit durable request, material finding, or `changes-requested`, `blocked`, or `inconclusive` result.

## Requirement-fidelity manual opt-in

Manual reviews may voluntarily apply the requirement-fidelity gate and record a fidelity receipt. Mandatory manual-review applicability classification is out of first-slice scope.

## Procedural assemblies

- `ARR0-core`: this file.
- `ARR0M-method`: this file plus package method.
- `ARR1-recorded`: this file plus recording procedure.
- `ARR1M-recorded-method`: this file plus both references.

Load each trigger at most once. A missing, unreadable, escaped, contradictory, stale, or mixed-version resource must stop before dependent judgment, recording, settlement, automation, or claim. The skill must not reconstruct missing procedure from memory.

## Isolation and Recording

Isolation governs handoff. Recording follows formal review triggers.

A direct or review-only request remains isolated by default: it does not automatically continue into downstream workflow stages.

Isolation does not suppress recording.

Every formal lifecycle review result must be recorded or explicitly blocked.

Use:

- `Recording status: recorded` when the required review evidence was created or updated.
- `Recording status: blocked` when the required review evidence could not be created or updated.

`not-required` is reserved for non-formal review-like requests outside the formal lifecycle review model.

For a clean review, create the lightweight review receipt required by the formal review recording spec and index it in `review-log.md`. Do not create an empty `review-resolution.md` solely for a clean review.

For material findings or blocking outcomes, create the required detailed review record and disposition artifacts.
Use a detailed review record for material or blocking review outcomes.

Material findings must include:

- Finding ID
- Severity
- Location
- Evidence
- Required outcome
- Safe resolution path, or `needs-decision` rationale

Do not merely tell the user that review artifacts should be created. Create or update them before final output, or report `Recording status: blocked` with the blocker and smallest next action.

For an isolated review with material findings, the final review output must state:

- no automatic downstream handoff
- material Finding IDs
- required review record path
- whether the record must be created before fixing or reconstructed
- whether owner decision is needed

## Stops and claims

Stop on ambiguous target or revision, conflicting authority, unsettled upstream direction, unsafe placement, failed required resources, or invalid identity, authority, lifecycle state, or retry basis. Preserve supported findings when recording is blocked. Approval covers only the exact subject; independent review stops after recording and separately authorized settlement.

## Resource map

- READ `references/architecture-package-review.md` for `canonical-architecture-update` and `ADR` before method judgment.
- READ `references/architecture-review-recording-and-settlement.md` exactly when durable recording is required, before recording or settlement.

## Expected output

Report Review surface, Review status, Recording status, Recording blocker, Review record, Review log, Review resolution, review subject, governing basis, targets and dispositions, settlement, findings, blockers, required updates, next stage, and claim limitations. Omit inapplicable fields; mark applicable unresolved fields blocked.
