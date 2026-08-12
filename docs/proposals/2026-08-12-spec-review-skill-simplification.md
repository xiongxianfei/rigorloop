# Spec-Review Skill Simplification

## Owning change record

`docs/changes/2026-08-12-spec-review-skill-simplification/change.yaml`

## Problem

The published `spec-review` skill is rigorous but its 284-line, 2,174-word common path mixes ordinary contract judgment with detailed formal settlement, workflow-managed review evidence, and a long boundary-first method that is also available through packaged references. A direct review pays this context cost even when it only needs to judge requirement clarity, completeness, testability, examples, compatibility, observability, security, non-goals, acceptance criteria, routing, and readiness.

Several rules also have overlapping textual owners. Artifact placement and settlement are spread across placement, change-record, recording, rules, and handoff sections. The inline boundary-first method repeats substantial concepts from two mapped references. Output fields appear in both skill prose and assets. This increases scan cost and synchronization risk without improving the review standard.

The optimization must respect existing contracts that require review dimensions, review guidance, verdicts, severity, material-finding sufficiency, recording obligations, validation obligations, lifecycle boundaries, and a compact boundary scan to remain inline. The problem is therefore not solved by hiding universal policy in references; it is solved by keeping the obligations compact and moving only genuinely conditional operational detail.

## Goals

- Make ordinary direct spec review materially shorter and easier to scan without weakening contract judgment or downstream safety.
- Keep `SKILL.md` self-sufficient for review classification, evidence, review dimensions, material findings, statuses, routing, readiness, isolation, universal recording obligations, lifecycle boundaries, stops, claims, and resource selection.
- Give detailed durable recording and exact formal settlement one conditional owner.
- Preserve the checked inline boundary scan while relying on existing boundary references for full boundary vocabulary and feature-record procedure.
- Keep the two existing assets as the only structural output owners.
- Account separately for common-path reduction, conditional loaded profiles, and total package change.
- Prove semantic preservation and literal compatibility without executing a target-agent runtime or adding permanent simplicity machinery.

## Non-goals

- Do not change spec-review quality, review statuses, severity meaning, material-finding shape, routing values, eventual test-spec readiness, recording obligations, artifact settlement, automation authority, or workflow continuation.
- Do not remove or rename the existing boundary-first references, identifiers, activation model, or inline compact-scan requirement.
- Do not optimize `spec`, `test-spec`, or another review skill in this change.
- Do not create a generic review engine, shared policy owner, runtime router, scheduler, state store, or new lifecycle schema.
- Do not add another asset or split each review dimension into a reference.
- Do not add target-agent journeys, transcript grading, model selection, permanent token budgets, or prose-quality gates.

## Vision fit

fits the current vision

The change makes a critical review gate easier to inspect and use while preserving explicit decisions, durable evidence, resumability, and human-reviewable lifecycle state.

## Context

The current package contains one main file, two projected boundary references, and two structural assets:

| Resource | Lines | Words | UTF-8 bytes | Current role |
| --- | ---: | ---: | ---: | --- |
| `SKILL.md` | 284 | 2,174 | 16,304 | Universal judgment plus conditional procedure |
| `boundary-first-method-v1.md` | 110 | 857 | 6,346 | Shared detailed boundary vocabulary and method |
| `boundary-first-feature-authoring-v1.md` | 66 | 350 | 2,324 | Feature boundary-record structure and semantic review |
| Two assets | 42 | 209 | 1,548 | Result and finding layout |
| Complete package | 502 | 3,590 | 26,522 | Maintenance and distribution footprint |

The existing architecture already defines published skills as canonical `SKILL.md` plus mapped references and assets. The two boundary references are projected from governed canonical resources and must retain their paths and raw-byte parity. This proposal adds one skill-owned conditional procedure reference; it does not give that reference independent lifecycle authority.

