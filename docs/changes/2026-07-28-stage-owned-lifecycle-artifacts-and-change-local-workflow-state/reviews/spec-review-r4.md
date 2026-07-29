<!-- Template: spec-review-result-skeleton-v1 -->
<!-- Skill: spec-review -->
<!-- Template status: normative -->

# Spec Review R4

Review ID: spec-review-r4
Stage: spec-review
Round: 4
Reviewer: Codex spec-review skill
Target: specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md
Status: changes-requested
Original review source: User-requested review after Constitution alignment,
published-skill ownership updates, and automation simplification on
2026-07-28.
Material findings: SLA-SR10
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready
Automatic downstream handoff: none

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: SLA-SR10
- Recording status: recorded
- Recording blocker: none
- Review record:
  docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/spec-review-r4.md
- Review log:
  docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-log.md
- Review resolution:
  docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-resolution.md#spec-review-r4
- Open blockers: SLA-SR10
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: Close the remaining same-rank compatibility conflicts and
  rerun spec-review before architecture assessment.

## Findings

## Finding SLA-SR10

Finding ID: SLA-SR10
Severity: blocking
Location: SLA-R074c through SLA-R074d; published-skill assets; approved
specifications that still require embedded status or downstream settlement
Evidence: The revised Constitution, AGENTS guidance, workflow guide, main
specification, and canonical published skills consistently make
`change.yaml` the sole mutable state owner. However,
`formal-review-recording.md`,
`downstream-status-settlement-before-reliance.md`,
`proposal-family-assets-progressive-disclosure.md`,
`spec-family-assets-progressive-disclosure.md`,
`review-finding-resolution-contract.md`,
`review-skill-family-consistency-parser-owned-finding-shape.md`,
`stage-evidence-access-contracts-for-cost-bounded-rigor.md`,
`stop-tracking-generated-public-adapter-skill-bodies.md`, and
`workflow-stage-autoprogression.md` retain approved requirements that require
artifact-local status or downstream status normalization. SLA-R074c names
only four source specifications, and SLA-R074d keeps every unlisted
same-rank requirement authoritative. A governed change would therefore have
two incompatible write contracts.
Required outcome: Establish one same-rank normative answer for embedded
status and downstream status settlement before approval.
Safe resolution path: Add a concise reciprocal subject-level notice to each
directly conflicting specification and list those sources in SLA-R074c with
the exact replaced subject and retained behavior. Keep historical records
read-only. Do not add requirement selectors, hashes, runtime interception, or
another automation parameter.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | pass | Stage writers, review-peer settlement, workflow routing, and downstream route-back are explicit. |
| normative language | pass | The selected target is now the complete public automation boundary and stage ownership remains fixed. |
| completeness | block | Same-rank conflicting status contracts remain outside the closed compatibility set. |
| testability | pass | Closed state, automation, stage ownership, and boundary requirements are directly testable. |
| examples | pass | Examples cover independent review, workflow continuation, downstream challenge, historical reads, and single-target automation. |
| compatibility | block | Unlisted approved status-settlement requirements contradict the new contract. |
| observability | pass | Status output and evidence pointers are defined without hashes or writer attribution. |
| security/privacy | pass | Repository-local scope and external-action prohibition remain explicit. |
| non-goals | pass | Hashes, interception, hosted state, amendment machinery, and selective reuse remain excluded. |
| acceptance criteria | concern | AC-SLA-027 and AC-SLA-032 are sound only after the complete conflicting source set is closed. |

## Confirmed prior-finding resolution

SLA-SR9 is resolved.
`CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, and `docs/project-map.md`
now assign mutable lifecycle state to `change.yaml`, make governed plans and
artifacts stable, and prohibit downstream write-back.

The revised automation contract also removes parent authorization, effective
capability, profile, and selector-ledger mechanisms.
One structured target is the complete public repository-local automation
boundary, while current prerequisites and fixed stage ownership still gate
each transition.

## Recommendation

Changes requested.
The behavior contract is substantially simpler and the public skill guidance
now reflects the intended mechanism, but same-rank compatibility must be
closed before approval.

This direct review is isolated and does not start architecture, planning, test
specification, implementation, or workflow automation.
