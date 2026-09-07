---
name: design-review
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Independently review architecture, specification, applicable ADRs, and accepted proposal constraints as one design package before delivery planning. Use design-review for design coherence and package authority; use architecture and spec for authorship.
argument-hint: [change ID, design package, architecture path, or specification path]
---

# Design review

## Review and Closeout application

When project authority explicitly adopts Review and Closeout policy, use the packaged application below for shared assessment meaning. It replaces source-local judgment, independence, applicability, concern-disposition and closeout rules in this skill and its conditional resources; retain specialist methods and contract-selected storage procedures. Historical contracts retain their own rules. Missing or contradictory required guidance stops dependent reliance.

## Explicit recording

Use this profile when the project has adopted the RigorLoop Record Format and explicitly selected the change. Read the project's model documents; The Workflow domain owns decision meaning (Review and Closeout owns adopted assessment policy), the Record Format model owns stored shapes, and the CLI model owns construction and persistence. New primary roots require `rigorloop-records-v2`; existing `explicit-recording-v1` roots retain their exact compatibility contract. Do not migrate an existing root. Unknown contracts stop without fallback.

This profile replaces historical package, transition, recording and output-shape procedures below, including their conditional resources. Retain substantive stage duties, permissions, independent assessment and proof obligations; historical contracts keep their own procedures.

Use `rigorloop context --root PATH --change ID --input - --format json` with explicitly selected kinds/filters and full detail. Expand the selection when needed: omitted content is not evidence of absence. Copy `record_contract` and `revision` into the targeted request's `contract` and `expected_revision`. Use `rigorloop subject inspect --root PATH --path FILE --content full --format json` for the exact engineering basis and mechanical identities; supply relied-on subjects as `reads` with their expected identities.

Make your decision, then use the purpose-specific command's `--help` and submit its targeted operation on stdin. Use `batch` for related explicit updates. Supply semantic values and any required applicability; the CLI constructs registry entries, preserves neighbors and serializes records. Do not reconstruct complete files or invoke historical eligibility first. Preview is optional; normal writes validate. A save does not approve work, establish readiness or select the next actor. Conflict requires rereading and reassessment; busy/recovery-required is not a save. Use explicit `record-store recover` for interrupted storage. Missing or stale evidence prevents reliance, not recording a correction.

Inspect the exact model package and engineering basis, including cross-model ownership and approved proposal bounds. Use review record for your independent complete judgment; use finding add/set for exact findings and dispositions. Preserve unresolved origins when a later assessment changes. Explicit applicability is your decision, not a consequence of matching hashes. Role labels do not authenticate independence.

Judge whether separately authored architecture and specification form one coherent design. Review the exact package without editing its members.

## Purpose

Trace the approved IR-level direction into coherent SRs and architecture realization.

Approve or reject one explicit design package and preserve precise finding ownership.

## When to use

Use after architecture and specification have been reconciled and before plan authoring relies on them.

## When not to use

Do not use to author architecture, specification, or ADR content; review implementation; verify final readiness; or infer package approval from historical artifact reviews.

## Workflow role

### Compact current-state contract

For `compact-current-state-v1`, consume the bounded CLI projection and exact design-package paths. Update one stable current review record for the design package through a transient CLI operation. Keep open findings in that record and retain only continuing material constraints in `material-decisions.md`. A changes-requested outcome returns to the exact authoring owner; a clean exact rereview approves the package. Do not create round-suffixed reviews, `review-log.md`, `review-resolution.md`, request files, or correction receipts.

- role_name: design-review
- stage: review
- upstream: one architecture, one specification, applicable ADRs, accepted proposal evidence, and the accepted Proposal Review ID
- downstream: plan authoring, author-owned correction, upstream proposal reconsideration, or isolated stop
- summary: Decide whether the exact design package is coherent and feasible.
- ownership: Write Design Review evidence and settle only the exact design package. Route owns semantic routing.
- must_not_claim: component authorship, implementation authority, implementation correctness, final verification, branch readiness, or PR readiness

