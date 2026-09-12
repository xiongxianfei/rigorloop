# Retire the v2 stored-record format

Owning change: [change.json](../changes/2026-09-11-retire-v2-record-format/change.json).

## Challenge

RigorLoop now creates v3 stores, but retains v2 recording, validation and recovery for existing work. Maintaining both stored contracts keeps compatibility branches, fixtures and consumer instructions that no longer serve new assessments. The [structured-assessment initiative](../changes/2026-09-10-structured-assessment-explanations/change.json) deliberately left v2 retirement to a separate decision so that it could finish its original assessment chain without conversion.

The repository currently contains twelve v2 stores, all marked completed and containing Verify reports. Those observations make retirement worth pursuing; they do not establish that every operational, governance or recovery dependency has been settled.

## Goals

- Make v3 the sole operational stored-record contract and simplify its supporting implementation and guidance.
- Preserve historical v2 bytes, identities and judgments without migrating approvals or retaining a permanent legacy reader.
- Remove test cases, fixtures and helpers that serve only v2, while retaining useful protection for v3 and shared behavior.
- Follow the user's explicit validation scope: do not add tests about retiring v2 or a dedicated v2-retirement test suite.

## Scope and non-goals

| Work family | Scope budget treatment | Boundary |
| --- | --- | --- |
| V2 stored-format runtime and exclusive resources | core to this proposal | Retire operational v2 support and remove dependencies used exclusively by it. |
| V2-only tests and supporting fixtures/helpers | core to this proposal | Remove obsolete cases; retain shared and v3 coverage, adjusting synthetic setup where necessary. |
| Owning policies, discovery, validators, canonical consumers and package inputs | same-slice dependency | Reconcile the support contract and preserve access to current governing authority without a v2 runtime dependency. |
| Existing work and recovery disposition | same-slice dependency | Establish a responsible disposition before removing required support; preserve completed historical evidence unchanged. |
| Migration services, permanent compatibility readers and unrelated cleanup | out of scope | Do not convert bodies or approvals, redesign reports, or remove unrelated document validators. |
| Release, publication and customer activation | out of scope | Keep their existing separate ownership and authorization. |

Retirement concerns `rigorloop-records-v2`, not every artifact named v2 or schema numbered 2. Independent request, response and document contracts, and definitions still required by v3, remain supported. Existing tests must be classified by the behavior they protect rather than their filenames. No new v2 rejection, retirement or archival-compatibility test cases are requested; run the retained applicable suites.

## Governing principle

Maintain operational support for current work while preserving the meaning of historical evidence.

## Proposed direction

Approve a bounded retirement of the v2 stored format. Continue this initiative in a new v3 store. Establish which existing v2 dependencies can become archival and explicitly resolve any unfinished work, interrupted storage or active-governance dependency before removing the support it needs. Do not infer that disposition from a completed label or the presence of a report.

Remove exclusive v2 runtime paths and their exclusive tests together, and reconcile the affected consumers around v3. Retain shared safety behavior and independently versioned interfaces. Historical v2 records remain inspectable as repository artifacts without becoming operational inputs or acquiring new approvals. Existing unsupported-format handling should serve the retired format without a new compatibility subsystem.

The [Record Format](../design/record-format/record-format.md) and [Workflow](../design/workflow/workflow.md) continuation clauses require this separate retirement decision. Design must reconcile those owners with CLI mechanics and assessment-policy dependencies; Delivery determines the bounded removal sequence and retained verification allocation. This proposal does not remove support or approve implementation.

## Feasibility

Assessment: feasible for Design, with a bounded dependency question before removal. Current [format dispatch](../../packages/rigorloop/dist/lib/record-store-format.js) explicitly selects v2 or v3, and the [v3 adapter](../../packages/rigorloop/dist/lib/record-format-v3.js) already uses shared core machinery. These inspected boundaries support selective removal, while also showing why deleting everything named v2 would be unsafe. The twelve-store inventory is a local observation, not a claim about all users or a completed recovery audit.

No new technology or migration service is needed. The material constraint is identifying support still needed by unfinished work, recovery, active governance or shared consumers. Any unresolved dependency blocks the affected removal and needs an owner disposition; it does not justify silently carrying a permanent v2 implementation forward. No blocker to drafting the owning Design has been identified.

## Impact and major trade-offs

This deliberately ends existing-v2 operational compatibility in a later adopted implementation. Users needing unfinished v2 operations must receive an explicit disposition before that dependency is removed. Preserving historical files does not preserve their CLI operability. Removing v2-only tests reduces maintenance but requires careful separation from shared protection; the selected scope does not introduce replacement retirement tests. Release communication and adoption remain separately owned.

## Decision requested

Approve v2 stored-format retirement as the next Design direction, including the explicit work/recovery disposition, unchanged historical evidence, coordinated consumer cleanup, removal of v2-only tests and no added v2-retirement tests. Retain v3 and shared behavior and all independently supported version domains. Approval of this proposal would authorize Design work, not retirement implementation, release or publication.
