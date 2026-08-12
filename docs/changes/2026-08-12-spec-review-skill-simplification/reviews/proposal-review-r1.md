# Proposal Review R1: Spec-Review Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-12-spec-review-skill-simplification.md`
Reviewed artifact: commit `360dcbb6`
Review date: 2026-08-12
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: SRSIM-PR1, SRSIM-PR2, SRSIM-PR3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-12-spec-review-skill-simplification/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-12-spec-review-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-12-spec-review-skill-simplification/review-resolution.md`
- Open blockers: invocation authority, result-group applicability, and boundary activation ownership require proposal revision
- Immediate next stage: proposal revision
- Automatic downstream handoff: none

## Overall assessment

The proposal chooses a proportionate package shape: a shorter universal skill, one new recording-and-settlement reference, the two existing projected boundary references, and the two existing structural assets. It correctly avoids a generic review engine, target-agent acceptance, permanent size gates, and excessive reference fragmentation.

The proposal also identifies the most important compatibility constraint: existing contracts require review judgment, recording obligations, lifecycle boundaries, and a checked compact boundary scan to remain inline. Three contracts still need proposal-level closure before specification can encode the design without guessing.

## Material findings

### SRSIM-PR1 — Major: formal-review recording and governed settlement authority are conflated

Finding ID: SRSIM-PR1
Severity: major
Location: Closed invocation predicates; Recording-and-settlement reference ownership
Evidence: `formal_lifecycle_context` is defined only when a governed change grants settlement authority, while `durable_recording_context` treats other reviews as advisory. Repository policy defines every supported invocation of `spec-review` as a formal lifecycle review for recording purposes, including direct isolated clean reviews that may need a generated minimal receipt root. Isolation removes downstream continuation, not formal recording. The current model could therefore let a direct clean `spec-review` use `SR0-core` and skip required recording, or incorrectly treat a generated recording root as advisory rather than formal evidence.
Required outcome: Separate review-kind, recording-location, settlement-authority, and automation classifications. Make supported `spec-review` formal recording exhaustive without implying governed settlement or workflow continuation.
Safe resolution path: Use `review_kind: formal-lifecycle | non-formal-review-like`, `recording_mode: required | not-required`, `settlement_mode: isolated | governed-spec-entry`, and `automation_mode: manual | workflow-managed-automated`. Every formal-lifecycle review has `recording_mode: required`; an isolated formal review may create or use a minimal review-recording root but has `settlement_mode: isolated`. Only exact same-change governed evidence selects `governed-spec-entry`, and automation additionally requires that governed settlement context. Treat `not-required` only as the existing non-formal review-like exception.
needs-decision rationale: none; existing formal-review-recording and lifecycle contracts already determine this ownership split.

### SRSIM-PR2 — Major: the existing result asset cannot express the proposed profiles without a closed applicability contract

Finding ID: SRSIM-PR2
Severity: major
Location: Asset ownership; Closed loaded-resource profiles
Evidence: The existing result asset always includes recording paths but contains no explicit boundary-result, settlement-result, automation-manifest, or authority group. The proposal says inapplicable optional sections are omitted but does not define which structural groups exist, which profiles select them, or whether expanding the asset would violate the older two-asset structural-only contract. Static scenarios and implementation would have to invent the layout boundary.
Required outcome: Define one core result group and closed recording, governed-settlement, boundary-review, and automated-review groups, including exact applicability, omission, blocked-data, and placeholder behavior. Confirm that the existing two assets remain sufficient and that no group owns policy.
Safe resolution path: Keep core status, findings, blockers, immediate stage, eventual readiness, and stop condition in every result; include recording fields for formal reviews; add governed-settlement fields only for same-change settlement; add boundary outcome fields only when boundary-first applies; add automation receipt fields only for workflow-managed automation. Omit inapplicable groups, report applicable unavailable data explicitly, and amend only directly coupled asset-contract wording necessary to allow structural groups.
needs-decision rationale: none; the proposal already selects the existing asset as the sole result structure.

### SRSIM-PR3 — Major: boundary-first activation is described as local predicates despite an existing checked-revision owner

Finding ID: SRSIM-PR3
Severity: major
Location: Closed invocation predicates; Boundary reference ownership
Evidence: The proposal defines `boundary_first_context` and `formal_boundary_record_context` locally but does not bind them to `specs/boundary-first-resources.yaml`, the checked-revision activation contract, or the existing distinction between compact scan, compact-core loading, and feature-authoring loading. It also says formal feature-record review may load the feature reference as an additive subcondition without specifying whether the compact core is always loaded first. This risks creating a second activation owner or changing grandfathering behavior during a simplification.
Required outcome: Preserve the existing boundary activation owner and define only the spec-review consumption mapping. Close the load order and false, late, grandfathered, substantive-revision, and missing-resource cases without inventing another activation policy.
Safe resolution path: State that the checked-revision boundary contract determines activation. Always run the inline four-question scan. Load `boundary-first-method-v1.md` when active boundary interpretation is required; load `boundary-first-feature-authoring-v1.md` only after the method reference when formal feature-record completeness or substantive grandfathered revision is judged. Non-substantive grandfathered reviews do not activate formal record adoption. Unknown substantive classification or required missing resources stops approval.
needs-decision rationale: none; existing boundary architecture and projection manifests already own these decisions.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path overload and overlapping ownership are concrete and measured. |
| User value | pass | Ordinary spec review should become easier to scan without weakening rigor. |
| Option diversity | pass | Unchanged, inline-only, boundary-only, one-reference, fragmented, and runtime alternatives are materially different. |
| Decision rationale | pass | One new reference is proportionate if authority and activation are closed. |
| Vision fit | pass | The direction improves reviewability while preserving durable evidence. |
| Scope control | pass | Adjacent skills, runtime machinery, and permanent simplicity gates remain excluded. |
| Architecture awareness | pass with revisions | Existing package architecture likely suffices, but boundary activation must remain externally governed. |
| Testability | block | Static fixtures cannot deterministically classify formal recording, result groups, or boundary loads yet. |
| Risk honesty | concern | The proposal names authority and activation risks but does not fully close them. |
| Rollout realism | pass | Atomic package rollout, parity, rollback, and no-data-migration boundaries are sound. |
| Readiness for spec | block | SRSIM-PR1 through SRSIM-PR3 require proposal revision. |

## Scope preservation review

All initial user goals remain in scope. The findings refine the selected package rather than adding another skill, runtime, asset family, or architecture model. Vision fit remains valid.

## Recommendation

Revise the proposal to separate formal recording from governed settlement, close result-asset structural groups, and defer boundary activation truth to the existing checked-revision contract. Then rerun independent `proposal-review` against a frozen revision.

No automatic downstream handoff follows this review. The proposal is not ready for specification.
