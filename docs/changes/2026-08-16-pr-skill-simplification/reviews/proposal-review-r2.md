# Proposal Review: PR Skill Simplification

Review ID: proposal-review-r2
Stage: proposal-review
Round: r2
Reviewer: external independent proposal-review result supplied by the user
Target: `docs/proposals/2026-08-16-pr-skill-simplification.md`

Reviewed artifact: `docs/proposals/2026-08-16-pr-skill-simplification.md` at commit `4742134e`
Review date: 2026-08-16
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PRSIM-PR4, PRSIM-PR5, PRSIM-PR6
- Open blockers: submission-intent side effects, exact verified base identity, and safe refresh units require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, mutate a PR, or continue the workflow

## Overall assessment

The package direction remains appropriate: a compact universal `SKILL.md`, one governed-readiness reference, and one PR-body structural asset. Universal external-action safety and truthfulness remain inline, governed lifecycle aggregation follows a genuine conditional boundary, and the asset owns layout rather than readiness policy.

The revision closes the first review's head-tail, refresh-authority, and remote-race concerns directionally. Three external-operation contracts still require proposal-level closure: intent-specific side effects, exact base/head verification binding, and safe refresh units that do not imply an unmanaged Markdown parser.

## Material findings

### PRSIM-PR4 — Major: submission intent lacks a closed side-effect and existing-state matrix

Finding ID: PRSIM-PR4
Severity: major
Location: `Recommended Direction` sections `Invocation and operation model` and `Exact verified-revision sequence`
Evidence: The proposal defines `open`, `draft`, and `prepare-only` but does not exhaustively decide whether each may push, create, refresh, publish an existing draft, or convert an existing open PR. The generic execution sequence still pushes and mutates after intent resolution.
Required outcome: Separate creation intent from existing PR state-transition authority and define every intent's permitted external writes.
Safe resolution path: Make `prepare-only` externally read-only; preserve existing draft/open state by default; require separate explicit authority for publication or conversion; report requested intent, actual operation, external state, and readiness independently.
needs-decision rationale: none; the package design remains unchanged.

### PRSIM-PR5 — Major: verification does not conclusively bind the current base revision

Finding ID: PRSIM-PR5
Severity: major
Location: `Recommended Direction` sections `Invocation and operation model` and `Exact verified-revision sequence`
Evidence: The proposal validates the verified subject, evidence tail, handoff revision, remote head, and PR head, but it does not require the current remote base to equal the base or merge-base used by verification. The `fast-forwardable` and `ahead` terms are also directionally ambiguous.
Required outcome: Bind readiness to an exact verified base/head pair and use directional remote-branch relations.
Safe resolution path: Record repository, remote, base branch, base revision or verified merge base, head branch, and verified subject; recheck the remote base before mutation and after read-back; invalidate readiness on change; replace ambiguous branch-state names with ancestry predicates.
needs-decision rationale: none; existing evidence surfaces should remain sufficient unless specification proves otherwise.

### PRSIM-PR6 — Major: section-level PR-body refresh lacks a safe ownership contract

Finding ID: PRSIM-PR6
Severity: major
Location: `Recommended Direction` sections `Invocation and operation model` and `PR-body-skeleton.md ownership`
Evidence: The proposal permits replacing exact body sections while explicitly adding no markers or managed-section protocol. Duplicate headings, code fences, nesting, renames, ordering, and user-authored content under generated headings make section boundaries and ownership ambiguous.
Required outcome: Remove section-level body refresh from the first version or define a complete managed-content contract.
Safe resolution path: Limit refresh to closed host-native scalar fields such as title and to explicitly authorized whole-body replacement. Preserve body bytes otherwise and defer managed sections to a separate reviewed proposal with parser, ownership, compatibility, and architecture treatment.
needs-decision rationale: none; removing section refresh is the smaller safe solution.

## Architecture assessment

The expected result remains `architecture-not-required` if the revision uses existing Git, host-native fields, verify evidence, and PR evidence without adding a managed-section parser, ownership schema, persistent transaction record, or new evidence owner.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path overload and unsafe implicit external outcomes are concrete. |
| User value | pass | Portable PR work becomes smaller without losing governed traceability. |
| Option diversity | pass | The proposal compares materially different package approaches. |
| Decision rationale | pass | One reference and one asset follow real activation boundaries. |
| Vision fit | pass | The change improves the traceable idea-to-PR chain. |
| Scope control | pass | Provider engines, merge, release, runtime acceptance, and new lifecycle ownership remain excluded. |
| Submission authority | block | Intent and existing state transitions lack an exhaustive write matrix. |
| Revision binding | block | The verified base identity is not revalidated with the head. |
| Refresh safety | block | Section replacement has no safe ownership or parsing model. |
| Remote idempotency | pass with revisions | Post-push reread is strong once directional relations and intent writes are closed. |
| Hosted-CI truthfulness | pass | Closed states and exact-head evidence remain sound. |
| Structural ownership | pass | One skeleton remains proportionate. |
| Testing boundary | pass | Static fixtures and ordinary review are proportionate. |
| Architecture awareness | pass with revisions | No architecture work is plausible only without managed sections or new durable evidence. |
| Readiness for spec | changes-requested | PRSIM-PR4 through PRSIM-PR6 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass; every original objective remains visible and the new findings refine same-slice external-action safety.

## Recommended Proposal Edits

- Recommended edits: add the intent/state side-effect matrix; make `prepare-only` read-only; bind verification to the exact base/head tuple; use directional branch relations; restrict refresh to host-native scalar fields or explicit whole-body replacement; update risks, scenarios, and acceptance criteria.

## Recommendation

- Recommendation: revise PRSIM-PR4 through PRSIM-PR6, then perform an independent proposal rereview. No automatic downstream handoff follows.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass; the findings remain same-slice dependencies and introduce no hidden follow-up
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-16-pr-skill-simplification/reviews/proposal-review-r2.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: proposal-review-r2
- Review record: `docs/changes/2026-08-16-pr-skill-simplification/reviews/proposal-review-r2.md`
- Review log: `docs/changes/2026-08-16-pr-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-16-pr-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-16-pr-skill-simplification`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview
