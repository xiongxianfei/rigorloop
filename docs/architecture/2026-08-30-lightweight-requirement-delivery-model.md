# Lightweight Requirement-to-Delivery Model Architecture

## Owning change record

- `docs/changes/2026-08-30-lightweight-requirement-delivery-model/change.yaml`

## Related artifacts

- Proposal: [Introduce a Lightweight Requirement-to-Delivery Model](../proposals/2026-08-30-lightweight-requirement-delivery-model.md)
- Spec: [Lightweight Requirement-to-Delivery Model](../../specs/lightweight-requirement-delivery-model.md)
- Plan: None yet.
- ADRs: None. This design uses the existing copied shared-resource and skill-local packaging architecture; it introduces no new durable runtime or repository boundary requiring a separate ADR.

## Introduction and Goals

This architecture establishes how RigorLoop will expose the approved requirement-refinement and work-decomposition model through its existing published skills. It must give agents a consistent explanation of `RR → IR → SR → AR`, keep `Epic → Feature → Story → Task` separate and optional, and preserve traceability without introducing new lifecycle entities or a requirements-management subsystem.

The intended stakeholders are contributors maintaining canonical skill sources, agents using published skills, and reviewers evaluating whether intent, requirements, design, work, implementation, and evidence remain connected.

## Architecture Constraints

- `skills/` remains the only authored skill source; generated adapter packages remain derived output.
- Shared portable guidance follows the existing `templates/shared/` canonical-source and copied-consumer pattern governed by `specs/skill-contract.md`.
- Published skills may load only skill-local packaged resources. They must not depend on RigorLoop repository paths in customer projects.
- The design adds no lifecycle stage, mandatory RR/IR/AR artifact, requirements database, external tracker integration, or expanded `change.yaml` state.
- Specification requirements remain the durable system-requirement identities used downstream.
- Stage-specific authority, routing, settlement, and readiness semantics remain in the owning skills and workflow contract rather than in the shared model.
- Terminology and decomposition depth must remain proportional to the change.

## Context and Scope

The design changes an authored guidance and packaging boundary, not a runtime service topology.

```text
Maintainer
  ↓ authors
Canonical shared model in templates/shared/
  ↓ copied and parity-checked
Selected skill-local references under skills/*/references/
  ↓ loaded conditionally by
Proposal, Design, Delivery, Review, and Verify skills
  ↓ produce or assess
Existing proposal, spec, architecture, plan, implementation, and evidence artifacts
```

The external boundary is the installed skill package in a customer repository. Customers receive self-contained skill-local guidance; they do not need access to RigorLoop's canonical shared-source path, build scripts, or repository governance files.

C4 system-context and container diagrams are not applicable because this change introduces no executable system, deployable container, service interaction, or data flow. The text boundary above is sufficient and avoids implying runtime components that do not exist.

## Solution Strategy

Create one concise canonical shared source at `templates/shared/requirement-to-delivery-model.md`. Copy it verbatim to `references/requirement-to-delivery-model.md` in each selected consuming skill. Add explicit `READ` entries with stage-specific load conditions to those skills' resource maps.

The shared reference owns only:

- the definitions of RR, IR, SR, and conceptual AR;
- the separation between requirement refinement and work decomposition;
- the proportional use of Epic, Feature, Story, Task, Milestone, and Subtask;
- the forward intent-to-implementation trace and reverse evidence-to-intent trace;
- the stable rule that SR identities are the primary durable downstream requirement references.

Each skill continues to own its local responsibilities, stop conditions, lifecycle authority, and output contract. The shared reference must not define stage transitions, settlement, artifact placement, required review outcomes, or verification authority.

The first integration set is:

| Skill | Model responsibility |
| --- | --- |
| `proposal` | Clarify raw input into an approved IR-level direction without creating an RR or IR artifact. |
| `proposal-review` | Judge whether the RR-to-IR refinement is responsible and sufficient for Design. |
| `architecture` | Explain how SRs are realized within technical constraints without becoming another requirement level. |
| `spec` | Author stable, observable SR identities from the approved direction. |
| `design-review` | Judge `IR → SR ↔ Architecture` coherence. |
| `plan` | Allocate SRs and architecture boundaries into milestones or optional work hierarchy. |
| `delivery-review` | Judge whether the allocation is safe, traceable, and implementable. |
| `code-review` | Check implementation against allocated work and its governing SRs and design boundaries. |
| `verify` | Traverse evidence backward through implementation and SRs to the approved direction. |

`implement` and `test-spec` continue consuming approved plan, design, and proof obligations through their existing contracts. They do not need the new terminology in the first slice because no responsibility is being redistributed to them.

## Building Block View

### Shared model source

`templates/shared/requirement-to-delivery-model.md` is the canonical portable wording. It is concise, implementation-independent, and contains no repository-maintainer paths or stage-specific authority.

### Skill-local model references

Each selected consumer contains a byte-identical `references/requirement-to-delivery-model.md`. Its skill resource map names the exact load condition. A consumer applies only its named responsibility even though the compact shared reference explains the complete chain.

### Stage integration points

Skill bodies keep short local instructions that connect the shared concepts to the stage's existing artifact or review responsibility. Templates add only fields or prompts needed to make an existing artifact's traceability explicit; they do not require all conceptual levels to appear.

### Package and parity validation

Existing skill-resource validation owns canonical-to-consumer copy parity, mapped-resource presence, generated adapter parity, and clean-install parity. The implementation should extend an existing owner rather than add a new standalone validator or traceability engine.

