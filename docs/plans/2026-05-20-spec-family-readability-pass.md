# Spec-Family Readability Pass Plan

## Status

- active
- Owner: maintainers
- Start date: 2026-05-20
- Last updated: 2026-05-20
- Related proposal: [Spec-Family Readability Pass](../proposals/2026-05-20-spec-family-readability-pass.md)
- Related spec: [Spec-Family Readability Pass](../../specs/spec-family-readability-pass.md)
- Change root: [docs/changes/2026-05-20-spec-family-readability-pass/change.yaml](../changes/2026-05-20-spec-family-readability-pass/change.yaml)
- Supersedes: none

## Purpose / big picture

Apply a presentation-only readability pass to the three spec-family skills, `spec`, `spec-review`, and `test-spec`, after `test-spec` contract normalization. The work tabulates long enumerations, creates authoritative closed-enum surfaces, aligns family section order where behavior clarity allows, and records deterministic proof that no rule, stop condition, lifecycle boundary, routing behavior, output obligation, or produced-artifact shape changed.

## Source artifacts

- Proposal: [Spec-Family Readability Pass](../proposals/2026-05-20-spec-family-readability-pass.md), accepted after [proposal-review-r2](../changes/2026-05-20-spec-family-readability-pass/reviews/proposal-review-r2.md).
- Spec: [Spec-Family Readability Pass](../../specs/spec-family-readability-pass.md), approved after [spec-review-r1](../changes/2026-05-20-spec-family-readability-pass/reviews/spec-review-r1.md).
- Architecture: not required. The change is Markdown-only skill text plus proof artifacts and generated-output validation. It does not add runtime components, persistence, APIs, deployment boundaries, security boundaries, or data flow.
- Test spec: [Spec-Family Readability Pass Test Spec](../../specs/spec-family-readability-pass.test.md), active proof surface for implementation; owner approved on 2026-05-20.
- Project map: not required; affected authored surfaces are explicitly named by the spec.

## Context and orientation

- `skills/` is the only authored skill source.
- Generated adapter skill bodies are derived output and must not be hand-edited.
- `skills/spec/SKILL.md`, `skills/spec-review/SKILL.md`, and `skills/test-spec/SKILL.md` are the only in-scope skill bodies.
- The accepted proposal and approved spec classify produced-artifact readability, packaged resources, routing-description changes, build-time partials, and generated public adapter skill-body hand edits as out of scope.
- `test-spec` normalization baseline is present on this branch:
  - `skills/test-spec/SKILL.md` has `version: "1.0.0"` and `schema-version: skill-readability-v1`;
  - `skills/test-spec/SKILL.md` has `## Workflow role`;
  - `skills/test-spec/SKILL.md` has `## Stop conditions`;
  - `skills/test-spec/SKILL.md` has `## Output skeleton`;
  - normalization behavior-preservation and behavior-parity evidence exists under `docs/changes/2026-05-20-test-spec-contract-normalization/`, with clean M3 code-review evidence.
- `docs/plan.md` still lists the predecessor normalization plan as active on this branch because its final closeout is tracked separately. This plan does not rewrite that unrelated lifecycle state.

## Non-goals

- Do not change produced spec, spec-review, or test-spec artifact readability.
- Do not change routing descriptions.
- Do not change workflow stage order or lifecycle state semantics.
- Do not introduce packaged `assets/`, `references/`, or `scripts/`.
- Do not introduce build-time partials or duplicated-block authoring mechanisms.
- Do not hand-edit generated public adapter skill bodies.
- Do not retroactively rewrite legacy adapter archives.
- Do not claim implementation, code review, final verification, branch readiness, PR readiness, or Done from this plan.

## Requirements covered

