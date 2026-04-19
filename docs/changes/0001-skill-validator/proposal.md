# 0001 Skill Validator Proposal

## Summary

This change ships the first proof-of-value RigorLoop example: a local skill metadata validator, fixture tests, deterministic generated-skill drift checks, CI integration, and the change-local artifact pack that explains the work.

## Source decisions

- Project direction: `../../proposals/2026-04-19-rigorloop-project-direction.md`
- Workflow product exploration: `../../proposals/2026-04-19-rigorloop-workflow-product.explore.md`
- Milestone commit policy: `../../proposals/2026-04-19-implementation-milestone-commit-policy.md`

## Change-local scope

- validate canonical `skills/` structure with a repo-owned command
- reject missing metadata, missing sections, duplicate names, placeholder text, and generated-source misuse
- test validator behavior with real fixtures under `tests/fixtures/skills/`
- detect `.codex/skills/` drift from canonical `skills/`
- run the same structural checks locally and in GitHub Actions
- publish the durable artifact pack at `docs/changes/0001-skill-validator/`

## Non-goals

- richer skill metadata than `name`, `description`, one top-level `#` title, and `## Expected output`
- subjective writing-quality or philosophy scoring
- hosted orchestration, release automation expansion, or non-Codex adapter generation

## Why this example

It is small, objective, and immediately useful to contributors. A contributor can run a command and get structural feedback without guessing hidden rules.
