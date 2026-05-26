# Explain Change: Spec-Review Testability Routing and Output Consolidation

## Summary

This change separates two concepts that `spec-review` previously mixed in prose:

- `Immediate next stage` is now a closed routing field that cannot be `test-spec`.
- `Eventual test-spec readiness` is now a separate quality assessment that remains required for approved `spec-review` outcomes.

The implementation adds fixture and canonical validation for that split, updates the canonical `spec-review` skill and result skeleton, aligns directly affected workflow and `test-spec` wording, preserves material-finding field ownership in the asset, and records generated-output proof for temporary public adapter archives.

The practical result is that `spec-review` can still say whether a spec is eventually ready for test-spec authoring, but it no longer routes directly to `test-spec` or implies an empty immediate-stage field.

## Problem

The accepted proposal identified two overloaded `test-spec` concepts in `spec-review`:

- direct routing to `test-spec`, which is wrong from `spec-review`;
- eventual readiness for test-spec authoring, which is a required quality gate for approval.

The old skill relied on scattered reminders to keep those concepts apart. That made the historical failure easy to repeat: a reviewer could put `test-spec` into the immediate routing field even though downstream workflow order still required architecture or plan.

The same area also had a smaller drift risk: material-finding field labels were described in both skill prose and `assets/material-finding.md`, even though the asset is supposed to own the field shape.

## Decision Trail

