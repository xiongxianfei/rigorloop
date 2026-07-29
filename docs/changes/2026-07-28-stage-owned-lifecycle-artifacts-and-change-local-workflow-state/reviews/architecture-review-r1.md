# Architecture Review R1

Review ID: architecture-review-r1
Stage: architecture-review
Round: 1
Reviewer: Codex architecture-review skill
Target: docs/architecture/system/architecture.md;
docs/architecture/system/diagrams/container.mmd;
docs/architecture/system/diagrams/component-workflow-automation.mmd;
docs/adr/ADR-20260729-stage-owned-change-local-lifecycle-state.md
Status: changes-requested
Original review source: User-requested `$architecture-review` on 2026-07-29.
Material findings: SLA-AR1
Immediate next stage: architecture revision
Automatic downstream handoff: none

## Result

- Review surface: `canonical-architecture-update`, `ADR`
- Review status: changes-requested
- Material findings: SLA-AR1
- Recording status: recorded
- Recording blocker: none
- Review record:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/architecture-review-r1.md`
- Review log:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-log.md`
- Review resolution:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-resolution.md#architecture-review-r1`
- Open blockers: SLA-AR1
- Required canonical updates: Complete the stage-owned model projection across
  current runtime, boundary, quality, glossary, follow-on, readiness, and
  component-diagram statements.
- Required ADR updates: None. The proposed ADR is coherent, bounded, and
  records its supersession scope clearly.
- Next stage: architecture revision, followed by a fresh architecture-review

## Review inputs

- Constitution: `CONSTITUTION.md`
- Repository instructions: `AGENTS.md`
- Architecture method: `specs/architecture-package-method.md`
- Accepted proposal:
  `docs/proposals/2026-07-28-approved-specification-baselines-and-controlled-amendment-workflow.md`
- Approved feature specification:
  `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`
- Approved spec review:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/spec-review-r6.md`
- Canonical architecture: `docs/architecture/system/architecture.md`
- Container diagram:
  `docs/architecture/system/diagrams/container.mmd`
- Workflow component diagram:
  `docs/architecture/system/diagrams/component-workflow-automation.mmd`
- Proposed ADR:
  `docs/adr/ADR-20260729-stage-owned-change-local-lifecycle-state.md`
- Related ADR:
  `docs/adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md`

## Findings

## Finding SLA-AR1

Finding: The canonical package still makes retired workflow profiles,
capabilities, policy-registry fields, and receipt-era state normative alongside
the new stage-owned model.
Finding ID: SLA-AR1
Location: `docs/architecture/system/architecture.md` Runtime View steps 19,
27, 29, and 30; Independent adversarial review gate boundary; Quality
Requirements; Glossary; Follow-on artifacts; Readiness; and
`docs/architecture/system/diagrams/component-workflow-automation.mmd` lines
39-42
Severity: material
Evidence: The revised architecture says one target is sufficient
repository-local consent and explicitly removes parent authorization,
effective capability, activation-selector, risk-profile, and selector-ledger
layers. However, Runtime View still advances and authorizes through workflow
profiles and names an implementation profile. The review-gate boundary still
depends on profile state and profile-off behavior. The quality table still
requires an immutable sixteen-field stage-policy projection and a
profile-managed review invocation. The glossary and current follow-on summary
still describe authority, transition receipts, implementation-profile
correction, two-level authority, and prepared transition receipts as current
architecture. The component diagram also draws generated adapters as the
source of author, reviewer, and workflow boundaries even though they are
derived from canonical published skills. These statements contradict
SLA-R052, SLA-R059, SLA-R067, SLA-R072 through SLA-R074c, AC-SLA-018,
AC-SLA-026, AC-SLA-030, and AC-SLA-032.
Required outcome: Present one internally consistent current architecture in
which `change.yaml` owns mutable lifecycle state, author and review peers own
only matching transitions, workflow owns routing, and one structured target
is sufficient repository-local continuation consent without a retired
profile, capability, policy-registry, or receipt state layer.
Recommendation: Reproject every remaining current statement from the retired
model. Replace profile-authorized routing with target, prerequisite, and fixed
write-boundary checks; remove the sixteen-field policy-registry quality
requirement and capability-era glossary claims; describe retained
review-independence evidence without making it another workflow authorization
profile; classify superseded profile designs as historical; update the
readiness/ADR summary; and reverse the adapter relationships so canonical
skills generate or constrain adapters.
Safe resolution path: Revise only the named canonical sections and component
diagram, preserving the independent adversarial review and
requirement-fidelity safeguards as review gates. Keep the new ADR's decision
and explicit ADR-20260721 supersession boundary unchanged unless the canonical
reprojection exposes a real decision conflict. Then rerun architecture-review.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| Spec alignment | block | Current profile, capability, policy, and receipt requirements contradict the approved simplified state and consent model. |
| Package shape | pass | The update uses the canonical arc42 package, linked C4 source diagrams, and a dedicated ADR. |
| Boundary clarity | concern | The new ownership boundary is clear in prose, but the adapter relationships point from derived output toward canonical skill owners. |
| Data ownership | pass | The proposed model separates `artifact_states`, `workflow_state`, target state, and evidence links without duplicating governed content. |
| Interface safety | block | Two current automation contracts remain visible: target-only continuation and profile/capability authorization. |
| Runtime and failure handling | block | Recovery is addressed, but current runtime steps still route correction and closeout through retired profiles. |
| Deployment and execution boundaries | pass | The design remains repository-local and introduces no service, database, deployment target, or external action. |
| Security/privacy | pass | The external-action boundary remains human controlled, and the design adds no secrets or privileged runtime. |
| Quality and operations | block | The quality table still mandates the removed sixteen-field stage-policy registry. |
| Testing feasibility | block | A plan or test spec could implement either the removed registry contract or the approved stage-owned contract. |
| Complexity discipline | block | Retaining current profile and capability language defeats the approved simplification. |
| ADR quality | pass | The ADR records context, decision, alternatives, consequences, follow-up, and precise partial supersession. |
| Plan readiness | block | Planning must wait until the canonical package has one unambiguous current model. |

## Missing package elements

No required arc42 section, C4 source view, ADR section, or deployment view is
missing. The issue is consistency inside the otherwise complete package.

## Recommendation

Changes requested.

SLA-AR1 must be recorded before its architecture revision and resolved by a
fresh architecture-review. No owner decision is needed because the approved
spec and proposed ADR already select the governing model.

This direct review is isolated. It does not automatically hand off to
architecture revision, plan, test specification, implementation, or workflow
automation.
