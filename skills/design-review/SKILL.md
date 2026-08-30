---
name: design-review
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Independently review architecture, specification, applicable ADRs, and accepted proposal constraints as one design package before delivery planning. Use design-review for design coherence and package authority; use architecture and spec for authorship.
argument-hint: [change ID, design package, architecture path, or specification path]
---

# Design review

Judge whether separately authored architecture and specification form one coherent design. Review the exact package without editing its members.

## Purpose

Trace the approved IR-level direction into coherent SRs and architecture realization.

Approve or reject one explicit design package and preserve precise finding ownership.

## When to use

Use after architecture and specification have been reconciled and before plan or test-specification authoring relies on them.

## When not to use

Do not use to author architecture, specification, or ADR content; review implementation; verify final readiness; or infer package approval from historical artifact reviews.

## Workflow role

- role_name: design-review
- stage: review
- upstream: one architecture, one specification, applicable ADRs, accepted proposal evidence, and the accepted Proposal Review ID
- downstream: plan and test-specification authoring, author-owned correction, upstream proposal reconsideration, or isolated stop
- summary: Decide whether the exact design package is coherent and feasible.
- ownership: Write Design Review evidence and settle only the exact design package. Workflow owns routing.
- must_not_claim: component authorship, implementation authority, implementation correctness, final verification, branch readiness, or PR readiness

The reviewer does not edit architecture, specification, ADRs, proposal content, or routing state. Approval is package authority, never component-only approval.

## Quick operating guide

Use this skill to: review one exact architecture/specification package and its proposal constraints.

Read first: `change.yaml`, `context design-review`, every member path shown there, the accepted proposal evidence, and relevant prior findings.

Produce: one recorded package outcome, precise findings or a no-finding rationale, and an isolated or workflow-owned handoff.

Stop when: membership, upstream authority, evidence, independence, or lifecycle identity is missing, unsafe, stale, or contradictory.

Do not claim: implementation authorization, final readiness, or approval of only one member.

Next stage: workflow may route an approved package to plan and test-specification authoring; otherwise route named corrections or stop.

## Inputs to read

Resolve the governed change, then obtain the package with `rigorloop lifecycle context design-review --change <change-id> --format json`. Read the complete architecture, specification, every applicable ADR, accepted proposal evidence, and the accepted Proposal Review ID named by the context. Read project governance and prior review or resolution evidence only when they affect the judgment.

The package member map must show stable artifact IDs and exact normalized repository-relative paths in this order: architecture, specification, then applicable ADR entries ordered by artifact ID. Do not calculate or request aggregate revisions or content hashes.

## Review contract

Evaluate all of the following as one decision:

1. The architecture can support every specified behavior and failure outcome.
2. The specification respects real technical, authority, compatibility, migration, security, and operational constraints.
3. Architecture does not weaken an accepted proposal goal for implementation convenience.
4. System, data, ownership, trust, recovery, and external boundaries are explicit and mutually consistent.
5. Applicable ADRs are included and agree with the architecture and specification.
6. Contradictions are resolved enough for safe delivery planning.

Use exactly one outcome: `approved`, `changes-requested`, `blocked`, or `inconclusive`. Only `approved` authorizes plan and test-specification authoring. Every other outcome grants no progression authority.

## Findings and ownership

Every material finding uses exactly one scope:

- `artifact-local`: name exactly one member artifact ID and its owning authoring stage.
- `cross-artifact`: name at least two affected artifact IDs and every authoring stage needed for reconciliation.
- `upstream-direction`: name the proposal or accepted proposal direction that must be reconsidered.

Each finding records a stable Finding ID, Severity, Location, Evidence, Required outcome, Safe resolution path or `needs-decision` rationale, finding scope, affected artifact IDs, and owning stages. Copy the finding asset once per material finding. Review resolution does not replace a required current Design Review after package members change.

## Isolation and recording

A direct or review-only invocation remains isolated by default. It records required evidence and may settle the exact package, but it does not route downstream. Workflow-managed continuation returns control to workflow after settlement.

Every formal result must be recorded or explicitly blocked. Clean review uses a lightweight receipt and review-log entry. Material or blocking results use a detailed record and `review-resolution.md` when disposition is required. Do not create an empty `review-resolution.md` solely for a clean result.

## Package recording and settlement

Recording mode is `none`, `advisory-durable`, or `formal-lifecycle`. Settlement is `none` or `exact-package`. Only formal lifecycle review may settle, and loading the procedure grants no authority.

For a formal review, load the mapped procedure before any write or settlement claim. `record-package-review` records the exact current member map, accepted Proposal Review ID, review identity, outcome, findings, correction targets, and evidence path. `settle-review-package` revalidates and atomically settles that same package. Settlement never advances workflow.

## Outputs

Produce the package identity, upstream review ID, outcome, findings, correction targets, recording and settlement results, blockers, next owner, and claim limits.

## Handoff

An approved workflow-managed review returns to workflow for plan and test-specification authoring. `changes-requested` routes each named artifact-local or cross-artifact correction to its owning authoring stage. `blocked` routes only to the named upstream owner. `inconclusive` stops for missing evidence. Direct review remains isolated.

## Stop conditions

Stop on incomplete or unsafe member maps, missing applicable ADR evidence, stale lifecycle revision, wrong upstream review ID, self-review or reviewer-authored member changes, unresolved direction, failed recording, or an owner decision. Preserve supported findings even when settlement blocks.

## Claims this skill must not make

Do not claim that architecture or specification is independently approved, that implementation is authorized, that reviewed content was fixed, or that verification, branch, PR, release, or deployment readiness exists.

## Resource map

- READ `references/requirement-to-delivery-model.md` when tracing proposal direction into system requirements and architecture realization.
- READ `references/boundary-first-method-v1.md` initially for every `design-review` invocation.
- READ `references/boundary-first-feature-authoring-v1.md` after the method reference when judging specification boundary completeness and example ownership.
- READ `references/design-review-recording-and-settlement.md` for every durable or formal review before recording or settlement.
- COPY `assets/review-result-skeleton.md` when producing every result. Omit inapplicable groups and unfilled placeholders.
- COPY `assets/material-finding.md` when a material finding exists, once per finding.

## Evidence collection efficiency

Use exact member IDs, paths, requirement IDs, ADR IDs, findings, and targeted excerpts before broad scans. Expand only when the package cannot be judged from bounded evidence.

## When full-file read is required

Read every package member in full because the review decides cross-artifact coherence. Read other files in full only when bounded evidence is insufficient or surrounding context changes the conclusion.

## Output skeleton

```md
COPY `assets/review-result-skeleton.md` when producing the review result.
COPY `assets/material-finding.md` when a material finding exists.
Fill <every applicable result and finding field> and do not emit unfilled placeholders.
```

## Expected output

Copy the result asset and each required finding asset. Report unavailable required data as blocked; do not invent package members, authority, or evidence.
