# Bounded Review-Fix Autoprogression in Chat Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Change ID: 2026-06-30-bounded-review-fix-autoprogression-in-chat
- Owner: agent
- Start date: 2026-06-30
- Last updated: 2026-06-30
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved bounded review-fix autoprogression contract so a user can explicitly run `$workflow auto: <target-stage>`, persist review-fix authorization under `workflow.autoprogression.review_fix`, let the workflow driver apply only deterministic auto-safe fixes, rerun the same review, and continue through the proposal-side lifecycle no later than `test-spec-review`.

The implementation must preserve direct review isolation, existing `authoring-through-plan-review` and `implementation-through-verify` behavior, durable review recording, owner-decision stops, and the no-implementation/no-verify/no-PR/no-release boundary.

## Source artifacts

- Proposal: [Bounded Review-Fix Autoprogression in Chat](../proposals/2026-06-30-bounded-review-fix-autoprogression-in-chat.md)
- Spec: [Review-Fix Autoprogression](../../specs/review-fix-autoprogression.md)
- Architecture: [Canonical System Architecture](../architecture/system/architecture.md)
- ADR: [ADR-20260630 Bounded Review-Fix Autoprogression](../adr/ADR-20260630-bounded-review-fix-autoprogression.md)
- Test spec: [Review-Fix Autoprogression Test Spec](../../specs/review-fix-autoprogression.test.md)
- Change metadata: [change.yaml](../changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml)
- Review log: [review-log.md](../changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/review-log.md)
- Review resolution: [review-resolution.md](../changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/review-resolution.md)
- Proposal reviews: [proposal-review-r1](../changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/reviews/proposal-review-r1.md), [proposal-review-r2](../changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/reviews/proposal-review-r2.md)
- Spec reviews: [spec-review-r1](../changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/reviews/spec-review-r1.md), [spec-review-r2](../changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/reviews/spec-review-r2.md)
- Architecture reviews: [architecture-review-r1](../changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/reviews/architecture-review-r1.md), [architecture-review-r2](../changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/reviews/architecture-review-r2.md)

## Upstream status settlement

- Settlement result: not-needed
- New status: not-applicable
- Settlement blocker: none
- Evidence: proposal status is `accepted`; spec status is `approved`; canonical architecture status is `approved`; ADR status is `accepted`; proposal-review R2, spec-review R2, architecture-review R2, plan-review R2, and test-spec-review R1 are approved with no material findings; matching test spec is active; `review-resolution.md` is closed and `review-log.md` has no open findings.

## Context and orientation

RigorLoop is an artifact-driven workflow repository. This change affects workflow policy state, review routing, review-resolution evidence, validators, stage skill guidance, generated adapter validation, and lifecycle proof artifacts. It does not add a service, background worker, scheduler, database, CLI command, external API, release operation, or hosted PR actor.

Relevant implementation areas:

- `schemas/change.schema.json` and `scripts/change_metadata_semantics.py` own change metadata shape and semantic checks.
- `scripts/lifecycle_state_sync.py`, `scripts/artifact_lifecycle_validation.py`, and `scripts/validate-artifact-lifecycle.py` own workflow route evaluation and lifecycle proof.
- `scripts/review_artifact_validation.py` and `scripts/validate-review-artifacts.py` own review record and review-resolution structure.
- `skills/workflow/SKILL.md` and proposal-side stage skills own user-facing orchestration guidance.
- `scripts/test-*.py`, `tests/fixtures/`, generated-skill checks, and adapter validation own regression proof.

## Non-goals

- Do not implement code-review, verify, PR, release, publication, network, destructive, or external-state automation in this profile.
- Do not add dry-run mode, apply-mode state, or an `apply safe fixes` command.
- Do not make direct `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, `test-spec-review`, or `code-review` invocations activate or resume the profile.
- Do not let review skills edit their reviewed artifact during the review pass.
- Do not auto-apply product, requirement, architecture, validation-ownership, release, generated-output ownership, or owner-decision changes.
- Do not make review-fix policy metadata own active plan state, branch readiness, PR readiness, review verdicts, or final workflow completion.
- Do not hand-edit generated public adapter package output.

## Requirements covered

- `R1`-`R10`, `R39`-`R43`: M1 and M2 implement command/state shape, durable authorization, direct-review isolation, terminal transitions, and fail-closed validation.
- `R11`-`R22g`: M2 implements proposal-side routing, target-stage bounds, preflight, current-gate checks, architecture assessment, `architecture-not-required`, and `target-not-applicable`.
- `R23`-`R38`: M3 implements driver-owned auto-safe classification evidence, budgets, stale-review stops, generated-owner stops, review-resolution disposition, and same-review rerun linkage.
- `R41`: M4 aligns chat result guidance and user-facing stage behavior.
- `R44`-`R45`: M4 and M5 preserve existing autoprogression behavior and prevent partial user-visible enablement before the full proposal-side contract is proven.
- `AC1`-`AC26`: covered across M1 through M5 and operationalized by the pending test spec.

## Current Handoff Summary

- Current milestone: M1. Review-Fix State Schema and Metadata Validation
- Current milestone state: review-requested
- Latest review evidence: code-review-m1-r1
- Last reviewed milestone: none
- Review status: inconclusive; stage=code-review; round=r1
- Remaining in-scope implementation milestones: M1, M2, M3, M4, M5
- Next stage: blocked
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: lifecycle-gates-open, implementation-milestones-open, milestone-review-pending, explain-change-pending, verify-pending, pr-handoff-pending — code-review M1 R1 is inconclusive because governing artifacts are local-only/untracked; M1 remains open, and M2-M5, explain-change, verify, and PR handoff are not complete.

## Milestones

### M1. Review-Fix State Schema and Metadata Validation

- Milestone state: review-requested
- Goal: Add durable `workflow.autoprogression.review_fix` state support with closed profile, status, target-stage, cursor, stop-reason, and evidence fields.
- Requirements: `R1`-`R10`, `R39`, `R42`, `AC1`-`AC6`, `AC15`-`AC19`
- Files/components likely touched:
  - `schemas/change.schema.json`
  - `scripts/change_metadata_semantics.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/test-change-metadata-validator.py`
  - `tests/fixtures/change-metadata/`
  - `docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml`
- Dependencies:
  - Approved spec and architecture-review R2.
  - Plan-review approval before test-spec starts.
  - Approved matching test spec and clean test-spec-review before implementation starts.
- Tests to add/update:
  - Valid `workflow.autoprogression.review_fix` fixture for `bounded-review-fix`.
  - Unknown top-level autoprogression profile value fails closed.
  - Unknown review-fix profile, status, target stage, and stop reason fail closed.
  - Required authorization and cursor fields are enforced when state is armed or active.
  - Direct-review-only metadata does not create review-fix authorization.
  - Terminal transitions for `off`, `cancelled`, `completed`, and target reached are deterministic.
- Implementation steps:
  - Extend the change metadata schema for the nested `review_fix` profile without widening existing profile behavior.
  - Add semantic checks for closed values, required fields, matching change ID when present, and forbidden live-state ownership.
  - Add positive and negative fixtures for state shape and unknown values.
  - Keep `workflow-policy.yaml` as an auditable fallback only when change metadata cannot carry the policy data.
- Validation commands:
  - `python scripts/test-change-metadata-validator.py -k review_fix`
  - `python scripts/test-change-metadata-validator.py -k autoprogression`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml`
- Expected observable result: Review-fix authorization can be represented durably and invalid state fails before routing or mutation.
- Implementation notes:
  - Added `workflow.autoprogression.review_fix` as a named change-metadata policy record without adding `bounded-review-fix` to the legacy top-level autoprogression profile enum.
  - Added review-fix closed vocabularies for profile, status, target stage, current stage, and stop reason, plus required authorization, cursor, evidence, and change-ID checks.
  - Extended query-summary evidence for named review-fix policy records while filtering live workflow ownership fields.
  - Left `scripts/change_metadata_semantics.py` unchanged because existing autoprogression policy checks live in `scripts/validate-change-metadata.py`.
- Validation notes:
  - `python scripts/test-change-metadata-validator.py -k review_fix` passed.
  - `python scripts/test-change-metadata-validator.py -k autoprogression` passed.
  - `python scripts/test-change-metadata-validator.py` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml` passed.
- Commit message: `M1: add review-fix profile state validation`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before M2 starts
- Risks:
  - New schema rules could reject older autoprogression metadata.
  - Policy fields could be mistaken for live workflow state.
- Rollback/recovery:
  - Revert schema, semantic checks, and fixtures together; leave the profile unrecognized and inactive.

### M2. Review-Fix Driver Routing, Preflight, and Target Bounds

- Milestone state: planned
- Goal: Add route evaluation and lifecycle proof for `$workflow auto: <target-stage>`, activation gates, preflight, direct-review isolation, architecture assessment, and target-boundary stops.
- Requirements: `R11`-`R22g`, `R37`, `R39`-`R40`, `R43`, `AC7`, `AC13`-`AC24`
- Files/components likely touched:
  - `scripts/lifecycle_state_sync.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `tests/fixtures/artifact-lifecycle/`
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md`
- Dependencies:
  - M1 state shape and validation.
- Tests to add/update:
  - `$workflow auto: <target-stage>` rejects unknown target stages.
  - Activation requires durable authorization plus clean current gate.
  - Proposal-start activation requires accepted proposal, approved recorded proposal-review, no open findings, closed resolution, and unambiguous placement.
  - Direct review invocation does not activate, resume, or advance review-fix state.
  - Unknown, malformed, missing, stale, or contradictory state pauses before mutation.
  - Approved `spec-review` requires exactly one architecture assessment value.
  - `architecture-required`, `architecture-not-required`, `architecture-ambiguous`, and `target-not-applicable` route or stop correctly.
  - Target-stage upper bound prevents continuation past the requested target.
- Implementation steps:
  - Add a review-fix route evaluator alongside existing authoring and implementation profile evaluators.
  - Add preflight evidence inputs for change ID, target artifact, review state, profile state, artifact freshness, and next transition.
  - Add architecture-assessment routing and skipped-target behavior.
  - Add lifecycle fixtures for activation, resume, direct-review isolation, stale review evidence, and target bounds.
  - Update workflow guidance with the command shape, state transitions, and stop reasons.
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py -k review_fix`
  - `python scripts/test-artifact-lifecycle-validator.py -k autoprogression`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path skills/workflow/SKILL.md --path docs/workflows.md --path docs/plans/2026-06-30-bounded-review-fix-autoprogression-in-chat.md --path docs/plan.md --path docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml`
- Expected observable result: The route evaluator can explain start, pause, completion, target-not-applicable, and direct-review isolation without hidden downstream handoff.
- Commit message: `M2: route bounded review-fix autoprogression`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before M3 starts
- Risks:
  - Routing could accidentally overlap `authoring-through-plan-review`.
  - Resume logic could infer readiness from artifact existence instead of review evidence.
- Rollback/recovery:
  - Disable route activation while keeping state validation in place; preserve direct manual workflow behavior.

### M3. Auto-Safe Classification, Review-Resolution, and Rereview Evidence

- Milestone state: planned
- Goal: Enforce driver-owned auto-safe classification, budget limits, review-resolution disposition, stale-review protection, generated-owner stops, and mandatory same-review reruns.
- Requirements: `R18`-`R20`, `R23`-`R38`, `R41`-`R43`, `AC7`-`AC13`, `AC21`-`AC23`, `AC26`
- Files/components likely touched:
  - `scripts/review_artifact_validation.py`
  - `scripts/validate-review-artifacts.py`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `tests/fixtures/review-artifacts/`
  - `tests/fixtures/artifact-lifecycle/`
  - `templates/review-resolution.md`
  - review-stage skill guidance when needed
- Dependencies:
  - M2 route evaluator and stop reason vocabulary.
- Tests to add/update:
  - Driver classification values are closed.
  - Exact reviewer wording requires target artifact, target section or line range, exact quoted replacement, no owner decision, and no semantic scope change.
  - Needs-decision, ambiguous alternatives, scope/requirement/architecture/validation ownership changes, generated output ownership, and missing patch targets stop.
  - Budget exhaustion stops for cycle, finding, per-cycle file, and per-chat file budgets.
  - Auto-applied dispositions include finding ID, classification, rationale, changed files, validation evidence, and rereview linkage.
  - Auto-applied fixes without same-review rerun are rejected.
  - Stale reviewed artifact cannot authorize fixes or continuation.
- Implementation steps:
  - Add review-resolution fields and parser checks for review-fix auto-applied dispositions.
  - Add closed classification and stop-reason validation.
  - Add budget and rereview-linkage consistency checks in review artifacts or lifecycle validation.
  - Add fixtures for safe mechanical fixes, exact reviewer wording, non-auto-safe blockers, and stale evidence.
  - Keep implementation-profile `auto_fix_class` semantics separate from review-fix driver classification.
- Validation commands:
  - `python scripts/test-review-artifact-validator.py -k review_fix`
  - `python scripts/test-artifact-lifecycle-validator.py -k review_fix`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat`
- Expected observable result: Review-fix mutations are accepted only when bounded, recorded, current, and followed by same-review rerun evidence.
- Commit message: `M3: validate review-fix safe corrections`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before M4 starts
- Risks:
  - The review-resolution shape could become too broad and accept semantic edits.
  - Validator overlap with implementation-profile auto-fix fields could create confusing error messages.