The reviewer does not edit architecture, specification, ADRs, proposal content, or routing state. Approval is package authority, never component-only approval.

## Quick operating guide

Use this skill to: review one exact architecture/specification package and its proposal constraints.

Read first: `change.yaml`, `context design-review`, every member path shown there, the accepted proposal evidence, and relevant prior findings.

Produce: one recorded package outcome, precise findings or a no-finding rationale, and an isolated or route-owned handoff.

Stop when: membership, upstream authority, evidence, independence, or lifecycle identity is missing, unsafe, stale, or contradictory.

Do not claim: implementation authorization, final readiness, or approval of only one member.

Next stage: `route` may send an approved package to plan authoring; otherwise route named corrections or stop.

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

Apply the packaged assessment rule when adopted; approval covers this exact package for authorized plan authoring. Under historical contracts, use exactly one outcome: `approved`, `changes-requested`, `blocked`, or `inconclusive`; only approved package evidence permits reliance for plan authoring. Recording is not permission.

## Findings and ownership

Every material finding uses exactly one scope:

- `artifact-local`: name exactly one member artifact ID and its owning authoring stage.
- `cross-artifact`: name at least two affected artifact IDs and every authoring stage needed for reconciliation.
- `upstream-direction`: name the proposal or accepted proposal direction that must be reconsidered.

Each finding records a stable Finding ID, Severity, Location, Evidence, Required outcome, Safe resolution path or `needs-decision` rationale, finding scope, affected artifact IDs, and owning stages. Copy the finding asset once per material finding. Review resolution does not replace a required current Design Review after package members change.

## Isolation and recording

The following recording and settlement procedure applies to historical profiles only. Adopted Review and Closeout assessments use the packaged application and their selected recording interface.

A direct or review-only invocation remains isolated by default. It records required evidence and may settle the exact package, but it does not route downstream. Workflow-managed continuation returns control to `route` after settlement.

Every formal result must be recorded or explicitly blocked. For registered historical contracts, clean review uses a lightweight receipt and review-log entry, while material or blocking results use a detailed record and triggered `review-resolution.md`. Compact results update the stable current review and conditional material-decision surface described above.

## Package recording and settlement

The following recording and settlement procedure applies to historical profiles only. Adopted Review and Closeout assessments use the packaged application and their selected recording interface.

Recording mode is `none`, `advisory-durable`, or `formal-lifecycle`. Settlement is `none` or `exact-package`. Only formal lifecycle review may settle, and loading the procedure grants no authority.

For a formal review, load the mapped procedure before any write or settlement claim. `record-package-review` records the exact current member map, accepted Proposal Review ID, review identity, outcome, findings, correction targets, and evidence path. `settle-review-package` revalidates and atomically settles that same package. Settlement never advances workflow.

## Outputs

Produce the package identity, upstream review ID, outcome, findings, correction targets, recording and settlement results, blockers, next owner, and claim limits.

## Handoff

An approved workflow-managed review returns to `route` for plan authoring. `changes-requested` routes each named artifact-local or cross-artifact correction to its owning authoring stage. `blocked` routes only to the named upstream owner. `inconclusive` stops for missing evidence. Direct review remains isolated.

## Stop conditions

Stop on incomplete or unsafe member maps, missing applicable ADR evidence, stale lifecycle revision, wrong upstream review ID, self-review or reviewer-authored member changes, unresolved direction, failed recording, or an owner decision. Preserve supported findings even when settlement blocks.

## Claims this skill must not make

Do not claim that architecture or specification is independently approved, that implementation is authorized, that reviewed content was fixed, or that verification, branch, PR, release, or deployment readiness exists.

## Resource map

- READ `references/review-reliance.md` when applying adopted assessment applicability, correction or closeout policy.
- READ `references/review-assessment.md` for every review under explicitly adopted Review and Closeout policy.

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
