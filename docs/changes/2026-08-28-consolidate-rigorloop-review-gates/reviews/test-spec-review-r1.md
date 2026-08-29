# Test-Spec Review R1: Consolidated Review Gates

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: r1
Reviewer: Codex independent test-spec-review context
Target: `specs/consolidated-review-gates.test.md`
Reviewed artifact: `specs/consolidated-review-gates.test.md` at `sha256:d8e54ff5e9a6d4bf45bd738fb80b2424412657347757f0bac873daf8c72b0fb3`
Reviewed artifact path: specs/consolidated-review-gates.test.md
Reviewed artifact identity: sha256:d8e54ff5e9a6d4bf45bd738fb80b2424412657347757f0bac873daf8c72b0fb3
Review date: 2026-08-29
Status: changes-requested
Review status: changes-requested
Material findings: CRG-TSR1-1
Recording status: recorded
Lifecycle mode: formal
Handoff mode: isolated
Boundary applicability: `boundary-first-v1` applicable
Recording applicability: required for formal review
Immediate next stage: test-spec revision
Implementation handoff: not-allowed
Automatic downstream handoff: none from this isolated review

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: CRG-TSR1-1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/test-spec-review-r1.md`
- Review log: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`
- Review resolution: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md#test-spec-review-r1`
- Open blockers: CRG-TSR1-1
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: implementation remains blocked until the test specification reconciles the approved plan's validation commands and receives a clean rereview

## Findings

## Finding CRG-TSR1-1

Finding ID: CRG-TSR1-1
Severity: major
Location: `specs/consolidated-review-gates.test.md` Validation commands and Milestone proof map, especially lines 93-113
Evidence: The approved plan requires focused and owner-specific commands that are absent from the test specification's command ledger and milestone proof map. Missing proof includes `scripts/test-artifact-lifecycle-validator.py` in M1 and M5, `scripts/test-governed-lifecycle-cli-validator.py` in M2 and M6, three workflow policy/state commands in M3, documentation prose validation in M4, lifecycle CLI conformance in M6, and three exact lifecycle closeout validators in M7. CMD-001's package-wide npm suite and CMD-009's broad smoke do not identify those omitted obligations or preserve their first-required milestone ownership.
Required outcome: Reconcile every approved-plan validation command with the test-spec command ledger and milestone proof map so each required command has an exact command ID, classification, owner, first required milestone, failure and zero-test behavior, evidence target, and side-effect boundary.
Safe resolution path: Add the omitted plan commands to the test specification and reference them from the applicable cases, proof obligations, and M1-M7 rows. If any approved command should no longer be required, route that change to the plan owner instead of silently weakening it in the proof map, then independently rereview the resulting exact test-spec revision.
needs-decision rationale: none

## Review assessment

- Requirement, example, edge-case, boundary, and interaction coverage is otherwise complete and uses the approved stable IDs.
- All eight boundary dimensions and INT-001 through INT-008 have direct automated proof obligations at appropriate contract, integration, end-to-end, or smoke levels.
- Negative partitions cover unknown vocabularies, incomplete and contradictory packages, stale identities, interrupted transactions, mixed topology evidence, activation failure, and rollback.
- The plan-command mismatch prevents implementation handoff because milestone completion could be claimed without executing validation that the approved plan makes mandatory.
- Existing command paths and the `broad-smoke` mode resolve in the repository; this finding concerns missing traceability and milestone ownership, not nonexistent commands.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| governing-contract alignment | pass | The proof map preserves the approved topology, authority, compatibility, and no-per-document-hash direction. |
| requirement and acceptance traceability | pass | CRG-R1 through CRG-R45 map to cases, and the acceptance criteria remain traceable through their governing requirement groups and targeted end-to-end proof. |
| boundary and interaction coverage | pass | PRF-001 through PRF-016 cover all approved boundaries and interactions with exact IDs. |
| negative and recovery coverage | pass | Unknown, missing, duplicate, contradictory, stale, interrupted, partial, hybrid, and rollback states have direct assertions. |
| proof-level adequacy | pass | Contract, integration, end-to-end, and smoke levels match their observable claims. |
| command validity | pass | Every command currently listed resolves or is explicitly planned, and the broad-smoke flag is supported. |
| plan-command alignment | block | Required commands from every affected plan milestone are missing from the ledger or milestone map. |
| milestone mapping | block | M1-M7 do not retain the approved plan's complete first-required validation set. |
| fixtures and determinism | pass | Repository-local fixtures, fixed aggregate vectors, and bounded fault injection avoid network and machine-local dependencies. |
| manual-proof boundary | pass | No acceptance outcome improperly depends on unowned manual QA. |
| implementation handoff | block | Implementers cannot use the test specification alone to execute all approved milestone proof. |

## Claim limitations

This review records proof-map readiness only. It does not authorize implementation, alter the reviewed test specification, claim any implementation validation result, or establish verification, branch, release, or pull-request readiness.
