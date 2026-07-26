# Boundary-First Proof Modeling Architecture Review R1

Review ID: architecture-review-r1
Stage: architecture-review
Round: 1
Reviewer: Codex architecture-review skill
Target: docs/architecture/system/architecture.md
Status: changes-requested

## Result

- Review surface: canonical-architecture-update and ADR
- Review status: changes-requested
- Material findings: `BFP-AR1`, `BFP-AR2`
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/architecture-review-r1.md
- Review log: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md
- Review resolution: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md
- Open blockers: capability-evaluator ownership and component-view containment
- Required canonical updates: name the evaluator owner and correct the component boundary
- Required ADR updates: record the evaluator ownership and one-writer report rule
- Next stage: architecture revision

## Review inputs

- Accepted proposal: `docs/proposals/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills.md`
- Approved specs: `specs/rigorloop-workflow.md` R28-R28z and `specs/skill-contract.md` R56-R56q
- Approved spec review: `reviews/spec-review-r2.md`
- Canonical architecture: `docs/architecture/system/architecture.md`
- Container diagram: `docs/architecture/system/diagrams/container.mmd`
- Component diagram: `docs/architecture/system/diagrams/component-boundary-proof.mmd`
- Proposed ADR: `docs/adr/ADR-20260725-boundary-first-proof-modeling.md`
- Architecture method: `specs/architecture-package-method.md`

## Findings

### BFP-AR1

Finding ID: BFP-AR1
Finding: The capability evaluator is shown as a runtime component but has no named physical owner or exclusive report-write boundary.
Location: `docs/architecture/system/architecture.md`, Level 2 White-Box: Boundary-Proof Validation and Evaluation; `docs/architecture/system/diagrams/component-boundary-proof.mmd`; `docs/adr/ADR-20260725-boundary-first-proof-modeling.md`, Decision
Severity: material
Evidence: The component diagram introduces a distinct `Capability report evaluator`, while the Building Block View assigns only model parsing, structural validation, tests, fixtures, selector routing, resources, adapters, and the report artifact. The ADR likewise says the first result is computed but does not identify the code that computes or writes it. Planning would therefore have to choose whether the model, validator, release tooling, or another script owns aggregation and report mutation.
Required outcome: The architecture MUST identify one physical evaluator owner, define whether it is pure computation or mutation, and name the only component permitted to write the capability report.
Safe resolution path: Assign aggregate computation to a pure evaluator in `scripts/boundary_proof_model.py`, assign report serialization to `scripts/validate-boundary-proof.py`, forbid other writers, and record the same boundary in the ADR and component diagram.
Recommendation: Add an evaluator row and an explicit report-write rule to the canonical architecture and ADR.

### BFP-AR2

Finding ID: BFP-AR2
Finding: The component diagram does not place the model, validator, selector, fixtures, evaluator, and generators inside their owning validation-and-generation container.
Location: `docs/architecture/system/diagrams/component-boundary-proof.mmd`
Severity: material
Evidence: All nodes are peers in one flat flowchart. `Shared boundary reference source` is styled as an internal component although it is owned by the sibling template container, while lifecycle specs, skills, report evidence, and release notes are also shown as peer containers. A component view must make the refined container boundary explicit so contributors can distinguish executable internals from repository sibling containers.
Required outcome: The component view MUST contain executable boundary-proof components inside one named validation-and-generation container and represent specs, skills, templates, fixtures/evidence, and release surfaces as sibling containers.
Safe resolution path: Wrap the executable model, validator, selector, evaluator, and adapter integration in a Mermaid subgraph labeled `Validation and generation scripts`; keep specifications, canonical skills, templates, test fixtures, change-local evidence, and release evidence outside it with container classes and labeled relationships.
Recommendation: Redraw the component view at one consistent C4 level without changing the approved design.

## Review dimensions

| Review dimension | Result | Notes |
| --- | --- | --- |
| Spec alignment | pass | The architecture preserves the approved closed model and lifecycle ownership. |
| Package shape | concern | The arc42 package is complete; the component view has a containment defect. |
| Boundary clarity | block | Executable component containment and evaluator ownership are ambiguous. |
| Data ownership | concern | Report location is exact, but its only writer is not named. |
| Interface safety | pass | Version, activation, resource, and adapter boundaries are explicit. |
| Runtime and failure handling | pass | Fail-closed validation, stale evidence, rollback, and mixed-version handling are covered. |
| Deployment and execution boundaries | pass | Packaged references and installed adapter parity are addressed. |
| Security/privacy | pass | No new secret, network, or external mutation boundary is introduced. |
| Quality and operations | pass | Measurable early detection, portability, overhead, and activation scenarios are present. |
| Testing feasibility | pass | Typed projection, fixtures, selectors, parity, and aggregate behavior are directly testable. |
| Complexity discipline | pass | One model, one validator, and mapped references are proportionate. |
| ADR quality | concern | The durable direction is sound; evaluator ownership must be added. |
| Plan readiness | block | The two named ownership boundaries must be resolved and rereviewed. |

## Readiness

The direction remains aligned with the accepted proposal and approved specs.
No proposal or spec revision is required.
Planning is blocked until `BFP-AR1` and `BFP-AR2` are resolved and an
architecture rereview approves the package.
