# Plan Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `plan` package while preserving portable planning quality and moving governed lifecycle procedure behind one exact trigger. The work also changes initial `planned_work` creation into an evidence-first, plan-owned transaction after clean plan review, migrates new plan writers to stable-intent milestone structures, and proves read-old/write-new compatibility without adding a runtime or permanent simplicity validator.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-12-plan-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-12-plan-skill-simplification.md`
- Spec: `specs/plan-skill-simplification.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260813-reviewed-plan-initialization-and-settlement.md`
- Test spec: pending at `specs/plan-skill-simplification.test.md`

## Context and orientation

`skills/plan/` is the only authored skill-package source. The target package keeps portable planning, quality, stops, claims, and resource triggers in `SKILL.md`; moves governed inspection, create, revise, and approved-plan initialization into `references/governed-plan-authoring.md`; retains the checked boundary reference; and keeps exactly three structural assets.

The lifecycle transaction crosses `plan`, `plan-review`, and `workflow`. `plan` owns stable plan content and initial derivation, `plan-review` owns judgment and settlement, and `workflow` owns coordination and routing. The implementation must amend the current lifecycle contract, metadata semantics, parsers, tests, and published skill text atomically.

This plan is a bootstrap artifact under the currently active contract, which still initializes `planned_work` when registering a primary plan. That bootstrap state is recorded only in this change's `change.yaml`; it is not the target behavior. The plan body intentionally contains no mutable milestone state, and implementation switches future authoring to the reviewed-plan transaction defined by the approved spec and ADR.

## Non-goals

- Change milestone quality, validation, recovery, claim, destructive-action, or handoff semantics beyond the approved transaction and ownership corrections.
- Add hashes, `content_identity`, a new runtime, scheduler, state store, lifecycle stage, package model, target-agent acceptance, or permanent size validator.
- Infer or repair live `planned_work` from historical plan prose, rewrite historical terminal plans, or reverse-synchronize mutable state into plan bodies.
- Hand-edit generated adapter packages or tracked installed runtime copies.
- Treat a percentage reduction as more important than semantic preservation.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| PSIM-R006-PSIM-R020, PSIM-R023-PSIM-R028, PSIM-R034-PSIM-R035; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001; INT-001, INT-003 | M1 lifecycle transaction, state semantics, compatibility readers, and migration proof |
| PSIM-R001-PSIM-R005, PSIM-R021-PSIM-R022, PSIM-R029; BND-COMPOSE-001, BND-RECOVERY-001; INT-002 | M2 package ownership, stable-intent assets, rule/literal disposition, and focused validation |
| PSIM-R030-PSIM-R033; BND-COMPOSE-001, BND-COMPAT-001; INT-002, INT-003 | M3 assembly measurement, semantic preservation, and canonical-through-installed parity |

## Milestones

### M1. Implement the reviewed-plan lifecycle transaction and compatibility boundary

- Milestone kind: implementation
- Goal: Amend the lifecycle contract, state validation, review settlement, workflow coordination, and historical readers so clean plan-review evidence precedes one-time initialization and new writers stop emitting mutable plan state.
- Requirements: PSIM-R006-PSIM-R020, PSIM-R023-PSIM-R028, PSIM-R034-PSIM-R035; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001; INT-001, INT-003.
- Architecture decisions: ADR-20260813 reviewed-plan initialization and settlement; canonical lifecycle and state-ownership architecture.
- Files/components likely touched:
  - `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`
  - `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.test.md`
  - `specs/rigorloop-workflow.md`
  - `specs/rigorloop-workflow.test.md`
  - `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` where current initialization order is normative
  - `scripts/change_metadata_semantics.py`, `scripts/artifact_lifecycle_validation.py`, `scripts/lifecycle_state_sync.py`, `scripts/workflow_automation.py`, and bounded query helpers
  - focused validator and workflow test modules
- Dependencies: Approved spec, architecture, ADR, and clean plan review.
- Tests and proof:
  - operation classification for create, revise, initialize, unknown, and ambiguous inputs
  - legal and illegal plan/review/`planned_work` combinations
  - clean evidence before initialization, stale review rejection, identical initialization no-op, interrupted settlement retry, and no semantic rereview
  - stable artifact and reviewed revision identity without document hashes
  - old-format complete active plans, incomplete active plans, conflicts, portable plans, and terminal historical plans
  - removal of current-state authority from plan-body `Milestone state`
- Implementation steps:
  - add failing deterministic tests for the approved legal-state table, transaction ordering, identity, retry, and read-old/write-new matrix
  - amend governing lifecycle specs and repository instructions to make the new transaction authoritative
  - update metadata and lifecycle validators to allow only the enumerated temporary states and to fail closed on all other combinations
  - update workflow coordination and plan-review settlement to reuse recorded judgment after matching initialization
  - migrate readers to use plan content only for stable intent and `change.yaml` only for current state
  - preserve historical parsing without automatic repair or reverse synchronization