| Requirement | Planned coverage |
|---|---|
| `SFRP-R1` | M1 through M3 edit only canonical spec-family skill files plus change-local proof, plan, review, and metadata artifacts. |
| `SFRP-R2` | Every milestone records content-preservation evidence before code-review. |
| `SFRP-R3` | Milestones explicitly avoid produced-artifact output shape changes and compare output skeleton obligations. |
| `SFRP-R4` | All milestones exclude routing, packaging, partials, and generated body hand edits. |
| `SFRP-R5`, `SFRP-R6` | Plan records the normalized `test-spec` baseline gate in Context before implementation starts. |
| `SFRP-R7` | M1 tabulates `spec` required-section prose; M3 tabulates `test-spec` required-section prose. |
| `SFRP-R8` | M2 tabulates `spec-review` review-dimension guidance. |
| `SFRP-R9` | M3 tabulates `test-spec` coverage expectations where it improves scanning without changing obligations. |
| `SFRP-R10` through `SFRP-R14` | Each implementation milestone records enum authority evidence for changed enum surfaces. |
| `SFRP-R15` through `SFRP-R18` | Each milestone applies family ordering as best effort and records any section-order exception. |
| `SFRP-R19`, `SFRP-R20` | Each milestone records a content-preservation matrix. |
| `SFRP-R21` through `SFRP-R23` | Each milestone records representative behavior-parity classification for its skill. |
| `SFRP-R24` | M3 validates current generated adapter output from canonical skills or records an explicit deferral. |
| `SFRP-R25` | M3 records cold-read notes across all three changed skills when practical; otherwise records why cold-read is deferred. |

## Current Handoff Summary

- Current milestone: M2. Spec-Review Skill Readability
- Current milestone state: review-requested
- Last reviewed milestone: M1. Spec Skill Readability
- Review status: `SFRP-M2-CR1` accepted and resolved; M2 fix ready for code-review rerun
- Remaining in-scope implementation milestones: M2, M3
- Next stage: code-review M2 rerun
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M2 rerun code-review, M3 implementation and code-review, explain-change, verify, and PR handoff remain open.

## Milestones

### M1. Spec Skill Readability

- Milestone state: closed
- Goal: make `skills/spec/SKILL.md` scannable by tabulating required-section guidance, fencing remaining closed enums, and aligning section order where behavior clarity allows.
- Requirements: `SFRP-R1`, `SFRP-R2`, `SFRP-R3`, `SFRP-R4`, `SFRP-R7`, `SFRP-R10` through `SFRP-R23`
- Files/components likely touched:
  - `skills/spec/SKILL.md`
  - `scripts/test-skill-validator.py`
  - `docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md`
  - `docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`
  - `docs/changes/2026-05-20-spec-family-readability-pass/change.yaml`
  - this plan
- Dependencies:
  - plan-review approval
  - approved test spec for this plan
- Tests to add/update:
  - Enum authority evidence for `spec` settlement/status-related closed enums changed by the milestone.
  - Content-preservation matrix for tabulated required-section guidance and any moved sections.
  - Representative behavior-parity classification for `spec`.
  - Skill-validator regression fixture alignment when selected CI requires it for the new enum-authority shape.
- Implementation steps:
  - Identify current required-section prose and any narrated closed enum values in `skills/spec/SKILL.md`.
  - Convert required-section prose to a table without adding, removing, or changing section obligations.
  - Create or designate one authoritative closed-enum surface per changed enum.
  - Apply shared section order only where it does not weaken status settlement, source-of-truth handling, output expectations, or handoff clarity.
  - Record preservation, enum authority, section-order exception, and behavior-parity evidence before code-review.
  - Align stale validation fixture expectations if they still require duplicate inline enum values.
- Validation commands:
  - `python scripts/validate-skills.py skills/spec/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-readability-pass/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-20-spec-family-readability-pass.md --path docs/plan.md --path specs/spec-family-readability-pass.md --path specs/spec-family-readability-pass.test.md --path docs/changes/2026-05-20-spec-family-readability-pass/change.yaml --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`
  - `git diff --check -- skills/spec/SKILL.md scripts/test-skill-validator.py docs/plans/2026-05-20-spec-family-readability-pass.md docs/plan.md specs/spec-family-readability-pass.md specs/spec-family-readability-pass.test.md docs/changes/2026-05-20-spec-family-readability-pass`
  - `bash scripts/ci.sh --mode explicit --path skills/spec/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-20-spec-family-readability-pass.md --path docs/plan.md --path specs/spec-family-readability-pass.md --path specs/spec-family-readability-pass.test.md --path docs/changes/2026-05-20-spec-family-readability-pass/change.yaml --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`
