# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review skill
Target: specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md
Status: changes-requested
Original review source: User-invoked `$spec-review` on 2026-07-28.
Material findings: SLA-SR1, SLA-SR2, SLA-SR3, SLA-SR4, SLA-SR5
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready
Automatic downstream handoff: none

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: SLA-SR1, SLA-SR2, SLA-SR3, SLA-SR4, SLA-SR5
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/spec-review-r1.md
- Review log: docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-log.md
- Review resolution: docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-resolution.md#spec-review-r1
- Open blockers: SLA-SR1, SLA-SR2, SLA-SR3, SLA-SR4, SLA-SR5
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: Resolve SLA-SR1 through SLA-SR5 and rerun spec-review before architecture assessment or downstream reliance.

## Findings

## Finding SLA-SR1

Finding ID: SLA-SR1
Severity: blocking
Location: SLA-R005 through SLA-R007; SLA-R011; State and invariants
Evidence: `artifact_states` is described as a mapping whose registered keys are the closed artifact kinds, and the invariant allows exactly one current entry for one kind. A change can legitimately contain multiple ADRs, architecture documents, specs, plans, or test specs. The current shape cannot identify which same-kind artifact a review settles, and a second artifact would either overwrite the first entry or violate the invariant.
Required outcome: Define an artifact registry that supports multiple artifacts of the same kind and gives every authoring and review transition one unambiguous target.
Safe resolution path: Key `artifact_states` by a stable change-local artifact ID. Require each entry to contain `kind` and `path`, make artifact IDs and paths unique, and bind authoring transitions, review evidence, settlement, replacement pointers, and routing dependencies to the artifact ID.
needs-decision rationale: The spec author must choose the stable artifact-ID syntax and whether one kind may designate a primary artifact. Owning stage: `spec`.

## Finding SLA-SR2

Finding ID: SLA-SR2
Severity: blocking
Location: Glossary authoring transition; Examples E1 and E3; SLA-R018 through SLA-R021; SLA-R032; Edge cases EC3
Evidence: The authoring peer changes a settled artifact to `review-required` before it begins revising content, while review eligibility and settlement also start from `review-required`. No state or authoring-completion evidence distinguishes “revision is in progress” from “the artifact is ready to review.” An independently invoked review can therefore settle partially revised content without violating the written state contract.
Required outcome: Separate invalidation during authoring from readiness for formal review, and define the complete legal transition sequence.
Safe resolution path: Add `authoring` or `revision-in-progress` as an unsettled state. Require the authoring peer to enter it before content mutation, then move to `review-required` only after durable authoring completion evidence exists. Permit review settlement only from `review-required`.
needs-decision rationale: The spec author must select the state name and authoring-completion evidence shape. Owning stage: `spec`.

## Finding SLA-SR3

Finding ID: SLA-SR3
Severity: blocking
Location: SLA-R016 through SLA-R017; SLA-R034 through SLA-R041; Inputs and outputs; State and invariants; AC-SLA-013 through AC-SLA-014
Evidence: The spec removes current milestone, milestone state, review status, remaining milestones, next stage, and final-closeout readiness from the plan. It then defines `workflow_state` with only lifecycle state, current stage, next stage, blocker, and evidence. No authoritative field remains for the current milestone occurrence, milestone state, remaining in-scope milestones, review round, or final-closeout readiness. Repeated `implement` and `code-review` targets cannot bind or resume deterministically, and workflow cannot prove final verification eligibility.
Required outcome: Assign every displaced planned-initiative live-state fact to one exact change-local owner with closed values and consistency rules.
Safe resolution path: Extend `workflow_state` with a structured planned-work block containing current milestone ID, milestone state, latest review reference, remaining milestone IDs, and final-closeout readiness plus reason codes. Enumerate the complete stage registry, blocker representation, evidence type, milestone transitions, and repeated-stage occurrence binding.
needs-decision rationale: The spec author must choose the minimal planned-work schema while preserving milestone resumability and final-closeout proof. Owning stage: `spec`.

## Finding SLA-SR4

Finding ID: SLA-SR4
Severity: major
Location: SLA-R024; SLA-R035 through SLA-R037; SLA-R048 through SLA-R059; Inputs and outputs; Error and boundary behavior
Evidence: Several purportedly closed contracts remain open-ended. ADR approval maps to `accepted` or `active` “according to the reviewed decision” without a required decision field. The standard stage registry is not enumerated. `blocker`, `evidence`, maximum path root, mutation categories, external-action policy, structured target, and target-consent transition legality have no types or closed values. Effective capabilities have no required identity binding to target consent. Validators and adapters would have to invent these schemas and transitions.
Required outcome: Define exact closed data shapes and legal transitions for review settlement, routing state, target consent, and capability derivation.
Safe resolution path: Reuse existing structured-target, capability, receipt, path-scope, and mutation-category contracts where retained; enumerate every new or changed field and state transition; require capabilities to bind the target-consent identity; and replace the ambiguous ADR mapping with an explicit reviewed settlement value.
needs-decision rationale: The spec author must choose which existing automation vocabularies are preserved unchanged and define exact replacements for the rest. Owning stage: `spec`.

## Finding SLA-SR5

Finding ID: SLA-SR5
Severity: blocking
Location: Normative amendment registry; SLA-R002 through SLA-R003; SLA-R065 through SLA-R067; AC-SLA-027
Evidence: Current approved specs directly require artifact-local status, active-plan ownership of current handoff, prohibition on change-local next-stage authority, and separate risk-class authorization. The draft uses broad “superseded where conflicting” language and assigns exact selector-level disposition to the downstream implementation change. Implementation cannot decide normative precedence, and the current automation spec itself requires exact affected-selector accounting to avoid two writable authorities.
Required outcome: Settle exact normative ownership and compatibility precedence in the specification before approval.
Safe resolution path: Add a closed selector-level disposition ledger covering every affected requirement, example, acceptance criterion, and public alias in the four named specs. Give each selector one disposition such as preserved, preserved-rebound, or superseded; add reciprocal amendment notices to the owning specs in the same approval change; and require a static completeness and duplicate-selector check.
needs-decision rationale: The spec author must own the exact normative disposition set; architecture and implementation may not infer it. Owning stage: `spec`.

## Review Dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | block | Artifact identity, authoring readiness, milestone ownership, and several state fields are ambiguous. |
| normative language | concern | Requirements use firm language, but open-ended closed registries and “where conflicting” precedence weaken it. |
| completeness | block | Same-kind artifacts, in-progress authoring, planned-work state, legal transitions, and exact amendments are missing. |
| testability | block | Validators cannot construct deterministic fixtures for the incomplete shapes and transition tables. |
| examples | concern | Normal and isolation flows are useful, but multi-artifact, mid-revision, milestone-resume, and conflicting-authority examples are absent. |
| compatibility | block | Current approved owners conflict directly, and selector disposition is deferred downstream. |
| observability | concern | Status output is described, but the missing authoritative milestone and field schemas make it underdetermined. |
| security/privacy | pass | Repository-local scope, external-action prohibition, credential boundaries, and diagnostic limits are explicit. |
| non-goals | pass | Hashing, interception, hosted state, selective reuse, and external automation remain clearly excluded. |
| acceptance criteria | block | Several criteria are not implementable until the missing identities, owners, shapes, and dispositions are settled. |

## Exact Wording Suggestions

- Replace artifact-kind keys with stable artifact IDs and store `kind` inside
  each entry.
- Add an in-progress authoring state and permit review only after an explicit
  transition to `review-required`.
- Add the displaced planned-work facts to `workflow_state` with closed
  milestone and readiness vocabularies.
- Enumerate the stage, blocker, evidence, target-consent, scope, mutation, and
  legal-transition registries.
- Replace implementation-owned amendment discovery with an exact
  specification-owned selector ledger.

## Recommendation

Changes requested.
Revise the spec against SLA-SR1 through SLA-SR5, then rerun `spec-review`.
Eventual test-spec readiness is `not-ready` because proof cases cannot be
mapped without inventing the missing contracts.
This direct review is isolated and does not start architecture, planning, test
specification, implementation, or workflow automation.
