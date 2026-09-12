---
name: design-review
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Independently assess the exact affected Designs, scoped legacy members, examples and interactions against approved direction before delivery planning. Use design-review for design coherence and package authority; use design for authorship.
argument-hint: [change ID, affected Design package, or authorized legacy amendment]
---

# Design review

## Test criteria application

When the project explicitly adopts Test-model criteria, use the selectively loaded guidance below for test quality and maintenance. These criteria replace source-local shared test-purpose, case-selection and maintenance criteria for adopted work; retain specialist methods and historical evidence. Actual judgments, evidence applicability and closeout consequences remain with the responsible assessors under the project's review policy.

## Review and Closeout application

When project authority explicitly adopts Review and Closeout policy, use the packaged application below for shared assessment meaning. It replaces source-local judgment, independence, applicability, concern-disposition and closeout rules in this skill and its conditional resources; retain specialist methods and contract-selected storage procedures. Historical assessments retain their original meaning but grant no current runtime support. Missing or contradictory required guidance stops dependent reliance.

## Explicit recording

Use this profile when the project has adopted the RigorLoop Record Format and explicitly selected the change. Read the project's governing documents. The Workflow model owns coordination, Review and Closeout owns assessment policy, Record Format owns stored shapes, and CLI owns construction and persistence. Current storage uses `rigorloop-records-v3`; historical stores remain unchanged archival evidence. Select the actual record contract; never mix versions within a store. Retired or unknown stored formats are rejected without fallback. Do not migrate or reinterpret historical records; preserve their bytes and meaning as archival evidence. The project need not contain RigorLoop's internal design repository.

Use the contract-selected recording procedures in this skill and its conditional resources. Dispatch primary results by schema_version (2 or 3), then status and operation; a schema-3 error alone does not establish v3 storage. Read scope and omissions before relying on selected content. Retain substantive stage duties, permissions, independent assessment and proof obligations. Historical records grant no current execution authority.

Use `rigorloop context --root PATH --change ID --input - --format json` with explicitly selected kinds/filters and full detail. Expand the selection when needed: omitted content is not evidence of absence. Copy `record_contract` and `revision` into the targeted request's `contract` and `expected_revision`. Use `rigorloop subject inspect --root PATH --path FILE --content full --format json` for the exact engineering basis and mechanical identities; supply relied-on subjects as `reads` with their expected identities.

Make your decision, then use the purpose-specific command's `--help` and submit its targeted operation on stdin. Use `batch` for related explicit updates. Supply semantic values and any required applicability; the CLI constructs registry entries, preserves neighbors and serializes records. Do not reconstruct complete files or invoke historical eligibility first. Preview is optional; normal writes validate. A save does not approve work, establish readiness or select the next actor. Conflict requires rereading and reassessment; busy/recovery-required is not a save. Use explicit `record-store recover` for interrupted storage. Missing or stale evidence prevents reliance, not recording a correction.

Inspect the exact model package and engineering basis, including cross-model ownership and approved proposal bounds. Use review record for your independent complete judgment; use finding add/set for exact findings and dispositions. Preserve unresolved origins when a later assessment changes. Explicit applicability is your decision, not a consequence of matching hashes. Role labels do not authenticate independence.

Judge whether required behavior, technical realization, important decisions and representative acceptance intent form one coherent engineering contract across the affected owners. Review the exact package without editing its members.

## Purpose

Trace the approved IR-level direction into coherent requirements and their Design realization.

Approve or reject one explicit design package and preserve precise finding ownership.

## When to use

Use after the affected owning Designs and relevant interactions have been reconciled and before plan authoring relies on them.

## When not to use

Do not use to author architecture, specification, or ADR content; review implementation; verify final readiness; or infer package approval from historical artifact reviews.

## Workflow role

- role_name: design-review
- stage: review
- upstream: the exact affected models, scoped legacy members, relied-on examples, relevant interactions and accepted proposal evidence
- downstream: plan authoring, author-owned correction, upstream proposal reconsideration, or isolated stop
- summary: Decide whether the exact design package is coherent and feasible.
- ownership: Write Design Review evidence and settle only the exact design package. Route owns semantic routing.
- must_not_claim: component authorship, implementation authority, implementation correctness, final verification, branch readiness, or PR readiness

The reviewer does not edit architecture, specification, ADRs, proposal content, or routing state. Approval is package authority, never component-only approval.

## Quick operating guide

Use this skill to: review one exact owning Design package and its proposal constraints.

Read first: `change.json`, scoped `rigorloop context`, every member path shown there, the accepted proposal evidence, and relevant prior findings.

Produce: one recorded package outcome, precise findings or a no-finding rationale, and an isolated or route-owned handoff.

Stop when: membership, upstream authority, evidence, independence, or lifecycle identity is missing, unsafe, stale, or contradictory.

Do not claim: implementation authorization, final readiness, or approval of only one member.

