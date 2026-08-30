---
name: delivery-review
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Independently review an execution plan and test specification as one delivery package before implementation. Use delivery-review to judge sequencing, traceability, proof adequacy, recovery, and exact package authority; use plan and test-spec for authorship.
argument-hint: [change ID, delivery package, plan path, or test specification path]
---

# Delivery review

Judge whether the approved design can be implemented safely and proved adequately through one reconciled plan and test specification. Review without editing either artifact.

## Purpose

Approve or reject one explicit delivery package and preserve requirement-to-proof traceability and precise finding ownership.

## When to use

Use after the execution plan and test specification have been reconciled against an approved design package and before implementation.

## When not to use

Do not use to author the plan or test specification, redesign upstream behavior or architecture, review implementation, execute final verification, or combine historical plan-review and test-spec-review evidence into package authority.

## Workflow role

- role_name: delivery-review
- stage: review
- upstream: one execution plan, one test specification, and the approved Design Review ID
- downstream: implementation, author-owned correction, upstream design reconsideration, or isolated stop
- summary: Decide whether the exact delivery package can implement and prove the approved design.
- ownership: Write Delivery Review evidence and settle only the exact delivery package. Workflow owns routing.
- must_not_claim: plan or test-specification authorship, implementation completion, code-review, final verification, branch readiness, or PR readiness

The reviewer does not edit the execution plan, test specification, design package, implementation, or routing state. Approval is package authority, never plan-only or proof-only approval.

## Quick operating guide

Use this skill to: review one exact plan/test-specification package against the approved design.

Read first: `change.yaml`, `context delivery-review`, both member paths, the approved Design Review ID and member map, and relevant prior findings.

Produce: one recorded package outcome, precise findings or a no-finding rationale, and an isolated or workflow-owned handoff.

Stop when: membership, upstream authority, evidence, independence, or lifecycle identity is missing, unsafe, stale, or contradictory.

Do not claim: implementation completion, code correctness, or final readiness.

Next stage: workflow may route an approved package to implementation; otherwise route named corrections or stop.

## Inputs to read

Resolve the governed change, then obtain the package with `rigorloop lifecycle context delivery-review --change <change-id> --format json`. Read the complete execution plan and test specification plus the approved Design Review ID and member map they operationalize. Read current proposal constraints, architecture, specification, ADRs, and prior review or resolution evidence only as needed to validate the trace.

The package member map must show stable artifact IDs and exact normalized repository-relative paths in this order: execution plan, then test specification. Do not calculate or request aggregate revisions or content hashes.

## Review contract

Evaluate this exact trace for every applicable requirement and architecture risk:

`requirement -> architectural boundary -> implementation milestone -> required proof -> validation command or manual evidence`

Reject or request correction for missing milestone ownership, unsafe or overly broad sequencing, unreviewable milestones, proof at the wrong boundary, architecture risk without validation, compatibility or migration work without evidence, nondeterministic or unavailable proof, and tests that require a different implementation order than the plan.

Use exactly one outcome: `approved`, `changes-requested`, `blocked`, or `inconclusive`. Only `approved` authorizes implementation. Every other outcome grants no progression authority.

## Findings and ownership

Every material finding uses exactly one scope:

- `artifact-local`: name exactly one plan or test-specification artifact ID and its owning stage.
- `cross-artifact`: name at least two affected artifact IDs and every authoring stage needed for reconciliation.
- `upstream-direction`: name the approved design package whose direction must be reconsidered.

Each finding records a stable Finding ID, Severity, Location, Evidence, Required outcome, Safe resolution path or `needs-decision` rationale, finding scope, affected artifact IDs, and owning stages. Copy the finding asset once per material finding. Review resolution does not replace a required current Delivery Review after package members change.

## Isolation and recording

A direct or review-only invocation remains isolated by default. It records required evidence and may settle the exact package, but it does not route downstream. Workflow-managed continuation returns control to workflow after settlement.

Every formal result must be recorded or explicitly blocked. Clean review uses a lightweight receipt and review-log entry. Material or blocking results use a detailed record and `review-resolution.md` when disposition is required. Do not create an empty `review-resolution.md` solely for a clean result.

## Package recording and settlement

Recording mode is `none`, `advisory-durable`, or `formal-lifecycle`. Settlement is `none` or `exact-package`. Only formal lifecycle review may settle, and loading the procedure grants no authority.

For a formal review, load the mapped procedure before any write or settlement claim. `record-package-review` records the exact current member map, approved Design Review ID, review identity, outcome, findings, correction targets, and evidence path. `settle-review-package` revalidates and atomically settles that same package. Settlement never advances workflow.

## Outputs

Produce the package identity, upstream review ID, traceability judgment, outcome, findings, correction targets, recording and settlement results, blockers, next owner, and claim limits.

## Handoff

An approved workflow-managed review returns to workflow for implementation. `changes-requested` routes each named artifact-local or cross-artifact correction to its owning plan or test-spec stage. `blocked` routes only to the named design owner. `inconclusive` stops for missing evidence. Direct review remains isolated.

## Stop conditions

Stop on incomplete or unsafe member maps, missing or stale design authority, stale lifecycle revision, wrong upstream review ID, self-review or reviewer-authored member changes, unresolved proof feasibility, failed recording, or an owner decision. Preserve supported findings even when settlement blocks.

## Claims this skill must not make

Do not claim that plan or test specification is independently approved, that implementation is complete or correct, or that code review, verification, branch, PR, release, or deployment readiness exists.

## Resource map

- READ `references/boundary-first-method-v1.md` initially for every `delivery-review` invocation.
- READ `references/boundary-first-proof-v1.md` after the method reference when the delivery package consumes a `boundary-first-v1` proof map.
- READ `references/delivery-review-recording-and-settlement.md` for every durable or formal review before recording or settlement.
- COPY `assets/review-result-skeleton.md` when producing every result. Omit inapplicable groups and unfilled placeholders.
- COPY `assets/material-finding.md` when a material finding exists, once per finding.

## Evidence collection efficiency

Use exact member IDs, paths, requirement IDs, boundary IDs, milestone IDs, proof IDs, command IDs, findings, and targeted excerpts before broad scans. Expand only when the delivery package cannot be judged from bounded evidence.

## When full-file read is required

Read both package members in full because the review decides cross-artifact coherence. Read other files in full only when bounded evidence is insufficient or surrounding context changes the conclusion.

## Output skeleton

```md
COPY `assets/review-result-skeleton.md` when producing the review result.
COPY `assets/material-finding.md` when a material finding exists.
Fill <every applicable result and finding field> and do not emit unfilled placeholders.
```

## Expected output

Copy the result asset and each required finding asset. Report unavailable required data as blocked; do not invent package members, authority, proof, or evidence.
