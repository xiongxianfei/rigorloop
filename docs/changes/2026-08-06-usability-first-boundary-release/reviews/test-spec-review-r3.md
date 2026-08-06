<!-- Template: test-spec-review-result-skeleton-v1 -->
<!-- Skill: test-spec-review -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/test-spec-review/SKILL.md -->

# Usability-First Boundary-First v0.4.0 Test-Spec Review R3

Review ID: test-spec-review-r3
Stage: test-spec-review
Round: 3
Reviewer: Codex independent test-spec-review peer
Target: specs/usability-first-boundary-release.test.md
Review date: 2026-08-06
Status: changes-requested
Review status: changes-requested
Material findings: UBR-TSR3-001
Immediate next stage: test-spec revision
Implementation handoff: not-allowed
Automatic downstream handoff: none

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: UBR-TSR3-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/test-spec-review-r3.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md#test-spec-review-r3`
- Open blockers: UBR-TSR3-001
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: T24 must prove lifecycle-contract authority rather than treating an owning-change pointer as sufficient authority.

## Findings

## Finding UBR-TSR3-001

Finding ID: UBR-TSR3-001
Severity: major
Location: `specs/usability-first-boundary-release.test.md`, T24 fixture/setup and steps, PRF-007, and the R021/AC-UBR-013 coverage rows
Evidence: Approved UBR-R021 permits the owner-pointer marker form only when the feature spec is governed by `stage-owned-change-local-v1`; every other feature spec retains PBF-R002 status placement. T24 calls one fixture "stage-owned" but requires only a normalized owner pointer, and its mutations cover before-pointer, outside-section, and duplicate placement. It never requires a referenced `change.yaml` declaring the lifecycle contract or rejects the owner-pointer form when that contract is absent or non-stage-owned. Its stated failure claim that a marker lacks lifecycle authority therefore has no corresponding step. The claimed existing seam confirms the gap: `validate_feature_record(stage_owned)` accepts owner-pointer text without reading a change record. The amendment also labels T24 `integration` while its requirement and PRF-007 rows label the proof `contract`.
Required outcome: T24 must establish lifecycle authority from a matching owning change record, prove the stage-owned owner-pointer and non-stage-owned status positives, and fail when a non-stage-owned or missing-contract record uses the owner-pointer form, in addition to the three named placement/cardinality negatives. Its coverage and proof-level labels must agree, and the evidence artifact must name the resulting direct proof.
Safe resolution path: Extend T24's fixture/setup and steps with paired feature-spec and `change.yaml` fixtures: one exact `stage-owned-change-local-v1` positive, one retained non-stage-owned status positive, and one absent or different lifecycle-contract owner-pointer negative. Keep CMD06 and M2 ownership if the boundary test suite exercises the path-aware validator; otherwise identify the existing path-scoped boundary command that can resolve the owning record without adding a new public interface. Align the T24, requirement-map, and PRF-007 proof-level labels and update the planned evidence reference. Then request test-spec-review R4.
needs-decision rationale: none; UBR-R021 already defines the authority distinction and the approved plan assigns compatibility validation to M2.

## Review dimensions

| Dimension | Verdict | Evidence |
| --- | --- | --- |
| Governing-contract alignment | block | T24 reduces the UBR-R021 lifecycle-contract predicate to pointer syntax. |
| Requirement coverage | block | R021 is mapped, but its decisive stage-owned versus non-stage-owned authority partition lacks direct negative proof. |
| Example coverage | pass | E1 through E6 are unchanged and retain their approved mappings. |
| Negative and boundary coverage | block | Before-pointer, outside-section, and duplicate cases are named, but non-stage-owned owner-pointer use is not rejected. |
| Proof-level adequacy | concern | T24 is labeled integration while its coverage and PRF-007 rows label the proof contract. |
| Milestone mapping | pass | T24, CMD06, BND-COMPAT-001, and M2 remain owner-aligned. |
| Command validity | concern | CMD06 exists, but the planned proof must identify its path-aware seam for resolving the referenced change record. |
| Fixture and data design | block | The fixture does not require the change record that owns the lifecycle-contract distinction. |
| Manual-proof boundary | pass | The outcome is locally automatable; no manual proof is needed. |
| Observability | pass | T24 requires a bounded marker-placement failure, though the lifecycle-authority case still must be added. |
| Determinism and isolation | pass | Temporary repository-local feature and change-record fixtures can prove the outcome without network or mutable external state. |
| Scope and non-goals | pass | The amendment adds no new command, lifecycle writer, publisher, or historical migration. |
| Execution economics | pass | One focused T24 case in the existing boundary suite is proportional. |
| Traceability | block | The failure claim about lifecycle authority is not linked to a fixture mutation or step, and proof-level labels disagree. |
| Implementation handoff | block | Implementation would have to invent how lifecycle governance is distinguished from a syntactically valid pointer. |

## Exact proof-map gap

The structural proof map is valid and now includes UBR-R021, BND-COMPAT-001, AC-UBR-013, and EC11. The remaining gap is semantic: no T24 scenario proves that the owner-pointer form derives authority from `lifecycle_contract: stage-owned-change-local-v1` rather than from the pointer's presence alone.

## Recommendation

Revise T24 and its linked proof rows using the safe resolution path, then request test-spec-review R4. This direct review is isolated and does not edit the test spec, start implementation, modify workflow routing or milestone state, or claim test execution, verification, branch, or PR readiness.
