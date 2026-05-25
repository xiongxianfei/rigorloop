# Proposal Review: Target-Native Init Commands and Adapter Terminology Retirement R2

Review ID: proposal-review-r2
Stage: proposal-review
Round: 2
Reviewer: Codex proposal-review
Target: docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md
Status: approved

## Review Inputs

- Revised proposal: `docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md`
- R1 material finding: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/proposal-review-r1.md`
- Review resolution: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-resolution.md`
- User-provided R1 confirmation and recommended resolution text.

## Result

- Skill: proposal-review
- Review status: approved
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/proposal-review-r2.md`
- Review log: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-log.md`
- Review resolution: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-resolution.md`
- Open blockers: none
- Immediate next stage: spec or spec amendment
- Eventual spec readiness: ready
- No automatic downstream handoff: this review is isolated and does not start spec, plan, test-spec, or implementation work.

## Findings

No material findings.

## R1 Closeout

`TINIT-PR1-F1` is resolved. The proposal now states one consistent first-slice boundary:

- public CLI syntax, public docs, and user-visible state content written by `--write-state` use target/tool terminology;
- default `init <target>` preserves existing state files unchanged;
- non-user-visible internal code names, `dist/adapters/` paths, archive filenames, package-bundled metadata field names, historical release evidence, and existing state files preserved by default init may continue to use `adapter` until a later migration;
- the state-file schema boundary explicitly requires target-oriented keys for new `rigorloop.yaml` and `rigorloop.lock` content written by `--write-state`;
- legacy state files with `adapter` keys are compatibility input whose migration, rewrite, or block behavior must be specified.

## Review Dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| Problem clarity | pass | The proposal clearly separates command UX, default state-file friction, and release-smoke gaps. |
| User value | pass | Target-native init, no default state files, and opt-in managed state are concrete improvements. |
| Option diversity | pass | The proposal covers current syntax, aliases, hard removal, top-level target commands, state-file defaults, and internal rename scope. |
| Decision rationale | pass | The 0.3.0 hard-removal, install-only default, `--write-state`, and release-smoke decisions are tied to user goals and incident evidence. |
| Scope control | pass | The revised terminology boundary distinguishes user-visible state schemas from deferred non-user-visible internals. |
| Architecture awareness | pass | Release archive internals, package metadata, docs, CLI syntax, and state-file schemas are treated as separate surfaces. |
| Testability | pass | CLI parsing, docs sweep, state-file behavior, metadata/archive coherence, packed smoke, and live smoke are testable. |
| Risk honesty | pass | Compatibility breaks, metadata drift, release smoke gaps, docs drift, internal rename churn, and managed-state ambiguity are named. |
| Rollout realism | pass | Packed pre-publish and live post-publish gates are appropriately separated. |
| Readiness for spec | pass | The proposal is ready for a target-native init spec or spec amendment. |

## Scope Preservation

Initial user goals remain preserved:

- Use `init codex`, `init claude`, and `init opencode` directly: in scope.
- Remove `--adapter` totally in `0.3.0`: in scope.
- Accept only `codex`, `claude`, and `opencode`: in scope.
- Show `@latest` for manual quick start and pinned versions for automation: in scope.
- Use packed smoke before publish and live registry/download smoke after publish: in scope.
- Avoid default `rigorloop.yaml` and `rigorloop.lock`: in scope.
- Add `--write-state`: in scope.
- Preserve existing state by default and overwrite/regenerate with `--write-state`: in scope.
- Rename user-visible state-file keys away from `adapter`: in scope.
- Avoid full non-user-visible internal rename unless necessary: deferred follow-up.

## Recommendation

Approved for spec. The next artifact should amend or supersede the existing multi-adapter init and lockfile specs so the target-native command syntax, install-only default, `--write-state` behavior, and release-smoke gates become the authoritative implementation contract.
