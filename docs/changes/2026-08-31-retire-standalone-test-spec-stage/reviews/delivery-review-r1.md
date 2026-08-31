# Delivery Review R1: Retire the Standalone Test-Spec Stage

Review ID: delivery-review-r1
Stage: delivery-review
Round: r1
Reviewer: Independent Codex delivery-review context
Reviewer authority: delivery-review
Target: delivery package `plan`, `test-spec`
Reviewed artifact: delivery package `plan`, `test-spec`
Review date: 2026-08-31
Package kind: delivery
Package members: plan=docs/plans/2026-08-31-retire-standalone-test-spec-stage.md, test-spec=specs/retire-standalone-test-spec-stage.test.md
Upstream review ID: design-review-r2
Status: changes-requested
Material findings: RTS-DLR1
Correction targets: test-spec
Recording status: recorded

## Result

- Skill: delivery-review
- Review status: changes-requested
- Package members: `plan` = `docs/plans/2026-08-31-retire-standalone-test-spec-stage.md`; `test-spec` = `specs/retire-standalone-test-spec-stage.test.md`
- Upstream review ID: `design-review-r2`
- Review ID and round: `delivery-review-r1`, `r1`
- Traceability result: Every approved requirement, acceptance criterion, boundary, interaction, example, edge case, and implementation milestone reaches direct proof, but three plan-dependent validation commands lack stable command-ledger ownership and timing in the test specification.
- Material findings: `RTS-DLR1`
- Correction targets: `test-spec` owned by `test-spec`
- Recording status: recorded
- Settlement status: withheld pending exact-package settlement of the changes-requested outcome
- Open blockers: `RTS-DLR1`
- Immediate next stage: test-spec authoring owner
- Claim limitations: This review does not approve either member independently, authorize implementation, initialize planned work, advance workflow, or claim code, verification, branch, PR, release, or deployment readiness.

### Finding RTS-DLR1

Finding ID: RTS-DLR1
Severity: medium
Location: `docs/plans/2026-08-31-retire-standalone-test-spec-stage.md`, M3 and M6 validation commands; `specs/retire-standalone-test-spec-stage.test.md`, Validation commands and Milestone proof map
Evidence: The plan requires focused `python scripts/validate-skills.py ...` validation in M3 and requires `python scripts/validate-review-artifacts.py --mode closeout ...` plus `python scripts/validate-change-metadata.py ...` in M6. The test-spec command ledger assigns no stable command IDs, classifications, owners, failure behavior, zero-test behavior, evidence, or side-effect boundaries to those three depended-on commands, and its M3/M6 milestone rows therefore cannot show their timing.
Required outcome: Add stable command rows for all three plan-dependent commands and map them to every proof obligation, test case, and milestone that relies on them, without changing the approved engineering sequence.
Safe resolution path: The test-spec owner should add the missing command identities and complete their timing and side-effect fields, update affected proof and milestone mappings, register the exact revision, close this accepted finding with validation evidence, and request a fresh Delivery Review of the exact package.
needs-decision rationale: none
Finding scope: artifact-local
Affected artifact IDs: test-spec
Owning stages: test-spec

## Delivery package judgment

The implementation sequence is otherwise safe and reviewable. M1 establishes a non-authoritative classifier, M2 adds inactive dual-contract behavior, M3 establishes authoring and review ownership, M4 proves preactivation parity, and M5 performs one guarded activation only after prior-contract work no longer needs retired authoring entrypoints. M6 contains closeout only. Recovery preserves v1 default behavior before activation and uses forward correction after first v2 use.

All eight boundaries and five selected interactions have direct proof at appropriate contract, integration, or end-to-end levels. The package covers active legacy rejection, exact historical interpretation, post-gate v1 continuation, activation blocking for pre-gate work, unknown-value ordering, package parity, and rollback boundaries. The finding concerns command-ledger completeness, not missing behavior, unsafe sequencing, or an unavailable implementation path.

## Independence statement

This review context did not edit either package member, the approved design package, implementation, or workflow routing state while reaching the R1 judgment.
