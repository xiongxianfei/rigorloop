---
name: delivery-review
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Independently review one plan-centered delivery package before implementation. Judge safe sequencing and verification adequacy together; use plan for delivery and verification allocation and design for behavioral gaps.
argument-hint: [change ID, delivery package, or plan path]
---

# Delivery review

## Test criteria application

When the project explicitly adopts Test-model criteria, use the selectively loaded guidance below for test quality and maintenance. These criteria replace source-local shared test-purpose, case-selection and maintenance criteria for adopted work; retain specialist methods and historical evidence. Actual judgments, evidence applicability and closeout consequences remain with the responsible assessors under the project's review policy.

## Review and Closeout application

When project authority explicitly adopts Review and Closeout policy, use the packaged application below for shared assessment meaning. It replaces source-local judgment, independence, applicability, concern-disposition and closeout rules in this skill and its conditional resources; retain specialist methods and contract-selected storage procedures. Historical assessments retain their original meaning but grant no current runtime support. Missing or contradictory required guidance stops dependent reliance.

## Explicit recording

Use this profile when the project has adopted the RigorLoop Record Format and explicitly selected the change. Read the project's governing documents. The Workflow model owns coordination, Review and Closeout owns assessment policy, Record Format owns stored shapes, and CLI owns construction and persistence. Current storage uses `rigorloop-records-v3`; historical stores remain unchanged archival evidence. Select the actual record contract; never mix versions within a store. Retired or unknown stored formats are rejected without fallback. Do not migrate or reinterpret historical records; preserve their bytes and meaning as archival evidence. The project need not contain RigorLoop's internal design repository.

Use the contract-selected recording procedures in this skill and its conditional resources. Dispatch primary results by schema_version (2 or 3), then status and operation; a schema-3 error alone does not establish v3 storage. Read scope and omissions before relying on selected content. Retain substantive stage duties, permissions, independent assessment and proof obligations. Historical records grant no current execution authority.

Use `rigorloop context --root PATH --change ID --input - --format json` with explicitly selected kinds/filters and full detail. Expand the selection when needed: omitted content is not evidence of absence. Copy `record_contract` and `revision` into the targeted request's `contract` and `expected_revision`. Use `rigorloop subject inspect --root PATH --path FILE --content full --format json` for the exact engineering basis and mechanical identities; supply relied-on subjects as `reads` with their expected identities.

Make your decision, then use the purpose-specific command's `--help` and submit its targeted operation on stdin. Use `batch` for related explicit updates. Supply semantic values and any required applicability; the CLI constructs registry entries, preserves neighbors and serializes records. Do not reconstruct complete files or invoke historical eligibility first. Preview is optional; normal writes validate. A save does not approve work, establish readiness or select the next actor. Conflict requires rereading and reassessment; busy/recovery-required is not a save. Use explicit `record-store recover` for interrupted storage. Missing or stale evidence prevents reliance, not recording a correction.

Inspect the exact plan with the approved model package and assess safe sequencing, proof adequacy and closeout dependencies. Record your independent judgment with review record and findings with finding add/set, retaining unresolved origin. Do not change the plan or route work as review bookkeeping. Recorded role labels are attribution, not proof of independence.

Judge whether the approved design can be implemented safely and proved adequately through the exact primary plan. Review without editing the plan or approved design.

## Purpose

Trace SRs and architecture boundaries into proportional allocated work and proof.

Approve or reject one explicit plan-centered package in one independent decision covering implementation readiness and verification adequacy. Preserve requirement-to-proof traceability and precise finding ownership.

## When to use

Use after the execution plan has allocated the approved design's behavior, work, milestone verification, and applicable change-level verification, and before implementation.

## When not to use

Do not use to author the plan, repair specification behavior, redesign architecture, review implementation, execute final verification, or combine historical artifact-review evidence into package authority.

## Workflow role

- role_name: delivery-review
- stage: review
- upstream: one exact primary plan and the approved Design Review ID
- downstream: implementation, author-owned correction, upstream design reconsideration, or isolated stop
- summary: Decide whether the exact delivery package can implement and prove the approved design.
- ownership: Write Delivery Review evidence and settle only the exact delivery package. Route owns semantic routing.
- must_not_claim: plan or specification authorship, implementation completion, code-review, final verification, branch readiness, or PR readiness

The reviewer does not edit the execution plan, design package, implementation, or routing state. Approval judges the plan's sequence and verification together; it is never a partial sequencing-only or proof-only approval.

## Quick operating guide

Use this skill to: review one exact primary-plan package against the approved design.

Read first: `change.json`, scoped `rigorloop context`, the exact primary plan, the approved Design Review ID and member map, and relevant prior findings.

Produce: one recorded package outcome, precise findings or a no-finding rationale, and an isolated or route-owned handoff.

Stop when: membership, upstream authority, evidence, independence, or lifecycle identity is missing, unsafe, stale, or contradictory.

Do not claim: implementation completion, code correctness, or final readiness.

Next stage: `route` may send an approved package to implementation; otherwise route named corrections or stop.

## Inputs to read

Resolve the governed change, then obtain the package with the scoped primary context and exact subject inspection described above. Read the complete exact primary plan plus the approved Design Review ID and member map it operationalizes. Read current proposal constraints, the exact affected models and examples, applicable retained legacy contracts, and prior review or resolution evidence as needed to validate the trace.

