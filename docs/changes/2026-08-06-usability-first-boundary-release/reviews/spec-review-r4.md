<!-- Template: spec-review-result-skeleton-v1 -->
<!-- Skill: spec-review -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/spec-review/SKILL.md -->

# Usability-First Boundary-First v0.4.0 Release Spec Review R4

Review ID: spec-review-r4
Stage: spec-review
Round: 4
Reviewer: Codex independent spec-review peer
Target: specs/usability-first-boundary-release.md
Review date: 2026-08-06
Status: changes-requested
Material findings: UBR-SR4-001
Immediate next stage: spec revision
Automatic downstream handoff: none

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: UBR-SR4-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/spec-review-r4.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md#spec-review-r4`
- Open blockers: UBR-SR4-001
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: Normalize the compatibility-migration applicability row and cited boundary definitions before spec rereview.

UBR-R021 supplies the previously missing normative authority for the stage-owned owner-pointer marker form while retaining the PBF-R002 status form for non-stage-owned specs. The amendment cannot be approved because its normalized boundary record assigns different governing requirement sets to one applicability row and its two cited boundary definitions.

## Findings

## Finding UBR-SR4-001

Finding ID: UBR-SR4-001
Severity: blocking
Location: `specs/usability-first-boundary-release.md`, compatibility-migration applicability row and `BND-COMPAT-001` / `BND-COMPAT-002` definitions
Evidence: The applicability row governs `UBR-R006, UBR-R007, UBR-R013, UBR-R015, UBR-R019, UBR-R021` through both boundaries, while `BND-COMPAT-001` omits `UBR-R021` and `BND-COMPAT-002` contains only `UBR-R021`. The feature-only structural validator reports `BFR-BOUNDARY-DEFINITION-MISMATCH` for both cited boundaries.
Required outcome: The compatibility-migration applicability row and every cited boundary definition use one coherent normalized ownership model, and feature-only boundary validation passes before downstream proof-map staleness is treated as the sole expected failure.
Safe resolution path: Prefer the smallest contract-valid shape, such as folding the UBR-R021 partitions, invariant, and outcomes into `BND-COMPAT-001` with the full applicability requirement set and removing `BND-COMPAT-002`; an alternative is acceptable only if every cited definition exactly matches the applicability requirements and does not overclaim ownership. Update spec-authoring evidence, run the feature-only structural check, and submit spec-review R5. Do not repair the test spec during spec revision.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Evidence |
| --- | --- | --- |
| requirement clarity | pass | UBR-R021 states the exact stage-owned owner-pointer form, ordering, count, legacy PBF-R002 form, and fail-closed placements. |
| normative language | pass | The amendment uses testable `MUST` clauses and explicitly distinguishes stage-owned from non-stage-owned feature specs. |
| completeness | changes-requested | The normative rule is complete, but the compatibility applicability row and both cited boundary definitions do not form a valid normalized record. |
| testability | changes-requested | AC-UBR-013 and EC11 are observable, but structural proof cannot pass while both compatibility boundary definitions disagree with their applicability row. |
| examples | pass | The marker-placement rule is exact enough to test directly; no new narrative example is required. |
| compatibility | pass | The amendment explicitly replaces PBF-R002 placement only for stage-owned specs and retains the legacy status form elsewhere. |
| observability | pass | Failure cases are bounded to ordering, governed-section placement, and exact-one occurrence. |
| security/privacy | pass | The metadata-only placement rule introduces no credential, network, or private-data surface. |
| non-goals | pass | The amendment does not add a lifecycle writer, new publication mechanism, or broader artifact migration. |
| acceptance criteria | pass | AC-UBR-013 directly covers both authorized forms and the named invalid placements. |

## Boundary-first semantic review

- UBR-R021 correctly closes the governing-authority gap recorded as UBR-PRFG-CR1-001 at the normative requirement level.
- The new stage-owned and legacy placement partitions are mutually distinguishable and fail closed.
- The normalized serialization is invalid because one applicability row cites two boundary definitions with different governing requirement subsets.
- No additional selected interaction is required: the change is a compatibility partition within one lifecycle-marker subject, not a new cross-boundary hazard.

## Prior finding reconciliation

- `UBR-PRFG-CR1-001`: substantively addressed by UBR-R021, the PBF-R002 compatibility disposition, EC11, and AC-UBR-013; final closure remains blocked by UBR-SR4-001 because the governing boundary record is not structurally valid.
- The amendment does not address `UBR-PRFG-CR1-002` or `UBR-PRFG-CR1-003`; both remain implementation-stage review-resolution work.

## Exact wording suggestions

The preferred minimal correction is to give the compatibility applicability row one cited boundary, extend that boundary's governing requirement set through UBR-R021, incorporate the stage-owned and non-stage-owned marker partitions and outcomes, and remove the second boundary. Equivalent wording is acceptable if it satisfies the normalized exact-set contract without weakening UBR-R021.

## Routing and readiness

The specification requires revision and spec-review R5. This direct review is isolated and starts no downstream stage automatically.

The current test spec remains downstream-stale: it identifies spec-review R3 and does not map UBR-R021, AC-UBR-013, BND-COMPAT-002, or EC11. That is a test-spec handoff after a later approved spec review, not a defect to repair during this spec-review. Eventual test-spec readiness is therefore not-ready.
