# Review-Skill Family Consistency and Parser-Owned Finding Shape

- Status: active
- Owner: maintainer
- Start date: 2026-05-21
- Last updated: 2026-05-21
- Related proposal: `docs/proposals/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape.md`
- Related spec: `specs/review-skill-family-consistency-parser-owned-finding-shape.md`
- Supersedes: none

## Purpose / big picture

This plan sequences the approved review-skill family spec into reviewable implementation slices. The work makes `assets/material-finding.md` the copied starting structure for material review findings in `code-review`, `proposal-review`, and `spec-review`, adds per-skill result skeleton assets, and adds deterministic validation that keeps the copied finding shape aligned with the existing review-artifact parser contract.

The change is structural. It must preserve review behavior, status vocabularies, severity values, recording rules, lifecycle boundaries, stop conditions, and handoff behavior.

## Source artifacts

- Proposal: `docs/proposals/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape.md`
- Spec: `specs/review-skill-family-consistency-parser-owned-finding-shape.md`
- Architecture: not required; the change is limited to skill text/assets, deterministic validators/fixtures, generated-output proof, and lifecycle evidence. It does not introduce new runtime architecture, data flow, persistence, external services, security boundaries, or adapter install-root behavior.
- Test spec: `specs/review-skill-family-consistency-parser-owned-finding-shape.test.md`
- Review evidence: `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/reviews/spec-review-r2.md`
- Review log: `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/review-log.md`
- Review resolution: `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/review-resolution.md`

## Context and orientation

Canonical skill sources live under `skills/`; generated public adapter output must not be hand-edited. `proposal-review` already has `assets/material-finding.md` and `assets/review-result-skeleton.md`; this initiative must make those assets conform to the review-family contract rather than duplicating them. `spec-review` currently has `assets/review-finding.md` and `assets/review-result-skeleton.md`; the implementation must migrate the material-finding asset name and resource-map references to `assets/material-finding.md` if that remains the approved path. `code-review` currently has no review-family assets.

The review-artifact parser contract remains unchanged. The implementation must prove parser-owned finding identity structure, including `Finding ID:` presence, spelling, and non-blank value, without adding severity-enum validation.

## Non-goals

- Do not change review judgment, review dimensions, severity values, severity-enum behavior, review-status values, recording rules, isolation rules, stop conditions, lifecycle boundaries, or handoff behavior.
- Do not add packaged `references/`, packaged `scripts/`, build-time partials, shared result skeletons, row assets, adapter install-root changes, lockfile changes, CLI behavior changes, or unrelated assets.
- Do not modify `plan-review`, `architecture-review`, or future `*-review` skills in this slice.
- Do not hand-edit generated adapter output or retroactively rewrite historical adapter archives.

## Requirements covered

- RSF-R1 through RSF-R4: M2, M3, M4
- RSF-R5 through RSF-R15: M1, M2, M3, M4
- RSF-R16 through RSF-R21: M1, M2, M3, M4
- RSF-R22 through RSF-R26: M2, M3, M4
- RSF-R27 through RSF-R30: M2, M3, M4
- RSF-R31 through RSF-R34: M5
- RSF-R35 through RSF-R37: M5
- RSF-R38 through RSF-R39: M1 and M5
- RSF-R40: prerequisite before implementation begins
- RSF-R41 through RSF-R42: M1 stop-or-proceed assessment
- RSF-R43 through RSF-R45: M2, M3, M4, M5
- AC-RSF-001 through AC-RSF-020: M1 through M5, with test-spec approval before M1 implementation

## Current Handoff Summary

- Current milestone: M3. Proposal-review asset conformance
- Current milestone state: review-requested
- Last reviewed milestone: M2. Code-review assets
- Review status: M3 implementation ready for code-review
- Remaining in-scope implementation milestones: M3, M4, M5
- Next stage: code-review M3
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation milestones, code-review, review-resolution if triggered, explain-change, verify, and PR handoff are still outstanding.

## Milestones