Two older clauses need focused clarification during specification. `SFA-R6` requires recording obligations and lifecycle boundaries inline; this proposal preserves those obligations and boundaries inline while distinguishing them from detailed operational mechanics. The checked boundary activation architecture requires an inline compact scan; this proposal keeps that scan and removes only duplicate detailed guidance.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Identify the best way to optimize `spec-review`. | in scope | Options Considered and Recommended Direction |
| Create a new branch. | in scope | Change-local authoring evidence |
| Create a proposal. | in scope | This artifact |
| Run proposal review. | in scope | Next Artifacts and formal review evidence |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Simplify the universal spec-review common path. | core to this proposal | Primary user-visible objective |
| Add one recording-and-settlement reference. | core to this proposal | Separates conditional durable mechanics from universal obligations |
| Preserve and remap existing boundary references precisely. | same-slice dependency | Boundary activation and package parity are compatibility surfaces |
| Keep existing result and finding assets structural. | same-slice dependency | Avoids duplicate output layouts and policy leakage |
| Amend directly coupled skill-contract clauses. | same-slice dependency | Older inline-only wording must distinguish obligations from mechanics |
| Add deterministic preservation and package proof. | same-slice dependency | Required for safe published-package change |
| Record a bounded architecture assessment. | same-slice dependency | Confirms whether the existing package model remains sufficient |
| Optimize adjacent skills. | out of scope | Each requires its own evidence and ownership decision |
| Add runtime evaluation or permanent simplicity validation. | out of scope | Disproportionate and nondeterministic for this refactor |

## Options Considered

### Option 0: Keep the package unchanged

This has no migration risk but preserves unnecessary common-path loading and duplicate ownership.

### Option 1: Editorial compression only

This can remove repetition without changing package shape. It cannot keep formal settlement detail out of ordinary reviews and is unlikely to produce a material common-path reduction.

### Option 2: Move only the inline boundary-first section

This removes duplication already represented by mapped resources, but formal placement, settlement, and workflow-managed review mechanics still load for every direct review.

### Option 3: Add one recording reference and tighten existing boundary disclosure

This keeps universal review policy inline, moves conditional durable mechanics into one reference, retains the compact scan, and loads the two existing boundary references only for their governed contexts. It creates one new navigation target while giving each conditional procedure a coherent owner.

### Option 4: Add separate recording, automation, requirement-fidelity, and boundary references

This maximizes segmentation but creates too many predicates and cross-reference interactions. Current automation is manifest-only and formal-authority-bound, while manual requirement fidelity is a small opt-in; neither justifies another resource in the first version.

### Option 5: Replace review prose with a shared review engine

This could centralize mechanics but would introduce cross-skill policy ownership and runtime complexity, obscure stage-specific judgment, and exceed the scope of content simplification.

## Recommended Direction

Adopt Option 3.

The target package is:

```text
skills/spec-review/
├── SKILL.md
├── references/
│   ├── spec-review-recording-and-settlement.md
│   ├── boundary-first-method-v1.md
│   └── boundary-first-feature-authoring-v1.md
└── assets/
    ├── review-result-skeleton.md
    └── material-finding.md
```

### Closed invocation predicates

Classify these predicates from current evidence before dependent side effects:

| Predicate | True when | False when |
| --- | --- | --- |
| `durable_recording_context` | The invocation is formal lifecycle review, explicitly requests durable recording, produces a material finding, or returns `changes-requested`, `blocked`, or `inconclusive`. | A clean isolated advisory review has no durable request or governing recording trigger. |
| `formal_lifecycle_context` | A current governed change resolves exactly one `spec` entry for this artifact in a reviewable state and grants spec-review settlement authority. | A direct request, an advisory recording root, ambiguous identity, or conversational wording alone. |
| `workflow_automated_context` | Current durable workflow authorization selects automated `spec-review` for the same governed change and spec entry. | Manual review, stale or mismatched authorization, or prompt wording alone. |
| `boundary_first_context` | The reviewed behavior contract is governed by active `boundary-first-v1`, or current checked-revision adoption makes the boundary contract applicable. | Non-behavioral or grandfathered non-substantive review with no active boundary contract. |
| `formal_boundary_record_context` | Review must judge the formal boundary record or a substantive grandfathered revision. | The compact scan suffices and no formal record completeness decision is required. |

`workflow_automated_context` implies `formal_lifecycle_context`. `formal_boundary_record_context` implies `boundary_first_context`. Unknown, stale, contradictory, or ambiguous predicate evidence stops before the dependent judgment, write, or claim. Late discovery reclassifies and loads the required resource before final status or recording.

### Closed loaded-resource profiles

Recording authority and boundary applicability remain independent, producing four resource assemblies:

| Profile | Durable procedure | Boundary procedure | Loaded resources |
| --- | ---: | ---: | --- |
| `SR0-core` | no | no | `SKILL.md` plus result asset; finding asset only when used |
| `SR0B-boundary` | no | yes | core plus boundary method and, when formally required, feature-authoring reference |
| `SR1-recorded` | yes | no | core plus recording-and-settlement reference |
| `SR1B-recorded-boundary` | yes | yes | core plus recording reference and applicable boundary references |

