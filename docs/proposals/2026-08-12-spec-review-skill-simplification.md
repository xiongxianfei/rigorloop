# Spec-Review Skill Simplification

## Owning change record

`docs/changes/2026-08-12-spec-review-skill-simplification/change.yaml`

## Problem

The published `spec-review` skill is rigorous but its 284-line, 2,174-word common path mixes ordinary contract judgment with detailed formal settlement, workflow-managed review evidence, and a long boundary-first method that is also available through packaged references. A direct review pays this context cost even when it only needs to judge requirement clarity, completeness, testability, examples, compatibility, observability, security, non-goals, acceptance criteria, routing, and readiness.

Several rules also have overlapping textual owners. Artifact placement and settlement are spread across placement, change-record, recording, rules, and handoff sections. The inline boundary-first method repeats substantial concepts from two mapped references. Output fields appear in both skill prose and assets. This increases scan cost and synchronization risk without improving the review standard.

The optimization must respect existing contracts that require review dimensions, review guidance, verdicts, severity, material-finding sufficiency, recording obligations, validation obligations, lifecycle boundaries, and a compact boundary scan to remain inline. The problem is therefore not solved by hiding universal policy in references; it is solved by keeping the obligations compact and moving only genuinely conditional operational detail.

## Goals

- Make the universal review contract materially shorter and easier to scan, and remove duplicated procedure from the loaded formal-review profiles without weakening contract judgment or downstream safety.
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

### Formal review and authority classification

Every invocation owned by `spec-review` is a formal lifecycle review and requires durable recording. This includes direct review, governed review, explicit approval or status judgment, implementation-handoff judgment, eventual test-spec readiness judgment, durable-record requests, and results intended as lifecycle evidence.

Feedback, critique, or discussion that explicitly does not request a formal review result is outside the `spec-review` skill contract. Route it to ordinary conversational assistance or an applicable ideation skill such as `explore`; do not create a `spec-review` resource profile, result variant, durable record, status, readiness claim, or boundary-review verdict for it.

Classify two independent authority axes for every formal review:

| Axis | Closed values | Governing rule |
| --- | --- | --- |
| `settlement_mode` | `isolated`, `governed-spec-entry` | Direct wording, a generated recording root, or a material finding never grants settlement; only current evidence resolving the exact same change, spec artifact, and reviewable spec entry permits `governed-spec-entry`. |
| `automation_mode` | `manual`, `workflow-managed-automated` | Automation requires current durable workflow authorization for the same governed change and spec entry; conversational wording, stale evidence, or mismatched identity is insufficient. |

`workflow-managed-automated` implies `governed-spec-entry`. An isolated formal review records evidence but never settles the spec entry or advances workflow. Unknown, mixed, stale, or ambiguous authority evidence stops before settlement, automation, or dependent claims.

### Closed loaded-resource profiles

Boundary applicability determines the two loaded-resource profiles; settlement and automation determine permitted branches inside the recording procedure rather than granting resources authority:

| Profile | Review kind | Boundary procedure | Loaded resources |
| --- | --- | ---: | --- |
| `SR1-formal` | `formal-lifecycle` | no | core plus recording-and-settlement reference |
| `SR1B-formal-boundary` | `formal-lifecycle` | yes | core plus recording reference and applicable boundary references |

Every `spec-review` is `SR1-formal` or `SR1B-formal-boundary`. The exact feature-authoring trigger remains an additive checked condition inside the boundary profile. Each unique resource loads once.

### Recording and settlement side effects

Loading the recording reference grants no write, settlement, automation, or continuation authority. The closed authority matrix is:

| Review execution | Durable review evidence | Spec-entry settlement | Workflow continuation | Automation evidence |
| --- | ---: | ---: | ---: | ---: |
| Isolated formal manual | yes | no | no | no |
| Governed formal manual | yes | yes, for the exact matching spec entry only | no; return control to workflow | no |
| Governed formal automated | yes | yes, for the exact matching spec entry only | no; return control to workflow | yes, under current same-change authorization |

### Isolated formal-review recording boundary

This simplification introduces no new placement authority. Isolated formal review reuses `specs/formal-review-recording.md`: `R31a` through `R31n` own change-ID selection and blocked-location behavior, while `R4h` through `R4l` and `R24` through `R26` own the minimal root and required evidence shape.

Location resolution uses the existing order: an active owning change root, reviewed-artifact or active-plan metadata, an explicit user change ID, then the deterministic generated review-recording ID. Ambiguous identity, unsafe placement, an unrelated collision, or a failed write produces `Recording status: blocked` and the smallest action needed to continue; the review judgment may still be returned, but formal completion, settlement, and continuation are not claimed. The result is not silently downgraded to informal feedback.

The permitted isolated write set is closed:

| Situation | Permitted artifacts |
| --- | --- |
| Existing owning root | The stage review record or clean receipt and `review-log.md`; `review-resolution.md` only when material findings, a blocking or revision outcome, or another approved trigger requires disposition; aggregate review metadata only as required by the existing recording contract. |
| New clean recording-only root | Minimal `change.yaml`, `review-log.md`, and `reviews/spec-review-r<n>.md`; no `review-resolution.md` solely for a clean result. |
| New material or disposition-required recording-only root | Minimal `change.yaml`, `review-log.md`, `reviews/spec-review-r<n>.md`, and required `review-resolution.md`. |

A recording-only `change.yaml` identifies the change ID, reviewed artifact, review-log path, review status, and unresolved count required by the existing schema. It does not create or modify a governed spec-entry settlement, active plan, workflow routing state, lifecycle progression, automation authorization, or automation run. Those mutations require separately valid governed authority. The existence of review evidence or a recording-only root never makes the reviewed work governed.

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

The reference contains clearly separated isolated-recording, governed-settlement, and governed-automation branches. `SKILL.md` selects the valid branch from the two authority axes. Isolated formal review may record but never settle; governed manual review may settle only the matching spec entry after recording; governed automated review adds current manifest-only evidence and returns control to workflow. No branch advances routing or edits the reviewed spec.

### Boundary reference ownership

The existing checked-revision boundary contract and `specs/boundary-first-resources.yaml` remain the sole activation owners. `spec-review` consumes their decision and does not define a second local activation policy. The inline four-question scan always runs. Load `boundary-first-method-v1.md` when the checked contract requires active boundary interpretation, then load `boundary-first-feature-authoring-v1.md` only when formal boundary-record completeness must be judged or a grandfathered revision is potentially substantive.

A grandfathered non-substantive revision does not trigger formal boundary-record adoption. Unknown substantive classification stops approval until resolved. Late discovery loads the method first and then the feature-authoring reference when required before the boundary conclusion or final verdict. A missing required reference stops the dependent conclusion. Existing activation grammar, grandfathering behavior, projection ownership, paths, and raw-byte parity remain unchanged.

The skill retains stage-specific judgment: whether the reviewed spec has adequate applicable boundaries, interactions, invariants, outcomes, and example ownership. It does not duplicate resource tables or identifier grammar inline. Existing projection ownership, paths, and raw bytes remain unchanged.

### Asset ownership

The result and finding assets remain the only structural assets. The result asset contains one formal core, one required recording group, and three conditional groups:

| Group | Applies when | Structural fields |
| --- | --- | --- |
| Formal review core | every `spec-review` | skill, review target, review status, material finding IDs or none, blockers, immediate next stage, eventual test-spec readiness, stop condition, and claim limitations |
| Recording | every `spec-review` | recording status, recording blocker, review record, review log, and review-resolution path when applicable |
| Governed settlement | `settlement_mode: governed-spec-entry` | governed change identity, spec-entry identity, settlement result, and formal next-stage eligibility |
| Boundary review | checked boundary activation applies to the formal review | activation evidence, boundary method outcome, feature-record outcome when applicable, and unresolved boundary blocker |
| Automated review | `automation_mode: workflow-managed-automated` | authorization or manifest identity, phase receipt, pause or promotion result, correction eligibility, and rereview requirement |

Every result emits the formal review core and recording group, then adds only the governed-settlement, boundary-review, and automated-review groups selected by current evidence. Informal feedback does not use this result asset because it is outside the skill contract.

The assets own headings, labels, ordering, tables, and placeholders only. `SKILL.md` and applicable references own group applicability, field meaning, status, recording, settlement, correction, and handoff policy. Inapplicable groups are omitted rather than filled with `not-applicable`. An applicable group with unavailable required data reports an explicit `blocked` or `unknown` value and its blocker. Unfilled placeholders are forbidden, and no additional asset is introduced.

### Conflict and failure behavior

A conditional reference may specialize only its activation context. It cannot override inline universal policy or another reference's contract. Any contradiction is a package defect and stops dependent work.

Missing or unreadable recording procedure stops required recording or settlement but does not erase the review judgment or complete findings. Missing required boundary procedure stops the dependent boundary conclusion. An untriggered resource does not load and does not block ordinary review. The skill never reconstructs missing procedure from memory.

### Preservation and measurement

Before moving prose, create separate change-local ledgers for semantic rules and literal dependencies. Semantic dispositions must account for every significant rule as retained inline, retained in the recording reference, retained in an existing boundary reference, asset-owned, removed duplicate, or removed only with an approved contract change. Literal dependencies must be classified as normative contract, parser/package contract, incidental test, or obsolete. Incidental tests must not become capitalization or prose-policy owners.

Measure LF-normalized canonical resources using UTF-8 bytes and Unicode whitespace-separated words. Report every resource and these assemblies separately:

| Measurement profile | Loaded resources |
| --- | --- |
| `SR1-isolated-formal` | Core plus recording-and-settlement reference |
| `SR1B-isolated-formal-boundary` | Core, recording reference, and applicable boundary resources |
| `SR1-governed-manual` | The formal resource assembly evaluated under governed settlement authority |
| `SR1-governed-automated` | The formal resource assembly evaluated under workflow-managed automation authority |

`SR1-isolated-formal` is the primary simplification surface because every supported direct formal `spec-review` uses it. Acceptance requires its loaded UTF-8 bytes and words to decrease from the current baseline, every behaviorally significant rule to have exactly one disposition and destination, every identified duplicate cluster to have one loaded owner, and no governing rule to remain both inline and in the recording reference except for a compact cross-reference or universal summary named in the rule ledger. Governed-manual and governed-automated profiles may share resources but are reported separately and cannot grow without an explicit semantic-preservation justification. Total package growth is reported and justified separately. A 25–40 percent `SKILL.md` reduction remains a planning target only; no fixed percentage overrides semantic or lifecycle preservation.

## Expected Behavior Changes

- Informal feedback is routed outside `spec-review` and creates no `spec-review` profile or result variant.
- Every supported direct or governed formal spec review loads the recording-and-settlement reference, while settlement and automation remain separately authorized.
- Boundary-first reviews load only the existing boundary resources required by their active context.
- Review outcomes, finding rigor, routing, readiness, recording duties, settlement authority, and workflow ownership remain unchanged.
- Missing required resources fail safely instead of causing partial or remembered procedure.

## Architecture Impact

The expected assessment is `architecture-not-required` because the existing architecture already supports mapped conditional references, structural assets, projected boundary resources, canonical source ownership, and package parity. The change adds no runtime, state, dependency, service, or lifecycle owner.

A bounded architecture documentation update is required only if the current package inventory presents `spec-review` as permanently limited to its existing resources. A new ADR is required only if specification changes the normative published-package model or gives the new reference independent authority. If implementation requires such an architecture change, this change owns and reviews the architecture document rather than treating architecture as an external prerequisite.

## Testing and Verification Strategy

Use three proof classes:

1. Deterministic structure and package proof for frontmatter, required inline sections, closed values, resource-map syntax, mapped resource existence, projection identity, placeholders, canonical/generated/archive/install parity, and missing-resource failure.
2. Static scenario fixtures for informal feedback routing outside `spec-review`; isolated clean formal review with formal core and recording group; isolated formal material finding; governed manual review with settlement group; governed automated review with automation group; boundary-enabled formal review; each permitted recording-root shape; forbidden governed mutations; blocked location without downgrade; grandfathered non-substantive revision; potentially substantive revision; formal boundary record; late activation; ambiguous identity; stale authorization; retry; and invalid axis combinations.
3. Independent semantic review of the final package against the rule-disposition and literal-compatibility ledgers.

Do not execute Codex, Claude Code, opencode, or another target-agent runtime. Do not add prompt journeys, transcript grading, model fixtures, permanent simplicity validators, tokenizer dependencies, or a new validator family. Extend existing skill, review-artifact, boundary, build, and adapter proof owners only when permanent contract coverage is genuinely missing.

