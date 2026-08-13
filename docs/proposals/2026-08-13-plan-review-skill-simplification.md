# Plan-Review Skill Simplification

## Owning change record

`docs/changes/2026-08-13-plan-review-skill-simplification/change.yaml`

## Problem

The published `plan-review` skill is rigorous but mixes ordinary plan-quality judgment with exact governed settlement, reviewed-plan initialization handoff, workflow-managed automation, repeated formal-recording structure, and a large inline output template. Its 211-line, 1,877-word `SKILL.md` is smaller than several recently simplified review skills, yet every invocation still loads lifecycle mechanics that only apply when a valid governed plan entry exists.

The recently merged plan-skill simplification makes this boundary more important. `plan-review` now has two distinct governed operations: an initial semantic review that records clean evidence before `planned_work` exists, and an identical settlement retry that reuses the original judgment after matching plan-owned initialization. Keeping both operations embedded in the universal review path increases scan cost and makes it easier to confuse clean judgment, initialization readiness, lifecycle settlement, and workflow continuation.

The skill also maintains its result and material-finding structure inline while other optimized review-family skills use structural assets. That duplicates stable field labels and makes it harder to keep policy ownership separate from output layout. The optimization must preserve plan-quality rigor, every formal-review recording obligation, direct-review isolation, exact identity checks, the reviewed-plan transaction, boundary-first review, automation limits, and truthful handoff claims.

## Goals

- Make ordinary plan review shorter and easier to scan without weakening source alignment, milestone quality, sequencing, validation, recovery, architecture alignment, or maintainability judgment.
- Keep `SKILL.md` self-sufficient for formal portable review, recording obligations, plan-quality judgment, status selection, material findings, isolation, stops, claims, and resource selection.
- Give exact governed plan-entry review and settlement procedure one conditional owner.
- Distinguish initial semantic review from identical settlement retry without allowing the retry to rerun or replace judgment.
- Add one result asset and one material-finding asset as structural owners while keeping status, applicability, settlement, and handoff policy in procedure.
- Preserve the existing checked boundary-first reference and compact inline scan.
- Measure portable and governed procedural profiles separately from structural assets and total package size.
- Prove semantic preservation, literal compatibility, state-transition safety, and package parity without executing a target-agent runtime or adding permanent simplicity machinery.

## Non-goals

- Do not change what makes an execution plan acceptable, add a new review status, weaken formal-review recording, or authorize implementation from a clean plan review.
- Do not change the reviewed-plan initialization and settlement transaction approved by the plan-skill simplification; this change packages and clarifies that existing contract.
- Do not let `plan-review` initialize or modify `planned_work`, advance workflow routing, edit the reviewed plan, or own automation state.
- Do not optimize `plan`, `test-spec`, `workflow`, or another skill except for directly coupled contract, validator, or package surfaces required by this change.
- Do not add a generic review engine, scheduler, state store, new lifecycle stage, target-agent journey, transcript grader, tokenizer dependency, prose-quality score, or permanent size gate.
- Do not add more than one new procedural reference or more than the two review-family structural assets.

## Vision fit

fits the current vision

The change makes plan review easier for humans and agents to inspect while preserving durable evidence, exact lifecycle authority, resumability, and the traceable handoff from plan judgment to test specification.

## Context

The current package contains `SKILL.md` and the shared boundary-first reference:

| Resource | Lines | Words | UTF-8 bytes | Current role |
| --- | ---: | ---: | ---: | --- |
| `SKILL.md` | 211 | 1,877 | 13,619 | Universal plan judgment, formal recording, governed settlement, automation, boundary bridge, handoff, and output template |
| `boundary-first-method-v1.md` | 110 | 857 | 6,346 | Shared detailed boundary vocabulary and review method |
| Complete package | 321 | 2,734 | 19,965 | Current maintenance and distribution footprint |

Every explicit `plan-review` invocation remains a supported formal review. Portable formal review therefore keeps concise recording obligations inline: select the recording root through the existing formal-review location contract, record a clean receipt or detailed findings, synchronize `review-log.md`, create `review-resolution.md` only when triggered, and report blocked recording when no safe location exists. The optimization does not create a non-formal feedback mode inside `plan-review` and does not hide universal recording safety behind governed settlement.

The merged lifecycle contract already defines the evidence-initialization-settlement transaction. Initial clean review records the exact reviewed revision and leaves the plan `review-required` while `planned_work` is absent. Plan later initializes only missing state from that exact review basis. Workflow then coordinates an identical `plan-review` retry, and only that retry may activate the matching plan entry. This proposal treats that transaction as governing authority rather than reopening it.

The existing review-family assets provide a proven structural pattern, but `plan-review` is not yet included in the validator's first-slice asset family. Adding the two assets therefore requires a bounded extension of existing review-family validation, including byte-identical parser-owned material-finding fields and plan-review-specific result labels. Tests and validators remain contract projections rather than prose-policy owners.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Identify the best solution for optimizing `plan-review`. | in scope | Options Considered and Recommended Direction |
| Create a new branch. | in scope | Change-local authoring evidence |
| Create a proposal. | in scope | This artifact |
| Run independent proposal review. | in scope | Next Artifacts and formal review evidence |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Simplify universal plan-quality review. | core to this proposal | Primary user-visible objective |
| Add one governed review-and-settlement reference. | core to this proposal | Removes exact change-record procedure from portable review |
| Add result and material-finding assets. | same-slice dependency | Removes duplicated output structure and aligns review-family ownership |
| Preserve checked boundary-first loading. | same-slice dependency | Boundary activation and package parity are compatibility surfaces |
| Preserve the reviewed-plan transaction. | same-slice dependency | The new reference must encode the merged lifecycle contract exactly |
| Extend existing review-family asset validation to `plan-review`. | same-slice dependency | Required to make the two new assets safe and parser-compatible |
| Add change-local preservation, scenario, and measurement evidence. | same-slice dependency | Required to prove simplification without permanent policy |
| Optimize adjacent skills or redesign lifecycle automation. | out of scope | Those changes require separate ownership and evidence |

## Options Considered

### Option 0: Keep the package unchanged

This avoids migration work but leaves governed settlement, automation, and output structure in every invocation and keeps `plan-review` inconsistent with optimized review-family packaging.

### Option 1: Editorial consolidation only

This can remove repeated prose and shorten the main file with minimal package change. It cannot keep portable review from loading exact `change.yaml`, initialization-basis, settlement-retry, and automation procedure.

### Option 2: Add structural assets but keep all procedure inline

This gives output fields one owner and reduces template duplication. It leaves the main context dominated by governed state procedure and does not clarify the initial-review versus settlement-retry boundary.

### Option 3: Add one governed procedure reference and two structural assets

This keeps portable formal review, plan judgment, recording safety, and classification inline; moves exact governed mutation and automation procedure behind an evidence-based trigger; retains the existing boundary reference; and adopts the proven review-family asset model. It adds three resources at two real ownership boundaries while avoiding procedure fragmentation.

### Option 4: Split formal recording, governed settlement, automation, and retry into separate references

This could reduce some specialized assemblies further, but every formal review needs recording and every governed retry depends on the same identity and settlement contract. Multiple references would create overlapping triggers and navigation cost disproportionate to the current 1,877-word file.

### Option 5: Replace review prose with a generic executable review engine

This could enforce deterministic state transitions but cannot own semantic plan-quality judgment and would add runtime and policy machinery outside the simplification goal.

## Recommended Direction

Adopt Option 3.

The target package is:

```text
skills/plan-review/
├── SKILL.md
├── assets/
│   ├── review-result-skeleton.md
│   └── material-finding.md
└── references/
    ├── governed-plan-review-settlement.md
    └── boundary-first-method-v1.md
```

### Invocation and operation classification

