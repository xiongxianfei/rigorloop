---
name: ci
description: >
  Create, update, or review focused CI workflows for spec-driven repositories. Use when a feature needs automated verification, when CI does not cover the changed paths, or when PR readiness depends on fast and reliable validation.
argument-hint: [feature name, workflow path, validation commands, or CI problem]
---

# CI workflow authoring and review

You are designing automated verification that matches the feature risk without wasting compute.

CI is part of verification. It should prove the right things at the right time.

## Inputs to read

Read:

- `AGENTS.md` and `CONSTITUTION.md` if present;
- feature spec and test spec;
- concrete plan validation commands;
- architecture doc when runtime or deployment boundaries matter;
- existing `.github/workflows/` files or other CI config;
- package/build/test config;
- changed paths and generated-code conventions.

## CI design goals

- Fast PR feedback.
- Scoped triggers.
- Reliable, deterministic jobs.
- Clear failure output.
- Appropriate caching that matches repo conventions.
- Heavy checks moved to scheduled, manual, or release workflows unless required for PR safety.
- Coverage for generated code, migrations, integration wiring, or platform-specific behavior when relevant.

## Workflow requirements

When creating or updating GitHub Actions, consider:

1. `name` that matches repo conventions.
2. `on.pull_request` for PR validation.
3. `on.push` for main branch validation when useful.
4. `paths` filters that include source, tests, configs, specs, and workflow files relevant to the feature.
5. `concurrency` for expensive workflows.
6. pinned or conventional action versions.
7. setup steps matching project toolchain.
8. cache keys based on lockfiles.
9. commands from the test spec and plan.
10. artifacts or logs for debugging when useful.
11. permissions minimized to what the workflow needs.

## Review checklist

Evaluate:

- Does CI cover all changed risk areas?
- Are path filters too narrow or too broad?
- Are required tests missing from PR validation?
- Are slow jobs appropriately separated?
- Are secrets avoided for untrusted PR contexts?
- Are caches correct and not stale-prone?
- Are generated files or migrations verified?
- Is failure output actionable?

## Rules

- Do not guess toolchain setup when repo conventions are available.
- Do not trigger workflows on unrelated files.
- Do not add slow, flaky jobs to every PR without justification.
- Do not claim caching improvements without checking repo support.
- Do not require secrets for pull requests from forks unless the repo intentionally supports that pattern.
- Do not treat CI as a substitute for local verification evidence.

## Expected output

- workflow file path;
- workflow summary;
- triggers and path filters;
- commands run by CI;
- concurrency and caching notes;
- coverage against feature risk;
- gaps or manual checks that CI does not cover.
