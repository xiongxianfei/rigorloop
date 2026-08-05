# Progressive Boundary-First Skill Guidance Architecture Review R1

Review ID: architecture-review-r1
Stage: architecture-review
Round: 1
Reviewer: Codex architecture-review skill
Target: docs/architecture/system/architecture.md;
docs/architecture/system/diagrams/container.mmd;
docs/architecture/system/diagrams/component-boundary-guidance.mmd;
docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md
Status: changes-requested
Original review source: User-requested `$architecture` followed by
`$architecture-review` on 2026-07-29.
Material findings: PBS-AR1, PBS-AR2
Immediate next stage: architecture revision
Automatic downstream handoff: none

## Result

- Review surface: `canonical-architecture-update`, `ADR`
- Review status: changes-requested
- Material findings: `PBS-AR1`, `PBS-AR2`
- Recording status: recorded
- Recording blocker: none
- Review record:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/architecture-review-r1.md`
- Review log:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/review-log.md`
- Review resolution:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/review-resolution.md#architecture-review-r1`
- Open blockers: `PBS-AR1`, `PBS-AR2`
- Required canonical updates: specify the exact resource-manifest schema and
  separate repository activation state from ephemeral generated/package proof.
- Required ADR updates: the same two corrections.
- Next stage: architecture revision followed by architecture-review R2.

## Review inputs

- Constitution: `CONSTITUTION.md`
- Repository instructions: `AGENTS.md`
- Architecture method: `specs/architecture-package-method.md`
- Accepted proposal:
  `docs/proposals/2026-07-29-progressive-boundary-first-skill-guidance.md`
- Approved feature specification:
  `specs/progressive-boundary-first-skill-guidance.md`
- Approved spec review:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/spec-review-r1.md`
- Canonical architecture: `docs/architecture/system/architecture.md`
- Container diagram:
  `docs/architecture/system/diagrams/container.mmd`
- Boundary-guidance component diagram:
  `docs/architecture/system/diagrams/component-boundary-guidance.mmd`
- Proposed ADR:
  `docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md`
- Related ADRs:
  `docs/adr/ADR-20260623-published-skill-resource-integrity.md` and
  `docs/adr/ADR-20260728-portable-boundary-first-release-manifest-and-package-rollback.md`

## Findings

## Finding PBS-AR1

Finding: The architecture names the projection-manifest fields conceptually
but does not settle the exact closed serialized schema required by the approved
spec.
Finding ID: PBS-AR1
Location:
`docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md` lines 45-49;
`docs/architecture/system/architecture.md` Runtime View step 4
Severity: material
Evidence: Spec-review made exact projection-manifest shape and identity a
condition for architecture readiness. The ADR names a closed ordered resource
list and four per-entry concepts, but it does not define the exact top-level
keys, entry keys, contract-version field, resource IDs, consumer ordering, or
whether unknown fields are forbidden. Runtime prose promises that unknown
fields and IDs fail closed, but planning and test-spec work cannot derive the
closed vocabulary it must implement or prove.
Required outcome: Define one exact manifest schema with all top-level and
per-resource fields, the three closed resource IDs, exact source and target
paths, ordered consumer lists, ordering rules, duplicate rules, and
unknown-field behavior.
Recommendation: Add a concise normative YAML example or equivalent field table
to the ADR and summarize its ownership in the canonical package. Keep raw-byte
manifest identity and projection-set identity unchanged unless the explicit
shape exposes a conflict.
Safe resolution path: Amend only the ADR decision and matching canonical
Runtime/Crosscutting statements, then use those exact fields as the source for
plan and proof-map fixtures.
needs-decision rationale: none; the approved spec already delegates this
closed schema to architecture.

## Finding PBS-AR2

Finding: The claimed commit-level activation and rollback bundle includes
generated packages and clean-installed targets even though those are ephemeral
or release outputs, making the atomic unit impossible to implement as written.
Finding ID: PBS-AR2
Location:
`docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md` lines 91-99;
`docs/architecture/system/architecture.md` Runtime View steps 12-14 and
Crosscutting Concepts lines 978-990
Severity: material
Evidence: Repository governance makes canonical skills authored source and
generated adapter packages release or temporary output, not tracked source.
The ADR says the commit-level activation change includes generated packages
and package/install evidence and that pre-activation rollback reverts the
complete bundle. Generated package directories and clean installed target
trees cannot be reverted by a Git change. The spec requires atomic activation
across those layers, but it does not require those layers to become tracked
commit contents.
Required outcome: Define an implementable two-part atomic boundary: the tracked
activation transaction and the derived proof set that must pass before the
activation marker changes. Define pre-activation rollback as reverting the
tracked source/manifest/selector transaction and regenerating or discarding
derived outputs, while preserving immutable-release rollback after activation.
Recommendation: List the exact tracked commit unit separately from generated,
packed, and installed validation evidence. State that activation-state mutation
is the atomic commit boundary and that ephemeral outputs must be regenerated
from or verified against that exact source identity before activation.
Safe resolution path: Revise the ADR, Runtime View, Crosscutting Concepts,
quality scenario, and risk wording to distinguish tracked rollback from
derived-output invalidation/regeneration without adding a transaction service
or tracking generated packages.
needs-decision rationale: none; existing source/generated boundaries and the
approved activation contract determine the correction.

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| Spec alignment | concern | The selected resource split and selector behavior align, but two architecture-owned readiness conditions remain under-specified or internally inconsistent. |
| Package shape | pass | Lifecycle metadata precedes all 12 arc42 sections, diagrams are linked source files, and the durable decision has an ADR. |
| Boundary clarity | concern | Component responsibilities are clear; the tracked-versus-derived activation boundary is not. |
| Data ownership | concern | The resource owner is clear, but the exact manifest data contract is incomplete. |
| Interface safety | concern | Stable core paths and version compatibility are credible; an unspecified closed manifest can drift across projection and validation implementations. |
| Runtime and failure handling | block | Interrupted projection blocks activation, but pre-activation rollback cannot revert ephemeral package/install layers as written. |
| Deployment and execution boundaries | block | Deployment View identifies generated outputs as derived, while the ADR includes them in a commit-level rollback unit. |
| Security/privacy | pass | No new secrets, personal data, hosted service, or external mutation authority is introduced. |
| Quality and operations | pass | Proportionality, parity, activation, rollback, and measurement scenarios are present and measurable once PBS-AR2 is corrected. |
| Testing feasibility | block | Tests cannot derive the exact closed manifest vocabulary, and rollback fixtures cannot implement the stated commit semantics. |
| Complexity discipline | pass | The design avoids runtime services, context packets, a second semantic model, and premature hard budgets. |
| ADR quality | concern | Context, alternatives, consequences, and follow-up are strong; the decision needs the exact schema and feasible transaction boundary. |
| Plan readiness | block | PBS-AR1 and PBS-AR2 must be resolved before planning can safely freeze implementation slices. |

## Package sufficiency

The context diagram is correctly unchanged because no actor, external system,
or repository system boundary changes. The updated container diagram and
focused component diagram are the right C4 levels and use separate Mermaid
source with role classes, technology labels, and intent-labeled
relationships. No deployment diagram is required once the tracked and derived
activation boundaries are corrected in prose.

All 12 arc42 sections remain present. Runtime, Deployment, Crosscutting,
Architecture Decisions, Quality Requirements, Risks and Technical Debt, and
Glossary were updated for the affected concerns.

## Recommendation

Changes requested.

Record and resolve `PBS-AR1` and `PBS-AR2` through architecture revision, then
run architecture-review R2. No owner decision is required.

This direct review is isolated. It does not edit the reviewed architecture or
ADR and does not automatically continue into revision, plan, test
specification, implementation, or workflow routing.