The exact feature-authoring reference trigger is an additive subcondition inside the boundary profiles, not a fifth authority profile. Each unique resource loads once.

### Universal `SKILL.md` ownership

Keep inline:

- purpose, trigger, stage ownership, near-miss routing, and review-only edit restriction;
- target identity, evidence precedence, bounded reading, and project-local portability;
- review dimensions and table structure, verdict enum, severity policy, and material-finding sufficiency;
- normal, empty, boundary, error, permission, migration, rollout, rollback, old-client, and old-data review prompts in compact form;
- review status, immediate-next-stage, eventual-test-spec-readiness, and stop-condition vocabularies and consistency rules;
- the identical shared `Isolation and Recording` obligation block;
- compact artifact-placement defaults and the rule that durable recording does not grant formal settlement;
- formal settlement and workflow-continuation boundaries without their detailed mutation sequence;
- the checked four-question boundary scan and exact reference triggers;
- manual requirement-fidelity opt-in as a compact conditional rule;
- universal stops, claims, result applicability, and missing-resource behavior.

### Recording-and-settlement reference ownership

`references/spec-review-recording-and-settlement.md` owns only conditional mechanics:

- change-ID and record-location resolution;
- minimal recording-root creation and collision handling;
- clean receipt versus detailed review record selection;
- review-log synchronization and conditional review-resolution procedure;
- reconstructed-record handling when fixes began before recording;
- exact complete-`change.yaml` inspection and matching spec-entry settlement sequence;
- idempotent retry, conflicting review-ID, concurrent update, illegal transition, failed validation, and blocked-write handling;
- workflow-managed context reset and manifest-only evidence required by the current rollout;
- automation-specific pause and return-to-workflow procedure.

Loading this reference grants no authority. `advisory-durable` may record but never settle. `formal-lifecycle/manual` may settle only the matching spec entry after recording. `formal-lifecycle/workflow-managed-automated` adds current manifest-only evidence and returns control to workflow. No mode advances routing or edits the reviewed spec.

### Boundary reference ownership

The inline compact scan decides applicability. `boundary-first-method-v1.md` owns detailed vocabulary, dimensions, identifiers, interactions, examples, consumption, semantic-versus-structural proof, and portable stops. `boundary-first-feature-authoring-v1.md` owns formal feature-record headings, tables, and owner-scoped completeness procedure.

The skill retains stage-specific judgment: whether the reviewed spec has adequate applicable boundaries, interactions, invariants, outcomes, and example ownership. It does not duplicate resource tables or identifier grammar inline. Existing projection ownership, paths, and raw bytes remain unchanged.

### Asset ownership

The result and finding assets remain the only structural assets. They own headings, labels, ordering, and placeholders only. `SKILL.md` and applicable references own field meaning, applicability, status, recording, settlement, and handoff. Inapplicable optional sections are omitted; applicable unavailable data reports `blocked` or `unknown`; unfilled placeholders are forbidden.

### Conflict and failure behavior

A conditional reference may specialize only its activation context. It cannot override inline universal policy or another reference's contract. Any contradiction is a package defect and stops dependent work.

Missing or unreadable recording procedure stops required recording or settlement but does not erase the review judgment or complete findings. Missing required boundary procedure stops the dependent boundary conclusion. An untriggered resource does not load and does not block ordinary review. The skill never reconstructs missing procedure from memory.

### Preservation and measurement

Before moving prose, create separate change-local ledgers for semantic rules and literal dependencies. Semantic dispositions must account for every significant rule as retained inline, retained in the recording reference, retained in an existing boundary reference, asset-owned, removed duplicate, or removed only with an approved contract change. Literal dependencies must be classified as normative contract, parser/package contract, incidental test, or obsolete. Incidental tests must not become capitalization or prose-policy owners.

Measure LF-normalized canonical resources using UTF-8 bytes and Unicode whitespace-separated words. Report `SKILL.md`, every resource, each profile, and the complete package separately. A 25–40 percent `SR0-core` reduction is a planning target, not a semantic acceptance threshold. No material ordinary-path reduction means the proposal objective was not met.

## Expected Behavior Changes

- Ordinary direct reviews load a shorter self-sufficient contract and the result structure.
- Durable or formal reviews additionally load one recording-and-settlement reference.
- Boundary-first reviews load only the existing boundary resources required by their active context.
- Review outcomes, finding rigor, routing, readiness, recording duties, settlement authority, and workflow ownership remain unchanged.
- Missing required resources fail safely instead of causing partial or remembered procedure.

