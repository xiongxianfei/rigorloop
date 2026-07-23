# Single Bounded Review-Fix Workflow Automation Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Change ID: 2026-07-20-single-bounded-review-fix-workflow-automation-mechanism
- Owner: agent
- Start date: 2026-07-21
- Last updated: 2026-07-23
- Related issue or PR: none yet
- Supersedes: none
- broad_smoke_required: true
- broad_smoke_reason: The final cutover changes workflow routing, schemas, validators, canonical skills, compatibility adapters, and generated public behavior.

## Purpose / big picture

Implement the approved single `bounded-review-fix` workflow-automation mechanism across proposal review, authoring, milestone implementation and code review, final verification, and legacy compatibility.

The implementation replaces three independently writable automation profiles with one target-driven engine, one immutable stage-policy projection, one state-write boundary, and one canonical `change.yaml#workflow.automation` record.

The work must preserve stage-owned artifacts, formal review independence, active-plan live-state ownership, separate authoring/implementation/verification authority, bounded correction policies, evidence-first recovery, dual-read/single-write migration, and the stop before PR or any other external action.

## Source artifacts

- Proposal: [Single Bounded Review-Fix Workflow Automation Mechanism](../proposals/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism.md)
- Spec: [Single Bounded Review-Fix Workflow Automation](../../specs/single-bounded-review-fix-workflow-automation.md)
- Architecture: [RigorLoop Canonical System Architecture](../architecture/system/architecture.md)
- ADR: [ADR-20260721 Single Bounded Review-Fix Workflow Automation Mechanism](../adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md)
- Test spec: [Single Bounded Review-Fix Workflow Automation Test Specification](../../specs/single-bounded-review-fix-workflow-automation.test.md)
- Change metadata: [change.yaml](../changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/change.yaml)
- Review log: [review-log.md](../changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md)
- Review resolution: [review-resolution.md](../changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md)
- Latest proposal review: [proposal-review-r4](../changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/proposal-review-r4.md)
- Latest spec review: [spec-review-r5](../changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/spec-review-r5.md)
- Latest architecture review: [architecture-review-r3](../changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/architecture-review-r3.md)
- Latest plan review: [plan-review-r2](../changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/plan-review-r2.md)

## Upstream status settlement

- Upstream artifact: `docs/architecture/system/architecture.md`, `docs/adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md`, and its three predecessor ADRs
- Review evidence: `architecture-review-r3` approved the canonical package and ADR with no material findings; `review-resolution.md` is closed and `review-log.md` has no open findings
- Previous status: architecture `draft`; unified ADR `proposed`; three predecessor ADRs `accepted`
- New status: architecture `approved`; unified ADR `accepted`; three predecessor ADRs `superseded` with replacement links
- Settlement result: updated
- Settlement blocker: none

## Context and orientation

The current repository still implements the three retired writable models separately:

- `schemas/change.schema.json` and `scripts/validate-change-metadata.py` validate `workflow.autoprogression`, its authoring and implementation profiles, and nested `review_fix` state.
- `scripts/lifecycle_state_sync.py` contains separate authoring, implementation, and review-fix route evaluators and closed vocabularies.
- `scripts/artifact_lifecycle_validation.py` and `scripts/validate-artifact-lifecycle.py` compose lifecycle and state-sync proof.
- `scripts/review_artifact_validation.py` and `scripts/validate-review-artifacts.py` validate review correction and closeout evidence.
- `skills/workflow/SKILL.md` still teaches three public automation mechanisms and their independent continuation boundaries.
- `scripts/test-change-metadata-validator.py`, `scripts/test-artifact-lifecycle-validator.py`, `scripts/test-review-artifact-validator.py`, and `scripts/test-skill-validator.py` preserve existing profile behavior.

The approved architecture adds these executable owners:

- `scripts/workflow_automation_policy.py`: immutable stage policies and closed enums.
- `scripts/workflow_automation_state.py`: sole `workflow.automation` reader/writer and receipt reconciler.
- `scripts/workflow_automation.py`: command adaptation, target and canonical-position resolution, capability evaluation, and transition coordination.
- `scripts/validate_workflow_automation.py`: policy, state, migration, and canonical-evidence validation.

The implementation must reuse existing lifecycle and review parsers where they already own canonical evidence. It must not create parallel artifact-status, plan-state, or review-verdict parsers inside the automation engine.

Until the final public-cutover milestone, the unified engine is reachable only through tests or an explicitly non-public internal harness. Earlier milestones must not advertise, activate, or route public commands into the incomplete mechanism.

## Non-goals

- Do not change the approved public target vocabulary or occurrence rules.
- Do not add a second YAML/JSON policy registry or a separate automation-state file.
- Do not make automation metadata own active-plan milestone state, current next stage, review verdicts, branch readiness, or PR readiness.
- Do not weaken independent formal review or let a review skill edit the artifact it reviews.
- Do not infer correction authority beyond driver-owned proposal classification and reviewer-owned implementation classification.
- Do not automatically repair verification failures.
- Do not remove legacy command adapters during the migration window.
- Do not restore a retired profile writer as rollback behavior.
- Do not open PRs, push, publish, release, deploy, merge, use credentials, perform destructive Git operations, or mutate external systems.
- Do not hand-edit generated public adapter output.
- Do not expose `$workflow auto: <stage>` or redirect a compatibility alias to the unified writer before the final cutover milestone passes its prerequisite integration reviews.

## Requirements covered

| Requirement group | Plan coverage |
| --- | --- |
| `BRF-R001`-`BRF-R017f` | M1 defines the unified schema, closed durable vocabularies, structured target records, and complete target/occurrence policy projection; M3 implements command binding. |
| `BRF-R018`-`BRF-R023` | M3 implements evidence-derived pre-plan position and active-plan ownership handoff without a competing cursor. |
| `BRF-R024`-`BRF-R046` | M1 defines parent/capability records and validation; M3 implements derivation, boundary pauses, and invalidation. |
| `BRF-R047`-`BRF-R062` | M4 implements proposal-review occurrence/gate separation, proposal correction, and post-proposal authoring routing through a non-public harness. |
| `BRF-R060`-`BRF-R067` | M5 implements independent implementation review, reviewer-owned correction, and verification-failure routing through a non-public harness. |
| `BRF-R068`-`BRF-R077` | M2 implements prepared receipts, the sole write boundary, evidence-first reconciliation, cancellation, and failure recovery. |
| `BRF-R078`-`BRF-R086` | M1 defines complete policies; M3-M5 integrate authoring and implementation stage owners, repeated milestones, final holistic review, explanation, and verify completion. |
| `BRF-R087`-`BRF-R090` | M4 and M5 prove isolation and external-action containment internally; M6 preserves them at public activation. |
| `BRF-R091`-`BRF-R098d` | M2 implements one-way state migration; M6 implements and proves mandatory command adapters and rollback behavior. |
| `BRF-R098e`-`BRF-R098i` | M6 implements exact cross-spec disposition and retired-writer contradiction validation. |
| `BRF-R099`-`BRF-R102` | M1 and M6 implement observable results, tracked resume evidence, fail-closed validators, and unknown-value regressions. |
| `BRF-AC001`-`BRF-AC026` and `AC-BRF-SR1-*`-`AC-BRF-SR6-*` | The active test spec maps each acceptance family to M1-M6 automated and bounded manual proof before implementation begins. |

## Current Handoff Summary

- Current milestone: M4. Authoring, Proposal Review, and Correction Integration
- Current milestone state: review-requested
- Last reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Latest review evidence: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m4-r2.md`
- Review status: review-requested; stage=code-review; round=r3
- Remaining in-scope implementation milestones: M4 rereview, M5, M6
- Next stage: code-review M4 R3
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation-milestones-open, milestone-review-pending, explain-change-pending, verify-pending, pr-handoff-pending — review-state=closed; open-count=0; open-findings=none

## Milestones

### M1. Unified State Model and Complete Policy Registry

- Milestone state: closed
- Goal: Establish the canonical `workflow.automation` schema, typed durable records, closed enums, complete immutable stage-policy registry, and fail-closed structural validation before any new routing becomes writable.
- Requirements: `BRF-R001`-`BRF-R017a`, `BRF-R024`-`BRF-R046`, `BRF-R069`-`BRF-R071`, `BRF-R079`-`BRF-R080`, `BRF-R099`-`BRF-R102`
- Files/components likely touched:
  - `schemas/change.schema.json`
  - `scripts/workflow_automation_policy.py`
  - `scripts/validate_workflow_automation.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/change_metadata_semantics.py`
  - `scripts/test-workflow-automation-policy.py`
  - `scripts/test-validate-workflow-automation.py`
  - `scripts/test-change-metadata-validator.py`
  - change-metadata fixtures under `tests/fixtures/`
- Dependencies:
  - Clean plan-review and approved test spec.
  - Approved spec and accepted ADR remain unchanged.
- Tests to add/update:
  - Exactly one complete immutable policy exists for every public and internal automatable stage.
  - Missing, duplicate, unknown, incomplete, and spec-inconsistent policies fail before consistency evaluation.
  - Run, parent-authorization, capability, capability-kind, target, occurrence, receipt, routing, retry, and stop vocabularies reject unknown values.
  - Parent records are non-executable; capabilities require a valid parent, stage basis, occurrence, and subset scope.
  - Structured repeated targets require plan and milestone identity before persistence.
  - `workflow.automation` rejects a legacy mechanism value and forbidden live-state ownership fields.
- Implementation steps:
  - Add the unified schema subsection and schema version without removing legacy read compatibility.
  - Implement frozen enums and `StagePolicy` records with all sixteen approved fields.
  - Encode each automatable public and internal stage exactly once.
  - Add structural and semantic validators that reject unknown values before cross-field checks.
  - Keep new writers disabled until M2 establishes the prepared-receipt state boundary.
- Validation commands:
  - `python scripts/test-workflow-automation-policy.py`
  - `python scripts/test-validate-workflow-automation.py -k vocabulary`
  - `python scripts/test-change-metadata-validator.py -k workflow_automation`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/change.yaml`
