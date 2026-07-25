# Code Review M6 R6

Review ID: code-review-m6-r6
Stage: code-review
Round: M6 R6
Reviewer: independent same-session context-reset reviewer
Target: M6 correction commit `df0ca693`
Reviewed artifact: M6 correction commit `df0ca693`
Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
Status: clean-with-notes
Review status: clean-with-notes
Review date: 2026-07-25
Recording status: recorded
Material findings: None
Immediate next stage: final holistic code-review

## Review context

- Invocation mode: direct isolated milestone rereview
- Independence level: `L1-same-session-context-reset`
- Review surface: commit `df0ca693` against parent `27b69385`
- Requirement-fidelity gate: applied to `BRF-R032`, `BRF-R068` through `BRF-R077`, T28, and T30
- Risk tier: elevated
- Automated independent-review gate: not required for this direct isolated invocation
- Context limitation: the reviewer shares the implementation session, intentionally reset to the governing recovery requirements and actual commit before challenging the released validation evidence, and does not claim blind L2 independence

## Independent risk map

### Affected behavior

- Prepared proposal-correction transition recovery.
- Replacement proposal-review capability derivation.
- New versus persisted capability timestamp requirements.
- M6 milestone closeout and final holistic review handoff.

### Highest-impact failure modes

- A resume-only timestamp silently rebinds replacement authority.
- Omitting a resume-only timestamp prevents valid prepared-transition reconciliation.
- Relaxing the timestamp requirement permits creation of new authority without a valid derivation time.
- Recovery replays the proposal mutation or creates duplicate replacement capabilities.

### Changed boundaries

- `scripts/workflow_automation.py`: persisted-capability reuse and replacement capability derivation.
- `scripts/test-workflow-automation.py`: altered and omitted recovery timestamp contrasts.
- Change-local review resolution and active-plan handoff state.

### Expected evidence

- Replacement authority uses the persisted correction capability's validated timestamp.
- Altered and omitted resume timestamps produce the same replacement authority timestamp.
- New capability derivation still requires an RFC3339 UTC timestamp.
- The original receipt completes without proposal replay, the correction capability is consumed, and exactly one fresh proposal-review capability becomes active.

### Direct-inspection areas

- `derive_post_correction_capabilities`.
- The persisted versus new capability branches in `coordinate_one_stage`.
- Both public proposal-correction process-loss regressions.
- Existing capability-derivation and prepared-receipt tests.

### Intentionally out-of-scope areas

- Final holistic review of the complete M1-M6 diff.
- `explain-change`, final `verify`, and PR handoff.
- Unchanged public aliases, migration projection, generated adapters, and external-action boundaries.

### Risk classes

- Applicable: durable authority, interruption recovery, deterministic state, correction replay, and audit integrity.
- Not applicable: personal-data processing, cryptographic protocol design, accessibility UI, and deployed-service availability.

### Falsifiable questions

