# Docs Changes Skill Enforcement Explain Change

## Summary

This change aligns the stage-local workflow skills with the already-approved docs-changes contract for ordinary non-trivial work. It makes the baseline change-local pack explicit in `workflow` and `implement`, turns missing required packs into visible blockers in `verify` and `pr`, aligns `explain-change` with the default `docs/changes/<change-id>/explain-change.md` surface, and keeps canonical/generated skill output synchronized.

## Problem

The repository had already approved the docs-changes baseline pack at the workflow and packaging-contract level, but the stage-local skills still left too much of that behavior to contributor memory. That gap made it easy to implement non-trivial work without `docs/changes/<change-id>/change.yaml` plus durable Markdown reasoning, and it also left `verify` and `pr` without explicit blocker wording for missing required packs.

## Decision trail

- Proposal: `docs/proposals/2026-04-21-docs-changes-skill-enforcement.md`
- Spec: `specs/docs-changes-skill-enforcement.md`
- Requirements: `R1`-`R9`
- Architecture: no separate architecture artifact was required for this small skill-alignment slice
- Plan milestones:
  - M1: align `workflow` and `implement`
  - M2: align `verify`, `pr`, and `explain-change`
  - M3: run repo-owned proof and close implementation

## Diff rationale by area

| File or area | Change | Reason | Source artifact | Test / evidence |
| --- | --- | --- | --- | --- |
| `skills/workflow/SKILL.md`, `skills/implement/SKILL.md` | added explicit baseline-pack guidance for ordinary non-trivial work and preserved fast-lane omission | operationalize the approved docs-changes contract at the entrypoint and implementation stages | `R2`-`R3b`, M1 | `specs/docs-changes-usage-policy.test.md`, `python scripts/validate-skills.py`, `python scripts/build-skills.py --check` |
| `skills/verify/SKILL.md`, `skills/pr/SKILL.md`, `skills/explain-change/SKILL.md` | added blocker/readiness wording for missing baseline packs and aligned default durable reasoning output | make downstream stages stop treating missing required docs-changes artifacts as acceptable silence | `R4`-`R6a`, M2 | `specs/workflow-stage-autoprogression.test.md`, `bash scripts/ci.sh`, feature-level verify commands |
| `specs/docs-changes-usage-policy.test.md`, `specs/workflow-stage-autoprogression.test.md` | updated existing relied-on proof surfaces to cover the changed skill behavior | keep already-authoritative test specs truthful where they already owned the relevant contract proof | M1, M2 plan requirements | manual review proof recorded in the plan, plus artifact-lifecycle validation |
| `specs/docs-changes-skill-enforcement.test.md` | added focused feature test spec for the new skill-alignment slice | map the follow-up spec into milestone-level proof without replacing existing docs-changes and workflow-stage proof surfaces | feature test-spec stage | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` |
| `.codex/skills/` mirrors | regenerated from canonical skill edits | preserve the canonical/generated contract and avoid hand-edited drift | `R7`, all milestones | `python scripts/build-skills.py`, `python scripts/build-skills.py --check` |
| `docs/changes/2026-04-21-docs-changes-skill-enforcement/` | added `change.yaml` and this explain artifact | make the feature itself comply with the docs-changes contract it enforces | docs-changes baseline contract, M2 discovery | `python scripts/validate-change-metadata.py docs/changes/2026-04-21-docs-changes-skill-enforcement/change.yaml` |
| `docs/plan.md`, `docs/plans/2026-04-21-docs-changes-skill-enforcement.md`, `specs/docs-changes-skill-enforcement.test.md` | kept lifecycle state and readiness current through implementation, review, verify, and explain-change | avoid stale active-state bookkeeping and keep downstream stages honest | plan policy in `AGENTS.md`, verify lifecycle rules | targeted artifact-lifecycle validation and `git diff --check` |

## Tests added or changed

- `specs/docs-changes-skill-enforcement.test.md`
  - Defines the focused proof for the new follow-up feature.
  - Proves the right level of behavior here because the feature is guidance- and skill-driven rather than a new runtime subsystem.
- `specs/docs-changes-usage-policy.test.md`
  - Extends the existing docs-changes proof surface to include stage-local `workflow` and `implement` guidance.
  - This is the correct level because that test spec already owned the baseline-pack and durable-reasoning contract.
- `specs/workflow-stage-autoprogression.test.md`
  - Extends the existing workflow-stage proof surface to include missing docs-changes-pack blockers in direct-`pr` and isolated-`verify` scenarios.
  - This is the correct level because that test spec already owned direct-stage readiness and blocker semantics.

## Verification evidence

- `python scripts/validate-change-metadata.py docs/changes/2026-04-21-docs-changes-skill-enforcement/change.yaml`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py`
- `python scripts/build-skills.py --check`
- `bash scripts/ci.sh`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-21-docs-changes-skill-enforcement.md --path specs/docs-changes-skill-enforcement.md --path docs/plans/2026-04-21-docs-changes-skill-enforcement.md --path specs/docs-changes-skill-enforcement.test.md --path specs/docs-changes-usage-policy.test.md --path specs/workflow-stage-autoprogression.test.md`
- `git diff --check ba8998e..HEAD`
- Hosted CI status: unobserved from this environment

## Alternatives rejected

- Adding validator-side inference for missing baseline packs without any `change.yaml`
  - Rejected because the approved feature explicitly kept that as a later possible follow-up.
- Redesigning `change.yaml` or the docs-changes contract itself
  - Rejected because this change only needed stage-local skill alignment.
- Creating a new top-level `docs/explain/` artifact for this feature
  - Rejected because the approved default for new ordinary non-trivial work is the change-local `docs/changes/<change-id>/explain-change.md` surface.

## Scope control

- Fast-lane omission remained unchanged.
- Standalone `review-resolution.md` and `verify-report.md` remained conditional.
- No `change.yaml` schema redesign was introduced.
- No repo-wide missing-pack inference was added.
- No broad workflow-lane redesign was introduced outside the touched skills and existing proof surfaces.

## Risks and follow-ups

- Hosted CI still needs to be observed on the eventual PR.
- This branch still carries the earlier docs-changes usage-policy work because the replacement PR will come from `feat/docs-changes-skill-enforcement-v2`.
- A later feature may still add executable missing-pack inference for ordinary non-trivial work when no `change.yaml` exists.