- Expected observable result: Unified state and every stage policy can be represented and exhaustively validated, but no transition is yet executed through the new writer.
- Commit message: `M1: define unified automation state and policies`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before M2 starts
  - milestone committed
- Risks:
  - A permissive compatibility shape could let malformed unified state bypass closed-vocabulary validation.
  - Hand-copied policy fields could drift from the approved spec.
- Rollback/recovery:
  - Remove the new unified schema and policy projection together while leaving all existing legacy readers and manual workflow behavior intact.

### M2. Sole State Writer, Prepared Receipts, and Recovery

- Milestone state: closed
- Goal: Implement atomic-file state updates, the sole automation-state write boundary, prepared/finalized receipts, reconciliation, cancellation, and one-way legacy-state migration without invoking stage work through the new engine yet.
- Requirements: `BRF-R006`-`BRF-R008f`, `BRF-R030`, `BRF-R044`-`BRF-R046`, `BRF-R068`-`BRF-R077`, `BRF-R091`-`BRF-R098`
- Files/components likely touched:
  - `scripts/workflow_automation_state.py`
  - `scripts/validate_workflow_automation.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/query-change-record.py`
  - `scripts/test-workflow-automation-state.py`
  - `scripts/test-validate-workflow-automation.py`
  - `scripts/test-query-change-record.py`
  - state and migration fixtures under `tests/fixtures/`
- Dependencies:
  - M1 unified model and policy registry.
- Tests to add/update:
  - A prepared receipt is durable before a stage invocation can begin.
  - Receipts carry the original `effective_capability_id` and never bind directly to parent authorization.
  - Resume reconciles valid completion evidence, retries only `idempotent-retry`, and pauses manual/reconcile-only cases.
  - Invalidated capability, changed output identity, partial output, unknown receipt state/policy version, or multiple in-flight transitions fails closed or pauses as specified.
  - Cancellation reconciles prepared work, cancels the run, revokes parents, invalidates capabilities, and preserves receipts.
  - Legacy projection is read-only; first mutating resume writes one unified migration receipt; mixed writers fail closed.
  - State replacement preserves unrelated valid change metadata and does not leave a truncated `change.yaml`.
- Implementation steps:
  - Implement typed load/validate/update operations for `change.yaml#workflow.automation`.
  - Use a repository-safe temporary-file and replace strategy for each complete YAML update while retaining logical write-ahead receipt ordering.
  - Implement prepared-receipt creation, finalization, reconciliation, and one-in-flight enforcement.
  - Implement legacy read projection and one-way migration receipts without writing retired records.
  - Extend bounded change-record queries to report unified status without treating it as live next-stage ownership.
- Validation commands:
  - `python scripts/test-workflow-automation-state.py`
  - `python scripts/test-validate-workflow-automation.py -k receipt`
  - `python scripts/test-validate-workflow-automation.py -k migration`
  - `python scripts/test-query-change-record.py`
  - `python scripts/test-change-metadata-validator.py`
- Expected observable result: Unified state updates and interrupted transitions are recoverable and auditable through one writer, while current command behavior remains unchanged.
- Commit message: `M2: add unified automation state recovery`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before M3 starts
  - milestone committed
- Risks:
  - YAML replacement could overwrite unrelated concurrent edits.
  - A migration retry could duplicate unified runs or receipts.
- Rollback/recovery:
  - Disable unified mutation entrypoints, retain read-only legacy interpretation and recorded evidence, and return affected work to explicit manual stage invocation.

### M3. Target Binding, Canonical Position, and Capability Evaluation

- Milestone state: closed
- Goal: Implement the target-driven engine through deterministic command normalization, repeated-stage binding, canonical-position resolution, parent/capability evaluation, and one-stage transition coordination.
- Requirements: `BRF-R003`-`BRF-R005`, `BRF-R009`-`BRF-R023`, `BRF-R024`-`BRF-R046`, `BRF-R068`, `BRF-R072`, `BRF-R078`-`BRF-R080`
- Files/components likely touched:
  - `scripts/workflow_automation.py`
  - `scripts/workflow_automation_policy.py`
  - `scripts/workflow_automation_state.py`
  - `scripts/lifecycle_state_sync.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/test-workflow-automation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - engine and active-plan fixtures under `tests/fixtures/`
- Dependencies:
  - M1 policies and M2 state/recovery boundary.
- Tests to add/update:
  - Current and legacy commands normalize to a structured target before persistence.
  - Bare `implement` and `code-review` bind exactly one current nonterminal milestone and current plan identity; missing or ambiguous state produces the exact required diagnostic.
  - Resume never rebinds a repeated target to a later milestone.
  - Pre-plan position derives from current artifacts, reviews, resolution, architecture applicability, and transition evidence; ambiguity and staleness pause.
  - Valid plan creation records the ownership handoff; afterward the plan summary owns live state.
  - Authoring, implementation, and verification parents remain separate; target selection never widens consent.
  - Capability derivation rejects stale basis, parent mismatch, cross-risk derivation, expanded paths/categories/budget, and conflicting active authority.
  - A run targeting verify pauses at the verification boundary until concrete verification authorization exists.
- Implementation steps:
  - Implement command parsing and compatibility normalization without exposing a second dispatcher state.
  - Implement structured target and occurrence binding from the closed policy registry.
  - Reuse lifecycle parsers for authoritative artifacts, review evidence, and active-plan handoff state.
  - Implement parent authorization and effective capability creation, invalidation, and single-use checks.
  - Coordinate one stage invocation through the M2 prepared-receipt boundary.
- Validation commands:
  - `python scripts/test-workflow-automation.py -k target`
  - `python scripts/test-workflow-automation.py -k position`
  - `python scripts/test-workflow-automation.py -k capability`
  - `python scripts/test-artifact-lifecycle-validator.py -k automation`
  - `python scripts/test-artifact-lifecycle-validator.py`
- Expected observable result: The engine can deterministically select and authorize one next stage without becoming a second workflow cursor or crossing a risk boundary.
- Commit message: `M3: coordinate target-bound workflow stages`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before M4 starts
  - milestone committed
- Risks:
  - Reimplemented artifact parsing could disagree with lifecycle validators.
  - A target binder could silently select the wrong milestone.
- Rollback/recovery:
  - Disable engine command entrypoints while keeping unified state validation and recovery tooling available for recorded runs.

### M4. Authoring, Proposal Review, and Correction Integration

- Milestone state: review-requested
- Goal: Integrate proposal review, bounded proposal correction, and post-proposal authoring through `test-spec-review` behind a non-public harness while preserving formal review independence and clean-gate semantics.
- Requirements: `BRF-R047`-`BRF-R062`, `BRF-R078`-`BRF-R080`, `BRF-R087`-`BRF-R090`, `BRF-R099`-`BRF-R100`
- Files/components likely touched:
  - `scripts/workflow_automation.py`
  - `scripts/workflow_automation_policy.py`
  - `scripts/review_artifact_validation.py`
  - `scripts/lifecycle_state_sync.py`
  - proposal, proposal-review, authoring, and review-resolution stage skills under `skills/` only when their non-public invocation contract must change
  - `scripts/test-workflow-automation.py`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - authoring and proposal-review fixtures under `tests/fixtures/`
- Dependencies:
  - M3 one-stage engine and authority evaluation.
  - The public workflow skill and compatibility aliases remain unchanged.
- Tests to add/update:
  - Proposal review records all four outcomes separately from clean-gate satisfaction; only approval continues to a later target.
  - Exact proposal-review targets stop after recording the occurrence regardless of gate outcome.
  - Proposal correction requires driver-owned deterministic classification and remaining budget; mutation makes the prior review stale and forces rereview.
  - Blocked and inconclusive review outcomes pause, and inconclusive review cannot spin without material evidence change.
  - Post-proposal authoring uses a separate effective capability and stops at every authorization or review boundary through `test-spec-review`.
  - Review skills cannot edit the reviewed artifact in the same pass, and isolated invocations do not activate or advance automation.
  - No current or legacy public command can route into the M4 integration harness.
- Implementation steps:
  - Connect proposal-review, proposal-correction, and post-proposal-authoring policies to stage-native completion evidence.
  - Implement review occurrence, clean-gate, exact-target, and later-target routing.
  - Enforce driver-owned proposal correction through existing review-resolution evidence and budgets.
  - Integrate singleton authoring stages and conditional architecture behavior through `test-spec-review`.
  - Exercise the stage chain only through an explicitly non-public test harness; do not edit `skills/workflow/SKILL.md` public command semantics.
- Validation commands:
  - `python scripts/test-workflow-automation.py -k proposal_review`
  - `python scripts/test-workflow-automation.py -k proposal_correction`
  - `python scripts/test-workflow-automation.py -k authoring`
  - `python scripts/test-workflow-automation.py -k non_public`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-skill-validator.py`
- Expected observable result: The internal engine can traverse proposal review and authoring safely through `test-spec-review`, but no public command or legacy alias can enter the incomplete unified mechanism.
- Commit message: `M4: integrate bounded authoring review stages`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before M5 starts
  - milestone committed
- Risks:
  - Consecutive authoring stages could collapse author/reviewer independence.
  - Proposal correction could accidentally inherit post-proposal authority.
