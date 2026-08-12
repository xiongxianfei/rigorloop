# Review Resolution: Spec-Review Skill Simplification

## Summary

Closeout status: open

Review closeout: proposal-review-r2

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`
- Findings resolved: 3
- Unresolved findings: 3
- Current result: proposal-review-r1 is closed; proposal-review-r2 requires proposal revision.

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `SRSIM-PR1` | accepted | resolved | Separated review kind, recording, governed settlement, and automation into closed authority axes with explicit side effects. |
| `SRSIM-PR2` | accepted | resolved | Defined one core result group and four conditional groups in the existing result asset. |
| `SRSIM-PR3` | accepted | resolved | Bound reference loading to the existing checked-revision activation owner and closed load order and grandfathering behavior. |
| `SRSIM-R2-PR1` | needs-decision | open | Proposal author must derive recording from review kind and remove the unsupported non-formal durable state. |
| `SRSIM-R2-PR2` | needs-decision | open | Proposal author must bind isolated recording to the existing contract and close its write set. |
| `SRSIM-R2-PR3` | needs-decision | open | Proposal author must make isolated-formal loaded-profile reduction the primary acceptance surface. |

## Finding details

### proposal-review-r1

#### SRSIM-PR1

Finding ID: SRSIM-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Replace the broad durable/formal predicates with independent review-kind, recording-mode, settlement-mode, and automation-mode axes and add a closed side-effect matrix.
Rationale: Every supported formal review must record evidence, while only exact same-change governed authority may settle the spec entry or enable workflow-managed automation.
Required outcome: Define exhaustive formal recording independently from governed settlement and automation authority.
Safe resolution path: Adopt the four-axis model recommended by `proposal-review-r1` and validate it through static profiles.
Validation target: Revised classification, profile, side-effect, recording-root, measurement, and scenario sections.
Validation evidence: The revised proposal defines all four axes, their implications, permitted side effects, and isolated formal review as the primary usage profile.

#### SRSIM-PR2

Finding ID: SRSIM-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Define the existing result asset as one universal core group plus recording, governed-settlement, boundary-review, and automated-review groups.
Rationale: Closed applicability keeps the existing asset as the sole layout owner without allowing it to decide policy.
Required outcome: Define core and conditional result groups with exact applicability and no policy ownership.
Safe resolution path: Adopt the group model recommended by `proposal-review-r1` and reconcile it with directly coupled asset contracts.
Validation target: Revised asset ownership, group table, omission behavior, blocked-data behavior, and scenarios.
Validation evidence: The revised proposal defines each group, its trigger, its structural fields, omission rules, blocker handling, and the prohibition on asset-owned policy.

#### SRSIM-PR3

Finding ID: SRSIM-PR3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Make the existing checked-revision contract and `specs/boundary-first-resources.yaml` the sole activation owners, with `spec-review` defining only consumption order.
Rationale: Simplification must preserve existing activation, grandfathering, projection, and parity behavior rather than creating a local competing predicate.
Required outcome: Define exact spec-review load order and cases under the existing activation owner.
Safe resolution path: Adopt the activation and load-order mapping recommended by `proposal-review-r1`.
Validation target: Revised boundary ownership, load order, grandfathering, late-discovery, missing-resource, and scenario sections.
Validation evidence: The revised proposal always runs the inline scan, loads the method before feature authoring, preserves non-substantive grandfathering, and stops on unknown substantive classification or missing required resources.

### proposal-review-r2

#### SRSIM-R2-PR1

Finding ID: SRSIM-R2-PR1
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Derive recording behavior from formal versus non-formal review classification.
Chosen action: pending proposal revision
Rationale: The current independent recording axis creates a non-formal durable state without a recording-procedure assembly.
Required outcome: Make formal review recording mandatory and non-formal durable evidence forbidden, with durable requests promoted to isolated formal review.
Safe resolution path: Adopt the simplified three-axis model from proposal-review-r2.
Validation target: Revised classification, resource-profile, side-effect, and scenario sections plus independent rereview.
Validation evidence: pending

#### SRSIM-R2-PR2

Finding ID: SRSIM-R2-PR2
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Bind isolated recording to the exact existing formal-review placement and artifact contract.
Chosen action: pending proposal revision
Rationale: Simplification cannot introduce an implicit lifecycle-root creation model.
Required outcome: Cite `R31a` through `R31n`, enumerate permitted isolated writes, forbid governed mutations, and define blocked recording.
Safe resolution path: Reuse the existing formal-review-recording contract without redefining it.
Validation target: Revised recording boundary, ownership, failure, and scenario sections plus independent rereview.
Validation evidence: pending

#### SRSIM-R2-PR3

Finding ID: SRSIM-R2-PR3
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Make primary formal loaded-context reduction an acceptance requirement.
Chosen action: pending proposal revision
Rationale: Main-file reduction alone can relocate rather than reduce the context loaded by every supported direct review.
Required outcome: Require lower loaded words and bytes for `SR1-isolated-formal`, one loaded owner per duplicate cluster, and separate profile and package reporting.
Safe resolution path: Adopt the closed simplification success criteria from proposal-review-r2.
Validation target: Revised success criteria, measurement assemblies, risks, and scenarios plus independent rereview.
Validation evidence: pending

## Shared validation evidence

| Validation area | Result | Notes |
| --- | --- | --- |
| Proposal revision inspection | pass | All three accepted findings have explicit proposal text and closed acceptance behavior. |
| Review artifact validation | pass | `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-12-spec-review-skill-simplification` passed. |
| Change metadata validation | pass | `python scripts/validate-change-metadata.py docs/changes/2026-08-12-spec-review-skill-simplification/change.yaml` passed. |
| Lifecycle consistency | pass | Explicit-path lifecycle validation passed for the revised proposal artifact pack. |
| Markdown readability | pass with advisory warnings | Validation passed for the revised proposal, resolution, and revision evidence; audit-only table and dense-prose warnings remain non-blocking. |

## Closeout checklist

- [x] Every material finding has a final disposition.
- [x] Every accepted finding has a chosen action.
- [x] Every accepted finding has proposal-level validation evidence.
- [x] No findings remain open.
