# Learn Session: Single Bounded Review-Fix Finding Volume

## Status

- captured
- routing pending contributor confirmation

## Frame

- Trigger: explicit maintainer invocation asking why the single bounded
  review-fix automation initiative accumulated more than 100 review findings
  and whether poor proposal or specification quality caused the volume.
- Trigger type: explicit maintainer request / repeated review findings /
  workflow-process retrospective.
- Date: 2026-07-25
- Scope:
  - change
    `2026-07-20-single-bounded-review-fix-workflow-automation-mechanism`;
  - formal findings from proposal review through final holistic code review;
  - the distinction between upstream contract quality, implementation proof
    quality, review depth, and finding-accounting behavior.
- Evidence in scope:
  - `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
  - `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md`
  - the accepted proposal, approved specification, architecture, execution
    plan, and test specification for the change;
  - prior learn sessions about autoprogression, review finding volume,
    boundary-driven implementation, and repeated verification cost.
- Explicit exclusions:
  - no proposal, specification, architecture, plan, workflow, skill,
    validator, or topic update from this session;
  - no reopening of resolved findings;
  - no claim about hosted CI or merge readiness;
  - no durable route without contributor confirmation.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-06-27-first-autoprogression-review-finding.md`
  - `docs/learn/sessions/2026-06-29-release-automation-review-findings.md`
  - `docs/learn/sessions/2026-06-24-verify-repetition-cost.md`
  - `docs/learn/sessions/2026-06-23-resource-integrity-review-finding-pattern.md`
- Session record path:
  `docs/learn/sessions/2026-07-25-single-bounded-review-fix-finding-volume.md`

## Observe

### O1 - The 104 findings belong to the full lifecycle, not only the proposal loop

The unique material findings recorded in `review-resolution.md` are distributed
as follows:

| Review stage | Findings |
| --- | ---: |
| Proposal review | 7 |
| Spec review | 6 |
| Architecture review | 3 |
| Plan review | 2 |
| Test-spec review | 4 |
| M1 code review | 12 |
| M2 code review | 6 |
| M3 code review | 15 |
| M4 code review | 23 |
| M5 code review | 14 |
| M6 code review | 11 |
| Final holistic code review | 1 |
| **Total** | **104** |

Proposal and spec review account for 13 findings, or 12.5 percent of the total.
All pre-implementation review stages together account for 22 findings, or about
21.2 percent. Implementation code review accounts for 82 findings, or about
78.8 percent.

These percentages describe where findings were discovered, not a mathematically
exact attribution of cause. A code finding can still expose an upstream
ambiguity. They do establish that calling all 104 findings a "proposal loop"
overstates the proposal's contribution.

### O2 - The initial proposal and spec were directionally sound but not contract-complete

Proposal review found real design gaps:

- canonical workflow position before an active plan existed;
- identity-bound authority and scope;
- interrupted-transition recovery;
- repeated-stage occurrence identity;
- proposal-review bootstrap authority;
- parent authorization versus effective capability;
- review occurrence versus clean-gate satisfaction.

Spec review then found closed contracts that remained implicit:

- stage-to-occurrence compatibility;
- durable status vocabularies and transitions;
- verify target versus verification authorization timing;
- legacy command mappings;
- exact cross-spec precedence;
- selector and source ownership.

These were not cosmetic review comments. The first drafts were not yet safe to
implement because a spec author or implementer would have needed to invent
architecture and lifecycle decisions.

The underlying direction was still sound: one writable mechanism,
dual-read/single-write migration, separate risk-class authority, stage-specific
correction policy, and exclusion of external actions survived review. The
accurate assessment is therefore "good direction, insufficient first-pass
contract completeness," not simply "bad proposal/spec."

### O3 - Most finding volume came from implementation at trust and recovery boundaries

Milestones M3 through M6 account for 63 findings, about 60.6 percent of the
total. Those milestones contain the densest state and trust boundaries:

- canonical position and repository-owned identity derivation;
- authorization and effective-capability validation;
- transition receipts, atomic persistence, interruption, and resume;
- proposal and implementation correction loops;
- formal-review chronology and review-resolution consistency;
- Git code-state and verification boundaries;
- compatibility migration, public command routing, and selector registration.

Repeated implementation findings commonly showed one of these proof gaps:

- caller-provided evidence was trusted instead of deriving canonical
  repository evidence;
- shape validation existed without semantic or cross-record validation;
- the obvious negative case was fixed while a neighboring bypass remained;
- helper behavior was tested without proving the composed public command path;
- mutation success was covered without restart, rollback, or partial-write
  recovery;
- a narrow fixture substituted for an exhaustive closed-vocabulary or
  state-transition matrix.

This is primarily a boundary-modeling and proof-translation problem. The
approved contracts named many invariants, but implementation often translated
them example by example instead of closing the entire adversarial state space
before requesting review.

