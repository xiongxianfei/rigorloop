# Code Review R4

Review ID: code-review-r4
Stage: code-review
Round: 4
Reviewer: Codex code-review
Target: M3 canonical skill and public skill portability alignment
Status: changes-requested

## Review inputs

- Review surface: M3 canonical skill changes under `skills/`, public skill generated copies under `.codex/skills/` and `dist/adapters/`, `scripts/test-skill-validator.py`, `scripts/test-select-validation.py`, `docs/plan.md`, `docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md`, and `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`.
- Tracked governing branch state: the existing tracked governance, spec, test-spec, architecture, skill, and validator files are present in Git. The active plan and change-local pack are local review-surface artifacts for this in-flight initiative; this review does not claim branch-ready or PR-ready state.
- Spec: `specs/rigorloop-workflow.md`, `specs/workflow-stage-autoprogression.md`, `specs/milestone-aware-review-handoff.md`, and `specs/skill-contract.md`.
- Test spec: `specs/rigorloop-workflow.test.md`, `specs/workflow-stage-autoprogression.test.md`, `specs/milestone-aware-review-handoff.test.md`, and `specs/skill-contract.test.md`.
- Plan milestone: M3 in `docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md`.
- Architecture / ADR: `docs/architecture/system/architecture.md`, approved by `architecture-review-r1`. M3 changes public workflow skill text and static checks only; it does not change runtime, storage, deployment, or system boundaries.
- Validation evidence inspected: `python scripts/validate-skills.py`, `python scripts/test-skill-validator.py`, `python scripts/test-select-validation.py`, retired-route scan, selected validation routing, selected CI, change-metadata validation, diff check, and whitespace scan recorded in the active plan and change metadata. During review, `python scripts/validate-skills.py`, `python scripts/test-skill-validator.py`, `python scripts/test-select-validation.py`, the retired-route scan, and selected CI for M3 paths passed.

## Diff summary

M3 updates canonical shipped skill text to replace lane-selection wording with standard workflow and isolated manual invocation guidance, make validation-command wording project-portable, and move public skill handoff language toward final closeout ordering. `scripts/test-skill-validator.py` adds case-insensitive retired-route checks over public workflow and shipped skill surfaces plus a published-skill portability check for repository-internal paths and maintainer-only mechanics. `scripts/test-select-validation.py` now expects project-portable validation selector and broad-validation wording.

## Findings

### CR2 - Code-review Handoff still routes final implementation closeout directly to verify

Finding ID: CR2
Severity: major

Evidence: The canonical `code-review` skill Handoff section still lists the final clean implementation path as direct `verify`: `Conditional next stages: ... \`verify\` only after the final in-scope implementation milestone is cleanly reviewed` (`skills/code-review/SKILL.md:49`-`52`). The generated Codex mirror and public adapter skill copies preserve the same stale line (`.codex/skills/code-review/SKILL.md:49`-`52`, `dist/adapters/codex/.agents/skills/code-review/SKILL.md:49`-`52`, `dist/adapters/claude/.claude/skills/code-review/SKILL.md:48`-`51`, and `dist/adapters/opencode/.opencode/skills/code-review/SKILL.md:48`-`51`). The same canonical file later states the correct final milestone handoff as `ci-maintenance` when triggered, otherwise `explain-change` (`skills/code-review/SKILL.md:233`-`241`), so the shipped skill is internally inconsistent.

Required outcome: Public `code-review` skill text must not preserve direct final-milestone-to-`verify` routing. The top-level Handoff section must route a clean final implementation milestone to final closeout: `ci-maintenance` when triggered, otherwise `explain-change`, then `verify`, then `pr`, subject to no open implementation milestones or required review-resolution.

Safe resolution: Update canonical `skills/code-review/SKILL.md`, refresh generated skill and adapter copies if they remain in the reviewed surface, and extend static checks so the phrase pattern around `` `verify` only after the final in-scope implementation milestone`` cannot return.

### CR3 - Verify skill still describes verification before explanation

Finding ID: CR3
Severity: major

Evidence: The canonical `verify` skill description says verification runs before "explanation or PR" (`skills/verify/SKILL.md:1`-`4`), and the purpose says the workflow moves from verify "toward explanation and PR" (`skills/verify/SKILL.md:16`-`18`). The generated Codex mirror carries the same stale wording (`.codex/skills/verify/SKILL.md:1`-`18`), as do the public adapter skill copies (`dist/adapters/codex/.agents/skills/verify/SKILL.md:1`-`18`, `dist/adapters/claude/.claude/skills/verify/SKILL.md:1`-`17`, and `dist/adapters/opencode/.opencode/skills/verify/SKILL.md:1`-`17`). This contradicts the approved final sequence where `explain-change` runs before final `verify`, and it weakens the M3 claim that shipped skills are aligned to the explain-before-verify order.

Required outcome: Public `verify` skill text must describe final verify as running after durable `explain-change` rationale exists and before `pr`, while preserving isolated direct `verify` behavior.

Safe resolution: Update canonical `skills/verify/SKILL.md`, refresh generated skill and adapter copies if they remain in the reviewed surface, and extend static wording checks to reject stale verify-before-explanation wording such as "before explanation or PR" and "toward explanation and PR".

## Checklist coverage

| Dimension | Result | Notes |
| --- | --- | --- |
| Spec alignment | concern | M3 aligns many shipped skill surfaces, but CR2 and CR3 preserve stale final-closeout ordering in `code-review` and `verify`. |
| Test coverage | concern | `python scripts/test-skill-validator.py` passes, but CR2 and CR3 show the static checks do not yet catch these stale phrases. |
| Edge cases | concern | Isolated direct `verify` remains valid, but public workflow-managed final closeout wording is inconsistent in the shipped `verify` and `code-review` skills. |
| Error handling | pass | The new public-skill portability check is narrow and does not overblock internal specs, plans, tests, generator scripts, or contributor docs. |
| Architecture boundaries | pass | M3 changes public skill text and static proof only; it does not change runtime architecture boundaries. |
| Compatibility | concern | Stale top-level skill descriptions and Handoff text can route future agents to the retired direct-verify closeout behavior. |
| Security/privacy | pass | The reviewed diff changes Markdown skill guidance and local validation tests only; no secrets, credentials, auth, or privacy-sensitive paths are introduced. |
| Derived artifact currency | concern | Generated Codex and adapter skill copies currently mirror the same stale CR2 and CR3 wording; drift checks pass because the generated output matches the canonical bug. |
| Unrelated changes | pass | The reviewed M3 slice is limited to canonical skill wording, static wording checks, selector fixture wording, and lifecycle handoff records. |
| Validation evidence | concern | M3 validation is current and passes, but the passing static proof missed CR2 and CR3, so additional phrase checks are needed. |

## Review outcome

Verdict: changes-requested.

Material findings: CR2, CR3.

No branch-ready, PR-ready, verification-passed, or final-closeout claim is made.

Recommended next stage: `review-resolution M3`, then rerun `code-review M3` after CR2 and CR3 are fixed and selected validation is current.