- Rollback/recovery:
  - Remove or disable the internal authoring harness, preserve stage evidence, and leave all public workflow behavior unchanged.

### M5. Implementation Review, Correction, and Verification Integration

- Milestone state: planned
- Goal: Integrate ordered milestone implementation and code review, reviewer-owned correction, final holistic review, explanation, and verification behind the same non-public boundary.
- Requirements: `BRF-R060`-`BRF-R067`, `BRF-R078`-`BRF-R090`, `BRF-R099`-`BRF-R100`
- Files/components likely touched:
  - `scripts/workflow_automation.py`
  - `scripts/workflow_automation_policy.py`
  - `scripts/review_artifact_validation.py`
  - `scripts/lifecycle_state_sync.py`
  - implementation, code-review, review-resolution, ci-maintenance, explain-change, and verify stage skills under `skills/` only when their non-public invocation contract must change
  - `scripts/test-workflow-automation.py`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - implementation and verification fixtures under `tests/fixtures/`
- Dependencies:
  - M4 authoring and proposal-review integration is closed and independently reviewed.
  - The public workflow skill and compatibility aliases remain unchanged.
- Tests to add/update:
  - Implementation correction requires reviewer-owned `auto_fix_class`; missing classification is `none`; new/non-shrinking findings and scope expansion pause.
  - `implement@M<n>` reaches `review-requested` only after milestone validation; `code-review@M<n>` closes only the bound milestone after approved review and resolution.
  - Milestones execute in plan order and every milestone receives independent local code review.
  - Final holistic review remains distinct from milestone review.
  - Verification authorization cannot exist before its complete concrete basis; explanation and verification do not run without it.
  - Verification failure pauses without repair; successful verify reports `pr` next but performs no external action.
  - No current or legacy public command can route into the M5 integration harness.
- Implementation steps:
  - Connect implementation, implementation-correction, milestone review, CI-maintenance, final holistic review, explanation, and verification policies to stage-native completion evidence.
  - Enforce reviewer-owned correction classifications and bounded convergence through existing review-resolution evidence.
  - Enforce ordered milestone implementation/review loops and final holistic review.
  - Implement verification authorization timing, explanation/verification completion checks, and the hard stop before PR.
  - Exercise the stage chain only through the non-public harness; do not edit `skills/workflow/SKILL.md` public command semantics.
- Validation commands:
  - `python scripts/test-workflow-automation.py -k implementation`
  - `python scripts/test-workflow-automation.py -k correction`
  - `python scripts/test-workflow-automation.py -k milestone`
  - `python scripts/test-workflow-automation.py -k verify`
  - `python scripts/test-workflow-automation.py -k non_public`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-skill-validator.py`
- Expected observable result: The internal engine can traverse implementation through final verify while preserving milestone review, authority, recovery, and external-action boundaries, but remains unreachable from public commands.
- Commit message: `M5: integrate bounded implementation verification stages`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before M6 starts
  - milestone committed
- Risks:
  - Reusing legacy implementation loops could preserve obsolete profile authority.
  - Final holistic review could be confused with milestone-local review.
- Rollback/recovery:
  - Remove or disable the internal implementation harness, preserve unified evidence and explicit stage behavior, and leave public routing unchanged.

### M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof

- Milestone state: planned
- Goal: Atomically activate unified public commands, map compatibility aliases, prohibit every legacy writer, implement cross-spec contradiction checks, regenerate derived guidance, and prove the complete mechanism.
- Requirements: `BRF-R002`-`BRF-R005`, `BRF-R087`-`BRF-R102`, including `BRF-R098a`-`BRF-R098i`
- Files/components likely touched:
  - `skills/workflow/SKILL.md`
  - affected review, implementation, verification, and planning skills under `skills/`
  - `docs/workflows.md`
  - `scripts/workflow_automation.py`
  - `scripts/validate_workflow_automation.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/lifecycle_state_sync.py`
  - `scripts/query-change-record.py`
  - `scripts/test-skill-validator.py`
  - `scripts/test-workflow-automation.py`
  - `scripts/test-validate-workflow-automation.py`
  - adapter generation and validation fixtures
- Dependencies:
  - M1-M5 are complete and independently reviewed.
  - Internal end-to-end authoring and implementation integration proof is clean before any public routing edit is made.
- Tests to add/update:
  - `$workflow auto: <stage>`, status, and off use only unified state.
  - `auto-through: plan-review` and `auto-through: verify` preserve historical target meaning without future-contingent authority or legacy writes.
  - Legacy status is side-effect free; legacy off migrates once and produces a unified cancelled run.
  - Terminal legacy records remain readable; active migration is one-way; mixed writable state fails closed.
  - Unknown aliases report allowed forms; alias removal remains blocked without a separate approved compatibility change.
  - Every affected legacy selector has one disposition, no retained rule exclusively names a retired writer, and duplicate/unknown selectors fail before consistency checks.
  - Run output reports target, position source, parent boundary, capability kind, outcome, gate, transition, fixes, decisions, artifacts, stop reason, and next action.
  - Generated adapters and installed skill projections match canonical guidance; no generated output is hand-edited.
  - No public routing state exists in which unified commands are active while a legacy writer remains enabled.
- Implementation steps:
  - Replace user-facing three-profile routing language with the unified target-driven mechanism and explicit risk-boundary authorization behavior.
  - Activate current commands and legacy adapters in the same reviewed slice that removes every legacy write path.
  - Implement the static affected-selector/disposition validator and retired-writer contradiction checks.
  - Update query/status output and compatibility diagnostics.
  - Regenerate public adapters into temporary release output and validate them with the version recorded in `dist/adapters/manifest.yaml`.
  - Run integration fixtures for proposal-review through verify, interruption recovery, cancellation, migration, isolated review, and stop-before-PR.
- Validation commands:
  - `python scripts/test-workflow-automation.py`
  - `python scripts/test-validate-workflow-automation.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `adapter_version="$(sed -n 's/^version: //p' dist/adapters/manifest.yaml | head -1)"; adapter_output="$(mktemp -d)"; trap 'rm -rf "$adapter_output"' EXIT; python scripts/build-adapters.py --version "$adapter_version" --output-dir "$adapter_output" && python scripts/validate-adapters.py --root "$adapter_output" --version "$adapter_version"`
  - `bash scripts/ci.sh --mode explicit --path skills/workflow/SKILL.md --path schemas/change.schema.json --path scripts/workflow_automation.py --path scripts/workflow_automation_policy.py --path scripts/workflow_automation_state.py --path scripts/validate_workflow_automation.py`
  - `bash scripts/ci.sh --mode broad-smoke`
- Expected observable result: All supported public commands converge atomically on one writable mechanism, legacy meaning remains readable, no retired writer survives, derived guidance is current, and broad integration proof passes without crossing the PR boundary.
- Commit message: `M6: activate bounded review-fix workflow automation`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
  - material findings resolved or explicitly dispositioned before final closeout
  - milestone committed
- Risks:
  - Generated guidance could retain stale profile terminology after canonical code changes.
  - A compatibility adapter could accidentally remain a legacy writer.
  - Public activation could occur before all internal integration proof is current.
- Rollback/recovery:
  - Stop creation and automatic continuation of unified runs, preserve all recorded evidence, retain legacy reads and aliases, and return users to explicit manual stages without restoring legacy writers.

## Validation plan

- Start each milestone with the matching test-spec cases and focused unit commands before broad suites.
- Run every command named by the approved test spec; the test spec may strengthen but not weaken the commands above.
- Run `python scripts/validate-change-metadata.py docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/change.yaml` whenever change metadata is updated.
- Run `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/` after formal review evidence changes.
- Run `python scripts/validate-review-artifacts.py --mode closeout ...` only when no material finding remains open.
- Run `python scripts/validate-artifact-lifecycle.py --mode explicit-paths` over the active plan, plan index, spec, architecture, ADRs, change metadata, and current review evidence before downstream handoffs.
- Run `git diff --check` for every milestone.
- This plan sets `broad_smoke_required: true`; run `bash scripts/ci.sh --mode broad-smoke` during M6 and final verification in addition to focused and selected checks.
- Before `explain-change` or verify, require final holistic code-review evidence across all six milestones and the complete final diff.

## Risks and recovery

- Risk: The migration changes multiple validators and workflow surfaces at once.
  - Recovery: Keep milestones independently reviewable and prevent public routing changes until M6 after the model, state, engine, authoring integration, and implementation integration are separately proven.
- Risk: `change.yaml` is both general metadata and the automation transaction store.
  - Recovery: Centralize writes in one adapter, use complete-file replacement, preserve unrelated fields, reject concurrent identity drift, and test interrupted writes.
- Risk: Current lifecycle parsers and the new engine could become competing sources of canonical position.
  - Recovery: Reuse existing parsers and compare observed identities; do not persist an engine-owned cursor.
- Risk: Legacy compatibility can prolong duplicate semantics.
  - Recovery: Make adapters read-only inputs, validate no legacy write path, and require a later audited compatibility proposal before removal.
- Risk: Automated review integration can weaken independence through shared context.
  - Recovery: Keep formal review invocation, manifests, evidence staging, and verdict ownership outside the transition coordinator and test isolated review behavior directly.
- Risk: A partially integrated engine could become publicly reachable before legacy writers are disabled.
  - Recovery: Keep M1-M5 behind a non-public harness and make M6 the only milestone that changes public command routing and legacy-writer availability.

## Dependencies

