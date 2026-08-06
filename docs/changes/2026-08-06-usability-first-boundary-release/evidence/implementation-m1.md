# M1 implementation evidence

Milestone: M1 — Automatic concise behavior and semantic journeys

Outcome: implemented and ready for code review.

## Implemented behavior

- Added semantic E1 specification, E2 loader-inspection, and E3 cleanup-review
  journeys that exercise automatic selection without naming the method.
- Added ordinary, wording-only, and no-admitted-boundary cases that select no
  irrelevant boundary output.
- Added paired contract-, risk-, and explicit-request journeys; each deeper case
  adds exactly one justified owned topic without expanding unrelated scope.
- Preserved formal artifact ownership: feature specification owns the normalized
  boundary record, test specification owns proof maps, and informal stages create
  no separate boundary artifact.
- Kept the existing shared compact scan and its ten canonical skill copies because
  they already express the approved automatic, concise, stage-owned behavior.

## Test-first evidence

`python scripts/test-skill-validator.py -k usability_journey` first failed with
three missing-fixture errors. After the semantic fixture was added, all three
focused tests passed. The closed fixture contract rejects unknown trigger,
artifact, and stage values and rejects presentation-metric fields such as exact
prose, word count, bullet count, or method-name requirements.

## Validation

- `python scripts/test-skill-validator.py` — pass, 285 tests, 16 skipped.
- `python scripts/test-boundary-first-reference.py` — pass, 28 tests.
- `python scripts/validate-skills.py` — pass, 24 skill files.
- `python scripts/build-skills.py --check` — pass.
- `python scripts/validate-boundary-first.py --check` — pass; pending snapshot.

## R1 review resolution

- `UBR-M1-CR1-001`: resolved by an independent contract-owned oracle for every
  stable journey. E1 and E2 now assert each named snapshot and malformed-input
  partition independently; coordinated required-topic removal, forbidden-topic
  admission, and stage/artifact reassignment all fail. Both `spec` boundary-record
  and `test-spec` proof-map ownership are exercised alongside informal no-artifact
  outcomes.
- `UBR-M1-CR1-002`: resolved by validating string types before closed-vocabulary
  membership or semantic evaluation. Array, object, and null mutations now return
  bounded validation errors rather than raising interpreter exceptions.
- The complete M1 validation command set passed again after both corrections.

No tag, publication, push, merge, registry write, or external state mutation was
performed.