## Architecture Impact

The expected assessment is `architecture-not-required` because the existing architecture already supports mapped conditional references, structural assets, projected boundary resources, canonical source ownership, and package parity. The change adds no runtime, state, dependency, service, or lifecycle owner.

A bounded architecture documentation update is required only if the current package inventory presents `spec-review` as permanently limited to its existing resources. A new ADR is required only if specification changes the normative published-package model or gives the new reference independent authority. If implementation requires such an architecture change, this change owns and reviews the architecture document rather than treating architecture as an external prerequisite.

## Testing and Verification Strategy

Use three proof classes:

1. Deterministic structure and package proof for frontmatter, required inline sections, closed values, resource-map syntax, mapped resource existence, projection identity, placeholders, canonical/generated/archive/install parity, and missing-resource failure.
2. Static scenario fixtures for direct clean review, late material finding, advisory recording, formal manual review, formal automated review, boundary review, formal boundary record, combined contexts, ambiguous identity, stale authorization, retry, blocked recording, and invalid predicate implications.
3. Independent semantic review of the final package against the rule-disposition and literal-compatibility ledgers.

Do not execute Codex, Claude Code, opencode, or another target-agent runtime. Do not add prompt journeys, transcript grading, model fixtures, permanent simplicity validators, tokenizer dependencies, or a new validator family. Extend existing skill, review-artifact, boundary, build, and adapter proof owners only when permanent contract coverage is genuinely missing.

## Rollout and Rollback

Roll out the canonical `SKILL.md`, new reference, unchanged or deliberately updated assets, directly coupled contract consumers, and generated package inventory as one reviewed revision. Validate all mapped resources before distribution and fail partial or mixed resource versions.

Rollback restores the complete previous canonical package and coupled consumers, then rebuilds and validates derived packages. Existing durable review records require no data migration because review schema and lifecycle state do not change.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Universal policy is hidden behind the recording reference. | Closed inline ownership list, rule ledger, semantic review, and direct-profile fixtures. |
| Older `SFA-R6` wording is violated or silently ignored. | Amend it explicitly to distinguish inline obligations from conditional mechanics. |
| Boundary-first compatibility is weakened. | Preserve the checked compact scan, exact reference paths, projection manifest, and raw-byte parity. |
| Resource triggers become ambiguous. | Closed predicates, implication rules, late reclassification, and fail-safe ambiguity behavior. |
| Automation gains authority through resource loading. | Separate loaded profiles from authority modes; automation requires current same-change formal authority. |
| Relocation is misreported as deletion. | Report profile and total-package measurements separately. |
| Tests freeze incidental wording. | Separate semantic and literal ledgers; migrate incidental consumers rather than preserving accidental prose. |
| Package growth outweighs direct benefit. | Require material `SR0` reduction and explain every total-package delta. |

## Open Questions

None. The specification must inventory exact current consumers and requirement IDs, but it should not reopen the selected package shape, ownership split, predicate implications, proof boundary, or non-normative size target without new contradictory evidence.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-12 | Select one new recording-and-settlement reference and retain the two existing boundary references. | These are the actual conditional procedure boundaries; more references would fragment authority. | Unchanged, inline-only, boundary-only extraction, many-reference split, shared engine |
| 2026-08-12 | Preserve universal obligations and the compact boundary scan inline. | Existing contracts require them and direct review must remain safe without optional procedure. | Moving all recording or boundary policy out of `SKILL.md` |
| 2026-08-12 | Keep target-runtime execution outside acceptance. | Static contract, package, and semantic proof are deterministic and proportionate. | Agent journeys and transcript grading |
| 2026-08-12 | Treat size reduction as evidence rather than a hard percentage. | Semantic preservation must not be traded for numerical optimization. | Permanent line, token, or prose-quality gates |

## Next Artifacts

- Formal `proposal-review` evidence and settlement.
- If approved, a focused spec or amendment covering the `spec-review` package contract and directly coupled older clauses.
- Bounded architecture assessment, followed by architecture work only if that assessment requires it.
- Execution plan and test specification before implementation.

## Follow-on Artifacts

None yet.

## Readiness

Ready for independent `proposal-review`. This proposal does not claim acceptance, specification readiness, implementation readiness, verification, branch readiness, or PR readiness.