### M1. Validator foundation and contract sufficiency assessment

- Milestone state: closed
- Goal: Add or update deterministic validation/fixtures for the review-family asset contract before skill edits rely on them, and record whether `specs/skill-contract.md` is sufficient.
- Requirements: RSF-R5 through RSF-R21, RSF-R38 through RSF-R42, AC-RSF-004 through AC-RSF-010, AC-RSF-020
- Files/components likely touched:
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `scripts/review_artifact_validation.py` only if existing parser-owned identity checks require fixture exposure without parser-contract changes
  - `scripts/validate-review-artifacts.py` fixtures or tests, if present
  - `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/`
- Dependencies:
  - Approved plan-review.
  - Approved matching test spec.
  - Confirmed no architecture package is required.
- Tests to add/update:
  - Asset inventory, resource-map `COPY`, asset metadata, placeholder policy, review-class asset boundary, parser-conformance, byte-identical parser-owned field block, representative valid fill, and invalid parser-owned identity fill checks.
  - Explicit proof that non-enum `Severity:` is not required to fail structure validation in this slice.
- Implementation steps:
  - Inspect current skill validator and review-artifact parser tests.
  - Add the smallest deterministic checks that prove the spec contract without broad semantic scoring.
  - Record the `specs/skill-contract.md` sufficiency assessment before skill edits proceed.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape`
  - `git diff --check --`
- Expected observable result: validators fail on missing/mis-mapped review-family assets, parser-owned field drift, invalid `Finding ID:` identity shapes, and review-policy leakage into assets without adding severity-enum validation.
- Result: Implemented. Added review-family validator fixture coverage and parser-owned material-finding fill tests. Recorded `specs/skill-contract.md` sufficiency in `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/skill-contract-sufficiency.md`.
- Commit message: `M1: add review-family asset validation foundation`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Accidentally expanding parser behavior into severity-enum validation.
  - Creating brittle semantic checks for review-policy leakage.
- Rollback/recovery:
  - Revert broad validator behavior and keep only deterministic checks tied to the approved parser-owned structure contract.

### M2. Code-review assets

- Milestone state: closed
- Goal: Add `code-review` material-finding and result-skeleton assets, resource-map entries, and preservation/parity evidence.
- Requirements: RSF-R1 through RSF-R30, RSF-R43, AC-RSF-001 through AC-RSF-013
- Files/components likely touched:
  - `skills/code-review/SKILL.md`
  - `skills/code-review/assets/material-finding.md`
  - `skills/code-review/assets/review-result-skeleton.md`
  - `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/`
- Dependencies:
  - M1 validation foundation closed.
- Tests to add/update:
  - Focused skill-validator coverage for `code-review` asset inventory, resource map, metadata, parser labels, and review-result status vocabulary.
  - Behavior-preservation and representative parity evidence for `code-review`.
- Implementation steps:
  - Extract only structural finding/result field shape into assets.
  - Keep review dimensions, severity enum, `clean-with-notes` status semantics, recording rules, isolation rules, and handoff behavior in `SKILL.md`.
  - Add resource-map `COPY` entries including literal `Finding ID:` confirmation before linking.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape`
  - `git diff --check --`
- Expected observable result: `code-review` has the two required assets, preserves `clean-with-notes | changes-requested | blocked | inconclusive`, and produces equivalent representative review behavior.
- Commit message: `M2: add code-review family assets`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Treating `code-review` result status as equivalent to proposal/spec `approved`.
- Rollback/recovery:
  - Reinline the extracted `code-review` result/finding structure and remove the new assets if preservation cannot be proven.

### M3. Proposal-review asset conformance

- Milestone state: review-requested
- Goal: Bring existing `proposal-review` assets and resource-map entries under the review-family contract without changing proposal-review behavior.
- Requirements: RSF-R1 through RSF-R30, RSF-R43, AC-RSF-001 through AC-RSF-013
- Files/components likely touched:
  - `skills/proposal-review/SKILL.md`
  - `skills/proposal-review/assets/material-finding.md`
  - `skills/proposal-review/assets/review-result-skeleton.md`
  - `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/`
- Dependencies:
  - M1 validation foundation closed.
  - M2 material-finding parser-owned field block available as the comparison baseline, or M3 establishes the baseline if implemented first.
- Tests to add/update:
  - Focused skill-validator coverage for proposal-review asset conformance and byte-identical material-finding field block.
  - Behavior-preservation and representative parity evidence for `proposal-review`.
- Implementation steps:
  - Update existing assets only where needed to match metadata, placeholder, parser-field, and review-class boundary requirements.
  - Keep proposal-review status vocabulary `approved | changes-requested | blocked | inconclusive` unchanged.
  - Add or refine resource-map text for literal `Finding ID:` confirmation before linking.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape`
  - `git diff --check --`
- Expected observable result: `proposal-review` assets meet the family contract and preserve existing verdicts, material findings, recording outcomes, and handoff statements.
- Commit message: `M3: conform proposal-review family assets`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Regressing the proposal-family assets contract while adding the review-family contract.
- Rollback/recovery:
  - Restore the prior proposal-review asset text and reapply only the missing review-family invariant with focused proof.

### M4. Spec-review asset conformance and material-finding rename

- Milestone state: planned
- Goal: Bring `spec-review` under the review-family asset contract, including the approved `assets/material-finding.md` name, while preserving spec-review readiness and status behavior.
- Requirements: RSF-R1 through RSF-R30, RSF-R43, AC-RSF-001 through AC-RSF-013
- Files/components likely touched:
  - `skills/spec-review/SKILL.md`
  - `skills/spec-review/assets/material-finding.md`
  - `skills/spec-review/assets/review-finding.md` if removed or replaced by the approved material-finding asset
  - `skills/spec-review/assets/review-result-skeleton.md`
  - `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/`
- Dependencies:
  - M1 validation foundation closed.
  - Byte-identical material-finding field block from M2/M3 available.
- Tests to add/update:
  - Focused skill-validator coverage for spec-review asset inventory, `review-finding.md` removal or non-family status if retained by an approved fallback, and result-skeleton status/field preservation.
  - Behavior-preservation and representative parity evidence for `spec-review`.
- Implementation steps:
  - Replace `assets/review-finding.md` references with `assets/material-finding.md` unless plan-review or test-spec finds a safer approved fallback.
  - Keep `approved | changes-requested | blocked | inconclusive`, eventual test-spec readiness fields, recording behavior, and downstream settlement guidance unchanged.
  - Add or refine resource-map text for literal `Finding ID:` confirmation before linking.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape`
  - `git diff --check --`
- Expected observable result: `spec-review` has the approved review-family assets and preserves spec-review output semantics, including eventual test-spec readiness.
- Commit message: `M4: conform spec-review family assets`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Leaving stale references to `review-finding.md` or changing spec-review downstream readiness behavior while renaming the asset.
- Rollback/recovery:
  - Restore the previous spec-review asset/reference pair and record a spec/test-spec blocker if the approved asset name cannot be adopted safely.

### M5. Generated output, token, cold-read, and lifecycle closeout

- Milestone state: planned
- Goal: Prove the canonical skill changes package correctly into generated mirrors and temporary adapters, record token/cold-read evidence, and prepare final lifecycle handoff.
- Requirements: RSF-R31 through RSF-R37, RSF-R43 through RSF-R45, AC-RSF-014 through AC-RSF-018
- Files/components likely touched:
  - Generated skill mirror check outputs, if repository-owned and tracked
  - Temporary adapter output outside tracked source
  - `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/`
  - `docs/plan.md`
  - this plan
- Dependencies:
  - M2, M3, and M4 closed after code-review.
- Tests to add/update:
  - Generated skill mirror asset presence proof.
  - Temporary adapter archive asset presence and adapter validation proof.
  - Token-cost evidence separating common-path `SKILL.md` body size from total packaged footprint and usage expectations.
  - Cold-read proof using installed skill output plus packaged assets.
- Implementation steps:
  - Run generated skill mirror and adapter validation from canonical `skills/`.
  - Record generated-output, token-cost, cold-read, preservation, and behavior-parity evidence.
  - Prepare explain-change input and final verify scope.
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version <version> --output-dir <tmpdir>`
  - `python scripts/validate-adapters.py --root <tmpdir> --version <version>`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape.md --path specs/review-skill-family-consistency-parser-owned-finding-shape.md --path docs/plans/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape.md --path docs/plan.md --path docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/change.yaml --path docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/review-log.md --path docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/review-resolution.md`
  - `git diff --check --`
- Expected observable result: generated mirrors and temporary adapter archives include all mapped assets; no generated output is hand-edited; evidence is ready for explain-change, verify, and PR.
- Commit message: `M5: close review-family asset evidence`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Temporary adapter proof passes but unrelated tracked generated-output debt appears.
  - Token footprint grows and is misread as a regression.
- Rollback/recovery:
  - Use temporary generated output as the adapter proof surface, record unrelated stale debt separately, and preserve the spec-approved token interpretation that common-path size and total packaged footprint are separate measures.

## Validation plan

- `python scripts/test-skill-validator.py`: deterministic review-family asset contract checks.
- `python scripts/validate-skills.py`: canonical skill validation.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape`: review-artifact structure during implementation.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape`: final review-recording closeout when required records exist.
- `python scripts/build-skills.py --check`: generated skill mirror asset presence and drift proof.
- `python scripts/build-adapters.py --version <version> --output-dir <tmpdir>`: temporary adapter package generation.
- `python scripts/validate-adapters.py --root <tmpdir> --version <version>`: temporary adapter package validation.
- `python scripts/measure-skill-tokens.py`: common-path and packaged-footprint evidence input.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/change.yaml`: change metadata consistency.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`: lifecycle status and artifact consistency for touched lifecycle artifacts.
- `git diff --check --`: whitespace and patch hygiene.

## Risks and recovery

- Risk: The implementation silently adds severity-enum validation.
  - Recovery: Revert the validator behavior and keep invalid-fill proof limited to parser-owned `Finding ID:` identity defects.
- Risk: A shared result skeleton homogenizes `code-review` and gate-review status semantics.
  - Recovery: Revert to one result skeleton per skill and preserve each source status enum verbatim.
- Risk: The three material-finding copies drift in non-parser content.
  - Recovery: Enforce byte-identical parser-owned field blocks, record any harmless non-parser variation, or make the copies identical.
- Risk: Review judgment leaks into assets.
  - Recovery: Move policy/rule text back to `SKILL.md` and keep assets to headings, labels, placeholders, and short fill hints.
- Risk: Generated adapter evidence is confused with hand-edited output.
  - Recovery: Generate into a temporary output directory and validate from canonical `skills/` sources only.

## Dependencies

- Plan-review must approve this plan before test-spec or implementation.
- A matching test spec must be approved before implementation begins.
- M1 must close before per-skill asset edits proceed.
- Each implementation milestone must pass code-review before the next implementation milestone starts, unless the active plan is explicitly replanned.
- Final explain-change, verify, and PR handoff remain downstream gates after all implementation milestones are closed.

## Progress

