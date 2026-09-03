# M2 implementation evidence: Optional discovery routing and guidance

Milestone: M2
Subject path: docs/plans/2026-09-03-refine-explore-research-optional-discovery-skills.md
Subject identity: sha256:24f3acd041bdd46b56a5a45007f71ee38d9244d4ed07f48d2317718484d3c3fb
Validation result: passed

## Result

## Core result

- Skill: implement
- Status: implemented
- Completed scope: M2 Route selection for Explore, Research, both, or neither; explicit-versus-incidental behavior; owner adoption and contradiction handoff; current workflow, contributor, public, and project-map coherence
- Artifacts changed: `skills/route/SKILL.md`, `specs/rigorloop-workflow.md`, `AGENTS.md`, `README.md`, `docs/project-map.md`, and `scripts/test-skill-validator.py`
- Tests added or updated: three focused routing and current-surface coherence regressions in `OptionalDiscoverySkillContractTests`
- Validation performed: focused red/green test, full skill-validator suite, validation-selection suite, canonical skill validation, generated local-skill validation, boundary-first validation, current-language audit, and whitespace validation
- Validation result: all required M2 commands pass
- Open blockers: none
- Next stage: code-review
- Claim limitations: M2 evidence does not claim generated adapter parity, final verification, branch readiness, PR readiness, release readiness, or publication

## Planned milestone

- Change ID: 2026-09-03-refine-explore-research-optional-discovery-skills
- Plan identity: `docs/plans/2026-09-03-refine-explore-research-optional-discovery-skills.md`, `sha256:24f3acd041bdd46b56a5a45007f71ee38d9244d4ed07f48d2317718484d3c3fb`
- Milestone ID: M2
- Milestone state: implementation in progress; ready for review-requested transition
- Baseline or change-pack status: complete for current routing and explanatory surfaces; historical records and immutable releases excluded
- Milestone validation evidence: this file and the command results below
- Commit status: M2 handoff commit subject `M2: align optional discovery routing and guidance`
- Code-review handoff: review semantic selection, explicit invocation, incidental checks, owner authority, contradiction routing, current-versus-historical scope, and documentation coherence

## Test-first evidence

Before current guidance changed, the focused suite failed all new routing cases: Route did not distinguish Explore, Research, both, or neither; current surfaces omitted the standalone artifact roots and owner handoff; and Route did not state the incidental-work or lifecycle non-authority rules. After implementation, all ten focused discovery-contract tests pass.

## Validation results

- `python scripts/test-skill-validator.py -k OptionalDiscoverySkillContractTests` — passed, 10 tests after the expected failing baseline.
- `python scripts/test-skill-validator.py` — passed, 362 tests.
- `python scripts/test-select-validation.py` — passed, 154 tests in 70.44 seconds.
- `python scripts/validate-skills.py` — passed, 20 canonical skills.
- `python scripts/build-skills.py --check` — passed using temporary generated output.
- `python scripts/validate-boundary-first.py --check --path specs/refine-explore-research-optional-discovery-skills.md` — passed with the approved eight-dimension proof and rollback snapshot.
- `git diff --check` — passed.

## Routing and authority evidence

- Explore is selected when the material option space is unclear; Research is selected when a material decision depends on an uncertain fact.
- Both are selected in divergent-then-convergent order only when bounded research questions could materially change the option comparison; neither is selected when direction and decision-relevant facts are sufficiently clear.
- Route does not auto-run either skill. Explicit invocation or specific higher authority is required for a standalone discovery artifact, and an incidental local check creates no discovery artifact or completion claim.
- Proposal, Design, Delivery, Implementation, Verify, or another named owner may receive the handoff. Only that owner can adopt a conclusion that changes its decision; discovery cannot approve, edit the owner artifact, settle a package, or advance lifecycle state.
- Contradictions return to the stage that owns the affected decision, and stale, unavailable, unsafe, repeated, or out-of-scope support work stops or qualifies its result.

## Changed and unaffected surfaces

- Changed: the Route core selection rules, normative workflow categories and requirements, concise root guidance, public workflow overview, affected project-map paths and data-flow orientation, and focused coherence tests.
- Unaffected with rationale: lifecycle stage graphs, CLI transitions, change metadata, schemas, and stage settlement stay unchanged because discovery remains optional support without lifecycle authority.
- Unaffected with rationale: historical proposals, plans, reviews, change records, and immutable release archives preserve the contract in force when written and are not current routing authority.
- Unaffected with rationale: adapter metadata and generated/installed archive parity remain M3 scope after M2 current text is reviewed.
- Unaffected with rationale: existing examples, selection fixtures, and benchmark inventories contained no old Explore/Research distinction requiring semantic edits; the complete selection suite confirms affected-path routing remains valid.

## Current-language audit and recovery

A bounded search of `skills/`, `AGENTS.md`, `README.md`, `specs/rigorloop-workflow.md`, and `docs/project-map.md` found no remaining fixed five-option quota, inline explicit-Research completion, pre-Proposal-only restriction, proposal-only dependent list, or stale external-facts-only definition after the glossary correction. M2 can be rolled back as the Route, workflow, root-guidance, project-map, and regression-test slice without invalidating the internally coherent M1 packages.
