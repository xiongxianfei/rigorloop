## Result

Milestone: M3
Validation result: passed

## Core result

- Skill: implement
- Status: implemented
- Completed scope: Strengthened specification behavior ownership, made plan the v2 verification-allocation owner, added milestone and change-level verification-group structure, packaged eight conditionally loaded specialist methods, made Delivery Review one plan-centered implementation-and-verification readiness decision, and staged contract-keyed workflow and legacy test-spec guidance without activating v2.
- Artifacts changed: canonical `spec`, `plan`, `delivery-review`, `workflow`, and compatibility-only `test-spec` skill packages; spec and plan assets; eight plan references; skill contract tests; and this evidence.
- Tests added or updated: Added TS-007 through TS-011 and TS-016 contract coverage for behavioral ownership, engineering-led milestone structure, TG traceability, progressive disclosure, plan-centered Delivery Review, contract-keyed routing, and the compatibility-only test-spec package. Updated the earlier allocation-field assertion to the approved architecture-responsibility field.
- Validation performed: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py skills/spec/SKILL.md skills/plan/SKILL.md skills/delivery-review/SKILL.md skills/workflow/SKILL.md`; `python scripts/test-build-skills.py`; `python scripts/build-skills.py --check`; and `git diff --check`.
- Validation result: Skill tests passed 376 tests; explicit canonical validation passed all four named skills; build-skill tests passed 8 tests; temporary generated-skill parity passed; whitespace validation passed.
- Open blockers: none.
- Next stage: code-review.
- Claim limitations: V2 remains inactive under the preactivation manifest. Canonical inventory removal, repository-wide governance and validator parity, adapter publication, activation, rollback, and final evidence closure remain M4-M6 work.

## Planned milestone

- Change ID: `2026-08-31-retire-standalone-test-spec-stage`
- Plan identity: `docs/plans/2026-08-31-retire-standalone-test-spec-stage.md`, sha256 `727b5a71f1d5ce001876cde59f195536c9671b4743e50a70ef95cf437ccc9938`.
- Milestone ID: M3.
- Milestone state: implementation evidence complete; workflow handoff to `review-requested` is pending.
- Baseline or change-pack status: Delivery Review package `delivery-review-r3` remains current under this change's registered v1 contract; M3 changes canonical future-facing ownership guidance but does not alter the approved plan or activate v2.
- Milestone validation evidence: this file.
- Commit status: the implementation commit is supplied by Git history after this evidence is recorded.
- Code-review handoff: review published-skill semantics, specification-versus-plan authority, engineering-led sequencing, TG identity limits, specialist trigger proportionality, plan-centered reviewer independence, v1 compatibility, and absence of premature v2 activation.

## Test-first record

The initial M3 contract test failed across all six ownership groups because the canonical packages still described specification behavior generically, omitted the new milestone fields and change-level groups, lacked specialist references, reviewed plan plus test-spec, exposed only the v1 workflow route, and treated test-spec as a normal authoring package. After the scoped package changes, all focused M3 tests passed.

The first full skill suite then exposed two stale compatibility assertions: the earlier requirement-to-delivery test expected `Architecture decisions` instead of the approved `Architecture responsibility`, and the consolidated Delivery Review test still required a test-specification member. Updating those assertions to the approved v2 ownership model restored the full suite.

## Authored and aligned surfaces

- `spec` asks what must be demonstrably true and covers applicable normal, invalid, failure, state, authority, compatibility, migration, retry, concurrency, recovery, boundary, scenario, and acceptance behavior without prescribing implementation mechanics.
- `plan` keeps safe engineering sequence primary, requires purpose/allocation/scope/completion/verification/evidence fields, separates change-level verification, and limits TGs to plan-local trace identities.
- Eight plan references cover the approved specialist families and are loaded only by explicit risk triggers; ordinary planning does not load them all.
- `delivery-review` reads the complete primary plan and jointly judges sequence and verification, routes allocation gaps to plan and behavior gaps to spec, and rejects a standalone test-spec substitute under v2.
- `workflow` states both contract routes during preactivation and forbids selecting v2 for newly governed work before activation.
- `test-spec` remains present only as registered v1 and historical compatibility until its coherent M5 inventory removal.

## Unaffected surfaces and rationale

- Delivery Review result and finding assets remain generic and already carry package membership, traceability, findings, correction targets, recording, and settlement fields without encoding test-spec membership.
- Workflow guide assets, repository governance, schemas, validators, adapter inventories, and generated publication surfaces remain M4-M5 scope so this milestone does not publish a mixed active contract.
- Implementation, Code Review, Verify, and PR skills are unchanged because RTS-R16 and RTS-R24 preserve their downstream authority; their complete parity audit remains in M4 and final review.
- The shared boundary compact-scan template remains for the M4 repository-wide coherence update. The three M3 owning skills now state contract-keyed gap routing locally so their v2 responsibility is not ambiguous before that synchronized projection change.

## Recovery

Rollback is the M3 implementation commit as one unit: restore the prior five skill entrypoints, spec and plan assets, plan references, and matching tests together. Do not retain plan-centered Delivery Review with old plan/spec guidance or remove the compatibility-only test-spec package before M5 activation.
