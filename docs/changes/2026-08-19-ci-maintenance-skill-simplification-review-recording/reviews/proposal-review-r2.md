# Proposal Review: CI-Maintenance Skill Simplification

Review ID: proposal-review-r2
Stage: proposal-review
Round: 2
Reviewer: user-supplied independent proposal-review result, recorded by Codex
Target: `docs/proposals/2026-08-19-ci-maintenance-skill-simplification.md`

Reviewed artifact: `docs/proposals/2026-08-19-ci-maintenance-skill-simplification.md` at `sha256:4411a998c3514c13a5d457606ab6af970d53a1a2dc0e6b0b0eb97c5d67c566f5`
Review date: 2026-08-19
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: CIMSIM-PR4, CIMSIM-PR5, CIMSIM-PR6, CIMSIM-PR7
- Open blockers: check-placement ownership, privileged loaded assemblies, conditional-write safety, and dependency-aware multi-target behavior require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: focused proposal revision followed by same-stage proposal rereview
- Automatic downstream handoff: none
- Claim limitations: this isolated review records judgment only; it does not settle the portable proposal, activate lifecycle authority, authorize specification, or continue workflow

## Overall assessment

The selected package remains appropriate:

```text
compact SKILL.md
+ one GitHub authoring reference
+ existing risk-to-check map
+ simplified GitHub workflow skeleton
+ no scripts
```

The revised operation, target, concern, provider, privilege, structure, and hosted-observation axes materially improve the contract. Prior findings `CIMSIM-PR1` through `CIMSIM-PR3` are directionally resolved. Four narrower but material contracts remain incomplete: semantic risk placement has two owners, approved privileged authoring has no exhaustive assembly, generic atomic replacement does not prevent concurrent clobbering, and multi-target decomposition does not model dependencies or safe partial completion.

## Material findings

### CIMSIM-PR4 - Check-placement policy has overlapping owners

Finding ID: CIMSIM-PR4
Severity: major
Location: GitHub authoring-reference ownership and risk-to-check-map ownership
Evidence: The proposal assigns PR checks versus slower boundary checks to the authoring reference while also assigning PR, merge, release, schedule, and other boundary placement to the risk map. Either resource could therefore decide which risk runs at which boundary.
Required outcome: Give semantic risk, check, command, and execution-boundary placement one owner, and limit GitHub procedure to serialization.
Safe resolution path: Let the risk map own `changed path -> risk -> check -> authoritative command -> required boundary`. Let the GitHub authoring reference translate only a settled mapping into jobs, events, expressions, paths, matrices, and dependencies. Stop on a conflict rather than choosing local precedence.
needs-decision rationale: none; ownership can be closed without changing the package shape.

### CIMSIM-PR5 - Approved privileged implementation has no complete assembly

Finding ID: CIMSIM-PR5
Severity: major
Location: privileged authority matrix, authoring-reference scope, skeleton ownership, and loaded assemblies
Evidence: The proposal permits create or revise under an exact approved privileged design, but the authoring reference and loaded assemblies cover only ordinary GitHub work and do not identify the approved design or approving review as required external evidence.
Required outcome: Add a closed privileged approved-design authoring family or remove privileged mutation support.
Safe resolution path: Add a named privileged approved-design assembly using `SKILL.md`, the GitHub authoring reference, exact approved design and approving review as external evidence, the risk map when coverage-sensitive, and the skeleton only for creation or authorized structural replacement. Missing design fields retain safe defaults or stop and are never inferred.
needs-decision rationale: none; preserving the already-selected compatibility behavior is preferred.

### CIMSIM-PR6 - Generic atomic replacement does not prevent concurrent clobbering

Finding ID: CIMSIM-PR6
Severity: major
Location: single-file write protocol and retry behavior
Evidence: A re-read followed by an overwrite-capable atomic rename can still replace a file created or changed by another actor between validation and commit. Read-back proves the result but does not prove that concurrent work was preserved.
Required outcome: Use distinct conditional commit semantics for creation and revision.
Safe resolution path: Creation uses atomic no-clobber creation. Revision uses identity-guarded replacement through compare-and-swap, an exclusive transient lock, or an equivalent safe primitive. Unsupported conditional-write capability blocks. Idempotent success requires exact intended content and unchanged decision evidence.
needs-decision rationale: none; transient conditional writes preserve the provisional no-architecture result.

### CIMSIM-PR7 - Multi-target decomposition lacks dependency and partial-state rules

Finding ID: CIMSIM-PR7
Severity: major
Location: target-kind classification, multi-target decomposition, and single-file mutation protocol
Evidence: Validation scripts, platform configuration, and thin workflow wrappers can depend on one another. Ordered independent writes can leave a workflow referencing a missing command or a command change temporarily invalidating its current workflow. The proposal does not classify dependency, intermediate validity, or aggregate partial outcomes.
Required outcome: Add a bounded dependency-aware non-atomic batch contract.
Safe resolution path: Classify target sets as `independent`, `ordered-dependent`, or `atomic-group-required`; prepare and cross-validate all targets before writing; commit dependency providers before wrappers; stop unsupported atomic groups before mutation; report `complete`, `partial-blocked`, or `blocked-before-write`; and re-resolve the full target graph on retry.
needs-decision rationale: none; dependency-aware batches remain compatible with the one-file commit boundary.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path overload and unsafe skeleton defaults remain concrete. |
| User value | pass | Narrow review and revision should load less unrelated procedure. |
| Option diversity | pass | Flat, compressed, catch-all, focused, fragmented, and executable alternatives remain distinct. |
| Decision rationale | pass | One authoring reference, one conditional map, and one skeleton remain proportionate. |
| Scope control | pass | Live CI, runtime generation, historical migration, and external platform mutation remain excluded. |
| Operation and concern model | pass | The independent axes are directionally sound. |
| Policy ownership | block | Semantic check placement is duplicated. |
| Privileged implementation | block | A supported path lacks a named assembly and realization branch. |
| Single-file concurrency | block | Atomic replacement alone is not no-clobber or identity-guarded. |
| Multi-target behavior | block | Dependencies, intermediate validity, and partial results are incomplete. |
| Hosted-CI truthfulness | pass | Hosted observation remains fixed and non-authoritative. |
| Structural ownership | pass | The reduced skeleton is safe and non-normative. |
| Testing boundary | pass | Static and package proof remain appropriate. |
| Architecture awareness | concern | No-architecture depends on avoiding persistent coordination and external state. |
| Readiness for spec | changes-requested | Resolve CIMSIM-PR4 through CIMSIM-PR7. |

## Scope Preservation Review

- Scope-preservation result: pass; the initial goals and work-item treatments remain explicit, and the requested corrections do not expand the selected package shape.

## Recommended Proposal Edits

- Assign semantic boundary placement exclusively to the risk map and GitHub serialization to the authoring reference.
- Add a privileged approved-design assembly family and complete design-basis fields.
- Replace generic atomic replacement with no-clobber create and identity-guarded revise.
- Add dependency classification, safe ordering, intermediate-validity checks, partial results, and fresh-graph retry for multi-target requests.
- Add a closed target-kind and provider compatibility matrix for repository-file targets.

## Recommendation

- Recommendation: changes-requested. Retain the package direction, revise `CIMSIM-PR4` through `CIMSIM-PR7`, and perform a fresh isolated rereview. No automatic downstream handoff follows.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass; the scope budget remains complete
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-19-ci-maintenance-skill-simplification-review-recording/reviews/proposal-review-r2.md`
- Finding-record paths: this detailed review record and `review-resolution.md#proposal-review-r2`

## Formal-settlement group

- Review ID: `proposal-review-r2`
- Review record: `docs/changes/2026-08-19-ci-maintenance-skill-simplification-review-recording/reviews/proposal-review-r2.md`
- Review log: `docs/changes/2026-08-19-ci-maintenance-skill-simplification-review-recording/review-log.md`
- Review resolution: `docs/changes/2026-08-19-ci-maintenance-skill-simplification-review-recording/review-resolution.md#proposal-review-r2`
- Proposal settlement: not-settled; the recording-only root has no proposal lifecycle authority
- Governed change identity: none; recording-only root `2026-08-19-ci-maintenance-skill-simplification-review-recording`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview
