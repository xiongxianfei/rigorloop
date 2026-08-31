# Retire the Standalone Test-Spec Stage Architecture

## Owning change record

- `docs/changes/2026-08-31-retire-standalone-test-spec-stage/change.yaml`

## Related artifacts

- Proposal: [Retire the Standalone Test-Spec Stage](../proposals/2026-08-31-retire-standalone-test-spec-stage.md)
- Spec: None yet; specification reconciliation follows this architecture.
- Plan: None yet.
- ADRs: [ADR-20260831-verification-ownership-without-test-spec-stage](../adr/ADR-20260831-verification-ownership-without-test-spec-stage.md)

## Introduction and Goals

This architecture removes the standalone test-spec lifecycle surface while preserving the property it was intended to provide: before implementation, RigorLoop knows what behavior must be demonstrated, where verification responsibility is allocated, and what evidence the change must produce.

It defines the responsibility split among specification, architecture, plan, Delivery Review, implementation, and Verify; the lifecycle and package activation boundary; and historical compatibility. Its stakeholders are contributors maintaining canonical workflow sources, agents executing governed changes, reviewers approving delivery readiness, and users installing supported adapter packages.

## Architecture Constraints

- This change governs new changes only after coherent activation. It must itself complete the currently registered lifecycle, including the existing test-spec stage and Delivery Review package contract.
- `skills/` remains the only authored skill source. Generated adapter packages and release archives remain derived output.
- The specification remains authoritative for stable, observable SR-level behavior; it does not own test filenames, frameworks, fixtures, mocks, exact commands, or milestone allocation.
- The plan remains primarily an engineering and dependency sequence. Verification expectations attach to safe milestones rather than determining milestone boundaries by default.
- No replacement verification artifact, mandatory verification skill, proof-obligation hierarchy, or additional lifecycle stage may be introduced.
- Delivery Review remains an independent peer and may write only its review evidence and matching package settlement.
- `change.yaml` remains the sole mutable governed-state snapshot, and the lifecycle CLI remains the mutation boundary for supported operations.
- `lifecycle_contract: stage-owned-change-local-v2` is the new graph discriminator; prior v1 and unversioned records are compatibility inputs only when named by the frozen activation manifest.
- Closed vocabularies fail closed. Removing known test-spec values must not create permissive fall-through for unknown values.
- Historical artifacts and evidence are records, not migration targets. Existing governed changes retain their registered contract unless Workflow performs an explicit validated migration.

## Context and Scope

The change affects the repository system that publishes and enforces the workflow:

```text
Canonical contract sources
  specs/ + skills/ + templates/ + docs/
          │
          ├── lifecycle schemas, CLI engine, validators, and fixtures
          ├── workflow routing and review-package membership
          └── skill/package generation and adapter release validation
                         │
                         ↓
              installed RigorLoop workflow
                         │
              new changes │ historical records
                         ↓             ↓
       plan-centered Delivery Review   read-only compatibility
```

Repository maintainers author the contract. The lifecycle CLI and validators enforce it. Skill generators and release tooling project it into supported adapters. Agents and reviewers consume those installed packages to create and settle governed artifacts.

C4 context and container diagrams are not applicable because this change alters a repository-owned workflow protocol and packaged guidance rather than adding a service, executable container, or runtime network relationship. The boundary diagram above captures the affected authority and projection flow without implying nonexistent deployment topology.

## Solution Strategy

Activate one coherent contract revision with five coordinated changes:

1. Strengthen specification guidance so SRs express demonstrably true normal, negative, boundary, state, authority, compatibility, migration, retry, concurrency, recovery, and representative-scenario behavior where relevant.
2. Strengthen plan guidance so each implementation milestone identifies its SR and architecture allocation and the verification groups required for completion, while a change-level section covers behavior spanning milestones or boundaries.
3. Change Delivery Review to approve the exact plan-centered delivery package by evaluating safe execution and verification adequacy together.
4. Remove test-spec and test-spec-review from the v2 active skill inventory, routing, lifecycle state, templates, examples, schemas, validators, and generated packages, while preserving manifest-bound prior-contract interpretation.
5. Prove activation and rollback across canonical sources, lifecycle behavior, validators, fixtures, generated adapters, and documentation so no supported package can combine old and new ownership rules.

