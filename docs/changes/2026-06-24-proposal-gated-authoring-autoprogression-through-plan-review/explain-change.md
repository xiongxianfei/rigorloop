# Explain Change: Proposal-Gated Authoring Autoprogression Through Plan Review

## Summary

This change adds a bounded, explicitly armed `authoring-through-plan-review`
workflow profile. The profile lets a workflow-managed change continue after a
clean proposal gate through `spec`, `spec-review`, recorded architecture
assessment, conditional `architecture` and `architecture-review`, `plan`, and
`plan-review`, then stop with `test-spec` reported as the next stage.

The implementation keeps the profile change-local, persists authorization before
activation, preserves direct-review isolation, records formal reviews before
downstream action, fails closed on ambiguity, and does not start `test-spec`,
implementation, verification, PR, release, deploy, merge, or review-fix loops.

## Problem

The accepted proposal identifies a workflow gap: after a proposal has been
accepted and proposal-review is clean, users still have to manually trigger
several deterministic authoring and review stages. The goal was to remove those
redundant prompts without turning the workflow into unrestricted autopilot.

## Decision Trail

| Source | Decision |
| --- | --- |
| Proposal | Use a bounded opt-in profile instead of `auto=true`; preserve proposal approval as the human decision checkpoint; stop after clean `plan-review`. |
| `specs/workflow-stage-autoprogression.md` | Defines closed values `off` and `authoring-through-plan-review`, durable authorization persistence, gate activation, architecture assessment, review independence, stop conditions, transition budget, and completion boundary. |
| `specs/rigorloop-workflow.md` | Carries the workflow-level stage-order, isolation, policy metadata, direct-review, and profile state rules. |
| ADR | Records the durable decision for a separately armed profile, `auto-through: plan-review` mapping, change-local persistence, architecture-assessment routing, and stop-before-`test-spec` boundary. |
| Architecture | Updates the canonical system architecture with the no-service/no-background-worker profile design, policy ownership boundary, audit trail, and generated-guidance impact. |
| Plan | Splits implementation into five milestones: policy persistence, routing/state gates, skill alignment, generated/adapter validation, and integrated behavior-preservation proof. |

## Diff Rationale By Area

| Area | Files | Change | Reason | Test/evidence |
| --- | --- | --- | --- | --- |
| Proposal/spec/test contract | `docs/proposals/...md`, `specs/workflow-stage-autoprogression.md`, `specs/workflow-stage-autoprogression.test.md`, `specs/rigorloop-workflow.md`, `specs/rigorloop-workflow.test.md` | Added the profile contract, examples, requirements, acceptance criteria, stop rules, persistence tightening, and APGA/T test coverage. | Convert the accepted proposal into normative workflow behavior and executable/manual proof obligations. | `spec-review-r2`; T11-T17; APGA-001 through APGA-037. |
| Architecture and ADR | `docs/architecture/system/architecture.md`, `docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md` | Recorded the durable profile decision and current architecture impact. | The change affects workflow orchestration, profile policy persistence, review independence, and generated guidance. | `architecture-review-r1`. |
| Profile policy metadata | `schemas/change.schema.json`, `scripts/validate-change-metadata.py`, `scripts/change_metadata_semantics.py`, `scripts/query-change-record.py`, `scripts/test-change-metadata-validator.py`, change metadata fixtures | Added validated `workflow.autoprogression` policy shape, closed profile values, required authorization fields, cancellation semantics, fallback evidence rules, and query output support. | Durable change-local authorization is an activation precondition; policy metadata must not own live workflow state. | M1 validation: 26 change-metadata tests and metadata validation. |
| Workflow routing and lifecycle state | `scripts/lifecycle_state_sync.py`, `scripts/artifact_lifecycle_validation.py`, `scripts/test-artifact-lifecycle-validator.py`, `skills/workflow/SKILL.md`, `docs/workflows.md` | Added authoring profile route evaluation, profile-state gates, resume/cancel handling, architecture assessment outcomes, stop reasons, transition budget behavior, and fail-loud active handoff parsing. | The workflow must advance only through approved profile states and must pause instead of silently skipping or restarting. | M2 validation: 108 lifecycle tests after CR-M2 fixes. |
| Stage skill guidance | `skills/proposal-review/SKILL.md`, `skills/spec/SKILL.md`, `skills/spec-review/SKILL.md`, `skills/architecture/SKILL.md`, `skills/architecture-review/SKILL.md`, `skills/plan/SKILL.md`, `skills/plan-review/SKILL.md`, `scripts/test-skill-validator.py` | Aligned stage skills so workflow-managed profile execution can continue through deterministic stages while direct review requests remain isolated and reviews stay independent. | Consecutive stages must not collapse authoring and review into one self-certifying pass. | M3 validation: 231 skill-validator tests and `validate-skills.py`. |
| Generated and adapter guidance proof | `scripts/build-skills.py`, `scripts/test-build-skills.py`, `scripts/test-adapter-distribution.py`, `dist/adapters/README.md`, `dist/adapters/manifest.yaml`, `scripts/adapter_templates/` | Left generator and adapter support surfaces unchanged with explicit rationale after validation. | Existing generation and adapter surfaces already preserve canonical-source boundaries and do not imply broader autoprogression. | M4 validation: `build-skills.py --check`, 7 build tests, 129 adapter tests, 23 skill files validated. |
| Behavior preservation and lifecycle evidence | `docs/changes/.../behavior-preservation.md`, `review-log.md`, `review-resolution.md`, `reviews/*.md`, active plan, `docs/plan.md`, `change.yaml` | Recorded integrated APGA behavior proof, formal reviews, review-resolution closeout, validation history, and current handoff state. | The first slice needs an audit trail showing what ran, why it stopped or continued, and which stages remain. | M5 validation and `code-review-m5-r1`. |

