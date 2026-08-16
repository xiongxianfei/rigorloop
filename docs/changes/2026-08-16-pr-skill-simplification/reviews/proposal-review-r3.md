# Proposal Review: PR Skill Simplification

Review ID: proposal-review-r3
Stage: proposal-review
Round: r3
Reviewer: Codex independent proposal-review context reset to tracked revision
Target: `docs/proposals/2026-08-16-pr-skill-simplification.md`

Reviewed artifact: `docs/proposals/2026-08-16-pr-skill-simplification.md` at commit `56dbbcfa`
Review date: 2026-08-16
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PRSIM-PR7
- Open blockers: the exact verified base/head tuple has no explicit current durable evidence owner or same-slice contract amendment
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve specification, architecture, implementation, verification, branch readiness, or PR readiness

## Overall assessment

The selected package remains sound, and the round-two revision closes `PRSIM-PR4` through `PRSIM-PR6`. `prepare-only` is now externally read-only, existing PR state transitions require separate authority, branch relationships are directional, base movement invalidates readiness, external success remains truthful, and Markdown section mutation is excluded.

One cross-skill evidence dependency remains unresolved. The proposal requires `pr` to consume an exact verified repository, remote, base revision, optional merge base, head branch, and subject revision, but the current `verify` skill and workflow contract do not require one normalized durable record containing that tuple. Historical verify reports encode bases inconsistently through prose, commands, branch names, merge bases, or stacked-branch notes. The proposal's rollout and scope budget currently mention only the `pr` package and directly coupled validators, so specification would have to invent the evidence owner or silently weaken the new base-safety rule.

## What is strong

- The intent side-effect matrix prevents `prepare-only` and default creation intent from acquiring unrelated external authority.
- Existing body bytes are preserved unless whole-body replacement is explicit; no parser or marker system is introduced.
- The base, remote head, and PR state are reread at the correct external-operation boundaries.
- External mutation success is reported separately from readiness when concurrent state changes.
- Static fixtures and ordinary operational use remain proportionate acceptance surfaces.

## Material findings

### PRSIM-PR7 — Major: the exact verified base/head basis has no explicit durable evidence owner in scope

Finding ID: PRSIM-PR7
Severity: major
Location: `Recommended Direction` section `Exact verified-revision sequence`, `Architecture Impact`, `Testing and Verification Strategy`, `Rollout and Rollback`, and `Scope budget`
Evidence: The revised proposal requires the verify report to provide exact repository, remote, base branch, base revision, optional merge base, head branch, and verified subject identities. Current `skills/verify/SKILL.md` owns `branch-ready` but does not require that normalized tuple, and current verify reports use inconsistent command, prose, branch-name, merge-base, and stacked-base representations. The proposal does not explicitly include an amendment to the existing verify evidence contract or its compatibility behavior.
Required outcome: Assign the normalized verification basis to the existing `verify` evidence owner and place the directly coupled contract and fixture amendment in the same slice without transferring `branch-ready` ownership to `pr`.
Safe resolution path: State that final or branch-readiness verification records the exact repository, remote, base branch, resolved base revision, optional merge-base identity, head branch, and verified subject. Treat legacy or portable evidence without a resolvable exact basis as insufficient for `pr-open-ready`; allow preparation but require fresh verification. Add the verify contract, fixtures, preservation ledger, rollout, architecture condition, scope budget, and acceptance proof as same-slice dependencies. If this cannot fit the existing verify-report evidence surface, change the architecture result to required.
needs-decision rationale: none; the existing verify stage remains the correct owner.

## Architecture assessment

The expected result remains `architecture-not-required` only if the normalized base/head tuple is added to the existing verify report or existing verify-owned evidence surface. A new persistent evidence type, owner, schema, or cross-process transaction would require architecture work.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The common-path and external-operation problems are concrete. |
| User value | pass | Portable and governed PR preparation become smaller and safer. |
| Option diversity | pass | The alternatives are materially different. |
| Decision rationale | pass | One reference and one structural asset remain proportionate. |
| Vision fit | pass | The proposal improves traceability and reviewer clarity. |
| Scope control | block | The required verify-evidence amendment is not classified in the same slice. |
| Submission authority | pass | Intent, refresh, and existing-state authority are independent and closed. |
| Revision binding | concern | The base/head semantics are sound, but the required upstream evidence contract is absent. |
| Refresh safety | pass | No unmanaged section mutation remains. |
| Remote idempotency | pass | Directional states, non-force behavior, and post-push reread are deterministic. |
| Hosted-CI truthfulness | pass | Current-head evidence and claim limits remain closed. |
| Testing boundary | pass with revisions | Static proof is appropriate after verify-evidence compatibility fixtures are added. |
| Architecture awareness | pass with condition | Existing evidence ownership can avoid architecture work; a new owner cannot. |
| Readiness for spec | changes-requested | PRSIM-PR7 requires proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass for the user's initial goals; one newly required same-slice dependency is missing from the proposal budget.

## Recommended Proposal Edits

- Recommended edits: name `verify` as the existing normalized base/head evidence owner; add the directly coupled verify-contract and fixture amendment to scope, rollout, risks, architecture, preservation, scenarios, and acceptance; fail closed on legacy or portable reports without an exact basis.

## Recommendation

- Recommendation: revise PRSIM-PR7 and run another independent proposal review. No automatic downstream handoff follows.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: changes requested because the new verify-evidence work is an unclassified same-slice dependency
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-16-pr-skill-simplification/reviews/proposal-review-r3.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: proposal-review-r3
- Review record: `docs/changes/2026-08-16-pr-skill-simplification/reviews/proposal-review-r3.md`
- Review log: `docs/changes/2026-08-16-pr-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-16-pr-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-16-pr-skill-simplification`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview
