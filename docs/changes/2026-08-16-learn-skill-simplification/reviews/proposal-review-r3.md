# Proposal Review: Learn Skill Simplification

Review ID: proposal-review-r3
Stage: proposal-review
Round: r3
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-16-learn-skill-simplification.md`

Reviewed artifact: `docs/proposals/2026-08-16-learn-skill-simplification.md` at commit `a140f046`
Review date: 2026-08-17
Recording status: recorded
Status: approved

## Result

- Skill: proposal-review
- Review status: approved
- Material findings: none
- Open blockers: none
- Proposal readiness: ready for focused specification
- Immediate next stage: focused learn contract specification
- Automatic downstream handoff: none
- Claim limitations: approval establishes proposal readiness only; it does not author or approve the specification, architecture assessment, plan, implementation, verification, branch, or PR

## Overall assessment

The proposal now selects a bounded and defensible simplification:

```text
compact universal SKILL.md
+ one session-method reference
+ no templates or scripts
+ fail-closed interruption rather than a transaction engine
+ narrow owner-result backlink recording rather than cross-stage reconciliation
```

The bounded inventory removes the unobserved trigger-assessment operation instead of preserving an artificial profile. Every valid session loads the method reference, and the proposal honestly makes the complete `LR1-learn-session` assembly—not main-file shrinkage—the primary acceptance surface.

The proposal also closes the authority contradiction without weakening derivative obligations. Contributor confirmation settles classification; destination authority remains with the owning skill or stage; `learn` owns only its session record, confirmed topic guidance, and exact backlink to an owner-produced result. Transaction-grade phase recovery, polling, aggregate workflow state, and destination mutation remain outside the change.

## What is strong

### Real profiles replace theoretical progressive disclosure

The proposal no longer claims that trigger assessment is a current learn invocation. `LR0-route-result` is a concrete narrow operation required for session backlink traceability, while `LR1-learn-session` represents every valid session and must strictly decrease from baseline.

### Interruption behavior is proportionate

Unique deterministic paths, content-identity checks, and fail-closed partial-state handling provide safe behavior without inventing durable phase state or an execution engine. Any later transaction-grade design is explicitly architecture-bearing and out of scope.

### Route traceability remains bounded

Stable per-route records permit later exact backlinks, but `record-learn-route-result` cannot repeat classification, change topic guidance, discover or poll destinations, derive workflow state, or mutate another artifact. This is sufficient to carry the existing session-link obligation without making learn a workflow owner.

### Scope and proof remain honest

The proposal retains the established three-surface model, contributor confirmation, sensitive-data protection, no-template direction, package parity, semantic-rule disposition, and static acceptance. It reports total package size separately and excludes target-agent execution.

## Architecture assessment

The expected bounded result is `architecture-not-required`. The selected first version uses the existing Markdown session record, skill package model, stage ownership, and generated-package pipeline. It introduces no persistent phase state, transaction artifact, poller, coordinator, external integration, or new state owner.

The bounded assessment must change to `architecture-required` if specification discovers that stable route backlinks cannot be represented safely inside the existing session record or that implementation needs persistent phase/effect state, automated reconciliation, or another owner.

## Specification notes

These are downstream contract details, not material proposal findings:

- Apply `record-learn-route-result` prospectively to sessions containing the new stable route identity; historical sessions without such identity remain readable and are not mutated implicitly.
- Name or define route completion so it means the learn backlink was recorded, not that the destination proposal, ADR, spec, issue, or other artifact was reviewed, accepted, closed, or implemented.
- Define the deterministic suffix and stable route-ID syntax in the specification and test it without introducing a template or machine-owned session schema.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Flat ownership, duplicated procedure, and cross-owner ambiguity are explicit. |
| User value | pass | The actual session assembly must shrink while judgment and evidence remain intact. |
| Option diversity | pass | Unchanged, editorial compression, one reference, fragmented references, and executable machinery are materially distinct. |
| Decision rationale | pass | One coherent method reference plus a compact backlink operation is proportionate. |
| Vision fit | pass | Durable human-confirmed, Git-tracked lessons remain aligned with project vision. |
| Scope control | pass | Transaction recovery, polling, templates, scripts, engines, integration, migration, and unrelated skills remain excluded. |
| Universal safety | pass | Trigger, evidence, confirmation, ownership, sensitive-data, stops, claims, and resource selection remain inline. |
| Operation model | pass | Session execution and exact backlink recording have non-overlapping authority. |
| Interruption safety | pass | Partial or ambiguous state fails closed without an unsupported resume claim. |
| Derivative ownership | pass | Destination mutation and review remain with the owning skill or stage. |
| Compatibility | pass with specification notes | Historical sessions remain readable; new route-result writes should be prospective. |
| Testability | pass | Real profiles, collisions, partial state, route identities, forbidden writes, and package parity have deterministic scenarios. |
| Risk honesty | pass | Scope expansion and architecture triggers are explicit. |
| Rollout realism | pass | The focused contract amendment precedes package changes; no data migration is required. |
| Architecture awareness | pass | Existing architecture is likely sufficient under the stated boundary. |
| Readiness for spec | pass | Remaining questions are bounded field, vocabulary, and compatibility details. |

## Scope Preservation Review

- Scope-preservation result: pass; all original optimization, evidence-quality, confirmation, authority, no-template, deterministic-proof, branch, proposal, and review goals remain explicitly treated.

## Recommended Proposal Edits

- Recommended edits: none

## Recommendation

- Recommendation: approve the proposal for focused learn contract specification and bounded architecture assessment. This direct review remains isolated and performs no automatic downstream handoff.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass; core work, same-slice dependencies, first-slice candidates, exclusions, and separate future architecture-bearing work are bounded
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-16-learn-skill-simplification/reviews/proposal-review-r3.md`
- Finding-record paths: none

## Formal-settlement group

- Review ID: proposal-review-r3
- Review record: `docs/changes/2026-08-16-learn-skill-simplification/reviews/proposal-review-r3.md`
- Review log: `docs/changes/2026-08-16-learn-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-16-learn-skill-simplification/review-resolution.md`
- Proposal settlement: accepted
- Governed change identity: `2026-08-16-learn-skill-simplification`
- Formal next-stage eligibility: eligible for focused specification; no automatic continuation
