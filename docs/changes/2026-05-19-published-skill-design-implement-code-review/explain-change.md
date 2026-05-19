# Published Skill Design Implement And Code-Review Change Explanation

Change: `2026-05-19-published-skill-design-implement-code-review`

## Summary

This change continues the accepted published-skill design rollout for the execution/review pair: `implement` and `code-review`.

The diff makes those two skills more portable and easier to route by tightening frontmatter descriptions, adding explicit workflow-role blocks, adding compact output skeletons, and preserving the high-risk lifecycle guardrails that make the skills useful.

## Problem

The accepted proposal requires published skills to behave like portable operating documentation. Before this slice, `implement` and `code-review` had strong procedural guidance, but their routing descriptions were broad, their lifecycle roles were implicit, and their result shapes were buried in long expected-output prose.

## Decision Trail

| Source | Decision |
|---|---|
| Proposal | Continue the published-skill design contract after the pilot and spec-family slices. |
| Spec | Preserve R27-R35: description routing, workflow role, resource self-containment, output skeleton, routing coverage, and behavior preservation. |
| Test spec | Add T25-T28 for execution/review audit, deterministic evidence checks, skill rewrite proof, generated output, adapter validation, and token evidence. |
| Plan | Split work into M1 evidence, M2 deterministic test support, and M3 skill rewrite. |
| Reviews | Plan-review, M1, M2, and M3 code-review all recorded clean outcomes with no material findings. |

## Diff Rationale By Area

| File | Change | Reason | Test/evidence |
|---|---|---|---|
| `skills/implement/SKILL.md` | Added readability frontmatter, routing-focused description, workflow role, and output skeleton. | Makes implementation routing and handoff expectations visible before deep body reading while preserving first-pass completeness and no-review-claim boundaries. | `test_skill_readability_execution_review_opts_into_contract`; M3 behavior-preservation evidence. |
| `skills/code-review/SKILL.md` | Added readability frontmatter, routing-focused description, workflow role, and first-pass review output skeleton. | Makes independent implementation review routing and review-record shape explicit while preserving finding, recording, direct-proof, and milestone-routing rules. | `test_skill_readability_execution_review_opts_into_contract`; M3 behavior-parity evidence. |
| `scripts/test-skill-validator.py` | Added focused regression for execution/review readability opt-in and M2 evidence scaffolding. | Protects the deterministic parts of the contract without adding broad prose scoring or runtime model-selection claims. | Full `python scripts/test-skill-validator.py` passes. |
| `docs/changes/.../skill-audit.md` | Recorded M3 audit result and token estimates. | Shows existence gate, no merge/retire action, and token-cost discipline. | `python scripts/measure-skill-tokens.py --skills-root skills`. |
| `docs/changes/.../routing-coverage.md` | Recorded final routing notes for both descriptions. | Keeps routing coverage reviewable and bounded. | M2/M3 regression and manual review evidence. |
| `docs/changes/.../behavior-preservation.md` | Replaced pending rows with M3 preservation evidence. | Shows behavior-significant wording was preserved. | M3 code-review. |
| `docs/changes/.../behavior-parity.md` | Recorded final parity and token-cost result. | Shows representative implementation handoff and code-review outcomes remain intact. | M3 code-review and validation notes. |
| `docs/plans/...`, `docs/plan.md`, `change.yaml`, review records | Kept lifecycle state, validation, review evidence, and next stage synchronized. | Required by the planned workflow and review-recording contract. | Review artifact, artifact lifecycle, and change metadata validation. |

## Tests Added Or Changed

- `test_published_design_execution_review_evidence_is_scaffolded`: proves the new change-local evidence scaffold covers both target skills and bounded routing classes.
- `test_skill_readability_execution_review_opts_into_contract`: failed before skill edits, then passed after both skills declared `skill-readability-v1`, `Workflow role`, and `Output skeleton`.

## Validation Evidence Before Final Verify

- `python scripts/validate-skills.py` passed.
- `python scripts/test-skill-validator.py` passed.
- `python scripts/measure-skill-tokens.py --skills-root skills` passed: `implement` 4860 tokens, `code-review` 5554 tokens.
- `python scripts/build-skills.py --check` passed.
- Temporary adapter archive build and validation for `v0.1.5` passed.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-published-skill-design-implement-code-review` passed.
- Change metadata, artifact lifecycle, whitespace, and selected CI checks passed as recorded in the active plan.

## Review Resolution Summary

No material findings were recorded. No `review-resolution.md` is required for this change.

## Alternatives Rejected

- Rewriting all skills: rejected by the plan scope.
- Adding semantic prose scoring or runtime model-selection assertions: rejected by the proposal and test spec.
- Accepting token-cost hard-cap overruns: rejected during M3; duplicated output prose was trimmed until both skills were below `+10%`.
- Hand-editing generated adapter output: rejected because canonical `skills/` remains the authored source.

## Scope Control

The change does not merge, retire, rename, remove, or change ownership of any skill. It does not change workflow stage order, validation selector semantics, adapter install roots, generated-output trust boundaries, release metadata, or public adapter source policy.

## Risks And Follow-Ups

The remaining risk is that both target skills are still large because they carry high-risk lifecycle guardrails. Token cost is below the hard cap but close enough that future edits should avoid duplicating output or review-record prose.

Current readiness: ready for `verify`, not PR-ready.
