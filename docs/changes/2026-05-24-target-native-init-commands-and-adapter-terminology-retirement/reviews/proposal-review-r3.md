# Proposal Review: Target-Native Init Commands and Adapter Terminology Retirement R3

Review ID: proposal-review-r3
Stage: proposal-review
Round: 3
Reviewer: Codex proposal-review
Target: docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md
Status: approved

## Review Inputs

- Proposal: `docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md`
- Prior review log: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-log.md`
- Prior review resolution: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-resolution.md`
- Prior R2 approval: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/proposal-review-r2.md`
- User-provided proposal-review instruction and expected R1/R2 conclusion.

## Result

- Skill: proposal-review
- Review status: approved
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/proposal-review-r3.md`
- Review log: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-log.md`
- Review resolution: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-resolution.md`
- Open blockers: none
- Immediate next stage: normalize proposal status to accepted, then proceed to spec or spec amendment.
- Eventual spec readiness: ready after proposal status normalization.
- No automatic downstream handoff: this review is isolated and does not start spec, plan, test-spec, or implementation work.

## Findings

No material findings.

## Review Dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| Problem clarity | pass | The proposal states the UX problem, default state-file friction, and release-smoke failure mode clearly. |
| User value | pass | Target-native init, install-only default behavior, and explicit `--write-state` remove concrete first-run friction. |
| Option diversity | pass | The proposal considers current syntax, aliases, hard removal, top-level target commands, default state writing, and explicit managed state. |
| Decision rationale | pass | The chosen `0.3.0` breaking cleanup follows the owner decisions and is paired with release-smoke hardening. |
| Scope control | pass | Public command/docs/state-file terminology is in scope; non-user-visible `dist/adapters/`, archive filenames, and metadata field names are deferred. |
| Architecture awareness | pass | CLI parsing, state-file schemas, release metadata, package archives, docs, and smoke gates are treated as separate surfaces. |
| Testability | pass | The proposal names CLI, docs, default state, `--write-state`, metadata coherence, packed smoke, and live smoke checks. |
| Risk honesty | pass | Compatibility breakage, metadata drift, dry-run gaps, docs drift, internal rename churn, and managed-state ambiguity are named. |
| Rollout realism | pass | Packed pre-publish smoke and live post-publish smoke are split at the right gates. |
| Readiness for spec | pass | The proposal is ready for a target-native init spec or spec amendment once its status is normalized from `draft` to `accepted`. |

## Scope Preservation

The proposal preserves the user's stated goals:

- Use `init codex`, `init claude`, and `init opencode` directly: in scope.
- Remove `--adapter` totally in `0.3.0`: in scope.
- Accept only `codex`, `claude`, and `opencode`: in scope.
- Show `@latest` for manual quick start and pinned versions for automation: in scope.
- Use packed smoke before publish and live registry/download smoke after publish: in scope.
- Avoid default `rigorloop.yaml` and `rigorloop.lock`: in scope.
- Add `--write-state`: in scope.
- Preserve existing state by default and regenerate with `--write-state`: in scope.
- Rename user-visible state-file keys away from `adapter`: in scope.
- Defer full non-user-visible internal rename: deferred follow-up with rationale.

## Notes

The proposal body still has `## Status` set to `draft` and `## Readiness` saying it is ready for proposal-review. That is not a material proposal-quality finding, but downstream spec work should not rely on the proposal until the status/readiness text is normalized to accepted.

## Recommendation

Approved. No new material findings. Normalize the proposal status to accepted before using it as the source of truth for spec or implementation work.
