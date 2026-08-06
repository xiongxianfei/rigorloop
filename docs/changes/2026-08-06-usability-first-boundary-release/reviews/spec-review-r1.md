# Spec Review R1: Usability-First Boundary-First v0.4.0 Release

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex independent spec-review peer
Target: specs/usability-first-boundary-release.md
Review date: 2026-08-06
Status: changes-requested
Automatic downstream handoff: none

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: UBR-SR1-001, UBR-SR1-002, UBR-SR1-003
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md#spec-review-r1`
- Open blockers: UBR-SR1-001, UBR-SR1-002, UBR-SR1-003
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: Resolve the active-state compatibility boundary, make the three concise-output journeys independently testable, and give helper retirement stable requirement ownership before architecture assessment.

## Findings

## Finding UBR-SR1-001

Finding ID: UBR-SR1-001
Severity: blocking
Location: UBR-R006 through UBR-R008; UBR-R019; State and invariants; Compatibility and migration; BND-STATE-001; BND-COMPAT-001
Evidence: The spec changes activation from tag-dependent public state to tree-local behavior state, but it does not define the complete legal `pending -> active` transition or enumerate which standing activation requirements are replaced. The standing proof-model contract still binds active state to an activating release tag, a transition-parent grandfathering baseline, a complete grandfathered-spec inventory, rollback metadata, and all governed projections. UBR-R006 and UBR-R007 remove the tag discriminator and name only a subset of those fields, while the general exception at lines 153-154 leaves architecture and tests to infer whether baseline derivation, grandfathering inventory, transition immutability, and activating-release semantics are retained, replaced, or removed.
Required outcome: Define one complete tree-local activation transition and an exact compatibility disposition for every standing activation subject changed by this spec, including activating-release meaning, rollback selection, grandfathering baseline and inventory, canonical and projected resources, legal and illegal transitions, and the boundary between local activation and public release proof.
Safe resolution path: Add one compact requirement/table that retains the existing manifest fields and grandfathering behavior needed for historical compatibility, reclassifies `activating_release: v0.4.0` as release intent rather than tag proof, requires canonical/generated/package coherence before `active`, removes tag and network presence only from local activation acceptance, and explicitly names the standing proof-model requirements or subjects superseded by that change. Update BND-STATE-001 and BND-COMPAT-001 without adding new dimensions or Git publication choreography.
needs-decision rationale: none; the approved proposal already selects tree-local activation and preservation of historical compatibility.

## Finding UBR-SR1-002

Finding ID: UBR-SR1-002
Severity: major
Location: Examples E1 through E3; UBR-R001 through UBR-R003; UBR-R018; AC-UBR-001, AC-UBR-002, AC-UBR-011; BND-INPUT-001
Evidence: The three representative journeys name artifact categories but no concrete task, admitted interfaces, expected included boundaries, or intentionally omitted scenarios. “Cover material boundaries” is therefore both the rule being tested and the unstated oracle. A test-spec author would have to invent which boundaries make the spec, inspection, and code-review fixtures correct, so semantic journey assertions cannot independently distinguish concise correctness from superficial or exhaustive output.
Required outcome: Give each representative journey a small, concrete fixture contract with observable inclusion and omission expectations, without introducing exact prose, word-count, bullet-count, or fixed global scenario-count checks.
Safe resolution path: Add one bounded example/table row each for specification, code inspection, and code review. For each, name a simple behavior or diff, two or three correctness-relevant boundaries that must be handled, at least one remote scenario that must be omitted unless explicitly requested, and the observable stage-owned result. Keep the fixtures illustrative of existing requirements rather than adding a broad scenario matrix.
needs-decision rationale: none; the proposal already requires these three representative journeys and rejects brittle verbosity checking.

## Finding UBR-SR1-003

Finding ID: UBR-SR1-003
Severity: major
Location: UBR-R013; Compatibility and migration lines 149-151; EC9; AC-UBR-008
Evidence: The exact checker, publisher, test, and selector retirement inventory appears only as lower-case normative prose outside the stable requirement set. UBR-R013 and AC-UBR-008 prohibit those paths from ordinary selection and release execution, but they still permit the rejected helpers and candidate protocol to remain as dormant or apparently supported repository surfaces. That is weaker than the proposal's explicit same-slice removal and gives the test spec no stable requirement ID for exact retirement proof.
Required outcome: Give the exact custom-helper and candidate-only selector retirement one stable testable requirement while preserving the standing structural boundary validator and routine release checks.
Safe resolution path: Amend UBR-R013 or add one adjacent requirement that names the three retired helper/test files and the five files whose candidate-only behavior must be removed, states whether each surface is deleted or reduced to its standing tree-local role, and maps AC-UBR-008 and the compatibility inventory to that ID. Use `MUST NOT` for the release-path prohibition instead of `No ... MAY`.
needs-decision rationale: none; the approved proposal and proposal review already require exact retirement and preservation of ordinary validation.

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | block | The active transition and its retained manifest semantics are incomplete. |
| normative language | concern | Exact helper retirement is buried outside stable requirement IDs, and UBR-R013 uses an avoidable `No ... MAY` prohibition. |
| completeness | block | The tag-era activation compatibility disposition is not closed. |
| testability | block | The concise-output journeys lack independent semantic oracles. |
| examples | concern | Release examples are concrete; the three usability examples remain category-level. |
| compatibility | block | Standing activation requirements are overridden only by a broad subject exception. |
| observability | pass | Local activation, public release, failure, and closeout claims are visibly separated. |
| security/privacy | pass | Local checks and committed evidence have clear credential and private-data limits. |
| non-goals | pass | The spec consistently rejects exhaustive matrices, brittle prose checks, and custom publication machinery. |
| acceptance criteria | block | AC-UBR-001/002 lack fixture-owned expected outcomes, and AC-UBR-008 is weaker than the intended exact retirement. |

## Exact wording direction

- Add a compact “tree-local activation transition” requirement that lists retained manifest invariants and explicitly removes only tag/network proof from local activation.
- Add three concrete journey rows with required inclusions, required omissions, and observable stage outcomes; do not add prose-length metrics.
- Move the exact retirement inventory under a stable `UBR-R...` requirement and change the UBR-R013 prohibition to `MUST NOT`.
- Update the existing state, compatibility, input, composition, examples, and acceptance mappings only where these corrections require it; do not add more dimensions or speculative release scenarios.

## Recommendation

Changes requested.
The direction is appropriately simpler and preserves the right routine release safeguards, but architecture and test-spec work would currently have to guess at activation compatibility and the semantic journey oracle.

This direct review is isolated and does not start spec revision, architecture, planning, test specification, implementation, or release work.
