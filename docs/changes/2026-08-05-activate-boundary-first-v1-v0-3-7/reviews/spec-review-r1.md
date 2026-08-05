# Specification Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: independent Codex spec-review peer
Target: specs/boundary-first-v1-v0-3-7-activation-release.md
Status: changes-requested
Material findings: BFA-SR1-001, BFA-SR1-002, BFA-SR1-003, BFA-SR1-004
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready
Automatic downstream handoff: workflow-owned after recording

## Result

- Skill: spec-review
- Review status: changes-requested
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/review-log.md`
- Review resolution: `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/review-resolution.md`
- Open blockers: BFA-SR1-001, BFA-SR1-002, BFA-SR1-003, BFA-SR1-004
- Immediate next stage: spec revision, with BFA-SR1-002 routed through proposal revision first
- Eventual test-spec readiness: not-ready

## Material Findings

## Finding BFA-SR1-001

Finding ID: BFA-SR1-001
Severity: blocking
Location: Glossary; BFA-R008 through BFA-R021; state and invariants; BND-AUTH-001
Evidence: The spec uses `B` both as transition `T`'s first parent/grandfathering baseline and as the expected remote `main` compare-and-swap value. Normal pre-transition preparation commits make `B` later than the remote branch fork point.
Required outcome: Define publication base `P` separately from grandfathering baseline `B`, then require `P` to equal or precede `B` on the same first-parent chain `P ... B -> T ... H`.
Safe resolution path: Candidate output and diagnostics expose `P/B/T/H`; remote compare-and-swap uses `P`; the activation manifest baseline remains `B`; remote `main` fast-forwards from `P` to `H`; all identity, example, boundary, interaction, and acceptance mappings use the four identities consistently.
needs-decision rationale: none; separate identities are required for any valid pre-transition preparation history.

## Finding BFA-SR1-002

Finding ID: BFA-SR1-002
Severity: blocking
Location: BFA-R001; proposal release decision
Evidence: BFA-R001 mandates patch release `v0.3.7`, but activation adds backward-compatible public skill and adapter behavior. Governing release-process requirements REL-R9 and REL-R10 reserve patches for changes that add no public behavior and require a minor release for backward-compatible public skill behavior.
Required outcome: Select the contract-compliant next minor release `v0.4.0`, or amend the higher-ranked release versioning contract before retaining a patch.
Safe resolution path: Route to proposal, replace `v0.3.7`/`0.3.7` with `v0.4.0`/`0.4.0`, retain `v0.3.6` as immediate rollback, and rereview the proposal before revising the spec.
needs-decision rationale: none; the governing release contract already determines the minor classification.

## Finding BFA-SR1-003

Finding ID: BFA-SR1-003
Severity: major
Location: BFA-R015, BFA-R016, BFA-R023; error and recovery behavior
Evidence: A corrective payload commit after `T` violates the post-transition restriction, while appending another activation transition cannot restore the unique-transition invariant. “Rebased or regenerated” does not define a legal recovery history.
Required outcome: Define how an invalid unpublished transition is abandoned without preserving it in the replacement candidate's first-parent history.
Safe resolution path: Create a replacement branch from the current authorized publication base, regenerate a single transition, rerun full validation and review, and supersede the invalid branch/PR without force-pushing or publishing its tag.
needs-decision rationale: none; replacement history is the only non-destructive path consistent with the unique transition requirement.

## Finding BFA-SR1-004

Finding ID: BFA-SR1-004
Severity: major
Location: Boundary model; boundary definitions; selected interactions
Evidence: Tagged-tree self-containment BFA-R014, changed-path rejection BFA-R016, and split strict validation BFA-R019 are not all governed by the relevant identity, composition, and temporal boundaries. The current record also lacks `P/B/T/H` and invalid-candidate replacement hazards.
Required outcome: Give every core release identity and recovery requirement semantic boundary and interaction ownership.
Safe resolution path: Add BFA-R014, BFA-R016, BFA-R019 and revised identity/replacement requirements to existing boundary definitions and selected interactions; update examples and acceptance mappings without adding Cartesian scenarios.
needs-decision rationale: none; this is formal contract completeness.

## Review Dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | block |
| normative language | concern |
| completeness | block |
| testability | block |
| examples | concern |
| compatibility | block |
| observability | concern |
| security/privacy | pass |
| non-goals | concern |
| acceptance criteria | block |

## Exact wording direction

- Introduce `P` as remote publication base and preserve `B` as `T`'s parent.
- Change the release target to stable minor `v0.4.0` with npm `0.4.0` and `latest`.
- Replace invalid candidate suffixes with a new branch from the authorized base;
  do not append a second transition or force-push.
- Expand boundary ownership only for the missing identity, self-containment,
  strict-composition, drift, and replacement hazards.

## Stop condition

The spec is not ready for architecture or eventual test-spec work until all
four findings are revised and a later spec-review approves the contract.
