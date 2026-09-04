# Code Review M1 R3: Compact authoritative model

Review ID: code-review-m1-r3
Stage: code-review
Round: r3
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: current M1 working-tree slice
Reviewed artifact: compact schema, parser, identity, complete-set validation, projection modules, tests, lifecycle compatibility fixes, and M1 evidence
Reviewed milestone: M1
Review date: 2026-09-04
Status: approved
Review status: approved
Material findings: none
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Open blockers: none
- Next stage: Workflow may close M1 after exact validation and review registration
- Review status: approved
- Material findings: none
- Recording status: recorded
- Review record: `docs/changes/2026-09-03-compact-current-state-change-record/reviews/code-review-M1-r3.md`
- Reviewed milestone: M1
- Milestone closeout: eligible after lifecycle registration
- Remaining implementation milestones: M1, M2, M3, M4, M5
- Required review-resolution: closed
- Verify readiness: not-claimed

## Review inputs

- Actual diff: compact contract, projection, JSON Schema and tests; bounded lifecycle package-routing and resolution-freshness corrections; governed proposal, Design, Delivery, finding-resolution, and M1 evidence.
- Approved Design package: `design-review-r4`.
- Approved Delivery package: `delivery-review-r4` for plan identity `sha256:6a27b852d9e803c3e226d8e01aed413a612f340e815da397ec333702f6f7149c`.
- Finding closeout: CCSR-M1-CR1 through CCSR-M1-CR5 are accepted, resolved, registered against current evidence, and absent from the current open-finding set.
- Direct proof: 19 focused compact tests; 19 focused lifecycle-evidence tests; 13 correction-route tests with 2 historical skips; 395 passing package tests with 2 historical skips; 107 metadata-validator tests; boundary-first, Draft 2020-12 metaschema, review closeout, prose, and diff validation.

## Rereview judgment

The current model defines and validates all eight compact schemas, every closed vocabulary, all fifteen semantic payload variants, candidate-file partitions and inline identities, exact Projection attribution, result consistency, calendar-valid timestamps, transaction-private recovery content paths, exact lifecycle revision input, and fixed-shape bounded projections.

Complete-set validation now admits only paths named by the current authoritative model and enforces both directions of finding, decision, and evidence membership. Verify evidence resolves to current manifest entries. Prototype-sensitive identifiers cannot bypass own-property checks. Optional decision, evidence, and Verify surfaces remain absent unless applicable.

The lifecycle compatibility fixes required to govern the corrections are bounded and tested: downstream corrections return through invalidated Design or Delivery packages, package rereview waits for every named owner, pending settlement remains distinct from rereview, resolved findings require current resolution evidence, and a semantically unchanged stale registration can refresh that evidence without enabling conflicting replacement.

No public compact writer or creation command is exposed. Existing v3 behavior passes the full suite, and the implementation has no Git, pull-request, network, hosted-service, or local-log correctness dependency.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | Exact schema tables, SR-01–SR-06 and SR-37–SR-42 are represented in executable and JSON Schema validation. |
| Test coverage | pass | All surfaces, vocabularies, operation variants, limits, identities, reverse membership, recovery roots, projections, and legacy behavior have direct or full-suite proof. |
| Edge cases | pass | Unknown, extra, missing, malformed, multibyte, contradictory, hidden, extraneous, stale, and unsafe recovery cases fail closed. |
| Error handling | pass | Stable errors preserve existing repository state; stale resolution evidence reopens the finding and permits only refresh. |
| Architecture boundaries | pass | The slice is read-only; transaction mutation and activation remain owned by later milestones. |
| Compatibility | pass | 395 package tests pass with 2 explicit historical skips. |
| Security/privacy | pass | Recovery paths are private-root constrained; no external correctness dependency or raw diagnostic retention was added. |
| Derived artifact currency | pass | JSON Schema parses and validates against Draft 2020-12 metaschema and matches executable operation/projection constraints. |
| Validation evidence | pass | Current M1 evidence names the exact plan identity and latest passing scopes. |

## Independence statement

This rereview inspected the current diff, approved contracts, all recorded findings and resolutions, current lifecycle projection, and exact validation results without modifying implementation or lifecycle state.

## No-finding statement

No material finding remains against the exact M1 R3 candidate.