Every explicit `plan-review` invocation is a formal review. Determine the operation from complete current transaction state before semantic judgment or writes:

```text
initial-review
settlement-retry
```

`initial-review` is valid only when the current plan revision is reviewable, the matching plan entry is `review-required` where governed, required authoring evidence is current, `planned_work` is absent, and no current clean review exists for the exact plan path, content identity, and repository revision tuple. It performs semantic plan judgment and records one new review occurrence.

Once one exact current clean review exists for that tuple, every later invocation is `settlement-retry`, including while `planned_work` remains absent. A retry reuses the existing judgment and record without semantic rereview. A changed plan identity makes the prior review stale and requires a fresh `initial-review`; multiple matching reviews or initialization bases, an open review resolution, `planned_work` without one valid current clean review, mismatched initialization basis, or other contradictory state blocks before writes. This classification prevents duplicate clean reviews while plan-owned initialization is pending.

Classify a load-only predicate before validating settlement authority:

```text
governed_plan_candidate_context
```

`governed_plan_candidate_context` is true when an explicit change ID, reviewed-plan metadata, a current workflow-managed plan-review request, or an identical settlement-retry request identifies a governed change candidate. The predicate only selects the governed reference. It does not establish a valid plan entry, legal state, settlement authority, or workflow continuation.

After loading the governed reference, validate exactly one outcome:

```text
validated-governed-plan-entry
invalid-governed-candidate
```

`validated-governed-plan-entry` requires one exact current change, valid lifecycle marker, one matching plan entry, legal plan state, complete authoring evidence for initial review or matching initialization basis for retry, and the current reviewed revision. `invalid-governed-candidate` stops without governed mutation or portable fallback. A request with no governed candidate uses portable formal recording. Late candidate discovery loads and validates the reference before dependent recording-location selection, judgment completion, status, write, or handoff claims.

Classify governed settlement and execution authority independently:

```text
settlement_mode:
  isolated-recording
  governed-plan-entry

execution_mode:
  manual
  workflow-managed
```

`isolated-recording` writes required formal review evidence but cannot settle a plan entry or report governed next-stage eligibility. `governed-plan-entry` is selected only after the governed reference establishes `validated-governed-plan-entry`. `workflow-managed` additionally requires current same-change authorization, but it does not enlarge the plan-review write set. Loading a resource or detecting a candidate never grants settlement or continuation authority.

Keep semantic review status separate from lifecycle transaction result. Review status remains exactly `approved`, `changes-requested`, `blocked`, or `inconclusive`. Transaction result is exactly `recorded-isolated`, `initialization-required`, `revision-required`, `blocked`, `settled-active`, or `not-settled`.

Use this closed matrix:

| Operation and context | Review status | Recording behavior | Plan entry result | Transaction result | Immediate action or handoff |
| --- | --- | --- | --- | --- | --- |
| Portable `initial-review`, clean | `approved` | Create one clean receipt and log entry. | none | `recorded-isolated` | Report `test-spec` only as a possible next stage; no formal eligibility. |
| Governed `initial-review`, clean, `planned_work` absent | `approved` | Create one clean receipt and review mapping. | remain `review-required` | `initialization-required` | Plan-owned initialization; withhold `test-spec` eligibility. |
| Governed `initial-review`, material actionable findings | `changes-requested` | Create detailed record, log, and required resolution. | `revision-required` | `revision-required` | Plan revision. |
| Governed `initial-review`, blocking result | `blocked` | Create detailed record, log, and required resolution before settlement. | `blocked` after recording succeeds | `blocked` | Resolve the blocker through its owner. |
| Governed `initial-review`, insufficient evidence | `inconclusive` | Record the formal result when possible. | remain `review-required` | `blocked` with `review-inconclusive` reason | Supply authority or evidence before another review. |
| Any `initial-review` with blocked required recording | judgment may be returned | Report paths as blocked and create no settlement. | unchanged | `not-settled` | Repair recording before formal completion. |
| Exact `settlement-retry`, `planned_work` absent | reuse prior `approved` | Reuse the existing receipt, review mapping, and log entry; create no new review evidence. | remain `review-required` | `initialization-required` | Plan-owned initialization. |
| Exact `settlement-retry`, matching `planned_work`, entry `review-required` | reuse prior `approved` | Reuse existing evidence; create no new review evidence. | compare-and-set to `active` | `settled-active` | `test-spec` becomes formally eligible; return control to workflow when managed. |
| Exact `settlement-retry`, matching `planned_work`, entry already `active` | reuse prior `approved` | Reuse existing evidence; create no new review evidence. | remain `active`; no write | `settled-active` | Report idempotent success with `state_changed: false`. |
| Changed plan identity after prior review | no reused status | Create no retry evidence. | unchanged | `blocked` | Perform a fresh `initial-review` for the changed revision. |
| Mismatched basis, multiple matching reviews or bases, open resolution, or `planned_work` without clean review | no new review status unless one exact prior judgment is safely resolved | Create no new review evidence. | unchanged | `blocked` | Correct the contradictory or ambiguous state through its owner. |

