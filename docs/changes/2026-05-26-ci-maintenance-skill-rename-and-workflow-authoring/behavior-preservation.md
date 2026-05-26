# Behavior Preservation: CI-Maintenance Skill Rename and Workflow Authoring

## Scope

This proof covers M1 and M2: canonical skill rename, packaged workflow resources, direct authored skill-identifier reference updates, and deterministic validator coverage for the renamed skill contract.

## Preservation Matrix

| Surface | Baseline | M1 result | Preservation result |
| --- | --- | --- | --- |
| Skill identity | `skills/ci/SKILL.md` used `name: ci` while the body described `ci-maintenance`. | Canonical source is `skills/ci-maintenance/SKILL.md` with `name: ci-maintenance`, `version`, and `schema-version`. | corrected |
| Workflow role | Existing skill authored and reviewed CI infrastructure and did not run validation. | Renamed skill keeps the CI infrastructure authoring/review role and preserves the no-run, no-test-design, no-readiness-claim boundary. | preserved |
| Handoff | Existing body mixed `ci-maintenance` with direct `ci` invocation wording. | Handoff wording consistently uses `ci-maintenance`, with workflow-managed handoff to `explain-change` and isolated direct invocation staying isolated. | strengthened |
| Packaged resources | No workflow skeleton asset or risk-to-check reference existed. | Added copy-and-fill GitHub Actions skeleton and read-only risk-to-check reference with portable/project-specific split. | strengthened |
| Command ownership | Existing skill said validation commands come from spec, test spec, and plan. | Renamed skill keeps that boundary and expands it to approved project sources, existing scripts/conventions, or explicit user commands. | strengthened |
| Public portability | Existing skill was short and project-neutral. | New public skill text uses project-local sources when present and labels RigorLoop-only risk-map rows as project-specific examples. | preserved |
| Repository workflow behavior | No `.github/workflows/*.yml` change was in scope. | M1 does not edit `.github/workflows/*.yml`. | unchanged |
| Validator coverage | Existing validator had generic skill checks and no `ci-maintenance`-specific resource/skeleton/risk-map checks. | M2 adds deterministic checks for renamed front matter, stale identifiers, resource-map verbs, skeleton defaults, risk-map split/fail-safe language, command blockers, and workflow-review guardrails. | strengthened |
| Generated adapters | Baseline generated adapter support still named `ci`. | M3 updates tracked adapter metadata to `ci-maintenance` and records temporary archive proof that all public adapters package `ci-maintenance` and its resources without an active `ci` body. | migrated |
| Migration guidance | No adopter-facing rename note existed. | M3 adds adapter README migration guidance telling adopters to update direct `ci` invocations to `ci-maintenance` and stating that no `ci` compatibility alias is installed in this release. | strengthened |

## Stale Reference Classification

The M1 stale-reference scan is expected to find intentional legacy references in `specs/ci-maintenance-skill.md` and `specs/ci-maintenance-skill.test.md` because those artifacts define the hard rename, negative fixtures, and migration behavior.

Other touched governance and test surfaces were updated when they asserted that `skills/ci/` remained the active entrypoint. Generic continuous-integration wording and `scripts/ci.sh` references remain unchanged.

## Workflow Diff Proof

M1 does not intentionally modify `.github/workflows/*.yml`. Final M1 validation must include either `git diff -- .github/workflows` with no output or an equivalent review-visible statement that no repository workflow files changed.

## M2 Validator Proof

M2 adds copied-fixture regression tests in `scripts/test-skill-validator.py`. Each test copies the canonical `skills/ci-maintenance/` directory into a temporary directory, mutates one required contract surface, and proves `scripts/validate-skills.py` fails with a stable error. This keeps the negative fixtures close to the canonical skill shape without duplicating a permanent fixture tree.

Covered M2 regression surfaces:

- missing `schema-version`;
- stale `role_name: ci`;
- wrong `READ`/`COPY` resource-map verb;
- missing skeleton `permissions: contents: read`;
- missing unmapped-surface fail-safe language;
- weakened command blocker and workflow-review guardrails.

## M3 Generated Adapter Proof

M3 records generated-output evidence in `generated-output-proof.md`.

The proof uses temporary generated output rather than hand-edited adapter package output. It validates `v0.1.5` adapter archives and inspects archive contents for:

- `ci-maintenance/SKILL.md`;
- `ci-maintenance/assets/github-workflow-skeleton.yml`;
- `ci-maintenance/references/risk-to-check-map.md`;
- absence of an active `/ci/` skill body.