### O4 - Stable finding accounting made residual defects visible

The repository correctly gives each material finding a stable identity and
does not rewrite an earlier finding when a correction exposes a residual or
neighboring defect. Several review rounds therefore record a resolved finding
and a new finding for the remaining bypass.

That behavior increases the raw count compared with a process that repeatedly
edits one broad review comment. It is good auditability, but it means "104
findings" is not equivalent to "104 independent mistakes present in the first
draft."

Raw finding count should be paired with:

- root-cause cluster count;
- first-pass versus failed-remediation findings;
- review rounds per milestone;
- direct-proof escape rate;
- final holistic escape count.

### O5 - Adversarial review was expensive, but it converged

The reviews exercised identity substitution, closed-enum rejection, stale
evidence, restart recovery, transaction ordering, cancellation, compatibility,
and public selector behavior. These are exactly the areas in which a workflow
engine can appear correct on happy paths while remaining unsafe.

Only one finding remained at final holistic review, and the following review was
clean. That convergence is evidence that the review system worked. The avoidable
cost was allowing independent review to become the first exhaustive boundary
audit for several milestones.

### O6 - The reusable prevention is a boundary-completeness gate before code review

Before implementation handoff, each milestone should enumerate:

1. canonical state owner;
2. authority source and exact bound identity;
3. trusted versus untrusted inputs;
4. mutation boundary and atomicity expectation;
5. restart, reconciliation, and cancellation behavior;
6. every closed vocabulary and illegal transition;
7. composed public command path;
8. validation selector and CI registration;
9. direct positive, negative, tamper, and stale-evidence proofs.

After fixing a finding, the implementer should sweep the sibling boundary rather
than patching only the reported example. This is the main opportunity to reduce
review rounds without weakening review.

## Root Cause

The finding volume was not caused by one bad proposal or specification.

Four factors combined:

1. **Large state space.** The change unified three historical automation
   mechanisms while adding durable authorization, capability, recovery,
   migration, and review semantics.
2. **Upstream abstraction debt.** The first proposal and spec drafts had the
   right direction but left several closed contracts implicit. This caused 13
   direct proposal/spec findings and influenced later work.
3. **Incomplete proof translation.** Most findings appeared during
   implementation because first-pass code and tests covered named examples more
   readily than complete trust, state, transaction, and recovery boundaries.
4. **High-resolution review accounting.** Independent adversarial review
   recorded each material residual with a new stable identity instead of
   compressing multiple defects into one mutable comment.

The dominant preventable cause was not weak strategic direction. It was failure
to perform the same exhaustive boundary and negative-proof audit before
requesting code review that reviewers later performed independently.

## Classify

| Observation ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | Session record only | Review-resolution finding inventory | The distribution corrects the misleading "proposal loop" framing without requiring policy. |
| O2 | process-follow-up | pending confirmation | Possible proposal/spec-review closed-contract completeness guidance | Not yet confirmed | Automation state-machine proposals need deterministic ownership, authority, occurrence, recovery, and outcome contracts earlier. |
| O3 | process-follow-up | pending confirmation | Possible implement/code-review boundary-proof checklist | Not yet confirmed | The pattern repeated across multiple implementation milestones. |
| O4 | observation | observation | Possible future review metrics guidance | Review artifact contract and stable finding IDs | Raw counts are auditable but insufficient as a quality metric. |
| O5 | observation | observation | Session record only | Final holistic review convergence | Strong review was valuable; earlier self-audit is the optimization target. |
| O6 | process-follow-up | pending confirmation | Possible test-spec, implement, and code-review guidance | Not yet confirmed | A reusable boundary-completeness gate could reduce repeated review-resolution cycles. |

## Route

No derivative routing performed.

Contributor confirmation is unavailable for changes to proposal/spec review
guidance, implementation or code-review skills, workflow policy, validation
scripts, or learn topics. This session records evidence-bound candidate
improvements and stops.

## Best Practices

- Judge quality using finding distribution and root-cause clusters, not raw
  count alone.
- For automation proposals, close state ownership, authority binding, target
  occurrence, outcome semantics, transaction recovery, compatibility, and
  precedence before specification handoff.
- Require a stage-policy and state-transition matrix in the spec instead of
  relying on prose inference.
- Build a milestone boundary inventory before coding and map every boundary to
  direct positive, negative, stale, tamper, and restart tests.
- Derive trusted evidence from its canonical owner; do not allow callers to
  assert repository truth.
- Test the composed public path and its validation selector, not only helper
  functions.
- After every material fix, audit sibling inputs and equivalent transitions for
  the same bypass class.
- Track failed-remediation rate and final holistic escapes alongside unique
  finding count.

## No Durable Route Rationale

The session identifies likely workflow and skill improvements, but applying
them would change authoritative development guidance. The explicit learn request
confirms the retrospective, not those policy changes. Durable routing therefore
waits for contributor confirmation.
