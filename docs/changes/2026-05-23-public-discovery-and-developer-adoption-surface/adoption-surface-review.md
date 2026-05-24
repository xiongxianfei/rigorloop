# Adoption Surface Review

## Scope

This M1 record starts the adoption-surface review with baseline stale-version
and unsupported-claim sweeps. Full cold-read, link-check, command-check, and
visual-accuracy evidence remains owned by M2 after README changes exist.

## Reviewer

- Reviewer or role: Codex implement skill, M1 baseline proof
- Review stage: before README/package adoption-surface implementation

## Current first command identified

```bash
npx @xiongxianfei/rigorloop@latest --help
```

## Current value proposition identified

RigorLoop is a Git-first workflow for AI-assisted software delivery that keeps
intent, requirements, tests, validation evidence, and review concerns in durable
project artifacts.

## Current target audience identified

Individual contributors doing AI-assisted software delivery, with maintainers
and small teams as secondary users.

## Stale-version sweep baseline

- Command: `rg -n "@xiongxianfei/rigorloop@0\\.1\\.5" README.md packages/rigorloop/README.md packages/rigorloop/package.json docs/ || true`
- Result: current-use stale pinned examples exist in `README.md` and `packages/rigorloop/README.md`.
- Required follow-up: M2 and M3 must update current-use adoption examples to `@latest` or `@0.2.0`; historical release/retrospective references may remain if clearly historical.

## Unsupported-claim sweep baseline

- Command: `rg -n "hosted|SaaS|control plane|autonomous|merge|replacement|replace|production|stars|forks|adoption|security status|CI status" README.md packages/rigorloop/README.md docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface || true`
- Result:
  - README contains negative or boundary wording for hosted platform/control plane and replacement claims.
  - README `new-change` text says it does not replace proposal, spec, review, verification, or PR judgment.
  - Change-local lifecycle artifacts discuss adoption-surface scope and explicitly avoid hosted runtime/autonomous merge positioning.
- Unsupported claim result: no unsupported broad adoption, production maturity, hosted-platform, autonomous-merge, fake status, or replacement claim was identified in M1 baseline evidence.

## Links checked

Not yet checked in M1. M2 must record required README link checks after the
adoption-surface link group is updated.

## Quick Start commands checked

Baseline only. `@latest` help/init commands are present, but current-use pinned
examples still use `@0.1.5` and must be updated in M2/M3.

## Visual accuracy check result

Not yet checked in M1. The README lifecycle diagram is added in M2, and M2 must
record visual accuracy evidence.

## M1 status

M1 establishes baseline evidence only. It does not complete the full
`DXA-R15`/`AC-DXA-014` adoption-surface review requirement.

## M2 cold-read and link-check evidence

- Reviewer or role: Codex implement skill, M2 README adoption-surface review.
- Review stage: after root README first-contact changes.
- First command identified:

```bash
npx @xiongxianfei/rigorloop@latest --help
```

- One-sentence value proposition identified:
  - RigorLoop keeps AI-assisted changes reviewable by moving ideas through
    durable Git-tracked proposals, specs, tests, review gates, validation
    evidence, and PR-ready rationale.
- Target audience identified:
  - Individual contributors first, with maintainers and small teams as
    secondary users that need auditable AI-assisted delivery.
- Quick Start commands checked:
  - `npx @xiongxianfei/rigorloop@latest --help`
  - `npx @xiongxianfei/rigorloop@latest init --adapter codex`
  - `npx @xiongxianfei/rigorloop@0.2.0 init --adapter codex`
  - `npx @xiongxianfei/rigorloop@0.2.0 init --adapter codex --json`
- Links checked:
  - `docs/workflows.md`: exists.
  - `specs/rigorloop-workflow.md`: exists.
  - `docs/changes/0001-skill-validator/`: exists.
  - `CONTRIBUTING.md`: exists.
  - `.github/ISSUE_TEMPLATE/bug.yml`: exists.
  - `.github/ISSUE_TEMPLATE/feature.yml`: exists.
  - `SECURITY.md`: exists.
  - `specs/README.md`: exists.
  - `skills/`: exists.
  - `.github/pull_request_template.md`: exists.
- Link-check method:
  - No dedicated README link checker exists in the repository.
  - Manual path-existence check was used:
    `for p in docs/workflows.md specs/rigorloop-workflow.md docs/changes/0001-skill-validator CONTRIBUTING.md SECURITY.md .github/ISSUE_TEMPLATE/bug.yml .github/ISSUE_TEMPLATE/feature.yml specs/README.md skills .github/pull_request_template.md; do test -e "$p" && printf 'exists %s\n' "$p" || printf 'missing %s\n' "$p"; done`
- Stale-version sweep result:
  - `README.md` has no remaining `@0.1.5` examples.
  - `packages/rigorloop/README.md` still has current-use `@0.1.5` examples
    for M3.
  - Historical `docs/releases/v0.1.5/` and retrospective references remain.
- Unsupported-claim sweep result:
  - README matches are boundary/negative wording for hosted/control-plane and
    replacement behavior, plus workflow terms such as `pr`.
  - No unsupported broad-adoption, production maturity, hosted-platform,
    autonomous-merge, fake-status, or replacement claim was identified.
- Visual accuracy check result:
  - README includes a static Mermaid `flowchart LR` from `Idea` through `PR`.
  - The caption states the full chain is recommended for complete
    AI-assisted delivery and manual skill invocations may use only relevant
    stages without implying full workflow completion.
  - No CLI GIF, long product video, or marketing screenshot gallery was added.
- First-contact result:
  - The README top section now answers what RigorLoop is, who it is for, why
    it matters, how to try it, where to see proof/workflow evidence, and where
    to contribute, report feedback, or find security guidance.

M2 completes the README-owned portions of `DXA-R15`/`AC-DXA-014`. Package
README command checks remain owned by M3, and live metadata after-state proof
remains owned by M4.

## M3 npm package landing review

- Reviewer or role: Codex implement skill, M3 npm package landing review.
- Review stage: after package metadata and package README changes.
- Package metadata checked:
  - Description mirrors approved repository positioning.
  - Keywords are present and mirror the approved topic set where package
    metadata supports keywords.
  - Keyword syntax check passed with lowercase letters, numbers, and hyphens.
- Package README commands checked:
  - Quick-trial commands use `@latest`.
  - Reproducible public CLI examples use `@0.2.0`.
  - Local archive examples use matching `v0.2.0` archive names.
  - `new-change` examples use `@0.2.0`.
- Stale-version sweep result:
  - No `@0.1.5` matches remain in current README, package README, or package
    metadata surfaces.
  - Remaining `@0.1.5` matches are historical release or retrospective records.
- Unsupported-claim sweep result:
  - npm-facing copy keeps npm positioned as the CLI delivery channel and not
    the canonical source for workflow rules, skills, schemas, templates, or
    adapter archives.
  - No unsupported broad-adoption, production maturity, hosted-platform,
    autonomous-merge, fake-status, replacement, or unsupported CLI behavior
    claim was identified.
- Package behavior check:
  - `npm test --prefix packages/rigorloop` passed with 107 tests.

M3 completes the npm/package-facing portions of `DXA-T006`. Live repository
metadata after-state proof remains owned by M4.
