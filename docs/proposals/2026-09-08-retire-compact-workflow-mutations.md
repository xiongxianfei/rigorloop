# Retire Legacy Record Formats and Workflow Engines

Owning change record: [change.json](../changes/2026-09-08-retire-compact-workflow-mutations/change.json).

## Challenge

RigorLoop retains semantic workflow execution mechanisms alongside the explicitly adopted recorder. Tests for those mechanisms cannot be judged unnecessary merely by age, filenames or a newer architecture. Removing their tests while keeping supported behavior reduces regression protection without simplifying the supported product.

The user-selected destination is rigorloop-records-v2 as the only supported runtime record format, retiring explicit-recording-v1 and the old compact/lifecycle formats with their exclusive execution mechanisms. The compact engine illustrates the existing coupling: it derives workflow progression, assessment settlement and active work through `compact-current-state-v1`. The recorder has a separate dispatch and persistence boundary. However, the current [CLI Design](../design/cli/cli.md) expressly preserves compact handlers; it did not approve retirement. Current canonical and packaged activation metadata both declare compact writing active, and new-change creation consumes that setting. This is a proposed compatibility change, not removal of an already inactive engine.

## Goals

Converge runtime record support on rigorloop-records-v2. Retire the old record readers, validators, creators, writers and progression mechanisms with their exclusively owned implementation and tests after existing-work and recovery obligations are dispositioned. Preserve historical evidence without reinterpreting its meaning, exact contract identity, v2 recorder safety and independent review obligations.

Use actual callers and protected failures to determine removal. Report changes in maintained code, discovered cases, runtime and agent context separately; no savings target or measured benefit is asserted here.

## Scope and non-goals

| Initial intent | Treatment | Destination |
| --- | --- | --- |
| Reconcile duplicate test name and audit five rollout assertions | in scope; same-slice dependency | Preparatory audit below; one unused duplicate definition removed without discovery loss |
| Retire explicit-recording-v1 and compact/lifecycle formats and their exclusive engines | in scope; core to this proposal | Record Format, Workflow and CLI compatibility Design, then reviewed Delivery slices |
| Existing records, historical evidence, active-work continuation and interrupted-write recovery | in scope; same-slice dependency | Define archival treatment and temporary transition/recovery obligations with explicit removal conditions |
| Historical lifecycle readers, validators, mutation and progression | in scope; separate implementation slice | Exact contract inventory and supported cutover before removing exclusive machinery |
| Capability/receipt automation and calibration enforcement | deferred follow-up; separate proposal | Respective automation and Review and Closeout policy owners; establish actual support first |
| Old release procedures | deferred follow-up; separate proposal | Release-tooling owner; retain published evidence and current release safety |
| Other test-only consolidation | deferred follow-up; separate implementation slice | Test maintenance assessment comparing actual boundaries; previous mirror consolidation remains complete |
| Current rigorloop-records-v2 safety and recovery | in scope; same-slice dependency | Preserve protection at the surviving recorder boundary; do not discard shared safety tests with retired-format cases |

The exact retirement set is `explicit-recording-v1`, `compact-current-state-v1`, `stage-owned-change-local-v1`, `stage-owned-change-local-v2`, `stage-owned-change-local-v3`, and `legacy-unversioned`. Design must inventory their subordinate record shapes and registered variants rather than infer contracts from directory names or schema numbers. The destination is unsupported runtime input with safe rejection, not permanent read-only compatibility for these formats.

The coordinated initiative covers creation, reading, validation, projection, writing, progression, schemas, exclusive fixtures and tests, activation, guidance, packaging and selectors where affected. Delivery must split this broad direction into independently reviewable retirement slices with explicit dependencies. Shared parsing, transaction and safety helpers remain wherever v2 or approved temporary transition tooling still relies on them.

The `Model validation contract: explicit-recording-v1` document marker and `targeted-recording-v1` request transport are separate version domains, not old stored records. Do not remove them by name matching. Design must resolve any confusing marker or shared-schema coupling without silently changing transport or historical document meaning.

No blanket restoration or further deletion of the 13 historical suites already removed on the preceding branch is selected. Those deletions were explicitly recorded as coverage loss, not capability retirement or replacement evidence. Any proof needed for a later retirement must be established before reliance.

No historical evidence deletion, automatic conversion, reinterpretation of approvals, new record type, new retirement ledger, lifecycle gate, publication or implementation is selected. Any conversion or export needed for transition requires its own explicit Design mapping and later execution authority; this proposal does not select a migration mechanism. The duplicate-definition correction is a small preparatory test-only correction, not implementation of the proposed retirement.

## Governing principle

Retire a supported capability through an explicit compatibility decision, then remove only the code and tests that no surviving obligation requires.

## Proposed direction

