# Review Resolution: Boundary-First Proof Modeling for Published Lifecycle Skills

## Summary

Closeout status: open

- Review closeout: code-review-m1-r1
- Review closeout: code-review-m1-r2 open
- Review closeout: spec-review-r3 open
- Review closeout: spec-review-r4 open
- Review closeout: spec-review-r5 open
- Review closeout: spec-review-r6 open
- Review closeout: spec-review-r7 open
- Review closeout: spec-review-r8 open
- Review closeout: spec-review-r9 open
- Review closeout: spec-review-r10 open
- Review closeout: spec-review-r11 open
- Review closeout: spec-review-r12 open
- Review closeout: spec-review-r13
- Review closeout: architecture-review-r3
- Review closeout: architecture-review-r4
- Review closeout: plan-review-r3
- Review closeout: plan-review-r4
- Review closeout: plan-review-r5
- Review closeout: test-spec-review-r3
- Review closeout: test-spec-review-r4
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
- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `spec-review-r1`, `spec-review-r2`, `architecture-review-r1`, `architecture-review-r2`, `plan-review-r1`, `plan-review-r2`, `test-spec-review-r1`, `test-spec-review-r2`, `code-review-m1-r1`, `code-review-m1-r2`, `spec-review-r3`, `spec-review-r4`, `spec-review-r5`, `spec-review-r6`, `spec-review-r7`, `spec-review-r8`, `spec-review-r9`, `spec-review-r10`, `spec-review-r11`, `spec-review-r12`, `spec-review-r13`, `architecture-review-r3`, `architecture-review-r4`, `plan-review-r3`, `plan-review-r4`, `plan-review-r5`
- Findings resolved: 29
- Unresolved findings: 2
- Current result: M1 R2 retained BFP-M1-CR4 and BFP-M1-CR7; M1 remains resolution-needed.

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
| BFP-M1-CR1 | accepted | resolved | Enforce stable unique example evidence IDs and per-reference requirement ownership. |
| BFP-M1-CR2 | accepted | resolved | Freeze exact incident ID, omission class, and owning gate. |
| BFP-M1-CR3 | accepted | resolved | Enforce the complete legacy/v1 marker and scope matrix. |
| BFP-M1-CR4 | accepted | open | Enforce byte identity plus tracked-or-current-change-local evidence provenance. |
| BFP-M1-CR5 | accepted | resolved | Canonicalize capability-report serialization. |
| BFP-M1-CR6 | accepted | resolved | Use a closed boundary-state envelope evaluated independently of fixture labels by the shared stage-gate evaluator. |
| BFP-M1-CR7 | accepted | open | Implement the exact R28y trace, snapshot, review-bundle, evidence, inventory, and formula contract. |
| BFP-SR3-1 | accepted | resolved | Incident derivation now requires exactly one field/value trigger and a trigger-free contrast. |
| BFP-SR3-2 | accepted | resolved | Trace observations, formal-review bundles, output capture, inventory, and terminal branches are deterministic. |
| BFP-SR3-3 | accepted | resolved | Filesystem inputs, typed dependencies, manifests, result identities, and report projection are bound losslessly. |
| BFP-SR9-1 | accepted | resolved | A standalone hermetic harness binds immutable runs to complete packages, instructions, contracts, components, and invocation profile inputs. |
| BFP-AR3-1 | accepted | resolved | Durable publication installs the run before the fsynced receipt and atomic pointer, then fsyncs the parent and reconciles cleanup. |
| BFP-AR3-2 | accepted | resolved | The parent attests the runtime sandbox and keeps opaque authentication outside child authority and durable evidence. |
| BFP-AR3-3 | accepted | resolved | The ADR records rejected hermetic-runtime alternatives and operational consequences. |
| BFP-PL4 | accepted | resolved | Preserve approved R28y M1-M4 ownership and keep runtime feasibility as a pre-harness promotion gate. |
| BFP-PL5 | accepted | resolved | Name exact evidence inputs, outputs, production/validation commands, promotion receipts, and failure stops. |
| BFP-TSR3-1 | accepted | resolved | Expand T48-T50 so every closed manifest, instruction, contract, profile, baseline, and input-set field has explicit positive and negative proof. |

## Finding Details

### code-review-m1-r2

M1 R2 introduced no new finding IDs. It confirmed BFP-M1-CR1,
BFP-M1-CR2, BFP-M1-CR3, BFP-M1-CR5, and BFP-M1-CR6 resolved, and retained
BFP-M1-CR4 and BFP-M1-CR7 as open because evidence provenance and the exact
R28y synthetic trace contract remain incomplete.

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

### code-review-m1-r1

#### BFP-M1-CR1 - False traceability and invalid regression identities

