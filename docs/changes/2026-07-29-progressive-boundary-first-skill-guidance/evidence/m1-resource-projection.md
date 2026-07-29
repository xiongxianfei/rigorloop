# M1 resource projection evidence

## Scope

Milestone M1 replaces the one-reference projection with the reviewed three-resource manifest while keeping the compact-core compatibility path and activation state `pending`.

## Decisions

- `specs/boundary-first-resources.yaml` is the projection authority.
- The compact core retains `boundary-first-method-v1.md`; feature-authoring and proof guidance have owner-scoped canonical files and projections.
- The projection parser uses a dependency-free closed YAML subset, rejects unknown closed values before consistency checks, validates the complete matrix before writes, and hashes raw bytes.
- The activation record retains its compact-core compatibility fields and adds manifest identity; `projection_sha256` now covers all 14 expected targets.
- Published resource maps use `READ` with stage-specific load conditions. Only the feature-spec family maps feature authoring, and only the test-spec family maps proof guidance.

## Boundary and proof coverage

| Contract slice | Proof |
| --- | --- |
| BND-AUTH-001 / PRF-005 | Closed manifest, consumer vocabulary, exact skill resource sets, and mapped-resource tests |
| BND-COMPOSE-001 / PRF-008 | Canonical-to-skill raw-byte parity for 14 targets |
| BND-TEMPORAL-001 / PRF-011 | Repeated write identity and preflight-before-write tests |
| BND-RECOVERY-001 / PRF-012 | Missing source, unsafe path, stale, missing, and unexpected projection diagnostics |
| BND-ENV-001 / PRF-016 | Repository-relative POSIX containment and symlink rejection |

## Validation

| Command | Result |
| --- | --- |
| `python scripts/test-boundary-first-reference.py` | pass, 24 tests |
| `python scripts/project-boundary-first-reference.py --check` | pass, 14 projections |
| `python scripts/test-boundary-first-validation.py` | pass, 61 tests |
| `python scripts/validate-boundary-first.py --check` | pass |
| `python scripts/test-skill-validator.py` | pass, 272 tests with 16 documented skips |
| `python scripts/validate-skills.py` | pass, 24 skill files |

## Aligned-surface audit

The manifest, three canonical resources, 14 skill-local projections, ten resource maps, projection and activation validators, activation identities, and focused tests were updated together.
Generated adapter, archive, and clean-install parity remain M4 scope.

## Follow-up

M2 will add the automatic compact scan and stage-owned behavior guidance.

## R1 finding corrections

- `CR-M1-R1-001`: exact resource tuples and canonical resource versions now fail closed before projection.
- `CR-M1-R1-002`: the compact core owns the exact four-question scan; automatic stage invocation remains M2 scope.
- `CR-M1-R1-003`: handled write failures restore every prior target snapshot, with injected early, middle, and final failures followed by a successful retry.
- `CR-M1-R1-004`: activation validation preserves structured manifest error identity, path, expectation, and reason.

The full M1 command set passed after these corrections and is awaiting independent R2 review.

## R2 finding corrections

- `CR-M1-R2-001`: canonical and governed skill reference inventories now scan the complete recursive `boundary-first-*.md` namespace, rejecting alternate-version, arbitrary, nested, and symlink additions.
- `CR-M1-R2-002` and the remaining `CR-M1-R1-004` path: missing family sources and symlinks now carry structured identity through activation; the projection CLI prints bounded check, path, message, offending value, and expectation fields.

The full M1 command set passed after these corrections and is awaiting independent R3 review.

## R3 finding corrections

- `CR-M1-R3-001` and the reopened `CR-M1-R1-003`: the write transaction restores both pre-existing bytes and initially absent targets before propagating a catchable `KeyboardInterrupt`, then retries deterministically.
- `CR-M1-R3-002`: the projection module no longer restates the complete source, target, and consumer matrix. The manifest determines projection, while one approved raw manifest identity independently rejects contract drift after structural and closed-vocabulary checks.
- `CR-M1-R3-003` and the remaining diagnostic paths from `CR-M1-R1-004` and `CR-M1-R2-002`: a missing manifest now reports its exact repository-relative path and expected condition through both the public projection CLI and activation validation.

The full M1 command set passed after these corrections and is awaiting independent R4 review.