- Can an altered recovery timestamp change replacement authority?
- Can valid recovery proceed when the resume request omits a timestamp?
- Can a genuinely new capability be created without a derivation timestamp?
- Does either recovery variant replay mutation, replace the receipt, or activate more than one fresh capability?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review receipt, `review-log.md`, `review-resolution.md`, `change.yaml`, active plan, and plan index
- Open blockers: none for M6 milestone closeout
- Next stage: final closeout, beginning with final holistic code-review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m6-r6.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m6-r6`; no new finding resolution required
- Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
- Milestone closeout: closed
- Remaining implementation milestones: none
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Clean-review sufficiency receipt

- Review target identity: commit `df0ca693`
- Independence level: `L1-same-session-context-reset`
- Governing artifacts inspected: `BRF-R032`, `BRF-R068` through `BRF-R077`, T28, T30, the active M6 plan, and the accepted `BRF-M6-CR11` resolution
- Risk classes considered: durable authority, interruption recovery, deterministic state, mutation replay, audit integrity, compatibility, generated artifacts, and scope containment
- Adversarial hypotheses tested: altered resume timestamp, omitted resume timestamp, missing timestamp for new capability creation, mutation replay, receipt replacement, and duplicate replacement authority
- Direct proofs performed: five focused recovery/authority tests and the full 73-test engine suite passed; both process-loss variants complete the original receipt without mutation replay, consume the original correction capability, preserve proposal/review bytes, and activate one fresh capability with the persisted timestamp
- Validation evidence challenged: the implementation's selected-CI and broad-smoke records were treated as supporting evidence; the reviewer independently reran focused contrasts and the complete engine suite against the actual commit
- Unreviewed or uncertain surfaces: complete cross-milestone final diff, final explanation, final verification, and PR handoff
- Confidence: high for the bounded R6 correction
- No-finding rationale: The new-capability branch retains mandatory timestamp validation, while every persisted-capability execution and recovery path uses the validated durable record. Resume-only timestamp presence or value cannot affect the receipt or activated authority, and the direct proof retains no-replay and atomic settlement assertions.

## Review inputs

- Review surface: commit `df0ca693` against parent `27b69385`.
- Tracked governing branch state: approved specification, approved test specification, approved architecture, accepted ADR, active M6 plan, and closed `BRF-M6-CR11` resolution are tracked.
- Direct review proof: altered and omitted recovery timestamps, new-capability derivation, prepared-receipt creation, no-caller-callback correction, and the complete engine suite.
- Released validation evidence: 73 engine, 60 state/recovery, 68 automation-validator, and 16 policy tests; Python compilation; 12 selected CI checks; and 11-check broad smoke.

## Diff summary

The correction changes replacement proposal-review capability derivation to use the persisted correction capability's `derived_at` instead of the current resume request.

It makes `derived_at` conditional in `coordinate_one_stage`: persisted capability execution does not require a new timestamp, while the branch that derives a new capability still rejects omission.

The process-loss proof now runs altered and omitted resume-timestamp variants and verifies that both retain the original durable capability timestamp.

## Prior-finding reconciliation

| Prior finding | R6 result | Evidence |
| --- | --- | --- |
| `BRF-M6-CR11` | resolved | Replacement authority reads `derived_at` from the persisted capability; altered and omitted resume inputs both settle with `2026-07-22T00:01:00Z`. |
| `BRF-M6-CR10` | resolved | Both R6 variants retain same-receipt completion, no mutation replay, original capability consumption, historical review preservation, and exactly one fresh proposal-review capability. |

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | Persisted authority controls recovery, and valid completion evidence reconciles the prepared receipt without rerunning the stage as required by `BRF-R032` and `BRF-R074`. |
| Test coverage | pass | Altered and omitted timestamp contrasts exercise the reproduced defect; new-capability and ordinary correction controls remain covered. |
| Edge cases | pass | Recovery is independent of resume timestamp presence/value, while genuinely new authority still requires a valid derivation timestamp. |
| Error handling | pass | Missing `derived_at` fails before capability creation only when no persisted capability exists. |
| Architecture boundaries | pass | Authority remains in the persisted effective capability, and the coordinator/state writer boundary is unchanged. |
| Compatibility | pass | Public command forms, legacy adapters, migration semantics, and state schema are unchanged. |
| Security/privacy | pass | The correction removes caller influence over durable authority and introduces no secret, credential, or external-action surface. |
| Derived artifact currency | pass | No canonical skill or generated adapter source changed. |
| Unrelated changes | pass | The implementation diff is limited to recovery authority, its regression proof, and required lifecycle synchronization. |
| Validation evidence | pass | Five independent focused tests and all 73 engine tests pass; recorded selected CI and broad smoke cover the wider repository boundary. |

## Requirement-fidelity result

| Contract property | Result | Evidence |
| --- | --- | --- |
| Only active effective capability authorizes the operation | pass | Recovery locates and validates the persisted active correction capability before settlement. |
| Prepared receipt reconciles valid completion without rerun | pass | Both recovery tests trap every attempted second proposal replacement. |
| Resume is deterministic across process-local input | pass | Altered and omitted timestamps produce the persisted replacement-authority timestamp and identical settlement predicates. |
| New authority remains basis-complete | pass | The new-capability branch retains the required `derived_at` check and delegates RFC3339 validation to capability derivation. |
| At most one replacement review capability activates | pass | Both recovery variants assert exactly one active proposal-review capability after consuming the correction capability. |

## No-finding rationale

The correction fixes the authority source rather than validating one special resume value. The callback receives the persisted capability selected and checked by the coordinator, and replacement capability derivation uses that record. Removing `derived_at` from the unconditional request field set does not weaken new authority creation because the derivation branch performs the requirement immediately before mutation or persistence. Direct process-loss proof covers altered and omitted inputs while retaining the original no-replay and atomic-settlement assertions. No contradictory in-scope evidence was found.

## Residual risks

- M6 is the final implementation milestone, but a separate final holistic code review must assess the complete M1-M6 diff and cross-milestone interactions.
- `explain-change`, final verification, and PR handoff remain pending.
- The existing lifecycle merge-language warning remains non-blocking baseline evidence.

## Milestone handoff

- Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
- Review status: clean-with-notes
- Milestone state after review: closed
- Required review-resolution: no; all 103 material findings are resolved
- Remaining in-scope implementation milestones: none
- Next stage: final closeout, beginning with final holistic code-review
- Final closeout readiness: not ready; final holistic review, explanation, verification, and PR handoff remain

This direct review is isolated and does not start final holistic code-review automatically.
