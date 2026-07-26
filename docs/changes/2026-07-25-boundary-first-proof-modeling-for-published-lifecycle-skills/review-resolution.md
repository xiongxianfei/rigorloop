# Review Resolution: Boundary-First Proof Modeling for Published Lifecycle Skills

## Summary

Closeout status: closed

- Review closeout: test-spec-review-r2
- Review closeout: test-spec-review-r1
- Review closeout: plan-review-r2
- Review closeout: plan-review-r1
- Review closeout: architecture-review-r2
- Review closeout: architecture-review-r1
- Review closeout: spec-review-r2
- Review closeout: spec-review-r1
- Review closeout: proposal-review-r1
- Review closeout: proposal-review-r2
- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `spec-review-r1`, `spec-review-r2`, `architecture-review-r1`, `architecture-review-r2`, `plan-review-r1`, `plan-review-r2`, `test-spec-review-r1`, `test-spec-review-r2`
- Findings resolved: 14
- Unresolved findings: 0
- Current result: `test-spec-review-r2` approved the corrected proof maps for implementation handoff.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| BFP-PR1 | accepted | resolved | The first release is closed to eight named skills and a complete evidence predicate controls progressive-disclosure resumption. |
| BFP-PR2 | accepted | resolved | Mandatory closed core dimensions and optional namespaced extensions now have distinct compatibility and validation behavior. |
| BFP-PR3 | accepted | resolved | Public activation is prospective at the first complete release; approved initiatives are grandfathered and synchronized opt-in forbids partial adoption. |
| BFP-PR4 | accepted | resolved | Seeded detection, preservation, false-blocking, ownership, artifact-count, and correction-cycle gates now control rollout. |
| BFP-SR1 | accepted | resolved | Exact version, scope, activation, and rollback markers are defined. |
| BFP-SR2 | accepted | resolved | Closed boundary and proof record shapes, IDs, and reference rules are defined. |
| BFP-SR3 | accepted | resolved | Eight fixtures and the versioned capability-report aggregate are frozen. |
| BFP-AR1 | accepted | resolved | Pure evaluation belongs to the typed model; only the validator serializes the report. |
| BFP-AR2 | accepted | resolved | Executable components are contained inside the validation-and-generation container. |
| BFP-PL1 | accepted | resolved | Status, handoff, and Readiness now satisfy the active-plan contract. |
| BFP-PL2 | accepted | resolved | Adapter and lifecycle commands are executable and exact. |
| BFP-PL3 | accepted | resolved | R28y report pass and R28o resumption are separate closeout predicates. |
| BFP-TSR1 | accepted | resolved | Canonical report validation begins in M4; M1 uses synthetic report fixtures. |
| BFP-TSR2 | accepted | resolved | Every manual procedure ID now resolves to a complete bounded proof contract. |

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

### spec-review-r1

#### BFP-SR1 - Version and activation evidence are not deterministic

Finding ID: BFP-SR1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Decision owner: accepted proposal and workflow contract
Decision needed: none
Required outcome: Define one exact artifact version marker and activation identity.
Chosen action: Add closed `legacy | v1` marker semantics and release activation evidence.
Rationale: Version parity and grandfathering cannot depend on inferred dates or prose.
Validation target: spec-review-r2
Validation evidence: `specs/rigorloop-workflow.md` R28r and R28z; `spec-review-r2`.

#### BFP-SR2 - Boundary and proof record shapes are incomplete

Finding ID: BFP-SR2
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Decision owner: accepted proposal and workflow contract
Decision needed: none
Required outcome: Define exact minimum fields, IDs, uniqueness, and references.
Chosen action: Add closed row contracts for core entries, extensions, examples, interactions, and proof mappings.
Rationale: Downstream artifacts need one interoperable trace model.
Validation target: spec-review-r2
Validation evidence: `specs/rigorloop-workflow.md` R28s through R28w; `spec-review-r2`.

#### BFP-SR3 - First-release fixtures and aggregate gate are not frozen

Finding ID: BFP-SR3
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Decision owner: accepted proposal and workflow contract
Decision needed: none
Required outcome: Define exact seeded IDs, report path, result vocabulary, and computed gate.
Chosen action: Add eight fixture IDs and one deterministic versioned report contract.
Rationale: Test-spec and implementation must operationalize the release gate rather than choose it.
Validation target: spec-review-r2
Validation evidence: `specs/rigorloop-workflow.md` R28p, R28x, and R28y; `specs/skill-contract.md` R56o; `spec-review-r2`.

### spec-review-r2

No material findings.
`spec-review-r2` confirmed `BFP-SR1` through `BFP-SR3` resolved and approved
the amendments for required architecture work.