The plan-local trace is deliberately small:

```text
SR → milestone allocation → verification group → concrete test/check → evidence
```

Specialist test-design methods become conditionally loaded references owned by `plan`. Ordinary changes use compact inline guidance; complex changes load only the relevant boundary, state-machine, concurrency, migration, failure-recovery, security, integration, or operational-evidence method.

## Building Block View

### Specification authoring package

The `spec` skill and its templates own testable SR behavior and important scenarios. They provide enough behavioral input for downstream verification planning without prescribing implementation mechanics.

### Architecture package

Architecture maps SRs to realization boundaries and calls out technical properties that affect verification, such as state transitions, trust boundaries, compatibility seams, concurrency control, migration ordering, and recovery paths. It does not allocate concrete tests.

### Plan authoring package

The `plan` skill, skeleton, and conditionally loaded test-design references own the complete delivery contract. A milestone records purpose, SR allocation, architecture responsibility, dependencies, implementation scope, completion criteria, required verification groups, and evidence expectations. Change-level verification records integrated behavior not safely attributable to one milestone.

### Delivery Review package

`delivery-review` reviews exactly one primary plan plus its approved Design Review authority. It checks implementation sequencing and verification coverage as one decision. It neither authors missing verification nor accepts a standalone test-spec member.

### Governed lifecycle engine and validation

Workflow routing, lifecycle schemas, CLI transitions, review-package calculation, validators, and fixtures define the active stage graph and artifact vocabulary. They remove test-spec from newly created v2 state while retaining narrowly specified prior-contract readers and an optional explicit migration operation. Unknown values remain errors.

### Contract activation manifest

One tracked schema-validated manifest records the activating source revision and every pre-activation change ID, sorted by raw UTF-8 bytes and bound to exactly `stage-owned-change-local-v1` or `legacy-unversioned`. It is frozen activation evidence rather than mutable state, stage authority, or a runtime history query. New-change scaffolding emits v2 after activation.

Classification is fail-closed:

| Record facts | Contract interpretation |
| --- | --- |
| Explicit `stage-owned-change-local-v2` with v2-valid state | New no-test-spec graph. |
| Explicit v1 and matching manifest entry | Prior graph; continue or read historically. |
| No contract and matching `legacy-unversioned` manifest entry | Existing legacy reader only. |
| V1 or unversioned without an exact manifest entry | Invalid; it cannot claim prior status. |
| Unknown contract, manifest class mismatch, or v2 with active test-spec state | Invalid before consistency checks. |

Creation date, filename date, current stage, test-spec artifact presence, Git reachability, and network state never select a contract.

### Publication boundary

Canonical skills, mapped references, generators, adapter manifests, release archives, installation guidance, and parity checks publish the same ownership model. Generated packages are never hand-edited.

No component diagram is needed beyond these repository building blocks because they are authored content and deterministic enforcement modules inside the existing RigorLoop package.

## Runtime View

### New governed change after activation

1. Proposal Review accepts direction.
2. Architecture and specification define realization and observable SR behavior; Design Review approves the exact package.
3. Plan allocates SRs and architecture responsibilities into a safe sequence, with milestone and change-level verification groups.
4. Delivery Review rejects or approves the same plan based on both implementation and verification readiness.
5. Implementation creates code, concrete tests or checks, and evidence for the approved groups.
6. Code Review evaluates implementation slices; Verify evaluates complete evidence closure.

### Historical record read

1. A reader encounters a historical test-spec artifact or review entry.
2. The record's v1 or unversioned class must match its exact frozen activation-manifest entry.
3. Compatibility interpretation recognizes the previously valid identity and evidence without making it an active stage for new changes.
4. The record remains immutable historical authority and is not synthesized into the new plan structure.

### In-flight governed change

1. Workflow reads the change's registered lifecycle contract and package state.
2. The v1 value, or legacy-unversioned class, must match the change's frozen manifest entry.
3. The change continues through test-spec and its registered Delivery Review contract by default.
4. Only an explicit workflow-owned migration may adopt v2, and only after validation proves an unambiguous v2 target state, current evidence identities, plan-owned verification content, and correct review-authority invalidation or preservation.

### Explicit contract migration

1. Workflow selects one manifest-listed in-flight change and obtains its exact current lifecycle revision and artifact identities.
2. Validation proves the plan already owns the verification content needed by v2 and computes one v2-valid target stage and package state.
3. One guarded lifecycle transaction writes `lifecycle_contract: stage-owned-change-local-v2` and an identity-bound migration receipt in existing lifecycle coordination state.
4. The operation preserves or invalidates package review authority according to changed membership and never manufactures approval.
5. Any stale identity, ambiguous target, missing plan content, unknown state, or failed post-validation leaves the prior bytes and authority unchanged.

The migration operation is optional in the first implementation. If delivery planning omits it, every prior-contract change must finish its registered graph.

### Failure paths

- A new plan lacking material verification coverage fails Delivery Review; the reviewer routes correction to `plan`.
- A new package containing test-spec as an active Delivery Review member fails package validation.
- An unknown lifecycle stage, artifact kind, review kind, or settlement value fails before consistency interpretation.
- A generated adapter mixing old routing with new skills fails parity or release validation before publication.
- A record missing from the activation manifest, contradicting its recorded class, or combining v2 with active test-spec state blocks with an explicit compatibility diagnostic rather than being guessed or rewritten.

## Deployment View

Activation is a repository and release compatibility boundary:

```text
canonical workflow revision
  ├── skills and references
  ├── specs, schemas, templates, and docs
  ├── CLI engine, validators, and fixtures
  └── adapter generation and release metadata
             ↓ one validated package revision
      supported adapter archives
```

The implementation plan must order changes so every checked revision is internally valid, generate and validate the frozen compatibility manifest from the reviewed activation baseline, use compatibility fixtures while old and new interpreters overlap, and select one release boundary for public activation.

Before any v2 record is created, rollback restores the last complete standalone-test-spec authoring and routing package and regenerates all derived targets while retaining the manifest as unused evidence. After a v2 record exists, recovery is forward through a compatible corrective release. A later return to v1-by-default would need a separate approved migration design because silently rewriting v2 records or imposing missing test-spec obligations would violate their registered contract.

## Crosscutting Concepts

### Traceability

SR IDs remain the durable requirement join points. Plans allocate SRs to milestones and verification groups; implementation evidence names the approved group or directly names the governing SR and milestone where that is clearer. Individual test functions need no RigorLoop identity unless a concrete traceability need justifies one.

### Verification sufficiency

Milestone completion proves only the behavior allocated to that milestone. Cross-milestone, end-to-end, compatibility, migration, concurrency, security, authority, failure, and recovery behavior receives change-level verification whenever complete-change correctness cannot be inferred safely from milestone proof.

### Progressive disclosure

Basic verification guidance stays inline in `plan`. Specialist methodology is packaged under the plan skill and loaded only when the design exposes the corresponding risk. Removing the standalone skill must reduce ordinary context without reducing access to expertise.

### Authority

Specification answers what must be demonstrably true. Architecture answers how responsibilities realize SRs. Plan answers where implementation and verification responsibility is allocated. Delivery Review decides readiness. Implementation chooses concrete mechanics within the approved contract. Verify evaluates actual evidence.

### Compatibility and migration

V2 active vocabulary, exact manifest-bound prior vocabulary, and explicit migration are separate paths. Historical acceptance never authorizes a new test-spec stage, and active removal never invalidates previously settled evidence. The manifest identifies eligibility only; each `change.yaml` remains the mutable state owner.

### Validation

Structural validation checks required plan fields, known vocabularies, package membership, resource mapping, generated parity, and compatibility fixtures. Semantic adequacy remains review-owned: validators do not decide whether scenarios or proof are sufficient.

## Architecture Decisions

- [ADR-20260831-verification-ownership-without-test-spec-stage](../adr/ADR-20260831-verification-ownership-without-test-spec-stage.md) — co-locates verification ownership in specification and plan, makes Delivery Review the joint readiness gate, and separates active removal from historical compatibility.

## Quality Requirements

| Quality | Scenario | Measure |
| --- | --- | --- |
| Verification rigor | A change includes important negative and cross-boundary behavior. | Its approved plan allocates milestone and change-level verification sufficient for Delivery Review to judge before implementation. |
| Traceability | A verifier investigates evidence for an SR. | The repository can traverse SR, allocated milestone, verification group, concrete check, and evidence without a standalone test-spec artifact. |
| Lifecycle safety | A new record supplies an unknown stage or artifact kind. | Validation returns an explicit closed-vocabulary error before consistency checks. |
| Historical compatibility | A completed pre-activation change contains test-spec settlement and review evidence. | Its exact change ID and prior class match the frozen manifest, and the record remains readable without mutation or conversion. |
| Package consistency | A supported adapter is generated or released. | Routing, skills, references, schemas, and templates all express one ownership model; mixed revisions fail validation. |
| Context efficiency | An ordinary low-complexity change reaches planning. | It loads compact inline verification guidance without loading unrelated specialist methods or a test-spec skill. |
| Review independence | A plan omits a material verification boundary. | Delivery Review records a finding and routes correction to plan rather than authoring the missing content. |
| Recoverability | Activation validation exposes an uncovered compatibility case before v2 creation. | The release can restore the last complete contract without rewriting historical records; after v2 creation, recovery uses a forward compatible release. |

## Risks and Technical Debt

- Plan authors may treat verification as a checklist after sequencing. Required milestone and change-level sections plus independent Delivery Review mitigate this, but plan quality remains a central risk.
- Complex plans may grow. Progressive-disclosure references and lightweight verification groups constrain ceremony while retaining real risk detail.
- Historical compatibility code and the frozen activation manifest may become permanent debt. The implementation must define the narrow accepted legacy surface and fixtures rather than retaining broad permissive parsing.
- The repository must use the old lifecycle to remove that lifecycle. The self-hosting constraint requires the current change to complete its registered test-spec and Delivery Review path before activation.
- A missed skill, template, validator, example, or adapter surface could publish contradictory guidance. The plan needs an explicit removal inventory, generated-package parity proof, and mixed-version negative fixtures.
- Existing closed-vocabulary checks may use permissive membership guards. Every changed vocabulary requires an unknown-value regression test before removal is accepted.

## Glossary

- **Verification group (TG):** A lightweight plan-local identity for a related verification objective and its important scenarios.
- **Milestone verification:** Behavior that must be demonstrated before one allocated implementation milestone is complete.
- **Change-level verification:** Integrated behavior spanning milestones or system boundaries that must be demonstrated for complete-change correctness.
- **Active vocabulary:** Lifecycle values permitted for newly governed changes after activation.
- **Historical compatibility:** Read-only interpretation of artifacts and evidence valid under a prior lifecycle contract.
- **Contract activation manifest:** Frozen repository evidence binding each pre-activation change ID to its observed v1 or legacy-unversioned contract class.
- **Explicit migration:** A workflow-owned validated transition of an in-flight governed change between compatible lifecycle contracts.
- **Coherent activation:** Publication of canonical, executable, validated, documented, and generated surfaces as one compatible contract revision.

## Next artifacts

- Specification reconciliation.
- Design Review of the architecture, ADR, and specification as one exact package.

## Follow-on artifacts

- None yet.

## Readiness

The architecture and ADR are ready for specification reconciliation. They do not authorize implementation and are not approved until Design Review accepts the exact design package.