For a governed delivery assessment, the package must identify exactly the registered primary-plan artifact ID and normalized repository-relative path. A standalone test-spec substitute or extra member is invalid. Historical packages remain readable but grant no current review or progression authority. Use CLI subject inspection for exact identities; do not calculate an aggregate package revision.

## Review contract

Evaluate implementation readiness and verification adequacy in the same decision. Check safe dependency order, acceptable intermediate states, milestone boundaries, migration sequence, reversibility, SR allocation, milestone verification, applicable change-level verification, important normal and negative scenarios, compatibility, migration, recovery, concurrency, security and authority concerns, and realistic evidence expectations.

Evaluate this exact trace for every applicable requirement and architecture risk:

`requirement -> architectural boundary -> implementation milestone -> required proof -> validation command or manual evidence`

Reject or request correction for missing SR allocation, unsafe or overly broad sequencing, unreviewable milestones, insufficient milestone or change-level verification, proof at the wrong boundary, architecture risk without validation, compatibility or migration work without evidence, unrealistic proof, and verification that requires a different implementation order than the plan. Milestone completion must not be treated as complete-change correctness. Under adopted policy, check the named final whole-change Code Review checkpoint and its implementation/correction dependencies separately from integrated proof groups, as required by the packaged closeout application.

Route the correction to `plan` when verification allocation is missing or inadequate; route missing observable behavior to `design`. Do not author the correction, accept a standalone test-spec substitute, or defer material pre-implementation coverage to final Verify.

Apply the packaged assessment rule when adopted; approval covers this exact package for authorized implementation. Under historical contracts, use exactly one outcome: `approved`, `changes-requested`, `blocked`, or `inconclusive`; only approved package evidence permits reliance for implementation. Recording is not permission.

## Findings and ownership

Every material finding uses exactly one scope:

- `artifact-local`: name exactly one plan artifact ID and its owning stage.
- `cross-artifact`: name the plan plus affected approved design artifact IDs and every authoring stage needed for reconciliation.
- `upstream-direction`: name the approved design package whose direction must be reconsidered.

Each finding records a stable Finding ID, Severity, Location, Evidence, Required outcome, Safe resolution path or `needs-decision` rationale, finding scope, affected artifact IDs, and owning stages. Copy the finding asset once per material finding. Review resolution does not replace a required current Delivery Review after package members change.

## Isolation and recording

Recording mode is `none`, `advisory-durable`, or `formal-lifecycle`. Load the mapped procedure before durable recording. Use the contract-selected `review record` and finding operations with exact subjects, judgment, rationale and explicit applicability. Record supported non-approvals without requiring eligibility. There is no separate legacy settlement operation; successful recording does not advance workflow or grant authority. Isolated advisory assessments need no lifecycle artifacts.

## Outputs

Produce the package identity, upstream review ID, traceability judgment, outcome, findings, correction targets, recording results and current applicability, blockers, next owner, and claim limits.

## Handoff

An approved workflow-managed review returns to `route` for implementation. `changes-requested` routes plan allocation gaps to `plan` and behavioral or design gaps to their named upstream owner. `blocked` identifies the necessary decision and its actual owner; this may be the plan or an upstream owner. `inconclusive` stops for missing evidence. Direct review remains isolated.

## Stop conditions

Stop on incomplete or unsafe member maps, missing or stale design authority, stale record revision, wrong upstream review ID, self-review or reviewer-authored member changes, unresolved proof feasibility, failed recording, or an owner decision. Preserve supported findings even when reliance or recording is blocked.

## Claims this skill must not make

Do not claim plan authorship, implementation completion or correctness, or code-review, verification, branch, PR, release, or deployment readiness.

## Resource map

- READ `references/test-quality.md` when adopted criteria apply and this invocation authors, allocates or assesses test obligations.
- READ `references/test-maintenance.md` when adopted criteria apply and this invocation changes tests or assesses test maintenance, removal or its impact.

- READ `references/review-reliance.md` when applying adopted assessment applicability, correction or closeout policy.
- READ `references/review-assessment.md` for every review under explicitly adopted Review and Closeout policy.

- READ `references/requirement-to-delivery-model.md` when tracing approved design into allocated milestones, work, and proof.
- READ `references/boundary-first-method-v1.md` initially for every `delivery-review` invocation.
- READ `references/boundary-first-proof-v1.md` after the method reference when the delivery package consumes a `boundary-first-v1` proof map.
- READ `references/delivery-review-recording-and-settlement.md` for every durable or formal review before recording or settlement.
- COPY `assets/review-result-skeleton.md` when producing every result. Omit inapplicable groups and unfilled placeholders.
- COPY `assets/material-finding.md` when a material finding exists, once per finding.

## Evidence collection efficiency

Use exact member IDs, paths, requirement IDs, boundary IDs, milestone IDs, proof IDs, command IDs, findings, and targeted excerpts before broad scans. Expand only when the delivery package cannot be judged from bounded evidence.

## When full-file read is required

Read the primary plan in full because the review decides its complete sequencing and verification contract. Read other files in full only when bounded evidence is insufficient or surrounding context changes the conclusion.

## Output skeleton

```md
COPY `assets/review-result-skeleton.md` when producing the review result.
COPY `assets/material-finding.md` when a material finding exists.
Fill <every applicable result and finding field> and do not emit unfilled placeholders.
```

## Expected output

Copy the result asset and each required finding asset. Report unavailable required data as blocked; do not invent package members, authority, proof, or evidence.
