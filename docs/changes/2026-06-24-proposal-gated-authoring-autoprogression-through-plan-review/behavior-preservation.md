# Behavior Preservation: Proposal-Gated Authoring Autoprogression Through Plan Review

## Scope

This proof records integrated behavior preservation for the
`authoring-through-plan-review` first slice. It covers the accepted proposal
boundary, the approved spec and workflow amendments, the `SR-APGA-001`
persistence tightening, implementation milestones M1 through M4, and the final
T17 proof surface before M5 code-review.

The first slice is guidance-, artifact-, and validator-driven. It does not add a
runtime workflow router, queue, daemon, background worker, or end-to-end router
harness. The repository-owned proof is therefore the combination of fixture
validators, canonical skill guidance, generated-skill drift checks, adapter
support checks, formal review records, and this behavior-preservation matrix.

## Baseline Preservation Matrix

| Surface | Baseline | New proof | Result |
| --- | --- | --- | --- |
| Proposal-to-proposal-review | Existing workflow-managed autoprogression | unchanged | preserved |
| Direct proposal-review | isolated | still isolated | preserved |
| Proposal-review-to-spec | explicit user action | profile-controlled automatic transition | intentionally extended |
| Spec-to-spec-review | already bounded automatic pair | unchanged | preserved |
| Architecture-to-review | already bounded automatic pair | unchanged | preserved |
| Spec-review routing | architecture or plan | unchanged | preserved |
| Plan-review routing | test-spec | still next stage; not auto-run | preserved |
| Review findings | stop/manual resolution | unchanged in first slice | preserved |
| Fast lane | explicit-step | unchanged | preserved |
| Bugfix lane | explicit-step | unchanged | preserved |
| Implementation chain | existing bounded behavior | unchanged | preserved |
| Review recording | formal evidence required | unchanged | preserved |
| Profile authorization persistence | optional/advisory | mandatory durable record; pause on absence or failure | intentionally tightened |

## APGA Boundary Proof

| Boundary | Evidence | Result |
| --- | --- | --- |
| Default profile is `off`; unknown profiles fail closed | `scripts/test-change-metadata-validator.py`; `scripts/test-artifact-lifecycle-validator.py`; `schemas/change.schema.json`; `scripts/change_metadata_semantics.py` | preserved and fixture-backed |
| Authorization must be explicit and durable before activation | `workflow.autoprogression` schema and semantic validation; APGA-031 through APGA-036 fixtures; `authorization-not-persisted` route handling | intentionally tightened |
| Pre-pack arming is session intent only | Change-metadata validator fixtures and workflow guidance require re-assertion once the change pack exists | preserved safety boundary |
| Proposal gate activates only when accepted proposal and recorded clean proposal-review evidence exist | Workflow routing guidance plus formal proposal-review receipt in `reviews/proposal-review-r1.md` | preserved human proposal gate |
| Direct review invocations remain isolated | Canonical stage skills, workflow guidance, and skill-validator assertions for direct `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, `code-review`, `verify`, and `explain-change` requests | preserved |
| Clean `spec-review` routes through recorded architecture assessment | Workflow route evaluator guidance and artifact-lifecycle validator coverage for `architecture-required`, `architecture-not-required`, and `architecture-ambiguous` | preserved; ambiguity pauses |
| Required architecture is not skipped | Architecture-required path is recorded in the approved architecture and ADR, and validated by workflow routing fixtures | preserved |
| Review independence remains formal and recorded | Canonical review skills require tracked-artifact review targets, formal criteria, and recorded evidence before downstream action | preserved |
| Non-clean review statuses, material findings, owner decisions, missing evidence, ambiguous architecture, and contradictory state pause | Artifact-lifecycle validator fixtures for route stop reasons, review-resolution records for material findings, and fail-loud handoff parsing | preserved |
| Paused and completed profiles do not restart automatically | CR-M2-001 resolution added terminal state gates and durable resume/cancel route semantics | preserved |
| Duplicate or partial stage execution is not inferred from file existence | Artifact lifecycle validation requires structured evidence and fails on incomplete or unparseable active handoff state | preserved |
| Transition budget remains bounded | Workflow routing guidance and validator tests enforce the six-slot `authoring-through-plan-review` budget and fail closed on unexpected cycles | preserved |
| Clean `plan-review` completes the profile and reports `test-spec` next | Spec, workflow guidance, plan-review handoff wording, and skills all stop before `test-spec` invocation | preserved |
| The profile cannot start `test-spec`, implementation, code-review, explain-change, verify, PR, merge, release, deploy, or destructive Git actions | Approved spec, ADR, canonical skill wording, and T17 manual proof explicitly keep those stages outside this profile | preserved |
| Fast-lane and bugfix execution remain explicit-step | Workflow guidance and canonical skill alignment did not broaden manual skill or bugfix execution behavior | preserved |
| Generated and adapter-facing guidance remains aligned | `python scripts/build-skills.py --check`, `python scripts/test-build-skills.py`, `python scripts/test-adapter-distribution.py`, and `python scripts/validate-skills.py` | preserved |

## Review And Audit Evidence

| Evidence surface | Proof |
| --- | --- |
| Formal reviews | Proposal-review R1, spec-review R1/R2, architecture-review R1, plan-review R1, code-review M1 R1, code-review M2 R1/R2, code-review M3 R1, and code-review M4 R1 are recorded under `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/`. |
| Review findings | `SR-APGA-001`, `CR-M2-001`, and `CR-M2-002` have final dispositions in `review-resolution.md`; `review-log.md` has no open material findings. |
| Milestone proof | M1 covers durable policy persistence, M2 covers workflow routing and state gates, M3 covers canonical skill alignment, M4 covers generated-skill and adapter validation, and M5 records integrated proof. |
| Active state owner | The active plan `Current Handoff Summary` owns live milestone and next-stage state; `change.yaml` records scoped evidence and changed files only. |

## Result

The implemented first slice preserves default behavior, direct-review isolation,
manual skill and bugfix explicit-step behavior, formal review recording, and the
existing stage order while intentionally extending only the approved
workflow-managed `proposal-review -> spec` boundary for durably authorized
`authoring-through-plan-review` profiles.

The profile remains bounded to authoring through clean `plan-review`. It reports
`test-spec` as the next stage, records profile completion, and does not start
`test-spec`, implementation, PR, or any external-boundary action.
