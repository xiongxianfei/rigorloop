# Explain Change: Stage Evidence Access Contracts M3/M4 Static Validation And Measurement

## Summary

This change completes the M3/M4 follow-through slice for stage evidence access contracts.

M3 audited the existing stage evidence access static validator coverage and recorded a no-change rationale because current concept checks already cover the required evidence-access concepts. M4 ran static skill token measurement and recorded that canonical skill size is unchanged from the M2 merged baseline: 23 skills, 235521 bytes, and 58868 estimated tokens.

The change also closes stale M2 lifecycle state after PR #60 merged, creates and advances the M3/M4 lifecycle artifacts, records formal plan and code reviews, and keeps the next stage at `verify`.

## Problem

The accepted stage evidence access contract rollout needed two follow-through steps after M1 and M2:

- M3: prevent accidental removal of evidence-access guidance with concept-based static checks, but only add checks when existing coverage is insufficient.
- M4: run static skill token measurement and record whether skill size increased, decreased, or stayed unchanged.

The work also needed to avoid expanding into runtime enforcement, semantic read auditing, hard token gates, lifecycle token-cost reports, dynamic benchmarks, release validation, adapter packaging, or generated-output source-model changes.

## Decision Trail

| Source | Decision or requirement | How this change follows it |
|---|---|---|
| Proposal | Use M3 for static validation and M4 for measurement after M1/M2. | Created a focused M3/M4 plan instead of reopening M1 or M2. |
| Spec `R30` | Static checks, when added, must be concept-based and avoid exact long paragraph locks. | M3 audited existing concept checks and avoided adding duplicative or brittle assertions. |
| Spec `R31` | Concept checks may cover evidence access, default evidence, conditional evidence, reason recording, bounded evidence before broad reads, and full-file-read escape behavior. | M3 mapped existing checks to those concepts and recorded them as covered. |
| Spec `R32` | No runtime enforcement, semantic read auditing, hard token gates, lifecycle token-cost summary, release validation, adapter packaging, generated-output source model, or dynamic benchmark expansion. | The diff changes lifecycle artifacts and test-spec expectations only; no runtime, release, adapter, or generated-output behavior changed. |
| Spec `R33` | Static skill token measurement remains diagnostic and warning-only. | M4 records the static measurement and unchanged delta without creating a gate. |
| Spec `R34` | Safety-critical review, validation, material-finding, source-of-truth, verify, PR, and release rules remain intact. | Formal reviews were recorded and no review-resolution was created because there were no material findings. |
| Plan M0 | Align the test spec before M3/M4 implementation. | Added explicit T15 and T16 proof coverage for M3 and M4, then recorded maintainer approval. |
| Plan M3 | Audit existing validator checks before changing them. | Confirmed current checks are sufficient; `scripts/test-skill-validator.py` was not edited. |
| Plan M4 | Measure static skill size against the M2 baseline. | Recorded 0 delta from the M2 baseline. |

