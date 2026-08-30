# Spec Review R4: Consolidated Review Gates

Review ID: spec-review-r4
Stage: spec-review
Round: r4
Reviewer: Codex independent spec-review context
Target: `specs/consolidated-review-gates.md`
Reviewed artifact: `specs/consolidated-review-gates.md` at `sha256:9284fbeacd3aaaf1fc330f477e5c171c860b864435ea5eb7fec5be9ec9a99ad5`
Reviewed artifact path: specs/consolidated-review-gates.md
Reviewed artifact identity: sha256:9284fbeacd3aaaf1fc330f477e5c171c860b864435ea5eb7fec5be9ec9a99ad5
Review date: 2026-08-30
Recording status: recorded
Status: changes-requested
Material findings: CRG-SR5

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: CRG-SR5
- Open blockers: the byte-change invariant contradicts the explicit governed-operation invalidation boundary
- Immediate next stage: review-resolution, then spec correction and same-stage rereview
- Eventual test-spec readiness: not-ready until the lightweight package identity contract is internally coherent
- Stop condition: downstream architecture and implementation remain paused until the specification is revised and approved

## Recording

- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/spec-review-r4.md`
- Review log: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`
- Review resolution: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md`

## Governed settlement

- Settlement mode: governed-spec-entry
- Settlement status: changes-requested
- Governed change identity: `2026-08-28-consolidate-rigorloop-review-gates`

## Boundary review

- Boundary applicability: `boundary-first-v1` applicable; the temporal boundary contains the material contradiction below
- Boundary resources: `boundary-first-method-v1.md`, `boundary-first-feature-authoring-v1.md`
- Boundary blocker: CRG-SR5 affects `BND-STATE-001` and `BND-TEMPORAL-001`

## Automated review

- Automation mode: manual
- Automation evidence: focused requirement and invariant comparison
- Automation result: semantic contradiction found

## Findings

## Finding CRG-SR5

Finding ID: CRG-SR5
Severity: major
Location: CRG-R24; State and invariants; EC4; BND-TEMPORAL-001
Evidence: CRG-R24 deliberately limits automatic invalidation to a change recorded through a governed authoring operation and explicitly says direct edits are not automatically detected in the first slice. The State and invariants section instead says that any component byte change invalidates package review. That broader invariant would require reading or hashing document contents to detect direct edits, contradicting CRG-R22, CRG-R24, Observability, Security and privacy, Performance expectations, and the requested lightweight package model.
Required outcome: define one consistent invalidation boundary in which a governed member or upstream-review revision event marks an approved package `review-required`, while unrecorded direct edits are outside automatic first-slice detection and no content hash is introduced for package authority.
Safe resolution path: replace the byte-change invariant with a governed-revision-event invariant; clarify CRG-R24 so member revision recording and upstream review settlement are the two invalidation triggers; retain explicit member IDs, repository-relative paths, review IDs, lifecycle revision checks, and current package status as the complete first-slice authority model.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | changes requested | One invalidation trigger has contradictory scopes. |
| normative language | changes requested | “Any component byte change” overrules the narrower governed-operation wording unless corrected. |
| completeness | pass | The lightweight identity, authority, outcome, routing, and cutover surfaces are otherwise complete. |
| testability | changes requested | Direct-edit behavior has two incompatible expected results. |
| examples | pass | Examples otherwise align with explicit member maps and governed revision events. |
| compatibility | pass | The atomic cutover contract remains explicit. |
| observability | pass | Member IDs, paths, review IDs, status, blockers, targets, and next operation are directly visible. |
| security/privacy | pass | The intended contract avoids absolute paths and package content hashes. |
| non-goals | pass | Exact schema and command spelling remain architecture-owned. |
| acceptance criteria | changes requested | CRG-AC4 cannot have one result until the invalidation trigger is consistent. |

## Claim limitations

This review records one specification finding only. It does not revise the specification, approve architecture, update the plan or test specification, validate implementation, or claim branch or PR readiness.