- 2026-05-21: Proposal accepted and proposal-review recorded clean.
- 2026-05-21: Spec drafted, reviewed, revised for `RSF-SR1`, and approved by `spec-review-r2`.
- 2026-05-21: Spec status settled from `draft` to `approved` before plan reliance.
- 2026-05-21: Plan created and indexed; no implementation has started.
- 2026-05-21: Plan-review approved the execution plan and active test spec was created; no implementation has started.
- 2026-05-21: M1 implementation started. Scope is validator/test foundation and the skill-contract sufficiency assessment only; no review-skill asset edits are part of M1.
- 2026-05-21: M1 implemented review-family validator foundation, review-artifact parser-owned identity fixture proof, and skill-contract sufficiency assessment. M1 is ready for code-review.
- 2026-05-21: First-pass code-review for M1 requested changes for `RSF-M1-CR1`; M1 is in review-resolution before M2 can start.
- 2026-05-21: `RSF-M1-CR1` accepted and fixed. The non-enum severity test now inserts an actual `Severity: not-a-current-enum` field before asserting structure validation passes. M1 is ready for code-review rerun.
- 2026-05-21: M1 code-review rerun returned clean-with-notes. M1 is closed and the active handoff is `implement M2`.
- 2026-05-21: M2 added `code-review` material-finding and result-skeleton assets, resource-map entries, focused validator coverage, and preservation evidence. M2 is ready for code-review.
- 2026-05-21: M2 code-review returned clean-with-notes. M2 is closed and the active handoff is `implement M3`.
- 2026-05-21: M3 conformed proposal-review's existing assets by adding literal `Finding ID:` resource-map confirmation, explicit gate-review status vocabulary, focused validator coverage, and preservation evidence. M3 is ready for code-review.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-21 | No separate architecture package is required before planning. | The approved spec touches skill text/assets, deterministic validation, generated-output proof, and lifecycle evidence without new runtime architecture, persistence, security, external service, or adapter install-root design. | Create an architecture artifact with no additional architectural decision to make. |
| 2026-05-21 | Sequence validator foundation before skill edits. | The spec's first-principle fix depends on deterministic parser-conformance and asset-boundary checks, so the checks should exist before the per-skill changes rely on them. | Edit all skills first and add proof only during closeout. |
| 2026-05-21 | Use one implementation milestone per first-slice review skill. | Per-skill milestones make behavior preservation, status vocabulary preservation, and review evidence tractable. | Combine all review skills into one large implementation milestone. |
| 2026-05-21 | Keep result skeletons per skill. | `code-review` and gate-review skills use different status semantics, and a shared skeleton risks behavior-changing vocabulary homogenization. | Shared result skeleton or shared base in this slice. |
| 2026-05-21 | Treat `specs/skill-contract.md` sufficiency as an M1 stop-or-proceed check. | The approved spec requires this assessment before skill edits, and M1 is the first point where validator gaps can be tested concretely. | Assume sufficiency without recorded evidence. |

## Surprises and discoveries

- `proposal-review` already has the two target assets, so M3 is a conformance pass rather than a pure addition.
- `spec-review` currently uses `assets/review-finding.md`; M4 must account for the approved `assets/material-finding.md` contract and avoid stale references.

## Validation notes

- 2026-05-21: Plan authoring, plan-review recording, and active test-spec authoring validation passed.
- 2026-05-21: M1 targeted validation passed: `python scripts/test-skill-validator.py`; `python scripts/test-review-artifact-validator.py`; `python scripts/validate-skills.py`; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape`; `git diff --check --`.
- 2026-05-21: M1 code-review found the non-enum severity validation proof was vacuous because the fixture did not contain a `Severity:` field before replacement. Corrected proof is required before M1 closeout.
- 2026-05-21: After `RSF-M1-CR1` fix, focused validation passed: `python scripts/test-review-artifact-validator.py`; `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`.
- 2026-05-21: M1 code-review rerun recorded clean-with-notes after `RSF-M1-CR1` resolution.
- 2026-05-21: M2 targeted validation passed: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape`; `git diff --check --`.
- 2026-05-21: M2 code-review recorded clean-with-notes with no material findings.
- 2026-05-21: M3 targeted validation passed: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape`; `git diff --check --`.

## Outcome and retrospective

- Pending. This section will be filled after implementation, review, verification, and PR handoff complete.

## Readiness

- See `Current Handoff Summary`.
- Ready for `code-review M3`.
- Not ready for final closeout or PR; implementation, code-review, review-resolution if triggered, explain-change, verify, and PR handoff remain.
