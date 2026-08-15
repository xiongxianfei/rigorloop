# Proposal Review R1: Spec Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-15-spec-skill-simplification.md`
Reviewed artifact: commit `5650fe20`
Review date: 2026-08-15
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: SPSIM-PR1, SPSIM-PR2
- Open blockers: stale-authoring recovery authority and skeleton/boundary-block composition require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, or continue the workflow

## Overall assessment

The proposal selects the right package boundary: a compact universal behavioral-contract skill, one governed authoring reference, both existing boundary-first references under their approved loading profile, and the existing skeleton. It correctly avoids fragmenting universal specification quality and avoids changing the boundary model merely to reduce context.

The proposal also uses honest acceptance surfaces. Both real procedural profiles must shrink, existing boundary resources remain visible in those profiles, assets and total package size are reported separately, and no target-agent runtime or new permanent simplicity gate is introduced.

Two contracts remain incomplete. The stale-authoring recovery model assumes a reusable workflow authorization mechanism that is not established for `spec`, and the proposal assigns ordinary structure and formal boundary structure to different owners without defining their composition point or when the formal block appears.

## What is strong

### The progressive-disclosure boundary follows lifecycle authority

Portable specification writing needs behavioral-contract judgment but cannot mutate a RigorLoop change record. Governed proposal settlement, entry mutation, authoring evidence, retry, and lifecycle transition form one legitimate conditional procedure.

### Boundary-first compatibility is preserved

The proposal does not treat the large shared references as arbitrary extraction targets. It preserves the approved compact-core and feature-authoring resource identities, byte ownership, consumer set, and representative initial-loading profile while removing only duplicated stage-local procedure.

### Universal specification quality remains inline

Requirements, examples, failure behavior, compatibility, observability, security, accessibility, performance, edge cases, non-goals, acceptance criteria, stops, claims, and `spec-review` handoff remain universal obligations rather than optional references.

### Measurement and proof are proportionate

The proposal measures `SA0` and `SA1` instead of claiming success from a smaller main file. Rule and literal inventories, deterministic scenarios, package parity, and ordinary lifecycle review provide suitable evidence without runtime transcript grading.

## Material findings

### SPSIM-PR1 — Major: stale-authoring recovery assumes an unowned authorization contract

Finding ID: SPSIM-PR1
Severity: major
Location: Stale governed authoring attempts; Ownership model; Architecture assessment
Evidence: The proposal says workflow issues exact current reset authorization and the governed spec reference consumes it while adding no evidence type, persistence mechanism, or write owner. The current general lifecycle contract permits `spec` to mutate its own entry and evidence but does not define this workflow-owned reset authorization. The accepted proposal-skill contract defines such authorization specifically for proposal, while the accepted test-spec contract uses a different same-entry restart owned by test-spec. Neither stage-specific contract automatically grants the mechanism to `spec`.
Required outcome: Select one complete stale-authoring recovery contract for `spec`, identify its existing or newly amended governing authority, define the exact resulting entry/evidence state, and align the architecture expectation with that decision.
Safe resolution path: Prefer a same-entry `restart-stale-authoring` procedure owned by `spec`, following existing stage ownership: workflow may classify and route, while spec validates the exact `authoring` entry, no review or downstream reliance, preserved artifact ID/kind/role/path, replacement authoring-evidence identity, and treatment of partial bytes. If the proposal retains workflow reset authorization instead, it must cite or amend an exact governing workflow contract and acknowledge architecture work if that adds a persistent authorization surface.
needs-decision rationale: none; the selected package can remain unchanged while the recovery contract is made executable.

### SPSIM-PR2 — Major: ordinary skeleton and boundary-record structures have no closed composition interface

Finding ID: SPSIM-PR2
Severity: major
Location: Context; Ownership model; Expected Behavior Changes; Required-resource failure behavior
Evidence: The proposal keeps ordinary headings in `spec-skeleton.md` and the contiguous `Boundary model`, `Boundary definitions`, `Selected interactions`, and `Example ownership` block in the feature-authoring reference. It removes the main file's complete section inventory, but it does not state where the formal block is inserted relative to the skeleton or when an initially loaded boundary reference produces no formal block. Initial resource loading and output applicability are different contracts; without an insertion and omission rule, valid implementations can produce different document order or emit formal tables for non-applicable work.
Required outcome: Define one structural composition point and a closed applicability/omission rule without duplicating the boundary block or moving semantic policy into the skeleton.
Safe resolution path: Add one conditional boundary-record insertion point to the existing skeleton, placed after `Error and boundary behavior` and before `Compatibility and migration`. The skeleton owns that position only; the feature-authoring reference continues owning the four contiguous headings and tables. Emit the block when the active boundary contract requires a formal feature record; omit the insertion point completely for valid non-applicable or grandfathered non-substantive work. Applicable but unresolved formalization blocks readiness rather than leaving a placeholder.
needs-decision rationale: none; this preserves both existing owners and supplies the missing interface.