No component or lower C4 view is applicable because these building blocks are authored Markdown and deterministic packaging checks rather than executable components.

## Runtime View

### Authoring flow

1. An agent loads an existing stage skill.
2. The resource map condition determines whether the requirement-to-delivery reference is relevant.
3. The agent reads the skill-local reference and applies only the stage-specific responsibility named by the skill.
4. The stage writes its existing artifact type and existing governed evidence.
5. No new RR, IR, or AR lifecycle record is created.

### Review flow

1. A reviewer reads the existing package and its stable SR references.
2. The relevant review skill uses the shared vocabulary to check forward or reverse traceability at its owned boundary.
3. Findings continue to identify existing artifact owners and cross-artifact relationships.
4. Review recording and settlement use the existing lifecycle operations unchanged.

### Failure behavior

- A missing or drifted mapped reference is a package-integrity failure owned by existing skill validation.
- Missing traceability required by an owning stage is a semantic review finding, not an automatically invented requirement or work item.
- An unneeded decomposition level is omitted rather than emitted as an empty placeholder.
- A newly desired lifecycle entity or machine-readable traceability mechanism routes to a separate proposal.

## Deployment View

The change ships through the existing skill build and adapter release pipeline:

```text
templates/shared canonical source
  ↓ checked copy parity
skills/<consumer>/references/requirement-to-delivery-model.md
  ↓ existing skill build
generated adapter archive
  ↓ existing install flow
target-local skill tree
```

No service deployment, data migration, feature flag, runtime configuration, or external dependency is introduced. Supported adapter packages must activate the model coherently; mixed canonical and packaged wording is a validation failure before publication.

## Crosscutting Concepts

### Traceability

SR IDs remain the durable downstream join points. Architecture, plan, review, implementation evidence, and verification cite SRs where their existing contracts require traceability. RR, IR, and AR do not receive mandatory persisted identities in the first slice.

### Progressive disclosure

Skill bodies retain short stage-local instructions. The complete terminology is in the mapped reference and is loaded only when the stage needs to refine, allocate, or verify the chain. Small changes may use only Proposal/IR, SRs, one milestone, and tasks.

### Authority

The model describes relationships but grants no lifecycle authority. Proposal Review, Design Review, Delivery Review, Code Review, and Verify retain their existing decisions and settlement boundaries.

### Compatibility

Historical artifacts remain valid without retrofitted RR, IR, or AR labels. Current artifacts adopt the model when their governing skills and templates are updated. No compatibility interpreter or historical migration is required.

### Validation

Deterministic checks may validate resource mapping, byte parity, stable structural fields, and generated-package consistency. Semantic adequacy—whether a milestone genuinely realizes an SR or evidence genuinely closes the intent chain—remains review-owned.

## Architecture Decisions

No new ADR is required. The accepted proposal owns adoption of the conceptual model, while the existing skill-contract architecture already owns canonical shared sources, copied skill-local resources, resource maps, build parity, and adapter publication. This architecture applies those established mechanisms without creating a new durable technical boundary.

## Quality Requirements

| Quality | Scenario | Measure |
| --- | --- | --- |
| Consistency | Two consuming skills explain the same model. | Shared model text is byte-identical across the canonical source and every mapped consumer. |
| Progressive disclosure | A small change uses the workflow. | No RR, IR, AR, Epic, Feature, or Story artifact is required merely to satisfy taxonomy. |
| Traceability | A reviewer asks why a milestone exists. | The plan can cite governing SRs and relevant architecture boundaries using existing artifact fields. |
| Portability | A supported adapter is installed outside this repository. | Every mapped reference resolves within the installed skill root without repository-local dependencies. |
| Authority safety | A shared-model statement conflicts with a stage contract. | The stage contract and governing specs retain authority; validation or review blocks the conflicting package. |
| Maintainability | The model wording changes. | One canonical source and existing parity checks identify every consumer that must be updated. |

## Risks and Technical Debt

- Copying the reference to several skills increases tracked bytes. The existing copied shared-resource model accepts this cost to preserve self-contained packages and deterministic parity.
- Loading the complete vocabulary too often could increase agent context. Resource-map conditions and short stage-local mappings must prevent unconditional loading.
- The terms `IR` and `AR` may be unfamiliar or interpreted differently outside RigorLoop. The glossary and examples must define RigorLoop's use without claiming an external standard.
- The first slice leaves semantic traceability review-owned. Machine-readable traceability, if later justified, requires a separate proposal rather than incremental schema creep.

## Glossary

- **RR — Raw Requirement:** The original incoming need before clarification; normally represented by the existing request, issue, or prompt.
- **IR — Initial Requirement:** The approved proposal-level clarification of the need and direction; no separate artifact is required.
- **SR — System Requirement:** A stable, observable, testable specification requirement used for downstream traceability.
- **AR — Allocated Requirement:** The conceptual assignment of an SR to a realization boundary or work package; no mandatory identity is required.
- **Work decomposition:** Optional structuring of delivery effort into Epic, Feature, Story, Task, Milestone, or Subtask levels.
- **Realization:** The architecture's explanation of how technical boundaries can satisfy SRs.
- **Allocation:** The plan's assignment of SR and architecture responsibilities to executable work.

## Next artifacts

- Specification reconciliation.
- Design Review of the architecture and specification as one package.

## Follow-on artifacts

- None yet.

## Readiness

The architecture is ready for specification authoring and reconciliation. It is not approved until Design Review accepts the exact architecture/specification package.
