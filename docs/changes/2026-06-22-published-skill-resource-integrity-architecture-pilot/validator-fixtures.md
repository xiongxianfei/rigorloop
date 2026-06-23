# Validator Fixtures

## Status

active

## Scope

This note records the M2 canonical resource-integrity validator fixture coverage.
It is evidence for the architecture pilot; the generic rules live in
`specs/skill-contract.md`.

## Fixture Strategy

M2 uses temporary fixture skill trees in `scripts/test-skill-validator.py`
instead of committing many one-case fixture directories. The tests still invoke
the repository CLI validator against real `SKILL.md` files and real
skill-local resource files.

## Covered Cases

| Case | Proof |
| --- | --- |
| Valid mapped resources | `test_published_skill_resource_map_copy_read_run_classes_pass` covers `COPY assets/...`, `READ references/...`, and `RUN scripts/...` entries pointing to existing skill-local files. |
| Verb-to-class failures | `test_published_skill_resource_map_copy_must_point_to_assets`, `test_published_skill_resource_map_read_must_point_to_references`, and `test_published_skill_resource_map_run_must_point_to_scripts`. |
| Unsupported `templates/` class | `test_published_skill_resource_map_rejects_templates_class`. |
| Missing mapped resource | `test_published_skill_resource_map_rejects_missing_mapped_resource`. |
| Path containment | `test_published_skill_resource_map_rejects_path_traversal` and `test_published_skill_resource_map_rejects_absolute_path`. |
| Legacy unmapped reference | `test_published_skill_legacy_template_loading_instruction_fails` covers `assets/`, `references/`, `scripts/`, and legacy `templates/` resource-loading instructions with ordinary load-condition wording such as `when relevant`, `when available`, `when needed`, and `if present`. |
| False-positive boundary | `test_published_skill_legacy_lint_avoids_examples_and_docs_paths` covers explicit project-provided, repository-root, and user-provided ownership wording, illustrative examples, fenced examples, generated-artifact strings, and non-skill-local `docs/templates/...` paths. |
| Temporary architecture migration debt | `test_current_architecture_legacy_references_are_temporary_migration_debt` and `test_published_skill_architecture_migration_exception_is_exact`. |

The legacy-resource lint uses resource-lint-specific context rules. It does not
reuse the broader repository-root dependency allowlist, and ordinary
load-condition wording does not suppress unqualified skill-local resource
references.

## Temporary Exception

The current `skills/architecture/SKILL.md` legacy references to
`templates/architecture.md`, `templates/diagram-styles.mmd`, and
`templates/adr.md` are recorded as temporary migration debt from M1. The
validator allows exactly those architecture references until M3 normalizes the
architecture skill resource map and resources.

The exception does not add `templates/` as a supported resource class. A mapped
`templates/...` resource still fails verb-to-class validation.

The exception is skill-specific and path-specific: another skill using
`templates/architecture.md` fails, and the architecture skill using an
unapproved `templates/...` path fails.
