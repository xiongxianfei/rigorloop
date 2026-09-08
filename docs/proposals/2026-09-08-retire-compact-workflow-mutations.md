# Retire Compact Workflow Mutation and Progression

Owning change record: [change.json](../changes/2026-09-08-retire-compact-workflow-mutations/change.json).

## Challenge

RigorLoop retains semantic workflow execution mechanisms alongside the explicitly adopted recorder. Tests for those mechanisms cannot be judged unnecessary merely by age, filenames or a newer architecture. Removing their tests while keeping supported behavior reduces regression protection without simplifying the supported product.

The compact engine is a concrete first candidate: it derives workflow progression, assessment settlement and active work through `compact-current-state-v1`. The recorder has a separate dispatch and persistence boundary. However, the current [CLI Design](../design/cli/cli.md) expressly preserves compact handlers; it did not approve retirement. Current canonical and packaged activation metadata both declare compact writing active, and new-change creation consumes that setting. This is a proposed compatibility change, not removal of an already inactive engine.

## Goals

Reduce the number of supported semantic execution mechanisms by deliberately retiring one bounded writer/progression capability and its exclusively owned implementation and tests. Preserve honest historical reading, required recovery, exact contract identity, current recorder safety and independent review obligations.

Use actual callers and protected failures to determine removal. Report changes in maintained code, discovered cases, runtime and agent context separately; no savings target or measured benefit is asserted here.

## Scope and non-goals

| Initial intent | Treatment | Destination |
| --- | --- | --- |
| Reconcile duplicate test name and audit five rollout assertions | in scope; same-slice dependency | Preparatory audit below; one unused duplicate definition removed without discovery loss |
| Retire compact creation, mutation and progression | in scope; core to this proposal | Workflow/CLI-owned compatibility Design, then reviewed Delivery |
| Compact historical reading, validation, projection and interrupted-write recovery | in scope; same-slice dependency | Define retained responsibilities and any bounded continuation before disabling writers |
| Historical lifecycle mutation under other exact contracts | deferred follow-up; separate proposal | Workflow/CLI owners; do not delete its readers or writers under this proposal |
| Capability/receipt automation and calibration enforcement | deferred follow-up; separate proposal | Respective automation and Review and Closeout policy owners; establish actual support first |
| Old release procedures | deferred follow-up; separate proposal | Release-tooling owner; retain published evidence and current release safety |
| Other test-only consolidation | deferred follow-up; separate implementation slice | Test maintenance assessment comparing actual boundaries; previous mirror consolidation remains complete |
| Current record-store safety and explicit-recording-v1 compatibility retirement | out of scope | Retain current contracts and protection; rigorloop-records-v2 remains distinct from compact and historical lifecycle version labels |

The first retirement encompasses the selected compact writer's complete dependency path: creation entry points, mutation/progression evaluation, exclusive fixtures and tests, activation, projection dependencies, guidance, packaging and selectors where affected. This is a bounded impact inventory, not approval to delete every compact module. Shared parsing, transaction and safety helpers remain until their surviving callers and obligations are established.

No blanket restoration or further deletion of the 13 historical suites already removed on the preceding branch is selected. Those deletions were explicitly recorded as coverage loss, not capability retirement or replacement evidence. Any proof needed for a later retirement must be established before reliance.

No automatic conversion of historical data, reinterpretation of approvals, new record type, new retirement ledger, lifecycle gate, publication or implementation is selected. The duplicate-definition correction is a small preparatory test-only correction, not implementation of the proposed retirement.

## Governing principle

Retire a supported capability through an explicit compatibility decision, then remove only the code and tests that no surviving obligation requires.

## Proposed direction

Pursue retirement of compact creation and ordinary semantic mutation/progression, with historical reading and validation preserved under their exact contract. Explicit-recording-v1 and rigorloop-records-v2 recorder behavior and safety remain supported independently.

Before adoption, Design must map public commands, direct library callers, scripts, registered work, recovery artifacts, fixtures, selectors and installed guidance to an exact disposition: supported, read-only compatibility, explicitly unsupported, or temporarily retained for continuation/recovery. This is a decision aid in existing owning documents, not a new serialized state machine. No writer may be disabled while it is the only supported continuation or recovery path for active work.

A historical reader must explain preserved data without silently conferring current progression authority. The compact projection imports eligibility logic today; Design must distinguish historical explanation from any continued executable eligibility service. Recovery may still require narrowly bounded writes, so “read-only compatibility” must not erase an unresolved transaction's recovery path. Detailed commands, diagnostics, exit statuses, rollout and continuation mechanisms belong to Design.

Retained tests must establish declared reading, unsupported-operation rejection, no fallback or unintended mutation, identity checks and recovery at surviving boundaries before reduced-suite evidence is used. Preserve independent assessment, truthful subjects, visible findings, justified disposition and fresh final whole-change Code Review before successful Verify.

