# Proposal Review R2: Spec Skill Simplification

Review ID: proposal-review-r2
Stage: proposal-review
Round: r2
Reviewer: external proposal-review supplied by the user and reconstructed by Codex
Target: `docs/proposals/2026-08-15-spec-skill-simplification.md`
Reviewed artifact: commit `e2243953`
Review date: 2026-08-15
Reconstruction status: reconstructed from the complete review result supplied in chat before proposal correction
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: SPSIM-R2-PR1, SPSIM-R2-PR2, SPSIM-R2-PR3
- Open blockers: governed-signal fallback, stale-restart authorization and byte preservation, and boundary-block transition behavior require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision followed by same-stage proposal rereview
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, or continue the workflow

## Overall assessment

The selected package design remains sound: a compact universal `SKILL.md`, one conditional governed-authoring reference, both existing always-loaded boundary references, and one existing structural skeleton. Portable and governed operations are separated, governed resource selection does not grant mutation authority, create and revise operations are identity-bound, identical interrupted transactions are recoverable, `spec-review` remains the independent settlement gate, and no target-agent runtime is added.

Three fail-closed contracts remain incomplete. Invalid governed indicators can disappear into portable classification, stale-attempt detection can lead to replacement without explicit current restart authority or deterministic preservation of nonempty partial content, and the boundary-block matrix overlaps while leaving grandfathered structural adoption unresolved.

## Material findings

### SPSIM-R2-PR1 — Major: invalid governed indicators can be misclassified as portable context

Finding ID: SPSIM-R2-PR1
Source finding ID: SPSIM-PR1
Severity: major
Location: Invocation profiles and resource loading; Portable and governed operations
Evidence: The proposal makes governed candidate context depend on a valid structured owning-change pointer. A malformed, duplicated, escaped, stale, missing-root, or conflicting pointer can therefore fail candidate parsing and appear equivalent to no governed signal, allowing portable revision of an artifact that is attempting to declare governed ownership.
Required outcome: Define a closed tri-state governed-signal classifier in which only absence permits portable authoring and every invalid or ambiguous signal stops without fallback.
Safe resolution path: Use `no-governed-signal`, `single-governed-candidate`, and `invalid-or-ambiguous-governed-signal`; treat any explicit change ID, workflow-managed identity, or structured owning-change field as a signal; require all present signals to resolve to the same exact change.
needs-decision rationale: none; this is a fail-closed classification correction within the selected package.

### SPSIM-R2-PR2 — Major: stale-authoring restart lacks explicit authority and deterministic partial-content preservation

Finding ID: SPSIM-R2-PR2
Source finding ID: SPSIM-PR2
Severity: major
Location: Same-entry stale-authoring restart; Ownership model; Proposal acceptance criteria
Evidence: The proposal distinguishes stale detection from identical retry but does not require an explicit user request or same-change workflow handoff before replacement. It also permits a subjective decision that nonempty content has no durable evidentiary value, allowing different implementations to discard different user-authored bytes.
Required outcome: Separate diagnostic detection from an explicitly authorized restart operation, record the current authority in authoring evidence, deterministically preserve every nonempty matching partial file, and close the restart write set.
Safe resolution path: Require an explicit user request or same-change workflow handoff naming the stale attempt and new basis; snapshot matching nonempty bytes and hash before replacement; record absent or empty states deterministically; stop on unknown, unrelated, conflicting, or unpreservable content.
needs-decision rationale: none; existing authoring evidence can record the decision without a new persistent authorization subsystem.

### SPSIM-R2-PR3 — Major: formal boundary-block applicability and structural adoption are not exhaustive

Finding ID: SPSIM-R2-PR3
Source finding ID: SPSIM-PR3
Severity: major
Location: Structural composition and boundary-block applicability; Proposal acceptance criteria
Evidence: The current matrix can simultaneously require preservation of an existing block and omission for non-applicable work. It does not govern implicit removal, contract deactivation or supersession, adoption by a grandfathered document without unique ordered anchors, or partial, duplicated, and misplaced boundary blocks.
Required outcome: Define a closed transition matrix across current block state, current applicability, revision class, and structural-anchor state, including explicit grandfathered adoption and removal authority.
Safe resolution path: Use block states `absent`, `present-complete`, `present-incomplete`, `present-duplicated`, and `present-misplaced`; preserve complete blocks absent explicit reviewed deactivation; require unique ordered anchors for bounded insertion or an authorized full rewrite; stop on malformed structure or unresolved applicability.
needs-decision rationale: none; the skeleton and feature-authoring reference remain the selected structural owners.

## Architecture assessment

The expected result remains `architecture-not-required` only when restart uses existing artifact-entry and authoring-evidence ownership and introduces no schema, lifecycle state, persistent authority, or write owner. A new persistent restart-authorization surface or cross-stage recovery owner requires architecture reassessment.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path lifecycle procedure and duplicated boundary and layout ownership are concrete and measured. |
| User value | pass | Portable and governed authoring should become easier to scan without losing contract rigor. |
| Option diversity | pass | The alternatives include no change, inline compression, boundary-only extraction, one governed reference, fragmented references, and an executable engine. |
| Decision rationale | pass | One governed reference follows a real mutation-authority boundary while universal quality remains inline. |
| Vision fit | pass | The change supports traceable behavioral contracts and customer portability. |
| Scope control | pass | Boundary redesign, adjacent-skill optimization, runtime machinery, historical rewriting, and permanent gates remain excluded. |
| Portable and governed separation | concern | Valid candidates stop safely, but invalid signals can fall through to portable behavior. |
| Transaction recovery | block | Restart lacks explicit current authority and deterministic preservation of nonempty partial content. |
| Boundary compatibility | block | Block presence, applicability, removal, malformed structure, and grandfathered adoption are not exhaustive. |
| Structural ownership | concern | The owner split is sound after transition behavior is closed. |
| Missing-resource safety | pass | Required resources fail closed without remembered reconstruction. |
| Semantic preservation | pass | Separate rule and literal inventories remain appropriate. |
| Measurement | pass | Both actual loaded profiles must shrink and package growth remains visible. |
| Testing boundary | pass | Static proof and ordinary lifecycle review are proportionate; runtime execution is excluded. |
| Architecture awareness | concern | The expected result depends on keeping restart inside the existing state and evidence model. |
| Readiness for spec | block | SPSIM-R2-PR1 through SPSIM-R2-PR3 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass; the original optimization, solution-selection, branch, governed proposal, and formal review goals remain visibly classified.

## Recommended Proposal Edits

- Recommended edits: add tri-state governed-signal classification, explicit restart authority and deterministic byte preservation, and an exhaustive boundary-block transition and structural-adoption matrix; update ownership, risks, validation, architecture conditions, acceptance criteria, and decision history.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass; all public-skill work items remain classified with valid treatments
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-15-spec-skill-simplification/reviews/proposal-review-r2.md`
- Finding-record paths: this reconstructed detailed review record

## Formal-settlement group

- Review ID: proposal-review-r2
- Review record: `docs/changes/2026-08-15-spec-skill-simplification/reviews/proposal-review-r2.md`
- Review log: `docs/changes/2026-08-15-spec-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-15-spec-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-15-spec-skill-simplification`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview

## Recommendation

- Recommendation: revise the proposal to resolve SPSIM-R2-PR1 through SPSIM-R2-PR3, then run a new independent proposal review against the committed revision. No automatic downstream handoff follows this review.
