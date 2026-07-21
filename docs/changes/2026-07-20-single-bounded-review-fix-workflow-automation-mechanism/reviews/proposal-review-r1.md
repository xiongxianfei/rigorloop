# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: User-provided proposal-review result
Target: docs/proposals/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism.md
Status: changes-requested
Original review source: User-provided proposal-review result dated 2026-07-20.
Material findings: BRF-PR1, BRF-PR2, BRF-PR3, BRF-PR4
Architecture assessment: architecture-required
Scope-preservation result: changes-requested
Immediate next stage: proposal revision
Automatic downstream handoff: none

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: `BRF-PR1`, `BRF-PR2`, `BRF-PR3`, `BRF-PR4`
- Recording status: recorded
- Open blockers: canonical-position derivation, grant binding, transition recovery, and repeated-stage target identity
- Immediate next stage: proposal revision
- Spec readiness: not ready

## Material Findings

### BRF-PR1 - Canonical workflow-position resolution remains undefined before an active plan exists

Finding ID: BRF-PR1
Severity: major
Location: Canonical state ownership and transition routing
Evidence: The proposal names the active plan as canonical after planning but does not identify the canonical workflow-position derivation for proposal-review through plan creation, when no active plan may exist.
Required outcome: Define pre-plan position as a derivation from authoritative artifacts, formal reviews, review-resolution state, architecture applicability, and the closed transition registry; define the valid active plan as canonical after plan creation; keep automation metadata evidence-only.
Safe resolution path: Add two workflow-position epochs, a deterministic plan-creation ownership handoff, stale and contradictory evidence stops, and direct proof criteria.

### BRF-PR2 - Grants are statuses rather than identity-bound authorities

Finding ID: BRF-PR2
Severity: major
Location: Single bounded-review-fix run and Target and authority are independent
Evidence: The illustrative grant state records only `authorized` or `pending`, so implementation or verification authority could survive material changes to its reviewed basis, scope, paths, milestones, commands, or policy.
Required outcome: Define each grant as explicit authority plus concrete basis plus bounded scope, with stable identity, policy version, authorizer, timestamp, invalidation triggers, and grant-specific basis requirements.
Safe resolution path: Add a common grant envelope, bind implementation and verification grants to concrete reviewed evidence, make external actions non-grantable, and pause on basis or scope drift.

### BRF-PR3 - Transition receipts do not define a recoverable transaction protocol

Finding ID: BRF-PR3
Severity: major
Location: Single transition engine
Evidence: A receipt written after transition completion cannot reconcile interruption between stage invocation, artifact writes, review recording, plan synchronization, and receipt finalization.
Required outcome: Define a write-ahead two-phase transition protocol with a prepared receipt, deterministic key, policy version, expected postcondition, closed statuses, stage retry policy, reconciliation rules, and at most one in-flight transition.
Safe resolution path: Add prepare, invoke, inspect, synchronize, and finalize steps plus a resume matrix that never reruns work before checking stage-owned completion evidence.

### BRF-PR4 - Repeated target stages need occurrence identities

Finding ID: BRF-PR4
Severity: major
Location: Expanded target boundary
Evidence: `target_stage: code-review` cannot identify a milestone occurrence and cannot distinguish milestone-local review from the final holistic code review required before verification.
Required outcome: Persist a structured target containing stage, occurrence identity, and completion predicate; bind repeated targets to milestone IDs; distinguish public targets from internal trigger stages.
Safe resolution path: Add target envelopes for singleton, milestone, and final occurrences; define `implement@M<n>`, `code-review@M<n>`, and final `verify` completion; preserve conditional architecture behavior.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Duplication among the three automation mechanisms is clear. |
| User value | pass | One mechanism simplifies status, continuation, cancellation, and extension. |
| Option diversity | pass | Existing mechanisms, dispatcher-only, expanded engine, declarative graph, and blanket authority are compared. |
| Decision rationale | pass | Expanding one target-driven mechanism is defensible. |
| Scope control | pass with revisions | External actions remain excluded; target identity needs closure. |
| State ownership | block | Pre-plan canonical position is undefined. |
| Authorization safety | block | Grants lack concrete basis and scope binding. |
| Resume and idempotency | block | No write-ahead transition and recovery protocol exists. |
| Repeated-stage semantics | block | `implement` and `code-review` require occurrence identities. |
| Migration | pass with revisions | Dual-read, single-write is correct; active legacy migration needs one-way semantics. |
| Architecture awareness | pass | Architecture and a superseding ADR are required. |
| Readiness for spec | changes-requested | Resolve `BRF-PR1` through `BRF-PR4`. |

## Recommendation

Revise the proposal for deterministic canonical-position derivation, identity-bound grants, write-ahead transition recovery, and structured repeated-stage targets before specification.