- Plan-review approval is required before test-spec authoring.
- An active matching test spec and clean test-spec-review are required before M1 implementation.
- M1-M6 execute in order, and each milestone receives independent code review before the next begins.
- M1-M5 must remain unreachable through public workflow commands; M6 may activate public routing only after current internal integration evidence for all earlier milestones passes.
- Any material review finding must be recorded and resolved or explicitly dispositioned before milestone closure.
- Verification authorization remains absent until its complete post-implementation basis exists.
- No PR or external action is authorized by this plan.

## Progress

- 2026-07-21: Architecture-review R3 approved the design; lifecycle statuses were normalized for planning reliance.
- 2026-07-21: Initial five-milestone execution plan created; plan-review pending.
- 2026-07-21: Plan-review R1 requested executable final-cutover validation and one atomic public activation boundary.
- 2026-07-21: Plan revised to six milestones, split authoring from implementation integration, reserve public activation for M6, and use versioned generated-adapter plus executed selected-CI proof; plan-review R2 pending.
- 2026-07-21: Plan-review R2 approved the six-milestone plan with no material findings; the lifecycle handoff was synchronized to test-spec authoring.
- 2026-07-21: The matching test specification was authored as the active M1-M6 proof map; formal test-spec-review is pending before implementation.
- 2026-07-21: Test-spec-review R1 requested correction of manual-proof contracts, CMD30 executability, and deterministic fixture controls; implementation remains blocked.
- 2026-07-21: Test spec revised with complete MP1-MP3 contracts, a directly executable pipe-free CMD30, normalized CMD18 ownership, deterministic fixture controls, and repeat/order-independence case T29; rereview pending.
- 2026-07-21: Test-spec-review R2 confirmed the three R1 findings resolved and opened `BRF-TSR4`; implementation remains blocked until multi-milestone proof activation is explicit and rereviewed.
- 2026-07-21: Test spec revised for `BRF-TSR4`: T29 now owns independently executable M2 determinism, T30 owns M6 composed-engine determinism, and every progressive case names milestone-local assertions, commands, and deferrals; R3 pending.
- 2026-07-21: Test-spec-review R3 confirmed the determinism split but kept `BRF-TSR4` open because T26 remains listed at M6 without a matching case-level or progressive activation contract.
- 2026-07-21: Test spec revised to complete `BRF-TSR4`: T26 now proves non-public routing at M4/CMD17 and public composition at M6/CMD25 with explicit deferral; R4 pending.
- 2026-07-21: Test-spec-review R4 approved the 30-case proof map, confirmed all four test-spec findings resolved, and allowed M1 implementation handoff; this isolated review did not start implementation.
- 2026-07-21: M1 implementation started from the approved R4 handoff; scope is limited to the unified state model, immutable policy projection, and fail-closed structural validation, with public routing intentionally unchanged.
- 2026-07-21: M1 added the canonical unified schema, immutable eighteen-stage policy projection, closed state/authority vocabularies, stage-relative capability validation, and metadata integration. All five M1 commands passed; the milestone is review-requested and no writer or public route was enabled.
- 2026-07-21: Code-review M1 R1 requested changes in `BRF-M1-CR1` through `BRF-M1-CR4`: internal and milestone capability occurrences, concrete basis/invalidation validation, complete receipt bindings, and exhaustive negative proof remain incomplete. M1 is resolution-needed; M2 is blocked.
- 2026-07-21: M1 review resolution implementation started for the four accepted R1 findings. The correction remains limited to policy/state validation and direct M1 proof; M2 writer and routing work remain out of scope.
- 2026-07-21: Resolved `BRF-M1-CR1` through `BRF-M1-CR4` by deriving occurrence validation from the immutable policy registry, enforcing concrete authority/invalidation evidence, validating complete capability-bound receipts, and expanding the negative proof matrix. M1 is review-requested; M2 remains blocked pending M1 rereview.
- 2026-07-21: Code-review M1 R2 confirmed all four R1 findings resolved and opened `BRF-M1-CR5` through `BRF-M1-CR7` for receipt destination/operation conflation, incorrect proof contrasts, placeholder evidence acceptance, and incomplete parent maximum targets. M1 is resolution-needed; M2 remains blocked.
- 2026-07-21: Resolved `BRF-M1-CR5` through `BRF-M1-CR7` with destination/operation separation, operation-to-target bounds, recursive concrete evidence validation, complete parent structured targets, and corrected contrast fixtures. M1 is review-requested; M2 remains blocked pending M1 R3.
- 2026-07-21: Code-review M1 R3 resolved `BRF-M1-CR7` but opened `BRF-M1-CR8` and `BRF-M1-CR9` after direct proof showed arbitrary/backward from-positions, mutable validator-local reachability policy, whitespace evidence, and non-finite evidence still pass. M1 is resolution-needed; M2 remains blocked.
- 2026-07-21: Resolved `BRF-M1-CR8` and `BRF-M1-CR9` by moving canonical predecessor/next-stage relations into the frozen policy projection, validating receipt transitions through that graph, and rejecting recursively non-deterministic evidence. M1 is review-requested; M2 remains blocked pending M1 R4.
- 2026-07-21: Code-review M1 R4 confirmed `BRF-M1-CR9` resolved but classified `BRF-M1-CR8` as failed remediation and opened `BRF-M1-CR10`: cyclic reachability permits code review after exact implement targets and proposal correction after exact proposal-review targets. M1 is resolution-needed; M2 remains blocked.
- 2026-07-21: Resolved `BRF-M1-CR10` by replacing cyclic stage-name reachability with immutable target-aware transition rules bound to predecessor, operation, target frontier, guard, and occurrence constraint. Exact implement and proposal-review stopping regressions pass; M1 is review-requested and M2 remains blocked pending M1 R5.
- 2026-07-21: Code-review M1 R5 confirmed the exact-target fixtures but classified `BRF-M1-CR10` as failed remediation and opened `BRF-M1-CR11`: transition selectors ignore their declared guards and occurrence constraints, so missing architecture-applicability evidence and arbitrary next-milestone context still pass. M1 is resolution-needed; M2 remains blocked.
- 2026-07-21: Resolved `BRF-M1-CR11` with one typed transition evaluator that enforces target frontier, all guarded branches, plan-bound same/next milestone identities, and missing-context rejection from identity-bound receipt evidence. M1 is review-requested; M2 remains blocked pending M1 R6.
- 2026-07-21: Code-review M1 R6 confirmed guard enforcement but classified `BRF-M1-CR11` as failed remediation and opened `BRF-M1-CR12`: the stage-only next-milestone frontier rejects valid `implement@M2` and `code-review@M2` targets. M1 is resolution-needed; M2 remains blocked.
- 2026-07-22: Resolved `BRF-M1-CR12` by admitting repeated targets on the next-milestone edge only when their persisted target occurrence equals the identity-bound next milestone. M1 is review-requested; M2 remains blocked pending M1 R7.
- 2026-07-22: Code-review M1 R7 independently confirmed `BRF-M1-CR12` resolved with no new material findings. M1 is closed and the next stage is implement M2.
- 2026-07-22: M2 added the sole atomic state adapter, capability-bound prepared/finalized receipts, evidence-first recovery and cancellation, exact one-way legacy migration receipts, and read-only unified status projection. All plan-mandated M2 commands pass; M2 is review-requested and the public workflow route remains unchanged.
- 2026-07-22: Code-review M2 R1 requested changes in `BRF-M2-CR1` through `BRF-M2-CR4`: recovery is not bound to the persisted receipt or immutable retry policy, T29 proof is incomplete, and unified status bypasses state validation. M2 is resolution-needed; M3 remains blocked.
- 2026-07-22: M2 review-resolution implementation started for the four accepted R1 findings. The correction is limited to canonical receipt/policy binding, complete T29 determinism proof, and validated read-only status projection; public routing remains out of scope.
- 2026-07-22: Resolved `BRF-M2-CR1` through `BRF-M2-CR4` by binding recovery to canonical persisted receipt IDs, deriving retry from the immutable registry with key-bound projections, completing the fresh-root T29 repeat/reverse proof, and validating unified status before projection. M2 is review-requested for R2; M3 remains blocked.
- 2026-07-22: Code-review M2 R2 confirmed `BRF-M2-CR1`, `BRF-M2-CR3`, and `BRF-M2-CR4` resolved, classified `BRF-M2-CR2` as failed-remediation, and opened `BRF-M2-CR5` and `BRF-M2-CR6` for missing persisted transition-key validation and invalid all-family retry fixtures. M2 is resolution-needed; M3 remains blocked.
- 2026-07-22: M2 R2 review-resolution implementation started with proof-first stale-key tests across validator, canonical read, recovery, and query boundaries plus complete persisted states for all three retry policies. No public routing or M3 behavior is in scope.
- 2026-07-22: Resolved `BRF-M2-CR5` and `BRF-M2-CR6` by centralizing deterministic transition-key validation across canonical state boundaries and replacing synthetic retry tests with complete persisted states for architecture-assessment, proposal-review, and implement@M2. M2 is review-requested for R3; M3 remains blocked.
- 2026-07-22: Code-review M2 R3 independently confirmed `BRF-M2-CR5` and `BRF-M2-CR6` resolved with no new material findings. M2 is closed and the next stage is implement M3.
- 2026-07-22: M3 implementation started with T4-T9 and T14 as the same-slice proof boundary. Public workflow skill commands, legacy public adapters, stage-native authoring/review behavior, and M4-M6 integration remain intentionally unaffected until their approved milestones.
- 2026-07-22: M3 added closed current/legacy command normalization, structured occurrence binding, immutable repeated-target resume, pre-plan and active-plan canonical-position resolution, risk-scoped parent/capability evaluation, and one-stage prepared-receipt coordination. All M3 commands and repository broad smoke pass; M3 is review-requested while public routing remains unchanged.
- 2026-07-22: Code-review M3 R1 requested changes in `BRF-M3-CR1` through `BRF-M3-CR4`: canonical evidence is not bound to invocation, target completion is mutable, correction budgets are not enforced during derivation, and arbitrary output is finalized as synchronized. M3 is resolution-needed; M4 remains blocked.
- 2026-07-22: M3 R1 review-resolution implementation started with proof-first regressions for canonical evidence binding, exact target completion, correction-budget scope, and stage-owned completion/synchronization. Public routing and M4-M6 integration remain unchanged.
- 2026-07-22: Resolved `BRF-M3-CR1` through `BRF-M3-CR4` by binding canonical evidence before invocation, deriving immutable target completion from policy, enforcing proposal and implementation correction budgets, and requiring typed stage completion plus canonical synchronization proof. M3 is review-requested for R2; M4 remains blocked.
- 2026-07-22: Code-review M3 R2 confirmed `BRF-M3-CR1` and `BRF-M3-CR2` resolved, classified `BRF-M3-CR3` and `BRF-M3-CR4` as failed remediations, and opened `BRF-M3-CR5` and `BRF-M3-CR6` for unbound implementation budget identity and callback-fabricated completion/synchronization. M3 is resolution-needed; M4 remains blocked.
- 2026-07-22: Resolved `BRF-M3-CR5` and `BRF-M3-CR6` by requiring exact correction-budget basis binding and replacing callback-selected completion with immutable policy postconditions plus independently rehashed repository evidence and durable synchronization identities. M3 is review-requested for R3; M4 remains blocked.
- 2026-07-22: Code-review M3 R3 confirmed `BRF-M3-CR5` resolved, classified `BRF-M3-CR6` as failed remediation, and opened `BRF-M3-CR7`. Arbitrary in-scope bytes still satisfy stage completion, synchronization may echo callback evidence, and recovery/cancellation consume authority from nonexistent evidence. M3 is resolution-needed; M4 remains blocked.
- 2026-07-22: Resolved `BRF-M3-CR7` with a repository-parser-backed proposal-review completion verifier enforced by the sole state writer and reused by coordinator completion, prepared/completed recovery, and cancellation. Exact reviewed-proposal identity and canonical review-log occurrence are independently reread; unsupported later-stage verifiers fail closed until M4/M5. M3 is review-requested for R4; M4 remains blocked.
- 2026-07-22: Code-review M3 R4 classified `BRF-M3-CR7` as failed remediation and opened `BRF-M3-CR8`. A symlinked review log outside the repository still satisfies canonical completion, and review-log identity drift is not persisted or detected during completed recovery. M3 is resolution-needed; M4 remains blocked.
- 2026-07-22: M3 R4 review-resolution implementation started with proof-first repository-containment, canonical-log identity drift, and engine-derived persistence contrasts. Public routing and M4-M6 integration remain unchanged.
- 2026-07-22: Resolved `BRF-M3-CR8` by rejecting symlinks in every repository-owned completion path, independently hashing the canonical review log, and making normal completion, recovery, and cancellation persist only verifier-derived normalized proof. M3 is review-requested for R5; M4 remains blocked.
- 2026-07-22: Code-review M3 R5 confirmed the path-level symlink and log-drift cases resolved, classified the repository-owned portion of `BRF-M3-CR8` as failed remediation, and opened `BRF-M3-CR9` plus `BRF-M3-CR10`. A caller-selected root can still supply unrelated-repository evidence, and the R4 handoff reason contradicted its closed review state. M3 is resolution-needed; M4 remains blocked.
- 2026-07-22: Resolved `BRF-M3-CR9` and `BRF-M3-CR10` by binding the state store to its canonical repository root, rejecting foreign roots before invocation or finalization, inferring and validating canonical change-metadata ownership, and requiring the plan handoff reason code to agree with structured open-finding evidence. M3 is review-requested for R6; M4 remains blocked.
- 2026-07-22: Code-review M3 R6 classified both R5 corrections as failed remediations and opened `BRF-M3-CR11` plus `BRF-M3-CR12`. Constructor-time ancestor or symlink root rebinding remains possible, and authoritative bounded detail can still contradict formal open-finding state. M3 is resolution-needed; M4 remains blocked.
- 2026-07-22: M3 R6 review-resolution implementation started with proof-first ancestor-root, canonical metadata symlink, exact-root, review-state count/ID, and contradictory-detail regressions. M4-M6 and public routing remain out of scope.
- 2026-07-22: Resolved `BRF-M3-CR11` and `BRF-M3-CR12` by binding construction to the lexical canonical metadata layout, rejecting metadata-path symlinks and non-exact explicit roots, removing the finalizer root override, and validating an exact open-review count/ID detail projection with no independent finding claims. M3 is review-requested for R7; M4 remains blocked.
- 2026-07-22: Code-review M3 R7 classified both R6 corrections as failed remediations and opened `BRF-M3-CR13` plus `BRF-M3-CR14`. A symlink earlier than the derived repository root still redirects ownership, and a second structured review-state claim can contradict the validated detail prefix. M3 is resolution-needed; M4 remains blocked.
- 2026-07-22: M3 R7 review-resolution implementation added proof-first earlier-ancestor symlink and duplicate/unstructured state-field regressions; each reproduced the reported bypass before production correction.
- 2026-07-22: Resolved `BRF-M3-CR13` and `BRF-M3-CR14` by checking the entire absolute lexical metadata chain before resolution and rejecting all additional structured fields outside the single review-state projection. M3 is review-requested for R8; M4 remains blocked.
- 2026-07-22: Code-review M3 R8 confirmed the full-chain symlink correction, classified the R7 review-state correction as failed remediation, and opened `BRF-M3-CR15`. Alternate structured keys and plain contradictory prose remain accepted in the authoritative detail. M3 is resolution-needed; M4 remains blocked.
- 2026-07-22: Resolved `BRF-M3-CR15` by replacing the prefix-plus-remainder parser and denylist with one exact generated projection for the complete live review-state detail in both open and closed states. Exact open/closed and alternate-key/plain-prose regressions pass; M3 is review-requested for R9 and M4 remains blocked.
- 2026-07-22: Code-review M3 R9 independently confirmed `BRF-M3-CR15` resolved with no new material findings. M3 is closed; the next explicit stage is implement M4.
- 2026-07-22: M4 implementation started with proposal-review outcome routing, bounded driver-owned proposal correction, conditional authoring progression through `test-spec-review`, and explicit non-public harness isolation. Public workflow and legacy adapter activation remain reserved for M6.
- 2026-07-22: M4 added exhaustive proposal-review occurrence/gate routing, unchanged-inconclusive retry prevention, driver-owned bounded proposal correction with stale-review/rereview enforcement, and deterministic authoring/architecture routing through `test-spec-review`. CMD14-CMD20, the full engine suite, and repository broad smoke pass; M4 is review-requested and remains unreachable from public and legacy commands.
- 2026-07-22: Code-review M4 R1 requested changes in `BRF-M4-CR1` and `BRF-M4-CR2`: the M4 authoring path is helper-only rather than receipt-backed, and proposal correction trusts unbound caller assertions with optional classification history. M4 is resolution-needed; M5 remains blocked.
- 2026-07-22: The user accepted the recorded safe resolutions for `BRF-M4-CR1` and `BRF-M4-CR2`. M4 correction implementation started with transactional stage proof and canonical correction-evidence binding; M5 and public routing remain out of scope.
- 2026-07-22: Resolved `BRF-M4-CR1` and `BRF-M4-CR2` by connecting authoring and proposal correction to the prepared-receipt coordinator, adding parser-backed completion for all M4 stages, and deriving correction authority from exact persisted capability identities. M4 is review-requested for R2; public and legacy routing remain unchanged.
- 2026-07-22: Code-review M4 R2 classified both R1 findings as failed remediations and opened `BRF-M4-CR3` plus `BRF-M4-CR4`: non-review completed recovery is review-log-specific, and correction authority/convergence remains caller-substitutable. M4 is resolution-needed; M5 remains blocked.
- 2026-07-23: The user accepted the recorded safe resolutions for `BRF-M4-CR3` and `BRF-M4-CR4`. M4 correction implementation started with stage-generic recovery, identity-stable routing, repository-derived correction authority, and independent post-mutation convergence proof; M5 and public routing remain out of scope.
- 2026-07-23: Resolved `BRF-M4-CR3` and `BRF-M4-CR4` with stage-generic completed recovery, verifier-owned route facts, canonical tracked correction evidence, exact persisted budget identities, independent post-mutation convergence, and atomic correction-capability handoff. Failed postconditions pause the receipt and invalidate spent correction authority; successful finalization consumes it and activates exactly one fresh proposal-review capability in the same state write. M4 is review-requested for R3; M5 and public routing remain blocked.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-21 | Build the immutable model before enabling any new writer. | Closed policy and state contracts provide a safe base for transactional and routing behavior. | Editing public workflow guidance first would expose an unimplemented contract. |
| 2026-07-21 | Establish the sole state writer before the transition engine. | Prepared receipts and recovery must exist before a coordinator can safely invoke stages. | Letting the engine write YAML directly would duplicate persistence and recovery logic. |
| 2026-07-21 | Reserve public and legacy command cutover for M6. | Compatibility, retired-writer removal, and public guidance must activate atomically after internal behavior is proven. | Editing public routing during M4 or M5 could expose a partially migrated engine. |
| 2026-07-21 | Use six independently reviewed implementation milestones. | Authoring/review correction and implementation/verification have different authority, evidence, and recovery risks. | One combined stage-integration milestone would be too broad; per-stage milestones would create excessive coupling and overhead. |
| 2026-07-21 | Require generated release-output adapter proof and executed selected CI at cutover. | The active adapter contract is archive-based and selection output alone is not validation execution. | Bare tracked-tree adapter checks and selection-only output are not reliable milestone gates. |
| 2026-07-21 | Treat receipt target as the run destination and effective-capability stage as the concrete operation. | Target selection and executable authority are independent; direct equality rejects valid earlier transitions toward later targets. | Reusing one field for both concepts or adding an unapproved receipt schema field. |
| 2026-07-22 | Reuse the canonical handoff parser and persist no engine-owned cursor. | Target binding and position resolution must agree with existing lifecycle validation before and after plan creation. | Reimplementing plan handoff semantics inside the engine would create a competing workflow truth. |
| 2026-07-22 | Validate the candidate capability-and-receipt state before the first M3 write. | Invalid transition inputs and an existing in-flight receipt must fail before invocation or partial authority persistence. | Relying only on sequential writer validation could leave avoidable orphan capability state after a predictable precondition failure. |
| 2026-07-21 | Represent predecessor and next-stage relations as an immutable typed graph in the policy projection. | Conditional stages, correction loops, and repeated milestones cannot be modeled safely by a mutable linear rank table. | Validator-local frontier/rank maps and free-form predecessor strings. |
| 2026-07-21 | Bind transition permission to an immutable edge-specific target frontier. | Generic reachability over a cyclic graph cannot preserve exact structured targets as stopping boundaries. | Unqualified breadth-first reachability and validator-local cycle exceptions. |
| 2026-07-21 | Make `evaluate_transition` the only executable transition-permission decision. | Immutable guard and occurrence metadata is not a policy unless every selected rule evaluates it against concrete evidence. | Decorative predicate fields and boolean helpers whose names imply executable permission. |
| 2026-07-22 | Evaluate repeated-stage target frontiers against the bound next-milestone occurrence. | Stage names alone cannot distinguish an already-reached M1 target from the same stage requested for M2. | M2-specific exceptions, unqualified cyclic reachability, and allowing every repeated-stage occurrence. |
| 2026-07-22 | Treat policy-derived, repository-backed artifact identities as the M3 completion boundary. | A typed callback is transport, not proof; the coordinator must independently reread concrete evidence before consuming capability authority. | Caller-selected postconditions, status-only synchronization, and callback-supplied observed identities. |
| 2026-07-22 | Bind completion to no-symlink canonical paths and verifier-derived canonical-owner identities. | Canonical evidence remains trustworthy only when its repository-owned path and independently observed bytes are stable across completion and resume. | Following in-repository or external symlinks, or persisting callback-selected canonical identities. |
| 2026-07-22 | Bind every mutable automation operation to the state store's immutable repository root. | Path containment is meaningful only when the root is the repository that canonically owns the change metadata. | Caller-selected evidence roots and silent rebinding during finalization or recovery. |
| 2026-07-22 | Derive canonical state ownership from the lexical metadata layout before resolving filesystem paths. | Resolving first erases symlink and repository-boundary evidence that must be rejected. | Ancestor containment and post-resolution layout inference. |
| 2026-07-22 | Reserve one exact review-state clause in live closeout detail. | Count and ID projection is deterministic, while broad prose interpretation is incomplete and unsafe. | Free-form finding-state claims and repository-wide historical prose scanning. |
| 2026-07-22 | Validate canonical metadata symlinks across the complete absolute lexical chain. | Starting at the derived root leaves earlier ancestors able to erase ownership evidence during resolution. | Partial descendant-only symlink walks and post-resolution inference. |
| 2026-07-22 | Serialize the complete live review-state detail as one exact generated projection with no remainder. | Exact equality against formal review evidence closes both structured-key and equivalent-prose bypasses without attempting natural-language classification. | Prefix validation, remainder denylists, and any unrestricted trailing detail. |
| 2026-07-22 | Serialize complete change metadata behind a directory lock and compare-and-swap identity check. | One stable lock boundary prevents concurrent writers from both passing the identity check while atomic replacement prevents truncation. | Direct subsection edits, unlocked replacement, and a second persisted state file. |
| 2026-07-22 | Bind migration receipts to the canonical hash of exactly one active legacy source record. | A boolean read-only marker alone cannot prove which historical writer was frozen or prevent fabricated migration evidence. | Unbound compatibility markers and rewriting the legacy record. |
| 2026-07-23 | Finalize correction completion and replacement review authority in one state write. | A completed correction receipt without its fresh review capability creates an unrecoverable authority gap. | Finalizing first and persisting replacement authority in a second write. |

