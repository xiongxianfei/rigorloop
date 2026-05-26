---
name: ci-maintenance
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Author or review CI infrastructure such as GitHub Actions workflows, validation automation, and related platform configuration. Use when CI workflow coverage is missing, stale, too slow, too broad, too narrow, or needs least-privilege, cache-aware, risk-scoped maintenance.
argument-hint: [feature name, workflow path, validation commands, or CI problem]
---

# CI maintenance

Design CI infrastructure that matches project risk without wasting compute.

This skill creates and updates CI infrastructure. It does not run validation, does not design tests, does not specify validation commands, and does not wait for existing CI checks. In this repository workflow, validation execution stays under `verify`.

## Workflow role

- role_name: ci-maintenance
- stage: support
- upstream: user request, approved specs, active test specs, plan validation commands, existing project CI conventions, package scripts, changed paths, and current workflow files
- downstream: explain-change in workflow-managed execution, or no automatic handoff for isolated direct invocation
- summary: Author or review hosted CI workflow files, validation automation, and related platform configuration.
- must_not_claim: validation execution, test design, CI pass status, verify readiness, branch readiness, PR readiness, release readiness, or deployment readiness.

## Resource map

- COPY `assets/github-workflow-skeleton.yml` when authoring a new GitHub Actions workflow or replacing a workflow structure. Fill placeholders from project-owned command sources and project policy; do not emit unfilled placeholders in final workflow output.
- READ `references/risk-to-check-map.md` when deriving CI checks from changed paths, reviewing risk coverage, deciding path filters, or separating PR checks from boundary checks. Adapt the map to the target project; do not treat project-specific examples as universal requirements.

## When to use

Use this skill when the user asks to:

- create or revise a GitHub Actions workflow;
- review workflow permissions, triggers, path filters, caching, or job structure;
- make PR checks faster without losing changed-risk coverage;
- split fast PR checks from scheduled, release, manual, or protected-boundary checks;
- harden workflow permissions or secret boundaries;
- add dependency caching when a stable invalidation key exists;
- audit whether CI covers changed paths and changed risk surfaces.

## When not to use

Do not use this skill merely to run local tests, design test coverage, interpret one CI failure log, wait for hosted checks, or claim branch/PR readiness. Use the project verification stage for validation execution and the test-planning stage for test design.

Do not use this first-slice skill to design deployment, secret-bearing release publishing, self-hosted runner policy, or organization-level Actions policy. Those need a separate approved design.

## Inputs to read

Read only the context needed for the requested CI maintenance:

- project-local instructions when present;
- relevant specs, test specs, plans, and validation-command sections;
- existing workflow files and CI configuration;
- package manifests, lockfiles, and package scripts;
- changed paths, generated-output conventions, and release/package metadata when relevant;
- explicit user-provided validation commands or CI constraints.

## Command ownership boundary

Wire known project validation commands into CI. Do not invent validation commands.

Allowed command sources are approved specs, approved or active test specs, plan validation sections, existing package scripts, existing project CI conventions, and explicit user-provided commands.

If no reliable command source exists, report a blocker instead of guessing. You may state that the project lacks a known validation command, but you must not define the missing test contract yourself.

## Operating procedure

1. Classify the request: author new workflow, revise workflow, review workflow, optimize speed, harden security, add caching, or audit coverage.
2. Identify the changed or requested project surface from the smallest relevant set of files.
3. Read the risk-to-check map and derive changed-risk classes from changed paths or requested scope.
4. Choose fast PR checks for changed risk.
5. Choose boundary checks for broad, slow, flaky, environmental, release, manual, scheduled, or protected-branch validation.
6. Apply GitHub Actions safety defaults.
7. Produce concise workflow or review output with risk coverage, blockers, and tradeoffs.

## GitHub Actions defaults

Use this design principle:

```text
Run fast changed-risk checks on every PR.
Run heavy comprehensive checks at scheduled, release, manual, or other boundary points.
```

Default to least privilege. Generic read-only CI starts with:

```yaml
permissions:
  contents: read
```

Add broader job-specific permissions only when a known workflow need requires them, and record the rationale. Do not add write permissions, token permissions, package permissions, pull request permissions, deployment permissions, or OIDC permissions unless the workflow purpose requires them and the rationale names the need.

Use path filters only when the risk map proves they will not skip required checks. Use concurrency to cancel redundant in-progress runs. Use dependency caches only when a stable invalidation key exists, normally a lockfile hash; otherwise omit caching or report that caching is intentionally not used.

Prefer full-length commit SHA pinning for third-party actions in high-security, release, or privileged workflows. If the project intentionally uses trusted version tags instead, record that as the project policy. Never invent a SHA.

Do not use `pull_request_target` for untrusted code unless the workflow is explicitly designed and reviewed for that security boundary. Avoid secrets in PR workflows from forks.

## Workflow review behavior

When reviewing workflows, flag:

- overbroad permissions without a named workflow need;
- path filters that skip required checks for mapped risk surfaces;
- slow comprehensive checks on every PR without justification;
- dependency caches without stable invalidation keys;
- invented or unsupported validation commands;
- `pull_request_target`, secrets, deployment, release publishing, or privileged permissions without a separate hardened design;
- missing risk coverage or unmapped changed surfaces.

Review findings should include evidence, required outcome, and a safe resolution path.

## Outputs

For workflow authoring, report:

- skill: `ci-maintenance`;
- status: created, updated, or blocked;
- workflow file path;
- PR checks and boundary checks;
- risk coverage;
- open blockers;
- workflow YAML or diff summary;
- tradeoffs and intentionally deferred checks.

For workflow review, report:

- skill: `ci-maintenance`;
- review status: approved, changes-requested, blocked, or inconclusive;
- material findings or none;
- risk coverage against changed surfaces;
- immediate next stage or blocker.

## Expected output

Use the output skeleton. Keep the result concise and concrete. Include workflow YAML only when authoring or materially revising a workflow. Include findings only when reviewing a workflow.

## Output skeleton

```md
Result

- Skill: ci-maintenance
- Status: created | updated | reviewed | blocked
- Workflow file: <path or not applicable>
- PR checks: <summary or not applicable>
- Boundary checks: <summary or not applicable>
- Risk coverage: <summary>
- Open blockers: <none or blockers>
- Next stage: explain-change | none | blocked

Workflow

<workflow YAML or diff summary when authored>

Findings

<workflow review findings, or none>

Tradeoffs

- <why this is fast enough>
- <why this covers the important changed risk>
- <what is intentionally deferred to schedule, release, manual, or another boundary>
```

## Handoff

When this skill is part of a workflow-managed standard workflow, successful CI maintenance hands off to `explain-change` unless a stop condition applies.

When `ci-maintenance` is run directly or for a narrower isolated purpose, report the CI infrastructure result without implying downstream continuation.

## Stop conditions

Stop and report a blocker when:

- validation commands would have to be invented;
- changed surfaces cannot be mapped enough to choose safe PR checks;
- path filters would skip required checks;
- the workflow needs deployment, release publishing, privileged permissions, secrets, self-hosted runners, or `pull_request_target` without a separate design;
- generated or packaged CI automation cannot be updated safely.

## Claims this skill must not make

Do not claim validation was run, tests were designed, hosted CI passed, verification passed, branch readiness, PR readiness, release readiness, deployment readiness, or final lifecycle completion.

## Evidence collection efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations when inspecting large files, repeated scans, generated output, or validation output. Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.