A settlement retry never performs semantic rereview, creates another receipt, finding set, resolution entry, or review-log entry, changes the prior review ID or round, initializes or modifies `planned_work`, or advances workflow routing. It may validate and settle only the exact matching plan entry. Retry success with an already-active exact entry is idempotent and creates no receipt, log entry, resolution entry, workflow transition, or other duplicate evidence.

### Loaded-resource profiles

Use four procedural assemblies:

| Profile | Governed candidate | Boundary detail | Loaded procedure |
| --- | ---: | ---: | --- |
| `PRV0-portable` | no | no | `SKILL.md` |
| `PRV0B-portable-boundary` | no | yes | `SKILL.md` plus boundary reference |
| `PRV1-governed` | yes | no | `SKILL.md` plus governed reference; then validate authority or stop |
| `PRV1B-governed-boundary` | yes | yes | `SKILL.md` plus both references; then validate authority or stop |

The initial-review and settlement-retry operations may use the same governed resource assembly but have different allowed semantic work and writes. Profiles describe loaded resources; operation, settlement mode, and execution mode describe authority. Assets are copied output resources and are measured separately.

Late discovery of governed-candidate or boundary context loads the required reference before dependent interpretation, recording-location selection, write, status, or handoff claim. A failed governed candidate does not reclassify as portable. Missing, unreadable, escaped, contradictory, or mixed-version required resources stop dependent work without reconstruction from memory.

### Universal `SKILL.md` ownership

Keep inline:

- purpose, trigger, workflow role, near-miss routing, and customer-project portability;
- review target, original plan identity, source precedence, and bounded evidence access;
- exact operation, governed-candidate, settlement-mode, execution-mode, review-status, and transaction-result classification;
- plan-quality dimensions covering context, source alignment, milestone size, sequencing, scope, dependencies, validation, TDD readiness, recovery, architecture, risk, operations, and maintainability;
- materiality, severity, review status, and plan readiness meanings;
- concise formal recording location, clean receipt, detailed finding, review-log, review-resolution, and blocked-recording obligations;
- the rule that isolation stops continuation but never suppresses required recording;
- the compact four-question boundary scan and exact reference triggers;
- universal stops, claims, status-to-handoff behavior, and the distinction between immediate `test-spec` handoff and downstream implementation readiness;
- the structural-asset applicability rules and concise expected-output instruction.

The universal file remains sufficient to perform and record a portable formal plan review. It does not need exact governed plan-entry mutation procedure.

### Governed reference ownership

`references/governed-plan-review-settlement.md` loads exactly when `governed_plan_candidate_context` is true. It first validates `validated-governed-plan-entry` or stops as `invalid-governed-candidate`; only the validated result can select `governed-plan-entry`. It owns:

- complete `change.yaml` inspection, candidate validation, and exact plan-entry resolution by artifact ID, kind, role, normalized path, review ID, round, record path, reviewed artifact path, and reviewed repository revision;
- initial-review preconditions, review-first durable evidence, exact review mapping, and legal mapping of non-clean statuses;
- clean initial review with absent `planned_work`, preservation of `review-required`, and `initialization-required` reporting;
- complete operation-state validation, including clean-review reuse before initialization, already-active idempotency, changed plan identity, missing clean review, duplicate bases, and open resolution;
- settlement-retry preconditions, exact initialization-basis comparison, reuse of prior judgment, and the sole matching `review-required` to `active` compare-and-set write;
- deterministic settlement retention of authoring, review, and initialization evidence as immutable historical basis evidence;
- identical interrupted-write reconciliation, concurrent-write checks, conflicting review-ID reuse, stale revision, open resolution, illegal state, and failed validation handling;
- workflow-managed review manifest and profile-completion procedure only where current workflow authority already requires it;
- fail-closed diagnostics for missing, invalid, stale, ambiguous, or contradictory candidate evidence without portable fallback.

The reference does not own plan-quality judgment, finding materiality, recording requirements, plan edits, `planned_work` initialization or mutation, workflow routing, automation target state, test-spec authoring, or implementation authorization. `plan` owns one-time initialization, `plan-review` owns judgment and matching settlement, and `workflow` owns coordination and continuation.

### Structural assets

Add `assets/review-result-skeleton.md` with one universal operation group and five applicability-controlled groups:

| Group | Applicability | Structural content |
| --- | --- | --- |
| Core operation | every formal invocation | skill, target, operation, transaction result, blockers, immediate action or handoff, claim limitations |
| Semantic judgment | an initial review performed judgment or a retry safely resolved one exact prior judgment | judgment mode `performed` or `reused`, review ID, round, reviewed plan identity, review status, material finding IDs |
| Durable recording | every formal invocation | recording status, recording blocker, review record, review log, review resolution, finding-record paths, and whether new evidence was created |
| Governed settlement | `validated-governed-plan-entry` | change identity, plan-entry identity, reviewed revision, `planned_work` basis result, entry state before and after, settlement result, state-changed flag, formal eligibility |
| Boundary review | boundary procedure loaded | active boundary and interaction IDs, boundary outcome, unresolved gap |
| Workflow-managed | current workflow-managed execution | manifest/profile identity, pause or completion result, workflow handoff |

Add `assets/material-finding.md` with the byte-identical parser-owned review-family field block. The existing review-family validator will be extended to cover `plan-review` rather than creating a new validator family.

The core operation and durable-recording groups are never omitted because every explicit `plan-review` is formal. The semantic-judgment group appears only when judgment was performed or one exact prior judgment was safely reused. An invalid retry emits `operation: settlement-retry`, transaction result `blocked`, the exact blocker, and no new review evidence; it omits semantic judgment unless one exact prior review was safely resolved. Other inapplicable groups are omitted. Applicable groups with unavailable required data report an explicit `blocked` or `unknown` value and the blocker. Unfilled placeholders are forbidden. Assets own labels and layout only; `SKILL.md` and the governed reference own applicability, status meaning, settlement, authority, and handoff.

### Deterministic settlement sequence

The governed reference uses one settlement sequence:

1. Read the complete current change record.
2. Validate the exact plan identity, clean review identity, repository revision, initialization identity, entry state, and absence of open or competing resolution.
3. Reject stale, mismatched, conflicting, ambiguous, or unsupported state before mutation.
4. If the exact matching plan entry is already `active`, return idempotent `settled-active` with `state_changed: false`.
5. Otherwise compare-and-set only the exact matching entry from `review-required` to `active`.
6. Preserve authoring, review, and initialization evidence unchanged as durable historical evidence.
7. Validate the resulting change record and report `settled-active`.

