# Skill Contract Optimization Explain Change

## Summary

This change defines and implements the first slice of the RigorLoop skill contract. It adds `specs/skill-contract.md` as the normative source for skill shape, claim boundaries, result output, shared blocks, generated-output boundaries, evidence-reading guidance, and minimum viable skill rules.

The implementation normalizes only the approved first-slice skills: `workflow`, `plan`, `implement`, `code-review`, `verify`, `pr`, and `learn`. It also adds focused static proof, contributor-facing shared policy guidance, public skill surface cleanup, and regenerated Codex and public adapter skill output.

Final branch verification was rerun after this explanation artifact was added. The prior `verify` pass confirmed selected validation and review closeout were clean, then correctly blocked because this durable reasoning artifact was missing.

## Problem

The proposal identified a recurring workflow bug: skills were too stateful and could blur progress, readiness, closeout, Done, review outcome, validation proof, branch readiness, and PR readiness.

That confusion had already appeared in recent workflow lessons. `Ready for verify` was sometimes treated as if it meant Done or PR-ready, and implementation progress could be mistaken for milestone closeout before review, validation, and closeout evidence were reconciled.

## Decision Trail

| Source | Decision |
| --- | --- |
| Proposal | Use a phased skill-contract rollout so skills become smaller, claim-safe, summary-first, and handoff-explicit without normalizing every skill at once. |
| Proposal review | Resolved SCO1, SCO2, SCO3, SCO4, SCO6, SCO7, and SCO8 before relying on the proposal downstream. |
| Spec | `specs/skill-contract.md` owns skill-contract behavior and the published skill surface boundary; `specs/rigorloop-workflow.md` continues to own stage order, obligation, handoff, and downstream blocking. |
| Test spec | `specs/skill-contract.test.md` maps the approved contract to static proof, public-surface checks, selected CI, generated-output drift checks, adapter validation, review closeout, and manual contract review. |
| Plan | M1 added static proof, M2 aligned source-of-truth summaries and shared blocks, M3 normalized the first-slice canonical skills, and M4 refreshed generated outputs. |
| Architecture | Not required because the slice changes repository guidance, static validation, generated mirrors, and adapter output, not runtime components or deployment boundaries. |
| Verification | Selected CI, review artifact closeout, change metadata validation, lifecycle validation, and diff hygiene passed before this artifact existed; `verify` stopped only because the baseline change-local durable reasoning artifact was missing. Final verify later passed after this artifact was committed. |

## Diff Rationale By Area

| Files | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `docs/proposals/2026-05-08-skill-contract-optimization.md` | Accepted the skill-contract direction, chose the first implementation slice, defined later normalization waves, and settled shared-block and overclaim decisions. | Gives spec and plan authors a decided scope instead of open-ended skill cleanup. | Proposal review findings SCO1-SCO8 | Proposal-review R2 approved; review artifacts close out SCO findings. |
| `specs/skill-contract.md` | Added the normative contract for required core sections, conditional sections, claim boundaries, result blocks, public skill surface boundaries, shared blocks, generated-output handling, evidence reading, and minimum viable skills. | Provides one source of truth for validator-enforced skill behavior and prevents maintainer-only repository details from leaking into shipped skills. | Proposal recommended direction; public-surface learn session | `scripts/test-skill-validator.py`; lifecycle validation. |
| `specs/rigorloop-workflow.md` | Added the pointer that `specs/skill-contract.md` owns skill-contract behavior while the workflow spec retains routing semantics. | Prevents skill-contract guidance from competing with workflow stage-order rules. | Spec R1-R1b, R20-R20b | `scripts/test-skill-validator.py`; lifecycle validation. |
| `docs/workflows.md`, `AGENTS.md` | Added concise contributor and agent reminders for canonical skill source, generated-output boundaries, public skill surface boundaries, skill-contract ownership, and minimum viable skill creation. | Keeps everyday guidance aligned without duplicating the full spec or exposing maintainer details in shipped skills. | Spec R1c, R3d, R19b | M2 selected CI and artifact lifecycle validation. |
| `templates/shared/evidence-collection-efficiency.md` | Kept evidence collection as public shared text and removed the unused generated-output handling shared block. | Public skills need evidence-reading consistency, but generated-output authoring and packaging mechanics belong in contributor surfaces rather than an unused shared source file. | Spec R14-R16 | Shared-block and public-surface assertions in `scripts/test-skill-validator.py`. |
| `scripts/test-skill-validator.py` | Added focused static assertions for source split, first-slice scope, shared block sources, required core sections, result blocks, claim boundaries, copied shared blocks, public skill surface boundaries, and narrow overclaim behavior. | Makes the guidance slice testable without adding broad semantic scoring or a runtime workflow simulator. | Test spec T1-T14 | Validator tests passed after the expected red/green iterations. |
| `skills/workflow/SKILL.md`, `skills/plan/SKILL.md`, `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, `skills/verify/SKILL.md`, `skills/pr/SKILL.md`, `skills/learn/SKILL.md` | Added or aligned required core sections, local handoff guidance, claims-not-owned sections, progress/readiness/closeout wording where relevant, compact result output, copied public evidence-reading guidance, and removal of maintainer-only generated-output mechanics. | Implements the approved first-slice normalization while preserving local stage behavior and keeping shipped skill text user-facing. | Spec R3-R13, R16, R18; public-surface learn session | `python scripts/validate-skills.py`; `python scripts/test-skill-validator.py`. |
| `.codex/skills/<skill>/SKILL.md` for the seven first-slice skills | Regenerated local Codex runtime mirrors from canonical skills. | Keeps local generated output derived from authored skill source. | Spec R2-R2d | `python scripts/build-skills.py --check`; `cmp` checks during code-review M4. |
| `dist/adapters/{codex,claude,opencode}/.../<skill>/SKILL.md` for the seven first-slice skills | Regenerated public adapter skill copies from canonical skills. | Keeps adapter packages aligned with the normalized first-slice guidance. | Spec R2-R2d, test spec T9 | `python scripts/build-adapters.py --version 0.1.1 --check`; `python scripts/validate-adapters.py --version 0.1.1`; adapter fixtures. |
| `docs/plans/2026-05-08-skill-contract-optimization.md`, `docs/plan.md` | Added and maintained the active execution plan, milestone state, validation notes, current handoff, and lifecycle closeout gates. | Keeps plan index and plan body synchronized through milestone implementation and review. | Plan policy; workflow lifecycle rules | Selected CI and lifecycle validation. |
| `docs/changes/2026-05-08-skill-contract-optimization/*` | Added change metadata, review records, review-resolution closeout, and this explanation. | Provides durable traceability for proposal decisions, review findings, validation, and final rationale. | Workflow baseline change-local pack | Change metadata validation and review artifact closeout. |

## Tests Added Or Changed

- `specs/skill-contract.test.md` adds T1-T14 to cover the normative source split, required and conditional sections, first-slice scope, claim boundaries, result blocks, readiness wording, shared blocks, public skill surface cleanup, generated output, overclaim validation, minimum viable skill guidance, compatibility, and final closeout.
- `scripts/test-skill-validator.py` adds static checks for the approved contract. The checks intentionally use bounded evidence, including exact backticked first-slice skill names and canonical skill paths, instead of broad prose scoring.
- `scripts/test-skill-validator.py` also checks that copied public shared blocks match their canonical `templates/shared/` sources and that no unused generated-output handling shared block remains.
- Existing generated-output and adapter validation scripts prove derived outputs match canonical skills.
- No runtime tests, workflow simulator, broad natural-language quality scoring, standalone `review-resolution` skill, or `skills/ci-maintenance/SKILL.md` path were added.

## Verification Evidence

Implementation evidence is recorded in the active plan and `change.yaml`. Key validation before this explanation artifact was added:

- `python scripts/validate-skills.py` passed after M3 normalization.
- `python scripts/test-skill-validator.py` passed after M3 with 42 tests.
- `python scripts/test-skill-validator.py` passed after public-surface cleanup with 43 tests.
- `python scripts/build-skills.py --check` passed after M4 regeneration.
- `python scripts/build-adapters.py --version 0.1.1 --check` passed after M4 regeneration.
- `python scripts/validate-adapters.py --version 0.1.1` passed after M4 regeneration.
- `python scripts/test-adapter-distribution.py` passed after M4 with 56 tests.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-skill-contract-optimization` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-08-skill-contract-optimization/change.yaml` passed.
- `bash scripts/ci.sh --mode explicit ...` over the full branch changed-path set passed selected checks: `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- `git diff --check b8f64359a4d7642ef62ffc467c5c9c071ffcf871..HEAD` passed.

Hosted CI was not observed locally, so this artifact does not claim hosted CI passed. Broad smoke was not run because the selector, plan, test spec, review-resolution, and release metadata did not trigger it.

## Review Resolution Summary

Material findings are closed in [review-resolution.md](review-resolution.md).

Counts:

- Findings resolved: 8
- Accepted findings: 8
- Unresolved findings: 0
- `needs-decision` findings: 0

Proposal-review R1 findings SCO1, SCO2, SCO3, SCO4, SCO6, SCO7, and SCO8 were accepted and resolved before downstream proposal reliance. Code-review R1 finding CR1-F1 was accepted, fixed, and closed by code-review R2.

## Alternatives Rejected

- Do not normalize every skill in this first slice. The accepted proposal and spec limit implementation to seven high-risk lifecycle skills and defer other skills by phase.
- Do not add a standalone `review-resolution` skill. The current change keeps review-resolution behavior in workflow/spec guidance and review artifacts.
- Do not add `skills/ci-maintenance/SKILL.md`. The visible stage label remains `ci-maintenance`, while the existing `ci` skill remains the entrypoint.
- Do not generate shared blocks into skills in v1. Shared blocks are copied into consuming skills and checked for drift.
- Do not copy maintainer-only generated-output handling into published skills. That guidance remains in contributor and governance surfaces.
- Do not add broad semantic quality scoring. Validator coverage stays static, narrow, and incident-based.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output. Generated files were refreshed from canonical skill source.

## Scope Control

The change preserves these non-goals:

- no lifecycle stage-order change;
- no replacement of `specs/rigorloop-workflow.md`;
- no all-skill normalization;
- no runtime architecture, storage, API, deployment, or schema change;
- no broad smoke requirement unless selected by the repository validation contract;
- no Phase 2, Phase 3, or Phase 4 skill normalization.

## Risks and Follow-ups

- PR #34 is opened for this change. Hosted CI status was not observed locally before handoff.
- Later phases still need separate proposals or plans to normalize `proposal`, `proposal-review`, `spec`, `spec-review`, `architecture`, `architecture-review`, `plan-review`, `test-spec`, `explain-change`, `ci`, and the later on-demand skills.
- Shared-block scope should stay conservative. More shared blocks should be added only after their wording stabilizes enough to justify drift checks.
- Future skill changes should preserve the public-surface boundary: published skills explain how to operate the skill, while repository-maintainer source, generation, adapter, selector-path, drift-check, and shared-block mechanics stay in contributor surfaces.

## PR Handoff Summary

- Source artifacts are present: accepted proposal, approved spec, active test spec, active plan, closed review-resolution, and this explanation.
- Implementation milestones M1-M4 are closed after code-review.
- Final verify rerun passed after this explanation artifact existed in the change-local pack.
- PR readiness: PR #34 is opened from the verified branch state; hosted CI remains the external reviewer-visible check.