- Validation commands:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-workflow-automation.py`
  - `python scripts/test-workflow-automation-state.py`
  - `python scripts/test-query-change-record.py`
- Expected observable result: A new governed plan can reach review without live work state; clean review can request initialization; workflow can coordinate one bounded initialization and identical settlement retry; stale, conflicting, and legacy-incomplete states fail closed.
- Completion criteria: Focused lifecycle tests pass, target contracts agree on ordering and ownership, and no current-state consumer relies on plan-body mutable state.
- Required evidence: M1 implementation evidence, exact test commands and results, touched-contract inventory, compatibility fixture results, and independent code review.
- Review handoff: `code-review` reviews M1 against PSIM-R006-PSIM-R020 and PSIM-R023-PSIM-R028 before M2 begins.
- Commit boundary: `M1: implement reviewed plan settlement transaction`
- Risks: Partial rollout could leave a validator, reviewer, or router enforcing the old invariant.
- Rollback/recovery: Revert contract, validator, workflow, and parser changes as one slice; do not retain half-supported temporary states.

### M2. Simplify the plan package and stable-intent assets

- Milestone kind: implementation
- Goal: Give universal, governed, boundary, and structural rules one owner while making both portable and governed procedural assemblies smaller.
- Requirements: PSIM-R001-PSIM-R005, PSIM-R021-PSIM-R022, PSIM-R029; BND-COMPOSE-001, BND-RECOVERY-001; INT-002.
- Architecture decisions: Published skill resources remain skill-owned; assets remain structural leaves; missing triggered resources fail closed.
- Files/components likely touched:
  - `skills/plan/SKILL.md`
  - `skills/plan/references/governed-plan-authoring.md`
  - `skills/plan/references/boundary-first-method-v1.md` only if parity metadata requires regeneration
  - `skills/plan/assets/plan-skeleton.md`
  - `skills/plan/assets/milestone.md`
  - `skills/plan/assets/decision-log-row.md`
  - `skills/plan-review/SKILL.md` and `skills/workflow/SKILL.md` only for the approved cross-stage transaction
  - `scripts/test-skill-validator.py` and directly coupled literal consumers
  - change-local rule, literal, fixture, and baseline evidence
- Dependencies: M1 contract and compatibility slice is closed by code review.
- Tests and proof:
  - exact PL0, PL0B, PL1, and PL1B resource assemblies and forbidden loads
  - portable and governed authority separation, missing-resource stops, create/revise/initialize ownership, and no downstream authority from loading
  - stable-intent milestone fields, absence of mutable state, complete sentences, placeholder rejection, and exactly three assets
  - unknown semantic dispositions and literal classifications fail before consistency checks
- Implementation steps:
  - inventory every significant rule and exact-string consumer before moving prose
  - add focused failing skill-validation assertions for resource loading, authority, stable-intent structure, and missing-resource behavior
  - rewrite `SKILL.md` as the self-sufficient portable path and create the single governed reference
  - remove mutable fields from new structural assets while preserving completion criteria, evidence, review handoff, risk, recovery, and optional commit boundaries
  - migrate real parser/package literals atomically and update incidental tests rather than preserving accidental prose
  - finalize rule and literal destinations and record the post-change scenario results
- Validation commands:
  - `python scripts/validate-skills.py skills/plan/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: Portable planning remains complete from a shorter common path, governed procedure loads only with matching authority, new copied milestones contain stable intent only, and conditional failure is safe.
- Completion criteria: Focused skill and build tests pass, every semantic rule and literal has one disposition, and no policy is owned by an asset.
- Required evidence: Rule and literal ledgers, scenario fixtures, baseline and after measurements, implementation evidence, and independent code review.
- Review handoff: `code-review` reviews M2 against package ownership, authority, asset, and readability requirements before M3 begins.
- Commit boundary: `M2: simplify plan package ownership`
- Risks: Universal safety could be hidden behind the governed trigger or duplicated between package files.
- Rollback/recovery: Restore the previous canonical package and validators together, then regenerate derived packages.

### M3. Prove profile reduction, semantic preservation, and package parity

- Milestone kind: implementation
- Goal: Prove both primary procedural profiles shrink, the lifecycle and migration semantics remain complete, and every supported package carries byte-identical mapped resources.
- Requirements: PSIM-R030-PSIM-R033; BND-COMPOSE-001, BND-COMPAT-001; INT-002, INT-003.
- Architecture decisions: Canonical authored resources generate every derived package; words and UTF-8 bytes are primary change-local measurements.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if existing focused selection cannot prove `plan`
  - existing adapter fixtures only where focused coverage is absent
  - change-local simplification measurement, semantic preservation, migration, and package-proof evidence
- Dependencies: M2 package refactor is closed by code review.
- Tests and proof:
  - LF-normalized PL0, PL0B, PL1, and PL1B words, bytes, resource order, and identities
  - separate structural-asset and total-package accounting
  - generated, archived, and temporary clean-installed resource path and byte parity
  - missing, stale, escaped, transformed, contradictory, or mixed resources fail closed
  - independent semantic review against the approved spec, ADR, rule ledger, and literal inventory
- Implementation steps:
  - run deterministic profile measurement and require both PL0 and PL1 to decrease without a fixed percentage gate
  - explain all boundary-profile and total-package deltas and verify each duplicate cluster has one loaded owner
  - generate adapters in a temporary directory and prove selected archive and installed-tree parity
  - independently review the complete skill package and lifecycle transaction without running a target agent
  - record final migration and package evidence and run the complete approved validation set
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-adapters.py --help`
  - `python scripts/validate-boundary-first.py --check --path specs/plan-skill-simplification.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-12-plan-skill-simplification/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-12-plan-skill-simplification`
- Expected observable result: PL0 and PL1 are measurably smaller, boundary variants have no unexplained growth, semantics are preserved, and canonical-through-installed resources retain required parity.
- Completion criteria: All approved commands pass, semantic review finds no material loss, profile and total-package evidence is honest, and no target-agent runtime or new permanent simplicity validator exists.
- Required evidence: Simplification measurements, semantic preservation review, adapter package proof, final validation results, and independent code review.
- Review handoff: `code-review` reviews M3 and then performs the final holistic implementation review before explanation and verify.
- Commit boundary: `M3: prove plan simplification and package parity`
- Risks: Main-file reduction could hide governed-profile or total-package growth, or generic package tests could miss `plan` resources.
- Rollback/recovery: Restore the last complete canonical package and lifecycle slice, regenerate every derived package, and discard temporary output.

## Validation plan

- M1 closes transaction, state, retry, migration, and parser behavior with focused lifecycle and workflow tests before package prose moves.
- M2 closes skill structure, resource ownership, stable-intent assets, readability, and build parity with focused skill validators.
- M3 closes boundary proof, adapter distribution, change metadata, formal review structure, semantic preservation, and profile accounting.
- No command may run Codex, Claude Code, opencode, or another target-agent runtime. Temporary adapter generation uses repository-owned scripts and must not publish or mutate external state.

## Risks and recovery

- Risk: The bootstrap change record reflects the old initialization order while the plan describes the new order.
  - Recovery: Keep bootstrap state only in `change.yaml`, label it explicitly here and in authoring evidence, and make M1 switch future behavior atomically.
- Risk: Clean review evidence and live initialization could drift between writes.
  - Recovery: Bind initialization to stable artifact and reviewed revision identities and fail closed on any later edit or contradictory review.
- Risk: Historical mutable plan text could regain authority through a parser fallback.
  - Recovery: Use explicit read-old/write-new fixtures and prohibit plan-to-state repair and reverse synchronization.
- Risk: Progressive disclosure could merely relocate duplication.
  - Recovery: Require one owner per rule, lower PL0 and PL1 loaded bytes and words, and report total package size separately.

## Dependencies

- Accepted proposal, approved spec, clean spec review, approved canonical architecture, accepted ADR, and clean architecture review.
- Current lifecycle, skill contract, workflow automation, formal review recording, boundary-first, and adapter package contracts.
- Existing repository-owned validators, fixtures, build scripts, and adapter generation paths.
- Approved test specification and clean test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-13 | Use three implementation milestones: lifecycle and compatibility, package refactor, and final proof. | Each slice has an independently reviewable failure and rollback boundary. | One cross-cutting rewrite or more narrowly fragmented milestones. |
| 2026-08-13 | Treat this plan as a bootstrap under the current initialization contract while keeping mutable state out of its body. | The target transaction is not active until M1, and `change.yaml` already owns current state. | Pretend the future contract is active or duplicate bootstrap state in plan prose. |
| 2026-08-13 | Change contracts and deterministic lifecycle tests before moving skill prose. | Package text must not advertise temporary states that validators and routing reject. | Skill-first rollout or partial compatibility shims. |
| 2026-08-13 | Keep migration read-old/write-new with explicit workflow-owned handling for incomplete active legacy state. | This preserves history without creating hidden repair authority. | Rewrite historical plans or infer current state from prose. |
| 2026-08-13 | Measure PL0 and PL1 directly and report assets and total package separately. | Main-file reduction alone cannot prove the primary invocation profiles improved. | Fixed percentage or `SKILL.md`-only success. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation and code-review milestones, explanation, verification, and PR handoff remain.
