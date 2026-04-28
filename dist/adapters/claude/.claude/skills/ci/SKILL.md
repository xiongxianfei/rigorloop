---
name: ci
description: >
  Create, update, or review focused CI workflows for spec-driven repositories. Use when a feature needs automated verification, when CI does not cover the changed paths, or when PR readiness depends on fast and reliable validation.
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

## Workflow handoff behavior

- When `ci` is part of a workflow-managed full-feature flow and the governing workflow contract elevated it after `verify`, a successful `ci` stage hands off to `explain-change` unless a stop condition applies.
- When `ci` is run for a narrower or explicitly isolated purpose, report the CI result without implying downstream continuation that was not requested.
- If the needed CI automation cannot be created or updated safely, stop and report the blocker instead of claiming the workflow is ready to continue.

## Evidence collection efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations when inspecting large files, repeated scans, generated output, or validation output. Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

- workflow file path;
- workflow summary;
- triggers and path filters;
- commands run by CI;
- concurrency and caching notes;
- coverage against feature risk;
- gaps or manual checks that CI does not cover;
- readiness statement for `explain-change` or blocker state when `ci` is part of a workflow-managed full-feature flow.
