# Explain Change: Separately Armed Implementation Autoprogression Through Verify

## Summary

This change adds the first implementation slice for a separately authorized `implementation-through-verify` autoprogression profile.

The implementation records the profile as change-local policy, evaluates activation and phase gates, settles test-spec readiness before implementation, enforces reviewer-owned auto-fix classifications, bounds automatic correction loops, updates public skill guidance, and adds behavior-preservation evidence. It deliberately stops before automatic Phase C execution, final `verify`, PR opening, deployment, publication, branch push, or other external effects.

## Problem

The accepted proposal identified repeated manual routing after clean planning: `test-spec`, milestone implementation, code review, eligible mechanical correction, rereview, explanation, and verification often have deterministic next steps. At the same time, implementation crosses materially different risk surfaces from authoring: code execution, dependency mutation, generated output, test fixtures, review-driven correction, validation cost, and PR/publication boundaries.

The selected design therefore adds a sibling profile rather than widening `authoring-through-plan-review`. The core invariant is that implementation automation requires separate recorded user authority, and reviewer-declared correction authority is the only basis for automatic review-driven fixes.

## Decision Trail

| Decision layer | Decision |
| --- | --- |
| Proposal | Add `implementation-through-verify`, user-facing `auto-through: verify`, stop before PR, and keep automatic owner decisions, verify-failure repair, deployment, publication, and project-wide defaults out of scope. |
| Spec | `workflow-stage-autoprogression` R2am-R2bz defines the profile, phase gates, test-spec settlement, milestone ordering, correction-loop bounds, Phase C guards, and PR boundary. |
| Workflow contract | `rigorloop-workflow` R7et-R7fad maps the same behavior into the standard workflow and keeps manual/bugfix invocations isolated by default. |
| Review-finding contract | `review-finding-resolution-contract` R1e-R1l and R11 define `auto_fix_class`, required mechanical/declared-safe fields, and structural validation for implementation-profile findings. |
| Architecture and ADR | The canonical architecture and ADR record the durable boundary: no new service or external actor, profile policy is not live workflow state, corrections are reviewer-owned, Phase C requires fresh evidence, and PR remains human-controlled. |
| Plan | M1-M5 split the work into profile metadata, route evaluation, review classification/guardrails, skill/adapters guidance, and final behavior-preservation proof. |

## Diff Rationale By Area

