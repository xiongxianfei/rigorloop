# Proposal: Retire the Standalone Test-Spec Stage

## Challenge

RigorLoop currently requires specification, planning, and a separate test specification before implementation. The approved lightweight requirement-to-delivery model now assigns observable system behavior to specification and allocates system requirements and architecture responsibilities into delivery work through planning. A mandatory test-spec artifact overlaps both owners by repeating scenarios from the specification and reconnecting them to milestones, concrete tests, validation, and evidence.

That overlap creates synchronization work across three artifacts, separates verification thinking from milestone design, adds lifecycle and review state, and repeatedly loads related context. It can also let a plan appear ready before its milestone boundaries and integrated verification obligations have been challenged together.

The required property is not a separate `test-spec.md`. Before implementation begins, RigorLoop must know what behavior must be demonstrated, where that responsibility is allocated, and what evidence implementation must produce.

## Goals

This change should:

- remove `test-spec` as a mandatory artifact and lifecycle stage for new governed changes;
- retire the standalone test-spec authoring skill and the remaining standalone test-spec-review compatibility surface from the active workflow contract;
- preserve pre-implementation verification rigor without creating a replacement mandatory artifact or stage;
- strengthen specifications as the source of testable SR-level behavior, boundaries, failures, compatibility expectations, and important scenarios;
- strengthen plans as the delivery contract for SR allocation, engineering sequence, milestone verification, and complete-change verification;
- keep milestone decomposition driven primarily by safe engineering, dependencies, intermediate states, reversibility, risk, and reviewability;
- make Delivery Review jointly assess implementation readiness and planned verification adequacy;
- preserve lightweight traceability from SR to allocated work, verification objectives, concrete proof, and evidence;
- preserve specialist test-design methodology through conditionally loaded plan references; and
- reduce lifecycle ceremony, duplicated artifacts, and agent context while retaining historical evidence.

## Scope and non-goals

### In scope

The direction covers the contracts and active surfaces owned by `spec`, `plan`, `delivery-review`, and `test-spec`; remaining test-spec-review lifecycle compatibility; test-spec templates and references; workflow routing and lifecycle state; validation and fixtures; supported adapter packaging; and contributor documentation, examples, governance, and vision wording that describe a standalone test specification as part of the current chain.

### Initial intent treatment

| Initial goal | Treatment | Destination |
| --- | --- | --- |
| Remove the mandatory test-spec artifact and stage | in scope | Active workflow and lifecycle contract |
| Remove standalone test-spec and test-spec-review skills | in scope | Authored test-spec package and remaining active or compatibility review surfaces; already-retired published review entrypoints are not recreated |
| Strengthen specification behavior and scenario ownership | in scope | Specification contract and Design Review inputs |
| Strengthen milestone and change-level verification planning | in scope | Plan contract and Delivery Review criteria |
| Preserve engineering-led milestone decomposition | in scope | Plan contract |
| Preserve SR-to-evidence traceability with lightweight verification groups | in scope | Cross-artifact direction; exact representation belongs to Design and Delivery |
| Move specialist testing guidance under plan | in scope | Progressive-disclosure direction; exact reference organization belongs to Design |
| Preserve historical test-spec evidence without migration | in scope | Compatibility policy |
| Avoid a replacement proof artifact, verification stage, or one-test-per-SR rule | out of scope | Explicit non-goals below |

### Scope budget

| Work item | Treatment |
| --- | --- |
| Redistribute verification responsibility across specification, plan, and Delivery Review | core to this proposal |
| Retire the authored test-spec package and active workflow stage | core to this proposal |
| Remove or constrain test-spec and test-spec-review lifecycle, schema, CLI, validation, fixture, and automation surfaces | same-slice dependency |
| Update governance, workflow guidance, examples, templates, and vision wording | same-slice dependency |
| Update supported adapter metadata and generated release packages through repository-owned generation | same-slice dependency |
| Organize specialist plan-owned verification references | separate implementation slice |
| Define exact plan structure, verification-group syntax, lifecycle schema changes, validation rules, and migration mechanics | first-slice candidate for Design and Delivery, not settled here |
| Rewrite historical test specs or review evidence | out of scope |
| Redesign the lightweight requirement-to-delivery model | out of scope |

### Non-goals

This change does not remove test design, automated tests, manual checks, operational evidence, Code Review, or Verify. It does not make the specification own implementation-level test mechanics or make milestone sequencing primarily test-driven. It does not require one SR per test, define every concrete test before implementation, merge specification and plan, introduce a `proof-obligation` artifact, or add another mandatory verification skill under a new name. It does not make Code Review or Verify substitutes for pre-implementation verification planning, and it does not rewrite historical test-spec artifacts or their review evidence.

## Governing principle

> **Verification requirements should live with the system requirements and allocated delivery work they validate, rather than in a separate lifecycle artifact that duplicates both.**

## Proposed direction

Retire the standalone test-spec stage and redistribute its useful responsibilities without weakening the pre-implementation gate.

The specification remains the authoritative SR-level behavioral contract. It must make demonstrable behavior clear enough for downstream verification planning, including applicable normal behavior, invalid input, failure behavior, state transitions, permissions and authority, compatibility and migration, retries and concurrency, recovery, important boundaries, representative scenarios, and acceptance conditions. It should answer what must be demonstrably true while leaving test frameworks, fixtures, mocks, filenames, commands, milestone allocation, and other implementation mechanics downstream.

