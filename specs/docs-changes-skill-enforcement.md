# Docs Changes Skill Enforcement

## Status
- approved

## Related proposal

- [Docs Changes Skill Enforcement](../docs/proposals/2026-04-21-docs-changes-skill-enforcement.md)

## Goal and context

This spec defines how the repository's canonical workflow skills must operationalize the approved `docs/changes/<change-id>/` contract for non-trivial work.

The docs-changes policy is already approved at the workflow and feature-spec level. What is missing is stage-local enforcement in the skills that agents actually follow during implementation, verification, explanation, and PR preparation. The goal of this follow-up is to make the skills stop treating the baseline change-local pack as optional for ordinary non-trivial work while preserving the existing fast-lane omission boundary and the current conditional rules for `review-resolution.md` and `verify-report.md`.

## Glossary

- `baseline change-local pack`: the minimum required change-local artifact set for non-trivial work:
  - `docs/changes/<change-id>/change.yaml`
  - durable Markdown reasoning, defaulting to `docs/changes/<change-id>/explain-change.md` for new work
- `approved equivalent reasoning surface`: another durable reasoning artifact explicitly allowed by the governing workflow contract.
- `ordinary non-trivial work`: non-fast-lane work that is not exempt from the baseline `docs/changes/` contract.
- `stage-local skill`: a canonical workflow skill such as `workflow`, `implement`, `verify`, `explain-change`, or `pr`.

## Examples first

### Example E1: ordinary non-trivial implementation creates the baseline pack

Given a contributor is executing ordinary non-trivial feature work
When the `implement` skill guides the change
Then the skill directs the agent to create or update `docs/changes/<change-id>/change.yaml` and the required durable reasoning surface for that change.

### Example E2: fast-lane work keeps the current omission rule

Given a contributor is making a trivial fast-lane documentation clarification
When the `workflow` or `implement` skill routes the work
Then the skills do not require `docs/changes/<change-id>/` unless the approved fast-lane policy or maintainer direction says otherwise.

### Example E3: verify blocks a missing required baseline pack

Given a non-trivial change reaches `verify`
When the branch lacks the required baseline change-local pack for that change
Then `verify` reports a blocker instead of treating the omission as a non-blocking note.

### Example E4: PR preparation checks docs-changes readiness

Given a non-trivial change reaches `pr`
When the required baseline change-local artifacts are missing
Then `pr` reports the missing docs-changes pack as a readiness blocker and does not open the pull request.

### Example E5: explain-change aligns with the default reasoning surface

Given new non-trivial work reaches `explain-change`
When no approved equivalent durable reasoning surface applies
Then the skill treats `docs/changes/<change-id>/explain-change.md` as the default durable explanation artifact for that change.

## Requirements

R1. The canonical workflow skills MUST operationalize the approved docs-changes contract for ordinary non-trivial work instead of leaving the baseline change-local pack to reviewer memory alone.

R1a. This follow-up MUST preserve the current normative split:
- `specs/rigorloop-workflow.md` remains the normative workflow contract;
- `specs/docs-changes-usage-policy.md` remains the focused packaging contract;
- skills summarize and operationalize those rules for stage-local behavior.

R2. `skills/workflow/SKILL.md` MUST state that ordinary non-trivial work carries the baseline change-local pack.

R2a. `skills/workflow/SKILL.md` MUST preserve the approved fast-lane boundary and MUST NOT imply that every change requires `docs/changes/<change-id>/`.

R2b. `skills/workflow/SKILL.md` MUST preserve the distinction that standalone `review-resolution.md` and `verify-report.md` remain conditional rather than universal.

R3. `skills/implement/SKILL.md` MUST instruct the agent to create or update the baseline change-local pack for ordinary non-trivial work.

R3a. For new non-trivial work, `skills/implement/SKILL.md` MUST treat `docs/changes/<change-id>/explain-change.md` as the default durable reasoning artifact unless an approved equivalent reasoning surface already applies under the governing workflow contract.

R3b. `skills/implement/SKILL.md` MUST NOT broaden the docs-changes requirement to approved fast-lane work.

R4. `skills/verify/SKILL.md` MUST treat a missing required baseline change-local pack for ordinary non-trivial work as a blocker to PR readiness.

R4a. `skills/verify/SKILL.md` MUST continue to use changed files, `docs/changes/<change-id>/change.yaml`, explain-change artifacts, active plans, and other authoritative artifacts as part of its related-artifact reasoning, but it MUST NOT treat the absence of a required baseline pack as acceptable silence.

R5. `skills/pr/SKILL.md` MUST include required docs-changes artifacts in its readiness checks for ordinary non-trivial work.

R5a. `skills/pr/SKILL.md` MUST preserve the existing rule that `pr` opens the PR when readiness passes and reports blockers when readiness fails.

R6. `skills/explain-change/SKILL.md` MUST align its durable-output guidance with the default change-local durable reasoning surface for new non-trivial work.

R6a. `skills/explain-change/SKILL.md` MUST NOT imply that PR text alone is enough to satisfy durable reasoning for ordinary non-trivial work.

R7. Generated `.codex/skills/` output MUST be regenerated from the canonical skill changes and remain in sync.

R8. This follow-up MUST NOT redesign the `change.yaml` schema, MUST NOT redefine the approved docs-changes contract, and MUST NOT require backfilling historical changes with new change-local packs.

R9. This follow-up MUST remain compatible with the current approved docs-changes policy:
- baseline pack required for ordinary non-trivial work;
- fast-lane omission still allowed when the governing workflow contract allows it;
- legacy approved top-level `docs/explain/*.md` artifacts remain valid where the governing workflow contract says they do;
- standalone `review-resolution.md` and `verify-report.md` remain conditional.

## Inputs and outputs

Inputs:

- change classification as fast-lane or ordinary non-trivial work;
- governing docs-changes contract from the workflow spec and docs-changes usage-policy spec;
- current stage-local responsibilities for `workflow`, `implement`, `verify`, `explain-change`, and `pr`;
- generated `.codex/skills/` compatibility output.

Outputs:

- stage-local skill guidance that makes the baseline change-local pack operational for ordinary non-trivial work;
- regenerated `.codex/skills/` output synchronized with the canonical skill edits;
- clearer stage-local blocker behavior for missing required docs-changes artifacts.

## State and invariants

- The workflow spec remains the normative home for the docs-changes contract.
- Stage-local skills operationalize that contract but do not replace it.
- Ordinary non-trivial work still requires the baseline change-local pack.
- Fast-lane omission remains narrow and unchanged.
- Standalone `review-resolution.md` and `verify-report.md` remain conditional.
- Generated `.codex/skills/` content remains derived output, not a second source of truth.

## Error and boundary behavior

- If a skill update would make fast-lane work appear to require the baseline change-local pack, the change is incorrect.
- If a skill update suggests PR text alone satisfies durable reasoning for ordinary non-trivial work, the change is incorrect.
- If `verify` or `pr` still allow ordinary non-trivial work to proceed silently when a required baseline change-local pack is missing, the change is incomplete.
- If a skill update copies the full docs-changes contract into stage-local text so broadly that it competes with the workflow spec, the change is incorrect.
- If generated `.codex/skills/` output drifts from canonical `skills/`, the change is incomplete.

## Compatibility and migration

- This feature is guidance alignment, not a schema or storage migration.
- It preserves the approved docs-changes contract from the stacked base feature.
- It does not require historical backfill of old changes.
- It does not invalidate legacy approved top-level explain artifacts where the governing workflow contract still allows them.
- It should be merged after or on top of the docs-changes usage-policy change it depends on.

## Observability

- Reviewers should be able to inspect the touched skills and see the baseline-versus-conditional docs-changes rule without reverse-engineering it from only the top-level specs.
- Generated-skill drift checks should make canonical/generated mismatches visible.
- `verify` and `pr` outcomes should make missing required baseline packs observable as blockers instead of implicit omissions.

## Security and privacy

- The skill updates MUST NOT encourage moving durable reasoning into private chat or untracked notes.
- The skill updates MUST NOT encourage storing secrets, credentials, or sensitive runtime configuration in `change.yaml`, `explain-change.md`, `review-resolution.md`, or `verify-report.md`.
- No new network, secret, or credential dependency is introduced by this feature.

## Performance expectations

- No runtime performance change is expected.
- Validation and generated-skill drift checks should remain lightweight and file-based.
- The change should not add a new subsystem or expensive repository scan.

## Edge cases

1. A trivial fast-lane change may still omit `docs/changes/<change-id>/` under the approved fast-lane rule.
2. New ordinary non-trivial work defaults to `docs/changes/<change-id>/explain-change.md` for durable reasoning unless an approved equivalent surface applies.
3. A non-trivial change with conditional standalone `review-resolution.md` or `verify-report.md` requirements must still carry the baseline pack in addition to those conditional artifacts.
4. A skill update must not imply that the rich `0001-skill-validator` pack is the universal minimum for all non-trivial work.
5. Generated `.codex/skills/` output must stay synchronized after the canonical skill edits.
6. The feature may remain stacked on the docs-changes policy branch until that base change merges, but the resulting contract should not depend on long-term stacked-branch state.

## Non-goals

- Adding repository-wide executable enforcement that infers missing baseline packs without any `change.yaml` file present.
- Redesigning `schemas/change.schema.json`.
- Changing the docs-changes baseline-versus-conditional contract itself.
- Broadening docs-changes requirements to fast-lane work.
- Requiring updates to every skill in the repository when only a small stage-local set owns this behavior.

## Acceptance criteria

- A reviewer can inspect the touched canonical skills and see that ordinary non-trivial work requires the baseline change-local pack.
- A reviewer can see that fast-lane omission remains unchanged.
- A reviewer can see that `verify` and `pr` treat missing required baseline packs as blockers for ordinary non-trivial work.
- A reviewer can see that `explain-change` aligns with the default change-local durable reasoning surface for new non-trivial work.
- Canonical and generated skills remain in sync.

## Open questions

- Should a separate later feature add validator-side missing-pack enforcement beyond the skill layer?

## Next artifacts

- `plan`
- `test-spec`

## Follow-on artifacts

- `docs/plans/2026-04-21-docs-changes-skill-enforcement.md`
- `specs/docs-changes-skill-enforcement.test.md`

## Readiness

- This spec is approved.
- It intentionally stays inside a small skill-alignment slice and does not require a separate architecture artifact.
- No open question blocks implementation planning.
- The test spec now exists and the next stage is `implement`.
