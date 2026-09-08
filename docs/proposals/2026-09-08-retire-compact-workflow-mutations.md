# Retire Legacy Record Formats and Workflow Engines

Owning change record: [change.json](../changes/2026-09-08-retire-compact-workflow-mutations/change.json).

## Challenge

The project owner confirms that work depending on the named legacy mechanisms is complete and that the v2 mechanism is operational. RigorLoop still contains the superseded record-format support and workflow execution machinery. This initiative completes their removal while preserving the functioning v2 system; it does not reopen whether completed legacy work needs continuation. The completion baseline is owner-provided confirmation, not an independently executed repository check.

The user-selected destination is rigorloop-records-v2 as the only supported runtime record format, retiring explicit-recording-v1 and the old compact/lifecycle formats with their exclusive execution mechanisms. The compact engine illustrates the existing coupling: it derives workflow progression, assessment settlement and active work through `compact-current-state-v1`. The recorder has a separate dispatch and persistence boundary. The current [CLI Design](../design/cli/cli.md) still preserves compact handlers, and canonical and packaged activation metadata still enable compact writing. These are coordinated removal targets under the selected retirement direction. Completed legacy work does not mean those technical surfaces have already disappeared; disabling a flag alone would not complete their removal.

## Goals

Converge runtime record support on rigorloop-records-v2. Retire the old record readers, validators, creators, writers and progression mechanisms with their exclusively owned implementation and tests under the confirmed completed-work baseline. Preserve historical evidence without reinterpreting its meaning, exact contract identity, v2 recorder safety and independent review obligations.

Use actual callers and protected failures to determine removal. Report changes in maintained code, discovered cases, runtime and agent context separately; no savings target or measured benefit is asserted here.

## Scope and non-goals

| Initial intent | Treatment | Destination |
| --- | --- | --- |
| Reconcile duplicate test name and audit five rollout assertions | in scope; same-slice dependency | Preparatory audit below; one unused duplicate definition removed without discovery loss |
| Retire explicit-recording-v1 and compact/lifecycle formats and their exclusive engines | in scope; core to this proposal | Record Format, Workflow and CLI compatibility Design, then reviewed Delivery slices |
| Historical evidence and current-work discovery | in scope; same-slice dependency | Preserve archival bytes and identities; keep archives out of current v2 discovery without concealing malformed v2 stores |
| Historical lifecycle readers, validators, mutation and progression | in scope; separate implementation slice | Exact contract inventory and supported cutover before removing exclusive machinery |
| Capability/receipt automation and calibration enforcement | deferred follow-up; separate proposal | Respective automation and Review and Closeout policy owners; establish actual support first |
| Old release procedures | deferred follow-up; separate proposal | Release-tooling owner; retain published evidence and current release safety |
| Other test-only consolidation | deferred follow-up; separate implementation slice | Test maintenance assessment comparing actual boundaries; previous mirror consolidation remains complete |
| Current rigorloop-records-v2 safety and recovery | in scope; same-slice dependency | Preserve protection at the surviving recorder boundary; do not discard shared safety tests with retired-format cases |

The exact retirement set is `explicit-recording-v1`, `compact-current-state-v1`, `stage-owned-change-local-v1`, `stage-owned-change-local-v2`, `stage-owned-change-local-v3`, and `legacy-unversioned`. Design must inventory their subordinate record shapes and registered variants rather than infer contracts from directory names or schema numbers. The destination is unsupported runtime input with safe rejection, not permanent read-only compatibility for these formats.

The coordinated initiative covers creation, reading, validation, projection, writing, progression, schemas, exclusive fixtures and tests, activation, guidance, packaging and selectors where affected. Delivery must split this broad direction into independently reviewable retirement slices with explicit dependencies. Shared parsing, transaction and safety helpers remain wherever v2 still relies on them.

The `Model validation contract: explicit-recording-v1` document marker and `targeted-recording-v1` request transport are separate version domains, not old stored records. Do not remove them by name matching. Design must resolve any confusing marker or shared-schema coupling without silently changing transport or historical document meaning.

No blanket restoration or further deletion of the 13 historical suites already removed on the preceding branch is selected. Those deletions were explicitly recorded as coverage loss, not capability retirement or replacement evidence. Any proof needed for a later retirement must be established before reliance.

