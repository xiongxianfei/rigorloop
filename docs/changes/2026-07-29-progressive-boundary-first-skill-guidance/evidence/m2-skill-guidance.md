# M2 automatic skill-guidance evidence

## Scope

Milestone M2 makes the four-question compact scan automatic in all ten governed skills while keeping formal authoring, proof ownership, and downstream consumption stage-scoped.

## Behavior

- The scan runs before a behavior-changing stage decision or whenever an active stable boundary identity is cited; it does not depend on the user naming the method.
- Non-behavior work continues under the ordinary stage contract without creating formal records, IDs, proof maps, artifacts, or scenario inventories.
- `spec` and `spec-review` own feature semantics. `test-spec` and `test-spec-review` own proof semantics. Downstream stages start from exact approved rows and route semantic or proof gaps upstream.
- Context expands only for missing, stale, unknown, ambiguous, conflicting, escaped, or insufficient identities or outcomes.
- Scenarios cover distinct outcomes and material hazards, then stop; no Cartesian inventory is required.
- Pending, active, grandfathered non-substantive, and undecidable substantive-revision states remain distinct.
- Structural validation cannot author, repair, or approve semantic content.

## Boundary and proof coverage

| Contract slice | Proof |
| --- | --- |
| BND-INPUT-001 / PRF-001 | Exact prompt-independent compact scan in all ten skills |
| BND-INPUT-002 / PRF-002 | Closed expansion conditions and owner routing |
| BND-AUTH-002 / PRF-006 | Feature, proof, downstream, and structural-validator authority boundaries |
| BND-COMPOSE-002 / PRF-009 | Exact-slice first reads plus material sibling-path coverage |
| BND-RECOVERY-001 / PRF-012 | Normative gaps route to `spec`; proof-only gaps route to `test-spec` |
| BND-COMPAT-001 / PRF-014 | Pending, active, grandfathered, and substantive-revision guidance |

## Red/green evidence

The exact shared-block test failed once for each of the ten governed skills before the skill prose changed. After the implementation, the three focused M2 tests passed.

## Validation

| Command | Result |
| --- | --- |
| `python scripts/test-skill-validator.py` | pass, 278 tests with 16 documented skips |
| `python scripts/validate-skills.py` | pass, 24 skill files |
| `python scripts/build-skills.py --check` | pass using temporary generated output |
| `python scripts/project-boundary-first-reference.py --check` | pass, 14 projections |
| `python scripts/validate-boundary-first.py --check` | pass |
| `git diff --check` | pass |

## Follow-up

M2 requires independent code review before M3 begins. Repository activation remains `pending`.

## R1 finding correction

- `CR-M2-R1-001`: the semantic fixture now covers all ten skills, every expansion identity, named and unnamed active behavior, pending and grandfathered states, sufficient slices, normative and proof gaps, material sibling and recovery paths, duplicate outcomes, ownerless discovery, and structural-pass semantic failure.
- A test-owned decision oracle derives action, route, explanation, consent, and scenario outcomes independently from fixture expectations.
- Required and forbidden phrases bind every scenario to its owning shipped skill.
- Negative mutations prove contradictory inputs, wrong actions or routes, missing expansion states, and missing skill coverage fail.

The complete M2 skill suite passed after the correction and is awaiting independent R2 review.
