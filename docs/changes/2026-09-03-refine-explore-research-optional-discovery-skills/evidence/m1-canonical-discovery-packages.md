# M1 implementation evidence: Canonical optional discovery packages

Milestone: M1
Subject path: docs/plans/2026-09-03-refine-explore-research-optional-discovery-skills.md
Subject identity: sha256:24f3acd041bdd46b56a5a45007f71ee38d9244d4ed07f48d2317718484d3c3fb
Validation result: passed

## Result

## Core result

- Skill: implement
- Status: implemented
- Completed scope: M1 canonical shared discovery policy, self-contained Explore and Research packages, standalone artifact assets, conditional methods, skill-contract admission, and fail-closed validator coverage
- Artifacts changed: `templates/shared/discovery-support.md`, `skills/explore/`, `skills/research/`, `specs/skill-contract.md`, `scripts/skill_validation.py`, and `scripts/test-skill-validator.py`
- Tests added or updated: six focused `OptionalDiscoverySkillContractTests`, including shared-copy drift and unknown-consumer failure cases
- Validation performed: focused test-first failure, focused passing suite, full skill-validator suite, canonical validation, generated local-skill validation, and whitespace validation
- Validation result: all required M1 commands pass
- Open blockers: none
- Next stage: code-review
- Claim limitations: implementation evidence does not claim a clean review, milestone closeout, final verification, branch readiness, PR readiness, release readiness, or published adapter currency

## Planned milestone

- Change ID: 2026-09-03-refine-explore-research-optional-discovery-skills
- Plan identity: `docs/plans/2026-09-03-refine-explore-research-optional-discovery-skills.md`, `sha256:24f3acd041bdd46b56a5a45007f71ee38d9244d4ed07f48d2317718484d3c3fb`
- Milestone ID: M1
- Milestone state: implementation in progress; ready for review-requested transition
- Baseline or change-pack status: complete for the M1 package, validation, evidence, rollback unit, and review scope
- Milestone validation evidence: this file and the command results below
- Commit status: M1 handoff commit subject `M1: refine canonical explore and research packages`
- Code-review handoff: review the exact M1 diff for public semantic distinction, resource integrity, progressive disclosure, authority exclusions, negative coverage, and absence of maintainer-only text

## Test-first evidence

Before production changes, `python scripts/test-skill-validator.py -k OptionalDiscoverySkillContractTests` failed six tests because the old fixed-quota and inline-output contracts remained, the new resources and skill-contract admission were absent, and the closed shared-copy validator did not exist. After implementation, the same six tests passed.

## Validation results

- `python scripts/test-skill-validator.py -k OptionalDiscoverySkillContractTests` — passed, 6 tests.
- `python scripts/test-skill-validator.py` — passed initially with 358 tests and after the review correction with 359 tests.
- `python scripts/validate-skills.py` — passed, 20 canonical skills.
- `python scripts/build-skills.py --check` — passed using temporary generated output.
- `git diff --check` — passed.

After Code Review R1 recorded ER-M1-CR1, a new package-wide public-text hygiene test failed on the canonical `skills/explore/SKILL.md` and `skills/research/SKILL.md` path comments embedded in the two artifact assets. The comments were removed, the focused seven-test discovery suite passed, and the complete skill-validator suite passed with 359 tests. Canonical validation, generated local-skill validation, review structure validation, and whitespace validation also passed after the correction.

## Changed and unaffected surfaces

- Changed: both public core contracts, their new structural assets and conditional references, the shared-block contract, its copied resources, skill-contract admission, validator integration, and focused tests.
- Unaffected with rationale: Route and workflow/public documentation remain unchanged until M2 so routing changes consume two already coherent canonical packages.
- Unaffected with rationale: adapter support metadata, generators, archives, and installed candidates remain M3 scope; M1 only proves the existing local generator can carry the new resources.
- Unaffected with rationale: lifecycle stages, CLI operations, schemas, proposal/design authority, and historical artifacts do not change under the approved non-goals.

## Boundary and recovery evidence

The packages explicitly cover absent defaults, exact selected revisions, collisions, ambiguous and escaped paths, missing resources, evidence unavailability, contradiction, scope expansion, owner judgment, and sensitive-data exclusion. `validate_discovery_support_copy` rejects unknown consumers before consistency and rejects missing or drifted canonical/local resources. Package rollback is one coherent unit comprising the shared admission, both complete packages, validation, and tests.
