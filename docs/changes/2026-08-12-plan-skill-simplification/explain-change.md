# Plan Skill Simplification Change Rationale

## Summary

This change makes portable planning substantially shorter while preserving a complete governed planning path. Universal plan quality and safety remain in `SKILL.md`; governed plan creation, revision, reviewed initialization, retry, and compatibility move to one exact conditional reference; milestone output becomes stable intent; and `change.yaml` remains the only live milestone-state owner.

## Problem

The previous `plan` skill loaded RigorLoop-specific lifecycle mutation for ordinary customer-project planning, repeated output structure already owned by assets, and emitted mutable milestone state inside plan bodies. The lifecycle also initialized live work before plan review, which conflicted with review-driven revisions and immutable later workflow state.

## Decision trail

The accepted proposal selected one governed reference rather than editorial compression, asset-only changes, fragmented references, or a new runtime. PSIM-R001-R035 define package ownership, exact governed operations, reviewed initialization, state authority, compatibility, measurement, and parity. The architecture update and ADR-20260813 establish evidence-first review, plan-owned initialization, stable identity without content hashes, and workflow-owned later transitions. M1 implemented the lifecycle transaction and readers, M2 simplified the package and assets, and M3 proved profile reduction, semantic preservation, and package parity.

## Diff rationale by area

| Area and files | Change | Reason | Contract and evidence |
| --- | --- | --- | --- |
| `skills/plan/SKILL.md` | Replaced inline governed mechanics and repeated output prose with a shorter portable contract and exact resource triggers. | Keep ordinary planning self-sufficient without loading conditional lifecycle procedure. | PSIM-R001-R005; T8-T9; `evidence/m2-plan-package.md` |
| `skills/plan/references/governed-plan-authoring.md` | Added create, revise, reviewed initialization, retry, historical compatibility, and write-boundary procedure. | Give governed behavior one owner while retaining exact artifact and review identity fields. | PSIM-R006-R020; PLSIM-CR1; `reviews/code-review-m2-r2.md` |
| `skills/plan/assets/milestone.md` | Replaced mutable state/progress fields with kind, architecture, completion, evidence, handoff, and optional commit intent. | Plans own stable execution intent; `change.yaml` owns live state. | PSIM-R021-R029; T6, T9 |
| `skills/plan-review/SKILL.md`, `skills/workflow/SKILL.md` | Made clean judgment precede one-time initialization and made workflow coordinate the identical settlement retry. | Prevent draft milestones from becoming live state before review while preserving stage ownership. | ADR-20260813; PSIM-R013-R020; T2-T5 |
| `scripts/change_metadata_semantics.py`, `scripts/workflow_automation_state.py`, `scripts/lifecycle_state_sync.py`, `scripts/query-change-record.py` | Admitted the legal review-before-initialization states, validated the review basis, removed plan-prose projection authority, and exposed bounded live state. | Implement the approved two-phase transaction and read-old/write-new boundary. | M1; PSIM-R013-R028; `evidence/m1-reviewed-plan-transaction.md` |
| Lifecycle and workflow specs, tests, `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` | Aligned normative ordering, ownership, temporary states, retry, and migration guidance. | Avoid conflicting higher-authority lifecycle instructions. | PSIM-R034-R035; architecture review R1 |
| Validator and workflow test files | Added valid, invalid, stale, retry, ownership, historical, profile, asset, and ledger regression coverage. | Prove the contract without executing a target agent. | T1-T10; CMD1-CMD9; PLSIM-CR2 |
| Change-local ledgers, fixtures, measurements, package evidence, and review records | Recorded every semantic/literal disposition, negative fixture, profile/resource identity, adapter result, and review outcome. | Make simplification and preservation auditable without permanent size policy. | PSIM-R029-R033; T7-T13 |
| Selector routing evidence | Recorded eight exact owner-approved deferrals for one-change ledgers and fixtures. | Keep registration debt visible and retain direct proof without creating permanent simplicity routing. | Existing owner-deferral contract; T7-T9, CMD7, MP1 |

## Tests added or changed

T1-T6 and T10 exercise create/revise classification, initialization basis, clean-review ordering, retry, current-state authority, historical compatibility, and governing alignment through metadata, lifecycle, workflow, automation-state, and query tests. T7 adds change-local ledger validation with closed vocabulary checked before consistency and rejects duplicate IDs, missing fields, and inconsistent destinations. T8-T9 cover exact resource profiles, missing-resource safety, three-asset structure, and absence of mutable plan state. T11-T13 cover deterministic measurements, adapter archive and clean-install parity, and independent semantic review.

These are deterministic contract, unit, integration, and package tests because the behavior is authored policy, metadata semantics, and resource parity. A target-agent journey would add nondeterminism without proving those contracts more directly.

## Validation evidence available before final verify

CMD1-CMD5 passed during M1: 63 change-metadata, 170 artifact-lifecycle, 76 workflow-automation, 65 automation-state, and 26 query tests. CMD6-CMD9 pass after M2 correction: one canonical skill, 317 skill-contract tests with 16 skips, 7 build tests, and generated-skill drift check. CMD10-CMD12 pass: adapter distribution, temporary Codex/Claude/opencode archive and clean-install validation, and boundary validation. CMD13-CMD14 pass at every handoff. Hosted CI status is not yet known, and final verify has not yet made a branch-readiness judgment.

## Review resolution summary

Nine proposal findings and two M2 code-review findings were accepted and closed. PLSIM-CR1 restored exact identity fields after over-compression. PLSIM-CR2 completed the deterministic invalid-ledger proof. The strictly later M2 rereview and final holistic review are clean, and `review-log.md` has no open findings. See [review-resolution.md](review-resolution.md).

## Alternatives rejected

Editorial compression alone would keep conditional lifecycle procedure in every invocation. Asset-only changes would not reduce common-path policy. Multiple small references would fragment one governed operation boundary. A routing engine, tokenizer gate, runtime journey suite, or permanent simplicity validator would add machinery unrelated to the content and state-ownership problem. Pre-review initialization was rejected because plan-review may legitimately change milestone definitions.

## Scope control

The change does not add a runtime, selector, scheduler, state store, schema field for content hashes, target-agent acceptance, release publication, or PR behavior. It does not rewrite historical plans, infer missing live state from prose, or change the existing boundary-first reference.

## Risks and follow-ups

The governed profile reduction is intentionally modest because deterministic identity and failure procedure remain explicit. Active legacy plans with incomplete `planned_work` still require explicit workflow-owned migration rather than automatic repair. The first final PR-mode selector correctly stopped on eight unsupported one-change evidence paths. Exact repository-maintainer deferrals preserve T7-T9, CMD7, and MP1, change no selector or check catalog, and require a focused rereview plus selector rerun. Final repository verification and hosted CI remain downstream gates; this explanation does not claim branch readiness or PR readiness.
