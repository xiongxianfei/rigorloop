# Proposal Review R1: Test-Spec Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-13-test-spec-skill-simplification.md`
Reviewed artifact: commit `d707ad21`
Review date: 2026-08-13
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: TSSIM-PR1, TSSIM-PR2, TSSIM-PR3
- Open blockers: test-spec activation ownership, governed creation recovery, and structural asset ownership require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, or continue the workflow

## Overall assessment

The proposal selects the right broad package boundary: a shorter universal `SKILL.md`, one conditional governed authoring reference, both existing and initially required boundary-first references, and the existing five structural assets. It correctly rejects an unapproved attempt to make proof guidance optional, separates candidate loading from mutation authority, keeps universal proof-ledger policy inline, and measures loaded profiles rather than only the main file.

The direction is stronger than generic editorial compression because it gives lifecycle procedure and repeated structure explicit owners while preserving the current proof model. Three contracts still need proposal-level closure before a specification can implement the change without inventing state, recovery, or structural behavior.

## Material findings

### TSSIM-PR1 — Major: authoring and settlement ownership overlap

Finding ID: TSSIM-PR1
Severity: major
Location: Recommended Direction; Invocation and authority model; Resource ownership; Expected Behavior Changes
Evidence: The governed reference is assigned both the author-owned `authoring → review-required` transition and “workflow-managed settlement preparation.” The proposal also says successful authoring hands off to `test-spec-review`, while the governing lifecycle contract assigns `review-required → active` to `test-spec-review` and defines later implementation-profile test-spec settlement as a workflow-owned gate requiring current review evidence. “Settlement preparation” is not a closed operation or write boundary and could let `test-spec` activate its own artifact, manufacture review settlement, write automation state, or duplicate the later workflow settlement gate.
Required outcome: Define exactly what `test-spec` completes, what `test-spec-review` settles, and what workflow-managed test-spec settlement checks, with one non-overlapping write and handoff matrix.
Safe resolution path: Rename the reference to governed authoring procedure or explicitly exclude settlement ownership. Make authoring completion stop at `review-required` after writing the test spec and authoring evidence; make `test-spec-review` the only owner of `review-required → active`; make the later workflow settlement gate read-only or workflow-owned validation that cannot be performed or persisted by `test-spec`. For an armed invocation, `test-spec` may emit the authoring receipt and return control to workflow, but it must not advance routing or implementation eligibility.
needs-decision rationale: none; the accepted lifecycle contract already assigns the three responsibilities.

### TSSIM-PR2 — Major: governed creation has no interruption-safe transaction

Finding ID: TSSIM-PR2
Severity: major
Location: Invocation and authority model; Static contract scenarios; Rollout and Rollback
Evidence: New governed creation is defined as writing a test spec and creating its matching artifact entry, but the proposal does not choose an exact write order, partial-write state, retry identity, or collision behavior. A crash after the file write but before entry creation produces the same file/entry asymmetry that the proposal currently classifies as a conflict and stops. A crash after entry creation but before complete authoring evidence can likewise leave an ambiguous candidate. The proposed static scenarios mention concurrent writes but not the intended interrupted-creation reconciliation.
Required outcome: Select one deterministic creation transaction and identical-retry behavior that distinguishes a recoverable partial write from an unrelated pre-existing file or entry.
Safe resolution path: Resolve and reserve one intended path and artifact ID, create the entry in `authoring` with the authoring-evidence path before content mutation, write the test spec and complete authoring record, validate identities, then move the same entry to `review-required`. On retry, reconcile only when the exact artifact ID, normalized path, authoring-evidence path, and intended change identity match; unrelated files, entries, changed content bases, multiple candidates, or conflicting reuse stop. Define no review or workflow state as part of this sequence.
needs-decision rationale: none; the accepted authoring-transition contract requires an authoring state before substantive content mutation.

### TSSIM-PR3 — Major: the full skeleton and repeated assets lack one structural owner

Finding ID: TSSIM-PR3
Severity: major
Location: Structural ownership; Testing and Verification Strategy
Evidence: The proposal says the five assets are the sole structural owners and that repeated assets are copied once per applicable row or case. However, `test-spec-skeleton.md` currently embeds example test, validation-command, and milestone table shapes while the four smaller assets also own those same repeated structures. The proposal does not state whether implementation will remove repeated example rows from the skeleton, treat the skeleton as the full-document owner with nested row assets, or permit intentional duplicated fingerprints. Without an exact composition rule, the single-owner objective is untestable and validators could preserve two structural sources.
Required outcome: Define one composition and ownership model for the full skeleton and the four repeated assets, including whether nested placeholders remain and how creation versus revision uses them.
Safe resolution path: Keep the skeleton as the sole owner of section order and table headers, while row/case assets own repeated body shapes. Replace duplicated example body rows in the skeleton with named insertion placeholders that reference the mapped row or case assets, or explicitly classify the skeleton rows as non-copying placement markers and validate that distinction. Full creation copies the skeleton then expands every applicable insertion from the smaller assets; bounded revision copies only the affected row or case asset unless a full rewrite is required. Assets remain policy-free and unfilled placeholders remain forbidden in emitted artifacts.
needs-decision rationale: none; this is an ownership and deterministic composition gap.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path overload, governed mutation, duplicated procedure, and structural overlap are concrete and measured. |
| User value | pass | Portable and governed proof authoring should become easier to scan without weakening traceability. |
| Option diversity | pass | Unchanged, editorial, one-reference, fragmented, and executable-engine options are materially different. |
| Decision rationale | pass | One governed reference plus retained shared resources and assets is proportionate. |
| Vision fit | pass | The direction improves usable, reviewable traceability and preserves durable proof. |
| Scope control | pass | Boundary redesign, adjacent skills, runtime machinery, historical rewriting, and permanent simplicity policy remain excluded. |
| Architecture awareness | pass with revisions | Existing package architecture likely suffices; lifecycle ownership language must be made exact. |
| Testability | block | Interrupted creation and asset composition lack deterministic expected outcomes. |
| Risk honesty | pass with revisions | The main risks are named, but settlement overlap and partial-write recovery need explicit mitigation. |
| Rollout realism | pass with revisions | Atomic canonical rollout is appropriate after the creation and asset migration sequences are closed. |
| Readiness for spec | block | TSSIM-PR1 through TSSIM-PR3 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass. Every initial user goal remains visible and in scope. The scope budget distinguishes the core skill simplification, same-slice boundary and validator dependencies, preservation evidence, and out-of-scope boundary-model or adjacent-skill work without hiding follow-ups.

## Recommended Proposal Edits

- Replace the open-ended “settlement preparation” responsibility with an exact authoring, review settlement, and workflow settlement ownership table and handoff sequence.
- Add an interruption-safe governed creation sequence plus identical retry, collision, and forbidden-write behavior.
- Define the skeleton as section/header owner and the smaller assets as repeated-body owners, with a deterministic full-create and bounded-revision composition rule.

## Recommendation

- Recommendation: revise the proposal to resolve TSSIM-PR1 through TSSIM-PR3, then rerun independent `proposal-review` against a frozen revision. No automatic downstream handoff follows this review.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass; every core, same-slice, and out-of-scope work item has a valid treatment and reason
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-13-test-spec-skill-simplification/reviews/proposal-review-r1.md`
- Finding-record paths: `docs/changes/2026-08-13-test-spec-skill-simplification/reviews/proposal-review-r1.md`

## Formal-settlement group

- Review ID: proposal-review-r1
- Review record: `docs/changes/2026-08-13-test-spec-skill-simplification/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-13-test-spec-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-13-test-spec-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-13-test-spec-skill-simplification`
- Formal next-stage eligibility: proposal revision only