- Expected observable result: `spec` is easier to scan, with the same behavior, output skeleton, required sections, status settlement behavior, and handoff boundaries.
- Commit message: `M1: improve spec skill readability`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Required-section tabulation could accidentally change the spec artifact contract.
  - Enum fencing could duplicate an existing value list.
- Rollback/recovery:
  - Revert `skills/spec/SKILL.md` and M1 evidence, then re-plan a narrower table-only edit if needed.

### M2. Spec-Review Skill Readability

- Milestone state: review-requested
- Goal: make `skills/spec-review/SKILL.md` scannable by tabulating review dimensions, creating authoritative verdict enum surfaces, and preserving review-recording and material-finding behavior.
- Requirements: `SFRP-R1`, `SFRP-R2`, `SFRP-R3`, `SFRP-R4`, `SFRP-R8`, `SFRP-R10` through `SFRP-R23`
- Files/components likely touched:
  - `skills/spec-review/SKILL.md`
  - `docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md`
  - `docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`
  - `docs/changes/2026-05-20-spec-family-readability-pass/change.yaml`
  - this plan
- Dependencies:
  - M1 code-review closed or M1 removed by reviewed re-plan
- Tests to add/update:
  - Enum authority evidence for review-dimension verdict values.
  - Content-preservation matrix for review-dimension table rows and any moved review guidance.
  - Representative behavior-parity classification for `spec-review`.
- Implementation steps:
  - Identify current review dimensions and verdict guidance.
  - Convert review dimensions to a table while preserving dimension names and pass/concern/block interpretation.
  - Ensure formal review recording, material-finding requirements, eventual test-spec readiness, and stop-condition boundaries remain intact.
  - Avoid adding output-skeleton obligations beyond existing review result shape.
  - Record preservation, enum authority, section-order exception, and behavior-parity evidence before code-review.
- Validation commands:
  - `python scripts/validate-skills.py skills/spec-review/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-readability-pass/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-20-spec-family-readability-pass.md --path docs/plan.md --path specs/spec-family-readability-pass.md --path specs/spec-family-readability-pass.test.md --path docs/changes/2026-05-20-spec-family-readability-pass/change.yaml --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`
  - `git diff --check -- skills/spec-review/SKILL.md docs/plans/2026-05-20-spec-family-readability-pass.md docs/plan.md specs/spec-family-readability-pass.md specs/spec-family-readability-pass.test.md docs/changes/2026-05-20-spec-family-readability-pass`
  - `bash scripts/ci.sh --mode explicit --path skills/spec-review/SKILL.md --path docs/plans/2026-05-20-spec-family-readability-pass.md --path docs/plan.md --path specs/spec-family-readability-pass.md --path specs/spec-family-readability-pass.test.md --path docs/changes/2026-05-20-spec-family-readability-pass/change.yaml --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`
- Expected observable result: `spec-review` is easier to scan, with the same review verdicts, material-finding obligations, recording behavior, and result output shape.
- Commit message: `M2: improve spec-review skill readability`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Verdict enum fencing could weaken or duplicate review dimension semantics.
  - Section movement could hide recording obligations.
- Rollback/recovery:
  - Revert `skills/spec-review/SKILL.md` and M2 evidence, then re-plan a review-dimension-only edit if needed.

### M3. Test-Spec Skill Readability And Generated Output Proof

- Milestone state: planned
- Goal: make normalized `skills/test-spec/SKILL.md` scannable, preserve the normalized baseline, and validate current generated adapter output from canonical skills.
- Requirements: `SFRP-R1` through `SFRP-R25`
- Files/components likely touched:
  - `skills/test-spec/SKILL.md`
  - `docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md`
  - `docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`
  - `docs/changes/2026-05-20-spec-family-readability-pass/change.yaml`
  - this plan
- Dependencies:
  - M2 code-review closed or M2 removed by reviewed re-plan
  - normalized `test-spec` baseline remains present
- Tests to add/update:
  - Enum authority evidence for `test-spec` status values and any other changed closed enums.
  - Content-preservation matrix for required sections, coverage expectations, output skeleton references, and any moved sections.
  - Representative behavior-parity classification for `test-spec`.
  - Generated adapter output validation or explicit deferral evidence.
  - Cold-read notes across all three changed skills when practical.