| Files | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `docs/proposals/2026-06-24-separately-armed-implementation-autoprogression-through-verify.md`, `docs/changes/**/reviews/proposal-review-r1.md` | Recorded and reviewed the proposal direction. | Establishes the selected implementation profile, separate authorization, bounded loops, Phase A/B/C rollout, and stop-before-PR boundary before spec work. | Proposal goals, non-goals, acceptance criteria `AC-ITV-001`-`AC-ITV-025`. | Proposal-review R1 approved with no material findings. |
| `specs/workflow-stage-autoprogression.md`, `specs/rigorloop-workflow.md`, `specs/review-finding-resolution-contract.md`, `docs/changes/**/reviews/spec-review-r1.md` | Added normative implementation-profile requirements and finding classification requirements. | Converts the proposal into enforceable workflow, route, correction, and review-record contracts. | R2am-R2bz, R7et-R7fad, R1e-R1l, R11. | Spec-review R1 approved with no material findings. |
| `docs/architecture/system/architecture.md`, `docs/adr/ADR-20260624-implementation-through-verify-autoprogression.md`, `docs/changes/**/reviews/architecture-review-r1.md` | Updated durable architecture and ADR surfaces for phase gating, policy ownership, correction-loop safety, fresh verify, and PR boundary. | The change affects workflow orchestration, persistence semantics, and review authority, so the architecture package needed to record long-lived decisions. | Architecture sections on workflow profiles and ADR decision/consequences. | Architecture-review R1 approved with no material findings. |
| `docs/plans/2026-06-24-implementation-autoprogression-through-verify.md`, `docs/plan.md`, `docs/changes/**/reviews/plan-review-r1.md` | Created and maintained the five-milestone execution plan and active index. | Keeps implementation slices reviewable and makes the active handoff state the live workflow owner. | Plan M1-M5 and current handoff summary. | Plan-review R1 approved; lifecycle explicit-path validation passed after each handoff. |
| `specs/implementation-autoprogression-through-verify.test.md` | Added test-spec coverage for T1-T15 and acceptance/test-check proof obligations. | Maps each approved requirement, edge case, and milestone to concrete validation or manual proof before implementation. | Proposal `ITV-001`-`ITV-039`, `AC-ITV-001`-`AC-ITV-025`. | User approved test spec before implementation. |
| `schemas/change.schema.json`, `scripts/validate-change-metadata.py`, `scripts/query-change-record.py`, `scripts/test-change-metadata-validator.py`, `tests/fixtures/change-metadata/implementation-autoprogression-container-next-stage/change.yaml` | Added implementation-profile metadata schema, semantic validation, query exposure, independent authorization fields, phase/state validation, and live-state rejection. | Profile policy must persist separately from authoring authorization and must never own current stage, next stage, review status, branch readiness, or PR readiness. | R2am-R2ar, R7et-R7ew, R7er. | M1 tests, M1 R2 clean review, and direct invalid-fixture proof for forbidden live-state fields. |
| `scripts/lifecycle_state_sync.py`, `scripts/test-artifact-lifecycle-validator.py` | Added implementation-profile route evaluation, activation gates, phase A/B/C boundaries, test-spec settlement identity checks, ordered milestone routing, idempotent resume, correction-loop guardrails, path locality, CI deny-list gating, and fresh closeout routing guards. | The orchestrator needs deterministic route decisions and fail-closed stop reasons before any automatic transition or correction can run. | R2as-R2bd, R2bm-R2bu, R7eu-R7fab. | M2 and M3 lifecycle tests; M2 R1 and M3 R2 clean reviews. |
| `scripts/review_artifact_validation.py`, `scripts/test-review-artifact-validator.py` | Added parser-owned validation for implementation-profile material finding fields. | Automatic correction eligibility must be recorded by code review, not inferred from severity or wording. | R1e-R1l and R11. | `python scripts/test-review-artifact-validator.py` and focused `-k auto_fix` passed. |
| `skills/workflow/SKILL.md`, `skills/test-spec/SKILL.md`, `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, `skills/explain-change/SKILL.md`, `skills/verify/SKILL.md`, `skills/plan/SKILL.md`, `skills/plan-review/SKILL.md`, `scripts/test-skill-validator.py` | Updated user-facing and agent-facing skill guidance for the profile, phase boundaries, reviewer-declared corrections, final full review, explain-change/verify boundaries, verify-failure pause, and human PR authorization. | The runtime behavior depends on skill guidance as well as validators; published guidance must not imply Phase C or PR automation before allowed. | R2bv-R2bz, R7fac-R7fad, M4. | Skill validation, build-skills check, adapter build/validation, adapter distribution tests, and M4 R1 clean review. |
| `docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/behavior-preservation.md` | Added the M5 behavior-preservation matrix, acceptance-criteria coverage, test-check coverage, falsification checklist, rollout placeholders, and boundary statement. | Proves the first slice preserves authoring behavior, avoids `test-spec-review`, keeps owner decisions manual, preserves review independence, and stops before PR. | Test-spec T14/T15 and proposal behavior-preservation proof. | `python scripts/test-skill-validator.py -k implementation_through_verify` and M5 R1 clean review. |
| `docs/changes/**/review-log.md`, `docs/changes/**/review-resolution.md`, `docs/changes/**/reviews/*.md`, `docs/changes/**/change.yaml` | Recorded formal lifecycle reviews, material finding dispositions, validation evidence, latest review pointers, and changed files. | The workflow requires durable evidence for every formal review and material finding, and future maintainers need a reconstructable audit trail. | Review-finding contract and workflow review-recording rules. | Review artifact validation passed in structure and closeout modes. |

## Tests Added Or Changed

| Test area | What it proves | Why this level fits |
| --- | --- | --- |
| Change metadata validator tests | Closed profile values, independent implementation authorization, phase/state enforcement, forbidden live-state fields, legacy compatibility, and query exposure. | Unit/fixture tests directly exercise metadata shape and semantic validation. |
| Artifact lifecycle validator tests | Activation gates, Phase A/B/C refusal, test-spec settlement, settlement identity mismatch, ordered milestones, idempotent resume, correction-round caps, shrinking/no-new-finding rules, path locality, scope-budget stops, command boundaries, CI deny-list stops, and audit evidence. | Workflow routing is table/fixture-heavy, so fixture tests make each stop reason directly inspectable. |
| Review artifact validator tests | Missing `auto_fix_class`, unsupported class/kind, incomplete mechanical fields, incomplete declared-safe recipes, and production-code proof requirements are rejected. | Parser-owned structural validation is the right level for review-record shape. |
| Skill validator tests | Public skill surfaces expose the implementation profile, phase boundaries, promotion evidence, fresh verify evidence, verify-failure pause, stop-before-PR, behavior-preservation coverage, and absence of `test-spec-review`. | Static public-surface checks prevent guidance drift without relying on generated adapters as source. |
| Adapter and generated-skill tests | Canonical skill updates remain buildable and packageable for supported adapter outputs. | Generated output is not hand-edited; build/adapter validation proves canonical changes propagate safely. |
| Behavior-preservation matrix | Cross-surface proof for all `ITV-001`-`ITV-039` and `AC-ITV-001`-`AC-ITV-025`. | This is a manual/evidence artifact by design because it links several milestone-level proof surfaces. |

## Validation Evidence Available Before Final Verify

Recorded passing evidence includes:

- `python scripts/test-change-metadata-validator.py -k autoprogression_policy`
- `python scripts/test-change-metadata-validator.py -k named_autoprogression_policy`
- `python scripts/test-change-metadata-validator.py -k forbidden_live_state`
- `python scripts/test-change-metadata-validator.py -k forbidden`
- `python scripts/test-change-metadata-validator.py`
- `python scripts/validate-change-metadata.py docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/change.yaml`
- `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/implementation-autoprogression-container-next-stage/change.yaml` with expected failure for forbidden live-state fields.
- `python scripts/test-artifact-lifecycle-validator.py -k implementation_profile`
- `python scripts/test-artifact-lifecycle-validator.py -k correction_guardrails`
- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/test-review-artifact-validator.py -k auto_fix`
- `python scripts/test-review-artifact-validator.py`
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/`
- `python scripts/test-skill-validator.py -k implementation_through_verify_public_skill_surfaces`
- `python scripts/test-skill-validator.py -k implementation_through_verify`
- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/test-build-skills.py`
- `python scripts/build-adapters.py --version v0.1.3 --output-dir /tmp/rigorloop-adapters-m5`
- `python scripts/validate-adapters.py --root /tmp/rigorloop-adapters-m5 --version v0.1.3`
- `python scripts/test-adapter-distribution.py`
- scoped `git diff --check` commands for implementation and review handoffs.