## Surprises and discoveries

- Existing automation behavior is implemented primarily as schema validation, lifecycle route evaluators, review validation, and skill guidance rather than one executable engine.
- The current change schema permits three legacy state families, so migration must preserve reads while proving that every new write uses only `workflow.automation`.
- The repository has no dedicated Mermaid renderer; architecture diagram changes route through canonical package lifecycle validation and manual review.
- A parent consent envelope still carries a complete structured target; reducing it to stage and occurrence kind silently loses repeated-stage identity before authorization persistence.
- A stage-only frontier cannot represent stopping order across repeated milestone occurrences; the target milestone must participate in next-edge permission.

## Validation notes

- M4 R2 resolution passes 36 engine, 51 state/recovery, and 54 automation-validator tests. Regression proof covers completed recovery for spec, architecture assessment, plan, and formal review stages; raw-path-free routing; forged or stale correction evidence; empty, extra, over-limit, and identity-drifted budgets; false validation; non-shrinking findings; historical-review drift; missing fresh authority; atomic correction-to-rereview capability handoff; and failed-postcondition invalidation.
- CMD14-CMD20 pass after the correction, and the required final repository broad-smoke suite passes all 12 checks in 253 seconds. Public workflow and legacy adapters, M5 behavior, generated outputs, and external-action surfaces are unaffected because this correction remains behind the M4 non-public harness.
- Code-review M4 R2 used an L2 separated blind-first risk map before releasing tests, validation summaries, or prior findings. CMD14-CMD20 and full engine/state/validator suites passed, but direct probes reproduced empty-budget routing, stale persisted budget acceptance, preflight authorization without post-mutation validation, and completed non-review recovery that always pauses for absent review-log identity.
- M4 R1 correction passes 3 proposal-review, 3 proposal-correction, 4 authoring, and 3 non-public selected tests; all 33 engine, 49 state/recovery, and 52 automation-validator tests pass. Receipt-backed spec and proposal-correction fixtures prove prepared-receipt ordering, parser-backed completion, exact capability consumption, rereview routing, and pre-write rejection of public, direct, bugfix, and legacy contexts.
- CMD14, CMD19, and CMD20 pass all 156 lifecycle, 103 review-artifact, and 259 skill-validator tests. All 53 metadata-validator tests, closeout review validation with 57/57 findings resolved, change metadata validation, guide validation, exact lifecycle validation, Python compilation, and diff checks pass.
- Validation selection reports expected manual routing for the four unsupported automation engine/test paths; the plan-owned CMD15-CMD18 and full engine/state/validator suites cover them directly. The required repository broad-smoke command passes. Public workflow/legacy adapters, external actions, and M5 implementation behavior remain unchanged.
- Code-review M4 R1 reran CMD14-CMD20 successfully, then found that the M4 authoring/correction evaluators have no non-test call sites and that the state-native verifier supports only `proposal-review`.
- Direct adversarial probes returned `correction-loop` from caller booleans without durable capability evidence and returned `rereview-required` when prior finding classifications were omitted. MP1 cannot pass until a composed non-public invocation path exists.
- Review structure passed with 38 reviews, 57 findings, and 2 open findings; metadata, guide-system, lifecycle state synchronization, and diff checks pass. Closeout validation correctly remains blocked by `BRF-M4-CR1` and `BRF-M4-CR2`.