Pursue rigorloop-records-v2-only runtime record support. Retire the named old formats across normal and advanced entry points, including old-format creation, reading, validation, mutation and semantic progression. Preserve v2 inspection, correction recording, atomic persistence, identity/conflict checks, safe paths, retry and recovery. Historical source artifacts and recorded identities may remain as archival evidence; their preservation must not imply continued execution support or current approval.

Before adoption, Design must map public commands, direct library callers, scripts, registered work, recovery artifacts, fixtures, selectors and installed guidance to an exact transition disposition: retained v2 support, archival evidence, explicitly unsupported, or temporarily retained for continuation/recovery with an owner and removal condition. This is a decision aid in existing owning documents, not a new serialized state machine. No writer may be disabled while it is the only supported continuation or recovery path for active work.

Any temporary historical reader must explain preserved data without conferring current progression authority and must have a defined exit condition. The compact projection imports eligibility logic today, so even reader removal requires dependency analysis. Recovery may require narrowly bounded old-format writes until existing transactions are safely resolved. Design must make that temporary boundary explicit; the final destination remains retirement rather than indefinite compatibility. Detailed commands, diagnostics, exit statuses, archival access, rollout and continuation mechanisms belong to Design. V1 data lacks v2 retained-origin guarantees; a transition must not fabricate missing origin or relabel historical judgments as newly approved.

Retained tests must establish v2 behavior, safe rejection of retired-format input without fallback or unintended mutation, and identity/recovery guarantees at surviving boundaries before reduced-suite evidence is used. Any temporary compatibility tool needs its own bounded proof. Dedicated old-format acceptance tests leave only with the supported capability they protect. Preserve independent assessment, truthful subjects, visible findings, justified disposition and fresh final whole-change Code Review before successful Verify.

Use the existing retirement mechanism and its applicable governing policy to record protected failures, owners, fixture knowledge, contract disposition, proof, removal evidence and rollback. Reconcile its historical scope and fixed vocabulary with this initiative in Design rather than inventing a parallel ledger or silently claiming a new adoption.

## Feasibility

**Assessment: feasible for detailed Design; retirement activation is not justified by current evidence.**

Direct source inspection establishes separate recording, compact and lifecycle dispatch in the CLI. Compact operations import eligibility, projection also imports eligibility, and compact CLI combines projection, evaluation and transaction recovery. New-change creation and workflow-context are concrete consumers. These dependencies bound the work and prevent a simple evaluator-file deletion.

The active canonical [activation manifest](../../specs/compact-current-state-activation.yaml), packaged metadata and [activation tests](../../packages/rigorloop/test/compact-activation.test.js) contradict an assumption that compact writing remains withheld. The retained activation and compact CLI suites passed 10 cases, including writer rollback, projection and recovery. This supports the need to preserve those boundaries; it does not establish complete caller coverage.

The project-wide `workflow-context --format json` query returned `RL_CONTEXT_CHANGE_INVALID` for `2026-04-24-multi-agent-adapters-first-public-release`. Its empty candidate list is therefore not evidence that no active changes exist. Design must resolve authoritative continuation inventory and external support assumptions before selecting cutover; directory or Git scans must not substitute for workflow authority. This known uncertainty blocks retirement implementation, not the bounded investigation proposed here.

The Record Format and CLI Designs currently retain explicit-recording-v1 reads, updates and advanced creation. Those compatibility clauses require explicit revision alongside Workflow; the previously reviewed compact-only proposal is insufficient authority for this expanded scope. Shared v1/v2 schemas, validators, constructors and recovery paths must be mapped before deletion. No new stored schema version is required by selecting existing v2 alone.

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

A v2-only runtime may reduce maintenance, but retiring active writers and old-format readers creates a real compatibility break. Users may need to finish work, export information or retain a separately identified historical tool before cutover. Design must select those dispositions without indefinite hidden compatibility or stranded recovery. Archival evidence alone is not an operational continuation path.

This scope expands the earlier compact-only proposal at the user’s explicit request. Record Format now joins Workflow and CLI in the minimum Design package. Automation, calibration and old release procedures remain separate decisions; any concrete dependency that prevents format retirement must be surfaced with its owner and disposition rather than silently removed or hidden as a prerequisite.

## Decision requested

Approve detailed Design of rigorloop-records-v2-only runtime record support, retiring explicit-recording-v1 and the named compact/lifecycle formats across readers, validators, creation, mutation and exclusive progression machinery. Require exact existing-record, active-work, archival and recovery dispositions, bounded temporary support where necessary, and coordinated consumer/test retirement with retained v2 safety proof.

Approval selects this broader direction and supersedes the earlier proposal's permanent old-format compatibility and compact-only scope. It does not retire any format now, settle unknown customer obligations, authorize exact handler or historical-record deletion, migrate records, or approve implementation, activation, publication or release. Support remains under existing contracts until the reviewed transition is adopted.
