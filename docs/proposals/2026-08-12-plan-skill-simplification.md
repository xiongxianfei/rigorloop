# Plan Skill Simplification

## Owning change record

`docs/changes/2026-08-12-plan-skill-simplification/change.yaml`

## Problem

The published `plan` skill remains rigorous, but its 270-line, 2,555-word `SKILL.md` loads portable planning guidance together with RigorLoop-specific `change.yaml` mutation, one-time `planned_work` initialization, workflow-managed milestone procedure, repeated boundary-first detail, and repeated output descriptions. A contributor creating an ordinary execution plan must scan procedure that applies only when a valid governed change grants stage-owned write authority.

The package also contains overlapping ownership. Purpose, trigger, inputs, evidence access, output, handoff, and readiness rules appear in multiple sections. The inline boundary method repeats concepts from the mapped 857-word reference. The milestone asset still contains mutable `Milestone state` and execution closeout fields even though the current Constitution and stage-owned lifecycle contract make `change.yaml` the sole owner of mutable milestone state. Repository parsers and tests still consume that literal, so this inconsistency cannot be fixed by silently deleting a line from the asset.

The optimization must preserve what makes `plan` valuable: requirement and architecture traceability, independently reviewable milestones, validation and recovery, stable execution intent, the exact one-time `planned_work` initialization exception, plan-review handoff, boundary-first planning, customer-project portability, and truthful claim boundaries.

## Goals

- Make the portable planning contract materially shorter and easier to scan without weakening milestone quality, validation, recovery, traceability, or handoff safety.
- Keep `SKILL.md` self-sufficient for invocation classification, upstream readiness, plan design, stable-state boundaries, universal stops, claims, and resource selection.
- Give governed plan registration, authoring-state mutation, one-time `planned_work` initialization, and workflow-managed procedure one conditional owner.
- Retain the existing boundary-first reference under its governed activation contract while removing duplicated detailed guidance from the common path.
- Keep the existing three assets as the sole structural plan owners and remove mutable lifecycle state from copied plan structure through an atomic contract-and-consumer migration.
- Measure the portable and governed loaded profiles separately from the main file and total package.
- Prove semantic preservation, literal compatibility, package parity, and migration safety without executing a target-agent runtime or adding permanent simplicity machinery.

## Non-goals

- Do not change the purpose of execution plans, lifecycle stage order, plan-review authority, implementation authorization, workflow continuation, or final-closeout semantics.
- Do not let a mapped reference become an independent lifecycle or policy owner.
- Do not optimize `plan-review`, `test-spec`, `implement`, or another skill in this change except for directly coupled consumers that must migrate away from mutable plan-body state.
- Do not create a generic planning engine, router, scheduler, state store, new lifecycle schema, fourth asset, or additional output template.
- Do not remove the boundary-first compact scan, stable IDs, validation timing, rollback obligations, or downstream gap routing.
- Do not add target-agent journeys, transcript grading, model selection, permanent word or token budgets, or prose-quality scoring.
- Do not reopen or rewrite the historical evidence for the completed assets-first plan pilot.

## Vision fit

fits the current vision

The change makes planning guidance easier to inspect and use while preserving the durable, reviewable chain from approved requirements and architecture to milestones, proof, implementation, and handoff.

## Context

The current package contains one main file, one shared boundary reference, and three normative structural assets:

| Resource | Lines | Words | UTF-8 bytes | Current role |
| --- | ---: | ---: | ---: | --- |
| `SKILL.md` | 270 | 2,555 | 18,680 | Portable plan judgment plus governed lifecycle procedure |
| `boundary-first-method-v1.md` | 110 | 857 | 6,346 | Shared detailed boundary vocabulary and method |
| Three assets | 102 | 363 | 2,860 | Plan, milestone, and decision-log structure |
| Complete package | 482 | 3,775 | 27,886 | Maintenance and distribution footprint |

The historical assets-first plan pilot deliberately prohibited references for that pilot and required exactly three assets. This proposal is a separate follow-on package refactor. The downstream spec must preserve the completed pilot as history while adding explicit authority for one plan-owned conditional reference under the repository's current mapped-resource integrity contract.

The current Constitution and `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md` establish that plan bodies carry stable intent and `change.yaml` owns mutable milestone state. The current `assets/milestone.md`, workflow parsers, lifecycle synchronization code, tests, and fixtures still treat a plan-body `Milestone state` line as a compatibility surface. The proposal therefore includes a bounded atomic migration: remove mutable state and execution-progress checklist fields from the canonical milestone asset, move every live consumer to `change.yaml`, and update incidental fixtures instead of preserving an obsolete second state owner.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Identify the best way to optimize `plan`. | in scope | Options Considered and Recommended Direction |
| Create a new branch. | in scope | Change-local authoring evidence |
| Create a proposal. | in scope | This artifact |
| Run proposal review. | in scope | Next Artifacts and formal review evidence |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Simplify the portable `plan` common path. | core to this proposal | Primary user-visible objective |
| Add one governed plan-authoring reference. | core to this proposal | Removes change-record mutation from portable planning |
| Preserve checked boundary-first loading. | same-slice dependency | Boundary activation and raw-byte parity are compatibility surfaces |
| Retain exactly three structural assets. | same-slice dependency | Existing assets already provide the correct structural ownership model |
| Remove mutable milestone state from the milestone asset. | same-slice dependency | Current higher-priority lifecycle ownership forbids a second mutable state owner |
| Migrate parsers, validators, and fixtures to `change.yaml`. | same-slice dependency | Required for an atomic compatibility-safe asset correction |
| Add deterministic preservation and package proof. | same-slice dependency | Required for a safe published-package change |
| Record a bounded architecture assessment. | same-slice dependency | Confirms whether the existing package and lifecycle models remain sufficient |
| Optimize adjacent skills. | out of scope | Each skill requires its own evidence and ownership decision |
| Add runtime evaluation or permanent simplicity validation. | out of scope | Disproportionate and nondeterministic for this refactor |

## Options Considered

### Option 0: Keep the package unchanged

This has no immediate migration cost but preserves unnecessary common-path loading, duplicate ownership, and the plan-body milestone-state inconsistency.

### Option 1: Editorial compression only

This can consolidate repeated prose and reduce scan cost with minimal package change. It cannot remove governed mutation procedure from portable planning, and it would leave the milestone asset as a second state surface.

### Option 2: Keep all policy inline and only correct the assets

This resolves mutable-state ownership and preserves a flat procedural file. It still makes portable plans load detailed `change.yaml` mutation and workflow-managed initialization procedure that they cannot use.

### Option 3: Add one governed reference, tighten boundary disclosure, and correct the milestone asset atomically

This keeps universal plan judgment and safety inline, moves only governed procedure behind one evidence-based trigger, retains the existing boundary resource, and aligns the assets and their consumers with current lifecycle ownership. It creates one new navigation target at a real authority boundary and one bounded parser migration.

### Option 4: Split milestone design, validation, recovery, governed state, automation, and boundary procedure into separate references

This could minimize each loaded variant but would fragment the core planning method, create too many predicates, and increase the chance that a plan omits a universal quality obligation.

### Option 5: Replace prose planning with an executable planning engine

This could enforce structure mechanically but would introduce runtime and policy ownership beyond the scope of skill simplification, and deterministic code cannot own semantic milestone decomposition or recovery judgment.

## Recommended Direction

Adopt Option 3.

The target package is:

```text
skills/plan/
├── SKILL.md
├── references/
│   ├── governed-plan-authoring.md
│   └── boundary-first-method-v1.md
└── assets/
    ├── plan-skeleton.md
    ├── milestone.md
    └── decision-log-row.md
```

### Invocation classification and resource loading

Use two independent predicates:

| Predicate | Meaning |
| --- | --- |
| `governed_change_context` | One exact current change, plan artifact identity, valid `lifecycle_contract: stage-owned-change-local-v1`, settled prerequisites, and plan-authoring authority are resolved. |
| `boundary_first_context` | The existing checked boundary contract or cited approved boundary evidence requires detailed interpretation for the plan. |

Conversational wording, a plan path, or the existence of any `change.yaml` does not establish governed authority. Missing, stale, contradictory, mismatched, or ambiguous identity stops before governed writes. A missing change record routes to `workflow` for creation or migration; `plan` does not invent governed state.

Use exactly four loaded-resource profiles:

| Profile | Governed change | Boundary procedure | Loaded resources |
| --- | ---: | ---: | --- |
| `PL0-portable` | no | no | `SKILL.md` |
| `PL0B-portable-boundary` | no | yes | `SKILL.md` plus boundary reference |
| `PL1-governed` | yes | no | `SKILL.md` plus governed reference |
| `PL1B-governed-boundary` | yes | yes | `SKILL.md` plus both references |

These profiles measure procedural context only. Structural assets are copied output resources and are measured separately because their use varies with plan shape. Each unique procedural resource loads once. The plan skeleton and milestone asset apply to every new multi-milestone plan; the decision-log row applies only when a material sequencing or planning decision is recorded. Late trigger discovery must load the required reference before dependent interpretation, mutation, or readiness claims.

Classify execution authority independently as `manual` or `workflow-managed`. Workflow-managed execution requires current same-change authorization and a valid governed change, but it does not create another resource assembly or enlarge the `plan` write set. Unknown, stale, contradictory, or mismatched automation evidence stops automation-dependent work without changing the underlying plan classification.

### Universal `SKILL.md` ownership

Keep inline:

- purpose, trigger, workflow role, project-local portability, and near-miss routing;
- source precedence, bounded evidence access, and compact upstream settlement checks;
- requirement and architecture traceability;
- plan-body stability, state ownership, artifact placement, and index-link rules;
- milestone decomposition, independently closeable slices, dependencies, proof timing, validation, risk, rollback, recovery, and lifecycle-closeout milestone kind;
- the universal rule that `plan` may initialize missing primary-plan `planned_work` exactly once under governed authority and may never replace or update existing `planned_work`;
- compact automation-aware planning obligations without the state mutation procedure;
- the checked four-question boundary scan, upstream gap routing, plan-specific boundary mapping, and exact reference triggers;
- universal stop conditions, claims, readiness-versus-Done distinction, result shape, and `plan-review` handoff.

Consolidate repeated sections so each rule has one owner. Merge purpose and use guidance; merge project evidence and inputs; merge placement and bounded change-record reads; merge output, result, skeleton, and handoff descriptions; and keep one concise readiness and claim boundary.

### Governed reference ownership

`references/governed-plan-authoring.md` loads exactly when `governed_change_context` is true. It owns only governed procedure:

- complete `change.yaml` inspection and exact plan-entry resolution;
- plan-entry creation and `authoring` to `review-required` transitions;
- authoring-evidence placement and completion fields;
- one-time deterministic `planned_work` initialization from ordered stable milestone definitions, including required initial values;
- the prohibition on replacing or updating existing `planned_work`;
- idempotent retry, collision, concurrent-write, illegal-transition, stale-evidence, and failed-validation handling.

The reference grants no authority merely because it is loaded. Manual and workflow-managed plan authoring use the same governed procedure and the same plan-owned write set. Under workflow-managed execution, `plan` may consume current authorization and emit only its ordinary plan artifact, authoring evidence, matching artifact transition, and permitted one-time initialization. It stops after the plan entry is `review-required` and reports `plan-review` as the handoff.

`plan-review` alone owns review evidence and settlement. `workflow` alone owns automation packets or receipts, routing, continuation, and every later `planned_work` transition. The reference must not own milestone design, stage order, review settlement, automation evidence, post-review return, later planned-work transitions, workflow continuation, or implementation authorization. Any contradiction with inline universal policy is a package defect and stops dependent work.

### Boundary reference ownership

The checked boundary activation contract remains the owner of adoption and applicability. The inline four-question scan always runs for qualifying decisions. Load `boundary-first-method-v1.md` only when approved boundary or interaction rows must be interpreted or when cited rows are missing, stale, unknown, ambiguous, conflicting, escaped, or insufficient.

Keep only the compact scan, upstream routing, and plan-specific mapping obligation inline. The reference remains the sole owner of detailed dimension vocabulary, identifier grammar, interaction selection, structural-versus-semantic validation, scenario stopping, and portable failure cases. Missing or unreadable required boundary procedure stops boundary-dependent planning; the skill must not reconstruct it from memory.

### Asset ownership and milestone-state migration

Retain exactly the existing three normative assets. Assets own section order, labels, table shape, and placeholders only; they do not own lifecycle policy, status meaning, routing, or authority.

`plan-skeleton.md` continues to carry only the stable owning change-record pointer in `Current Handoff Summary`. `decision-log-row.md` remains structural. Revise `milestone.md` so copied plan bodies contain stable execution intent:

```text
milestone ID and title
milestone kind
goal
requirements and architecture decisions
affected components
dependencies
tests and proof
implementation steps
validation commands
expected observable result
completion criteria
required evidence
review handoff
risks
rollback or recovery
commit boundary when useful
```

`completion criteria` states the stable observable conditions that make the planned slice complete. `required evidence` names the stable proof surfaces and command-result classes expected at execution. `review handoff` identifies the owning review or lifecycle gate after the slice. An `implementation` milestone produces implementation and proof and normally hands off to `code-review`. A `lifecycle-closeout` milestone contains no implementation work; it names a downstream evidence stage such as `ci-maintenance`, `explain-change`, or `verify`, its prerequisite evidence, and its owning handoff.

Remove mutable `Milestone state` and execution-progress closeout checkboxes from the plan asset. Actual command outcomes, validation progress, implementation progress, commit completion, current blockers, current review status, milestone state, and closeout readiness live only in `change.yaml` or stage-owned evidence.

The downstream spec must inventory every literal and parser consumer, classify it as normative, parser/package, incidental test, or obsolete, and migrate live state reads to the owning `change.yaml#workflow_state.planned_work`. Parser or schema consumers migrate atomically; incidental fixtures update instead of preserving obsolete prose. Historical plans may retain embedded state as historical evidence but never as current authority. No compatibility adapter may recreate mutable plan-body state as a second source of truth.

### Semantic preservation and literal compatibility

Create two change-local inventories before editing the skill package:

```text
docs/changes/2026-08-12-plan-skill-simplification/plan-rule-disposition.yaml
docs/changes/2026-08-12-plan-skill-simplification/plan-literal-compatibility.yaml
```

The rule ledger gives every behaviorally significant current rule one source, behavior, applicable profile, disposition, destination, governing requirement, and preservation proof. Closed dispositions are `retained-inline`, `retained-governed-reference`, `retained-boundary-reference`, `asset-owned`, `removed-duplicate`, and `removed-obsolete-with-approved-contract-change`.