This evidence is pre-final-verify evidence. It does not claim final `verify`, hosted CI success, branch readiness, PR readiness, or PR opening.

## Review Resolution Summary

Formal review records exist for proposal-review, spec-review, architecture-review, plan-review, and code-review M1 through M5.

Material finding summary:

| Disposition | Count |
| --- | ---: |
| accepted/resolved | 3 |
| rejected | 0 |
| deferred | 0 |
| partially-accepted | 0 |
| needs-decision | 0 |
| open | 0 |

The accepted findings were:

- `CR-M1-R1-F1`: autoprogression policy containers could carry forbidden live workflow-state fields.
- `CR-M3-R1-F1`: correction path locality could bypass reviewer-declared affected paths.
- `CR-M3-R1-F2`: mechanical correction eligibility did not require deterministic authority.

Detailed dispositions and validation evidence are in `docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/review-resolution.md`, whose closeout status is `closed`.

## Alternatives Rejected

| Alternative | Why it was rejected |
| --- | --- |
| Widen `authoring-through-plan-review` into implementation. | Authoring and implementation have different authority and risk surfaces; implementation needs separate authorization. |
| Add unrestricted `auto=true`. | It has no bounded meaning and would invite inferred auto-fix safety and external effects. |
| Infer auto-fixability from severity, wording, file count, or apparent simplicity. | The reviewer must declare eligibility; the orchestrator cannot choose owner intent. |
| Add `test-spec-review` in this slice. | The approved topology uses deterministic test-spec settlement and a static absence check for the review skill/stage. |
| Enable automatic Phase C immediately. | Phase C requires dogfood promotion evidence; the first slice guards it rather than enabling it. |
| Automatically repair verify failures. | Verify failures occur after review and explanation; automatic repair would bypass the human decision boundary. |
| Automatically open PRs or publish/deploy. | PR opening and publication are external-boundary actions and remain explicit human actions. |

## Scope Control

Preserved non-goals:

- No automatic PR opening, branch push, deployment, package publication, hosted reviewer notification, or external posting.
- No automatic verify-failure repair.
- No project-wide default implementation profile.
- No background/asynchronous execution.
- No automatic owner-decision resolution.
- No new `test-spec-review` skill or lifecycle stage.
- No substantive automatic edits to proposal, spec, test-spec, architecture, ADR, plan, constitution, workflow policy, release policy, or security policy during correction loops.

## Risks And Follow-Ups

- Phase C remains designed but not enabled until promotion evidence exists.
- Automatic PR opening, verify-failure repair, and project-wide default profiles still require separate proposals.
- Final `verify` still needs to run fresh actual evidence before PR handoff.
- The active plan remains `active` until verify and PR handoff complete the lifecycle.

## Readiness

All implementation milestones are closed and code-reviewed, review-resolution closeout is closed, and this explanation records the implementation rationale. The next workflow stage is `verify`.

This artifact does not claim final `verify`, branch readiness, PR readiness, hosted CI success, or PR opening.
