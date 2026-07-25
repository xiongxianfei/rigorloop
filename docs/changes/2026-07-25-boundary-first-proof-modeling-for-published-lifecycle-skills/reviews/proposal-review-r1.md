# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Codex proposal-review skill
Target: docs/proposals/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills.md
Status: changes-requested
Original review source: Codex proposal-review invocation on 2026-07-25.
Material findings: BFP-PR1, BFP-PR2, BFP-PR3, BFP-PR4
Architecture assessment: required after specification
Scope-preservation result: pass
Immediate next stage: proposal revision
Automatic downstream handoff: none

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: `BFP-PR1`, `BFP-PR2`, `BFP-PR3`, `BFP-PR4`
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md
- Review resolution: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md
- Open blockers: first-release baseline, taxonomy extension, adoption cutover, and measurable success gates
- Immediate next stage: proposal revision

## Material Findings

## Finding BFP-PR1

Finding ID: BFP-PR1
Severity: major
Location: Scope budget, Lifecycle Ownership, Rollout and Rollback, and Dependency and Sequencing
Evidence: The proposal assigns boundary-first responsibilities to every lifecycle stage and classifies all published lifecycle skill behavior updates as one `same-slice dependency`, but it does not identify the exact first-release skill set or the evidence that makes the new capability baseline complete. The rollout says to update “affected lifecycle skills” and then establish the baseline, while progressive disclosure remains blocked on that undefined event.
Required outcome: Define a closed first-release surface and a deterministic capability-baseline completion predicate, while routing remaining lifecycle-skill work as named later slices or explicitly unaffected surfaces.
Safe resolution path: Select the smallest end-to-end gate chain that can solve the observed problem, name every included skill and contract surface, name any deferred or unchanged skill with rationale, and define baseline completion in terms of approved contracts, implemented public-skill behavior, adapter parity, incident-replay proof, clean required reviews, and no open material findings.
needs-decision rationale: The proposal owner must choose the first-release product boundary and the minimum evidence required before the paused progressive-disclosure proposal may resume.

## Finding BFP-PR2

Finding ID: BFP-PR2
Severity: major
Location: Boundary Completeness Model and Mechanical and Judgment Boundaries
Evidence: The proposal calls the core boundary-dimension inventory closed and proposes validator rejection of unknown values, while also reserving reviewer judgment for undiscovered domain-specific dimensions. It does not say whether feature-specific dimensions may extend the core inventory, how extensions are identified, or how validators distinguish an invalid core value from a legitimate extension.
Required outcome: Define the relationship between mandatory closed core dimensions and feature-specific extensions before the schema is delegated to specification.
Safe resolution path: Keep the core dimension IDs closed and mandatory, add a separately represented namespaced extension mechanism with stable identity and rationale, prohibit a catch-all `other` value from satisfying a core dimension, and fail closed on unknown core IDs while allowing structurally valid extensions for semantic review.
needs-decision rationale: The proposal owner must decide whether extensions are supported and where their identity and validation boundary live; otherwise the spec author would choose a compatibility and extensibility policy.

## Finding BFP-PR3

Finding ID: BFP-PR3
Severity: major
Location: Compatibility behavior and Open Question 8
Evidence: The proposal says active work at adoption records whether it adopts the new model or finishes under its prior contract, but it leaves the adoption rule to the specification. It does not identify the decision owner, cutover event, artifact that records the choice, or whether partial adoption across spec, test spec, skills, and validators is valid.
Required outcome: Settle a deterministic prospective cutover and forbid mixed partial adoption before specification.
Safe resolution path: Make the accepted specification's effective revision the cutover; require newly authored or substantively revised behavior specs after that point to use the new model; allow already approved active initiatives to finish under their reviewed contract unless the owner explicitly opts in through synchronized spec and test-spec revision; and prohibit partial opt-in that claims the new gate without all required owners and proof.
needs-decision rationale: The proposal owner must select the compatibility policy and opt-in authority because this determines which active changes are blocked or grandfathered.

## Finding BFP-PR4

Finding ID: BFP-PR4
Severity: major
Location: Goals, Testing and Verification Strategy, Scope budget, and Risks and Mitigations
Evidence: The proposal's user value is reducing late boundary discovery and avoidable review cycles, but it defers review-efficiency metrics and defines no first-release success or stop condition for added authoring and review cost. Incident replay is proposed, yet the proposal does not say how much of the seeded omission corpus must move before code-review handoff or what evidence would show the process became ceremony without improving detection.
Required outcome: Define measurable first-release value, preservation, and cost guardrails without using raw finding count as a quota.
Safe resolution path: Require complete detection of the selected seeded omission classes no later than the owning pre-code-review gate, zero regression in existing claim and review behavior, explicit measurement of direct-proof escape and failed-remediation rates, and a bounded author/reviewer overhead measure with a stop-or-revise rule when the pilot adds recurring structure without earlier detection.
needs-decision rationale: The proposal owner must choose the pilot success and rollback signals; exact numeric thresholds may be finalized in the spec or test spec after the metric families and stop policy are fixed here.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The proposal distinguishes example-driven implementation from the legitimate use of examples and ties the problem to observed trust, state, recovery, and composition escapes. |
| User value | concern | Earlier detection and fewer failed remediations are valuable, but the first-release value and cost guardrails are not yet measurable. |
| Option diversity | pass | Do nothing, checklist-only, universal new artifact, existing-owner integration, and example-generated tests are materially different options. |
| Decision rationale | pass | Embedding normative boundaries in specs and proof in test specs is consistent with repository source-of-truth ownership. |
| Scope control | block | The broad lifecycle table and one `same-slice dependency` do not establish the exact first-release skill or capability-baseline boundary. |
| Architecture awareness | pass | The proposal separates specs, test specs, public skills, validators, and semantic review, and correctly triggers architecture assessment. |
| Testability | block | Boundary replay is promising, but taxonomy extension and success/stop semantics remain underdefined. |
| Risk honesty | pass | Boilerplate, semantic overclaim, historical invalidation, scope expansion, overfitting, and cross-spec contradiction are identified. |
| Rollout realism | block | Active-initiative cutover and the event that permits progressive-disclosure resumption are not deterministic. |
| Readiness for spec | block | Resolve `BFP-PR1` through `BFP-PR4` before specification. |

## Scope Preservation Review

- Scope-preservation result: pass.

The proposal preserves every initial user goal: it solves boundary modeling
before progressive disclosure, keeps examples subordinate rather than removing
them, applies the direction to published lifecycle skills, distinguishes
exhaustive partitions from infeasible Cartesian testing, and keeps the
progressive-disclosure initiative paused.

The scope budget is present and routes historical retrofit, progressive
disclosure, review-efficiency follow-up, validation, and the rejected standalone
artifact option.
`BFP-PR1` concerns the unresolved first-release boundary inside the declared
scope, not a missing initial goal.

## Blocking Questions

1. Which exact published skills and governing surfaces constitute the first
   release?
2. What exact evidence establishes the boundary capability baseline and permits
   progressive-disclosure review to resume?
3. Are feature-specific boundary dimensions permitted in addition to the
   mandatory closed core, and how are they represented?
4. Which active initiatives are grandfathered, who may opt in, and what prevents
   partial adoption?
5. Which metric families and stop policy demonstrate earlier detection without
   turning the workflow into ceremony?

## Recommended Proposal Edits

- Add a first-release scope table naming every included, deferred, and
  intentionally unaffected lifecycle skill and contract surface.
- Add a capability-baseline completion predicate and make it the sole resume
  dependency for progressive disclosure.
- Split the taxonomy into closed mandatory core IDs and explicitly represented
  feature-specific extensions.
- Replace Open Question 8 with a decided adoption and opt-in policy.
- Add first-release value, preservation, overhead, and stop-or-revise gates.
- Keep exact field schemas, fixture IDs, numeric thresholds, and validator
  implementation details for the specification and test specification.

## Recommendation

- Recommendation: changes-requested. The central direction is sound, vision-aligned, and worth pursuing, but the proposal is not ready for specification until the first-release baseline, taxonomy extension policy, adoption cutover, and measurable success gates are deterministic. This review is isolated and does not automatically revise the proposal or start `spec`.