## Architecture assessment

The expected architecture result remains `architecture-not-required` if SPSIM-PR1 adopts a spec-owned same-entry restart using existing artifact ownership and no new persistent authorization surface. A bounded architecture documentation correction is needed only for a stale package inventory or structural example.

Architecture becomes required if recovery introduces a new workflow-owned persisted authorization record, lifecycle state, write owner, or cross-stage mutation contract. The revised proposal must make this dependency explicit rather than asserting no architecture impact before choosing the recovery mechanism.

## Acceptance criteria to add

| ID | Criterion |
| --- | --- |
| `AC-SPSIM-001` | Stale-authoring recovery names one exact owner, authority source, operation, identity basis, and resulting state. |
| `AC-SPSIM-002` | Workflow routing alone cannot grant spec-owned mutation without the selected governing contract. |
| `AC-SPSIM-003` | A same-entry restart preserves artifact ID, kind, role, normalized path, and `authoring` state. |
| `AC-SPSIM-004` | Restart replaces only authorized incomplete authoring evidence and preserves required partial bytes or records their disposition. |
| `AC-SPSIM-005` | Review or downstream reliance, ambiguous identity, competing writes, or illegal state blocks restart. |
| `AC-SPSIM-006` | The ordinary skeleton defines one conditional insertion point for the formal boundary-record block. |
| `AC-SPSIM-007` | The feature-authoring reference remains the sole owner of the four contiguous boundary headings and tables. |
| `AC-SPSIM-008` | Initial loading of boundary resources does not by itself require emitting a formal boundary block. |
| `AC-SPSIM-009` | Inapplicable boundary structure is omitted and applicable unresolved structure blocks without placeholders. |
| `AC-SPSIM-010` | Both real procedural profiles decrease in words and bytes from the recorded baseline. |
| `AC-SPSIM-011` | No target-agent runtime or separate manual semantic-review acceptance stage is introduced. |
| `AC-SPSIM-012` | Canonical, generated, archived, release-candidate, and installed resources retain required parity. |

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path lifecycle procedure and duplicated boundary/layout ownership are concrete and measured. |
| User value | pass | Portable and governed specification authoring should become easier to scan without losing contract rigor. |
| Option diversity | pass | Unchanged, editorial compression, boundary-only extraction, one governed reference, fragmented references, and an executable engine are materially different. |
| Decision rationale | pass | One governed reference follows a real mutation-authority boundary while universal quality remains inline. |
| Vision fit | pass | The change supports traceable, reviewable behavioral contracts and customer portability. |
| Scope control | pass | Boundary redesign, adjacent-skill optimization, runtime machinery, historical rewriting, and new permanent gates are excluded. |
| Boundary compatibility | pass with revisions | Resource identities and initial loading are preserved; output applicability and composition still need closure. |
| Governed operations | pass with revisions | Create, revise, and identical retry are closed; changed-basis recovery is not. |
| Recovery authority | block | The proposed workflow authorization mechanism is not currently owned for `spec`. |
| Structural ownership | block | Two valid structural owners lack one deterministic composition interface. |
| Testing boundary | pass | Static proof, package parity, and normal lifecycle review are proportionate; runtime execution is excluded. |
| Measurement | pass | Real loaded profiles and total package size are separated with no fixed normative percentage. |
| Architecture awareness | concern | The result depends on which recovery contract is selected. |
| Readiness for spec | changes-requested | SPSIM-PR1 and SPSIM-PR2 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass; optimization, solution selection, branch creation, governed proposal authoring, and formal review are all visible and classified.

## Recommended Proposal Edits

- Recommended edits: replace the unowned reset-authorization assumption with one governed same-entry restart or an explicitly amended workflow contract; add the boundary-block insertion point and output-applicability matrix; update risks, architecture assessment, validation scenarios, and acceptance criteria accordingly.

## Specialized-gate group

- Active gate predicates: `initial_intent_table_context`, `scope_budget_context`
- Gate outcomes: pass for the reviewed artifact; all user goals and public-skill work items are classified with valid treatments
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-15-spec-skill-simplification/reviews/proposal-review-r1.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: proposal-review-r1
- Review record: `docs/changes/2026-08-15-spec-skill-simplification/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-15-spec-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-15-spec-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-15-spec-skill-simplification`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview

## Recommendation

- Recommendation: revise the proposal to resolve SPSIM-PR1 and SPSIM-PR2, then run a new independent proposal review against the committed revision. No automatic downstream handoff follows this review.
