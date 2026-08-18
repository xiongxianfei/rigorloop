# Proposal Review: Explain-Change Skill Simplification

Review ID: proposal-review-r2
Stage: proposal-review
Round: 2
Reviewer: user-supplied independent proposal-review result, recorded by Codex
Target: `docs/proposals/2026-08-18-explain-change-skill-simplification.md`

Reviewed artifact: `docs/proposals/2026-08-18-explain-change-skill-simplification.md` at `sha256:943cf2a7b15ef59838a5a9cc3ea78c117b71afeb479d43cf9bac673f1190be9f`
Review date: 2026-08-18
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: EXCSIM-PR4, EXCSIM-PR5, EXCSIM-PR6
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision followed by same-stage rereview
- Automatic downstream handoff: none
- Claim limitations: this isolated review records judgment only; it does not settle the portable proposal or continue workflow

## Overall assessment

The selected package boundary remains appropriate:

```text
compact universal SKILL.md
+ one governed-workflow reference
+ one structural explanation skeleton
+ no scripts
```

Universal actual-diff grounding, truthfulness, scope, validation gaps, stops, claims, and resource selection remain inline. Governed eligibility, final-review and diff-basis validation, review closeout, placement, staleness, and workflow handback belong in the conditional reference. Portable and governed contexts fail closed, the skill writes only its artifact, and acceptance avoids target-agent execution.

Three contracts remain incomplete: refresh and resource loading disagree, the reviewed code state is conflated with the later explanation write, and the proposed `Verify readiness` structure exceeds explain-change's claim authority.

## Material findings

### EXCSIM-PR4 - Durable refresh contradicts the assembly and skeleton-loading model

Finding ID: EXCSIM-PR4
Severity: major
Location: loaded assemblies, durable write protocol, and structural asset ownership
Evidence: `EC1` and `EC3` declare that every durable action loads the skeleton, while the refresh rule permits preserving a historical structure without using it. This makes the four assemblies, missing-resource behavior, measurement, and refresh authority non-exhaustive.
Required outcome: Choose one first-version durable-refresh contract with exhaustive loading and mutation semantics.
Safe resolution path: Compose every durable create and refresh from the current skeleton and replace the complete file after identity revalidation. Require an absent exact target for create and an existing exact target plus explicit current refresh authority for refresh. Exclude section-level refresh, mixed ownership, managed regions, and historical-layout parsing. Leave historical artifacts untouched until a genuine refresh occurs.

### EXCSIM-PR5 - Reviewed code state and the later explanation evidence write are conflated

Finding ID: EXCSIM-PR5
Severity: major
Location: governed explanation basis, staleness, and workflow order
Evidence: Final code review precedes explain-change, so a durable explanation changes the branch after the reviewed subject was fixed. Treating the later branch diff as the final reviewed diff makes the explanation self-stale and fails to distinguish the reviewed subject, recording revision, and verify handoff revision.
Required outcome: Represent the reviewed change basis separately from the explanation recording and handoff revisions.
Safe resolution path: Define the reviewed diff as base revision to reviewed-subject revision. Permit the handoff revision to equal that subject or to add one direct-child explain-change-owned evidence commit containing only the explanation artifact and any already-authorized matching evidence fields. Broader or unexplained post-review changes invalidate final-review reuse. Later verify-owned evidence alone does not stale the explanation.

### EXCSIM-PR6 - `Verify readiness` conflicts with workflow and verify ownership

Finding ID: EXCSIM-PR6
Severity: major
Location: explanation skeleton and readiness/routing ownership
Evidence: A structural group named `Verify readiness` can imply that explain-change authorizes verify, branch, PR, release, or lifecycle readiness, despite the proposal assigning next-stage routing to workflow and final readiness to verify.
Required outcome: Limit the conditional group to explain-change-owned facts.
Safe resolution path: Rename it `Workflow handback`. Report only explanation status and basis, validation cutoff, explain-change blockers, whether control returns to workflow, and workflow as the next-stage decision owner. Forbid verification, branch, PR, release, and lifecycle readiness claims.

## Architecture assessment

The expected outcome remains `architecture-not-required` only when existing evidence can represent the reviewed subject, explanation recording revision, handoff revision, allowed evidence tail, and atomic replacement. A new persistent identity model, transaction record, lifecycle state, or write owner requires architecture work.

## Acceptance criteria requested

Add `AC-EXCSIM-013` through `AC-EXCSIM-024` covering one durable composition rule, exhaustive assemblies, explicit refresh authority, no implicit governed state, separate reviewed and recording revisions, a closed evidence tail, no readiness overclaim, later verify evidence, and the architecture boundary.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The overloaded flat package and repeated structure are concrete. |
| Decision rationale | pass | One governed reference and one skeleton remain proportionate. |
| Universal truthfulness | pass | Diff, evidence, stops, claims, and triggers remain inline. |
| Output-action model | block | Refresh composition and loading are not exhaustive. |
| Reviewed-state identity | block | Reviewed subject and later evidence revisions are not separate. |
| Claim ownership | block | `Verify readiness` can overreach workflow and verify. |
| Atomic write model | pass with revisions | Whole-file replacement is sound after refresh scope is closed. |
| Testing boundary | pass | Static and package proof are proportionate. |
| Architecture awareness | concern | No-architecture depends on existing evidence-tail support. |
| Readiness for spec | changes-requested | Resolve EXCSIM-PR4 through EXCSIM-PR6. |

## Recommendation

Retain the package direction, revise the proposal to close EXCSIM-PR4 through EXCSIM-PR6, and perform a fresh same-stage proposal review. No automatic downstream handoff follows.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-18-explain-change-skill-simplification-review-recording/reviews/proposal-review-r2.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: `proposal-review-r2`
- Review log: `docs/changes/2026-08-18-explain-change-skill-simplification-review-recording/review-log.md`
- Review resolution: `docs/changes/2026-08-18-explain-change-skill-simplification-review-recording/review-resolution.md#proposal-review-r2`
- Proposal settlement: not-settled; the recording-only root has no proposal lifecycle authority
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview
