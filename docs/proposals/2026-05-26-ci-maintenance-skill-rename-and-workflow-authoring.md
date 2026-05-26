# Proposal: Rename `ci` to `ci-maintenance` and Add Risk-Scoped GitHub Workflow Authoring Support

## Status

accepted

## Problem

The current CI skill has two related problems.

First, the skill has a naming inconsistency. The skill body already describes the role as `ci-maintenance`, while the skill front matter still uses `name: ci`. That leaves one workflow role with two names across skill text, handoffs, workflow chains, selectors, adapters, docs, and tests.

Second, the skill has an output quality gap. It already favors fast, scoped, reliable CI, but it does not give the agent enough reusable structure to consistently author concise, efficient, risk-covering GitHub Actions workflows. The missing support is a concrete workflow skeleton, a changed-surface-to-check mapping, an explicit command ownership boundary, and an explicit principle that fast PR checks and comprehensive boundary checks serve different purposes.

These should be handled together only as two separate workstreams under one coherent `ci-maintenance` skill contract: an identifier migration and a skill capability enhancement.

## Goals

- Rename the published skill from `ci` to `ci-maintenance`.
- Update identifier references atomically so the skill has one canonical name.
- Preserve or explicitly migrate existing installed-skill references to `ci`.
- Clarify that the skill authors and reviews CI maintenance changes, rather than merely running CI.
- Improve GitHub Actions workflow authoring so generated workflows are concise, fast on PRs, robust against common CI risk, least-privilege by default, deterministic, cache-aware where safe, and explicit about PR, scheduled, release, and manual triggers.
- Add a reusable GitHub Actions workflow skeleton asset.
- Add a risk-to-check coverage map so CI checks are derived from changed surfaces.
- Keep public skill text portable and avoid requiring RigorLoop repository-internal docs unless running inside this repository.
- Add validation that catches stale `ci` references and verifies generated adapters include the renamed skill and resources.
- Prevent `ci-maintenance` from inventing validation commands while authoring workflow YAML.

## Non-goals

- Do not change repository CI behavior directly in this proposal.
- Do not add or modify a specific `.github/workflows/*.yml` workflow as part of this proposal.
- Do not rename unrelated CI scripts, shell commands, or GitHub workflow files unless they are skill references.
- Do not make CI slower by putting every heavy check on every PR.
- Do not claim generated workflows are secure without review.
- Do not require self-hosted runners.
- Do not introduce deployment, release publishing, or secret-bearing workflows in the first slice.
- Do not hide expensive checks behind vague robustness language.
- Do not move skill routing logic into assets.
- Do not use assets as hidden policy files; `SKILL.md` remains the operating contract.

## Vision fit

fits the current vision

RigorLoop’s skills should be self-contained operating documentation for smart agents. A CI-maintenance skill should teach not just how to write a workflow, but how to choose the right checks, structure them safely, and keep common PR validation fast. This supports the project vision of traceable, reviewable, and trustworthy AI-assisted work.

This proposal is falsified if the renamed skill leaves stale `ci` references in workflow stage names, installed adapters expose both `ci` and `ci-maintenance` ambiguously, the workflow skeleton encourages overbroad permissions or slow PR checks, the skill produces workflows without mapping changed risks to checks, CI guidance becomes longer but not more deterministic, or generated adapter output is hand-edited instead of rebuilt from canonical skills.

## Context

The rename is justified because the skill body already calls the role `ci-maintenance`, while the front-matter name remains `ci`. Skill names are identifiers referenced by workflow chains, selectors, adapters, docs, and handoff rules, so this should be treated as an identifier migration rather than a wording cleanup.

The current skill already expresses useful CI goals: fast PR feedback, scoped triggers, deterministic jobs, clear failure output, and moving heavy checks to scheduled or release contexts. The gap is that the skill states principles without a concrete workflow skeleton and a risk-to-coverage mapping.

GitHub’s Actions documentation supports several relevant workflow defaults. GitHub recommends limiting `GITHUB_TOKEN` permissions because actions can access that token through the `github.token` context, and the workflow `permissions` key can set minimum required permissions. GitHub’s secure-use guidance recommends pinning third-party actions to full-length commit SHAs when practical. GitHub Actions also supports workflow and job `concurrency`, and GitHub’s cache guidance describes cache keys based on files such as dependency lockfiles.

Sources:

- GitHub Docs, [Authenticate with GITHUB_TOKEN](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)
- GitHub Docs, [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- GitHub Docs, [Control workflow concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency)
- GitHub Docs, [Dependency caching reference](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Rename `ci` to `ci-maintenance` | in scope | Goals, Recommended Direction |
| Fix existing mixed naming | in scope | Problem, Workstream A |
| Make the skill produce concise workflows | in scope | Workstream B, Expected Behavior Changes |
| Make workflows efficient and time-saving | in scope | Core design principle, Acceptance Criteria |
| Make workflows robust against most risk | in scope | Risk-to-check map, Testing and Verification Strategy |
| Avoid overcomplicating CI | in scope | Non-goals, Scope budget |
| Keep skill portable | in scope | Goals, Public skill boundary |
| Avoid hidden repo-internal mechanisms | in scope | Non-goals, Resource layout |
| Avoid invented validation commands | in scope | Command ownership boundary |

## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| Rename skill directory/front matter from `ci` to `ci-maintenance` | core to this proposal | The skill already uses `ci-maintenance` internally. |
| Update references to the skill identifier | core to this proposal | Skill name is an identifier, not just prose. |
| Add compatibility handling for old `ci` references | core to this proposal | Avoid silent breakage while preventing duplicate routing ambiguity. |
| Add `assets/github-workflow-skeleton.yml` | core to this proposal | GitHub Actions YAML is substantial, indentation-sensitive, and security-sensitive enough to earn an asset. |
| Add `references/risk-to-check-map.md` | core to this proposal | Robust CI depends on deriving checks from changed surfaces. |
| Add concise output expectations | core to this proposal | The skill should output reviewable workflow diffs and rationale instead of generic advice. |
| Add GitHub Actions security defaults | core to this proposal | CI workflows are security-sensitive. |
| Add command ownership boundary | core to this proposal | Workflow authoring may wire known commands into CI but should not invent validation commands. |
| Add generated adapter validation | same-slice dependency | The renamed skill should ship correctly. |
| Add actual workflow implementation for this repo | out of scope | This proposal changes the skill, not project CI behavior. |
| Add deployment or release workflow templates | separate proposal | Secret-bearing and release-publishing workflows carry a higher risk boundary. |
| Add language-specific workflow skeletons for many ecosystems | deferable follow-up | First slice should prove one generic skeleton plus the risk map. |

## Options Considered

### Option 1: Rename only

Pros:

- Low risk.
- Fixes the existing naming inconsistency.

Cons:

- Does not improve the skill’s workflow output quality.
- Leaves the skill stating principles without concrete reusable structure.

### Option 2: Add CI workflow guidance only, keep `ci`

Pros:

- Avoids identifier migration.

Cons:

- Leaves the existing two-name inconsistency.
- Keeps a less descriptive public skill identifier.

### Option 3: Rename and add a workflow skeleton asset only

Pros:

- Fixes the identifier.
- Adds a concrete starting workflow.

Cons:

- Skeleton alone cannot decide what checks are required for changed surfaces.
- The model may still produce fast but under-covering CI.

### Option 4: Rename plus skeleton asset plus risk-to-check map

Pros:

- Fixes the identifier and the workflow quality gap.
- Makes good workflow shape the default.
- Makes risk coverage derivable from changed surfaces.
- Keeps broad checks off every PR by design.

Cons:

- Touches skill identity, resources, validators, generated adapters, and docs.
- Requires careful migration and validation.

## Recommended Direction

Choose Option 4: rename the skill to `ci-maintenance`, add a reusable GitHub Actions skeleton asset, and add a risk-to-check reference map.

Use this core design principle in the skill body:

```text
Run fast, changed-risk checks on every PR.
Run heavy comprehensive checks at the boundary: scheduled, release, or manual.
```

This reconciles efficiency and risk coverage. Robust CI should cover the risk introduced by changed paths now, while full-project checks run regularly or before release. It should not mean running every heavy check on every PR.

## Expected Behavior Changes

### Workstream A: Rename `ci` to `ci-maintenance`

The canonical skill identity changes from:

```yaml
name: ci
```

to:

```yaml
name: ci-maintenance
```

The implementation should not use the misspelling `ci-mantance`.

Identifier references should be updated where they mean the skill, including:

```text
skills/ci/ -> skills/ci-maintenance/
front matter name
workflow stage chain references
handoff references
docs/workflows.md entries
skill index or generated adapter metadata
validator allowlists or route tables
generated adapter package paths
tests and fixtures that name the skill
```

Generic prose where “CI” means continuous integration generally should stay unchanged.

## Compatibility alias decision

The first slice should use this compatibility behavior:

```text
Canonical installed skill: ci-maintenance.

Do not install both ci/ and ci-maintenance/ as active skills.

If safe alias support exists, map ci -> ci-maintenance for one compatibility
window and document the deprecation. If safe alias support does not exist, use a
hard rename with release-note migration guidance.
```

Legacy `ci` support is allowed only as a non-duplicating alias if the adapter, skill registry, or invocation layer already supports aliases safely and tests prove no duplicate routing ambiguity. If no safe alias mechanism exists, use a hard rename with release-note migration guidance:

```md
The CI workflow authoring/review skill has been renamed from `ci` to
`ci-maintenance` to match its workflow role. Use `ci-maintenance` when invoking
the skill directly. Existing `ci` references should be updated.
```

Do not leave both installed skill directories active. Two installed skills with overlapping descriptions can cause routing ambiguity.

### Workstream B: CI workflow authoring capability

## Command ownership boundary

`ci-maintenance` may wire known project validation commands into CI, but it should not invent validation commands.

Allowed command sources:

- approved specs;
- approved or active test specs;
- plan validation sections;
- existing package scripts;
- existing project CI conventions;
- explicit user-provided commands.

If no reliable command source exists, the skill should report a blocker instead of guessing. `ci-maintenance` authors or reviews CI infrastructure. It does not execute validation, design tests, or claim CI, verify, branch, or PR readiness.

The skill should use this resource layout:

```text
skills/ci-maintenance/
  SKILL.md
  assets/
    github-workflow-skeleton.yml
  references/
    risk-to-check-map.md
```

`assets/github-workflow-skeleton.yml` should be a copy-and-fill structure, not hidden policy prose. It should include least-privilege permissions, PR and boundary triggers, concurrency, job timeouts, deterministic install placeholders, scoped PR checks, cache placeholders where safe, and comprehensive boundary checks.

The skeleton should start from this structure:

```yaml
name: CI

on:
  pull_request:
    paths:
      - "<scoped paths>"
  push:
    branches: ["main"]
  workflow_dispatch:
  schedule:
    - cron: "<boundary schedule>"

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  changed-risk:
    name: Changed-risk checks
    runs-on: ubuntu-latest
    timeout-minutes: <timeout>
    steps:
      - name: Checkout
        uses: actions/checkout@<full-length-sha-or-policy-approved-ref>

      - name: Setup runtime
        uses: <setup-action>@<full-length-sha-or-policy-approved-ref>
        with:
          <runtime inputs>

      - name: Restore dependency cache
        uses: actions/cache@<full-length-sha-or-policy-approved-ref>
        with:
          path: <dependency cache path>
          key: ${{ runner.os }}-<runtime>-${{ hashFiles('<lockfile path>') }}

      - name: Install dependencies
        run: <deterministic install command>

      - name: Run scoped checks
        run: <scoped validation command>

  boundary:
    name: Boundary checks
    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    timeout-minutes: <timeout>
    steps:
      - name: Checkout
        uses: actions/checkout@<full-length-sha-or-policy-approved-ref>

      - name: Run comprehensive checks
        run: <comprehensive validation command>
```

The generic skeleton includes PR, push, schedule, and manual dispatch. Release triggers are optional and should be added only when the workflow owns release validation or packaging. Release and deployment workflows remain out of the first slice.

The skeleton should not invent real action SHAs. It should require an explicit action-reference policy and default placeholders toward pinned references. Prefer full-length commit SHA pinning for third-party actions in high-security, release, or privileged workflows. If the project intentionally uses trusted version tags instead, record that as the project policy. Never invent a SHA.

Use dependency caches only when there is a stable invalidation key, usually a lockfile hash. Otherwise omit caching.

Do not use `pull_request_target` for untrusted code unless the workflow is explicitly designed and reviewed for that security boundary.

## Risk-map portability boundary

`references/risk-to-check-map.md` should be decision guidance, not a copy-and-fill asset. It should split portable core guidance from project-specific extension rows. RigorLoop-specific surfaces such as skills, generated adapters, release metadata, and repository validators are examples, not universal public-skill requirements.

The risk-to-check reference should start from this map:

### Portable core

| Changed surface | PR check | Boundary check |
|---|---|---|
| workflow files | syntax/lint/security/path-filter review | full workflow validation or scheduled run |
| dependency lockfiles | install and test with lockfile-keyed cache | full dependency audit or scheduled validation |
| source code | affected unit/component tests | full suite |
| tests | changed tests and affected source checks | full suite |
| generated files | generated-output drift check if configured | full generated validation |
| docs | link or structure checks if configured | full docs validation |

### Project-specific extensions

Use these only when the project has the corresponding surface:

| Surface | Example check |
|---|---|
| RigorLoop skills | skill validation |
| RigorLoop generated adapters | generated adapter validation |
| release metadata | package/release validation |
| repository validators | validator unit tests and lifecycle validation |

## Architecture Impact

| Surface | Impact |
|---|---|
| `skills/ci/` | Rename to `skills/ci-maintenance/`. |
| Skill front matter | Change to `name: ci-maintenance`. |
| Skill body | Consolidate self-reference and handoff text. |
| `assets/github-workflow-skeleton.yml` | New copy-and-fill workflow template. |
| `references/risk-to-check-map.md` | New optional risk-coverage guidance. |
| Skill validator | Add checks for stale `ci` identifier references and resource-map entries. |
| Generated adapters | Include renamed skill and new resources. |
| `docs/workflows.md` | Update stage or skill name if it references `ci`. |
| Release notes | Add adopter-visible rename note. |
| Existing CI workflows | No direct change. |

Because this touches public skill identity, validation behavior, generated adapter output, and contributor-facing workflow text, later lifecycle stages should treat it as compatibility-sensitive.

## Testing and Verification Strategy

Suggested checks:

| Check ID | What is verified |
|---|---|
| `CIM-001` | Canonical skill directory/name is `ci-maintenance`. |
| `CIM-002` | No skill self-reference still says `ci` when it means the skill identifier. |
| `CIM-003` | Generated adapters include `ci-maintenance` and do not expose stale `ci` unless an alias is approved. |
| `CIM-004` | `assets/github-workflow-skeleton.yml` is mapped with `COPY` from `SKILL.md`. |
| `CIM-005` | `references/risk-to-check-map.md` is mapped with `READ` from `SKILL.md`. |
| `CIM-006` | Skeleton includes least-privilege permissions, concurrency, scoped PR checks, boundary checks, cache placeholders, and timeout placeholders. |
| `CIM-007` | Risk-to-check map covers workflow, dependency, source, test, generated-output, skill, package/release, validator/script, and docs surfaces. |
| `CIM-008` | Workflow review fixture flags overbroad permissions. |
| `CIM-009` | Workflow review fixture flags a path filter that skips required checks. |
| `CIM-010` | Workflow review fixture flags slow comprehensive checks on every PR when not justified. |
| `CIM-011` | Workflow authoring fixture produces concise YAML and a risk-coverage table. |
| `CIM-012` | No repository workflow behavior changes occur in this slice. |
| `CIM-013` | No generated adapter contains both an active `ci` skill and an active `ci-maintenance` skill unless a formal alias contract prevents duplicate routing. |
| `CIM-014` | If `ci` aliasing is supported, tests prove `ci` resolves to `ci-maintenance` without installing duplicate skill bodies. |
| `CIM-015` | If aliasing is not supported, release notes document the hard rename and migration path. |
| `CIM-016` | The skill states that validation commands come from approved project sources or explicit user input. |
| `CIM-017` | A workflow-authoring fixture with missing validation commands returns a blocker instead of inventing commands. |
| `CIM-018` | Skeleton placeholders do not weaken the boundary that `ci-maintenance` does not run validation or design tests. |
| `CIM-019` | `risk-to-check-map.md` separates portable core guidance from project-specific extensions. |
| `CIM-020` | RigorLoop-specific rows are labeled as project-specific examples, not universal public-skill requirements. |
| `CIM-021` | The public skill can be used in a non-RigorLoop repository without requiring RigorLoop-specific files or validators. |

Candidate validation commands:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py skills/ci-maintenance/SKILL.md
python scripts/validate-skills.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version <version> --check
python scripts/validate-adapters.py --version <version>
git grep -n "name: ci\\|role_name: ci\\|\\bci hands off\\|when `ci` is run" skills docs specs scripts || true
git diff --check --
```

Use the repository’s actual generated-adapter commands if they differ.

## Rollout and Rollback

Rollout:

1. Approve the proposal.
2. Write or amend the spec for the `ci-maintenance` skill identity and resource contract.
3. Write test-spec coverage for rename, resource packaging, workflow skeleton, and risk-map behavior.
4. Rename the canonical skill directory and front matter.
5. Update identifier references atomically.
6. Add the workflow skeleton asset and risk-to-check reference.
7. Add validator coverage and fixtures.
8. Rebuild or validate generated adapters.
9. Record behavior-preservation evidence.
10. Add release-note migration guidance.

Rollback:

- Restore the `ci` skill name only if adapter generation or routing breaks and cannot be resolved.
- Keep the risk-to-check map as follow-up only if the rename must be isolated.
- Do not leave both `ci` and `ci-maintenance` active unless alias behavior is explicitly approved.
- Do not revert unrelated CI workflows because none should change in this slice.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Skill rename breaks direct invocation | Add alias support if safe, or release-note migration guidance if not. |
| Generated adapters expose both names | Validate generated output and reject ambiguity. |
| Skeleton becomes hidden policy | Keep policy in `SKILL.md` and the reference map; keep the asset structural. |
| Workflow is too generic | Require the risk-to-check map and project adaptation step. |
| Workflow is too slow | Explicitly split PR checks from boundary checks. |
| Workflow is too narrow | Derive path filters from the risk map and retain boundary checks. |
| Security defaults become stale | Base guidance on GitHub-documented principles and keep security guidance concise. |
| Cache keys become unsafe | Require lockfile-keyed cache or no cache. |
| Public skill becomes RigorLoop-internal | Keep repo-specific details out of public default guidance. |

## Open Questions

None blocking for proposal-review.

The first proposal-review pass resolved the main decision questions:

- Do not install both `ci` and `ci-maintenance` as active skills.
- Allow `ci` only as a non-duplicating compatibility alias if the adapter, registry, or invocation layer supports aliases safely and tests prove no duplicate routing ambiguity.
- Use `references/risk-to-check-map.md` as a `READ` reference, not a copy-and-fill asset.
- Use action-reference placeholders that require a full-length SHA or a policy-approved reference; never invent SHAs.
- Keep language-specific skeletons out of the first slice.
- Keep actual RigorLoop `.github/workflows/*.yml` changes out of this proposal.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-26 | Rename `ci` to `ci-maintenance`. | The skill already uses that role name internally and it is more precise. | Keep mixed `ci` / `ci-maintenance`. |
| 2026-05-26 | Treat rename as identifier migration. | Skill names are referenced by generated adapters, docs, handoffs, and tests. | Pure wording change. |
| 2026-05-26 | Add workflow skeleton asset. | Workflow YAML is substantial, error-prone structure that earns an asset. | Principles-only guidance. |
| 2026-05-26 | Add risk-to-check reference. | Robustness should be derived from changed risk surfaces. | Generic CI checklist only. |
| 2026-05-26 | Keep actual workflows out of scope. | Skill improvement should not be bundled with CI behavior changes. | Update `.github/workflows` in the same slice. |
| 2026-05-26 | Do not install duplicate active `ci` and `ci-maintenance` skill directories. | Duplicate installed skill bodies can create routing ambiguity. | Keep both names as active installed skills. |
| 2026-05-26 | Require known command sources for workflow commands. | CI authoring should wire project-owned validation commands, not invent tests or verification. | Let the workflow skeleton imply commands. |
| 2026-05-26 | Split the risk map into portable core and project-specific extensions. | Public skill guidance should work outside RigorLoop repositories. | Present RigorLoop-specific rows as universal requirements. |

## Acceptance Criteria

| ID | Criterion |
|---|---|
| `AC-CIM-001` | Canonical skill name is `ci-maintenance`. |
| `AC-CIM-002` | No canonical skill body uses `ci` as the skill identifier after rename. |
| `AC-CIM-003` | All workflow-stage and handoff references use `ci-maintenance`. |
| `AC-CIM-004` | Adapter generation includes `ci-maintenance` and its resources. |
| `AC-CIM-005` | If `ci` compatibility is retained, it is documented as an alias and does not create duplicate routing ambiguity. |
| `AC-CIM-006` | `SKILL.md` maps `assets/github-workflow-skeleton.yml` with `COPY`. |
| `AC-CIM-007` | `SKILL.md` maps `references/risk-to-check-map.md` with `READ`. |
| `AC-CIM-008` | The skeleton includes least-privilege permissions, concurrency, PR trigger structure, boundary-check structure, cache placeholders, and timeout placeholders. |
| `AC-CIM-009` | The risk map derives checks from changed surfaces. |
| `AC-CIM-010` | The skill distinguishes PR checks from schedule/release/manual boundary checks. |
| `AC-CIM-011` | Workflow-review fixtures catch overbroad permissions, unsafe path filters, and unjustified slow PR checks. |
| `AC-CIM-012` | No actual repository workflow behavior changes in this slice. |
| `AC-CIM-013` | No generated adapter contains both an active `ci` skill and an active `ci-maintenance` skill unless a formal alias contract prevents duplicate routing. |
| `AC-CIM-014` | If `ci` aliasing is supported, tests prove `ci` resolves to `ci-maintenance` without installing duplicate skill bodies. |
| `AC-CIM-015` | If aliasing is not supported, release notes document the hard rename and migration path. |
| `AC-CIM-016` | The skill states that validation commands must come from approved project sources or explicit user input. |
| `AC-CIM-017` | A workflow-authoring fixture with missing validation commands returns a blocker instead of inventing commands. |
| `AC-CIM-018` | The skeleton placeholders do not weaken the existing boundary that `ci-maintenance` does not run validation or design tests. |
| `AC-CIM-019` | `risk-to-check-map.md` separates portable core guidance from project-specific extensions. |
| `AC-CIM-020` | RigorLoop-specific rows are labeled as project-specific examples, not universal public-skill requirements. |
| `AC-CIM-021` | The public skill can be used in a non-RigorLoop repository without requiring RigorLoop-specific files or validators. |

## Next Artifacts

Planned next artifacts:

```text
proposal-review
spec: ci-maintenance skill rename and workflow skeleton contract
spec-review
test-spec
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

If existing skill-contract rules already cover skill renames and resource packaging, a focused test-spec amendment may be enough. If not, write a focused spec amendment before implementation.

Potential future proposals:

- Language-specific CI workflow skeletons.
- Actual RigorLoop `.github/workflows/` optimization using `ci-maintenance`.
- GitHub Actions security scanner integration.
- Release/deploy workflow templates.
- Generated CI workflow linting or validation.

## Follow-on Artifacts

None yet

## Readiness

Ready for `spec`.

Core invariant:

```text
`ci-maintenance` is a skill for maintaining CI infrastructure, not merely running CI.

The rename should make the skill identity honest, and the enhancement should
make good GitHub Actions workflow shape the default: fast PR feedback, risk-based
coverage, least-privilege permissions, safe caching, clear failure output, and
heavy checks at schedule/release/manual boundaries.
```
