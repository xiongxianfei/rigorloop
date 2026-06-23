# Project-Map Validator Fixture Evidence

## Status

active

## Scope

This evidence belongs to M1, Project-Map Validator and Fixture Scaffolding.

M1 adds controlled validator coverage for the approved `project-map` contract
without enabling canonical enforcement against unchanged
`skills/project-map/SKILL.md` or requiring the M2 skeleton asset.

## Controlled fixture

- Valid fixture: `tests/fixtures/skills/project-map-contract/valid`
- Valid fixture asset: `tests/fixtures/skills/project-map-contract/valid/assets/project-map-skeleton.md`

The fixture proves structural recognition for:

- normalized frontmatter fields;
- workflow-role fields;
- `create`, `refresh`, `area`, and `audit` modes;
- map metadata fields;
- `observed`, `inferred`, and `unknown` evidence classes;
- material and incidental claim examples;
- root and area map registration table columns;
- required output headings;
- `COPY` resource-map entry for `assets/project-map-skeleton.md`;
- skeleton section coverage;
- skeleton policy boundary.

## Negative diagnostics

The M1 tests mutate temporary copies of the controlled valid fixture and assert
stable diagnostics for:

| Case | Expected diagnostic |
| --- | --- |
| Missing map baseline | `project-map contract missing map metadata field 'Baseline'` |
| Missing `audit` mode | `project-map contract missing operating mode 'audit'` |
| Non-`COPY` skeleton resource-map entry | `Resource map entry for 'assets/project-map-skeleton.md' must use literal COPY` |
| Hidden skeleton policy | `project-map skeleton must not own evidence-ranking or source-rank policy` |

## Canonical enforcement boundary

The helper `validate_project_map_contract_fixture` is called only by controlled
fixture tests in M1. It is not wired into canonical `validate_skill_file`
enforcement for `skills/project-map/SKILL.md`.

M2 owns updating the canonical `project-map` skill, adding the canonical
`assets/project-map-skeleton.md`, and enabling canonical enforcement together.

## Unaffected with rationale

- `skills/project-map/SKILL.md`: intentionally unchanged in M1 because M2 owns
  canonical content and enforcement atomically.
- `skills/project-map/assets/project-map-skeleton.md`: intentionally not added
  in M1 because M2 owns the canonical skeleton asset.
- Generated skill output and adapter packages: intentionally unchanged because
  generated/package parity belongs to later approved milestones.
