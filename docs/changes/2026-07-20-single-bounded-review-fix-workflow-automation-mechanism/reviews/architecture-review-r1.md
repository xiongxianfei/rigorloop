# Architecture Review R1

Review ID: architecture-review-r1
Stage: architecture-review
Round: 1
Target: docs/architecture/system/architecture.md
Reviewed artifact: docs/architecture/system/architecture.md
Review date: 2026-07-21
Reviewer: Codex architecture-review
Recording status: recorded
Status: changes-requested
Review surface: canonical-architecture-update and ADR

## Result

- Review surface: canonical-architecture-update and ADR
- Review status: changes-requested
- Material findings: `BRF-AR1`, `BRF-AR2`, `BRF-AR3`
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/architecture-review-r1.md
- Review log: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md
- Review resolution: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md
- Open blockers: incomplete stage-policy projection, ambiguous executable/persistence ownership, and obsolete receipt authority terminology
- Required canonical updates: complete the stage-policy contract, choose one code/state ownership boundary, align the C4 roles, and bind prepared receipts to effective capabilities
- Required ADR updates: carry the complete registry decision, precise ownership split, exact receipt authority identity, and acceptance-conditional supersession wording
- Next stage: architecture revision

## Review Inputs

- Canonical architecture: `docs/architecture/system/architecture.md`
- Component diagram: `docs/architecture/system/diagrams/component-workflow-automation.mmd`
- Container diagram: `docs/architecture/system/diagrams/container.mmd`
- Proposed ADR: `docs/adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md`
- Approved feature spec: `specs/single-bounded-review-fix-workflow-automation.md`
- Accepted proposal: `docs/proposals/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism.md`
- Governing architecture method: `specs/architecture-package-method.md`
- Existing supersession targets: `docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md`, `docs/adr/ADR-20260624-implementation-through-verify-autoprogression.md`, and `docs/adr/ADR-20260630-bounded-review-fix-autoprogression.md`
- Governance and operating context: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, and `docs/project-map.md`

## Findings

### Finding BRF-AR1

Finding ID: BRF-AR1
Severity: major
Location: `docs/architecture/system/architecture.md:367`; `docs/adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md:29`
Evidence: The canonical architecture projects owning skill, occurrence, prerequisites, authority class, applicability, completion, retry, and correction policy. The ADR projects owning skill, basis, authority, applicability, completion, retry, and correction. The approved specification's `BRF-R079` also requires predecessor, capability kind, permitted mutation category, required input identities, completion evidence, next-stage calculation, and stop behavior. Those fields decide routing, authority, and termination and therefore cannot be invented during planning or implementation.
Required outcome: The canonical architecture and ADR MUST identify the complete closed stage-policy projection required by `BRF-R079` and preserve the specification as its normative owner.
Safe resolution path: Enumerate all `BRF-R079` fields in the registry responsibility and ADR decision, using exact contract terms. Keep the registry an immutable typed Python projection and require exhaustive conformance tests against the approved spec.
needs-decision rationale: none; the approved specification already settles the required field set.

### Finding BRF-AR2

Finding ID: BRF-AR2
Severity: major
Location: `docs/architecture/system/architecture.md:315`; `docs/architecture/system/diagrams/container.mmd:17`; `docs/architecture/system/diagrams/component-workflow-automation.mmd:4-16`
Evidence: The architecture assigns typed Python policy and orchestration jointly to `scripts/` and `skills/` while also assigning change-local state to the automation building block. The container diagram embeds both typed policy and change-local YAML state inside the automation container even though the separate change-local-evidence container receives the persisted automation records. The component view presents repository-owned sibling containers and persisted state as external elements and does not select the concrete first-version `workflow.automation` persistence surface. This leaves the plan to decide which surface executes orchestration, which owns executable policy and validation, and where the canonical YAML state physically resides.
Required outcome: The architecture MUST define one plan-ready executable ownership split and one canonical first-version persistence surface, with consistent C4 system/container/component roles.
Safe resolution path: Assign public orchestration and command behavior to the canonical workflow skill, assign the typed registry/evaluator/validators to named repository Python modules under `scripts/`, and persist the sole canonical state at `docs/changes/<change-id>/change.yaml#workflow.automation` unless the architecture explicitly selects and schemas a separate change-local file. Model automation as code and change-local evidence as its state owner; render internal automation elements as components and repository sibling containers as containers rather than external systems.
needs-decision rationale: The architecture author must select the physical persistence surface and exact code-module boundary before planning; the approved spec constrains semantics but deliberately does not choose those implementation locations.

### Finding BRF-AR3

Finding ID: BRF-AR3
Severity: major
Location: `docs/architecture/system/architecture.md:398`; `specs/single-bounded-review-fix-workflow-automation.md:388`
Evidence: Runtime step 10 says a prepared transition receipt contains a `grant identity`. The approved two-level authority model deliberately replaced the ambiguous grant concept with bounded parent authorization and executable effective capability. `BRF-R069` specifically requires the prepared receipt to record the effective capability ID.
Required outcome: Every architecture description of executable transition authority MUST bind the receipt to an `effective capability ID`; a parent authorization MUST remain non-executable and reachable only through the capability's parent link.
Safe resolution path: Replace `grant identity` with `effective capability ID` in the runtime flow and audit the architecture and ADR for any remaining ambiguous grant terminology.
needs-decision rationale: none; the approved specification already settles this identity.

## Minor Observation

The proposed ADR says the decision already supersedes three accepted ADRs while its own status remains `proposed`. Use acceptance-conditional wording such as “On acceptance, this decision supersedes,” then normalize the new ADR and the three predecessors together after an approving architecture review.

## Review Dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| component ownership | block | Executable orchestration, policy modules, and persisted state do not yet have one unambiguous physical owner. |
| dependency direction | concern | The logical flow is sound, but component/container roles obscure which dependencies cross real boundaries. |
| data and state ownership | block | The neutral namespace is correct; the concrete first-version YAML owner and surface remain ambiguous. |
| runtime and recovery | concern | Prepared-receipt recovery is present, but the receipt names the wrong authority identity. |
| authorization safety | concern | Parent/capability separation is otherwise preserved; `grant identity` reintroduces ambiguity at the mutation boundary. |
| migration and compatibility | pass | Dual-read, single-write migration and mandatory adapter behavior align with the approved spec. |
| security and external actions | pass | No new service or external-action authority is introduced, and external operations remain prohibited. |
| failure handling | pass | Unknown values, ambiguous targets, stale evidence, partial transitions, and multiple in-flight transitions fail closed. |
| scalability and performance | pass | Repository-local evaluation and change-local persistence are proportionate to the workload. |
| operability and observability | pass | Runs, authorizations, capabilities, receipts, migration, cancellation, and stop reasons are durable and inspectable. |
| testability | block | Registry conformance cannot be exhaustive while architecture omits required policy fields and concrete ownership. |
| C4 and arc42 consistency | concern | The arc42 package is complete, but the new component view uses container/external roles for internal components and repository siblings. |
| ADR quality | concern | The decision direction is sound; registry completeness, physical ownership, and acceptance-conditional supersession need revision. |

## Readiness

The architectural direction is viable, and no proposal or specification reopening is required. It is not ready for execution planning until `BRF-AR1` through `BRF-AR3` are resolved in the canonical architecture, component/container views, and ADR, followed by an approving architecture rereview.

This direct architecture-review invocation is isolated. No architecture correction or downstream plan handoff was performed.
