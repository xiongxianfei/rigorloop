# M1 Preservation Inventories

## Result

- Milestone: M1
- Status: implementation-complete
- Canonical package changed: no
- Rules inventoried: 27
- Literals inventoried: 16
- Scenarios frozen: 33

The semantic ledger accounts for the complete current `SKILL.md`, both boundary references, all five assets, the governed transition cluster, proof policy, structure, stops, claims, and handoff. Similar text was not merged when it carried different lifecycle or proof meaning. The literal ledger separately classifies normative and parser/package strings, incidental headings, one historical lifecycle phrase, and their consumers.

MP0 passed by full-package reading plus targeted exact-string searches across `scripts/`, `specs/`, `skills/`, and tracked tests. Exact boundary resource hashes are frozen in `profile-size-baseline.md`; M2 must not change either boundary reference. Existing contributor guidance, schemas, workflow state, and other skills are unaffected because M1 records evidence only.

## Validation

- CMD1: passed; `rules=27 literals=16 scenarios=33 unknown_values=rejected-first`.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-13-test-spec-skill-simplification/change.yaml`: passed before implementation; workflow records the milestone transition separately.
- `git diff --check`: passed.

## Handoff

Ready for independent M1 `code-review`. This evidence does not claim package implementation, review approval, profile reduction, generated parity, or verification.
