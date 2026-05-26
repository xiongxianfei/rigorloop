# Behavior Preservation: CI-Maintenance Skill Rename and Workflow Authoring

## Scope

This proof covers M1: canonical skill rename, packaged workflow resources, and direct authored skill-identifier reference updates.

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
| Generated adapters | Baseline generated adapter support still names `ci`. | Generated adapter migration is intentionally deferred to M3, where adapter proof is planned. | pending by plan |

## Stale Reference Classification

The M1 stale-reference scan is expected to find intentional legacy references in `specs/ci-maintenance-skill.md` and `specs/ci-maintenance-skill.test.md` because those artifacts define the hard rename, negative fixtures, and migration behavior.

Other touched governance and test surfaces were updated when they asserted that `skills/ci/` remained the active entrypoint. Generic continuous-integration wording and `scripts/ci.sh` references remain unchanged.

## Workflow Diff Proof

M1 does not intentionally modify `.github/workflows/*.yml`. Final M1 validation must include either `git diff -- .github/workflows` with no output or an equivalent review-visible statement that no repository workflow files changed.
