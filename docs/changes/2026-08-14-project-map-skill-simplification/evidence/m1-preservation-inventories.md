# M1 Preservation Inventories

## Result

- Milestone: M1
- Status: implementation-complete
- Canonical package changed: no
- Rules inventoried: 24
- Literals inventoried: 15
- Scenarios frozen: 35

The semantic ledger accounts for universal orientation, evidence, freshness, commands, placement, reliance, stops, claims, conditional maintenance, coordination, area transactions, compatibility, and structural ownership. Similar passages remain separate when they carry different authority, freshness, or recovery behavior. The literal ledger separately classifies normative contracts, parser/package dependencies, historical compatibility, and the new result vocabulary.

The inventory was built from the complete current `skills/project-map/` package and targeted exact-string consumers under `scripts/`, `specs/`, and `skills/`. The canonical package remains unchanged in M1. Existing workflow state, schema, architecture, adapter roots, and other skills are unaffected because this milestone records proof only.

## Validation

- CMD1: passed with `rules=24 literals=15 scenarios=35 unknown_values=rejected-first`.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-14-project-map-skill-simplification/change.yaml`: passed before the implementation handoff.
- `git diff --check`: passed.

## Handoff

Ready for independent M1 `code-review`. This evidence does not claim canonical package implementation, review approval, profile reduction, generated parity, verification, or PR readiness.
