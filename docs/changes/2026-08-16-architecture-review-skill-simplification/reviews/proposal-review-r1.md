# Proposal Review: Architecture Review Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-16-architecture-review-skill-simplification.md`

Reviewed artifact: `docs/proposals/2026-08-16-architecture-review-skill-simplification.md` at commit `58d39a5e`
Review date: 2026-08-16
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: ARRSIM-PR1, ARRSIM-PR2, ARRSIM-PR3
- Open blockers: shared recording-block ownership, valid mode combinations, and record-only versus artifact-settlement authority require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, complete architecture assessment, or continue the workflow

## Overall assessment

The proposal selects the right package direction: a compact universal review contract, one conditional architecture-package review reference, one conditional recording-and-settlement reference, and no new runtime or structural asset. The references correspond to real method-depth and durable-side-effect boundaries rather than arbitrary prose fragments.

The proposal also protects important invariants. It retains the accepted four review surfaces, keeps core evidence and claim safety inline, separates semantic judgment from recording and settlement, treats loaded resources as procedure rather than authority, measures real formal profiles, and excludes target-agent acceptance and a new manual semantic gate.

Three contracts remain incomplete. The formal-review specification requires a byte-identical shared recording subsection to remain inline, but the proposal does not classify that normative literal against the new reference owner. The four independent mode axes lack an exhaustive valid-combination and write matrix. Finally, record-only surfaces contain an exception that could invent settlement authority, while artifact-bearing multi-target settlement does not close exact per-kind state mapping and partial retry behavior.

## What is strong

### Progressive disclosure follows real review boundaries

No-impact and upstream-gap review do not need the complete C4, arc42, diagram, and ADR checklist. Package-method procedure and durable recording procedure are independently triggered, which supports both lighter review and clearer ownership.

### Universal safety remains inline

Target identity, evidence precedence, four-surface classification, spec alignment, materiality, statuses, no-impact credibility, upstream routing, stops, claims, and resource triggers remain available before optional resources load.

### Existing architecture semantics are preserved

The proposal does not reopen the C4 plus arc42 plus ADR method, restore change-local deltas, move product direction into architecture-review, or introduce partial semantic approval.

### Measurement and acceptance are honest

The proposal identifies formal isolated and governed profiles as primary evidence, reports total package size separately, and does not present a shorter main file as sufficient proof.

## Material findings

### ARRSIM-PR1 — Major: the recording-reference boundary conflicts with the normative shared inline subsection

Finding ID: ARRSIM-PR1
Severity: major
Location: `Recommended Direction` sections `Universal SKILL.md ownership` and `architecture-review-recording-and-settlement.md ownership`
Evidence: `specs/formal-review-recording.md` R21 through R21d require proposal-review, spec-review, architecture-review, plan-review, and code-review to contain one identical `## Isolation and Recording` subsection copied from `templates/shared/review-isolation-and-recording.md`, with static byte-for-byte validation. The proposal assigns durable-recording trigger classification and isolation to the main file and detailed recording mechanics to the reference, but it does not identify the required shared block as a normative inline literal or define which sentences may move without breaking shared-block parity. The specification could therefore remove or rewrite required inline text while claiming one-owner cleanup.
Required outcome: Preserve the exact shared `## Isolation and Recording` block inline, classify it as a normative cross-skill literal, and define the recording reference as owning only stage-specific procedure outside that shared block.
Safe resolution path: Add a shared-block compatibility section and acceptance criteria. Require pre-edit byte comparison against `templates/shared/review-isolation-and-recording.md`; keep the block unchanged unless the formal-review recording spec and every consuming review skill are amended atomically; move only architecture-review-specific location, target, settlement, retry, and automation procedure to the reference.
needs-decision rationale: none; the two-reference design remains valid after closing the existing normative literal boundary.

### ARRSIM-PR2 — Major: independent mode axes lack an exhaustive valid-combination and side-effect matrix

Finding ID: ARRSIM-PR2
Severity: major
Location: `Recommended Direction` section `Independent classification axes`
Evidence: The proposal defines recording modes `none`, `advisory-durable`, and `formal-lifecycle`; settlement modes `isolated` and `governed`; and automation modes `manual` and `workflow-managed-automated`. It declares only that automated mode requires formal governed authority. It does not decide whether `none/governed/manual`, `advisory-durable/governed/manual`, or other non-automated combinations are valid, nor does it enumerate which combinations may write a review record, review log, review resolution, architecture or ADR review mapping, automation packet, or handoff evidence. Saying unknown or contradictory classifications stop does not define which known combinations are contradictory.
Required outcome: Define every valid recording, settlement, and automation combination and its exact permitted writes and handoff behavior; declare every other combination invalid.
Safe resolution path: Use a closed matrix with `none/isolated/manual`, `advisory-durable/isolated/manual`, `formal-lifecycle/isolated/manual`, `formal-lifecycle/governed/manual`, and `formal-lifecycle/governed/workflow-managed-automated` as the only candidate combinations. Confirm whether all five are truly needed, then assign review-record, log, resolution, lifecycle-settlement, automation-evidence, and continuation permissions explicitly. Package loading remains independent from this authority matrix.
needs-decision rationale: none; this is a proposal contract needed to prevent the later specification from inventing write authority.

### ARRSIM-PR3 — Major: record-only surfaces and artifact-target settlement do not have one closed authority rule

Finding ID: ARRSIM-PR3
Severity: major
Location: `Recommended Direction` sections `Exact target and review-occurrence identity` and `Judgment, recording, and settlement results`
Evidence: The proposal says no-impact rationale and proposal/spec-gap review are record-only unless an existing governed artifact entry explicitly represents the rationale. It does not identify an approved artifact kind, lifecycle state, or owning contract for that exception, so a specification could invent an architecture entry merely to settle a rationale. For artifact-bearing reviews, the proposal binds an ordered target set and one semantic status but leaves the exact architecture and ADR lifecycle mappings in the future reference, including how the ADR choice between `accepted` and `active` is resolved and how an interrupted subset differs from semantic partial approval.
Required outcome: Make record-only surfaces unconditionally non-settling in this first version and define the exact existing source for every artifact-bearing settlement state and partial-retry result.
Safe resolution path: State that `no-architecture-impact-rationale` and `proposal-or-spec-gap` create review evidence only and never settle architecture or ADR entries; workflow remains the owner of assessment and routing. Limit artifact settlement to exact canonical architecture and ADR entries already in `review-required` with complete matching authoring evidence. Map architecture approval to `approved`; obtain the intended ADR settlement state from one exact existing authoring or lifecycle field and block if it is absent or ambiguous; map non-approval outcomes using the existing contract. Treat subset completion only as an interrupted physical settlement requiring an identical retry, never as partial semantic approval or downstream eligibility.
needs-decision rationale: none; the proposal can preserve existing ownership without adding a rationale artifact type or new lifecycle state.

## Architecture assessment

The expected bounded result remains `architecture-not-required` if the revision preserves the current shared recording contract, uses existing artifact entries and authoring evidence for settlement, and introduces no new rationale artifact or multi-target transaction state.

Architecture becomes required if the resolution adds a new persisted review transaction, rationale artifact kind, lifecycle state, schema, or write owner. The proposal should retain that condition explicitly.

## Acceptance criteria to add

| ID | Criterion |
| --- | --- |
| `AC-ARRSIM-001` | The exact shared `Isolation and Recording` subsection remains inline and byte-identical to its normative template. |
| `AC-ARRSIM-002` | Architecture-review-specific recording procedure has one owner outside the shared block. |
| `AC-ARRSIM-003` | Recording, settlement, and automation modes have one exhaustive valid-combination matrix. |
| `AC-ARRSIM-004` | Every valid mode combination has explicit allowed writes and handoff behavior. |
| `AC-ARRSIM-005` | Every unlisted mode combination stops before dependent writes or claims. |
| `AC-ARRSIM-006` | No-impact and proposal/spec-gap surfaces never create or settle architecture or ADR entries. |
| `AC-ARRSIM-007` | Governed artifact settlement requires exact existing review-required entries and matching authoring evidence. |
| `AC-ARRSIM-008` | Architecture and ADR approval states resolve deterministically from existing authority. |
| `AC-ARRSIM-009` | Partial physical settlement is retry-only and never becomes partial semantic approval or handoff eligibility. |
| `AC-ARRSIM-010` | Primary isolated and governed formal loaded profiles decrease from baseline. |
| `AC-ARRSIM-011` | No target-agent runtime or separate manual semantic-review acceptance stage is introduced. |
| `AC-ARRSIM-012` | Canonical, generated, archived, release-candidate, and installed resources retain required parity. |

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Flat common-path method and settlement overload is concrete and measured. |
| User value | pass | No-impact, upstream-gap, and isolated review should load less irrelevant procedure. |
| Option diversity | pass | Unchanged, editorial compression, method-only extraction, two references, fragmented references, and executable routing are materially different. |
| Decision rationale | pass | Two references follow genuine semantic-method and durable-side-effect boundaries. |
| Vision fit | pass | The change improves inspectability and usability without weakening durable review evidence. |
| Scope control | pass | Method redesign, runtime machinery, new assets, schema changes, target-agent acceptance, and a manual semantic gate are excluded. |
| Universal judgment | pass | Evidence, surfaces, statuses, materiality, no-impact safety, stops, and claims remain inline. |
| Shared recording compatibility | block | The normative byte-identical inline subsection has no explicit preservation treatment. |
| Execution authority | block | Known mode values can form combinations whose writes and handoff are undefined. |
| Target settlement | block | Record-only exceptions and per-kind artifact settlement are not closed. |
| Resource failure | pass | Missing triggered method blocks verdict; missing triggered recording blocks formal completion and settlement. |
| Testing boundary | pass | Static proof, package parity, and ordinary lifecycle review are proportionate; runtime execution is excluded. |
| Measurement | pass with revisions | Real formal profiles are primary, but acceptance should name the exact profiles after the mode matrix is closed. |
| Architecture awareness | pass with revisions | No architecture work is plausible only if resolution reuses current evidence and states. |
| Readiness for spec | changes-requested | ARRSIM-PR1 through ARRSIM-PR3 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass; optimization, progressive disclosure, lifecycle safety, branch creation, governed proposal authoring, and formal review are visible and classified.

## Recommended Proposal Edits

- Recommended edits: preserve and classify the exact shared recording block; add the exhaustive valid mode and side-effect matrix; make no-impact and upstream-gap surfaces record-only without exception; close architecture and ADR settlement-state authority plus interrupted physical retry; then update profiles, risks, scenarios, and acceptance criteria before rereview.

## Recommendation

- Recommendation: revise the proposal to resolve ARRSIM-PR1 through ARRSIM-PR3, then run a new independent proposal review against the committed revision. No automatic downstream handoff follows this review.

## Specialized-gate group

- Active gate predicates: `initial_intent_table_context`, `scope_budget_context`
- Gate outcomes: pass; every initial goal and public-skill work item has a valid treatment and visible destination
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-16-architecture-review-skill-simplification/reviews/proposal-review-r1.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: proposal-review-r1
- Review record: `docs/changes/2026-08-16-architecture-review-skill-simplification/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-16-architecture-review-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-16-architecture-review-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-16-architecture-review-skill-simplification`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview
