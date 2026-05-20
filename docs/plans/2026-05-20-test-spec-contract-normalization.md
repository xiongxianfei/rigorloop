# Test-Spec Contract Normalization Plan

## Status

- active
- Owner: maintainers
- Start date: 2026-05-20
- Last updated: 2026-05-20
- Related proposal: [Test-Spec Contract Normalization](../proposals/2026-05-20-test-spec-contract-normalization.md)
- Related spec: [Skill Contract](../../specs/skill-contract.md)
- Change root: [docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml](../changes/2026-05-20-test-spec-contract-normalization/change.yaml)
- Supersedes: none

## Purpose / big picture

Normalize `skills/test-spec/SKILL.md` to the published-skill design contract without changing what `test-spec` does. The plan closes the one discovered contract gap in the skill-contract spec, creates focused proof obligations in the matching test spec, then applies the smallest canonical skill change with preservation evidence and generated-output validation.

## Source artifacts

- Proposal: [Test-Spec Contract Normalization](../proposals/2026-05-20-test-spec-contract-normalization.md), accepted after [proposal-review-r2](../changes/2026-05-20-test-spec-contract-normalization/reviews/proposal-review-r2.md).
- Spec: [Skill Contract](../../specs/skill-contract.md), approved after [spec-review-r1](../changes/2026-05-20-test-spec-contract-normalization/reviews/spec-review-r1.md).
- Architecture: not required. This change affects contract Markdown, test-spec proof planning, one canonical skill file, deterministic validation, change-local evidence, and generated adapter validation. It does not add runtime components, persistence, APIs, deployment boundaries, or data-flow decisions.
- Test spec: focused proof coverage T37 through T40 in [Skill Contract Test Spec](../../specs/skill-contract.test.md), owner-approved on 2026-05-20.
- Project map: [RigorLoop Project Map](../project-map.md), available as orientation only.

## Context and orientation

- `skills/` is the only authored skill source.
- `skills/test-spec/SKILL.md` currently lacks `version`, `schema-version`, `Workflow role`, and `Output skeleton`; its stop conditions are Rules items rather than a visible boundary.
- `skills/spec/SKILL.md` and `skills/spec-review/SKILL.md` already have the contract-required metadata, Workflow role, and output skeletons and are out of scope.
- The approved spec amendment added `R29g`, `R29h`, `R31e`, and `R34c` for frontmatter metadata, spec-family schema version, visible stop conditions, and output-skeleton preservation proof.
- The default proof route is not plan-only. A focused test-spec amendment is required before implementation unless a later approved artifact changes that route.
- Current generated adapter output must be rebuilt or validated from canonical `skills/`, unless a reviewed plan update records an explicit deferral with rationale.

## Non-goals

- Do not change `test-spec` routing description behavior.
- Do not change any normative rule, coverage rule, stop condition, or output obligation in `test-spec`.
- Do not tabulate `test-spec` required-section prose or fence enums.
- Do not edit `spec` or `spec-review`.
- Do not introduce packaged `assets/`, `references/`, or `scripts/`.
- Do not retroactively rewrite legacy adapter archives.
- Do not hand-edit generated adapter skill bodies.
- Do not claim implementation, review, verify, branch, or PR readiness from this plan.

## Requirements covered

| Requirement | Planned coverage |
|---|---|
| `R29g` | M3 adds frontmatter `version` and `schema-version` to `skills/test-spec/SKILL.md`; M1 defines proof. |
| `R29h` | M3 uses `schema-version: skill-readability-v1`; M1 defines exact expected value unless a later approved contract supersedes it. |
| `R30`, `R30a` | M3 adds `Workflow role` for `test-spec`; M1 defines field-level proof. |
| `R31e` | M3 surfaces invocation-blocking conditions in a dedicated `Stop conditions` section; M1 defines preservation proof. |
| `R34`, `R34c` | M3 adds a fenced output skeleton and records preservation evidence for section set, test-case format, coverage obligations, and output obligations. |
| Accepted proposal invariant | M1 and M3 require behavior parity and a preservation matrix before code-review. |
| Generated-output boundary | M3 validates current generated output from canonical `skills/` or records an approved deferral. |

## Current Handoff Summary

- Current milestone: final closeout sequence
- Current milestone state: pending
- Last reviewed milestone: M3. Test-Spec Skill Normalization
- Review status: code-review M3 R1 clean-with-notes; no material findings
- Remaining in-scope implementation milestones: none
- Next stage: hosted CI and human review for PR #77
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation milestones, explain-change, verify, and PR handoff are closed, but hosted CI and human review remain incomplete.

## Milestones

### M1. Skill Contract Test-Spec Amendment

- Milestone state: closed
- Goal: define focused proof obligations for `test-spec` contract normalization before any skill-body implementation begins.
- Requirements: `R29g`, `R29h`, `R30`, `R30a`, `R31e`, `R34`, `R34c`
- Files/components likely touched:
  - `specs/skill-contract.test.md`
  - `docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml`
  - `docs/plans/2026-05-20-test-spec-contract-normalization.md`
- Dependencies:
  - plan-review approval for this plan
  - approved `specs/skill-contract.md`
- Tests to add/update:
  - Test-spec coverage for frontmatter `version` and `schema-version` on normalized `test-spec`.
  - Test-spec coverage for `Workflow role` fields.
  - Test-spec coverage for dedicated `Stop conditions` and source-to-destination preservation.
  - Test-spec coverage for output-skeleton fidelity and behavior parity on representative input.
  - Test-spec coverage for generated adapter validation or explicit deferral.
- Implementation steps:
  - Add a focused test case or proof section for the `test-spec` normalization slice.
  - Name the representative input used for behavior parity.
  - Name the preservation matrix as required implementation evidence.
  - Name generated-output validation commands or the required deferral record.
  - Keep proof obligations scoped to `test-spec`; do not reopen spec-family readability.
- Validation commands:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/plans/2026-05-20-test-spec-contract-normalization.md --path docs/plan.md --path docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml`
  - `git diff --check -- specs/skill-contract.test.md docs/plans/2026-05-20-test-spec-contract-normalization.md docs/plan.md docs/changes/2026-05-20-test-spec-contract-normalization`
  - `bash scripts/ci.sh --mode explicit --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/plans/2026-05-20-test-spec-contract-normalization.md --path docs/plan.md --path docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml`
- Expected observable result: test-spec proof obligations are active and sufficient for implementation without relying on chat-only preservation claims.
- Commit message: `M1: define test-spec normalization proof obligations`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - M1 could broaden into family-wide readability proof.
- Rollback/recovery:
  - Revert the focused test-spec amendment and revise the plan if proof obligations reveal a broader contract gap.

### M2. Validator And Fixture Support

- Milestone state: closed
- Goal: add or confirm deterministic validation support for the new `test-spec` normalization proof obligations.
- Requirements: `R29g`, `R29h`, `R30`, `R30a`, `R31e`, `R34c`
- Files/components likely touched:
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/skills/`
  - `docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml`
  - `docs/plans/2026-05-20-test-spec-contract-normalization.md`
- Dependencies:
  - M1 closed, or M1 explicitly records that no validator change is needed.
- Tests to add/update:
  - Focused validator regressions for frontmatter metadata and spec-family schema value if not already covered.
  - Focused validator or fixture checks for Workflow role and output skeleton if existing coverage does not select `test-spec`.
  - No broad natural-language scoring.
- Implementation steps:
  - Inspect existing validator behavior against M1 proof obligations.
  - Add the narrowest deterministic tests needed for missing checks.
  - Avoid turning preservation or behavior parity into broad semantic scoring.
  - Record no-change rationale if existing validators are sufficient and only manual/change-local evidence is required.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml`
  - `git diff --check -- scripts tests docs/plans/2026-05-20-test-spec-contract-normalization.md docs/changes/2026-05-20-test-spec-contract-normalization`
  - `bash scripts/ci.sh --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path docs/plans/2026-05-20-test-spec-contract-normalization.md --path docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml`
- Expected observable result: deterministic proof can catch missing metadata or structural contract gaps where repository validation owns the check.
- Implementation result: added focused negative validator fixtures and regression tests for missing readability `version`, invalid `schema-version`, missing `Workflow role` field, and output skeleton without placeholders. Existing validator logic already enforced these structural checks, so no `scripts/skill_validation.py` change was needed.
- Commit message: `M2: validate test-spec normalization contract checks`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Validator changes could overfit prose or block unrelated skill wording.
- Rollback/recovery:
  - Revert validator changes and keep M1 manual proof obligations if deterministic validation is too brittle.

### M3. Test-Spec Skill Normalization

- Milestone state: closed
- Goal: normalize `skills/test-spec/SKILL.md` to the approved contract while preserving output behavior.
- Requirements: `R29g`, `R29h`, `R30`, `R30a`, `R31e`, `R34`, `R34c`
- Files/components likely touched:
  - `skills/test-spec/SKILL.md`
  - `docs/changes/2026-05-20-test-spec-contract-normalization/behavior-preservation.md`
  - `docs/changes/2026-05-20-test-spec-contract-normalization/behavior-parity.md`
  - `docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml`
  - generated output only when repository-owned commands require it
- Dependencies:
  - M1 closed
  - M2 closed or recorded as no validator changes needed
  - plan-review approval
- Tests to add/update:
  - Update focused validator tests if M2 required them.
  - Record behavior-preservation matrix for moved stop conditions and skeletonized output obligations.
  - Record behavior-parity comparison for the representative input named in M1.
- Implementation steps:
  - Add `version: "1.0.0"` and `schema-version: skill-readability-v1`.
  - Add `Workflow role` with role, stage, upstream, downstream, summary, and must-not-claim boundaries.
  - Add dedicated `Stop conditions` before normal artifact-generation procedure.
  - Add a compact fenced output skeleton that preserves the existing required sections, test-case format, and coverage maps.
  - Keep routing description unchanged unless validation proves a contract failure.
  - Record behavior-preservation and behavior-parity evidence before code-review.
  - Rebuild or validate generated output from canonical `skills/`, or record a reviewed deferral with rationale.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version v0.1.5 --check`
  - `python scripts/validate-adapters.py --version v0.1.5`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/plans/2026-05-20-test-spec-contract-normalization.md --path docs/plan.md --path docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml`
  - `git diff --check -- skills/test-spec/SKILL.md specs/skill-contract.md specs/skill-contract.test.md docs/plans/2026-05-20-test-spec-contract-normalization.md docs/plan.md docs/changes/2026-05-20-test-spec-contract-normalization`
  - `bash scripts/ci.sh --mode explicit --path skills/test-spec/SKILL.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/plans/2026-05-20-test-spec-contract-normalization.md --path docs/plan.md --path docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml`
- Expected observable result: `test-spec` has contract metadata, Workflow role, visible stop conditions, and a fenced output skeleton while producing the same test spec structure on representative input.
- Implementation result: normalized `skills/test-spec/SKILL.md`, recorded preservation and parity evidence, and validated temporary `v0.1.5` adapter archives from canonical `skills/`.
- Commit message: `M3: normalize test-spec skill contract structure`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Skeleton wording could imply new required sections or coverage obligations.
  - Stop-condition wording could add or weaken a blocker.
  - Generated-output checks could reveal stale baseline debt.
- Rollback/recovery:
  - Revert `skills/test-spec/SKILL.md` and generated output changes; keep M1/M2 proof artifacts for a narrower rewrite.

## Validation plan

- Use the smallest direct command first for each milestone, then selected CI for changed supported paths.
- Use `python scripts/validate-artifact-lifecycle.py --mode explicit-paths` for touched lifecycle artifacts.
- Use `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-test-spec-contract-normalization` after review records change.
- Use `python scripts/validate-change-metadata.py docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml` whenever change metadata changes.
- Use `python scripts/validate-skills.py` and `python scripts/test-skill-validator.py` before code-review for skill or validator changes.
- Use `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version v0.1.5 --check`, and `python scripts/validate-adapters.py --version v0.1.5` for current generated-output proof, unless a reviewed plan update explicitly defers generated output with rationale.
- Run broad smoke only if selector output, active test spec, review-resolution, release metadata, or a reviewer explicitly requires it.

## Risks and recovery

- Risk: scope creeps into spec-family readability.
  - Recovery: stop and route readability work to the separate follow-on proposal; only `test-spec` contract normalization is in scope.
- Risk: proof route becomes ambiguous during implementation.
  - Recovery: return to M1 and update the test spec before skill changes proceed.
- Risk: behavior parity cannot be demonstrated cleanly.
  - Recovery: keep `test-spec` unchanged and revise the skeleton or stop-condition wording before code-review.
- Risk: generated adapter validation is stale for unrelated reasons.
  - Recovery: record the exact drift and either fix in scope when caused by this change or request owner decision for an explicit deferral.

## Dependencies

- Plan-review must approve this plan before M1 starts.
- M1 test-spec amendment must be approved or owner-accepted before M2 or M3 implementation work relies on it.
- M2 must either close or record no validator changes needed before M3.
- Code-review must inspect M3 preservation and behavior-parity evidence before final closeout.
- Explain-change, verify, and PR handoff remain downstream gates after all implementation milestones close.

## Progress

- 2026-05-20: Created active plan after proposal acceptance and clean spec-review.
- 2026-05-20: Plan-review R1 approved the plan with no material findings.
- 2026-05-20: Closed M1 by adding focused proof coverage T37 through T40 to `specs/skill-contract.test.md`.
- 2026-05-20: Owner approved the focused test-spec amendment and cleared M2 to start.
- 2026-05-20: Started M2 validator and fixture support.
- 2026-05-20: Added M2 validator regression tests and fixtures; existing validator logic was sufficient, so M2 is ready for code-review.
- 2026-05-20: Code-review M2 R1 returned clean-with-notes with no material findings; M2 closed and M3 is next.
- 2026-05-20: Started M3 test-spec skill normalization.
- 2026-05-20: Normalized `skills/test-spec/SKILL.md`, recorded behavior preservation and parity evidence, and set M3 to review-requested.
- 2026-05-20: Code-review M3 R1 returned clean-with-notes with no material findings; M3 closed and all implementation milestones are complete.
- 2026-05-20: Recorded durable explain-change rationale and advanced the handoff to verify.
- 2026-05-20: Final local verification passed with a documented adapter expanded-tree warning; branch is ready for PR handoff.
- 2026-05-20: Opened PR #77 for human review.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-20 | Use a three-milestone sequence: proof planning, validator support, skill normalization. | Keeps implementation blocked until proof obligations are approved and validation needs are known. | Implement `test-spec` immediately after spec-review. |
| 2026-05-20 | Treat architecture as not required. | The change affects Markdown contracts, proof planning, one skill, validators, and generated-output validation without new runtime or data-flow boundaries. | Create an architecture artifact for a single skill-contract normalization. |
| 2026-05-20 | Keep generated-output proof in M3. | Generated output must reflect canonical skill changes, but only after the canonical skill changes exist. | Validate generated output before any canonical skill change. |
| 2026-05-20 | Use T37 through T40 as the focused test-spec normalization proof plan. | The active skill-contract test spec already owns skill-contract proof and can add the narrow normalization slice without creating a competing test-spec surface. | Create a separate one-off test spec file. |
| 2026-05-20 | Leave `scripts/skill_validation.py` unchanged in M2. | Existing readability contract logic already enforces `version`, `schema-version`, required `Workflow role` fields, and output-skeleton fenced placeholders; M2 only needed focused regression fixtures. | Add duplicate validator logic for the `test-spec` slice. |

## Surprises and discoveries

- Existing `specs/skill-contract.md` already covered Workflow role and output skeletons but did not explicitly require `version` and `schema-version`, so the spec amendment route was required before planning.
- Existing readability validation already covered M2's machine-checkable structure; the missing piece was regression coverage for metadata and field-level failure cases.
- Tracked `dist/adapters` expanded-tree validation for `v0.1.5` is baseline-stale because release archives, not expanded generated public adapter skill bodies, are the current generated public surface. M3 used temporary adapter archive generation plus `validate-adapters --root` for current generated-output proof.

## Validation notes

- Plan-review R1 approved the plan with no material findings.
- M1 validation passed with artifact lifecycle validation, change metadata validation, whitespace check, and selected CI for the focused test-spec amendment.
- Focused test-spec amendment owner approval recorded on 2026-05-20.
- M2 validation passed:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
- Code-review M2 R1 recorded clean-with-notes and closed M2.
- M3 validation passed:
  - `python scripts/validate-skills.py skills/test-spec/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/tmp.NBI6tpmMoX`
  - `python scripts/validate-adapters.py --root /tmp/tmp.NBI6tpmMoX --version v0.1.5`
- M3 tracked adapter-tree check result:
  - `python scripts/build-adapters.py --version v0.1.5 --check` failed against baseline expanded-tree adapter output; see Surprises and discoveries.
- Code-review M3 R1 recorded clean-with-notes and closed M3.
- Explain-change recorded at `docs/changes/2026-05-20-test-spec-contract-normalization/explain-change.md`.
- Verify recorded at `docs/changes/2026-05-20-test-spec-contract-normalization/verify-report.md`; local validation passed and hosted CI was not observed.
- PR opened: [PR #77](https://github.com/xiongxianfei/rigorloop/pull/77).

## Outcome and retrospective

- Pending completion.

## Readiness

- See `Current Handoff Summary`.
- PR opened as [PR #77](https://github.com/xiongxianfei/rigorloop/pull/77); hosted CI and human review remain pending.
