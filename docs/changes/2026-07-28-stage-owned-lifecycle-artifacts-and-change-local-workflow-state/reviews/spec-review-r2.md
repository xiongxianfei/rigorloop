<!-- Template: spec-review-result-skeleton-v1 -->
<!-- Skill: spec-review -->
<!-- Template status: normative -->

# Spec Review R2

Review ID: spec-review-r2
Stage: spec-review
Round: 2
Reviewer: Codex spec-review skill
Target: specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md
Status: changes-requested
Original review source: User-invoked `$spec-review` after requested spec revision on 2026-07-28.
Material findings: SLA-SR6, SLA-SR7, SLA-SR8
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready
Automatic downstream handoff: none

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: SLA-SR6, SLA-SR7, SLA-SR8
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/spec-review-r2.md
- Review log: docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-log.md
- Review resolution: docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-resolution.md#spec-review-r2
- Open blockers: SLA-SR3, SLA-SR4, SLA-SR5, SLA-SR6, SLA-SR7, SLA-SR8
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: Resolve SLA-SR3 through SLA-SR8 and rerun spec-review before architecture assessment or downstream reliance.

## Findings

## Finding SLA-SR6

Finding ID: SLA-SR6
Severity: blocking
Location: SLA-R037d through SLA-R037p; Example E13; AC-SLA-030
Evidence: The new planned-work block owns milestone order and names one `latest_review`, but that review has no artifact ID, occurrence kind, or milestone ID. It therefore cannot distinguish the review for the current implementation milestone from a prior milestone or another reviewed artifact. In addition, `final_closeout.readiness: ready` is constrained only to the reason `ready`; no rule derives readiness from closed implementation milestones, closed required review resolution, clean final holistic review, current explanation, fresh verify evidence, and PR-handoff state. A syntactically valid record can therefore bind the wrong review or claim readiness while required work remains open.
Required outcome: Make current review and final-closeout state mechanically derivable from the exact milestone occurrence and required stage evidence.
Safe resolution path: Add artifact and occurrence identity to `latest_review`, require milestone ID for milestone reviews, reset or rebind the review when `current_milestone` advances, and define positive-evidence consistency rules for every final-closeout readiness value and reason code.
needs-decision rationale: none

## Finding SLA-SR7

Finding ID: SLA-SR7
Severity: major
Location: SLA-R012a through SLA-R012b; SLA-R037; SLA-R055a through SLA-R056; compatibility references
Evidence: The terminal transition contract points to ownership clauses but does not enumerate legal source-to-destination transitions or state whether terminal states are terminal. The closed stage registry omits standard `explore`, `research`, and `learn` stages from the governing workflow, even though this proposal explicitly preserves learning after operational settlement. The capability schema does not contain a target or external-action field, while SLA-R055b and SLA-R056 require the capability's target and external-action policy to be subset-validated. Finally, retained automation behavior is referenced through open-ended requirement ranges, leaving exact capability fields and semantics to inference.
Required outcome: Provide one internally consistent closed transition, stage, and capability contract that covers every retained lifecycle stage and every field used by subset validation.
Safe resolution path: Enumerate terminal transitions and terminality; add the applicable on-demand and periodic stages or explicitly define why they never occupy routing state; add or explicitly inherit target and external-action values in the capability shape; and replace open-ended retained-contract ranges with exact selectors.
needs-decision rationale: none

## Finding SLA-SR8

Finding ID: SLA-SR8
Severity: blocking
Location: Normative amendment registry; SLA-R074a through SLA-R074d; repository diff
Evidence: The source-selector tables now contain 323 existing selectors with no duplicate or nonexistent selector, which resolves the registry-key ambiguity. However, SLA-R074a makes reciprocal notices in four owning specs a condition of this specification's approval, and none of those notices is present. The revised spec also uses open-ended `through` references for retained and replacement requirements even though SLA-R074c requires rejection of open-ended prose ranges used as normative precedence. Current approved contracts therefore remain conflicting at the requested approval gate.
Required outcome: Satisfy the specification-owned approval prerequisites and leave one exact current authority for activated changes.
Safe resolution path: Add matching reciprocal notices to all four owning specs, replace every normative range reference with exact selectors or one explicitly named replacement contract, and run a duplicate, existence, and reciprocal-consistency check before the next review.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | block | Planned review identity and readiness derivation remain ambiguous. |
| normative language | concern | Firm language remains internally inconsistent where absent capability fields and open ranges are referenced. |
| completeness | block | Terminal transitions, standard stages, closeout proof, and reciprocal notices are incomplete. |
| testability | block | Fixtures cannot determine valid final readiness or capability subset checks without inventing rules. |
| examples | concern | Multi-artifact and interrupted-authoring examples are strong; the milestone example does not settle review identity or readiness proof. |
| compatibility | block | Reciprocal notices required by the spec are absent at the approval gate. |
| observability | concern | Status fields exist, but latest-review identity and truthful final readiness remain underdetermined. |
| security/privacy | concern | External actions remain prohibited, but the capability subset schema lacks the field it says to validate. |
| non-goals | pass | Hashes, interception, selective reuse, hosted state, and automatic external actions remain clearly excluded. |
| acceptance criteria | block | AC-SLA-030 through AC-SLA-032 cannot yet be proven without filling the remaining contracts. |

## Confirmed R1 resolutions

- SLA-SR1 is resolved: stable unique artifact IDs, paths, roles, multi-artifact examples, and review binding remove same-kind ambiguity.
- SLA-SR2 is resolved: `authoring` is distinct from `review-required`, review settlement accepts only review-ready artifacts, and interruption behavior is explicit.

## Exact wording suggestions

- Make `latest_review` identify `artifact_id`, occurrence kind, and milestone ID when applicable.
- Define `final_closeout.readiness` as a positive-evidence conjunction rather than a freely writable label.
- List all legal terminal transitions and all stages that may occupy routing state.
- Make capability target and external-action inheritance explicit and replace range references with exact selectors.
- Land the four reciprocal amendment notices before requesting approval again.

## Recommendation

Changes requested.
The revised spec materially improves identity and authoring isolation, but
planned-work proof, closed capability/state schemas, and normative precedence
still require guessing.
This direct review is isolated and does not start architecture, planning, test
specification, implementation, or workflow automation.