Finding ID: BFP-M1-CR1
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution M1
Decision owner: approved R28s, R28u, and R28w contract
Decision needed: none
Required outcome: Bind proof requirements to referenced boundary ownership and enforce stable unique regression and discovery IDs.
Chosen action: Apply the reviewer-provided declared-safe recipe after all M1 decisions are settled.
Rationale: Direct probes accepted unrelated known requirements and malformed or duplicate example evidence IDs.
Validation target: code-review-m1-r2
Validation evidence: Stable/duplicate ID, unrelated-known requirement, and mixed-reference negative regressions pass in `scripts/test-boundary-proof.py`.

### spec-review-r5

No new material findings.
`spec-review-r5` resolved `BFP-SR3-1` and kept `BFP-SR3-2` and
`BFP-SR3-3` open for exact snapshot and operation-registry closure.

### spec-review-r6

No new material findings.
`spec-review-r6` confirmed the closed row schemas but kept `BFP-SR3-2` and
`BFP-SR3-3` open because candidate/input/output roles, behavior-workspace
inventory, historical evidence, typed-result identity, aggregate observations,
marker-absence selection, and canonical fixture paths were not yet
deterministic.

### spec-review-r7

No new material findings.
`spec-review-r7` confirmed trace and typed-result improvements but kept
`BFP-SR3-2` and `BFP-SR3-3` open because oracle labels could still drive
results, canonical review output was modeled as one file rather than a complete
formal-recording bundle, and manifest/baseline selectors were not uniquely
owned.

### spec-review-r8

No new material findings.
`spec-review-r8` confirmed oracle independence, formal-review bundle
membership, baseline authority, canonical manifests, result identities, and
the dependency graph, while retaining the two prior findings for an exact
review-evidence union, portable immutable-run publication, and disjoint
filesystem/typed selector representations.

### spec-review-r9

#### BFP-SR9-1 - Fresh validation cannot reproduce or safely reuse the published behavior run

Finding ID: BFP-SR9-1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Decision owner: approved immutable behavior-evidence direction
Decision needed: none
Required outcome: Separate one-shot behavior generation from deterministic recorded-run validation and bind run reuse to a complete current input-set identity.
Chosen action: Define generate and validate modes, exact input-set identity and pointer schemas, immutable-run validation, and interrupted-publication reconciliation.
Rationale: Random run paths and nondeterministic skill output make complete typed-result rerun equality impossible, while an unbound old pointer could accept stale evidence.
Validation target: spec-review-r13
Validation evidence: `spec-review-r13` approved the standalone harness, closed import policy, complete resource and instruction binding, observable invocation profile, and validation-only reuse.

### spec-review-r10

No new material findings.
`spec-review-r10` confirmed the generation-versus-validation split, post-commit
validation, pointer/run binding, dependency reconstruction, and inventory
rules, while retaining `BFP-SR9-1` for an immutable prior-pointer value and an
exact execution-affecting implementation manifest.

### spec-review-r11

No new material findings.
`spec-review-r11` confirmed inline prior-pointer recovery but retained
`BFP-SR9-1` because the manual implementation list omitted imported workflow
modules, governing repository instructions, and exact environment derivation.

### spec-review-r12

No new material findings.
`spec-review-r12` retained `BFP-SR9-1` because the proposed transitive closure
omitted participating skill resources and runtime-supplied instructions, could
not model the existing dynamic import path, and did not define a complete
static-import or observable runtime identity contract.

### spec-review-r13

No new material findings.
`spec-review-r13` approved the hermetic standalone harness contract and
resolved `BFP-SR9-1`.
Architecture must now place the child runtime, isolated workspace, package
assembly, invocation attestation, immutable publication, and recovery
responsibilities before the test specification is revised.

### architecture-review-r3

#### BFP-AR3-1 - Publication ordering contradicts the approved recovery contract

Finding ID: BFP-AR3-1
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture revision
Decision owner: approved R28y publication contract
Decision needed: none
Required outcome: Represent immutable-run installation before the fsynced prepared receipt and atomic pointer replacement.
Chosen action: Correct runtime, component, ADR, and diagram sequencing and state that the receipt provides recovery rather than joint atomicity.
Rationale: A receipt written before run installation can name a missing run after a crash.
Validation target: architecture-review-r4
Validation evidence: `architecture-review-r4` approved the exact run, receipt, pointer, fsync, reconciliation, and cleanup sequence.

#### BFP-AR3-2 - Child-runtime trust is asserted but not enforceably owned

Finding ID: BFP-AR3-2
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture revision
Decision owner: approved hermetic invocation contract
Decision needed: none
Required outcome: Assign confinement, profile attestation, and secret-free authentication to a trusted boundary outside child self-report.
Chosen action: Use a parent-verified runtime-native sandbox or parent tool broker, opaque runtime-owned control-plane credentials, and non-secret attestation.
Rationale: Workspace copying and child-returned observations do not prove confinement.
Validation target: architecture-review-r4
Validation evidence: `architecture-review-r4` approved parent-observed sandbox attestation and private runtime-only authentication.