Any failure before the compare-and-set leaves state unchanged. An interruption after that write is reconciled by rereading the record and accepting only the exact active entry with the same review and initialization identities; reconciliation performs no semantic rereview and creates no duplicate record.

### Boundary-first ownership

Keep the inline four-question scan and the existing `boundary-first-method-v1.md` activation contract unchanged. Load the boundary reference only when cited approved boundary or interaction rows are missing, stale, unknown, ambiguous, conflicting, or insufficient for plan review. The boundary reference owns detailed plan-boundary analysis; the governed reference owns lifecycle review settlement. Neither reference may override universal rules or duplicate the other's contract.

### Simplification measurement

Use canonical authored files with LF-normalized content. Count Unicode whitespace-separated words and UTF-8 bytes, count each unique procedural resource once, and record file identities and assembly order.

Measure `PRV0`, `PRV0B`, `PRV1`, and `PRV1B` as procedural profiles. Report each asset and total package separately. Also report initial-review and settlement-retry semantic scenarios even when they share a loaded-resource assembly. The primary acceptance surface is both `PRV0` and `PRV1`: each should have fewer words and bytes than its current equivalent. `SKILL.md` reduction alone is insufficient, and no fixed percentage overrides semantic or lifecycle preservation.

### Semantic and literal preservation

Create separate change-local inventories for behaviorally significant rules and exact literal dependencies. Every rule receives one disposition and destination. Every literal consumer is classified as normative contract, parser/package contract, test-only incidental, obsolete, or historical fixture. Preserve real contract literals or migrate every consumer atomically; update incidental tests rather than freezing accidental prose.

## Expected Behavior Changes

- A portable formal plan review performs complete plan-quality judgment and recording without loading exact governed settlement procedure.
- An explicit governed candidate loads the reference before authority validation; an invalid candidate stops and never falls back to portable review.
- A governed initial review loads one reference, writes review evidence first, and reports `initialization-required` when live state is absent without activating the plan.
- `approved` remains the semantic review status while `initialization-required` remains a separate transaction result.
- A second invocation after an exact clean review is a settlement retry even before initialization; it reuses the review and reports `initialization-required` without duplicate semantic evidence.
- A matching settlement retry activates only the exact plan entry after matching initialization, while an already-active exact entry returns idempotent success without another write.
- A retry with stale, contradictory, ambiguous, or unresolved evidence blocks without manufacturing a semantic review status.
- Settlement retains authoring, review, and initialization evidence and converges on one identity-bound final state.
- Direct and isolated review never advances routing, even when formal settlement is permitted.
- Workflow-managed review records only its current manifest/profile evidence and returns control to workflow; it does not start `test-spec` or implementation.
- Review results and material findings use the two mapped assets, omitting inapplicable groups and forbidding empty placeholders.
- Missing triggered resources stop dependent review or settlement safely.

## Architecture Impact

The expected architecture assessment is `architecture-not-required`. The existing architecture already defines published skills as canonical `SKILL.md` plus mapped references and assets, raw-byte resource parity, stage-owned review settlement, the reviewed-plan initialization transaction, and `change.yaml` as mutable lifecycle owner.

A bounded assessment is still required after specification review. If current architecture contains a flat `plan-review` package inventory, update that example or pointer without creating a new design decision. A new ADR is warranted only if specification changes the reviewed-plan transaction, package model, lifecycle ownership, or persistent state. Mutable architecture-assessment status and artifact pointers belong only in this change's `change.yaml`; stable design rationale remains in architecture artifacts.

## Testing and Verification Strategy

Use three proof classes:

1. Deterministic structural and package proof for frontmatter, required headings, Resource map verbs, reference and asset existence, path containment, closed vocabularies, placeholder absence, review-family asset parity, generated resources, archives, and clean-installed parity.
2. Static contract scenarios for absent, valid, stale, ambiguous, conflicting, and late-discovered governed candidates; portable and governed initial review; every row in the closed review-status and transaction-result matrix; blocked recording; clean review with absent initialization; matching initialization; already-active idempotent retry; changed plan identity; duplicate reviews or bases; open resolution; `planned_work` without clean review; blocked and inconclusive outcomes; invalid-retry judgment omission; retained basis evidence; pre-write failure; interrupted-write reconciliation; boundary loading; isolated execution; workflow-managed execution; missing resources; and forbidden writes.
3. Independent semantic review of the final package against the rule ledger, literal inventory, governing lifecycle contract, and current skill behavior.

Do not execute Codex, Claude Code, opencode, or another target-agent runtime for acceptance. Do not add prompt journeys, transcript grading, model-version evidence, a permanent token budget, or a new validator family. Words and bytes are required metrics; token estimates are optional only when an existing pinned repository-owned implementation already supports the exact assemblies.

## Rollout and Rollback

Implement atomically in canonical `skills/`: add the governed reference and two assets, rewrite `SKILL.md`, extend existing review-family validation, update directly coupled contracts and fixtures, regenerate derived packages, and prove canonical-through-installed parity before handoff.

Historical review records and plan artifacts remain unchanged. No data migration is expected because the lifecycle transaction and metadata shape do not change. If implementation discovers that the merged transaction must change, stop and route that decision back to specification and architecture rather than hiding it inside package simplification.

Rollback restores the previous complete canonical `plan-review` package, validator expectations, and any directly coupled contract wording together, then regenerates every derived package. Do not leave a shortened main file without its resources or assets.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Universal formal-recording safety moves behind the governed trigger. | Keep recording obligations, location fallback, clean/detailed record distinction, and blocked-recording behavior inline; cover portable formal review directly. |
| Settlement retry accidentally performs semantic rereview or replaces judgment. | Use a closed operation classification and exact review/plan/revision/initialization identity with static retry and conflict scenarios. |
| A second invocation while initialization is pending creates a duplicate clean review. | Once one exact clean review exists, classify every same-tuple invocation as settlement retry and return `initialization-required` until initialization appears. |
| An invalid retry manufactures a semantic status. | Keep transaction output universal and emit semantic judgment only when performed or safely reused. |
| Optional evidence cleanup creates divergent success states. | Retain authoring, review, and initialization evidence and use one identity-checked compare-and-set transition. |
| Loading a reference is mistaken for settlement or automation authority. | Classify resource profile, settlement mode, and execution mode independently; require exact current evidence before writes. |
| Candidate validation becomes circular or an invalid candidate falls back to portable behavior. | Use candidate evidence only to load the reference; validate authority inside it and stop invalid candidates without fallback. |
| Review status, initialization, and settlement are conflated. | Use separate closed review-status and transaction-result vocabularies with one complete outcome matrix. |
| Assets omit mandatory recording paths, become policy owners, or introduce incompatible field labels. | Require the durable-recording group for every result, limit assets to closed structural groups, extend the existing review-family validator, and keep parser-owned material fields byte-identical. |
| Main-file reduction merely relocates content. | Require both portable and governed procedural profiles to shrink and report assets and total package separately. |
| Boundary-first behavior drifts. | Preserve the existing trigger and reference unchanged unless exact parity metadata requires regeneration; test false, true, late, and missing-resource cases. |
| Tests freeze accidental prose. | Separate semantic-rule and literal-dependency inventories and classify exact consumers before editing. |
| Package rollout is partial. | Require canonical, generated, archived, and clean-installed resource parity and fail closed on mixed versions. |

## Open Questions

None. The downstream specification should inventory exact compatibility-sensitive literals and existing validator consumers before editing, but the ownership and acceptance decisions are closed here.

## Acceptance Criteria

| ID | Criterion |
| --- | --- |
| `AC-PRVSIM-001` | An exact current clean review prevents duplicate semantic rereview of the same plan revision. |
| `AC-PRVSIM-002` | A settlement retry returns `initialization-required` while `planned_work` remains absent. |
| `AC-PRVSIM-003` | Matching initialized state and `review-required` settle exactly one plan entry. |
| `AC-PRVSIM-004` | An already-active matching entry returns idempotent `settled-active` with no duplicate write or evidence. |
| `AC-PRVSIM-005` | `planned_work` without one valid current clean review fails closed. |
| `AC-PRVSIM-006` | Multiple matching review or initialization bases fail closed. |
| `AC-PRVSIM-007` | `blocked` and `inconclusive` produce distinct deterministic plan-entry effects. |
| `AC-PRVSIM-008` | Review status is emitted only for a performed or safely reused semantic judgment. |
| `AC-PRVSIM-009` | An invalid settlement retry does not manufacture a review status. |
| `AC-PRVSIM-010` | Operation result and semantic judgment use separate result-asset groups. |
| `AC-PRVSIM-011` | Settlement retry has one deterministic final evidence state. |
| `AC-PRVSIM-012` | Authoring, review, and initialization evidence remains durable after settlement. |
| `AC-PRVSIM-013` | Retry creates no duplicate review, log, resolution, finding, receipt, or workflow-transition records. |
| `AC-PRVSIM-014` | Missing or conflicting required resources and identities stop before writes. |
| `AC-PRVSIM-015` | Portable and governed loaded profiles both decrease from their baselines. |
| `AC-PRVSIM-016` | No target-agent runtime executes during acceptance. |

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-13 | Use one conditional governed review-and-settlement reference. | Exact plan-entry inspection and retry form one authority boundary, while portable recording remains universal. | Inline-only procedure and multiple fragmented references. |
| 2026-08-13 | Distinguish `initial-review` from `settlement-retry`. | The merged lifecycle transaction requires judgment reuse and exact retry behavior. | Treat every invocation as a fresh semantic review. |
| 2026-08-13 | Add the two standard review-family assets. | Stable output structure should have one owner and not inflate procedural prose. | Keep the inline template or add stage-specific duplicate structures. |
| 2026-08-13 | Measure portable and governed procedural profiles separately from assets. | Main-file size and total-package size alone do not prove invocation-context improvement. | Fixed percentage or `SKILL.md`-only acceptance. |
| 2026-08-13 | Expect `architecture-not-required` after bounded assessment. | The package and reviewed-plan transaction already have approved architecture. | Skip assessment or create a new ADR preemptively. |
| 2026-08-13 | Use candidate-trigger loading followed by reference-owned authority validation. | The resource trigger must not depend on validation owned by the triggered resource. | Validate the complete governed contract inline or fall back after failed validation. |
| 2026-08-13 | Separate semantic review status from lifecycle transaction result. | `approved`, `initialization-required`, and `settled-active` are different claims with different effects. | Add another review status or infer handoff from approval alone. |
| 2026-08-13 | Require a durable-recording asset group for every result. | Every explicit plan review is formal and must report recording paths or blocked states. | Keep recording fields inline or omit them from portable results. |
| 2026-08-13 | Select retry from complete transaction state once an exact clean review exists. | Initialization delay must not cause duplicate semantic review. | Require initialization before retry classification or rerun review while pending. |
| 2026-08-13 | Separate universal operation output from conditional semantic judgment. | Invalid retries are transaction failures, not new plan-quality verdicts. | Require review status in every result or add a fifth non-review status. |
| 2026-08-13 | Retain all authoring, review, and initialization basis evidence after settlement. | One immutable evidence policy makes settlement deterministic, auditable, and idempotent. | Optional or mandatory evidence deletion during settlement. |

## Next Artifacts

- Independent `proposal-review`.
- Focused feature specification and `spec-review` after proposal acceptance.
- Bounded architecture assessment recorded in the owning change record.
- Execution plan, plan review, test specification, and test-spec review before implementation.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent `proposal-review`. This proposal does not claim acceptance, specification readiness, implementation readiness, verification, branch readiness, or PR readiness.
