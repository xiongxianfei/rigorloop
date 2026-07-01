# Explain Change: Bounded Review-Fix Autoprogression in Chat

## Summary

This change adds an explicitly armed, bounded `bounded-review-fix` workflow profile for `$workflow auto: <target-stage>`. The profile is proposal-side only: it can route through proposal, spec, conditional architecture, plan, and test-spec gates, ending no later than `test-spec-review`.

The implementation is guidance-, metadata-, and validator-driven. It adds durable state validation, route evaluation proof, review-resolution validation for auto-safe fixes, workflow skill guidance, behavior-preservation evidence, and regression tests. It does not add a daemon, background worker, service, CLI command runner, network operation, release operation, PR automation, or implementation/verify automation under this profile.

## Problem

The manual lifecycle loop was repetitive:

```text
author artifact -> review -> resolve safe findings -> rereview -> trigger next stage
```

The accepted direction was to automate the repetitive review-fix routing only when the user explicitly arms the workflow, while preserving direct review isolation, formal review recording, owner-decision stops, current clean gates, same-review rereview, and target-stage bounds. The owner also rejected a separate dry-run/apply-mode model, so the final contract keeps the command surface simple and relies on explicit arming, closed target stages, auto-safe criteria, budgets, durable dispositions, and validators.

## Decision Trail

- Proposal decision: implement one integrated proposal-side feature through `test-spec-review`, not several partial user-visible slices.
- Spec requirements: `R1`-`R10` define command and state shape; `R11`-`R22g` define proposal-side routing, current gates, and architecture assessment; `R23`-`R38` define driver-owned auto-safe classification, budgets, stale-review stops, and review-resolution proof; `R39`-`R45` define terminal state, compatibility, reporting, and no partial exposure.
- Acceptance criteria: `AC1`-`AC26` cover closed target stages, direct-review isolation, durable authorization, review evidence, same-review rereview, stop boundaries, architecture routing, compatibility, and chat result reporting.
- Architecture/ADR: the workflow skill remains the orchestrator; authoring and review skills keep their artifact/review authority; `workflow.autoprogression.review_fix` is profile-local policy/cursor evidence, not active plan state or PR readiness.
- Plan milestones: M1 added state/schema validation; M2 added route evaluation and target bounds; M3 added review-resolution auto-safe validation; M4 aligned workflow and skill guidance; M5 added behavior-preservation, generated-skill, adapter, and final integration proof.

## Diff Rationale By Area

| Area | Files | Why they changed | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| Lifecycle artifacts | `docs/proposals/...`, `specs/review-fix-autoprogression.md`, `specs/review-fix-autoprogression.test.md`, `docs/architecture/system/architecture.md`, `docs/adr/ADR-20260630-bounded-review-fix-autoprogression.md`, `docs/plans/...` | Record the accepted product contract, approved requirements, test proof map, architecture placement, ADR, and milestone plan for the new profile. | Proposal, spec, architecture, plan, test spec | Proposal/spec/architecture/plan/test-spec reviews all approved after required revisions. |
| Change-local evidence | `docs/changes/.../change.yaml`, `review-log.md`, `review-resolution.md`, `reviews/*.md`, `behavior-preservation.md` | Record durable review evidence, material finding dispositions, implementation review results, validation history, and behavior-preservation proof. | Workflow contract and review-resolution policy | `validate-change-metadata`, `validate-review-artifacts`, lifecycle validation, and code reviews. |
| Metadata validation | `schemas/change.schema.json`, `scripts/validate-change-metadata.py`, `scripts/query-change-record.py`, `tests/fixtures/change-metadata/review-fix-valid/change.yaml`, `scripts/test-change-metadata-validator.py` | Add `workflow.autoprogression.review_fix` shape, closed vocabularies, required fields, terminal states, fallback query output, and fail-closed tests. | Spec `R1`-`R10`, `R39`, `R42`, `AC1`-`AC6`, `AC15`-`AC19` | `python scripts/test-change-metadata-validator.py`; targeted `-k review_fix` and `-k autoprogression` runs. |
| Route evaluation | `scripts/lifecycle_state_sync.py`, `scripts/test-artifact-lifecycle-validator.py` | Add bounded review-fix route evaluation, durable authorization checks, direct-review isolation, current approved gate checks, target bounds, architecture assessment, `target-not-applicable`, and terminal state behavior. | Spec `R11`-`R22g`, `R37`, `R39`-`R43`, `AC7`, `AC13`-`AC24` | `python scripts/test-artifact-lifecycle-validator.py`; CR-RFA-M2-1 regression tests for missing, non-approved, and unsupported `latest_review_status`. |
| Review-resolution validation | `scripts/review_artifact_validation.py`, `scripts/test-review-artifact-validator.py`, `templates/review-resolution.md` | Validate review-fix auto-resolution markers, driver classifications, exact reviewer wording, not-auto-safe blockers, budgets, stale/current evidence, files changed, and same-review rerun linkage. | Spec `R23`-`R38`, `R41`-`R43`, `AC7`-`AC13`, `AC21`-`AC23`, `AC26` | `python scripts/test-review-artifact-validator.py`; CR-RFA-M3-1 and CR-RFA-M3-2 regression tests. |
| Workflow and skill guidance | `skills/workflow/SKILL.md`, `skills/code-review/SKILL.md`, `skills/test-spec-review/SKILL.md`, `docs/workflows.md`, `scripts/test-skill-validator.py` | Document `$workflow auto: <target-stage>`, `$workflow auto: status`, `$workflow auto: off`, direct-review isolation, architecture assessment behavior, chat-result fields, and boundaries against implementation/verify/PR/release. | Spec `R1`-`R3`, `R10`-`R17`, `R39`-`R45`, `AC1`-`AC5`, `AC14`-`AC26` | `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; `python scripts/build-skills.py --check`. |
| Adapter distribution proof | `scripts/test-adapter-distribution.py` | Keep adapter release fixture validation aligned when current canonical skills include non-portable skill exclusions such as `workflow`. | Plan M5 and behavior-preservation proof | `python scripts/test-adapter-distribution.py`; selected CI. |

## Tests Added Or Changed

- Change metadata tests prove `review_fix` closed vocabulary, required fields, terminal transitions, direct-review-only metadata isolation, and query-summary shape.
- Artifact lifecycle tests prove unknown targets fail, direct reviews do not activate or resume the profile, activation requires durable authorization and a clean approved current gate, architecture assessment routes correctly, target bounds hold, and terminal states are deterministic.
- Review artifact tests prove review-fix auto-resolution validation is fail-closed for missing or unsupported markers, preserves generic non-review-fix `Files changed:` dispositions, validates driver classifications, requires same-review rerun/current-artifact proof, enforces exact-reviewer-wording constraints, rejects owner/architecture/scope decisions, and enforces budgets.
- Skill tests prove user-facing command guidance, chat result fields, proposal-side bounds, direct-review isolation, and existing profile preservation.
- Adapter distribution tests prove fixture release metadata can represent current non-portable skill exclusions without changing tracked adapter support surfaces.

## Validation Evidence Available Before Final Verify

Recorded passing evidence includes:

- `python scripts/test-change-metadata-validator.py`
- `python scripts/test-review-artifact-validator.py`
- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/test-build-skills.py`
- `python scripts/test-adapter-distribution.py`
- `bash scripts/ci.sh --mode explicit --path specs/review-fix-autoprogression.md --path specs/review-fix-autoprogression.test.md --path skills/workflow/SKILL.md --path docs/workflows.md --path scripts/test-adapter-distribution.py --path docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/behavior-preservation.md --path docs/plans/2026-06-30-bounded-review-fix-autoprogression-in-chat.md --path docs/plan.md --path docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml`