Use the existing retirement mechanism and its applicable governing policy to record protected failures, owners, fixture knowledge, contract disposition, proof, removal evidence and rollback. Reconcile its historical scope and fixed vocabulary with this initiative in Design rather than inventing a parallel ledger or silently claiming a new adoption.

## Feasibility

**Assessment: feasible for detailed Design; retirement activation is not justified by current evidence.**

Direct source inspection establishes separate recording, compact and lifecycle dispatch in the CLI. Compact operations import eligibility, projection also imports eligibility, and compact CLI combines projection, evaluation and transaction recovery. New-change creation and workflow-context are concrete consumers. These dependencies bound the work and prevent a simple evaluator-file deletion.

The active canonical [activation manifest](../../specs/compact-current-state-activation.yaml), packaged metadata and [activation tests](../../packages/rigorloop/test/compact-activation.test.js) contradict an assumption that compact writing remains withheld. The retained activation and compact CLI suites passed 10 cases, including writer rollback, projection and recovery. This supports the need to preserve those boundaries; it does not establish complete caller coverage.

The project-wide `workflow-context --format json` query returned `RL_CONTEXT_CHANGE_INVALID` for `2026-04-24-multi-agent-adapters-first-public-release`. Its empty candidate list is therefore not evidence that no active changes exist. Design must resolve authoritative continuation inventory and external support assumptions before selecting cutover; directory or Git scans must not substitute for workflow authority. This known uncertainty blocks retirement implementation, not the bounded investigation proposed here.

The [retirement library](../../scripts/retirement_ledger.py) and [governing simplification contract](../../specs/published-skill-first-repository-simplification.md) already require named protection, fixture disposition, replacement or de-contracting authority, evidence and rollback. Their adoption compatibility needs analysis; no new ledger or schema is justified now.

### Preparatory test audit

Audit basis: preceding head `e435b4a0b7f9f23456c89d857e47c9fd43697778`, after the separately approved coverage removal; the original inventory describes older head `a98b6e3523869484b47f2ef5e1422276b36bea81`.

| Candidate | Actual finding and disposition |
| --- | --- |
| Duplicate `ChangeMetadataValidatorFixtureTests.test_valid_basic_fixture_passes` | Both definitions check the same `valid-basic/change.yaml`; the later definition shadows the earlier. Remove only the unused definition. Loader still discovers the same 58 class methods; complete module passes 116 tests. No executed-case or runtime reduction claimed. |
| `test_activation_remains_withheld_in_m4` | Targeted execution fails because the asserted source string is absent. Actual activation is active. Candidate for removing a completed rollout assertion while retaining established active/withheld and recovery proof; left unchanged by this audit. |
| `test_skill_contract_first_slice_scope_stays_limited` | Passes; mixes historical slice/prose assertions with current skill existence and forbidden-skill checks. Separate those obligations before removal. |
| `test_skill_contract_plan_keeps_m1_scaffolding_passable_before_skill_edits` | Passes; reads historical plan prose, including obsolete repository-tree adapter paths. Candidate for retiring the temporal plan assertion after its owning historical obligation is dispositioned; no production runtime is exercised. |
| `test_skill_contract_m3_first_slice_core_sections_and_result_blocks` | Passes; inspects live skill sections, result fields and handoffs. Preserve enduring structure protection; a milestone name alone is not a removal basis. |
| `test_output_contract_json_support_is_not_added_in_first_slice` | Passes; invokes the current runner with unsupported `--json` and checks rejection. Preserve current interface rejection; the name does not establish a permanent prohibition on future JSON support. |

The stale activation assertion is a demonstrated existing test failure. The other dispositions are bounded inspection results, not approval to retire their capabilities. Detailed commands and discovery evidence belong to this change's evidence record.

## Impact and major trade-offs

A smaller supported execution surface may reduce maintenance, but retiring an active writer can strand work and creates a real compatibility cost. Read-only explanation and narrowly retained recovery may limit the amount of code removed. Those costs are preferable to silently converting historical contracts or deleting their only recovery path.

The proposal is deliberately narrower than the overall shortlist. Automation, calibration and release procedures require different owner decisions and should not become hidden prerequisites or automatic follow-on deletions.

## Decision requested

Approve detailed Design of retirement for compact creation and semantic mutation/progression, subject to explicit historical reading, validation, continuation and recovery dispositions. Approve coordinated consumer and test removal only as a downstream Design/Delivery objective after retained protection is established.

This decision does not retire the engine now, resolve unknown customer obligations, authorize exact handler deletion, migrate records, retire current recorder v1 compatibility, or approve implementation, activation, publication or release. Other legacy engines and tooling remain separate proposals.