## Tests Added Or Changed

| Test/proof | What it proves | Why this level is appropriate |
| --- | --- | --- |
| Change metadata validator tests | Valid and invalid profile policy records, closed profile values, missing/malformed/partial records, cancellation, pre-pack arming, and fallback behavior. | Policy persistence is structured data and belongs in schema/semantic fixture tests. |
| Artifact lifecycle validator tests | Profile routing, proposal gate activation, architecture assessment, stop reasons, pause/completed/resume semantics, transition budget, contradictory state, and active handoff parsing. | v1 is guidance- and validator-driven, so workflow-state behavior is proved through lifecycle fixtures rather than a runtime router. |
| Skill validator tests | Stage skills preserve direct-review isolation, review independence, and bounded profile guidance. | Skill text is user-facing contract; static assertions prevent guidance drift. |
| Build/generation tests | Canonical skills remain valid and local generated skill output remains reproducible. | Generated output must stay derived from canonical skills. |
| Adapter distribution tests | Public adapter support boundaries remain valid and do not imply tracked generated public adapter bodies or broader autoprogression. | Adapter compatibility is a distribution contract, not profile runtime logic. |
| `behavior-preservation.md` T17 proof | Default-off behavior, architecture-required/not-required/ambiguous paths, stop paths, direct-review isolation, review evidence, and no `test-spec` or implementation start. | The approved test spec says no end-to-end router harness exists in v1; manual integration proof plus repo-owned validators is the intended proof surface. |

## Validation Evidence Available Before Final Verify

The following validation has been recorded in the active plan and change
metadata before final `verify`:

- `python scripts/test-change-metadata-validator.py`
- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/test-skill-validator.py`
- `python scripts/test-build-skills.py`
- `python scripts/test-adapter-distribution.py`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`
- `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `bash scripts/ci.sh --mode explicit ...`
- `git diff --check -- ...`

Final `verify`, hosted CI, branch readiness, PR-body readiness, and PR-open
readiness are not claimed by this artifact.

## Review Resolution Summary

Review-resolution closeout is recorded in
`docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md`.

- Findings resolved: 3
- Unresolved findings: 0
- Accepted findings: `SR-APGA-001`, `CR-M2-001`, `CR-M2-002`
- Clean later review rounds: `spec-review-r2`, `architecture-review-r1`, `plan-review-r1`, `code-review-m1-r1`, `code-review-m2-r2`, `code-review-m3-r1`, `code-review-m4-r1`, `code-review-m5-r1`

## Alternatives Rejected

| Alternative | Why rejected |
| --- | --- |
| Keep explicit triggering for every post-proposal stage | It keeps users acting as manual routers for deterministic transitions after the proposal gate has already carried the main judgment. |
| Add `auto=true` | The scope is ambiguous and could be mistaken for permission to skip architecture, advance after findings, auto-fix, start implementation, or affect isolated reviews. |
| Widen default autoprogression | Direct review-only requests and profile-off behavior must remain stable. |
| Use session-only authorization | Resumed workflows need durable evidence explaining why automatic transitions were authorized. |
| Make `change.yaml` the live state owner | The active plan remains the live state owner for planned initiatives; change metadata records policy and evidence only. |
| Continue through `test-spec` or implementation | Those stages cross different risk boundaries and require separate proposals and measured adoption evidence. |

## Scope Control

The change preserves the accepted non-goals:

- no automatic proposal approval;
- no automatic review-fix loop;
- no `test-spec`, implementation, verification, PR, release, deploy, merge, or destructive Git automation from this profile;
- no repository-wide default;
- no direct-review autoprogression;
- no fast-lane, bugfix, or on-demand stage automation changes;
- no live next-stage ownership by `change.yaml`.

## Risks And Follow-Ups

| Risk or follow-up | Status |
| --- | --- |
| Future pressure to add `authoring-through-test-spec` | Deferred; requires a separate proposal and measured safe adoption evidence. |
| Future implementation autoprogression | Out of scope; requires a separate profile and safety design. |
| Runtime router coverage | Intentionally absent in v1 because no repo-owned workflow router exists. |
| Final verification | Pending downstream `verify`. |
| PR readiness | Pending `verify` and `pr`; not claimed here. |

## Current Handoff

All in-scope implementation milestones are closed. The active plan remains
`active` because final lifecycle gates are still pending.

Next stage: `verify`.
