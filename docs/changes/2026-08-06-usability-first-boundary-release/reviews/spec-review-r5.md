<!-- Template: spec-review-result-skeleton-v1 -->
<!-- Skill: spec-review -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/spec-review/SKILL.md -->

# Usability-First Boundary-First v0.4.0 Release Spec Review R5

Review ID: spec-review-r5
Stage: spec-review
Round: 5
Reviewer: Codex independent spec-review peer
Target: specs/usability-first-boundary-release.md
Review date: 2026-08-06
Status: approved
Material findings: none
Immediate next stage: plan
Automatic downstream handoff: none

## Result

- Skill: spec-review
- Review status: approved
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/spec-review-r5.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md#spec-review-r5`
- Open blockers: none
- Immediate next stage: plan
- Eventual test-spec readiness: conditionally-ready
- Stop condition: none

The condition is a test-spec update and independent test-spec review for the approved R5 contract before implementation resumes. Architecture and the execution plan are already settled; this isolated review does not advance either or start a downstream stage.

## Findings

None.

## Review dimensions

| Review dimension | Verdict | Evidence |
| --- | --- | --- |
| requirement clarity | pass | UBR-R021 states the exact stage-owned owner-pointer form, ordering, count, legacy PBF-R002 form, and fail-closed placements. |
| normative language | pass | The amendment uses observable `MUST` clauses and makes the stage-owned replacement boundary explicit. |
| completeness | pass | BND-COMPAT-001 now owns the full compatibility requirement set and includes both marker-placement partitions, invariants, and outcomes. |
| testability | pass | UBR-R021, EC11, and AC-UBR-013 identify the valid forms and every named invalid placement without implementation guesswork. |
| examples | pass | The exact metadata forms and EC11 provide sufficient concrete proof targets without a redundant narrative example. |
| compatibility | pass | Stage-owned specs use the owner-pointer form while non-stage-owned specs retain the standing PBF-R002 status form. |
| observability | pass | Failures are bounded to ordering, governed-section placement, and exact-one occurrence. |
| security/privacy | pass | The metadata-only contract adds no network, credential, or private-data surface. |
| non-goals | pass | The amendment does not introduce a lifecycle writer, new publication mechanism, or historical-spec migration. |
| acceptance criteria | pass | AC-UBR-012 covers R001-R021 proof completeness and AC-UBR-013 directly covers the placement outcomes. |

## Boundary-first semantic review

- `UBR-SR4-001` is resolved: the compatibility applicability row and BND-COMPAT-001 definition cite the same six requirements, and the new marker partitions, invariant, and outcomes remain explicit.
- `UBR-PRFG-CR1-001` is resolved at the spec-authority layer: UBR-R021 expressly replaces PBF-R002 placement only for `stage-owned-change-local-v1` feature specs while preserving marker identity, cardinality, and legacy placement elsewhere.
- The feature-only structural validator passes with no issues.
- The path-scoped validator reports only `BFR-PROOF-MODEL-MISMATCH` because the unchanged test spec still declares R001-R020. That is a downstream proof-map handoff, not a feature-record defect.
- No new selected interaction is required because marker location is a partition of the existing compatibility boundary and does not change another boundary's outcome.

## Prior finding reconciliation

- `UBR-SR4-001`: resolved by folding UBR-R021 into BND-COMPAT-001 with exact applicability/definition requirement-set agreement.
- `UBR-PRFG-CR1-001`: resolved at the governing-spec layer by the approved UBR-R021 replacement rule, compatibility disposition, EC11, and AC-UBR-013. Final code-review disposition can rely on this authority after downstream proof-map refresh and implementation rereview.
- `UBR-PRFG-CR1-002` and `UBR-PRFG-CR1-003` are outside this spec-review scope and remain open in review-resolution.

## Exact wording suggestions

None.

## Routing and readiness

The specification is approved. Architecture and planning for the initiative are already settled, so no amendment to those artifacts is identified by this review.

The matching test spec must be refreshed to identify spec-review R5 and map UBR-R021, AC-UBR-013, EC11, and the revised single BND-COMPAT-001 scope, then receive independent test-spec review. This direct review is isolated and starts no downstream stage automatically.