The literal inventory separately classifies exact headings, phrases, asset metadata, field labels, vocabulary, and parser dependencies as `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, or `obsolete`. Preserve normative literals unless the governing contract is amended, migrate parser contracts and all consumers atomically, update incidental tests rather than freezing prose, and remove obsolete literals with evidence.

### Simplification measurement

Use canonical authored files, normalize line endings to LF, count each unique procedural resource once, and record the exact resource list and identities for every profile. UTF-8 bytes and Unicode whitespace-separated words are the required portable metrics. Reuse a repository-owned pinned tokenizer only if one already supports the exact assembly; otherwise omit token estimates rather than adding a dependency.

Procedural profile assemblies are deterministic:

| Profile | Exact measured assembly |
| --- | --- |
| `PL0-portable` | `SKILL.md` |
| `PL0B-portable-boundary` | `SKILL.md` plus `boundary-first-method-v1.md` |
| `PL1-governed` | `SKILL.md` plus `governed-plan-authoring.md` |
| `PL1B-governed-boundary` | `SKILL.md` plus both references |

Do not include assets in procedural loaded-context totals. Report every asset's canonical words and bytes separately. Also report one fixed representative output assembly consisting of `plan-skeleton.md` plus one `milestone.md`, with no decision-log row, and report `decision-log-row.md` as an additive delta. Do not multiply asset size by milestone or decision count. Report the total canonical package independently.

Report before and after:

| Metric | Purpose |
| --- | --- |
| `SKILL.md` lines, words, and bytes | Main-file common-path scale |
| `PL0-portable` loaded words and bytes | Primary customer-project planning cost |
| `PL1-governed` loaded words and bytes | Primary governed authoring cost |
| Boundary-profile deltas | Conditional boundary cost |
| Each reference and asset | Procedural or structural resource contribution |
| Fixed representative asset assembly | Stable output-structure comparison |
| Total package words and bytes | True maintenance and distribution footprint |
| Duplicate rule clusters | Ownership improvement |
| Literal/parser migrations | Compatibility evidence |

Acceptance requires both `PL0-portable` and `PL1-governed` procedural words and bytes to decrease from baseline, every duplicate cluster to have one loaded owner, and every significant rule to have one disposition. `PL0B` and `PL1B` must have no unexplained growth. Governed profile reduction prevents the change from presenting relocation as simplification. Asset and total-package changes are separate evidence and cannot substitute for procedural reduction. A 30–40 percent `SKILL.md` reduction is a planning target, not a normative gate; semantic and lifecycle preservation take precedence. Total package growth is allowed only when the new conditional reference improves loaded profiles, and the delta must be explained.

The completed historical assets-first pilot's 15 percent token target and package budget remain historical acceptance evidence for that pilot. The downstream spec adds a new follow-on acceptance slice rather than rewriting the old result.

## Expected Behavior Changes

- Ordinary customer-project planning loads a shorter universal planning contract and the applicable structural assets without RigorLoop-specific mutation procedure.
- Governed planning loads one additional plan-owned procedure only after exact stage authority is established.
- Manual and workflow-managed plan authoring use the same plan-owned writes; `workflow` retains automation and continuation, and `plan-review` retains review settlement.
- Boundary detail loads only under the existing checked activation contract or when approved boundary evidence requires interpretation.
- New plan bodies retain stable completion criteria, required evidence, and review handoff but no longer copy mutable milestone state or execution-progress fields; authoritative current state remains in `change.yaml`.
- Existing plan quality, milestone sequencing, validation, rollback, claim, and handoff behavior remains unchanged.
- A missing required conditional resource stops dependent work instead of triggering remembered or partial procedure.

## Architecture Impact

The expected architecture result is `architecture-not-required` after a bounded assessment. The existing architecture already defines a published skill as canonical `SKILL.md` plus mapped references and assets, with canonical, generated, packed, and installed resource parity. The new reference remains owned by `plan`, introduces no runtime, service, dependency, persistence model, or lifecycle owner, and uses the existing package model.

The assessment must also confirm that moving mutable milestone reads from plan bodies to the already-authoritative `change.yaml` is an alignment with the existing stage-owned lifecycle architecture rather than a new decision. Update an architecture inventory or example only if it incorrectly depicts `plan` as permanently flat or identifies the plan body as a mutable state owner. A new ADR is required only if implementation discovers a new durable package, persistence, or ownership decision.

The owning `change.yaml` for this simplification remains the owner of its architecture assessment result. The proposal and any architecture document record stable rationale; mutable assessment status and routing stay in the change record.

## Testing and Verification Strategy

Use three proof classes:

1. Deterministic structural and package proof validates frontmatter, required compact sections, closed vocabularies, resource-map grammar, exact asset count, asset metadata and fingerprints, mapped-resource existence, placeholder absence, canonical/generated/archive/install parity, and fail-closed unknown values.
2. Static contract fixtures cover all four resource profiles, manual and workflow-managed execution authority, exact governed authority, plan-owned write boundaries, new-plan initialization, existing `planned_work`, ambiguous identity, boundary activation, late triggers, missing resources, stable milestone completion structure, lifecycle-closeout distinction, parser migration, result claims, and handoff behavior.
3. Independent semantic review checks trigger clarity, source alignment, milestone quality, requirement coverage, sequencing, validation, recovery, lifecycle ownership, stops, claims, output usefulness, and preservation-ledger completeness.

Do not execute Codex, Claude Code, opencode, or another target-agent runtime for implementation, verification, or release acceptance. Do not add prompt journeys, transcript grading, model-selection fixtures, permanent simplicity checks, or a new validator family. Extend existing skill, asset, lifecycle, workflow, package, and adapter checks only where they already own the affected contract.

## Rollout and Rollback

Roll out the canonical package, direct contract amendments, parser migration, deterministic fixtures, and generated package resources atomically. Validate canonical source first, then generated staging, packed release candidates, and clean installed targets. Mixed resource versions, missing mapped references, stale asset fingerprints, or any remaining live plan-body milestone-state dependency block rollout.

Rollback reverts the canonical skill, reference, assets, directly coupled parser changes, fixtures, and generated package state together. Because the change introduces no new persistent format and moves live state reads to an existing authoritative field, no data migration rollback is expected. Historical plans remain readable evidence; they are not rewritten merely to remove old embedded state fields.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Universal plan quality is hidden behind a reference. | Keep milestone design, traceability, validation, recovery, stops, claims, and handoff inline; use the rule ledger and semantic review. |
| Loading the governed reference is mistaken for write authority. | Require exact identity and lifecycle evidence; state that loading grants no authority; test false and ambiguous cases. |
| Plan absorbs automation or plan-review ownership. | Keep execution mode separate from package loading and preserve workflow and plan-review as the exclusive owners of their evidence and continuation. |
| One-time `planned_work` initialization is weakened or duplicated. | Preserve the universal ownership rule inline, keep the exact procedure in one reference, and add initialization and existing-state fixtures. |
| Milestone cleanup removes stable exit criteria. | Retain completion criteria, required evidence, review handoff, and milestone kind while moving only runtime progress and state. |
| Removing `Milestone state` breaks parsers or old plans. | Inventory every consumer, migrate live reads atomically to `change.yaml`, retain historical-plan readability, and test both current and historical inputs. |
| Content is merely relocated and the common governed profile does not improve. | Require measured reductions for both `PL0` and `PL1`, plus separate total-package reporting. |
| Variable asset use makes measurements non-repeatable. | Exclude assets from procedural profiles and use one fixed representative structural assembly plus a decision-row delta. |
| Boundary activation gains a second owner. | Preserve the checked activation contract and make `plan` only a consumer. |
| Assets acquire hidden policy. | Keep assets structural, validate their metadata and fingerprints, and retain policy in `SKILL.md` or the governed reference. |
| Existing literal tests freeze accidental prose. | Classify semantic rules and literal dependencies separately and update incidental tests. |
| Package installation omits the new reference. | Require existing canonical-to-generated, archive, and clean-install parity checks. |

## Open Questions

None. The downstream specification must inventory exact parser consumers and governing requirement IDs, but it must not reopen the selected package shape, authority model, milestone-state ownership, proof boundary, or measurement model without a new proposal decision.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-12 | Use one governed plan-authoring reference. | Governed mutation is one genuine conditional authority boundary; more references would fragment core planning. | Inline-only compression and highly fragmented references |
| 2026-08-12 | Keep exactly three assets and no result asset. | Existing assets already own repeated plan structure; the compact invocation result does not justify another packaged template. | Fourth asset or re-inlined structures |
| 2026-08-12 | Remove mutable milestone state from copied plan structure through an atomic consumer migration. | Current lifecycle authority makes `change.yaml` the sole mutable state owner. | Preserve a conflicting second state surface |
| 2026-08-12 | Make both portable and governed loaded-profile reduction normative without a fixed percentage. | This proves real simplification while preventing numeric optimization from weakening semantics. | Main-file-only or hard-percentage acceptance |
| 2026-08-12 | Exclude target-agent runtime acceptance. | Static contract proof, package parity, and independent semantic review are deterministic and proportionate. | Prompt journeys and transcript grading |
| 2026-08-13 | Keep automation and post-review continuation outside `plan`. | Execution mode does not change plan-owned writes; workflow and plan-review retain their stage authority. | Plan-owned automation receipts or post-review return |
| 2026-08-13 | Preserve stable milestone completion fields while removing mutable progress. | Plans need durable exit and proof intent without becoming a second current-state owner. | Removing the entire closeout concept or retaining mutable checkboxes |
| 2026-08-13 | Separate procedural profile metrics from structural asset metrics. | Exact resource assemblies must be repeatable regardless of milestone or decision count. | Variable applicable-asset totals |

## Next Artifacts

- Independent `proposal-review` with durable formal review evidence.
- A focused plan-skill simplification specification after proposal approval.
- A bounded architecture assessment owned by this change record.
- Execution plan, plan-review, test specification, and test-spec-review before implementation.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent `proposal-review`. This proposal does not claim approval, specification readiness, implementation readiness, or automatic downstream handoff.