No migration, export mechanism, temporary legacy continuation, permanent historical reader, archival service, archive schema, historical evidence deletion, reinterpretation of approvals, new record type, new retirement ledger or lifecycle gate is planned. The stated operating situation requires none of those facilities. Exact implementation and publication remain downstream approvals. The duplicate-definition correction is a small preparatory test-only correction, not implementation of the proposed retirement.

## Governing principle

Retire a supported capability through an explicit compatibility decision, then remove only the code and tests that no surviving obligation requires.

## Proposed direction

Pursue rigorloop-records-v2-only runtime record support. Retire the named old formats across normal and advanced entry points, including old-format creation, reading, validation, mutation and semantic progression. Preserve v2 inspection, correction recording, atomic persistence, identity/conflict checks, safe paths, retry and recovery. Historical source artifacts and recorded identities may remain as archival evidence; their preservation must not imply continued execution support or current approval.

Design must map public commands, direct library callers, scripts, schemas, fixtures, selectors and installed guidance to removal, disconnection or retained v2 ownership. The purpose is to leave no broken imports, obsolete dispatch or hidden dependency on legacy behavior. Concrete contradictory residue encountered in selected removal paths, such as an unfinished transaction, requires a specific owner disposition before the affected removal proceeds. That bounded handling rule does not require designing legacy recovery or continuation facilities in advance.

Preserve historical records and recorded identities as archival evidence without changing their meaning. Explicit retired-format input to the current CLI must reject safely without fallback, mutation or reinterpretation as v2. Normal current-work discovery and validation must not promote unrelated archival legacy records into current candidates or let them obstruct valid v2 work. Conversely, malformed current v2 stores must still be diagnosed rather than silently dismissed as archives. Design owns the exact distinction and diagnostics; no archive schema or service is selected.

Current skills and packaged guidance must describe the v2-only operating contract and state the compatibility break without advertising removed paths. V1 data lacks v2 retained-origin guarantees; preservation of old evidence must not fabricate missing origin or relabel historical judgments as newly approved. Detailed interfaces, removal sequencing and proof allocation belong to Design and Delivery.

Retained tests must establish v2 behavior, safe rejection of retired-format input without fallback or unintended mutation, archival separation, and identity/recovery guarantees at surviving boundaries. Dedicated positive tests and fixtures for retired-format creation, reading, mutation and progression leave with their capabilities; v2 need not reproduce retired legacy behavior. Preserve or adapt tests for helpers still used by v2. Completed rollout expectations may be removed after separating any enduring protection. Preserve independent assessment, truthful subjects, visible findings, justified disposition and fresh final whole-change Code Review before successful Verify.

Use the existing retirement mechanism and its applicable governing policy to record protected failures, owners, fixture knowledge, contract disposition, proof, removal evidence and rollback. Reconcile its historical scope and fixed vocabulary with this initiative in Design rather than inventing a parallel ledger or silently claiming a new adoption.

## Feasibility

**Assessment: feasible as a bounded retirement of completed legacy support.**

The project owner confirms that legacy work is complete and v2 is operational. Remaining Design work concerns exact removal boundaries, shared dependencies, v2-only input handling, archival separation and coordinated consumer changes. No migration or temporary legacy continuation mechanism is selected. Delivery must demonstrate that removal preserves v2 behavior and safely rejects retired-format input; owner confirmation is not execution evidence for the future removal.

Direct source inspection establishes separate recording, compact and lifecycle dispatch in the CLI. Compact operations import eligibility, projection also imports eligibility, and compact CLI combines projection, evaluation and transaction recovery. New-change creation and workflow-context are concrete consumers. These dependencies bound the work and prevent a simple evaluator-file deletion.

The active canonical [activation manifest](../../specs/compact-current-state-activation.yaml), packaged metadata and [activation tests](../../packages/rigorloop/test/compact-activation.test.js) contradict an assumption that compact writing remains withheld. The retained activation and compact CLI suites passed 10 cases, including writer rollback, projection and recovery. These earlier results describe existing machinery and guide dependency analysis; they do not require continued legacy acceptance or establish proof for its removal.

The project-wide `workflow-context --format json` query returned `RL_CONTEXT_CHANGE_INVALID` for `2026-04-24-multi-agent-adapters-first-public-release`. That remains an earlier failed observation; its empty candidate list is not evidence of completed work. The subsequent owner confirmation supplies the current completion baseline. Repairing or successfully executing the legacy query is not a prerequisite for retirement. Removal-focused analysis must still surface concrete contradictory residue if encountered; it must not turn hypothetical legacy work into an open-ended investigation.