This is pre-verify evidence only. Final `verify` has not run yet, hosted CI has not been observed in this stage, and PR readiness is not claimed by this artifact.

## Review Resolution Summary

`review-resolution.md` is closed with 10 resolved findings and 0 unresolved findings.

Dispositions:

- Accepted: `AUTO-PR1`, `AUTO-PR2`, `SR-RFA-1`, `SR-RFA-2`, `AR-RFA-1`, `PR-RFA-1`, `CR-RFA-M2-1`, `CR-RFA-M3-1`, `CR-RFA-M3-2`
- Partially accepted: `AUTO-PR3`

The partially accepted item kept loop/edit budgets and fail-closed review-fix proof, but rejected dry-run/apply-mode state by owner decision.

## Alternatives Rejected

- Keep the loop fully manual: rejected because the repetitive safe-fix/rereview/next-stage sequence is low-value manual routing.
- Make review skills auto-fix and auto-continue by default: rejected because review skills are gates and direct review invocations must remain isolated.
- Add a global continue-until-done mode: rejected because implementation, verify, PR, release, publication, network, destructive, and external-state operations have different authority boundaries.
- Add dry-run/apply-mode state: rejected by owner direction in favor of a simpler explicit arming model.
- Include implementation, code-review, verify, PR, or release in this profile: rejected because this profile is proposal-side only and existing profiles own later workflow stages.
- Hand-edit generated public adapter package output: rejected by repository policy; canonical skills and adapter support metadata remain the source surfaces.

## Scope Control

The profile is explicitly bounded to proposal-side lifecycle stages through `test-spec-review`. It never invokes `implement`, `code-review`, `verify`, `pr`, release, publication, network, destructive, or external-state operations. Direct review invocations remain isolated. Review skills do not edit their reviewed artifacts during review. Review-fix metadata does not own active plan state, final closeout, branch readiness, or PR readiness.

The implementation also preserves existing `authoring-through-plan-review` and `implementation-through-verify` semantics.

## Risks And Follow-Ups

- Final `verify` remains pending and must decide overall branch readiness from the full artifact/code/test state.
- PR handoff remains pending after verify.
- The branch contains earlier release-transaction commits outside this active change range; this explanation is scoped to the review-fix change files and lifecycle artifacts.
- Adapter support surfaces were not changed because the install contract and supported skill list did not change; future adapter changes should continue to avoid hand-editing generated package output.

## Readiness

Ready for `verify`.

This artifact explains the reviewed implementation and available evidence. It does not claim final verify success, branch-ready state, PR-ready state, or hosted CI completion.