- Rollback/recovery:
  - Revert review-fix disposition validation and keep all review findings manual until the shape is narrowed.

### M4. Workflow, Stage Skill, and Contributor Guidance Alignment

- Milestone state: planned
- Goal: Align user-facing workflow and affected stage skills with the approved review-fix profile while preserving isolated direct review behavior.
- Requirements: `R1`-`R3`, `R10`-`R17`, `R39`-`R45`, `AC1`-`AC5`, `AC14`-`AC26`
- Files/components likely touched:
  - `skills/workflow/SKILL.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/test-spec/SKILL.md`
  - `skills/test-spec-review/SKILL.md`
  - `docs/workflows.md`
  - `scripts/test-skill-validator.py`
- Dependencies:
  - M1 through M3 vocabulary, state shape, and review-resolution evidence.
- Tests to add/update:
  - Public skill text names `bounded-review-fix` only as explicitly armed workflow-managed behavior.
  - Direct review invocations remain isolated in every affected review skill.
  - Workflow skill reports `$workflow auto: status` without mutation and `$workflow auto: off` as deterministic cancellation/clear behavior.
  - Stage handoffs do not imply implementation, verify, PR, release, or external operations.
  - Existing `authoring-through-plan-review` and `implementation-through-verify` wording remains unchanged in scope.
- Implementation steps:
  - Update workflow guidance for command forms, target-stage enum, activation gates, stop reasons, and chat result shape.
  - Update affected authoring and review skills only where the new profile changes handoff or review-recording wording.
  - Add skill-validator checks for direct-review isolation and no hidden downstream handoff.
  - Record unaffected-with-rationale for any stage skill intentionally not changed.
- Validation commands:
  - `python scripts/test-skill-validator.py -k review_fix`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path skills/workflow/SKILL.md --path docs/workflows.md --path docs/plans/2026-06-30-bounded-review-fix-autoprogression-in-chat.md --path docs/plan.md --path docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml`
- Expected observable result: Users and agents see one consistent, explicit, bounded review-fix profile and direct reviews still remain isolated by default.
- Commit message: `M4: align review-fix workflow guidance`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before M5 starts
- Risks:
  - User-facing skill text could expose too much maintainer-only path detail.
  - Multiple skills could drift on target-stage or stop-reason wording.
- Rollback/recovery:
  - Revert affected skill and workflow guidance as one unit and leave validators inactive for the profile until guidance is corrected.

### M5. Integration Proof, Generated Adapters, and Behavior Preservation

- Milestone state: planned
- Goal: Prove the integrated proposal-side feature through `test-spec-review`, generated guidance, behavior-preservation evidence, and final validation bundles before downstream closeout.
- Requirements: `R44`-`R45`, all acceptance criteria `AC1`-`AC26`
- Files/components likely touched:
  - `docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/behavior-preservation.md`
  - `scripts/build-skills.py`
  - `scripts/test-build-skills.py`
  - `scripts/test-adapter-distribution.py`
  - `dist/adapters/README.md`
  - `dist/adapters/manifest.yaml`
  - `docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml`
- Dependencies:
  - M1 through M4 complete and code-reviewed.
  - Approved matching test spec and clean test-spec-review completed before M1 implementation starts.
- Tests to add/update:
  - End-to-end fixture for armed loop through `test-spec-review`.
  - Behavior-preservation matrix proving direct review isolation and existing profiles unchanged.
  - Generated-skill and adapter checks after canonical skill changes.
  - Full acceptance criteria trace from spec to tests and validation evidence.
- Implementation steps:
  - Add behavior-preservation evidence for direct reviews, authoring profile, implementation profile, review recording, rereview, and stop boundaries.
  - Run generated-skill and adapter validation after skill changes.
  - Run final targeted and selected validation bundles.
  - Record any unaffected adapter surfaces with rationale.
- Validation commands:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-build-skills.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-30-bounded-review-fix-autoprogression-in-chat.md --path specs/review-fix-autoprogression.md --path specs/review-fix-autoprogression.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260630-bounded-review-fix-autoprogression.md --path docs/plans/2026-06-30-bounded-review-fix-autoprogression-in-chat.md --path docs/plan.md --path docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml --path docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/review-log.md --path docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/review-resolution.md`
  - `bash scripts/ci.sh --mode explicit --path specs/review-fix-autoprogression.md --path specs/review-fix-autoprogression.test.md --path skills/workflow/SKILL.md --path docs/workflows.md --path docs/plans/2026-06-30-bounded-review-fix-autoprogression-in-chat.md --path docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml`
- Expected observable result: The full proposal-side review-fix profile is validated end to end, with behavior-preservation evidence and no partial user-visible enablement gap.
- Commit message: `M5: prove review-fix autoprogression integration`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to final code-review
  - all material findings resolved before explain-change
- Risks:
  - Generated adapter validation may expose stale public guidance unrelated to this change.
  - Full integration fixtures may duplicate smaller validator tests instead of proving cross-surface behavior.
- Rollback/recovery:
  - Keep the profile disabled or unadvertised, preserve review records, and revert workflow/skill routing changes while retaining approved spec and architecture artifacts for a narrowed follow-up.

## Validation plan

- Plan authoring validation:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-30-bounded-review-fix-autoprogression-in-chat.md --path specs/review-fix-autoprogression.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260630-bounded-review-fix-autoprogression.md --path docs/plans/2026-06-30-bounded-review-fix-autoprogression-in-chat.md --path docs/plan.md --path docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml --path docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/review-log.md --path docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/review-resolution.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat`
  - `git diff --check`
- Milestone-specific validation commands are listed in each milestone and should be run before code-review handoff.
- Final validation expands to all changed validators, skills, generated-output checks, review artifacts, change metadata, artifact lifecycle validation, selected CI, `explain-change`, `verify`, and `pr` handoff after all implementation milestones close.

## Risks and recovery

- Risk: Review-fix policy state could become a competing live workflow owner.
  - Recovery: keep live state in active plans and review artifacts; validate review-fix metadata as policy/cursor evidence only.
- Risk: Auto-safe classification could accidentally authorize semantic changes.
  - Recovery: fail closed on requirements, architecture, scope, validation ownership, generated ownership, ambiguity, and owner decisions.
- Risk: Same-review rerun linkage could be skipped.
  - Recovery: validators reject auto-applied fixes without rereview linkage and current review evidence.
- Risk: Existing autoprogression profiles could drift.
  - Recovery: behavior-preservation tests compare direct-review isolation, `authoring-through-plan-review`, and `implementation-through-verify` before closeout.
- Risk: Stage skill text could over-promise implementation or PR readiness.
  - Recovery: skill-validator checks and plan-review require stop boundaries through `test-spec-review` only.

## Dependencies

- Approved proposal, spec, architecture, ADR, and clean architecture-review R2.
- Plan-review approval before test-spec and implementation.
- Matching test spec and test-spec-review before implementation.
- Existing change metadata, lifecycle, review artifact, skill, generated-skill, and adapter validators.
- No new runtime dependency is planned.

## Progress

- 2026-06-30: Proposal accepted after proposal-review R2; spec approved after spec-review R2; architecture package and ADR approved after architecture-review R2; execution plan created.
- 2026-06-30: Plan-review R1 requested plan revision for PR-RFA-1 before test-spec handoff or implementation readiness.
- 2026-06-30: Revised the plan for PR-RFA-1 so test-spec is a downstream lifecycle artifact after clean plan-review and before M1 implementation, not M5 implementation-owned work.
- 2026-06-30: Plan-review R2 approved the revised plan with no material findings; next stage is `test-spec`.
- 2026-06-30: Authored active test spec `specs/review-fix-autoprogression.test.md`; next stage is `test-spec-review`.
- 2026-06-30: Test-spec-review R1 approved the active test spec with no material findings; next stage is `implement`.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-30 | Split implementation into five internal milestones. | Keeps one integrated user-visible feature while allowing focused code-review over state, routing, review evidence, skill guidance, and integration proof. | One large implementation milestone; partial user-visible feature slices. |
| 2026-06-30 | Keep review-fix classification driver-owned and separate from implementation-profile `auto_fix_class`. | The approved spec assigns review-fix classification to the driver while existing implementation correction authority uses reviewer-owned code-review fields. | Reuse implementation-profile `auto_fix_class` directly for proposal-side review-fix automation. |

## Surprises and discoveries

- None yet.

## Validation notes

- 2026-06-30: Pre-plan validation already passed for review artifact closeout, change metadata, artifact lifecycle explicit paths, and diff whitespace after architecture-review R2.

## Outcome and retrospective

- Not started. Fill after implementation, review-resolution when triggered, explain-change, verify, and PR handoff complete.

## Readiness

- See `Current Handoff Summary`.
