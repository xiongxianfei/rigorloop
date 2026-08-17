# M2 learn package implementation evidence

## Scope

M2 aligned the approved learn artifact model with destination-owner mutation, split the canonical package into one universal skill and one session-method reference, and added focused static contract proof.

## Test-first evidence

`LearnSkillSimplificationTests` was added before the package reference existed. Its first run failed six cases with `FileNotFoundError` for `skills/learn/references/session-method.md`, proving that the new resource, operation, route, result, and profile contract was not already satisfied.

## Implemented contract

- `LR0-route-result` loads only `SKILL.md` and may update only one exact matching route in a learn-owned session record.
- `LR1-session` loads `SKILL.md` plus `references/session-method.md` exactly once.
- The public operations are exactly `run-learn-session` and `record-learn-route-result`; trigger assessment remains owned by the trigger source.
- Universal trigger, evidence, contributor-confirmation, sensitive-data, ownership, stop, claim, and resource-failure rules remain inline.
- New sessions use collision-safe paths, fail closed on partial records, and treat an exact complete rerun idempotently.
- Owner-bound routes use stable `ROUTE-NNN` IDs and closed settlement/completion vocabularies without polling or destination mutation.
- `specs/learn-artifact-model.md` and its test spec now require the destination owner to produce authoritative changes while `learn` records the route and exact owner-result identity.
- Historical sessions remain readable and are not migrated implicitly.

## Architecture boundary

The implementation adds no transaction-grade phase recovery, persistent route service, polling, external integration, new state owner, or cross-owner mutation authority. Existing Markdown session and topic surfaces remain the only learn-owned durable model, so the approved `architecture-not-required` result remains valid.

## Validation

Passed:

- `python scripts/validate-skills.py skills/learn/SKILL.md`
- `python scripts/test-skill-validator.py LearnSkillSimplificationTests`
- `python scripts/test-skill-validator.py`
- `python scripts/test-build-skills.py`
- `python scripts/build-skills.py --check`

The broader adapter-distribution command was also started for package parity; its final result is recorded in M3 distribution evidence rather than claimed here.

## Code-review correction

Code review R1 identified three semantic gaps that the initial phrase-level tests missed. The declared-safe correction now:

- selects route-result recording for an exact direct result request and stops missing-resource cases before session creation;
- requires the first session write to include identity, trigger, scope, basis, and complete Frame while preserving observation/evidence distinctions and fail-closed topic conflicts;
- records every required route field, fixes completion kind at creation, and validates the supplied owner-result kind against it.

Focused assertions were added before these corrections and failed all three affected test groups. They pass after correction.

## Result

M2 satisfies its focused completion criteria and is ready for independent code review. No destination lifecycle state, destination artifact, workflow routing state, or external system was mutated by the new learn operations.
