---
name: delivery-review
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Independently review one plan-centered delivery package before implementation. Judge safe sequencing and verification adequacy together; use plan for delivery and verification allocation and spec for behavioral gaps.
argument-hint: [change ID, delivery package, or plan path]
---

# Delivery review

Judge whether the approved design can be implemented safely and proved adequately through the exact primary plan. Review without editing the plan or approved design.

## Purpose

Trace SRs and architecture boundaries into proportional allocated work and proof.

Approve or reject one explicit plan-centered package in one independent decision covering implementation readiness and verification adequacy. Preserve requirement-to-proof traceability and precise finding ownership.

## When to use

Use after the execution plan has allocated the approved design's behavior, work, milestone verification, and applicable change-level verification, and before implementation.

## When not to use

Do not use to author the plan, repair specification behavior, redesign architecture, review implementation, execute final verification, or combine historical artifact-review evidence into package authority.

## Workflow role

### Compact current-state contract

For `compact-current-state-v1`, consume the bounded CLI projection and exact delivery-package paths. Update one stable current review record for the delivery package through a transient CLI operation. Keep open findings in that record and retain only continuing material constraints in `material-decisions.md`. A changes-requested outcome returns to plan; a clean exact rereview approves delivery. Do not create round-suffixed reviews, `review-log.md`, `review-resolution.md`, request files, or correction receipts.

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

Read first: `change.yaml`, `context delivery-review`, the exact primary plan, the approved Design Review ID and member map, and relevant prior findings.

Produce: one recorded package outcome, precise findings or a no-finding rationale, and an isolated or route-owned handoff.

Stop when: membership, upstream authority, evidence, independence, or lifecycle identity is missing, unsafe, stale, or contradictory.

Do not claim: implementation completion, code correctness, or final readiness.

Next stage: `route` may send an approved package to implementation; otherwise route named corrections or stop.

## Inputs to read

Resolve the governed change, then obtain the package with `rigorloop lifecycle context delivery-review --change <change-id> --format json`. Read the complete exact primary plan plus the approved Design Review ID and member map it operationalizes. Read current proposal constraints, architecture, specification, ADRs, and prior review or resolution evidence as needed to validate the trace.

For v3, the package member map must contain exactly the registered primary-plan artifact ID and normalized repository-relative path. A standalone test-spec substitute or extra member is invalid. Historical packages remain readable but grant no current review or progression authority. Do not calculate or request aggregate revisions or content hashes.

## Review contract

Evaluate implementation readiness and verification adequacy in the same decision. Check safe dependency order, acceptable intermediate states, milestone boundaries, migration sequence, reversibility, SR allocation, milestone verification, applicable change-level verification, important normal and negative scenarios, compatibility, migration, recovery, concurrency, security and authority concerns, and realistic evidence expectations.

Evaluate this exact trace for every applicable requirement and architecture risk:

`requirement -> architectural boundary -> implementation milestone -> required proof -> validation command or manual evidence`

Reject or request correction for missing SR allocation, unsafe or overly broad sequencing, unreviewable milestones, insufficient milestone or change-level verification, proof at the wrong boundary, architecture risk without validation, compatibility or migration work without evidence, unrealistic proof, and verification that requires a different implementation order than the plan. Milestone completion must not be treated as complete-change correctness.

Route the correction to `plan` when verification allocation is missing or inadequate; route missing observable behavior to `spec`. Do not author the correction, accept a standalone test-spec substitute, or defer material pre-implementation coverage to final Verify.

Use exactly one outcome: `approved`, `changes-requested`, `blocked`, or `inconclusive`. Only `approved` authorizes implementation. Every other outcome grants no progression authority.

## Findings and ownership

Every material finding uses exactly one scope:

- `artifact-local`: name exactly one plan artifact ID and its owning stage.
- `cross-artifact`: name the plan plus affected approved design artifact IDs and every authoring stage needed for reconciliation.
- `upstream-direction`: name the approved design package whose direction must be reconsidered.

Each finding records a stable Finding ID, Severity, Location, Evidence, Required outcome, Safe resolution path or `needs-decision` rationale, finding scope, affected artifact IDs, and owning stages. Copy the finding asset once per material finding. Review resolution does not replace a required current Delivery Review after package members change.

## Isolation and recording

A direct or review-only invocation remains isolated by default. It records required evidence and may settle the exact package, but it does not route downstream. Workflow-managed continuation returns control to `route` after settlement.

Every formal result must be recorded or explicitly blocked. For registered historical contracts, clean review uses a lightweight receipt and review-log entry, while material or blocking results use a detailed record and triggered `review-resolution.md`. Compact results update the stable current review and conditional material-decision surface described above.

## Package recording and settlement

Recording mode is `none`, `advisory-durable`, or `formal-lifecycle`. Settlement is `none` or `exact-package`. Only formal lifecycle review may settle, and loading the procedure grants no authority.

For a formal review, load the mapped procedure before any write or settlement claim. `record-package-review` records the exact current member map, approved Design Review ID, review identity, outcome, findings, correction targets, and evidence path. `settle-review-package` revalidates and atomically settles that same package. Settlement never advances workflow.

## Outputs

Produce the package identity, upstream review ID, traceability judgment, outcome, findings, correction targets, recording and settlement results, blockers, next owner, and claim limits.

## Handoff

An approved workflow-managed review returns to `route` for implementation. `changes-requested` routes plan allocation gaps to `plan` and behavioral or design gaps to their named upstream owner. `blocked` routes only to the named design owner. `inconclusive` stops for missing evidence. Direct review remains isolated.

## Stop conditions

Stop on incomplete or unsafe member maps, missing or stale design authority, stale lifecycle revision, wrong upstream review ID, self-review or reviewer-authored member changes, unresolved proof feasibility, failed recording, or an owner decision. Preserve supported findings even when settlement blocks.

## Claims this skill must not make

Do not claim plan authorship, implementation completion or correctness, or code-review, verification, branch, PR, release, or deployment readiness.

## Resource map

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