- M4 proof-first execution failed before production changes because the proposal-review, proposal-correction, and non-public authoring decision interfaces did not exist.
- CMD15-CMD18 pass with 3 proposal-review, 1 proposal-correction, 3 authoring, and 2 non-public selected tests; the full automation-engine suite passes all 30 tests.
- CMD14, CMD19, and CMD20 pass all 156 lifecycle, 103 review-artifact, and 259 skill-validator tests. Python compilation and `git diff --check` also pass.
- The validation selector selected lifecycle validation and broad smoke while reporting expected manual routing for the two unsupported automation script paths covered by CMD15-CMD18. The final repository broad-smoke rerun passed all 11 checks in 409 seconds after executable correction-capability binding was tightened.
- M4 does not change `skills/workflow/SKILL.md`, public command routing, legacy adapter behavior, or any external-action boundary; those remain reserved for M6.

- Code-review M3 R9 reran the exact open/closed and reported bypass contrasts, terminal-history compatibility, all 156 lifecycle tests, CMD10-CMD13, current lifecycle validation, selector routing, and diff checks. No new material finding was identified.

- M3 R8 proof-first regressions failed before correction for exact open and closed projections plus alternate-key and plain contradictory suffixes.
- The correction passes 48 state/recovery tests, 23 engine tests, CMD10-CMD14 including 156 lifecycle tests, 52 automation-validator tests, 103 review-parser tests, and Python compilation.
- The selector chose review-artifact, lifecycle, metadata, guide-system, and broad-smoke checks with no unclassified paths or registration debt. Repository broad smoke passed all 11 checks in 455 seconds.
- Governing spec, test spec, architecture, and ADR are unchanged: the correction completes their existing fail-closed live-state projection and leaves terminal plan history outside the live contract.

