# Review Resolution: Boundary-First Proof Modeling for Published Lifecycle Skills

## Summary

Closeout status: closed

- Review closeout: proposal-review-r1
- Review closeout: proposal-review-r2
- Reviews covered: `proposal-review-r1`, `proposal-review-r2`
- Findings resolved: 4
- Unresolved findings: 0
- Current result: `proposal-review-r2` approved the revised direction and confirmed all four R1 findings resolved.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| BFP-PR1 | accepted | resolved | The first release is closed to eight named skills and a complete evidence predicate controls progressive-disclosure resumption. |
| BFP-PR2 | accepted | resolved | Mandatory closed core dimensions and optional namespaced extensions now have distinct compatibility and validation behavior. |
| BFP-PR3 | accepted | resolved | Public activation is prospective at the first complete release; approved initiatives are grandfathered and synchronized opt-in forbids partial adoption. |
| BFP-PR4 | accepted | resolved | Seeded detection, preservation, false-blocking, ownership, artifact-count, and correction-cycle gates now control rollout. |

## Finding Details

### proposal-review-r1

#### BFP-PR1 - The first-release capability baseline is undefined

Finding ID: BFP-PR1
Disposition: accepted
Status: resolved
Owner: proposal owner
Owning stage: proposal revision
Decision owner: proposal owner
Decision needed: Select the closed first-release skill and contract surface and the capability-baseline completion predicate.
Required outcome: Define a closed first-release skill and contract surface plus the evidence that establishes the implemented capability baseline and permits progressive-disclosure review to resume.
Chosen action: Limited the first release to `spec`, `spec-review`, `test-spec`, `test-spec-review`, `implement`, `code-review`, `verify`, and `workflow`, plus their two governing specs, matching test specs, required resources, validators, fixtures, selectors, adapters, and incident corpus. Added a closed capability-baseline completion predicate and routed the other six lifecycle skills to a separate implementation slice.
Rationale: The current all-stage responsibility table and generic “affected lifecycle skills” rollout leave product scope and dependency completion for the spec author to choose.
Validation target: `proposal-review-r2`
Validation evidence: Proposal sections `First-release surface`, `Capability-baseline completion`, `Scope budget`, `Rollout and Rollback`, and `Next Artifacts`.

#### BFP-PR2 - Closed core and feature-specific extension semantics conflict

Finding ID: BFP-PR2
Disposition: accepted
Status: resolved
Owner: proposal owner
Owning stage: proposal revision
Decision owner: proposal owner
Decision needed: Select the supported feature-specific extension policy and its validation boundary.
Required outcome: Define whether and how feature-specific boundary dimensions extend the mandatory closed core, including fail-closed validator behavior.
Chosen action: Defined mandatory closed core IDs and applicability separately from optional stable namespaced extensions; prohibited `other`, prohibited extensions from satisfying core dimensions, required unknown core values to fail closed, and retained semantic review for structurally valid extensions.
Rationale: A closed core vocabulary cannot safely double as the complete domain vocabulary while semantic review remains responsible for discovering domain-specific dimensions.
Validation target: `proposal-review-r2`
Validation evidence: Proposal section `Boundary Completeness Model` and the corresponding Decision Log entry.

#### BFP-PR3 - Active-initiative adoption is not deterministic

Finding ID: BFP-PR3
Disposition: accepted
Status: resolved
Owner: proposal owner
Owning stage: proposal revision
Decision owner: proposal owner
Decision needed: Select the prospective cutover, grandfathering, opt-in authority, and no-partial-adoption policy.
Required outcome: Define the effective cutover, grandfathering, opt-in authority, synchronized artifact updates, and prohibition on partial adoption.
Chosen action: Selected public activation at the first released complete baseline, prospective `v1` adoption for new or substantively revised behavior specs, grandfathering for already approved specs, initiative-owner synchronized opt-in, version parity, and fail-closed rejection of partial adoption.
Rationale: Compatibility policy determines which active initiatives may proceed and cannot be invented during specification.
Validation target: `proposal-review-r2`
Validation evidence: Proposal sections `Expected Behavior Changes`, `Rollout and Rollback`, and Decision Log.

#### BFP-PR4 - First-release value and cost gates are not measurable

Finding ID: BFP-PR4
Disposition: accepted
Status: resolved
Owner: proposal owner
Owning stage: proposal revision
Decision owner: proposal owner
Decision needed: Select the first-release metric families, preservation gates, overhead guardrail, and stop-or-revise policy.
Required outcome: Define metric families and stop-or-revise behavior that demonstrate earlier boundary detection, preserve existing behavior, and bound added ceremony.
Chosen action: Added complete seeded-class pre-code-review detection, zero seeded direct-proof and sibling-remediation escapes, behavior and adapter preservation, one-owner and no-new-artifact gates, simple-fixture overhead bounds, explicit metric families, and stop-or-revise conditions.
Rationale: Incident replay alone does not decide whether the new process improved handoff quality enough to justify recurring authoring and review cost.
Validation target: `proposal-review-r2`
Validation evidence: Proposal section `First-release success and stop gates` and the corresponding Risks and Mitigations and Decision Log entries.

### proposal-review-r2

No material findings.
`proposal-review-r2` confirmed `BFP-PR1` through `BFP-PR4` resolved and approved
the proposal direction for owner acceptance and separate specification.
