# Proposal Review R2

Review ID: proposal-review-r2
Stage: proposal-review
Round: 2
Reviewer: User-provided proposal-review result
Target: docs/proposals/2026-07-27-portable-boundary-first-capability-for-published-skills.md
Status: changes-requested
Original review source: User-provided proposal-review result dated 2026-07-27.
Material findings: PBF-PR1, PBF-PR2, PBF-PR3, PBF-PR4
Architecture assessment: required
Scope-preservation result: pass with revisions
Immediate next stage: proposal revision
Automatic downstream handoff: none

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PBF-PR1, PBF-PR2, PBF-PR3, PBF-PR4
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/reviews/proposal-review-r2.md
- Review log: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-log.md
- Review resolution: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-resolution.md#proposal-review-r2
- Open blockers: PBF-PR1, PBF-PR2, PBF-PR3, and PBF-PR4
- Immediate next stage: proposal revision

## Material Findings

## Finding PBF-PR1

Finding ID: PBF-PR1
Severity: major
Location: docs/proposals/2026-07-27-portable-boundary-first-capability-for-published-skills.md, Scope budget, Recommended Direction, and Open Questions
Evidence: The proposal makes a closed boundary vocabulary and portable record shape core scope but defers both to specification while claiming no direction-level question remains.
Required outcome: Define the minimum closed first-version dimensions, applicability states, boundary-record relationships, proof-record relationships, and example classifications.
Safe resolution path: Add a first-version portable contract using the eight reviewed dimensions, `applicable` and `not-applicable`, stable boundary and proof identities, hazard-selected interactions, and the three closed example classifications.
needs-decision rationale: none; the proposal author accepted the user-provided first-version model for this revision.

## Finding PBF-PR2

Finding ID: PBF-PR2
Severity: major
Location: docs/proposals/2026-07-27-portable-boundary-first-capability-for-published-skills.md, Scope budget, Recommended Direction, Ownership split, and Testing and Verification Strategy
Evidence: The claimed end-to-end set omits `plan` and `plan-review`, although planning owns milestone isolation, dependencies, rollback units, and proof timing; semantic completeness is assigned only to generic independent reviewers.
Required outcome: Include `plan` and `plan-review` and assign exact boundary-first responsibility to each governed authoring, review, implementation, and verification skill.
Safe resolution path: Govern the reviewed ten-skill set, begin the normative model at feature-spec authoring, and make `spec-review`, `plan-review`, `test-spec-review`, `code-review`, and `verify` own their distinct semantic judgments.
needs-decision rationale: none; the proposal author accepted the user-provided governed path and responsibility split for this revision.

## Finding PBF-PR3

Finding ID: PBF-PR3
Severity: major
Location: docs/proposals/2026-07-27-portable-boundary-first-capability-for-published-skills.md, Recommended Direction and Architecture Impact
Evidence: The proposal requires one shared reference and end-to-end parity but leaves the resource class and one-source projection model unsettled, affecting published-skill self-containment and drift risk.
Required outcome: Choose the shared resource class and canonical-to-skill-local packaging model before specification.
Safe resolution path: Use a versioned `READ` reference, one canonical source, deterministic projections under each governed skill's `references/`, stage-specific load conditions, and byte parity through generated, packed, and installed surfaces.
needs-decision rationale: none; architecture may select the exact canonical path, but the proposal author accepted the one-source deterministic-projection model.

## Finding PBF-PR4

Finding ID: PBF-PR4
Severity: major
Location: docs/proposals/2026-07-27-portable-boundary-first-capability-for-published-skills.md, Rollout and Rollback
Evidence: The proposal defers the activation marker, substantive-revision boundary, in-flight behavior, partial activation, and rollback treatment even though they determine public compatibility.
Required outcome: Define prospective activation, substantive revision, in-flight opt-in, no-partial-activation conditions, grandfathering, and rollback preservation.
Safe resolution path: Select `boundary_contract: boundary-first-v1`, enumerate substantive and non-substantive revisions, allow bounded pre-test-spec opt-in, prohibit mixed-skill activation, and preserve already accepted versioned artifacts after rollback.
needs-decision rationale: none; the proposal author accepted the user-provided activation model for this revision.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The example-first completeness problem and runtime-certification overreach are clear. |
| User value | pass | Installed-skill users receive a portable method without maintainer infrastructure. |
| Option diversity | pass | The options are materially distinct. |
| Decision rationale | pass | The portable contract is the correct direction. |
| Scope control | concern | Core vocabulary and activation still need proposal-level closure. |
| Architecture awareness | concern | The reference source and projection ownership are unsettled. |
| Testability | concern | Exact record identities and semantic-review owners are missing. |
| Risk honesty | pass | Boilerplate, Cartesian expansion, drift, overclaiming, and false blocking are named. |
| Rollout realism | block | Activation and substantive-revision compatibility are not deterministic. |
| Readiness for spec | block | Resolve PBF-PR1 through PBF-PR4. |

## Scope Preservation Review

- Scope-preservation result: pass with revisions.

The proposal preserves the portable capability, packaged reference,
deterministic structural validation, adapter parity, independent semantic
review, and runtime-certification exclusion. The revised proposal must settle
the reviewed contract details without reintroducing the abandoned runtime
machinery.

## Recommended Proposal Edits

- Add a closed first-version portable contract and explicit acceptance criteria.
- Expand the governed path to ten skills with exact stage-local responsibilities.
- Select a versioned `READ` reference and deterministic skill-local projection model.
- Define prospective activation, substantive revision, no-partial-activation, grandfathering, and rollback.

## Recommendation

- Recommendation: changes-requested. Preserve the portable direction, resolve PBF-PR1 through PBF-PR4 in the proposal, then perform proposal-review R3 before specification. This review is isolated and does not automatically start downstream work.
