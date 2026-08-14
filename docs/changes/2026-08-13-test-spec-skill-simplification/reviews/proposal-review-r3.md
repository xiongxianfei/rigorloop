# Proposal Review R3: Test-Spec Skill Simplification

Review ID: proposal-review-r3
Stage: proposal-review
Round: r3
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-13-test-spec-skill-simplification.md`
Reviewed artifact: commit `5acf8afe`
Review date: 2026-08-13
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: TSSIM-PR7
- Open blockers: stale-attempt closeout cannot restart at the canonical artifact path under the existing lifecycle schema
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, or continue the workflow

## Overall assessment

The proposal now closes governed revision, stage ownership, creation retry, structural composition, and optional manual-verification ownership well. It correctly avoids a new manual-proof contract and asset. One recovery detail remains incompatible with the current lifecycle schema.

## Material findings

### TSSIM-PR7 — Major: terminal abandonment cannot support canonical-path restart

Finding ID: TSSIM-PR7
Severity: major
Location: Stale interrupted authoring; Acceptance criteria; Rollout and Rollback
Evidence: The proposal moves an incomplete primary test-spec entry from `authoring` to terminal `abandoned`, then starts a new creation with a new retry identity. The accepted lifecycle contract makes `abandoned` terminal, permits no `abandoned → authoring` transition, allows only one primary artifact per kind, and rejects duplicate artifact paths. A new primary entry at the canonical test-spec path would therefore conflict with the abandoned entry, while reusing the abandoned entry is illegal. The proposed recovery cannot reach the intended new creation without an unapproved schema or lifecycle change.
Required outcome: Choose a recovery path that remains legal under the current single-primary, unique-path, terminal-state contract, or explicitly broaden the proposal to amend that contract.
Safe resolution path: Keep the same incomplete entry in `authoring` and introduce an explicit test-spec-owned `restart-stale-authoring` operation under workflow-routed authorization. The operation writes a closeout/restart evidence record for the stale attempt, replaces the entry's `authoring_evidence` with a new path, binds current governing inputs and a new retry identity, and preserves the same artifact ID and canonical path. It may replace or create only the incomplete, unreviewed test-spec content at that same path after proving no review or downstream reliance exists. It must not use terminal `abandoned`, create another primary entry, or mutate workflow and review state. If preserving the partial bytes is required, archive them to a distinct evidence path owned by the restart record before replacement. Alternatively, explicitly propose and specify a lifecycle-schema amendment allowing terminal-entry replacement and path reuse, but that is broader than this simplification.
needs-decision rationale: none; the smaller same-entry restart preserves current architecture and proposal scope.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The simplification problem remains well defined. |
| User value | pass | Loaded-context and ownership improvements remain valuable. |
| Option diversity | pass | The selected design remains proportionate. |
| Decision rationale | pass | Existing resources and one governed reference remain appropriate. |
| Vision fit | pass | The change improves usable traceability. |
| Scope control | pass | Manual-proof expansion is correctly rejected. |
| Architecture awareness | concern | The abandonment/restart sequence conflicts with existing terminal and uniqueness rules. |
| Testability | block | The proposed restart cannot form a valid metadata fixture. |
| Risk honesty | pass with revisions | Recovery needs the same-entry restart correction. |
| Rollout realism | block | Current rollout would strand or conflict with the primary artifact entry. |
| Readiness for spec | block | TSSIM-PR7 requires proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass. All user goals remain represented, and the proposal correctly keeps manual verification optional without new ceremony.

## Recommended Proposal Edits

- Replace terminal abandonment plus new entry with a same-entry `restart-stale-authoring` operation that keeps the artifact ID and path, changes the evidence path and retry identity, and is permitted only before review or downstream reliance.
- Preserve partial bytes at a distinct evidence path only when required; otherwise replace incomplete content under the same explicitly authorized restart.
- Add acceptance and static scenarios proving terminal states and duplicate paths are never used for restart.

## Recommendation

- Recommendation: revise TSSIM-PR7 and run one more independent proposal review. No automatic downstream handoff follows this review.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass; scope remains bounded and explicit
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-13-test-spec-skill-simplification/reviews/proposal-review-r3.md`
- Finding-record paths: `docs/changes/2026-08-13-test-spec-skill-simplification/reviews/proposal-review-r3.md`

## Formal-settlement group

- Review ID: proposal-review-r3
- Review record: `docs/changes/2026-08-13-test-spec-skill-simplification/reviews/proposal-review-r3.md`
- Review log: `docs/changes/2026-08-13-test-spec-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-13-test-spec-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-13-test-spec-skill-simplification`
- Formal next-stage eligibility: proposal revision only