## Rollout and Rollback

Roll out the canonical `SKILL.md`, new reference, unchanged or deliberately updated assets, directly coupled contract consumers, and generated package inventory as one reviewed revision. Validate all mapped resources before distribution and fail partial or mixed resource versions.

Rollback restores the complete previous canonical package and coupled consumers, then rebuilds and validates derived packages. Existing durable review records require no data migration because review schema and lifecycle state do not change.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Universal policy is hidden behind the recording reference. | Closed inline ownership list, rule ledger, semantic review, and isolated-formal fixtures. |
| Older `SFA-R6` wording is violated or silently ignored. | Amend it explicitly to distinguish inline obligations from conditional mechanics. |
| Boundary-first compatibility is weakened. | Consume the existing checked-revision activation decision, preserve the compact scan, exact load order, reference paths, projection manifest, grandfathering, and raw-byte parity. |
| Resource triggers become ambiguous. | One formal invocation model, two resource profiles, closed authority axes, and fail-safe ambiguity behavior. |
| Automation gains authority through resource loading. | Separate loaded profiles from authority modes; automation requires current same-change formal authority. |
| Relocation is misreported as deletion. | Report profile and total-package measurements separately. |
| Tests freeze incidental wording. | Separate semantic and literal ledgers; migrate incidental consumers rather than preserving accidental prose. |
| Package growth outweighs direct benefit. | Require lower words and bytes for `SR1-isolated-formal`, one loaded owner per duplicate cluster, and separate explanations for governed profiles and total-package change. |

## Open Questions

None. The specification must inventory exact current consumers and requirement IDs, but it should not reopen the selected package shape, ownership split, predicate implications, proof boundary, or non-normative size target without new contradictory evidence.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-12 | Select one new recording-and-settlement reference and retain the two existing boundary references. | These are the actual conditional procedure boundaries; more references would fragment authority. | Unchanged, inline-only, boundary-only extraction, many-reference split, shared engine |
| 2026-08-12 | Preserve universal obligations and the compact boundary scan inline. | Existing contracts require them and direct review must remain safe without optional procedure. | Moving all recording or boundary policy out of `SKILL.md` |
| 2026-08-12 | Keep target-runtime execution outside acceptance. | Static contract, package, and semantic proof are deterministic and proportionate. | Agent journeys and transcript grading |
| 2026-08-12 | Treat size reduction as evidence rather than a hard percentage. | Semantic preservation must not be traded for numerical optimization. | Permanent line, token, or prose-quality gates |
| 2026-08-12 | Separate formal recording, governed settlement, and automation authority. | Every supported formal review records evidence, while only exact same-change governed authority permits settlement or automation. | One broad durable/formal predicate |
| 2026-08-12 | Consume the existing checked-revision boundary activation contract. | Simplification must not create a second activation or grandfathering owner. | Local boundary activation predicates |
| 2026-08-12 | Treat every `spec-review` invocation as formal and route informal critique elsewhere. | An informal profile adds classification, output, and boundary complexity outside the skill's lifecycle responsibility. | Non-formal feedback profiles and independent recording mode |
| 2026-08-12 | Reuse `R31a`–`R31n`, `R4h`–`R4l`, and `R24`–`R26` for isolated recording. | The simplification must preserve the exact existing selection and artifact contract without creating governed authority. | New placement or root model |
| 2026-08-12 | Make `SR1-isolated-formal` reduction normative. | Main-file reduction alone can relocate the context loaded by every direct formal review. | `SKILL.md`-only acceptance |
| 2026-08-12 | Keep one formal result core, required recording group, and three conditional groups in the existing asset. | A formal-only skill needs no alternative feedback core, and assets remain structural. | Multiple cores or a second asset |

## Next Artifacts

- Formal `proposal-review` evidence and settlement.
- If approved, a focused spec or amendment covering the `spec-review` package contract and directly coupled older clauses.
- Bounded architecture assessment, followed by architecture work only if that assessment requires it.
- Execution plan and test specification before implementation.

## Follow-on Artifacts

None yet.

## Readiness

Ready for independent `proposal-review`. This proposal does not claim acceptance, specification readiness, implementation readiness, verification, branch readiness, or PR readiness.
