# Design Review R13: Current judgment and bootstrap coherence

Review ID: design-review-r13
Stage: design-review
Round: r13
Reviewer: Independent Codex design-review context
Reviewer authority: design-review
Target: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Reviewed artifact: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Review date: 2026-09-04
Package kind: design
Package members: architecture=docs/architecture/2026-09-03-compact-current-state-change-record.md, spec=specs/compact-current-state-change-record.md, adr-compact-current-state-transaction=docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md
Upstream review ID: proposal-review-r7
Status: approved
Current judgment: clear
Material findings: none
Correction targets: none
Recording status: recorded

## Result

- Skill: design-review
- Review judgment: clear
- Legacy recording status: approved
- Package members: architecture=`docs/architecture/2026-09-03-compact-current-state-change-record.md`, spec=`specs/compact-current-state-change-record.md`, adr-compact-current-state-transaction=`docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md`
- Upstream review ID: proposal-review-r7
- Review ID and round: design-review-r13, r13
- Material findings: none
- Correction targets: none
- Recording status: recorded
- Settlement status: pending exact-package CLI settlement
- Open blockers at the Design judgment layer: none
- Immediate next stage: settle the exact Design package, then reconcile the Plan and Delivery Review with SR-47, SR-48, `BND-STATE-003`, `BND-COMPAT-003`, `INT-006`, and `INT-007`
- Claim limitations: the legacy `approved` field is required only by the registered v3 recorder; the semantic judgment is `clear`, and progression remains mechanically derived. This review grants no Delivery, implementation, final verification, branch, pull-request, release, or deployment readiness.

## Package judgment

The Architecture, ADR, and Specification now separate three responsibilities coherently. Independent review records whether the exact current subject is clear, has open findings, or cannot be judged. A named decision owner explicitly accepts only a materially constraining choice. The lifecycle evaluator derives progression from the current judgment, finding state, accepted material decisions, evidence, and transition rules instead of storing another approval grant.

Finding occurrences now own stable identity and disposition independently of aggregate container identity. An artifact or record revision invalidates only declared current dependencies. It cannot reopen a settled occurrence; a genuine recurrence creates a new finding linked to the still-applicable decision. The lifecycle revision remains whole-set optimistic concurrency and is explicitly denied semantic-dependency meaning.

The implementing-change bootstrap is closed to one change ID, leaves that change structurally legacy, binds exact subjects and current lifecycle state, validates only current consequential state, ignores only individually settled superseded procedure, and atomically combines closeout with activation. The Specification resolves the legacy review bridge by deriving bootstrap `clear` only from an independently completed exact-subject review with no open blocking finding; its legacy outcome label is insufficient by itself and never enters compact vocabulary. Git, branch, diff, pull-request, hosted-service, and local-log identity are excluded.

The Specification boundary record is internally consistent. Repository boundary validation reports only that the already-registered downstream Plan does not yet allocate the two new boundaries and two interactions. That is a required Delivery correction, not a defect in this Design package, and this review grants no authority to skip it.

## Prior finding closeout

- CCSR-DR12-1 is resolved by Architecture stable-review replacement and identity/concurrency rules, the ADR's separated responsibility and per-occurrence non-loss decision, and Specification SR-08, SR-10 through SR-12, SR-25, SR-26, SR-32, SR-47, the exact schemas, settlement matrix, EC15, and AC-15.
- CCSR-DR12-2 is resolved by the Architecture bootstrap runtime, the ADR's closed preactivation exception, and Specification SR-23, SR-34 through SR-36, SR-48, the `bootstrap-closeout` request and eligibility rule, `BND-COMPAT-003`, INT-007, EC16, and AC-16.

## No-Finding Statement

Clean formal Design Review completed with no material findings against the exact R13 package.

## Independence statement

This review did not edit the proposal, architecture, specification, ADR, authoring evidence, or lifecycle routing state.