No architecture or ADR change was required because this is repository workflow validation and measurement work, not a runtime architecture change.

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml` | Closed the M2 change metadata following PR #60 landing with hosted CI success. | M3/M4 relies on the M2 execution/review evidence-access slice being merged and lifecycle-closed. | Active M3/M4 plan dependency. | PR #60 merge and hosted CI evidence recorded in M3/M4 metadata. |
| `docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md` | Marked the M2 plan done following PR #60 landing. | Prevents stale active-plan state before starting the M3/M4 follow-through plan. | Plan index lifecycle rules. | Lifecycle validation passed after planning. |
| `docs/plan.md` | Moved M2 to done and tracked M3/M4 as the active plan through implementation, reviews, and explain-change. | Keeps the plan index aligned with the active plan's Current Handoff Summary. | `AGENTS.md` and workflow state-sync rules. | Artifact lifecycle validation and state-sync notes. |
| `docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md` | Added the active execution plan, M0/M3/M4 milestones, static validation audit, measurement table, progress, decisions, and validation notes. | Provides the living lifecycle owner for this planned initiative. | Approved spec and M3/M4 proposal rollout. | Plan-review, code-review, lifecycle validation, and measurement evidence. |
| `specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md` | Added explicit M3/M4 proof expectations and requirement mappings. | Makes static validation and measurement proof durable before implementation. | Approved M3/M4 plan M0. | Maintainer approval and test-spec alignment validation. |
| `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml` | Added change metadata, requirements, review status, validation evidence, M3 no-change rationale, and M4 measurement result. | Keeps the change-local metadata aligned with the plan and review artifacts. | Workflow change metadata contract. | `validate-change-metadata.py` and artifact lifecycle validation. |
| `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/review-log.md` | Added the formal review ledger. | Records every formal lifecycle review for this change. | Formal review recording rules. | Review artifact validation. |
| `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/reviews/plan-review-r1.md` | Recorded clean plan review. | Establishes readiness for test-spec alignment and implementation. | `plan-review` stage contract. | Review log entry. |
| `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/reviews/code-review-m3-r1.md` | Recorded clean-with-notes M3 code review. | Closes M3 without review-resolution because there were no material findings. | `code-review` stage contract. | Review log entry and plan state sync. |
| `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/reviews/code-review-m4-r1.md` | Recorded clean-with-notes M4 code review. | Closes all implementation milestones and hands off to explain-change. | `code-review` stage contract. | Review log entry and plan state sync. |
| `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/explain-change.md` | Added this durable rationale. | Makes the diff reviewable before final verify and PR handoff. | `explain-change` stage contract. | Explain-change validation in this stage. |

## Tests Added Or Changed

| Test ID or proof | What it proves | Why this level is appropriate |
|---|---|---|
| `T15` M3 Static Validation Audit And Gap Fill | Existing or added concept checks cover the evidence-access static validation expectations without phrase-locking. | Static validation is the requested M3 mechanism; no runtime enforcement is in scope. |
| `T16` M4 Static Measurement And Size-Delta Recording | Static skill token measurement is run and the size delta is recorded as diagnostic evidence. | M4 is a measurement milestone, not a behavior change or hard gate. |
| `python scripts/test-skill-validator.py` | Current skill validator checks pass, including existing stage evidence access concept checks. | Direct proof for M3. |
| `python scripts/measure-skill-tokens.py` | Static skill token measurement runs successfully and reports unchanged totals. | Direct proof for M4. |
| `python scripts/validate-skills.py` | Canonical skills remain valid after the measurement slice. | Confirms no skill-contract drift from this lifecycle work. |
| Lifecycle and change metadata validators | Plan, metadata, review, and lifecycle surfaces remain coherent. | This change is mostly lifecycle and workflow evidence, so those validators are the right proof surface. |

## Validation Evidence Available Before Final Verify

Validation already recorded before this explain-change stage:

- `python scripts/test-skill-validator.py` passed for M3 and M4.
- `python scripts/test-build-skills.py` passed during M3 validation.
- `python scripts/measure-skill-tokens.py` passed during M4 and reported 23 skills, 235521 bytes, and 58868 estimated tokens.
- `python scripts/validate-skills.py` passed during M4 validation.
- `python scripts/test-change-metadata-validator.py` passed during M0, M3, and M4 validation.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml` passed during M0, M3, and M4 validation.
- `python scripts/validate-artifact-lifecycle.py ...` passed for the relevant M0, M3, and M4 artifact sets.
- `python scripts/select-validation.py ...` passed for selected M0, M3, and M4 paths.
- `git diff --check -- ...` passed for M0, M3, and M4 changed paths.

Final `verify` has not run yet. This artifact records rationale only and hands off to `verify`.

## Review Resolution Summary

No material findings were recorded.

- `plan-review-r1`: approved, 0 material findings.
- `code-review-m3-r1`: clean-with-notes, 0 material findings.
- `code-review-m4-r1`: clean-with-notes, 0 material findings.

No `review-resolution.md` is required for this change.

## Alternatives Rejected

| Alternative | Reason rejected |
|---|---|
| Add new validator assertions anyway. | M3 found current checks already cover the required concepts; additional assertions would duplicate proof or lock phrasing. |
| Treat token measurement as a gate. | The spec requires static measurement to remain diagnostic and warning-only. |
| Run dynamic token benchmarks. | Dynamic benchmarks are out of scope unless a later approved plan or test spec requires them. |
| Update additional skills, including `plan`. | M3/M4 only validate and measure the M1/M2 evidence-access work; promoting future-slice skill guidance is out of scope. |
| Change release validation, adapter packaging, or generated-output policy. | The spec explicitly excludes those surfaces for this slice. |

## Scope Control

This change preserves the agreed non-goals:

- no runtime enforcement;
- no semantic read auditing;
- no hard token gates;
- no lifecycle token-cost summary implementation;
- no dynamic benchmark requirement;
- no release validation changes;
- no adapter packaging changes;
- no generated-output source-model changes;
- no additional skill rewrites;
- no weakening of formal review, validation, material-finding, source-of-truth, verify, PR, or release rules.

## Risks And Follow-Ups

Residual risks:

- Static checks can still drift if future skills add evidence-access wording outside the first-slice and M2 surfaces.
- Static token totals do not measure dynamic prompt or command-output savings.

Follow-ups:

- Future approved work can extend evidence-access concept checks if more skills adopt the contract.
- Dynamic benchmark comparison remains deferred until a later approved plan/test spec requires it.

## Readiness

This change is ready for `verify` after this explain-change artifact, active plan, plan index, and change metadata are validated and committed.