#### BFP-AR3-3 - The ADR omits the new durable architecture alternatives

Finding ID: BFP-AR3-3
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture revision
Decision owner: approved standalone harness direction
Decision needed: none
Required outcome: Preserve the rejected dependency, invocation, access-log, and network alternatives plus operational consequences.
Chosen action: Expand ADR alternatives and consequences for the hermetic runtime decision.
Rationale: Future maintainers need the rationale that prevents reintroduction of unsafe designs.
Validation target: architecture-review-r4
Validation evidence: `architecture-review-r4` approved the expanded ADR alternatives and consequences.

### architecture-review-r4

No new material findings.
`architecture-review-r4` approved the hermetic child-runtime trust boundary,
the exact recoverable publication sequence, the expanded ADR rationale, and
the aligned C4 views.

### plan-review-r3

#### BFP-PL4 - Five milestones conflict with the approved R28y phase contract

Finding ID: BFP-PL4
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan revision
Decision owner: approved R28y phase contract
Decision needed: none
Required outcome: Restore M1-M4 ownership while retaining feasibility before full harness or skill mutation.
Chosen action: Keep M1 deterministic; make `check-environment` the first bounded M2 implementation slice; run it before any other harness or skill mutation; keep upstream behavior in M2, preservation in M3, and aggregation in M4.
Rationale: Plan sequencing cannot renumber explicit normative phase ownership.
Validation target: plan-review-r5
Validation evidence: `plan-review-r5` approved the minimal preflight as the first bounded M2 slice and the M2-only evidence and failure stop.

#### BFP-PL5 - Evidence creation and promotion commands are incomplete

Finding ID: BFP-PL5
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan revision
Decision owner: approved R28y evidence contract
Decision needed: none
Required outcome: Make every evidence transition executable and independently promotable.
Chosen action: Add exact production and validation commands, output paths, pre-mutation baseline timing, failure stops, code-review promotion gates, tracked adapter input, four durable parity outputs, and release validation/test commands.
Rationale: Validation of an existing artifact does not define how current evidence is produced.
Validation target: plan-review-r5
Validation evidence: `plan-review-r5` approved the exact M4 adapter input, durable parity outputs, release fixtures, release tests, release validation, and promotion boundaries.

### plan-review-r4

No new material findings.
`plan-review-r4` partially resolved `BFP-PL4` and `BFP-PL5`; the exact retained
gaps are recorded in the R4 review and the original finding dispositions above.

### plan-review-r5

No new material findings.
`plan-review-r5` resolved `BFP-PL4` and `BFP-PL5` and approved the plan for
matching test-spec revision.

### test-spec-review-r3

#### BFP-TSR3-1 - Hermetic input-closure negative proof is not field-complete

Finding ID: BFP-TSR3-1
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec revision
Decision owner: approved R28y contract
Decision needed: none
Required outcome: Map every closed hermetic input field, selector, and format rule to explicit positive and negative proof.
Chosen action: Expand T48-T50 with exact field mutation matrices for manifest, instruction, contract, invocation profile, baseline, and input-set records.
Rationale: Aggregate class wording can pass while one normative closed field or selector remains unchecked.
Validation target: test-spec-review-r4
Validation evidence: `test-spec-review-r4` approved the exact field mutation matrices and M1-M4 regression scan.

### test-spec-review-r4

No new material findings.
`test-spec-review-r4` resolved `BFP-TSR3-1` and approved implementation
handoff under the existing separate implementation authorization.

### spec-review-r3

#### BFP-SR3-1 - Incident replay derivation is incomplete

Finding ID: BFP-SR3-1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Decision owner: approved incident-replay direction
Decision needed: none
Required outcome: Freeze field/value triggers, valid contrasts, first gates, and diagnostic families.
Chosen action: Add one exact incident rule table and make fixture labels non-authoritative expectations.
Rationale: The first amendment still required evaluator-authored mappings.
Validation target: spec-review-r5
Validation evidence: `spec-review-r5` confirmed exact-one trigger lookup, trigger-free contrast, current/non-current identity, and exact diagnostic equality.

### spec-review-r4

No new material findings.
`spec-review-r4` kept `BFP-SR3-1`, `BFP-SR3-2`, and `BFP-SR3-3` open because
their first correction remained incomplete.

#### BFP-SR3-2 - Simple-change observations are not computable

Finding ID: BFP-SR3-2
Disposition: accepted
Status: open
Owner: spec author
Owning stage: spec revision
Decision owner: approved simple-change workflow direction
Decision needed: none
Required outcome: Define trace shape, linkage, outcomes, correction events, inventory, and formulas.
Chosen action: Add exact trace and metric contracts plus malformed contrasts.
Rationale: Named observations without algorithms permit incompatible implementations.
Validation target: spec-review-r4
Validation evidence: pending

#### BFP-SR3-3 - Evidence is not operation-bound

Finding ID: BFP-SR3-3
Disposition: accepted
Status: open
Owner: spec author
Owning stage: spec revision
Decision owner: approved evidence-bound report direction
Decision needed: none
Required outcome: Bind every executed row to a current operation-specific receipt.
Chosen action: Add exact evidence receipt fields and cross-row substitution rejection.
Rationale: A current hash alone authenticates bytes, not relevance.
Validation target: spec-review-r4
Validation evidence: pending

#### BFP-M1-CR2 - Incident omission classes are not frozen

Finding ID: BFP-M1-CR2
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution M1
Decision owner: approved R28x registry
Decision needed: none
Required outcome: Freeze exact incident IDs, omission classes, and gates.
Chosen action: Replace the gate-only mapping with the exact immutable R28x registry and add per-field mutation tests.
Rationale: A changed non-empty omission description currently passes.
Validation target: code-review-m1-r2
Validation evidence: Every closed omission/gate/diagnostic mutation fails in the focused suite.

#### BFP-M1-CR3 - Legacy parity accepts partial marker state

Finding ID: BFP-M1-CR3
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution M1
Decision owner: approved R28r matrix
Decision needed: none
Required outcome: Synchronize marker presence, version, scope presence, and scope equality.
Chosen action: Implement the complete closed parity matrix and contrast tests.
Rationale: Partial and mismatched legacy records currently pass.
Validation target: code-review-m1-r2
Validation evidence: The full marker/scope contrast matrix passes in the focused suite.

#### BFP-M1-CR4 - Report evidence identity is undefined

Finding ID: BFP-M1-CR4
Disposition: accepted
Status: open
Owner: initiative owner
Owning stage: owner decision before review-resolution M1
Decision owner: initiative owner
Decision needed: none; the user authorized the best contract correction on 2026-07-26.
Required outcome: Evidence validation rejects missing, unsafe, stale, substituted, non-regular, and wrong-kind references.
Chosen action: Use `{path, identity}` evidence references bound to repository-relative regular files and current raw-byte SHA-256; use a closed `{code, detail}` blocker for not-run rows.
Rationale: The approved implementation contract requires current evidence but does not define its persisted identity or blocking-reason shape.
Validation target: code-review-m1-r3
Validation evidence: M1 R2 confirmed byte-identity and blocker checks but reproduced acceptance of untracked non-change-local evidence.

#### BFP-M1-CR5 - Report bytes depend on caller mapping order

Finding ID: BFP-M1-CR5
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution M1
Decision owner: approved deterministic report contract
Decision needed: none
Required outcome: Serialize semantically equivalent reports to identical bytes.
Chosen action: Canonicalize report mapping order and add permutation tests.
Rationale: Reordering an accepted checks mapping changes output bytes.
Validation target: code-review-m1-r2
Validation evidence: Reordered equivalent mappings serialize byte-identically.

#### BFP-M1-CR6 - Incident corpus is not executable

Finding ID: BFP-M1-CR6
Disposition: accepted
Status: resolved
Owner: initiative owner
Owning stage: owner decision before review-resolution M1
Decision owner: initiative owner
Decision needed: none; the user authorized the best contract correction on 2026-07-26.
Required outcome: Every exact incident is detected no later than its owning gate with escape and sibling-bypass evidence.
Chosen action: Use the closed R28x boundary-state envelope and a shared evaluator that derives stage and diagnostic without reading expected fixture labels.
Rationale: The approved implementation contract freezes the incidents but does not assign a payload or harness owner.
Validation target: code-review-m1-r2
Validation evidence: Eight canonical incident envelopes replay through the shared state evaluator; label changes do not drive results.

#### BFP-M1-CR7 - Simple-change workflow evidence is asserted

Finding ID: BFP-M1-CR7
Disposition: accepted
Status: open
Owner: initiative owner
Owning stage: owner decision before review-resolution M1
Decision owner: initiative owner
Decision needed: none; the user authorized the best contract correction on 2026-07-26.
Required outcome: Derive applicable-only proof mapping, artifact count, false blocking, and correction cycles from the same workflow path.
Chosen action: Use the shared structural evaluator to compute a four-stage trace with identities, diagnostics, correction events, artifact count, false blocking, and applicable-only proof mapping.
Rationale: The approved implementation contract states the measurements but not the executable trace boundary.
Validation target: code-review-m1-r3
Validation evidence: M1 R2 reproduced incomplete event/snapshot/bundle grammar and overbroad artifact subtraction.
