# ADR-20260625-independent-adversarial-review-gates: Independent Adversarial Review Gates for Automated Workflows

## Status

accepted

## Context

RigorLoop's autoprogression profiles reduce redundant human routing prompts, but automated handoff creates an independence risk when the same authoring context writes the artifact, knows the intended solution, runs validation, invokes review, and benefits from a clean result.

Existing review guidance already asks reviewers to inspect tracked artifacts and prefer fresh sessions. That is no longer enough for workflow-managed automation because context leakage, validation-result anchoring, prior-finding anchoring, and continuation incentives can all make a nominal review behave like authoring continuation.

The approved review-independence spec defines the structural contract for automated review gates. This is a durable architecture decision because it changes workflow orchestration, review invocation evidence, risk classification, clean-review handoff eligibility, second-review calibration, final holistic review requirements, and the boundary between reviewer verdict ownership and orchestrator continuation ownership.

## Decision

Add an independent adversarial review gate to workflow-managed automated reviews.

The orchestrator owns the process boundary:

```text
review invocation manifest
initial-packet inventory and hash
prompt template version
reviewer context identity
risk-tier classification
phase receipts
derived review_gate_outcome
second-review routing
autoprogression handoff eligibility
```

The reviewer owns the judgment boundary:

```text
independent risk map
adversarial hypotheses
direct inspection
evidence challenge
finding discovery
severity and required outcome
stage-native verdict
confidence
clean-review sufficiency receipt
prior-finding reconciliation
```

Automated reviews cannot advance from `L0` author-continuation mode. Standard-risk automated reviews require at least verifiable L1 fresh context. Elevated-risk reviews require L2 separation and the configured second-review policy. Critical-risk reviews require L3 authority, with human authority required for irreversible external actions.

The initial packet contains tracked artifacts, revisions, hashes, formal criteria, governing artifacts, review target identity, and neutral routing metadata. It excludes author hidden reasoning, desired review outcome, validation-result summaries, evidence menus, implementation safety narrative, prior finding content, and auto-fix budget before the reviewer records the initial risk map.

The review proceeds through blind-first evidence staging:

```text
initial packet
-> risk-map-recorded
-> evidence-menu-released
-> evidence-results-released
-> prior-findings-released
-> verdict-recorded
```

The orchestrator records immutable phase receipts and treats missing receipts, early forbidden-context release, invalid manifests, insufficient clean receipts, unresolved findings, second-review disagreement, `blocked`, and `inconclusive` as ineligible for automatic clean handoff.

The review gate preserves stage-native verdicts and derives a normalized `review_gate_outcome` for orchestration. A derived `stop` from native `changes-requested` means the review did not produce a clean advance; it may route to `review-resolution` only when an active profile independently authorizes that route and all independence, evidence, and correction-loop gates pass. Native `blocked` and `inconclusive` pause regardless of profile authorization.

Calibration is required evidence, not an optional dashboard. Rollout samples standard-risk clean automated reviews, second-reviews elevated-risk clean reviews, records downstream escapes, measures seeded-defect recall, separates recurrence detection from novel-defect detection when possible, and tracks quality metrics by review skill and risk tier. Protected rotating fixtures are preferred for measured calibration runs; public fixtures document defect classes.

No new hosted service, database, persistent external control plane, deployment target, or network dependency is introduced.

## Alternatives considered

### Require a finding in every review

Rejected because finding quotas reward noise, punish genuinely clean work, and move quality measurement away from defect sensitivity.

### Strengthen review prompts only

Rejected because prompt-only instructions do not prevent author-context leakage, outcome anchoring, validation anchoring, or fix-confirmation-only rereviews under automation.

### Always use a different model or vendor

Rejected as the base rule because model heterogeneity does not guarantee independence when the same biased evidence packet is supplied. It remains a risk-tier control for configured elevated or critical cases.

### Require human review for every automated stage

Rejected as the default because it removes most automation value and still does not solve evidence anchoring by itself. Human authority remains required for irreversible external actions and may be configured for other critical-risk triggers.

## Consequences

- Automated review handoff becomes more expensive because each gate records manifests, phase receipts, risk maps, evidence challenges, and clean-review sufficiency evidence.
- Review evidence becomes more auditable: reviewers can no longer rely on a bare "tests passed" clean result for workflow-managed automated handoff.
- The orchestrator must validate process shape without owning the verdict, and the reviewer must record verdicts without optimizing for continuation.
- Existing implementation autoprogression correction loops remain compatible: authorized `changes-requested` results may still route to `review-resolution` when profile gates pass, but `blocked` and `inconclusive` never auto-route.
- Final holistic code review becomes mandatory before `explain-change` and `verify` in the implementation profile.
- Calibration evidence and second-review sampling become part of rollout and steady-state confidence, with standard-risk sampling adjusted from measured material-disagreement data and elevated-risk clean reviews second-reviewed.
- Profile-off behavior and direct isolated review invocations remain compatible with existing formal review recording rules, but workflow-managed automated handoff cannot use missing independence evidence as a clean result.

## Follow-up

- Architecture-review this ADR and the canonical architecture package update.
- Author the matching test specification for review-independence requirements, examples, acceptance criteria, and RAI check IDs.
- Plan implementation of manifest creation, initial-packet hashing, phase receipts, risk-tier classification, normalized `review_gate_outcome`, review artifact schema changes, validator coverage, skill guidance, calibration fixtures, and generated adapter updates.
- Keep review-family rollout phased: pilot the full protocol in `code-review`, collect manifest-only data for earlier review stages during the pilot, then expand after evidence supports it.