The Record Format and CLI Designs currently retain explicit-recording-v1 reads, updates and advanced creation. Those compatibility clauses require explicit revision alongside Workflow; the previously reviewed compact-only proposal is insufficient authority for this expanded scope. Shared v1/v2 schemas, validators, constructors and recovery paths must be mapped before deletion. No new stored schema version is required by selecting existing v2 alone.

The [retirement library](../../scripts/retirement_ledger.py) and [governing simplification contract](../../specs/published-skill-first-repository-simplification.md) already require named protection, fixture disposition, replacement or de-contracting authority, evidence and rollback. Their adoption compatibility needs analysis; no new ledger or schema is justified now.

### Preparatory test audit

Audit basis: preceding head `e435b4a0b7f9f23456c89d857e47c9fd43697778`, after the separately approved coverage removal; the original inventory describes older head `a98b6e3523869484b47f2ef5e1422276b36bea81`.

| Candidate | Actual finding and disposition |
| --- | --- |
| Duplicate `ChangeMetadataValidatorFixtureTests.test_valid_basic_fixture_passes` | Both definitions check the same `valid-basic/change.yaml`; the later definition shadows the earlier. Remove only the unused definition. Loader still discovers the same 58 class methods; complete module passes 116 tests. No executed-case or runtime reduction claimed. |
| `test_activation_remains_withheld_in_m4` | Targeted execution fails because the asserted source string is absent. Actual activation is active. Candidate for removing a completed rollout assertion with the retired capability; retain only protection needed at surviving v2 boundaries. Left unchanged by the preparatory audit. |
| `test_skill_contract_first_slice_scope_stays_limited` | Passes; mixes historical slice/prose assertions with current skill existence and forbidden-skill checks. Separate those obligations before removal. |
| `test_skill_contract_plan_keeps_m1_scaffolding_passable_before_skill_edits` | Passes; reads historical plan prose, including obsolete repository-tree adapter paths. Candidate for retiring the temporal plan assertion after its owning historical obligation is dispositioned; no production runtime is exercised. |
| `test_skill_contract_m3_first_slice_core_sections_and_result_blocks` | Passes; inspects live skill sections, result fields and handoffs. Preserve enduring structure protection; a milestone name alone is not a removal basis. |
| `test_output_contract_json_support_is_not_added_in_first_slice` | Passes; invokes the current runner with unsupported `--json` and checks rejection. Preserve current interface rejection; the name does not establish a permanent prohibition on future JSON support. |

The stale activation assertion is a demonstrated existing test failure. The other dispositions are bounded inspection results, not approval to retire their capabilities. Detailed commands and discovery evidence belong to this change's evidence record.

## Impact and major trade-offs

A v2-only runtime may reduce maintenance, but removing enabled writers and old-format readers is a real compatibility break. The owner-confirmed completed-work baseline supports proceeding with removal rather than planning coexistence. Guidance must state that old-format runtime input is unsupported. Historical evidence remains untouched, and any concrete contradictory residue discovered during implementation receives a bounded disposition.

This scope expands the earlier compact-only proposal at the user’s explicit request. Record Format now joins Workflow and CLI in the minimum Design package. Automation, calibration and old release procedures remain separate decisions; any concrete dependency that prevents format retirement must be surfaced with its owner and disposition rather than silently removed or hidden as a prerequisite.

## Decision requested

Approve retirement of the named legacy stored-record formats and their exclusive runtime mechanisms, leaving `rigorloop-records-v2` as the only supported runtime record format.

Remove affected readers, validators, creators, writers, projections, progression handlers, exclusive schemas, fixtures, tests, activation entries and consumer references through coordinated Design and Delivery. Preserve historical evidence, required v2 safety, shared dependencies and independent review obligations. No migration, temporary continuation facility or permanent legacy reader is planned. Unrelated archival legacy records must not obstruct current v2 work, and malformed v2 input must not be silently ignored.

Approval selects retirement on the owner-confirmed completion baseline and authorizes focused Design in Record Format, CLI and Workflow. It replaces the earlier continuation uncertainty and compatibility-preservation premises. Exact implementation changes and publication remain subject to their normal reviewed scope; no historical records are deleted or rewritten by this decision.
