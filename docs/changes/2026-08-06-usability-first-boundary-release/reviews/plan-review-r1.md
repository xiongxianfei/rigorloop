# Usability-First Boundary-First v0.4.0 Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex independent plan-review peer
Target: docs/plans/2026-08-06-usability-first-boundary-release.md
Review date: 2026-08-06
Status: changes-requested
Material findings: UBR-PR1-001
Immediate next stage: plan revision
Automatic downstream handoff: none

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: `UBR-PR1-001`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/plan-review-r1.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md#plan-review-r1`
- Open blockers: `UBR-PR1-001`
- Immediate next stage: plan revision followed by plan-review R2.

## Findings

### UBR-PR1-001 - M3 selects but does not execute its release proof

Finding ID: UBR-PR1-001

- Severity: major
- Location: `docs/plans/2026-08-06-usability-first-boundary-release.md`, M3 Validation commands, Expected observable result, and Boundary/interaction ownership for BND-COMPOSE-001 and INT-003
- Evidence: M3 promises a reviewed pending revision containing the complete `v0.4.0` payload and coherent three-target package proof, and that exact revision becomes M4's baseline input. Its commands run release preparation, local preflight, three focused regression suites, and `select-validation.py --mode release`, but the selector only reports the required bundle; it does not execute the selected checks. M3 therefore has no command that runs the complete release-selected CI bundle or the standing full release gate before closeout. Deferring those commands to M4 couples M3's package-parity and routine-release claim to the next milestone and allows an incompletely proven pending baseline to become frozen activation input.
- Required outcome: Add an exact executable M3 command that runs the complete repository-owned release-selected validation bundle before M3 code review and baseline selection. The command must cover the routine release gate, generated adapter archives, package validation, three-target packed or clean-install proof, and preserved rollback metadata while activation remains pending.
- Safe resolution path: Add `bash scripts/ci.sh --mode release --release-version v0.4.0` and, if that wrapper does not itself invoke the standing full gate, also add `bash scripts/release-verify.sh v0.4.0` to M3. State that both run after M3 adds `v0.4.0` support and before the reviewed pending revision is selected. Keep the M4 rerun after activation; it proves the active integrated state rather than substituting for M3 closeout.
- needs-decision rationale: none; UBR-R011, UBR-R012, BND-COMPOSE-001, INT-003, and the existing routine release architecture already determine the required owner and proof timing.

## Review dimensions

| Review dimension | Verdict | Evidence |
| --- | --- | --- |
| Self-contained context | pass | The plan names governing artifacts, owners, current script surfaces, the stale project-map boundary, exact cleanup inventory, and external release separation. |
| Source alignment | pass | All UBR requirements, eight boundaries, three interactions, approved ADR decisions, and formal review settlements are represented without adding product behavior. |
| Milestone size | pass | Four milestones separate user-facing guidance, validator cleanup, pending release preparation, and active integrated proof into reviewable rollback units. |
| Sequencing | concern | M1-to-M4 dependencies are coherent, but M3 does not execute the proof needed before its output becomes M4's baseline. |
| Scope discipline | pass | The plan explicitly excludes new commands, writers, services, publication paths, proof-model redesign, historical mass migration, and lifecycle publication. |
| Validation quality | block | M3 uses the selector without executing its selected bundle, so its expected release/package result is broader than its direct proof. |
| TDD readiness | pass | Every milestone starts with named failing fixtures or tests, and the preimplementation test-spec gate must map every requirement, boundary, interaction, acceptance criterion, and edge case. |
| Risk coverage | pass | Concision drift, selector over-cleanup, frozen-inventory mistakes, local/public claim confusion, generated drift, and partial publication each have bounded recovery. |
| Architecture alignment | pass | The plan uses the internal derivation function once, keeps normal validation current-file-only, preserves the routine release owner, and adds no CLI or writer. |
| Operational readiness | concern | The external release handoff and immutable recovery are clear; M3 needs the standing local release execution gate before it can hand a baseline to M4. |
| Plan maintainability | pass | Stable requirement, boundary, interaction, milestone, command, and artifact identities make the plan usable without chat context; mutable state remains in `change.yaml`. |

## Missing milestones or dependencies

No additional milestone is needed. M3 already owns the pending routine release payload; its validation list must execute the proof it currently only selects.

## Exact suggested edits

In M3:

1. Add `bash scripts/ci.sh --mode release --release-version v0.4.0` after release selection.
2. Add `bash scripts/release-verify.sh v0.4.0` unless the selected CI bundle demonstrably invokes that exact standing full gate.
3. State that the commands run after `v0.4.0` support exists and before code-review handoff and baseline selection.
4. Retain the M4 reruns to prove the active snapshot and final integrated package.

## Routing and readiness

The plan is not ready for test-spec because M3 cannot independently close its BND-COMPOSE-001 and INT-003 obligations. Revise the plan, rerun plan authoring validation, and request plan-review R2. This isolated review does not revise the plan or start test-spec automatically.
