# Code Review M1 R1: Compact authoritative model

Review ID: code-review-m1-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: current M1 working-tree slice
Reviewed artifact: compact schema, parser, identity, complete-set validation, projection modules, tests, and M1 evidence
Reviewed milestone: M1
Review date: 2026-09-04
Status: changes-requested
Review status: changes-requested
Material findings: CCSR-M1-CR1, CCSR-M1-CR2, CCSR-M1-CR3
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-09-03-compact-current-state-change-record/reviews/code-review-M1-r1.md`, `docs/changes/2026-09-03-compact-current-state-change-record/review-log.md`, and `docs/changes/2026-09-03-compact-current-state-change-record/review-resolution.md`
- Open blockers: CCSR-M1-CR1, CCSR-M1-CR2, and CCSR-M1-CR3
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CCSR-M1-CR1, CCSR-M1-CR2, CCSR-M1-CR3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-09-03-compact-current-state-change-record/reviews/code-review-M1-r1.md`
- Review log: `docs/changes/2026-09-03-compact-current-state-change-record/review-log.md`
- Review resolution: `docs/changes/2026-09-03-compact-current-state-change-record/review-resolution.md`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4, M5
- Required review-resolution: yes
- Finding IDs: CCSR-M1-CR1, CCSR-M1-CR2, CCSR-M1-CR3
- Verify readiness: not-claimed

## Review inputs

- Actual diff: current working-tree M1 additions under `schemas/compact-current-state-v1.schema.json`, `packages/rigorloop/dist/lib/compact-*.js`, the two compact test files, and M1 evidence.
- Approved Design package: `design-review-r3` for `architecture`, `spec`, and `adr-compact-current-state-transaction`.
- Approved Delivery package: `delivery-review-r2` for plan identity `sha256:a9809d144a292541affb790777e5c8b65474b325dd9c3d2fb6606d90d4d4b53b`.
- Current milestone: M1 is implementing; M2 through M5 remain planned.
- Direct proof: focused compact tests, the complete package suite, change-metadata validator tests, boundary-first validation, and JSON schema parsing all pass.

## Actual-diff summary

The slice establishes the intended read-only v1 model without exposing a writer. It reuses the hardened YAML parser, rejects unknown fields and vocabularies, calculates an exact whole-set revision, binds referenced current records, and returns fixed-shape projections independent of supplied procedural history. The implementation is not yet contract-complete because one normative projection contradiction has no valid implementation and several boundary conditions are incompletely enforced.

## Finding CCSR-M1-CR1

Finding ID: CCSR-M1-CR1
Severity: major
Location: `specs/compact-current-state-change-record.md:95` and `specs/compact-current-state-change-record.md:255`
Evidence: SR-21 requires a successful skill-context projection to include change identity, lifecycle-contract identity, and lifecycle revision. The normative exact Projection record omits all three fields, and SR-39 forbids undeclared fields. The current implementation follows the table and therefore cannot satisfy SR-21; adding the identities would instead violate the exact table.
Required outcome: Define one closed Projection shape that contains the three required identities for every view or explicitly and coherently relocates them to an enclosing result, then align SR-21, the table, the schema artifact, implementation, and direct tests.
Safe resolution path: Accept the finding, route it to the specification owner as an upstream contract gap, add `change_id`, `lifecycle_contract`, and `lifecycle_revision` to the closed Projection shape as the smallest resolution consistent with SR-21, register the revised spec, obtain a fresh exact-package Design Review, then return M1 for implementation correction and Code Review R2.
needs-decision rationale: none; SR-21 already establishes that these identities are required, so adding them to the exact Projection table removes the contradiction without changing approved direction.

## Finding CCSR-M1-CR2

Finding ID: CCSR-M1-CR2
Severity: major
Location: `packages/rigorloop/dist/lib/compact-contract.js:82`, `packages/rigorloop/dist/lib/compact-contract.js:375`, and `schemas/compact-current-state-v1.schema.json` operation envelope
Evidence: `Text` enforces JavaScript character count rather than the specified UTF-8 16 KiB bound; the JSON Schema operation `payload` remains an open generic object instead of the exact operation-specific variants; and result validation does not enforce the specified projection-versus-mutation lifecycle-revision relationships. Existing tests cover representative surfaces but not valid and invalid records for all eight schemas and reusable nested records, so these gaps pass the suite.
Required outcome: Enforce every M1-allocated scalar, top-level, nested, and result consistency boundary in both the executable validator and schema artifact, with direct unknown, extra, limit, mismatch, and all-schema vectors.
Safe resolution path: Accept the finding for Implementation, add failing table-driven tests for multibyte Text overflow, every top-level schema, operation-specific payload closure/matching, and result-kind consistency; then make the smallest validator and schema corrections and rerun the complete M1 validation set before Code Review R2.
needs-decision rationale: none; the approved specification already defines the required shapes and outcomes.

## Finding CCSR-M1-CR3

Finding ID: CCSR-M1-CR3
Severity: major
Location: `docs/plans/2026-09-03-compact-current-state-change-record.md:57`
Evidence: After Design Review R4 became the authoritative Design judgment, M1's dependency list still required the superseded `design-review-r3`. Delivery Review R3 correctly bound its package to R4 but did not identify this stale exact dependency, so the plan does not yet name the authority under which the corrected Projection shape is being implemented.
Required outcome: Replace the stale M1 dependency with exact Design Review R4, register the plan revision through its owner, and obtain a fresh Delivery Review that explicitly verifies the corrected dependency before M1 rereview.
Safe resolution path: Accept the finding, route it to Plan as an upstream planning gap, make only the exact dependency correction, return through Delivery Review, and resume M1 without changing milestone scope or proof allocation.
needs-decision rationale: none; the current settled Design package already determines the exact review identity.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | CCSR-M1-CR1 is an internal normative contradiction; CCSR-M1-CR2 identifies incomplete exact-shape enforcement. |
| Test coverage | concern | Strong representative and legacy coverage exists, but all-schema and identified boundary vectors are absent. |
| Edge cases | concern | Alias, duplicates, byte identity, procedural-history independence, and stale revision are covered; multibyte limits and result partitions are not. |
| Error handling | concern | Parsing fails closed, but result consistency can admit contradictory successful shapes. |
| Architecture boundaries | pass | The slice is read-only and keeps writer activation withheld. |
| Compatibility | pass | The complete legacy package suite passes with compact commands absent. |
| Security/privacy | pass | No network, Git, PR, log, secret, or external-service dependency was added. |
| Derived artifact currency | concern | The canonical JSON Schema does not yet close operation payload variants. |
| Unrelated changes | pass | The reviewed slice remains within M1's model and test scope. |
| Validation evidence | concern | All selected commands pass, but the missing vectors allow the two findings. |

## No automatic downstream handoff

M1 remains open. All three findings require disposition and correction; CCSR-M1-CR1 requires the completed governed specification revision and fresh Design Review, CCSR-M1-CR3 requires an exact plan dependency correction and fresh Delivery Review, and all changed implementation must receive Code Review R2 before milestone closeout.
