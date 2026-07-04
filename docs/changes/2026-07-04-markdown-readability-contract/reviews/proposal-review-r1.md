# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Codex proposal-review skill
Target: docs/proposals/2026-07-04-markdown-readability-contract.md
Status: changes-requested
Original review source: User-invoked `$proposal-review` on 2026-07-04.
Material findings: MDREAD-PR1, MDREAD-PR2
Scope-preservation result: changes-requested
Immediate next stage: proposal revision
Automatic downstream handoff: none

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: MDREAD-PR1, MDREAD-PR2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-04-markdown-readability-contract/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-07-04-markdown-readability-contract/review-log.md
- Review resolution: docs/changes/2026-07-04-markdown-readability-contract/review-resolution.md#proposal-review-r1
- Open blockers: material findings require proposal revision and rereview
- Immediate next stage: proposal revision

## Material Findings

### MDREAD-PR1 - Settled owner decisions still appear as downstream choices

Finding ID: MDREAD-PR1
Severity: major
Location: docs/proposals/2026-07-04-markdown-readability-contract.md:224
Evidence: The proposal's decision log records settled decisions to use a dedicated Markdown readability validator script and paired generated-region markers with `surface`, `source`, and optional `generator` metadata. However, the recommended direction still says "The exact marker shape should be settled in the downstream spec, with this candidate form" at lines 224-230, and the testing strategy says "Candidate repository-owned validation can be a dedicated script" and that downstream artifacts should decide whether it stays standalone or composed at lines 286-292. That conflicts with the owner's open-question decisions and the proposal's own `Open Questions: None`.
Required outcome: The proposal must state the dedicated readability validator and canonical generated-region marker syntax as settled proposal decisions, while leaving only implementation details to the downstream spec.
Safe resolution path: Revise `Recommended Direction` and `Testing and Verification Strategy` so `scripts/validate-markdown-readability.py` is the owner validator composed by other validators as needed, and the generated-region marker syntax is canonical. Keep downstream spec ownership for field validation details, path selection, parser behavior, and integration mechanics.
needs-decision rationale: none

### MDREAD-PR2 - Latest multi-part owner decisions are not classified in Initial intent preservation

Finding ID: MDREAD-PR2
Severity: major
Location: docs/proposals/2026-07-04-markdown-readability-contract.md:71
Evidence: The proposal is broad and includes an `Initial intent preservation` table at lines 71-86, but the table only classifies the original best-practice goals. It does not classify the owner's later explicit decisions on validator ownership, changed-section README and `VISION.md` enforcement, manual-proof exclusion, canonical marker syntax, diagram guidance, or audit-only warning graduation. Those decisions appear later in scope budget and decision log rows, but the proposal-review scope-preservation contract requires every initial user goal in a broad or multi-part request to be visibly classified with an initial goal treatment enum.
Required outcome: The proposal must add initial-intent preservation rows for the later owner decisions and classify them with allowed treatment values.
Safe resolution path: Add rows for dedicated validator ownership, changed-section README and `VISION.md` enforcement, no manual-proof contracts, canonical generated-region marker syntax, diagrams encouraged but never required, and audit-only warning graduation policy. Point each row to the sections where the decision is recorded.
needs-decision rationale: none

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The proposal states the real problem: generated Markdown can render acceptably while source diffs, skimability, and evidence locality remain weak. |
| User value | pass | Better source-readable generated artifacts directly support RigorLoop's reviewable and resumable workflow. |
| Option diversity | pass | The proposal compares human review only, fixed line-length lint, auto-formatting, and an artifact-aware readability contract with bounded validation. |
| Decision rationale | concern | The recommended direction is sound, but two owner-settled decisions are still framed as candidate or downstream choices. |
| Scope control | concern | The scope budget excludes manual-proof contracts and historical migration, but the initial-intent table does not classify the later multi-part owner decisions. |
| Architecture awareness | pass | The proposal identifies affected specs, skills, assets, scripts, templates, workflow guidance, README and `VISION.md`, generated adapters, and historical documents. |
| Testability | pass | The validation strategy includes stable check IDs, regression fixtures, generated-region checks, placeholder checks, command-ledger checks, historical audit-only behavior, and cold-read proof. |
| Risk honesty | pass | The proposal names subjective validator risk, long-line fear, verbosity, skeleton-policy drift, historical churn, block-type false positives, diagram overuse, and generated-region maintenance risk. |
| Rollout realism | pass | The rollout avoids half-updated skills, skeletons, validators, and generated output, and it excludes historical mass migration. |
| Readiness for spec | block | Resolve MDREAD-PR1 and MDREAD-PR2 before spec authoring relies on the proposal. |

## Scope Preservation Review

- Scope-preservation result: changes-requested.

The original best-practice goals are preserved, and the proposal records the later owner decisions in the decision log.
However, because this is a broad multi-part proposal with an `Initial intent preservation` table, the later owner decisions also need visible initial-goal treatment rows before downstream reliance.

## Recommended Proposal Edits

- Recommended edits: revise `Recommended Direction` and `Testing and Verification Strategy` so settled validator and marker decisions are not framed as candidate choices.
- Recommended edits: add `Initial intent preservation` rows for the later owner decisions.

## Recommendation

- Recommendation: changes-requested. The direction is valuable and aligned with the project vision, but MDREAD-PR1 and MDREAD-PR2 must be resolved and rereviewed before the proposal can normalize to `accepted` or feed a downstream spec. This direct proposal-review remains isolated and does not automatically start `spec`.