- Implementation steps:
  - Confirm `test-spec` still has `version`, `schema-version`, Workflow role, Stop conditions, and Output skeleton before editing.
  - Convert required-section prose and coverage expectations to tables where scanning improves without changing obligations.
  - Create or designate one authoritative closed-enum surface per changed enum.
  - Preserve stop-condition visibility before normal output procedure.
  - Keep output skeleton artifact contract intact and avoid implying new produced-artifact obligations.
  - Record preservation, enum authority, section-order exception, behavior-parity, cold-read, and generated-output evidence before code-review.
- Validation commands:
  - `python scripts/validate-skills.py skills/test-spec/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version v0.1.5 --check`
  - `python scripts/validate-adapters.py --version v0.1.5`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-readability-pass/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-20-spec-family-readability-pass.md --path docs/plan.md --path specs/spec-family-readability-pass.md --path specs/spec-family-readability-pass.test.md --path docs/changes/2026-05-20-spec-family-readability-pass/change.yaml --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`
  - `git diff --check -- skills/spec/SKILL.md skills/spec-review/SKILL.md skills/test-spec/SKILL.md docs/plans/2026-05-20-spec-family-readability-pass.md docs/plan.md specs/spec-family-readability-pass.md specs/spec-family-readability-pass.test.md docs/changes/2026-05-20-spec-family-readability-pass`
  - `bash scripts/ci.sh --mode explicit --path skills/spec/SKILL.md --path skills/spec-review/SKILL.md --path skills/test-spec/SKILL.md --path docs/plans/2026-05-20-spec-family-readability-pass.md --path docs/plan.md --path specs/spec-family-readability-pass.md --path specs/spec-family-readability-pass.test.md --path docs/changes/2026-05-20-spec-family-readability-pass/change.yaml --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`
- Expected observable result: all three spec-family skills read consistently, `test-spec` remains contract-normalized, generated-output currency is proven or explicitly deferred, and no behavior or produced-artifact output obligation changes.
- Commit message: `M3: improve test-spec readability and validate generated output`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - `test-spec` required-section tables could drift from the output skeleton.
  - Adapter validation may expose baseline release archive layout issues unrelated to this proposal.
- Rollback/recovery:
  - Revert `skills/test-spec/SKILL.md` and M3 evidence; if adapter validation exposes unrelated baseline debt, record a deferral or separate follow-up rather than broadening this milestone.

## Validation plan

- Use direct skill validation after each skill-body edit.
- Use lifecycle validation for the plan, plan index, spec, test spec, and change-local proof artifacts whenever they change.
- Use review artifact validation after review records change.
- Use change metadata validation whenever `change.yaml` changes.
- Use selected CI for touched paths before each code-review handoff.
- Use generated-output validation in M3 from canonical skills, or record an explicit reviewed deferral with rationale.
- Run broad smoke only if selected CI, plan-review, code-review, or verify requires it.

## Risks and recovery

- Risk: a table rewords a rule or obligation.
  - Recovery: preserve source wording, record the source-to-destination proof, or defer the row if table form is unsafe.
- Risk: enum authority creates duplicate value lists.
  - Recovery: keep one authoritative block or table, replace later full lists with references or placeholders, and document duplicate handling.
- Risk: section-order alignment hides a lifecycle boundary.
  - Recovery: keep the safer placement and record a section-order exception.
- Risk: generated-output validation fails on existing archive-layout debt.
  - Recovery: distinguish current-output proof from retroactive archive rewriting and record a reviewed deferral or separate follow-up.
- Risk: the active predecessor plan in `docs/plan.md` causes lifecycle confusion.
  - Recovery: keep this plan's state scoped and do not rewrite the predecessor lifecycle state unless this branch takes ownership of that closeout.

## Dependencies

- Accepted proposal.
- Approved spec.
- Plan-review approval before implementation.
- Test spec after plan-review before implementation.
- Normalized `test-spec` baseline from PR #77.
- Repository-owned validation scripts and current adapter manifest/version value.

## Progress

- 2026-05-20: plan created; `specs/spec-family-readability-pass.md` settled to `approved` after clean spec-review R1.
- 2026-05-20: plan-review R1 approved the plan; `specs/spec-family-readability-pass.test.md` created as the active proof surface for implementation.
- 2026-05-20: owner approved the active test spec.
- 2026-05-20: M1 implementation started for `skills/spec/SKILL.md`; proof surfaces are being created before skill text edits.
- 2026-05-20: M1 selected CI exposed a stale downstream status-settlement fixture that required duplicate inline settlement-result values; the fixture is aligned to require the settlement result field without requiring the duplicate value list.
- 2026-05-20: M1 implementation completed and targeted validation passed; milestone is ready for code-review.
- 2026-05-20: code-review M1 R1 requested changes for `SFRP-M1-CR1`; the milestone is in resolution-needed state.
- 2026-05-20: implemented the `SFRP-M1-CR1` fixture fix; `spec` now asserts the `## Closed enums` settlement-result values while `architecture` and `plan` retain exact inline value-list coverage.
- 2026-05-20: code-review M1 R2 completed clean-with-notes; M1 is closed and the next stage is implement M2.
- 2026-05-20: M2 implementation started for `skills/spec-review/SKILL.md`; preservation and parity evidence are being updated before skill text edits.
- 2026-05-20: M2 implementation completed and targeted validation passed; milestone is ready for code-review.
- 2026-05-20: code-review M2 R1 requested changes for `SFRP-M2-CR1`; the milestone is in resolution-needed state.
- 2026-05-20: implemented the `SFRP-M2-CR1` source-preservation fix; the `spec-review` dimension table now contains only baseline dimensions and verdict placeholders, with non-baseline review-focus examples removed.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-20 | Use three implementation milestones, one per spec-family skill | The change touches three canonical skill bodies and needs per-skill preservation, parity, and review evidence. | One large implementation milestone |
| 2026-05-20 | Put generated-output validation in M3 | Current generated output can be validated after all canonical skill edits are present. | Validate generated output after each skill edit |
| 2026-05-20 | Do not close the predecessor active plan in this branch | The predecessor closeout is tracked separately and is not part of this readability proposal. | Rewrite unrelated lifecycle state while creating this plan |

## Surprises and discoveries

- The normalized `test-spec` baseline is present in canonical skill source and prior change evidence.
- `docs/plan.md` still lists the predecessor normalization plan as active on this branch; this plan records that as existing lifecycle state rather than changing it.
- M1 selected CI required a minimal regression fixture update in `scripts/test-skill-validator.py` because the prior assertion encoded the exact duplicate inline settlement enum that this proposal removes.

## Validation notes

- Plan-review validation passed before test-spec creation; see `change.yaml`.
- Test-spec lifecycle validation passed after creation; see `change.yaml`.
- Selected CI passed for the proposal, spec, active test spec, plan, plan index, change metadata, and review artifacts.
- M1 targeted validation passed:
  - `python scripts/validate-skills.py skills/spec/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-readability-pass/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-20-spec-family-readability-pass.md --path docs/plan.md --path specs/spec-family-readability-pass.md --path specs/spec-family-readability-pass.test.md --path docs/changes/2026-05-20-spec-family-readability-pass/change.yaml --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`
  - `git diff --check -- skills/spec/SKILL.md scripts/test-skill-validator.py docs/plans/2026-05-20-spec-family-readability-pass.md docs/plan.md specs/spec-family-readability-pass.md specs/spec-family-readability-pass.test.md docs/changes/2026-05-20-spec-family-readability-pass`
  - `bash scripts/ci.sh --mode explicit --path skills/spec/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-20-spec-family-readability-pass.md --path docs/plan.md --path specs/spec-family-readability-pass.md --path specs/spec-family-readability-pass.test.md --path docs/changes/2026-05-20-spec-family-readability-pass/change.yaml --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`
- `SFRP-M1-CR1` fix validation passed:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-readability-pass/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-20-spec-family-readability-pass.md --path docs/plan.md --path specs/spec-family-readability-pass.md --path specs/spec-family-readability-pass.test.md --path docs/changes/2026-05-20-spec-family-readability-pass/change.yaml --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md --path docs/changes/2026-05-20-spec-family-readability-pass/review-log.md --path docs/changes/2026-05-20-spec-family-readability-pass/review-resolution.md`
  - `git diff --check -- scripts/test-skill-validator.py docs/plans/2026-05-20-spec-family-readability-pass.md docs/plan.md docs/changes/2026-05-20-spec-family-readability-pass`
  - `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path docs/plans/2026-05-20-spec-family-readability-pass.md --path docs/plan.md --path specs/spec-family-readability-pass.md --path specs/spec-family-readability-pass.test.md --path docs/changes/2026-05-20-spec-family-readability-pass/change.yaml --path docs/changes/2026-05-20-spec-family-readability-pass/review-log.md --path docs/changes/2026-05-20-spec-family-readability-pass/review-resolution.md --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`
- M2 targeted validation passed:
  - `python scripts/validate-skills.py skills/spec-review/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-readability-pass/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-20-spec-family-readability-pass.md --path docs/plan.md --path specs/spec-family-readability-pass.md --path specs/spec-family-readability-pass.test.md --path docs/changes/2026-05-20-spec-family-readability-pass/change.yaml --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`
  - `git diff --check -- skills/spec-review/SKILL.md docs/plans/2026-05-20-spec-family-readability-pass.md docs/plan.md specs/spec-family-readability-pass.md specs/spec-family-readability-pass.test.md docs/changes/2026-05-20-spec-family-readability-pass`
  - `bash scripts/ci.sh --mode explicit --path skills/spec-review/SKILL.md --path docs/plans/2026-05-20-spec-family-readability-pass.md --path docs/plan.md --path specs/spec-family-readability-pass.md --path specs/spec-family-readability-pass.test.md --path docs/changes/2026-05-20-spec-family-readability-pass/change.yaml --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`
- Code-review M2 R1 recording validation passed:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-20-spec-family-readability-pass`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-readability-pass/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-20-spec-family-readability-pass.md --path docs/plan.md --path docs/changes/2026-05-20-spec-family-readability-pass/change.yaml --path docs/changes/2026-05-20-spec-family-readability-pass/review-log.md --path docs/changes/2026-05-20-spec-family-readability-pass/review-resolution.md --path docs/changes/2026-05-20-spec-family-readability-pass/reviews/code-review-m2-r1.md`
  - `git diff --check -- docs/plans/2026-05-20-spec-family-readability-pass.md docs/plan.md docs/changes/2026-05-20-spec-family-readability-pass`
  - `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-20-spec-family-readability-pass.md --path docs/plan.md --path docs/changes/2026-05-20-spec-family-readability-pass/change.yaml --path docs/changes/2026-05-20-spec-family-readability-pass/review-log.md --path docs/changes/2026-05-20-spec-family-readability-pass/review-resolution.md --path docs/changes/2026-05-20-spec-family-readability-pass/reviews/code-review-m2-r1.md`
- `SFRP-M2-CR1` fix validation passed:
  - `python scripts/validate-skills.py skills/spec-review/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-readability-pass`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-readability-pass/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-20-spec-family-readability-pass.md --path docs/plan.md --path specs/spec-family-readability-pass.md --path specs/spec-family-readability-pass.test.md --path docs/changes/2026-05-20-spec-family-readability-pass/change.yaml --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md --path docs/changes/2026-05-20-spec-family-readability-pass/review-log.md --path docs/changes/2026-05-20-spec-family-readability-pass/review-resolution.md`
  - `git diff --check -- skills/spec-review/SKILL.md docs/plans/2026-05-20-spec-family-readability-pass.md docs/plan.md docs/changes/2026-05-20-spec-family-readability-pass`
  - `bash scripts/ci.sh --mode explicit --path skills/spec-review/SKILL.md --path docs/plans/2026-05-20-spec-family-readability-pass.md --path docs/plan.md --path specs/spec-family-readability-pass.md --path specs/spec-family-readability-pass.test.md --path docs/changes/2026-05-20-spec-family-readability-pass/change.yaml --path docs/changes/2026-05-20-spec-family-readability-pass/review-log.md --path docs/changes/2026-05-20-spec-family-readability-pass/review-resolution.md --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`

## Outcome and retrospective

- To be filled after all milestones, explain-change, verify, and PR handoff are complete.

## Readiness

- See `Current Handoff Summary`.
- Ready for `code-review M2` rerun.