Next stage: `route` may send an approved package to plan authoring; otherwise route named corrections or stop.

## Inputs to read

Resolve the governed change, then obtain the package with the scoped primary context and exact subject inspection described above. Read each complete affected model and scoped legacy member, relied-on examples, relevant shared-contract owners and interactions, and accepted proposal evidence and accepted Proposal Review ID identified by the context. Expand for material missing or contradictory evidence; a whole-repository load is not the default. Read project governance and prior review or resolution evidence only when they affect the judgment.

The package member map identifies each affected owner and its exact path/subject, including retained legacy contracts and relied-on examples. Use an explicit stable order appropriate to that selected set; no fixed architecture/specification/ADR tuple is required. Use CLI subject inspection for exact identities; do not calculate an aggregate package revision.

## Review contract

Evaluate all of the following as one decision:

1. Technical realization can support each required behavior, invariant and failure outcome.
2. Required behavior respects real technical, authority, compatibility, migration, security and operational constraints.
3. A material feasibility constraint has not silently weakened an approved goal for implementation convenience.
4. System, data, ownership, trust, recovery, and external boundaries are explicit and mutually consistent.
5. Important decisions retain identity, context, alternatives and consequences, with one current owner. Applicable historical/legacy ADRs retain their original meaning.
6. Shared contracts have one owner, affected consumers are reconciled, and system-wide obligations reference component contracts without overriding them.
7. Important claims have credible assessment/feasibility bases, visible assumptions and representative local/integrated outcomes from which Delivery can derive concrete proof. Structural success alone is not approval.
8. Migration maps preserve each displaced obligation and decision, retire only the approved selected authorities, and assign remaining consolidation. Scoped legacy amendments retain their format without forced migration.

Apply the packaged assessment rule when adopted; approval covers this exact package for authorized plan authoring. Under historical contracts, use exactly one outcome: `approved`, `changes-requested`, `blocked`, or `inconclusive`; only approved package evidence permits reliance for plan authoring. Recording is not permission.

Assess examples alongside their owner and exact identity. Check parse/schema limits and illustrated before/after invariants separately from review applicability. If a relied-on example changed while the parent stayed unchanged, require its new exact subject in selection/handoff; prior parent or example approval is insufficient for current reliance without the required reassessment. Mechanical selection does not decide applicability or create automatic invalidation.

Representative scenarios are not a test whitelist. Apply adopted Test criteria to derived obligations and hazards and existing review policy to actual assessment/current reliance. Preserve required regression protection.

## Findings and ownership

Every material finding uses exactly one scope:

- `artifact-local`: name exactly one member artifact ID and its owning authoring stage.
- `cross-artifact`: name at least two affected artifact IDs and every authoring stage needed for reconciliation.
- `upstream-direction`: name the proposal or accepted proposal direction that must be reconsidered.

Each finding records a stable Finding ID, Severity, Location, Evidence, Required outcome, Safe resolution path or `needs-decision` rationale, finding scope, affected artifact IDs, and owning stages. Copy the finding asset once per material finding. Review resolution does not replace a required current Design Review after package members change.

## Isolation and recording

Recording mode is `none`, `advisory-durable`, or `formal-lifecycle`. Load the mapped procedure before durable recording. Use the contract-selected `review record` and finding operations with exact subjects, judgment, rationale and explicit applicability. Record supported non-approvals without requiring eligibility. There is no separate legacy settlement operation; successful recording does not advance workflow or grant authority. Isolated advisory assessments need no lifecycle artifacts.

## Outputs

Produce the package identity, upstream review ID, outcome, findings, correction targets, recording results and current applicability, blockers, next owner, and claim limits.

## Handoff

An approved workflow-managed review returns to `route` for plan authoring. `changes-requested` routes each named artifact-local or cross-artifact correction to its owning authoring stage. `blocked` routes only to the named upstream owner. `inconclusive` stops for missing evidence. Direct review remains isolated.

## Stop conditions

Stop on incomplete or unsafe member maps, missing applicable ADR evidence, stale record revision, wrong upstream review ID, self-review or reviewer-authored member changes, unresolved direction, failed recording, or an owner decision. Preserve supported findings even when reliance or recording is blocked.

## Claims this skill must not make

Do not claim that architecture or specification is independently approved, that implementation is authorized, that reviewed content was fixed, or that verification, branch, PR, release, or deployment readiness exists.

## Resource map

- READ `references/test-quality.md` when adopted criteria apply and this invocation authors, allocates or assesses test obligations.

- READ `references/review-reliance.md` when applying adopted assessment applicability, correction or closeout policy.
- READ `references/review-assessment.md` for every review under explicitly adopted Review and Closeout policy.

- READ `references/requirement-to-delivery-model.md` when tracing proposal direction into system requirements and architecture realization.
- READ `references/boundary-first-method-v1.md` when the selected legacy contract has boundary records or a relied-on boundary identity needs interpretation.
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
