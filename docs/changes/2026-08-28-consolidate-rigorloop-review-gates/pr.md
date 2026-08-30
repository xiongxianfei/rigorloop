# Pull Request Handoff

| Field | Value |
| --- | --- |
| PR URL | Not opened |
| PR state | prepared locally |
| Base branch | `main` at `7510513c669f6cf17a155f88378cc4f4f6a7c045` |
| Head branch | `proposal/consolidate-review-gates` |

## Result

- Skill: pr
- Status: prepared
- Open blockers: none in the change; external push and PR opening were not authorized
- Next stage: push branch and open PR when authorized
- Readiness: PR body ready; Verify reports branch-ready

## Title

refactor: consolidate RigorLoop review gates

## Summary

- Replace separate architecture/specification approval with one Design Review decision package.
- Replace separate plan/test-specification approval with one Delivery Review decision package.
- Keep Proposal Review, milestone and final Code Review, and Verify as distinct gates.
- Preserve separate artifact authorship while making review findings precisely attributable to a member artifact, a cross-artifact inconsistency, or an upstream decision.
- Embed one feasibility evaluation in the proposal and keep package identity explicit and hash-free.
- Cut over canonical workflow guidance, lifecycle behavior, validators, skills, and generated adapter inventories together.

## Why

The former topology created a mandatory review for nearly every authored file even when two files jointly represented one engineering decision. Consolidation removes repeated ceremony and partial approval states while retaining the artifacts, independent review, durable findings, and downstream assurance needed for safe implementation.

## What changed

- Added explicit Design and Delivery package membership and review authority to the governed lifecycle contract and CLI.
- Added canonical `design-review` and `delivery-review` skills and retired the four former artifact-review progression entrypoints.
- Added package-aware recording, settlement, invalidation, correction routing, status, validation, and failure outcomes without member or aggregate hashes.
- Updated proposal feasibility, workflow guidance, schema, validators, tests, adapter metadata, and generated archive proof.
- Preserved pre-cutover evidence for this implementing change through the explicit CRG-R40 grandfathering rule.
- Removed transient CLI request inputs from the final diff instead of treating them as durable lifecycle evidence.

## Tests and verification

| Check | Result | Evidence |
| --- | --- | --- |
| RigorLoop package suite | 298 total; 296 passed and two intentional historical scenarios skipped | `verify-report.md` |
| Focused lifecycle suite | 97 total; 95 passed and the same two historical scenarios skipped | `verify-report.md` |
| Metadata validator regression | 66 passed | `verify-report.md` |
| Review artifact validator regression | 104 passed | `verify-report.md` |
| Skill validator regression | 450 passed; 90 retired-topology cases skipped by design | `verify-report.md` |
| Adapter distribution regression | 154 passed | `verify-report.md` |
| PR validation selector | passed; zero blockers and zero unclassified paths | `verify-report.md` |
| Review closeout | passed; 40 reviews and 29 resolved findings | `review-resolution.md` |
| Broad smoke | 11 checks passed in 796 seconds | `verify-report.md` |
| Branch integration | conflict-free merge-tree and clean diff check | `verify-report.md` |

Hosted CI was not observed and is not claimed.

## Risks and recovery

- Direct ungoverned edits cannot automatically invalidate a package because this slice deliberately avoids content hashes; semantic review and Verify remain responsible for detecting drift.
- Applicable ADR membership remains an architecture-stage judgment even though the selected member map is explicit.
- Active pre-cutover changes need their documented compatibility interpretation; post-cutover changes must not infer Design or Delivery authority from former individual reviews.
- Ordinary source-control reversion remains available. This change intentionally adds no rollback-specific lifecycle state or command machinery.

## Reviewer notes

- Start with `specs/consolidated-review-gates.md` and `docs/adr/ADR-20260828-consolidated-review-package-topology.md` to review the decision and lifecycle boundaries.
- Confirm that package identity is the explicit artifact ID-to-path map plus upstream review IDs, with no per-document hash, aggregate revision, or activation manifest.
- Confirm Design and Delivery correction routes preserve member ownership and require coherent package rereview.
- Confirm retired review entrypoints are absent from canonical skills and public adapter inventories while historical evidence remains readable.
- Pay particular attention to the atomic cutover fixtures, package settlement replay, and CRG-R40 compatibility boundary.

## Follow-ups

- Proposal-content simplification remains a separate future change.
- Hosted CI and any release archive publication occur outside this local handoff.

## Spec / plan / architecture

- Proposal: `docs/proposals/2026-08-28-consolidate-rigorloop-review-gates.md`
- Spec: `specs/consolidated-review-gates.md`
- Test spec: `specs/consolidated-review-gates.test.md`
- Architecture / ADR: `docs/adr/ADR-20260828-consolidated-review-package-topology.md`
- Plan: `docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md`

## Requirement coverage

| Requirement | Proof | Changed surface |
| --- | --- | --- |
| CRG-R1–R11 | CRG-T01–T03 | topology, Proposal Review, embedded feasibility |
| CRG-R12–R34 | CRG-T04–T11 | member maps, package review authority, settlement, routing, failure behavior |
| CRG-R35–R40 | CRG-T12–T16 | atomic cutover, historical compatibility, retired entrypoints |
| CRG-R41–R45 | CRG-T15–T17 | Code Review, Verify, adapters, end-to-end traceability |

## Review resolution summary

| Disposition | Count |
| --- | ---: |
| Accepted | 25 |
| Rejected | 3 |
| Deferred | 0 |
| Partially accepted | 1 |
| Needs decision | 0 |

Open findings: 0.

## Lifecycle and verification evidence

- Change record: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/change.yaml`
- Explain-change: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/explain-change.md`
- Verify report: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/verify-report.md`

## Migration

The release uses one atomic public cutover. This implementing change is explicitly grandfathered under CRG-R40. Existing governed changes either complete under their pre-cutover contract or use a separately approved compatibility action; the runtime does not select between old and new topologies.

## Security and privacy

No new network, credential, permission, personal-data, or external-service surface is introduced. Lifecycle paths and closed vocabularies continue to fail closed.

## Release or operational impact

Canonical skills, lifecycle behavior, schema, validators, and adapter inventories must ship together. This local handoff does not publish archives, tag a release, deploy, or mutate any external system.
