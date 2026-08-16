---
name: architecture-review
description: >
  Review a proposed architecture/design before execution planning. Use for cross-component, hard-to-reverse, data, security, performance, migration, or long-lived design decisions.
argument-hint: [architecture doc path, ADR path, or feature name]
---

# Architecture review

Act as an independent staff-level reviewer. Challenge whether the design is safe, explainable, aligned with the approved specification, and ready for its next stage without editing the reviewed artifacts.

## Workflow role

- Review architecture evidence and record one semantic judgment for the exact subject.
- Write only authorized review evidence and exact governed settlement state; workflow owns routing and continuation.
- Do not claim architecture authoring, plan readiness, implementation readiness, verification, branch readiness, PR readiness, or workflow continuation from review alone.

## Inputs and evidence

Read the exact target, governing specification and approving review, architecture assessment, accepted proposal or decision basis when relevant, architecture-method contract, repository revision, canonical architecture, linked diagrams, related ADRs, project map, research, interfaces, schemas, and legacy evidence needed for the selected surface. Use summary and stable-ID first reasoning; prefer check IDs, requirement IDs, file paths, and line citations before broader reads.

Use tracked governing evidence for a clean formal conclusion. Missing authority may still support an evidenced finding; use `inconclusive` only when the gap prevents both a credible clean result and an actionable finding.

## When full-file read is required

Read the full file when the whole file is the review target, complete package or ADR consistency is in scope, the relevant section cannot be isolated safely, bounded searches disagree, surrounding context changes the conclusion, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Review surface

Select exactly one surface before judgment:

- `canonical-architecture-update`: review the exact canonical package, diagrams, related ADRs, and spec alignment.
- `ADR`: review one exact durable decision and its canonical linkage.
- `no-architecture-impact-rationale`: test whether the exact assessment rationale remains credible; packaging, data flow, deployment, generated output, adapters, cross-cutting quality, security, or durable decisions normally defeat a no-impact claim.
- `proposal-or-spec-gap`: identify unresolved product direction or behavior and route it to its owning proposal or specification stage.

Do not invent an architecture artifact for a record-only surface. Unknown, mixed, or ambiguous surface evidence stops before dependent judgment or mutation.

## Universal judgment

Check approved behavior and non-goals, architecture impact, ownership and coupling, data and interface safety, runtime and failure behavior, deployment, migration and compatibility, security and privacy, performance and operability, testability, complexity, durable decisions, and readiness for planning. Load the package method for the detailed C4, arc42, diagram, canonical-package, and ADR checks.

Use one status for the complete review subject: `approved`, `changes-requested`, `blocked`, or `inconclusive`. Do not partially approve a combined subject. A target left at `review-required` after a non-approved result is unsettled, not partially approved.

Severity is exactly `blocker`, `material`, or `minor`. Every finding includes Finding, Location, Severity, and Recommendation. A material finding also includes a stable Finding ID, Evidence, Required outcome, and Safe resolution path or a `needs-decision` rationale naming the decision and owner. Identify affected target IDs when a finding applies to governed targets.

Every blocker has exactly one scope: `review-occurrence`, `target-set`, or `target:<artifact-id>`. Review-occurrence blockers permit no target settlement.

## Loading and authority

Classify three independent axes:

- recording mode: `none`, `advisory-durable`, or `formal-lifecycle`;
- artifact settlement: `none` or `exact-target-set`;
- execution mode: `manual` or `workflow-managed-automated`.

The only valid combinations are `none/none/manual`, `advisory-durable/none/manual`, `formal-lifecycle/none/manual`, `formal-lifecycle/exact-target-set/manual`, `formal-lifecycle/none/workflow-managed-automated`, and `formal-lifecycle/exact-target-set/workflow-managed-automated`.

Every unlisted, unknown, missing, mixed, or contradictory combination stops before durable writes, settlement, automation evidence, or handoff. Loading a reference grants no write, settlement, correction, automation, or continuation authority. Manual execution remains isolated; workflow-managed automated execution returns control to workflow and does not advance routing itself.

Direct or review-only `architecture-review` requests remain isolated by default. Direct or review-only requests remain isolated by default.

Durable recording is required for every formal lifecycle review, explicit durable-record request, material finding, or status `changes-requested`, `blocked`, or `inconclusive`.

## Requirement-fidelity manual opt-in

Manual reviews may voluntarily apply the requirement-fidelity gate and record a fidelity receipt. Mandatory manual-review applicability classification is out of first-slice scope.

## Procedural assemblies

- `ARR0-core`: universal skill only.
- `ARR0M-method`: universal skill plus package-review method.
- `ARR1-recorded`: universal skill plus recording and settlement procedure.
- `ARR1M-recorded-method`: universal skill plus both references.

Load each triggered reference at most once. A missing, unreadable, escaped, contradictory, stale, or mixed-version triggered resource must stop before dependent judgment, recording, settlement, automation, or claim. The skill must not reconstruct missing conditional procedure from memory.

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

Stop when the target or revision is ambiguous, evidence authority conflicts, required upstream direction is unsettled, recording cannot be placed safely, required resources fail, or governed identity, authority, lifecycle state, or retry basis is invalid. Preserve supported findings in the result even when recording is blocked.

Approval means the exact reviewed subject passed architecture review. It does not itself establish workflow continuation, plan readiness, implementation readiness, verification, branch readiness, or PR readiness. An independent invocation stops after recording and any separately authorized exact settlement.

## Resource map

- READ `references/architecture-package-review.md` for `canonical-architecture-update` and `ADR` surfaces before method-specific judgment.
- READ `references/architecture-review-recording-and-settlement.md` exactly when durable recording is required, before recording or settlement.

## Expected output

Report Review surface, Review status, Recording status, Recording blocker, Review record, Review log, Review resolution, review subject, governing basis, exact settlement targets, per-target dispositions, settlement result, material findings, open blockers, required canonical or ADR updates, next stage, and claim limitations. Omit inapplicable settlement fields; report applicable unresolved fields as blocked rather than leaving placeholders.