### architecture-review-r1

#### BFP-AR1 - Capability evaluator ownership is incomplete

Finding ID: BFP-AR1
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture revision
Decision owner: approved specification and architecture author
Decision needed: none
Required outcome: Name one evaluator owner, its mutation behavior, and the only capability-report writer.
Chosen action: Assign pure aggregate evaluation to `scripts/boundary_proof_model.py` and report serialization to `scripts/validate-boundary-proof.py`.
Rationale: Planning must not invent a competing evaluator or report writer.
Validation target: architecture-review-r2
Validation evidence: canonical Building Block View, ADR decision, component diagram, and `architecture-review-r2`

#### BFP-AR2 - Component containment is ambiguous

Finding ID: BFP-AR2
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture revision
Decision owner: architecture package method
Decision needed: none
Required outcome: Place executable components inside the validation-and-generation container and keep repository siblings outside it.
Chosen action: Redraw the component diagram with an explicit script-container subgraph and consistent sibling-container roles.
Rationale: A flat peer graph obscures executable ownership and violates the intended C4 component view.
Validation target: architecture-review-r2
Validation evidence: `docs/architecture/system/diagrams/component-boundary-proof.mmd` and `architecture-review-r2`

### architecture-review-r2

No material findings.
`architecture-review-r2` confirmed `BFP-AR1` and `BFP-AR2` resolved and
approved the canonical architecture update and ADR for planning.

### plan-review-r1

#### BFP-PL1 - Active plan state is structurally invalid

Finding ID: BFP-PL1
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan revision
Decision owner: workflow state contract
Decision needed: none
Required outcome: Make the plan lifecycle-valid and keep live routing in one owner.
Chosen action: Add Change ID, normalize handoff fields, and remove routing from Readiness.
Rationale: Invalid or duplicated live state cannot safely drive downstream automation.
Validation target: plan-review-r2
Validation evidence: plan lifecycle validation and `plan-review-r2`

#### BFP-PL2 - Validation commands are not executable

Finding ID: BFP-PL2
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan revision
Decision owner: repository adapter and lifecycle contracts
Decision needed: none
Required outcome: Use runnable generated-adapter and explicit lifecycle validation commands.
Chosen action: Generate and validate temporary versioned adapter output and enumerate exact lifecycle paths.
Rationale: A reviewable plan must not defer command correctness to implementation.
Validation target: plan-review-r2
Validation evidence: M4 and Validation plan commands plus `plan-review-r2`

#### BFP-PL3 - Baseline closeout is ambiguous

Finding ID: BFP-PL3
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan revision
Decision owner: approved R28y-R28o contract
Decision needed: none
Required outcome: Separate report pass from the later resumption predicate.
Chosen action: Keep report generation in M4 and require later clean reviews, resolution closeout, explain-change, and verify for R28o.
Rationale: A report must not recursively depend on review of itself, and report pass alone cannot resume the paused proposal.
Validation target: plan-review-r2
Validation evidence: M4 expected result, Dependencies, Outcome, and `plan-review-r2`

### plan-review-r2

No material findings.
`plan-review-r2` confirmed `BFP-PL1` through `BFP-PL3` resolved and approved
the plan for test-spec authoring.

### test-spec-review-r1

#### BFP-TSR1 - Canonical report validation is required too early

Finding ID: BFP-TSR1
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec revision
Decision owner: approved plan
Decision needed: none
Required outcome: M1 uses synthetic report proof and M4 first requires the canonical report command.
Chosen action: Move CMD-BFP-2 first-required ownership to M4 and remove it from M1.
Rationale: A milestone cannot require a later milestone's canonical artifact.
Validation target: test-spec-review-r2
Validation evidence: `specs/rigorloop-workflow.test.md` command and milestone ledgers; `test-spec-review-r2`

#### BFP-TSR2 - Manual proof IDs are incomplete

Finding ID: BFP-TSR2
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec revision
Decision owner: test-spec-review contract
Decision needed: none
Required outcome: Every manual proof defines rationale, steps, environment, evidence, pass, failure, and owner.
Chosen action: Add complete manual-procedure tables to both active test specs.
Rationale: A stable ID without an executable proof contract is not traceable evidence.
Validation target: test-spec-review-r2
Validation evidence: both test specs' `Boundary-first manual procedures` tables; `test-spec-review-r2`

### test-spec-review-r2

No material findings.
`test-spec-review-r2` confirmed `BFP-TSR1` and `BFP-TSR2` resolved and
approved the active proof maps for test-driven M1 implementation.
