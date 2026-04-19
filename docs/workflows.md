# Workflows

This file defines the repository's normal human + Codex workflow. Keep it short and operational.

## When to use a plan

Use a plan when the work is multi-file, risky, ambiguous, architecture-affecting, migration-heavy, or likely to outgrow one small reviewable PR.

Do not require a full plan for tiny fixes, docs-only edits, mechanical refactors, or single-file changes with obvious verification.

## Default feature workflow

`plan -> spec -> test-spec -> implement -> verify -> docs -> review`

### What each step means

- `plan`: define milestones, constraints, and verification strategy
- `spec`: document user-visible or contract-level behavior
- `test-spec`: map the contract to tests
- `implement`: make the smallest change that satisfies the contract
- `verify`: run the smallest relevant checks first, then the broader checks required by this repo
- `docs`: update user-facing or maintainer-facing docs if behavior or workflow changed
- `review`: prepare the branch for human review

## Bugfix workflow

`reproduce -> regression-test -> implement -> verify -> document impact`

Notes:
- Add or update a regression test first when feasible.
- Keep the fix smaller than the bug report whenever possible.
- State the verified reproduction path and the verified fix path.

## CI workflow

Use `ci` work only for GitHub Actions, automation, or other delivery pipeline changes.

Expected flow:
`scope -> minimal workflow change -> local validation when possible -> workflow validation -> document required status checks`

## Release workflow

The default release path for this template is tag-driven:

1. ensure `main` is green
2. confirm version and compatibility notes
3. verify release readiness
4. create and push a version tag like `v1.2.3`
5. let GitHub create the release from the tag with generated notes
6. patch follow-up docs only if the release changed visible behavior or support policy

Do not cut releases from a dirty branch or from unverified commits.

## Documentation ownership

- `README.md`: user-facing overview and quick start
- `docs/workflows.md`: operational workflow for maintainers and Codex
- `docs/roadmap.md`: future ideas and unapproved work
- `docs/plan.md`: index of approved and historical plans
- `docs/plans/*.md`: living execution plans
- `specs/*.md`: behavior contract
- `specs/*.test.md`: contract-to-test mapping

## Final response expectations

A complete implementation response should say:

- what changed
- what was verified
- any assumptions, gaps, or follow-up work
