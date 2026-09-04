# Code Review M1 R2: Compact authoritative model

Review ID: code-review-m1-r2
Stage: code-review
Round: r2
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: current M1 working-tree slice
Reviewed artifact: compact schema, parser, identity, complete-set validation, projection modules, tests, lifecycle routing fixes, and M1 evidence
Reviewed milestone: M1
Review date: 2026-09-04
Status: changes-requested
Review status: changes-requested
Material findings: CCSR-M1-CR4, CCSR-M1-CR5
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Open blockers: CCSR-M1-CR4 and CCSR-M1-CR5
- Next stage: Implementation correction followed by Code Review M1 R3
- Review status: changes-requested
- Material findings: CCSR-M1-CR4, CCSR-M1-CR5
- Recording status: recorded
- Review record: `docs/changes/2026-09-03-compact-current-state-change-record/reviews/code-review-M1-r2.md`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4, M5
- Required review-resolution: yes
- Finding IDs: CCSR-M1-CR4, CCSR-M1-CR5
- Verify readiness: not-claimed

## Review inputs

- Actual diff: current compact contract, projection, JSON Schema, tests, M1 evidence, and bounded lifecycle routing corrections required to restore Design and Delivery authority.
- Approved Design package: `design-review-r4`.
- Approved Delivery package: `delivery-review-r4` for plan identity `sha256:6a27b852d9e803c3e226d8e01aed413a612f340e815da397ec333702f6f7149c`.
- Direct proof: 17 focused compact tests, 393 passing package tests with 2 historical skips, 107 metadata-validator tests, boundary-first validation, Draft 2020-12 metaschema validation, closeout validation, and diff checks.

## Finding CCSR-M1-CR4

Finding ID: CCSR-M1-CR4
Severity: major
Location: `packages/rigorloop/dist/lib/compact-contract.js` complete-set validation
Evidence: `validateCompactSet` verifies coordinator references in one direction only. It accepts an open finding present in a current stable review but omitted from `change.yaml`, and likewise does not reject unreferenced decision or evidence entries. It also includes any caller-supplied extra file in the lifecycle manifest without proving that the path is one of the authoritative surfaces allowed by SR-02. A caller can therefore hide current consequences from projections or make a request/log file part of the governed set.
Required outcome: Complete-set validation must enforce exact bidirectional membership for current review findings, decisions, and evidence; resolve every Verify evidence ID to a current evidence entry; and reject every supplied file outside the exact current authoritative path set.
Safe resolution path: Add failing complete-set fixtures for hidden findings, unreferenced entries, missing Verify evidence, and extra procedural files; then enforce exact membership before lifecycle-revision acceptance.
needs-decision rationale: none; SR-02, SR-03, SR-06, SR-09, SR-14, SR-17, and SR-26 already require the exact non-loss boundary.

## Finding CCSR-M1-CR5

Finding ID: CCSR-M1-CR5
Severity: major
Location: `packages/rigorloop/dist/lib/compact-contract.js` timestamp, milestone-operation, and recovery validation; matching JSON Schema
Evidence: Recovery content paths are accepted anywhere in the repository instead of only beneath `.rigorloop/transactions/<change-id>/prior/` or `candidate/`; `advance-milestone` accepts `closed` as a source and `planned` as a destination despite the narrower operation schema; and calendar-impossible RFC 3339 timestamps pass JavaScript `Date.parse` normalization. These are explicit exact-schema and containment conditions allocated to M1.
Required outcome: Enforce the exact recovery content roots, milestone transition endpoint vocabularies, and valid UTC calendar timestamps in executable validation and the JSON Schema wherever expressible, with direct invalid vectors.
Safe resolution path: Add failing recovery traversal/root, closed-source, planned-destination, and impossible-date vectors; then make the smallest validator and schema corrections.
needs-decision rationale: none; the approved schema tables and SR-38, SR-41, SR-43, and SR-44 determine the correction.

## Review judgment

The R1 findings and the plan dependency correction are substantively addressed, and the writer remains withheld. M1 cannot close because the missing reverse-membership and recovery constraints could hide authoritative state or admit unsafe recovery locations despite otherwise passing validation.