The plan becomes the complete delivery contract. Its milestones remain shaped primarily by dependencies, safe intermediate states, migration order, reversibility, integration boundaries, implementation risk, and reviewability. Each milestone must also identify the SRs and architecture responsibilities it realizes, what it implements, and what must be demonstrated before the milestone is complete. The plan must add change-level verification when important behavior spans milestones or boundaries, including applicable end-to-end, migration, compatibility, concurrency, recovery, security, authority, and generated-output concerns.

Plans may use lightweight verification-group identities to connect related objectives and important scenarios to concrete tests, checks, and evidence. The intended chain is:

```text
SR → allocated milestone → verification group → concrete proof → evidence
```

This is traceability, not a second requirements hierarchy. Individual test functions need no RigorLoop identity unless a concrete downstream need justifies one. Design and Delivery own the exact representation and proof mechanics.

Delivery Review becomes the single pre-implementation readiness gate for the plan. It must judge both whether the implementation sequence is safe and reviewable and whether planned milestone and complete-change verification can demonstrate the approved design. Approval must not permit important negative, boundary, compatibility, migration, recovery, concurrency, security, authority, integration, or evidence obligations to be postponed implicitly until final Verify.

Specialist test-design methods should move into conditionally loaded references owned by `plan`. Ordinary work should receive concise inline guidance, while changes with state-machine, concurrency, migration, recovery, security, cross-boundary, manual, or operational proof concerns load only the relevant deeper method. The exact reference split is a Design decision.

New governed changes use this contract after activation. Existing test specs and review records remain valid historical evidence. Any governed change still active at activation must either finish under its registered contract or follow an explicit workflow-owned migration; no skill may silently reinterpret or rewrite it.

## Feasibility

**Assessment: Feasible, with a predecessor and compatibility constraint.**

The direction builds on the lightweight requirement-to-delivery model already implemented on its predecessor branch: specifications own SR behavior, architecture realizes SRs, plans allocate them into work, and evidence traces backward through the chain. Current authored sources also provide natural homes for the redistributed responsibilities in `skills/spec`, `skills/plan`, and `skills/delivery-review`.

The change is broader than deleting one skill. Canonical `skills/test-spec` remains present, and test-spec or test-spec-review concepts are represented in governance, workflow guidance, schemas, lifecycle and review validators, automation, fixtures, examples, and adapter metadata. The standalone test-spec-review published progression entrypoint is already retired, but historical and compatibility handling remains. Design must distinguish active contract removal from historical readability so closed evidence does not become invalid.

The predecessor lightweight-model change is currently at Verify on this branch rather than merged into `main`. This proposal can be reviewed on the dependent branch, but Design and implementation must retain that dependency and must not claim the new ownership model is available independently. No conceptual blocker is known; responsible implementation requires an exact inventory, explicit activation and rollback behavior, and coherent updates across canonical, validation, documentation, and generated package surfaces.

## Impact and major trade-offs

The normal lifecycle loses test-spec authoring, its mandatory artifact, its stage and settlement state, and any remaining standalone review compatibility that is not required solely to read historical records. This reduces review rounds, lifecycle states, synchronization, and context, while making plan quality and Delivery Review materially more important.

The main risk is that verification design receives less independent attention. The mitigation is structural: specification owns demonstrable behavior, plan owns allocated verification expectations, Delivery Review independently challenges both delivery and verification readiness, implementation creates concrete proof, and Verify evaluates actual evidence. Complex plans may become longer where their real delivery risk warrants it.

`VISION.md` now describes traceability through testable system requirements, architecture, verification-aware delivery planning, concrete proof, and evidence without requiring a standalone test-spec artifact. That upstream revision resolves the earlier literal artifact conflict while preserving the vision's traceability and reviewability commitments. The implementing change must remain consistent with that standing direction and requires no vision exception.

Historical test specs and review records remain valid and readable. Removal must preserve that historical interpretation while preventing new changes from entering the retired stage. Rollback must restore the active stage, skills, routing, validation, and package surfaces coherently rather than leave a mixed workflow contract.

## Decision requested

Approve the direction to:

1. remove `test-spec.md` as a mandatory governed lifecycle artifact and stage for new changes;
2. retire the standalone test-spec authoring package and remaining active test-spec-review lifecycle surface while preserving historical readability;
3. strengthen specification guidance so SRs, boundaries, failures, compatibility expectations, and important scenarios provide sufficient behavioral input for verification planning;
4. strengthen plan guidance so milestones carry required verification and plans carry complete-change verification where needed;
5. keep milestone decomposition primarily driven by safe engineering and dependency sequencing;
6. use lightweight verification groups to connect SRs and allocated work to concrete proof and evidence without another heavy hierarchy;
7. move specialist test-design methodology into conditionally loaded plan references;
8. make Delivery Review jointly approve implementation readiness and verification adequacy before implementation;
9. preserve historical artifacts without rewrite and require explicit handling for any in-flight governed change at activation;
10. preserve SR-to-allocation-to-verification-to-evidence traceability under the lightweight requirement-to-delivery model.

Approval authorizes removal of the standalone test-spec lifecycle surface and redistribution of its responsibilities into specification, planning, and Delivery Review under the revised project vision. It does not approve exact templates, reference organization, lifecycle schema, migration mechanics, verification-group syntax, concrete tests, or implementation sequencing.