| Decision surface | Decision | Resulting implementation |
| --- | --- | --- |
| Proposal | Reject removing all `test-spec` mentions; keep readiness and structurally separate it from routing. | The skill and skeleton now expose separate `Immediate next stage` and `Eventual test-spec readiness` fields. |
| Spec R1-R3, R8 | Use closed enums, reject direct `test-spec` routing, require approved readiness, bind routing to status, and handle missing inputs with explicit `none`. | Validator helpers reject invalid enum values, approved/not-ready, status-routing contradictions, missing stop conditions, and unnamed conditional readiness. |
| Spec R4-R7 | Preserve workflow order, isolation, adjacent `plan-review -> test-spec` behavior, and generated-output consistency. | The change avoids workflow-stage redesign, updates only direct adjacent drift, and proves generated local skill and adapter archives. |
| Spec R8d | Keep material-finding field shape owned by `assets/material-finding.md`. | `SKILL.md` keeps the sufficiency rule and references the asset rather than duplicating the complete field list. |
| Test spec T1-T4 | First prove controlled result fixtures, then enable canonical skill/skeleton enforcement after canonical assets change. | M1 added controlled fixture validation; M2 enabled canonical enforcement. |
| Test spec T5-T9 | Preserve material-finding ownership, adjacent prerequisites, workflow boundaries, generated output, and lifecycle evidence. | M2/M3 added canonical, adjacent-drift, behavior-preservation, adapter, and lifecycle proof. |
| Plan | Use M1 fixture scaffolding, M2 canonical contract, M3 generated-output proof. | Each implementation slice reached a passable validation boundary before code review. |
| Architecture | Not required. | No architecture artifact was created because the work stays within skill text, assets, validation scripts, workflow wording, and generated-output proof. |

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `scripts/skill_validation.py` | Added `spec-review` result-field validation, canonical contract checks, allowed routing/readiness enums, status-to-routing checks, approval-readiness checks, stop-condition checks, and material-finding single-owner checks. | Makes the wrong immediate route structurally invalid and prevents the readiness field from becoming an escape hatch. | Spec R1-R3, R8; test spec T1-T5. | `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; M1/M2 code reviews. |
| `scripts/test-skill-validator.py` | Added controlled positive and negative fixtures, canonical skill/skeleton tests, adjacent workflow-spec drift checks, and generated-contract regression coverage. | Covers the direct historical failure, invalid pseudo-routing, approved/not-ready contradictions, missing-input `none`, and stale workflow wording. | Test spec T1-T5, T7. | 184-test validator runs after M2/M3 and targeted `-k spec_review` / `-k spec_review_routing_adjacent` runs. |
| `skills/spec-review/SKILL.md` | Added one consolidated routing/readiness section, closed enums, approval/readiness and condition rules, missing-input behavior, and status-to-routing bindings. Removed duplicate full material-finding field-list prose. | The shipped skill now teaches one routing contract and one readiness contract without weakening review substance. | Spec R1-R3, R8d; AC-SRTR-ROUTE-001 through AC-SRTR-ROUTE-005. | Canonical skill validation and code-review M2/M3. |
| `skills/spec-review/assets/review-result-skeleton.md` | Added distinct `Immediate next stage`, `Eventual test-spec readiness`, and `Stop condition` fields with the approved enums and a note that immediate routing must not be `test-spec`. | The result template is the structural output contract reviewers copy. | Spec R2-R3; test spec T4. | Canonical skeleton validation and generated archive content inspection. |
| `skills/test-spec/SKILL.md` | Removed stale `not-assessed` readiness wording and aligned upstream handling with `not-ready`. | `not-assessed` was rejected because it would let `spec-review` decline the readiness assessment it must perform. | Spec R6; test spec T6. | `python scripts/validate-skills.py skills/test-spec/SKILL.md`; code-review M2. |
| `specs/rigorloop-workflow.md` | Replaced stale empty-route and generic "immediate next repository stage" wording with explicit `Immediate next stage: none`, `Eventual test-spec readiness: not-ready`, and forward-stage language limited to `architecture` and `plan`. | The durable workflow spec still preserved old field semantics and caused `SRTR-CR1`. | Spec R1c, R7, R2h, R3j; AC-SRTR-ROUTE-005. | Adjacent-drift tests and code-review M2 rerun. |
| `specs/test-spec-readiness-and-skill-workflow-alignment.md` | Amended the governing feature spec with the closed routing/readiness contract, status bindings, missing-input behavior, UX rationale, and acceptance criteria. | The implementation needed a precise contract before test-spec and code relied on the changed output shape. | Proposal and spec-review findings `SRTR-SR1`, `SRTR-SR2`. | Spec-review r2/r3 approved. |
| `specs/test-spec-readiness-and-skill-workflow-alignment.test.md` | Mapped the approved requirements to controlled fixtures, canonical checks, material-finding ownership, adjacent prerequisites, generated-output proof, and lifecycle validation. | The previous test spec reflected older `not-assessed` and empty-route behavior. | Test spec T1-T9. | Maintainer approval before implementation; M1-M3 validations. |
| `docs/changes/.../behavior-preservation.md` | Recorded behavior-preservation proof for approval readiness, routing, readiness, material findings, recording, statuses, severities, workflow order, and generated adapters. | The change clarifies output shape without changing review semantics or lifecycle order. | Proposal behavior-preservation requirement; plan M2/M3. | Generated adapter archive proof and M3 code review. |
| `docs/changes/.../review-log.md`, `review-resolution.md`, and `reviews/*` | Recorded proposal/spec/plan/code reviews, material findings, dispositions, and clean reruns. | Formal lifecycle reviews required durable evidence, and material findings required closeout before downstream reliance. | Workflow contract and AGENTS.md review-recording rules. | Review artifact structure and closeout validation. |
| `docs/plans/2026-05-25-spec-review-testability-routing-output-consolidation.md` and `docs/plan.md` | Kept milestone state, validation notes, decisions, progress, and current handoff synchronized. | The active plan owns current workflow state for a planned initiative. | Plan-review r1/r2 and plan policy. | Lifecycle and change metadata validation. |
| `docs/proposals/2026-05-25-spec-review-testability-routing-output-consolidation.md` | Recorded the accepted direction to consolidate and enforce rather than remove testability assessment. | Preserves the key disagreement resolution that made the implementation safe. | Proposal-review r1. | Proposal-review approval. |

## Tests Added Or Changed

| Test surface | What it proves | Why this level is appropriate |
| --- | --- | --- |
| T1 controlled immediate-stage fixtures | Allowed values pass, while `Immediate next stage: test-spec` and pseudo-routing labels fail. | Unit fixture validation directly covers the historical routing bug. |
| T2 readiness fixtures | Approved results require `ready` or `conditionally-ready`, reject `not-ready`, reject `not-assessed`, and require named conditional readiness where inspectable. | Readiness is a field-level contract and can be tested without full skill execution. |
| T3 status-to-routing fixtures | Approved routes only to `architecture` or `plan`; missing inputs use `inconclusive`, `none`, `not-ready`, and a stop condition. | Cross-field checks prevent a new inconsistency between review status and routing. |
| T4 canonical skill/skeleton checks | The shipped canonical skill and result skeleton expose the final contract, not only controlled fixtures. | M2 is the milestone where enforcement moved from fixture scaffolding to public source. |
| T5 material-finding ownership checks | The complete material-finding field shape remains in the asset and is not duplicated in `SKILL.md`. | This checks structural ownership without overfitting exact prose. |
| T6 adjacent prerequisite review | `plan-review` and `test-spec` behavior remain intact where directly affected. | Adjacent skills were only edited or inspected when direct drift appeared. |
| T7 scope and workflow checks | Workflow order, isolation, autoprogression boundaries, and Markdown UX clarity are preserved. | These are workflow-contract risks best reviewed against the full diff. |
| T8 generated output proof | Temporary Codex, Claude, and opencode adapter archives contain the updated `spec-review` skill and skeleton. | The proposal required generated output to match canonical source. |
| T9 lifecycle and metadata validation | Review records, change metadata, lifecycle paths, and diff hygiene remain valid. | This is the repository-owned proof that the workflow evidence is coherent. |

## Validation Evidence Available Before Final Verify

Validation recorded during implementation and review includes:

```bash
python scripts/test-skill-validator.py -k spec_review_result_fixture
python scripts/test-skill-validator.py -k spec_review
python scripts/test-skill-validator.py -k spec_review_routing_adjacent
python scripts/test-skill-validator.py
python scripts/validate-skills.py skills/spec-review/SKILL.md
python scripts/validate-skills.py skills/test-spec/SKILL.md
python scripts/validate-skills.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-srto-m3-adapters-byvYm0
python scripts/validate-adapters.py --root /tmp/rigorloop-srto-m3-adapters-byvYm0 --version v0.1.5
python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-srto-m3-review-adapters-JwPaBr
python scripts/validate-adapters.py --root /tmp/rigorloop-srto-m3-review-adapters-JwPaBr --version v0.1.5
python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation
python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation
python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...
git diff --check -- ...
```

Manual archive checks used Python `zipfile` inspection against the temporary adapter archives and confirmed that generated `spec-review/SKILL.md` and `spec-review/assets/review-result-skeleton.md` contain the routing/readiness contract and do not reintroduce direct immediate `test-spec` routing or `not-assessed`.

Some lifecycle runs reported existing lifecycle-language warnings in `specs/rigorloop-workflow.md`; those runs still passed and did not report a blocker for this change. CI, final `verify`, branch readiness, and PR readiness are not claimed by this artifact.

## Review Resolution Summary

Material findings were recorded and closed in `review-resolution.md`.

| Finding ID | Disposition | Result |
| --- | --- | --- |
| `SRTR-SR1` | accepted | The spec now consistently names `Immediate next stage`, treats `none` as an explicit value, and reserves forward repository-stage language for `architecture` and `plan`. |
| `SRTR-SR2` | accepted | The spec now includes the required `Accessibility and UX` section with a Markdown-output clarity rationale. |
| `SRTR-PR1` | accepted | M1 was revised to fixture/parser scaffolding only; canonical enforcement begins in M2 with the canonical skill and skeleton updates. |
| `SRTR-CR1` | accepted | `specs/rigorloop-workflow.md` now uses explicit `Immediate next stage: none` and has adjacent-drift regression coverage. |

Closeout status is `closed`; unresolved findings are `0`. M1, M2 rerun, and M3 code reviews closed with no material findings.

## Alternatives Rejected

- Removing all `test-spec` mentions from `spec-review` was rejected because it would remove the approval-time testability assessment and reopen the documented misrouting failure.
- Keeping the old wording was rejected because the routing and readiness concepts would remain interwoven and prose-only.
- Adding another warning was rejected because it would not structurally prevent `Immediate next stage: test-spec`.
- Adding a `not-assessed` readiness value was rejected because it would let `spec-review` avoid the readiness assessment required for approval.
- Enabling canonical enforcement in M1 was rejected after plan review because unchanged canonical assets would have made M1 intentionally fail.
- Changing downstream workflow order, adding auto-handoff behavior, or broadening the review-family rewrite was kept out of scope.
- Hand-editing generated adapter output was rejected; M3 used repository-owned generation and temporary archives instead.

## Scope Control

The implementation stayed within the approved first slice:

- changed canonical `spec-review` source and its result skeleton;
- updated validation and test coverage for the routing/readiness contract;
- edited `skills/test-spec/SKILL.md` and `specs/rigorloop-workflow.md` only where direct drift existed;
- preserved `skills/spec-review/assets/material-finding.md` as the field-shape owner;
- kept review statuses, severity values, recording statuses, review dimensions, workflow stage order, and autoprogression boundaries unchanged;
- built generated output only in `/tmp`, without tracking public adapter package output.

## Risks And Follow-Ups

- Recorded review-artifact result-field validation remains a possible follow-up if the artifact parser gains result-field inspection support.
- Similar routing/readiness wording in other review-family skills should be handled by a separate proposal if a concrete drift pattern appears.
- The adapter archive content check is recorded as bounded proof rather than a reusable script; a future change can automate it if this check becomes recurring.
- Final `verify`, branch readiness, PR readiness, hosted CI status, and release readiness remain unclaimed until their owning stages run.

## Current Handoff

All in-scope implementation milestones are closed after code review, all material findings are closed, and this explain-change artifact records the rationale for the implemented diff. The next workflow stage is `verify`.