- Code-review M3 R8 independently reran 48 state and 154 lifecycle tests, confirmed the earlier-ancestor symlink is rejected, and reproduced three review-state remainder bypasses despite those suites passing.

- M3 R7 proof-first tests failed for a symlink above the derived repository root, a second `review-state`, and zero formal state with unstructured state fields before production changes.
- The correction passes 48 state/recovery tests, 23 engine tests, CMD10-CMD14 including 154 lifecycle tests, 52 automation-validator tests, 103 review-parser tests, and Python compilation.
- The selector chose `artifact_lifecycle.regression` and `broad_smoke.repo`, with expected manual-routing diagnostics for two unsupported automation-state script paths covered by explicit suites. Broad smoke passed all 11 checks in 478 seconds.
- Governing spec, test spec, architecture, and ADR are unaffected: this correction enforces their already-approved canonical ownership and fail-closed state-synchronization boundaries without changing the contract or component model.

- Code-review M3 R7 independently reran 47 state tests, 153 lifecycle tests, and CMD10-CMD12, then reproduced earlier-ancestor symlink rebinding and two contradictory structured review-state cases despite those suites passing.

- M3 R6 proof-first tests failed for ancestor-root construction, symlinked metadata file/directory, and contradictory review-state detail before production changes.
- The correction passes 47 state/recovery tests, 23 engine tests, CMD10-CMD14 including 153 lifecycle tests, 52 automation-validator tests, and 103 review-parser tests.
- The selector required lifecycle regression and broad smoke while reporting expected manual routing for three unsupported automation paths. Repository broad smoke passed all 11 checks in 400 seconds.

- Code-review M3 R6 independently reran CMD10-CMD14 and the focused new tests, then reproduced ancestor-root acceptance, metadata-symlink escape, and contradictory live reason detail despite those suites passing.

- M3 R5 proof-first regressions reproduced completion against a foreign repository root and both directions of review-finding reason drift before the production correction.
- The corrected boundary passed 23 engine tests, 43 state/recovery tests, and 151 lifecycle tests. Canonical-layout tests also prove repository-root inference and change-directory identity rejection.
- The validation selector chose the full lifecycle regression and required repository broad smoke; unsupported automation modules retained the expected plan-owned manual routing. Broad smoke passed all 11 checks in 443 seconds.

- `architecture-review-r3` approved the architecture package with no material findings.
- Review structure and closeout validation passed with 12 reviews and 16 resolved findings before planning.
- `python scripts/test-change-metadata-validator.py` passed 48 tests for the updated metadata contract.
- `python scripts/validate-change-metadata.py docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/change.yaml` passed.
- `python scripts/validate-guide-system.py` passed for the updated plan index.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` validated the plan, plan indexes, architecture, ADR settlement, and change metadata after contract-shape corrections.
- Plan-review R1 recorded `BRF-PL1` and `BRF-PL2`; this revision applies both bounded corrections and awaits plan-review R2.
- `bash scripts/ci.sh --mode explicit ...` passed all six selected checks for the revised plan, including repository broad smoke in 377.30 seconds.
- Plan-review R2 approved the revised plan with no material findings; `BRF-PL1` and `BRF-PL2` are resolved and review closeout is closed.
- `specs/single-bounded-review-fix-workflow-automation.test.md` records 30 test cases, 32 validation-command IDs, all six milestone proof gates, and upstream artifact identities for formal review.
- Test-spec-review R1 recorded `BRF-TSR1`, `BRF-TSR2`, and `BRF-TSR3`; no implementation validation was claimed or executed by the review.
- The bounded test-spec revision addresses all three R1 findings without changing approved feature, architecture, or milestone semantics; implementation remains blocked pending test-spec-review R2.
- Test-spec-review R2 confirmed `BRF-TSR1` through `BRF-TSR3` resolved and recorded `BRF-TSR4` for ambiguous command/assertion activation in multi-milestone proof cases; no implementation validation was run.
- Test-spec-review R2 recording checks passed with 16 reviews, 22 findings, and 1 open finding; change metadata and scoped diff checks also passed.
- The `BRF-TSR4` revision adds one M6-only composed determinism case and an exhaustive progressive activation map without changing the approved feature, architecture, or milestone sequence; no planned implementation command was executed during authoring.
- Static authoring checks confirmed 30 test cases, 32 command records, all 14 progressive activation entries, removal of the T29/CMD25 cross-boundary mapping, and the current plan identity recorded by the test spec.
- Test-spec-review R3 recorded no new finding ID and kept `BRF-TSR4` open for the remaining T26 M4/M6 mapping omission; no implementation validation was run.
- Test-spec-review R3 recording checks passed with 17 reviews, 22 findings, and 1 open finding; change metadata and scoped diff checks also passed.
- The final `BRF-TSR4` revision adds T26 as the fifteenth progressive activation entry without changing requirements, commands, milestones, or implementation scope; no planned implementation command was executed.
- Static authoring and lifecycle checks confirmed 30 tests, 32 commands, all 15 progressive entries, T26 M4/M6 ownership, current plan identity, valid review structure and change metadata, and a clean scoped diff.
- Test-spec-review R4 approved the active test specification with no material findings; planned commands were not executed by the review, and M1 is now the next implementation stage.
- Test-spec-review R4 recording checks passed in structure and closeout modes with 18 reviews and 22 resolved findings; change metadata and scoped diff checks also passed.
- M1 proof-first failures were observed before implementation: both new unit modules were missing and three unified metadata rejection cases incorrectly passed.
- Code-review M1 R1 reran the focused M1 suites successfully, then directly reproduced four malformed states that returned no validation errors: null required basis identity, wrong internal-stage occurrence, incompatible receipt target occurrence, and empty invalidation behavior. Review resolution and M1 rereview are required before M2.
- Review-resolution proof-first tests failed on all four reproduced gaps before the production validator changed. After correction, each reproduction returns an actionable validation error and valid records for all six capability kinds pass.
- M1 rereview validation passed: 9 policy tests, 5 selected vocabulary tests, 25 full automation-validator tests, 4 focused metadata tests, 52 full metadata regressions, and 11 repository broad-smoke checks. The validation selector reported manual-routing-required for the four new unsupported script paths; the plan-owned explicit M1 commands covered those paths and selected lifecycle/review/metadata/guide checks were executed directly.
- Final post-correction broad smoke passed all 11 checks in 376 seconds after adding explicit prepared/active, completed/consumed, and parent-revocation consistency proof.
- M1 R2 proof-first regressions failed for later-target/current-operation separation, four incomplete parent-target variants, and null/empty receipt evidence before production changes.
- M1 R2 resolution passed 30 automation-validator tests, 9 policy tests, 4 focused metadata tests, all 52 metadata-validator tests, and 11 repository broad-smoke checks in 346 seconds.
- M1 R3 proof-first tests failed because the typed transition graph exports did not yet exist; the prior validator also accepted the direct unknown/backward-position and non-deterministic-evidence cases.
- M1 R3 resolution passed 11 policy tests, 35 automation-validator tests, 4 focused metadata tests, all 52 metadata-validator tests, metadata validation, Python compilation, diff checks, and 12 repository broad-smoke checks in the final 230-second run.
- Code-review M1 R4 reran 11 policy tests, 35 automation-validator tests, and 4 focused metadata tests successfully, then directly reproduced two complete post-target receipts that returned no validation errors. Existing coverage is insufficient for exact-target stopping across cycles.
- M1 R4 proof-first regressions reproduced both complete post-target paths before the production correction. The final resolution passed 13 policy tests, 37 automation-validator tests, 5 selected vocabulary tests, 4 focused metadata tests, all 52 metadata tests, metadata validation, Python compilation, diff checks, and 12 repository broad-smoke checks in 216 seconds.
- Review structure and closeout validation passed with 22 reviews, 32 resolved findings, and no open findings. Explicit lifecycle validation passed for the five managed handoff artifacts with the existing merge-language warning, and guide-system validation passed after plan-index synchronization.
- Code-review M1 R5 reran 13 policy tests, 37 automation-validator tests, 4 focused metadata tests, metadata validation, and diff checks successfully, then directly reproduced two complete predicate-context gaps that returned no validation errors. Passing suites do not establish guard or occurrence-constraint enforcement.
- Code-review M1 R5 recording passed review-structure validation with 23 reviews, 33 findings, and 1 open finding; lifecycle validation passed for five managed artifacts with the existing merge-language warning; guide-system, change-metadata, and diff checks passed after handoff synchronization.
- M1 R5 proof-first tests failed on the missing evaluator and both complete predicate-context gaps before production changes. The final correction passed 15 policy tests, 41 automation-validator tests, 5 selected vocabulary tests, 4 focused metadata tests, all 52 metadata tests, metadata validation, Python compilation, diff checks, and 12 repository broad-smoke checks in the final 231-second run after plan and milestone identity binding was tightened.
- Review structure and closeout validation passed with 23 reviews, 33 resolved findings, and no open findings. Explicit lifecycle validation passed for the five managed handoff artifacts with the existing merge-language warning, and guide-system validation passed after the M1 R6 plan-index synchronization.
- M1 R6 proof-first regressions failed for valid `code-review@M1 -> implement@M2` transitions toward both `implement@M2` and `code-review@M2`; the final `verify` target control remained accepted.
- M1 R6 resolution passed 15 policy tests, 42 automation-validator tests, 5 selected vocabulary tests, 4 focused metadata tests, all 52 metadata tests, Python compilation, and 12 repository broad-smoke checks in 299 seconds. Bound M2 repeated targets pass while stale M1 and missing target occurrence identities fail closed.
- Code-review M1 R7 directly challenged the repeated-target boundary matrix, reran 15 policy, 42 automation-validator, 5 vocabulary, 4 focused metadata, and 52 metadata tests, and returned clean-with-notes. Review structure/closeout, lifecycle state sync, metadata, guide-system, compilation, and diff checks pass; M1 is closed.
- `python scripts/test-workflow-automation-policy.py` passed 7 tests.
- `python scripts/test-validate-workflow-automation.py -k vocabulary` passed 3 selected tests.
- `python scripts/test-change-metadata-validator.py -k workflow_automation` passed 4 selected tests.
- `python scripts/test-change-metadata-validator.py` passed 52 tests.
- `python scripts/validate-change-metadata.py docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/change.yaml` passed after handoff synchronization.
- `python scripts/test-validate-workflow-automation.py` passed all 11 tests in addition to the required vocabulary selection.
- `python scripts/validate-guide-system.py` passed for the synchronized plan index.
- Explicit-path artifact lifecycle validation passed for 5 lifecycle-managed artifacts and retained the existing non-blocking lifecycle-language warning in `review-resolution.md` line 444.
- `git diff --check` passed after handoff synchronization.
- M1 intentionally adds no `workflow.automation` writer, command adapter, stage invocation, or public skill change; those boundaries remain assigned to M2-M6.
- M2 proof-first execution failed because `workflow_automation_state.py` did not exist. The completed slice passes 24 state/recovery tests, 15 receipt-selected validator tests, 3 migration-selected validator tests, 17 query tests, all 53 metadata-validator tests, direct change-metadata validation, Python compilation, and diff checks.
- M2 keeps the new writer unreachable from public commands. It uses complete-file atomic replacement with file-mode preservation, directory locking, identity compare-and-swap, prepared receipt persistence, deterministic transition keys, evidence-first recovery, cancellation settlement, and exact legacy-source migration binding.
- Code-review M2 R1 reran CMD4-CMD9 successfully, then directly reproduced retry from an unpersisted receipt, retry-policy override without transition-key change, and successful status projection of an unknown run status. Static T29 inspection found no full repeated/reverse-order scenario or canonical-file comparison.
- M2 R1 resolution passed 27 state/recovery tests, 17 receipt-selected validator tests, 3 migration-selected validator tests, 18 query tests, all 53 metadata-validator tests, direct change-metadata validation, Python compilation, and diff checks. Direct contrasts reject missing/substituted receipt IDs, retry-policy mismatch, and unknown run/policy/receipt/migration status projection; T29 compares canonical bytes and cleanup across repeated and reverse-order fresh-root scenarios.
- Code-review M2 R2 independently reran CMD4-CMD9 and directly proved that stale transition keys survive canonical validation/recovery and that the architecture-assessment and implement retry fixtures are not validator-valid states. Passing suites do not close `BRF-M2-CR5` or `BRF-M2-CR6`.
- M2 R2 resolution passed 30 state/recovery tests, 18 receipt-selected validator tests, 3 migration-selected tests, 49 full automation-validator tests, 19 query tests, all 53 metadata-validator tests, direct metadata validation, Python compilation, diff checks, and 11 repository broad-smoke checks in 408 seconds. Prepared/completed stale keys fail canonical read; recovery, cancellation, and status fail closed; all three retry families pass canonical persisted-state validation before decision evaluation.
- Code-review M2 R3 reran 30 state/recovery tests, 18 receipt-selected validator tests, 49 full automation-validator tests, 19 query tests, and all 53 metadata-validator tests. A direct nine-field mutation matrix confirmed every immutable transition input changes the key and fails validation; M2 is clean-with-notes and closed.
- M3 proof-first execution failed because `workflow_automation.py` did not exist, and the lifecycle `-k automation` selection initially contained no tests. The completed slice passes 5 target-selected tests, 4 position-selected tests, 7 capability-selected tests, all 15 engine tests, 2 lifecycle automation tests, all 149 lifecycle regressions, 30 state-writer tests, 49 automation-validator tests, Python compilation, and diff checks.
- M3 keeps the coordinator non-public until M6. Candidate authority/receipt state is validated before persistence, prepared receipts exist before stage invocation, failed invocations remain failed without consuming authority, and an existing prepared transition prevents any new capability mutation.
- Validation selection required manual routing for the two new unsupported Python paths; the plan-owned CMD10-CMD14 commands covered them directly. The selected lifecycle regression and lifecycle validation passed, and repository broad smoke passed all 11 checks in 401 seconds.
- Code-review M3 R1 reran and inspected the M3 proof after a blind-first pass, then directly reproduced completion-predicate tampering, unknown/missing canonical evidence acceptance, mismatched basis/input invocation, exhausted correction-budget derivation, and false completed synchronization. Passing CMD10-CMD14 does not close the four recorded findings.
- M3 R1 resolution passed 5 target-selected, 4 position-selected, 10 capability-selected, and all 18 engine tests; 15 policy tests; 50 automation-validator tests; 30 state-writer tests; 2 selected and all 149 lifecycle tests; all 53 metadata-validator tests; Python compilation; diff checks; and a final 12-check broad-smoke run in 230 seconds. Canonical mismatches prevent invocation, target completion is policy-owned, correction budgets are identity-bound and positive, and incomplete synchronization pauses without consuming capability authority.
- Validation selection required manual routing for the six unsupported M3 Python paths. The plan-owned focused suites covered those paths directly; all five deterministically selected lifecycle, review, metadata, and guide checks passed, and the required final repository broad smoke passed all 12 checks.
- Code-review M3 R2 reran 5 target, 4 position, 10 capability-selected, all 18 engine, and all 50 automation-validator tests, then directly derived implementation correction with an unbound budget identity and finalized completed/synchronized state without any stage-owned artifact. Passing suites do not close `BRF-M3-CR5` or `BRF-M3-CR6`.
- M3 R2 resolution passed 5 target-selected, 4 position-selected, 10 capability-selected, all 18 engine, 15 policy, 30 state-writer, 52 automation-validator, 2 selected and all 149 lifecycle, and all 53 metadata-validator tests. Missing/mismatched correction-budget identities, absent/stale/out-of-scope artifacts, failed synchronization, mutable postconditions, and evidence-free completed receipts fail closed; the final 12-check repository broad-smoke suite passed in 257 seconds.
- Validation selection required manual routing for the five unsupported M3 Python paths. The plan-owned CMD10-CMD14 commands and full engine/state/validator suites covered them directly; selected review, lifecycle, metadata, and guide checks passed.
- Code-review M3 R3 reran 10 capability-selected, all 30 state-writer, and all 52 automation-validator tests, then directly completed proposal review from arbitrary non-review bytes and reconciled/cancelled a prepared transition from a nonexistent artifact. Passing suites do not close `BRF-M3-CR7`, which records failed remediation of `BRF-M3-CR6`.
- M3 R3 resolution passed CMD10-CMD14, 14 capability-selected tests, all 33 state/recovery tests, all 52 automation-validator tests, and all 103 review-parser tests. Arbitrary bytes, unknown review outcomes, wrong reviewed-artifact identity, missing canonical review-log synchronization, nonexistent recovery evidence, and disappeared completed-receipt canonical evidence now pause without consuming capability authority; a valid parser-produced review and matching log complete once.
- Aligned-surface audit for `BRF-M3-CR7`: the approved spec, test spec, architecture, ADR, public workflow skill, adapters, and schemas are unaffected because the correction implements their existing stage-owned evidence and sole-writer contracts inside the already selected M3 modules; M4-M6 activation surfaces remain intentionally untouched.
- Validation selection required manual routing for four unsupported automation Python paths; the plan-owned CMD10-CMD14 commands covered them directly. Selected review, lifecycle, metadata, and guide checks passed, and the required repository broad-smoke suite passed all 11 checks in 436 seconds.
- Code-review M3 R4 reran 14 capability-selected, all 33 state/recovery, and all 52 automation-validator tests, then directly reconciled and cancelled from an out-of-repository symlinked canonical review log and continued a completed receipt after canonical review-log identity drift. Passing suites do not close `BRF-M3-CR8`, which records failed remediation of `BRF-M3-CR7`.
- M3 R4 resolution passed CMD10-CMD14, all 22 engine tests, 40 state/recovery tests, 52 automation-validator tests, and 103 review-parser tests. External and in-repository canonical-log symlinks now pause without consuming authority; mismatched canonical occurrences and completed canonical-log byte drift pause; valid current proof continues; and normal completion plus cancellation persist only verifier-derived review-record and review-log identities. The final required repository broad-smoke suite passed all 11 checks in 445 seconds.
- Aligned-surface audit for `BRF-M3-CR8`: the approved spec, test spec, architecture, ADR, public workflow skill, adapters, schemas, and M4-M6 surfaces are unaffected because the correction tightens the existing repository-containment, canonical-identity, and sole-writer contracts inside the M3 state adapter and its tests.
- Validation selection required manual routing for the two unsupported automation Python paths; CMD10-CMD14 and the full engine/state/validator suites covered them directly. All five deterministically selected focused checks passed, and the required repository broad smoke passed.
- Code-review M3 R5 reran 14 capability-selected, all 40 state/recovery, and all 52 automation-validator tests, then directly finalized Store A from evidence located only in unrelated Repository B. It also identified a contradiction between the active plan's canonical handoff reason and the closed R4 review state. Passing suites do not close `BRF-M3-CR9` or `BRF-M3-CR10`.

## Outcome and retrospective

- Pending implementation, milestone reviews, final holistic review, explanation, verification, and PR handoff.

## Readiness

See `Current Handoff Summary` for the authoritative live workflow state and downstream readiness.
