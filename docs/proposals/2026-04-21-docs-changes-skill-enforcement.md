# Docs Changes Skill Enforcement

## Status

- accepted

## Problem

The repository now has an approved contract for `docs/changes/<change-id>/` packaging, but the stage-local skills still do not consistently operationalize it.

That leaves a real execution gap:

- the workflow/governance surfaces say non-trivial work needs `docs/changes/<change-id>/change.yaml` plus durable Markdown reasoning;
- the stage-local skills that drive day-to-day work do not consistently tell the agent when to create, verify, explain, and check that baseline pack;
- the current metadata validator only checks the contract when a `change.yaml` file already exists, so a missing baseline pack can still slip through if the skills do not demand it first.

Recent work exposed this directly: the docs-changes usage-policy feature itself initially moved through implementation, verification, explanation, and PR prep without a new `docs/changes/<change-id>/` pack, even though the approved contract for new non-trivial work said it should have one.

## Goals

- Make the skill layer operationalize the approved docs-changes contract instead of relying on reviewer memory.
- Reduce recurrence of non-trivial changes reaching `verify` or `pr` without the baseline `docs/changes/` pack.
- Keep stage responsibilities clear:
  - `workflow` routes and classifies;
  - `implement` creates or updates the baseline pack;
  - `verify` blocks on missing required pack artifacts;
  - `explain-change` uses the approved durable reasoning surface;
  - `pr` checks pack presence as part of readiness.
- Keep the change narrow and aligned with the already-approved docs-changes policy.

## Non-goals

- Redesigning `change.yaml` or its schema.
- Reopening the baseline-versus-conditional docs-changes contract itself.
- Forcing fast-lane work to create `docs/changes/` artifacts when the approved workflow still allows omission.
- Adding a new repository-wide storage model, registry, or orchestration system.
- Backfilling every historical non-trivial change with a new change-local pack.
- Solving every missing-pack case through validator automation in this same change if a smaller skill-alignment slice is sufficient first.

## Context

- The approved docs-changes policy now says:
  - non-trivial work requires `docs/changes/<change-id>/change.yaml`;
  - new non-trivial work defaults to `docs/changes/<change-id>/explain-change.md`;
  - standalone `review-resolution.md` and `verify-report.md` remain conditional.
- The governing workflow contract already says the same rule in `specs/rigorloop-workflow.md`.
- The current skills lag that contract:
  - `skills/workflow/SKILL.md` does not yet make the baseline change-local pack part of the ordinary non-trivial execution expectation;
  - `skills/implement/SKILL.md` does not tell the agent to create or update that baseline pack during implementation;
  - `skills/verify/SKILL.md` knows how to use `docs/changes/<change-id>/change.yaml` when it exists, but it does not yet clearly block when a non-trivial change should have a baseline pack and does not;
  - `skills/pr/SKILL.md` does not yet name the baseline docs-changes pack as an explicit readiness check;
  - `skills/explain-change/SKILL.md` does not yet connect its output expectations to the default change-local durable reasoning surface for new non-trivial work.
- Because the current validator only checks `change.yaml` shape and keys when the file exists, the skill layer remains the first line of enforcement for ordinary execution behavior.
- This proposal is a follow-up to the docs-changes policy change that is currently on the stacked feature branch, not a separate contract direction.

## Options considered

### Option 1: Do nothing and rely on specs, review, and maintainer memory

- Advantages:
  - no new skill text to maintain
  - avoids short-term duplication between workflow docs and skills
- Disadvantages:
  - the current miss can recur
  - review and verify stay too dependent on human memory
  - the skill layer remains visibly out of sync with the approved contract

### Option 2: Add only validator-side enforcement for missing baseline packs

- Advantages:
  - strongest executable enforcement
  - can catch omissions even if a skill forgets to mention them
- Disadvantages:
  - still leaves the day-to-day skill guidance stale
  - requires deciding how a validator determines that a change is non-trivial and therefore should have a pack
  - is larger and riskier than the immediate skill-alignment need

### Option 3: Align the stage-local skills to the approved docs-changes contract

- Advantages:
  - fixes the actual operator-facing gap where the miss occurred
  - keeps the change small and reviewable
  - respects the current architecture by reusing existing skills instead of adding a new subsystem
  - can be done without changing the schema or inventing new metadata inference logic
- Disadvantages:
  - relies on skill compliance rather than pure executable enforcement
  - still leaves open whether a later validator enhancement should catch missing packs automatically

### Option 4: Align the skills and also add a narrow follow-up validator blocker in the same feature

- Advantages:
  - gives both guidance and executable enforcement
  - reduces recurrence more aggressively
- Disadvantages:
  - broadens scope beyond the immediate skill gap
  - increases design and testing burden because the repository would need a principled rule for determining when a missing change-local pack is a validator error

## Recommended direction

Choose Option 3 for this follow-up.

The next change should align the canonical skills with the approved docs-changes policy, without reopening that policy itself.

The practical direction should be:

- `workflow` should state that ordinary non-trivial work carries the baseline change-local pack;
- `implement` should explicitly create or update `docs/changes/<change-id>/change.yaml` plus the default durable reasoning artifact for new non-trivial work unless an approved equivalent surface already exists;
- `verify` should treat a missing required baseline pack for non-trivial work as a blocker, not merely as incidental drift;
- `pr` should include the required docs-changes pack in its readiness checks for non-trivial work;
- `explain-change` should align its durable-output expectations with the default change-local reasoning surface for new non-trivial work;
- generated `.codex/skills/` output should be regenerated from the canonical skill edits.

This follow-up should stay skill-focused. If later experience shows that skill guidance is not enough, a separate proposal can add executable missing-pack enforcement in repo-owned validation.

## Expected behavior changes

- Agents will stop treating the docs-changes baseline pack as optional for new non-trivial work simply because the top-level spec is not in the immediate skill instructions.
- `implement` will more consistently create or update the required change-local artifacts during ordinary non-trivial feature work.
- `verify` and `pr` will more consistently block missing baseline pack artifacts instead of passing them through as review-time surprises.
- `explain-change` output will line up better with the approved change-local durable reasoning default for new work.
- Fast-lane behavior will remain unchanged.

## Architecture impact

This should remain a small workflow-guidance alignment, not a system redesign.

- Components likely touched:
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - matching generated `.codex/skills/`
  - any directly related workflow summary surfaces only if wording drift appears
- Boundaries preserved:
  - `specs/rigorloop-workflow.md` remains the normative home
  - `specs/docs-changes-usage-policy.md` remains the focused contract
  - no schema redesign
  - no new persistence or registry
  - no broad validator redesign in this slice

## Testing and verification strategy

- Manual contract review should confirm each touched skill says the same thing as the approved workflow/docs-changes contract.
- Generated-skill drift checks should prove `.codex/skills/` stays synchronized with canonical `skills/`.
- Repo-owned smoke validation should continue to pass after the skill updates.
- If the follow-up spec chooses to make `verify` or `pr` more explicit about missing-pack blockers, the matching test spec should include concrete manual checks for those stage outcomes.

## Rollout and rollback

Rollout:

- land the skill-alignment change after the docs-changes policy branch it depends on;
- regenerate `.codex/skills/`;
- verify that the next non-trivial change naturally creates and checks its baseline pack through the updated skills.

Rollback:

- revert the canonical/generated skill edits together;
- fall back temporarily to the top-level workflow/spec wording while designing a narrower or broader follow-up if needed.

## Risks and mitigations

- Risk: skill text duplicates too much policy detail and drifts from the workflow spec.
  - Mitigation: keep the workflow spec normative and limit the skills to stage-specific operational duties.
- Risk: the follow-up accidentally broadens fast-lane obligations.
  - Mitigation: keep fast-lane omission explicitly out of scope and restate that boundary in the updated skills.
- Risk: reviewers assume the skill update alone fully solves missing-pack enforcement.
  - Mitigation: say explicitly that validator-side missing-pack enforcement remains a separate possible follow-up.
- Risk: this proposal depends on the unmerged docs-changes policy branch.
  - Mitigation: keep that dependency explicit and treat this proposal as a stacked follow-up until the base branch merges.

## Open questions

- Should the follow-up stop at skill alignment, or should a later separate change add executable validator enforcement for missing baseline packs?
- Which stage-local skills need explicit per-stage docs-changes wording beyond `workflow`, `implement`, `verify`, `explain-change`, and `pr`?
- Should the related test spec stay manual-and-smoke only, or should it also add a concrete regression fixture once the repository has a reliable way to detect missing required packs?

## Decision log

- 2026-04-21: Chose a skill-alignment follow-up instead of a validator-first redesign. Reason: the observed miss came from the operator-facing guidance layer, and the smallest useful correction is to align the stage-local skills with the already-approved docs-changes contract before adding broader automation.

## Next artifacts

- `proposal-review`
- `spec`
- `spec-review`
- `architecture` if the follow-up broadens beyond a small skill-alignment slice

## Follow-on artifacts

- `specs/docs-changes-skill-enforcement.md`
- `docs/plans/2026-04-21-docs-changes-skill-enforcement.md`
- `specs/docs-changes-skill-enforcement.test.md`

## Readiness

- This proposal is accepted.
- The main dependency is explicit: it is stacked on the docs-changes policy branch because that contract is not merged yet.
- No open question currently blocks planning.
- The approved spec, active plan, and active test spec now exist.
- The next stage is `implement`.
