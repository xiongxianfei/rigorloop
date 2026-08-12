# Proposal Review R2: Spec-Review Skill Simplification

Review ID: proposal-review-r2
Stage: proposal-review
Round: r2
Reviewer: user-supplied independent proposal-review result
Target: `docs/proposals/2026-08-12-spec-review-skill-simplification.md`
Reviewed artifact: commit `ff0b0453`
Review date: 2026-08-12
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: SRSIM-R2-PR1, SRSIM-R2-PR2, SRSIM-R2-PR3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-12-spec-review-skill-simplification/reviews/proposal-review-r2.md`
- Review log: `docs/changes/2026-08-12-spec-review-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-12-spec-review-skill-simplification/review-resolution.md`
- Open blockers: classification, isolated recording authority, and primary simplification acceptance require proposal revision
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: no specification, implementation, verification, branch, or PR readiness is claimed

## Overall assessment

The package direction remains sound: a compact universal `SKILL.md`, one recording-and-settlement reference, two existing governed boundary references, and two existing structural assets. Universal judgment remains inline, boundary activation retains its existing owner, resource loading does not grant authority, and runtime-agent acceptance remains excluded.

Three proposal contracts remain open. The review kind and recording model permits a non-formal durable state with no resource assembly, minimal recording-root creation is not bounded to the exact existing formal-review contract and permitted write set, and the primary formal loaded profile is not yet required to shrink.

## Material findings

### SRSIM-R2-PR1 — Major: non-formal required recording has no valid resource profile

Finding ID: SRSIM-R2-PR1
Severity: major
Location: Review classification and authority axes; Closed loaded-resource profiles
Evidence: The proposal treats recording mode as independent, permits non-formal recording when separately required, and omits the recording reference from both non-formal profiles.
Required outcome: Derive recording from review kind so every formal review records, non-formal feedback never writes durable spec-review evidence or emits lifecycle status, and a durable-record request promotes the invocation to isolated formal review.
Safe resolution path: Remove `recording_mode` as an independent axis, define exhaustive formal-review triggers and non-formal conditions, and retain only the three closed axes and four resource profiles recommended by the review.
needs-decision rationale: none

### SRSIM-R2-PR2 — Major: minimal recording-root creation lacks a closed write boundary

Finding ID: SRSIM-R2-PR2
Severity: major
Location: Recording and settlement side effects; Recording-and-settlement reference ownership
Evidence: The proposal permits a direct formal review to create a minimal recording root without citing the exact governing requirement IDs, enumerating permitted artifacts, prohibiting governed mutations explicitly, or closing failure behavior when placement cannot be resolved.
Required outcome: Reuse `specs/formal-review-recording.md` requirements `R31a` through `R31n`, enumerate the isolated write set, prohibit governed settlement, plan, automation, and lifecycle mutation, and block formal completion when no location is safely selectable.
Safe resolution path: Add the exact change-ID order and artifact boundary from the existing contract without inventing a new placement model.
needs-decision rationale: none

### SRSIM-R2-PR3 — Major: primary loaded-profile reduction is not an acceptance requirement

Finding ID: SRSIM-R2-PR3
Severity: major
Location: Preservation and measurement; Expected Behavior Changes
Evidence: Every supported direct `spec-review` loads the recording reference, but acceptance currently requires only main-file reduction and permits the isolated formal loaded profile not to shrink when explained.
Required outcome: Make `SR1-isolated-formal` loaded words and UTF-8 bytes decrease from baseline, require one loaded owner for every duplicate cluster, report governed profiles and total package separately, and preserve semantic behavior without a fixed percentage gate.
Safe resolution path: Replace the current supporting-only formal-profile language with closed simplification success criteria and explicit measurement assemblies.
needs-decision rationale: none

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path and duplicate ownership costs remain concrete. |
| User value | pass | The intended review experience and maintenance benefit are clear. |
| Option diversity | pass | The proposal compares materially different package and runtime alternatives. |
| Decision rationale | pass | One new reference remains proportionate. |
| Vision fit | pass | The direction aligns with inspectable, durable workflow evidence. |
| Scope control | pass | Work remains limited to `spec-review` and directly coupled contracts. |
| Architecture awareness | pass | A bounded assessment with expected `architecture-not-required` remains appropriate. |
| Testability | block | Classification, isolated writes, and primary profile success are not yet closed. |
| Risk honesty | concern | Package growth can still be accepted without solving the primary context problem. |
| Rollout realism | pass | Atomic package rollout and parity remain sound. |
| Readiness for spec | block | SRSIM-R2-PR1 through SRSIM-R2-PR3 require revision. |

## Scope preservation review

All initial user goals remain classified and in scope. The findings refine the selected package without adding runtime, assets, lifecycle schema, or another skill.

## Recommendation

Revise the proposal to derive recording from review kind, bind isolated recording to `R31a` through `R31n` with an explicit write boundary, and make isolated-formal loaded-profile reduction normative. Then rerun independent proposal review against the frozen revision.
