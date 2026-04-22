# Code Review Independence Under Autoprogression Explain Change

## Summary

This change implements the approved first-pass `code-review` contract without broadening the existing v1 autoprogression boundary. It updates the canonical `code-review` and `workflow` skills plus the repository workflow summary so autoprogressed reviews must run in independent-review mode, emit a first-pass review record before any review-driven fixes, use the approved first-pass statuses, and treat clean reviews as evidence-backed rather than praise-backed.

## Problem

The repository had already approved an explicit contract for independent first-pass review under autoprogression, but the canonical workflow guidance still taught the older `approve / request changes / block` model. It also still implied positive notes were always expected and did not require a first-pass review record before the `review-resolution` loop began. That left the most important guidance surfaces weaker than the approved spec.

## Decision trail

- Proposal: `docs/proposals/2026-04-22-code-review-independence-under-autoprogression.md`
- Spec: `specs/code-review-independence-under-autoprogression.md`
- Test spec: `specs/code-review-independence-under-autoprogression.test.md`
- Requirements: `R1`-`R8d`
- Architecture: no separate architecture artifact was required for this first slice
- Plan milestone:
  - M1: implement the independent first-pass code-review contract

## Diff rationale by area

| File or area | Change | Reason | Source artifact | Test / evidence |
| --- | --- | --- | --- | --- |
| `skills/code-review/SKILL.md` | replaced the older verdict model with independent-review mode, first-pass statuses, required first-pass record contents, stop conditions, and the clean-review template shape | make the stage-local review guidance match the approved contract instead of relying on contributor memory | spec `R1`-`R7`, M1 | `specs/code-review-independence-under-autoprogression.test.md`, `python scripts/validate-skills.py`, `python scripts/build-skills.py --check` |
| `skills/workflow/SKILL.md` | clarified the full-feature lane and autoprogression chain so `code-review` emits a first-pass record, only `changes-requested` enters `review-resolution`, and `blocked` / `inconclusive` stop | preserve the existing stage boundary while making the workflow-managed status mapping explicit | spec `R4`-`R5`, `R8`-`R8d`, M1 | `specs/code-review-independence-under-autoprogression.test.md`, `specs/workflow-stage-autoprogression.test.md` |
| `docs/workflows.md` | summarized the new first-pass review record requirement, status mapping, and evidence-backed clean-review rule in the short workflow guide | keep contributor-facing operational guidance truthful without moving feature detail out of the approved spec | observability section, M1 | manual contract review plus repo-owned validation |
| `.codex/skills/` mirrors | regenerated generated `code-review` and `workflow` skill output from canonical sources | keep canonical and generated skill surfaces synchronized | spec `R8`, M1 | `python scripts/build-skills.py`, `python scripts/build-skills.py --check` |
| `docs/changes/2026-04-22-code-review-independence-under-autoprogression/` | added the required baseline change-local pack for this ordinary non-trivial change | make the feature itself comply with the repository’s docs-changes contract | docs-changes baseline policy, M1 | change-local artifact review plus repo-owned validation |

## Tests changed or relied on

- `specs/code-review-independence-under-autoprogression.test.md`
  - Owns the focused proof for independent-review mode, first-pass record contents, status mapping, evidence-backed clean reviews, optional positive notes, and sensitive-change coverage.
- `specs/workflow-stage-autoprogression.test.md`
  - Continues to own the broader execution-chain and isolated-stage proof, with only the already-applied proof-ownership clarification needed to avoid overlap drift.

## Verification evidence

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/build-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/validate-change-metadata.py docs/changes/2026-04-22-code-review-independence-under-autoprogression/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-independence-under-autoprogression.md --path specs/code-review-independence-under-autoprogression.md --path specs/code-review-independence-under-autoprogression.test.md --path docs/plans/2026-04-22-code-review-independence-under-autoprogression.md`
- `rg -n 'independent-review|first-pass review record|clean-with-notes|changes-requested|blocked|inconclusive|no-finding rationale|positive note|review-resolution' skills/code-review/SKILL.md skills/workflow/SKILL.md docs/workflows.md .codex/skills specs/code-review-independence-under-autoprogression.test.md specs/workflow-stage-autoprogression.test.md`
- `rg -n 'code-review|verify|validation|workflow-managed|isolated|review-resolution' AGENTS.md CONSTITUTION.md docs/workflows.md`
- `git diff --check -- skills/code-review/SKILL.md skills/workflow/SKILL.md skills/implement/SKILL.md docs/workflows.md specs/code-review-independence-under-autoprogression.test.md specs/workflow-stage-autoprogression.test.md docs/changes/2026-04-22-code-review-independence-under-autoprogression .codex/skills`
- `bash scripts/ci.sh`

## Scope control

- `AGENTS.md` was left unchanged because this slice did not require additional practical agent instructions beyond the approved feature spec, active test spec, and updated workflow summary.
- `CONSTITUTION.md` was left unchanged because the implementation refined stage-local workflow guidance rather than introducing a new governance principle.
- `skills/implement/SKILL.md` was left unchanged because its handoff wording already matched the approved `implement -> code-review` boundary.
- No hard fresh-session enforcement, mandatory human review, fast-lane expansion, bugfix autoprogression, or new standalone `review-resolution.md` requirement was introduced.
