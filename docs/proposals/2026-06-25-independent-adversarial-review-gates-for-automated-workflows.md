# Independent Adversarial Review Gates for Automated Workflows

## Status

accepted

## Relationship to prior work

This proposal builds on the accepted [Code Review Independence Under Autoprogression](2026-04-22-code-review-independence-under-autoprogression.md) proposal.

That earlier proposal kept hard fresh-session enforcement out of scope and focused on a narrower first-pass `code-review` contract. This proposal treats subsequent autoprogression work as new evidence that a stronger, workflow-level independence gate is worth considering.

For automated `code-review`, this proposal intentionally supersedes the April proposal's "hard fresh-session enforcement is out of scope" boundary once Phase 1 lands. The April proposal's evidence-backed clean-review and first-pass review-record expectations remain in force unless a follow-on spec explicitly replaces them.

For review skills not yet covered by this proposal's rollout, the April proposal and existing review-family contracts remain in force. A reader should not infer that every review-family skill has adopted this stronger contract until the relevant follow-on spec or implementation slice says so.

## Problem

After enabling workflow autoprogression, review stages increasingly return clean outcomes with no material findings.

A clean review is not inherently suspicious. Narrow changes, strong upstream contracts, and effective validators can legitimately eliminate many mechanical defects before review. A prior clean-workflow retrospective reached that conclusion and correctly avoided turning a single no-finding cycle into durable guidance.

However, automation creates a real independence risk:

```text
one context authors the artifact;
the same context knows the intended solution;
the same context runs validation;
the same context invokes review;
the workflow prefers a clean result so it can continue.
```

Under that pattern, a nominally separate review stage can become a continuation of authoring rather than an adversarial evaluation.

The current review skills already contain the right intent:

- `code-review` prefers a fresh session, separate reviewer, or separate agent and says the reviewer should inspect the actual diff and governing artifacts rather than review from memory.
- Automated proposal review resets context to tracked artifacts and must not rely on hidden authoring reasoning.
- Implementation-autoprogression guidance warns that later rounds can degrade into "did you make the requested edit?" checks and recommends a fresh full review before closeout.

The gap is structural enforcement.

These principles currently depend too heavily on the orchestrator or reviewer remembering to behave independently. In an automated flow, the authoring context, desired continuation outcome, validation summaries, prior review findings, and auto-fix policy can all anchor the reviewer before it has independently formed a judgment.

The resulting failure mode is not merely "too few findings." It is:

```text
the review process has low sensitivity to defects that share the author's
assumptions.
```

Review quality should therefore be measured through defect-detection sensitivity, downstream escape rate, independent-review disagreement, and evidence quality, not by requiring a minimum number of findings.

## Goals

- Make automated review stages structurally independent from their authoring stages.
- Require a fresh review context for workflow-managed automated reviews.
- Prevent author hidden reasoning and self-assessment from entering the reviewer's initial evidence set.
- Require every review to begin from the tracked artifact, actual diff when applicable, governing contracts, and formal review criteria.
- Separate independent defect discovery from prior-finding reconciliation.
- Require reviewers to challenge assumptions, boundary behavior, negative cases, evidence quality, and scope rather than merely check formatting or passing tests.
- Preserve the reviewer's freedom to discover new findings in any review round.
- Prevent autoprogression incentives from biasing the review verdict.
- Define a risk-based review-depth policy.
- Require a structured independence and criticality receipt for clean automated reviews.
- Make incomplete evidence produce `inconclusive`, not a convenient clean result.
- Require a final holistic review before `explain-change` and `verify`.
- Add calibration through second-review sampling, defect-seeded fixtures, and downstream escape analysis.
- Keep clean reviews valid when the independent evidence genuinely supports them.
- Preserve formal review recording, finding structure, and workflow-stage ownership.

## Non-goals

- Do not require every review to produce a finding.
- Do not treat a high clean-review rate alone as proof of poor quality.
- Do not reward reviewers based on finding count.
- Do not manufacture low-value findings to demonstrate criticality.
- Do not make different model vendors mandatory for every review.
- Do not expose private chain-of-thought or hidden model reasoning.
- Do not let the reviewer edit the artifact under review.
- Do not let validation results substitute for independent review.
- Do not let previous findings narrow a rereview to only confirming fixes.
- Do not suppress new findings because they would pause an automated loop.
- Do not weaken bounded evidence reading or require broad repository reads without risk justification.
- Do not automatically continue when the independence receipt is missing or invalid.
- Do not automatically resolve findings through this proposal.
- Do not change proposal, spec, plan, implementation, verification, or PR ownership.
- Do not introduce a hosted review service or persistent external control plane.
- Do not hand-edit generated skill or adapter output.

## Vision fit

fits the current vision

RigorLoop's value depends on AI-assisted work being genuinely reviewable by humans and agents, not merely passed through artifacts named "review."

This proposal strengthens human-understandable AI work, independent criticism, trustworthy automation, reviewable evidence, and safe autoprogression.

It is falsified if automated reviewers inherit the author's hidden reasoning, reviewers are pressured to approve, validation success is treated as proof that tests or requirements are adequate, rereviews inspect only prior findings, reviewers suppress new findings to preserve autoprogression, clean reviews lack evidence of what was challenged, high-risk changes receive the same shallow review as low-risk changes, known seeded defects routinely pass review, or downstream stages repeatedly find defects after automated clean reviews.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Restore review quality after automation | in scope | Goals, Recommended direction |
| Make review more independent | in scope | Review-context firewall |
| Make review more critical | in scope | Blind-first review protocol |
| Preserve automated workflow | in scope | Autoprogression binding |
| Avoid meaningless clean reviews | in scope | Clean-review sufficiency contract |
| Require findings in every review | rejected option | Non-goals, Options considered |
| Use separate reviewers where possible | in scope | Review-context firewall |
| Measure whether quality improves | in scope | Review calibration, Quality metrics |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Common review-independence contract | core to this proposal | All automated review gates need the same minimum separation. |
| Review invocation manifest | core to this proposal | Independence should be inspectable rather than asserted. |
| Blind-first review protocol | core to this proposal | Prevents author and prior-review anchoring. |
| Clean-review sufficiency receipt | core to this proposal | Clean results need affirmative evidence. |
| Risk-tiered review depth | core to this proposal | Review cost should match potential harm. |
| Final holistic review | core to this proposal | Milestone-local reviews can miss cross-milestone defects. |
| `code-review` pilot | first-slice candidate | It has the clearest implementation-risk surface. |
| Minimal `spec-review` and `plan-review` manifest collection | same-slice dependency | Captures independence data during the code-review pilot so earlier-stage degradation is visible. |
| Full `spec-review` and `plan-review` adoption | separate implementation slice | Apply after the code-review pilot proves the full contract. |
| `architecture-review` adoption | separate implementation slice | Architecture review needs specialized risk hypotheses. |
| `proposal-review` changes | deferable follow-up | Proposal remains the primary human checkpoint in the current automation model. |
| Heterogeneous model requirement | deferable follow-up | Useful for high risk but not required for normal changes. |
| Human review of all automated clean outcomes | out of scope | Removes most automation benefit. |
| Automated semantic scoring of review quality | separate proposal | Requires an independently validated evaluation model. |

## Context

Current review guidance already says to prefer a fresh session, separate reviewer, or separate agent; inspect the actual artifact or diff; read governing artifacts and validation evidence; avoid reviewing from memory; and avoid editing the reviewed artifact during review.

Those are good rules, but automation can still satisfy them superficially while leaking author context or optimizing toward continuation.

The implementation-autoprogression design also creates an incentive conflict:

```text
a clean review allows the workflow to continue;
a finding pauses or lengthens the workflow.
```

The reviewer should be insulated from that incentive. Review status is evidence for the orchestrator; it should not be treated as an objective the reviewer optimizes.

The reviewer should also be free to discover new findings during rereview. A "no new findings" rule may be valid as an orchestrator stop condition, but it should never become a reviewer constraint. If a new defect is found, the reviewer records it and the orchestrator pauses.

## Options considered

### Option 1: Require at least one finding per review

Pros:

- Immediately reduces zero-finding reviews.
- Easy to measure.

Cons:

- Incentivizes fabricated or low-value findings.
- Punishes genuinely clean work.
- Converts review quality into finding volume.
- Creates noise and reviewer distrust.

Rejected.

### Option 2: Strengthen review prompts only

Add instructions such as:

```text
be critical
look harder
do not rubber-stamp
```

Pros:

- Small change.
- No orchestration work.

Cons:

- Still depends on discipline.
- Does not prevent author-context leakage.
- Does not prove the reviewer ran independently.
- Likely degrades again under automated pressure.

Rejected as insufficient.

### Option 3: Always use a different model or vendor

Pros:

- Adds cognitive diversity.
- Reduces some correlated assumptions.

Cons:

- Model identity alone does not guarantee independence.
- A second model can receive the same biased evidence packet.
- Adds cost and platform coupling.
- Not always available.

Useful for high-risk tiers, but insufficient as the core contract.

### Option 4: Fresh-context, blind-first, risk-tiered adversarial review

Use:

```text
context firewall
-> independent risk formulation
-> full review
-> evidence challenge
-> prior-finding reconciliation
-> recorded verdict
```

Add second-review sampling and calibrated defect fixtures.

Pros:

- Addresses the structural cause.
- Preserves clean outcomes when justified.
- Works with the same or different model.
- Produces auditable independence evidence.
- Supports bounded autoprogression.

Cons:

- Increases review cost.
- Requires orchestration and review-record changes.
- Needs careful calibration to avoid boilerplate.

Recommended.

### Option 5: Require human review for every automated stage

Pros:

- Strongest independence.
- Simple authority boundary.

Cons:

- Removes most value of automation.
- Humans can also anchor on author explanations and passing tests.
- Does not improve the review skill itself.

Rejected as the default; retained for critical-risk escalation.

## Recommended direction

Adopt an Independent Adversarial Review Gate for automated workflows.

The gate has six required mechanisms:

```text
1. review-context firewall
2. blind-first evidence sequence
3. risk-based adversarial review plan
4. independent full-review pass
5. clean-review sufficiency receipt
6. calibration and escalation
```

A clean result may advance the automated workflow only when all six contracts are satisfied.

## Review-context firewall

An automated review should execute in one of these modes:

```text
separate-agent
fresh-session
fresh-context-same-model
human-review
```

Closed independence levels:

| Level | Mode | Use |
| --- | --- | --- |
| `L1` | Fresh context using the same model | Minimum for ordinary automated review |
| `L2` | Separate agent or independently created session | Required for elevated-risk review |
| `L3` | Heterogeneous reviewer or human reviewer | Required for critical-risk review |

The authoring session continuing directly into review without context reset is `L0`, which is not valid for an automated lifecycle review.

For this proposal, "fresh context" means a review invocation whose initial evidence packet is constructed from tracked artifacts and neutral routing metadata, with no inherited author chat, hidden reasoning, recent-work memory, implementation narrative, desired outcome, or auto-fix budget. The manifest should record a `reviewer_context_id` that is verifiably different from the author or implementation context identifier, plus the mechanism used to establish separation, such as separate agent, newly created session, or clean same-model invocation with isolated memory.

If a platform cannot expose enough identity or provenance data to distinguish the reviewer context from the authoring context, the review should be treated as `L0` for automated handoff purposes.

If the platform cannot establish the required independence level, the review status should be `inconclusive` with stop condition `independent review context unavailable`.

Before forming initial review hypotheses, the reviewer should not receive author hidden reasoning, author chain-of-thought, author self-assessment, claims that the change is correct, desired review outcome, autoprogression round budget, messages that approval is needed to continue, auto-fix eligibility, implementation-stage safety narrative, prior reviewer conclusion, validation result summaries, or the validation-evidence type menu.

The reviewer may receive objective routing data, review target identity, actual tracked artifact or diff, base and head revision when applicable, approved proposal, approved spec, test spec, architecture and ADRs when applicable, current plan milestone, formal review criteria, and repository governance needed for the decision.

Validation evidence should be staged later, after the reviewer has formed initial risks. The evidence-type menu should also be withheld until after initial risk recording, then disclosed as a closed menu the reviewer can request from.

## Review invocation manifest

Every automated review should record a manifest:

```yaml
review_id: code-review-m2-r1
review_stage: code-review
review_target: <artifact, diff, or commit>
independence_level: L2
reviewer_context_id: <opaque session or invocation ID>
author_context_id: <opaque session or invocation ID>
context_separation_mechanism: <separate-agent | fresh-session | fresh-context-same-model | human-review>
author_context_excluded: true
base_revision: <revision>
head_revision: <revision>
governing_artifacts:
  - <path>
formal_criteria:
  - <criterion ID or review dimension>
risk_tier: <standard | elevated | critical>
risk_tier_classifier: orchestrator-deterministic-surface-check
validation_evidence_deferred_until_phase: evidence-challenge
prior_findings_deferred_until_phase: reconciliation
```

The manifest records process facts only. It should not contain private reasoning.

A review without a valid manifest cannot automatically advance the workflow.

Manifest free-form fields should be short and schema-bounded. Where possible, use closed vocabulary fields, stable identifiers, file paths, check IDs, and recorded evidence references instead of open-ended rationale prose. Calibration should audit sampled records for private-reasoning leakage, excessive narrative, and evidence-free assertions.

## Blind-first review protocol

### Phase 1: Independent orientation

The reviewer reads the actual target, governing contracts, and formal review rubric. It records an independent risk map before reading author summaries or prior review conclusions.

Required risk-map fields:

```text
affected behavior
highest-impact failure modes
changed boundaries
evidence expected
areas requiring direct inspection
areas intentionally out of scope
```

### Phase 2: Adversarial hypothesis formation

For each applicable risk class, the reviewer formulates at least one falsifiable review question.

Candidate risk classes:

```text
contract mismatch
missing negative or boundary behavior
scope expansion
compatibility or migration regression
security or privacy boundary
data loss or state corruption
error handling and partial failure
test inadequacy or false-positive test
generated or derived artifact drift
workflow-state inconsistency
performance or resource regression
observability and operability gap
```

Not every class applies to every review. The reviewer records applicable and not-applicable classes with a brief reason.

### Phase 3: Direct inspection

The reviewer inspects the artifact or diff independently.

For code review, this includes the actual diff, affected code paths, tests, negative and boundary cases, and selected generated outputs.

For spec or plan review, this includes applicable requirements, edge cases, compatibility, sequencing, rollback, and validation boundaries.

### Phase 4: Evidence challenge

Only after the independent risk map exists, the orchestrator discloses the validation-evidence type menu. The reviewer then requests relevant evidence and inspects validation output, test results, implementation notes, selector output, and generated evidence.

Passing validation proves that selected checks passed. It does not prove the right checks were selected, tests exercise the intended behavior, negative cases are sufficient, the spec is complete, or scope did not drift.

The reviewer challenges evidence adequacy separately from evidence result.

### Phase 5: Prior-finding reconciliation

For rereviews, prior findings are read only after the new full pass. The reviewer then determines whether each item is resolved, still present, failed-remediation, reopened, superseded, or a new finding.

`failed-remediation` means a previously reported defect was claimed or expected to be fixed, but the blind-first pass independently rediscovered it. This is a stronger signal than ordinary `still present` because it indicates the correction attempt did not address the defect or the author misunderstood the finding. Failed remediation should surface in the audit trail and calibration metrics.

A rereview should not degrade into a fix-confirmation-only pass.

### Phase 6: Verdict and handoff

The reviewer determines status from the independent review:

```text
approved / clean-with-notes
changes-requested
blocked
inconclusive
```

Only after the verdict is recorded may the orchestrator inspect it and decide whether autoprogression continues.

## Reviewer-orchestrator separation

The reviewer owns finding discovery, severity, evidence, required outcome, review verdict, and confidence.

The orchestrator owns whether the workflow may continue, whether a new finding pauses an auto-fix loop, round-limit enforcement, profile state, and next-stage invocation.

The reviewer should not suppress a finding because it is a later review round, the workflow has already used its correction budget, a new finding will pause automation, the change is close to verify, or the user wants the workflow to finish.

Auto-fix classification, when required, should occur after the finding and verdict are recorded so fixability does not bias discovery. Prefer a separate classifier invocation from the reviewer when the workflow uses auto-fix routing, so the context that discovered the defect does not also decide how cheap it is to fix.

## Risk-tiered review depth

Risk tier should be determined by an orchestrator-owned deterministic check against affected paths, changed surfaces, metadata, and declared workflow actions, not by the authoring context's self-assessment. The resulting tier and trigger evidence should be recorded in the review manifest.

Classification fails closed. If a trigger ambiguously matches or the classifier cannot inspect enough evidence, the review uses the higher plausible tier or becomes `inconclusive` when the required tier cannot be satisfied.

### Standard risk

Examples:

```text
bounded documentation changes
small internal refactor with complete tests
localized non-security behavior
```

Expected coverage:

```text
L1 independence
one full blind-first review
clean-review sufficiency receipt
```

### Elevated risk

Triggers include:

```text
public API behavior
workflow or validator behavior
generated-output machinery
compatibility or migration logic
concurrency
persistent state
release packaging
authentication or authorization
security-relevant configuration
multi-component changes
```

Expected coverage:

```text
L2 independence
full review
at least one independent direct proof or reproduction
random or mandatory second-review policy as configured
```

### Critical risk

Triggers include:

```text
destructive migration
credential or secret handling
privilege boundary
deployment or publication
irreversible external action
high-impact security change
```

Expected coverage:

```text
L3 independence
human authorization for irreversible external actions such as deploy, publish, secret handling, destructive migration, or privileged remote mutation
independent heterogeneous reviewer acceptable only for high-impact internal codebase changes where no irreversible external action is authorized
no fully automated clean-review handoff
```

The downstream spec should close the precise trigger vocabulary.

## Clean-review sufficiency contract

No material findings is a valid outcome.

It requires a clean-review sufficiency receipt containing:

```text
review target identity
independence level
governing artifacts inspected
risk classes considered
adversarial hypotheses tested
direct proofs or reproductions performed
test and validation evidence challenged
unreviewed or uncertain surfaces
confidence
no-finding rationale
```

A no-finding rationale such as "Tests passed and the change looks correct" is insufficient.

If material risk remains unreviewed, the review status should be `inconclusive`, not clean.

## No finding quota

Do not establish:

```text
minimum one finding
average findings per review
finding count target
```

These incentives produce noise and hide genuine clean outcomes.

Use finding count only as a diagnostic signal. A sudden drop in findings should trigger calibration, but not automatic rejection.

## Final holistic review

Before an automated implementation workflow transitions into:

```text
explain-change
-> verify
```

require a fresh holistic code review.

It should evaluate:

```text
complete final diff
interaction across all milestones
governing proposal/spec/test-spec/architecture/plan
all review resolutions
final validation selection
generated and derived artifacts
cross-milestone scope
```

It should not be only the last milestone's local review.

This implements the existing guidance that automated rereviews should periodically return to the original contract rather than converge on a locally passing but globally wrong result.

## Review calibration

### Seeded-defect corpus

Maintain review fixtures containing known defects representative of each review family.

Examples:

| Review skill | Seeded defect |
| --- | --- |
| `spec-review` | Contradictory requirements or missing boundary behavior |
| `architecture-review` | Prose/C4 container mismatch |
| `plan-review` | Milestone that cannot close independently |
| `code-review` | Test passes for the wrong reason or missing failure-path coverage |

The evaluator should not require exact wording. It should assess whether the review identifies the intended defect class and required outcome.

Actual calibration should avoid overfitting to a fixed public fixture set. Public repository fixtures can document defect classes and examples, but measured calibration should use a private or access-controlled rotating instance set when practical.

Calibration records should distinguish recurrence-detection from novel-defect detection. A reviewer repeatedly catching a known fixture by recognition is useful as a regression check, but it is not the same evidence as detecting a new instance of the same defect class.

Run calibration when a review skill or prompt changes, when an autoprogression profile changes, on a periodic scheduled basis, and after a downstream escaped defect.

### Independent clean-review sampling

During initial rollout:

```text
sample 20% of automated standard-risk clean reviews
review all elevated-risk clean reviews
```

Send sampled reviews to a second independent reviewer or human audit.

Acceptable second-reviewer types should be explicit:

| Risk tier | Acceptable second reviewer during rollout |
| --- | --- |
| Standard | Same review skill in a fresh L1+ context, separate agent, heterogeneous reviewer, or human auditor |
| Elevated | Separate agent, independently created session, heterogeneous reviewer, or human auditor |
| Critical | Human auditor for irreversible external actions; heterogeneous reviewer only for high-impact internal changes where the critical-risk authority allows it |

Record the selected second-reviewer type, independence level, agreement, additional material findings, severity disagreement, and evidence gaps in the calibration record.

After rollout, the standard-risk sample rate should be measurement-driven rather than fixed. Set it high enough to bound the observed material-disagreement rate with a useful confidence interval. The rate may decrease as disagreement converges to a stable measured rate, and it should increase after workflow changes, model changes, prompt changes, calibration misses, or downstream escape findings.

Elevated-risk clean reviews remain sampled at 100% in steady state. Critical-risk reviews retain their configured authority gate rather than becoming ordinary sampled approvals.

### Downstream escape analysis

A review escape occurs when a material defect is first identified after a clean review in later code review, verify, hosted CI, PR review, release validation, or production incident.

Every escape should route to a review-calibration record.

## Quality metrics

Use:

```text
seeded-defect recall
second-review material-disagreement rate
downstream material-defect escape rate
clean-review sufficiency-receipt completion
inconclusive rate caused by missing evidence
false-positive finding rate
review duration by risk tier
```

Track metrics by risk tier and by review skill. Aggregated metrics may hide the exact stage or tier where review sensitivity is failing.

Do not optimize for number of findings, percentage of reviews that fail, or percentage of reviews that approve.

Initial rollout targets over the first 20 eligible automated reviews or 30 calendar days:

```text
100% valid independence manifests
100% clean reviews contain sufficiency receipts
100% elevated-risk clean reviews receive second review
zero critical-risk fully automated approvals
zero documented cases of finding suppression due to autoprogression
zero downstream material escapes attributable to an omitted mandated review surface
```

Seeded-defect recall targets should be established after the baseline corpus is measured rather than invented before evidence exists.

## Autoprogression binding

A review result may advance an automated profile only when the review invocation manifest is valid, the required independence level is satisfied, blind-first phases are complete, the review record is recorded, a clean-review receipt exists when no finding is reported, risk-tier escalation requirements are satisfied, no unresolved findings remain, and workflow-state synchronization passes.

Otherwise:

```text
profile state: paused
stop reason: review independence or sufficiency gate failed
```

Review automation does not bypass review recording.

## Expected behavior changes

Before:

```text
authoring context
-> review prompt in same workflow context
-> tests passed
-> no findings
-> continue
```

After:

```text
authoring context closes
-> orchestrator creates neutral review manifest
-> fresh reviewer forms independent risks
-> reviewer inspects target
-> reviewer challenges validation
-> reviewer records findings or clean sufficiency receipt
-> orchestrator evaluates handoff eligibility
```

Rereview before:

```text
read previous finding
-> check requested edit
-> approve
```

Rereview after:

```text
fresh full review
-> record any new or existing findings
-> reconcile previous findings
-> verdict
```

High-risk change:

```text
single automated clean review
-> second independent review or human gate
-> only then continue
```

## Architecture impact

| Surface | Impact |
| --- | --- |
| Autoprogression contracts | Add mandatory independent-review gate. |
| Workflow orchestrator | Create neutral review manifests and fresh invocations. |
| Review-family skills | Add blind-first protocol and criticality receipt. |
| Review result assets | Add independence, risk-map, confidence, and no-finding fields. |
| `code-review` | Pilot full independent adversarial review. |
| Review recording | Record process evidence without private reasoning. |
| Change metadata | Store review-manifest and calibration pointers, not review judgment. |
| Test fixtures | Add seeded-defect and clean-review calibration corpus. |
| Verify | Require final holistic review evidence before automatic verify. |
| Generated skills/adapters | Rebuild affected public review skills. |
| Runtime services | No new service, storage engine, or network dependency. |

Architecture assessment is recommended because this changes orchestration context boundaries and review evidence across automated profiles.

## Testing and verification strategy

Likely checks:

| Check ID | What is verified |
| --- | --- |
| `RAI-001` | Automated review cannot use `L0` author-continuation mode. |
| `RAI-002` | Fresh-context identity is recorded. |
| `RAI-003` | Author hidden reasoning is absent from the initial review packet. |
| `RAI-004` | Desired review outcome is not included in the review packet. |
| `RAI-005` | Reviewer creates a risk map before reading validation summaries. |
| `RAI-006` | Validation success is challenged for adequacy, not merely accepted. |
| `RAI-007` | Prior findings are deferred until after the fresh pass. |
| `RAI-008` | Rereview may report a new finding. |
| `RAI-009` | A new finding pauses the orchestrator without being suppressed. |
| `RAI-010` | Reviewer does not edit the target artifact. |
| `RAI-011` | Clean review requires a complete sufficiency receipt. |
| `RAI-012` | Missing review evidence produces `inconclusive`. |
| `RAI-013` | Elevated-risk clean review requires independent second review. |
| `RAI-014` | Critical-risk review cannot auto-approve without the required authority. |
| `RAI-015` | Final holistic review covers the complete cross-milestone diff. |
| `RAI-016` | No minimum-finding quota exists. |
| `RAI-017` | Seeded material defects are detected at the intended review stage. |
| `RAI-018` | Historical findings do not improperly anchor blind-first review. |
| `RAI-019` | Independence evidence schema uses closed-vocabulary or bounded fields and rejects private-reasoning fields. |
| `RAI-020` | Profile behavior remains unchanged when review automation is off. |

The first implementation slice should also create:

```text
docs/changes/<change-id>/behavior-preservation.md
```

Required matrix:

| Surface | Baseline | Revised proof | Result |
| --- | --- | --- | --- |
| Review ownership | Review skill owns verdict | unchanged | preserved |
| Review recording | Formal review result required | unchanged | preserved |
| Material findings | Existing finding structure | unchanged plus independence metadata | preserved |
| Clean reviews | Lightweight receipt | expanded sufficiency receipt in auto mode | strengthened |
| Direct review invocation | Isolated by default | unchanged | preserved |
| Manual workflow | Existing behavior | unchanged | preserved |
| Automated handoff | Clean recorded result | clean result plus independence gate | strengthened |
| Verify ownership | Verify owns branch readiness | unchanged | preserved |
| PR ownership | PR owns external handoff | unchanged | preserved |

## Rollout and rollback

### Phase 0: Baseline

Measure current clean-review rate, downstream finding escapes, review disagreement, and review duration.

Pair clean-review rate with baseline second-review disagreement rate. Clean-review rate is the surface symptom; disagreement rate is the stronger quality signal.

Review a recent sample manually to determine whether no-finding outcomes were genuinely clean or shallow.

### Phase 1: Code-review pilot

Apply the contract to automated `code-review`.

Enable fresh context, blind-first protocol, clean-review sufficiency receipt, final holistic review, and mandatory second review for elevated risk.

### Phase 2: Authoring review gates

Extend the common contract to:

```text
spec-review
architecture-review
plan-review
```

Use stage-specific risk classes and seeded fixtures.

### Phase 3: Calibrated autoprogression

Allow clean review results to advance automatically only after independence manifest validation, sufficiency receipt validation, risk escalation satisfaction, and acceptable calibration escape rate.

### Rollback

- Disable automated review handoff.
- Restore manual stage triggering.
- Preserve review records and calibration evidence.
- Do not delete valid findings or clean-review receipts.
- Keep the context-firewall contract available for manual reviews.
- Rebuild generated skills if canonical guidance is reverted.
- Do not restore same-context automated self-review as an accepted gate.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Review becomes expensive | Risk tiers and bounded evidence sets. |
| Standard-risk review cost rises 2-3x during rollout | State the expected multiplier, use sampling only where it gives calibration value, and tune steady-state sampling from measured disagreement. |
| Reviewer produces ritual hypotheses | Seeded calibration and evidence-based quality review. |
| Clean receipts become boilerplate | Require direct proof and audit sampled receipts. |
| Different model still shares assumptions | Context firewall and blind-first evidence sequence. |
| Reviewer misses author intent needed to assess correctness | Governing artifacts remain available; author narrative enters only after independent pass. |
| Rereview repeatedly rediscovers old issues | Reconciliation phase follows the independent pass. |
| High-risk work stalls | Explicit human or heterogeneous-review escalation. |
| Calibration fixtures overfit prompts | Use a rotating private calibration set where practical, keep public fixtures focused on defect classes, and evaluate defect classes rather than exact wording. |
| Reviewers over-report to appear critical | No finding quota; false-positive rate monitored. |
| Automation hides new findings | Reviewer may always report them; only orchestrator pauses. |
| Private reasoning leaks into records | Record inputs, checks, and outcomes in schema-bounded fields, audit sampled records, and avoid open-ended reasoning fields. |

## First-slice boundary

First implementation slice:

```text
common review-independence terminology
neutral review invocation manifest
fresh-context enforcement
risk-tier classifier and fail-closed tier handling
blind-first protocol
risk map
validation-evidence challenge phase
clean-review sufficiency receipt
no-finding rationale contract
code-review pilot
final holistic code review
seeded code-review calibration fixtures
elevated-risk second-review gate
minimal manifest collection for automated spec-review and plan-review
behavior-preservation evidence
```

Out of scope for the first slice:

```text
all review-family migration
mandatory heterogeneous models for ordinary work
automatic semantic scoring
human review of every clean result
proposal-review changes
hosted review service
```

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-RAI-001` | Automated reviews cannot run as an uninterrupted continuation of authoring context. |
| `AC-RAI-002` | Every automated review records an independence manifest. |
| `AC-RAI-003` | The initial review packet excludes author hidden reasoning and desired outcome. |
| `AC-RAI-004` | The reviewer performs an independent pass before reading prior findings. |
| `AC-RAI-005` | Reviewers may report new findings during any review round. |
| `AC-RAI-006` | Autoprogression incentives do not alter the review verdict contract. |
| `AC-RAI-007` | No material-finding quota is introduced. |
| `AC-RAI-008` | A clean automated review includes a complete sufficiency receipt. |
| `AC-RAI-009` | Missing or insufficient evidence produces `inconclusive`. |
| `AC-RAI-010` | Risk tier determines required independence and escalation. |
| `AC-RAI-011` | Elevated-risk clean reviews receive a second independent review during rollout and steady state unless a later accepted proposal revises the sampling policy. |
| `AC-RAI-012` | Critical-risk changes retain a human or equivalent authority gate. |
| `AC-RAI-013` | A final holistic code review occurs before explain-change and verify. |
| `AC-RAI-014` | Seeded-defect fixtures provide measurable review calibration. |
| `AC-RAI-015` | Downstream material-defect escapes are recorded and analyzed. |
| `AC-RAI-016` | Review records contain process evidence but no private chain-of-thought. |
| `AC-RAI-017` | Manual and profile-off review behavior remains compatible. |

## Open questions

### 1. Must ordinary automated reviews use a different model?

Candidate answer:

```text
No.

A fresh isolated context and clean evidence packet are mandatory. Model identity
is a risk-tier control, not the core independence control.

A different model fed the same biased evidence is still anchored. The same model
fed a clean evidence packet in a verifiably fresh context satisfies L1.

A different model or human reviewer is required only by the elevated or critical
risk tier.
```

### 2. Should validation evidence be withheld completely during the blind pass?

Candidate answer:

```text
Withhold result summaries and the evidence-type enumeration until the reviewer
records initial risks.

After initial risks are recorded, disclose the enumeration as a closed menu the
reviewer can request from. Result content remains staged until Phase 4.
```

### 3. Should prior findings be hidden during rereview?

Candidate answer:

```text
Yes during the initial independent pass.

Hide the actual finding list during the initial pass, but allow the reviewer to
know that prior rounds occurred and that resolution records exist.

Reveal the actual finding list during reconciliation so the reviewer can verify
resolution without reducing the rereview to the previous finding list.
```

### 4. What percentage of clean reviews should receive a second review?

Candidate answer:

```text
20% of standard-risk automated clean reviews during rollout.

After rollout, set the standard-risk sample rate from the observed
material-disagreement rate and the confidence interval the project wants.
Sampling can decrease as disagreement converges and should rise after workflow,
model, prompt, calibration, or downstream-escape events.

100% of elevated-risk clean reviews remain second-reviewed.
100% of critical-risk reviews require the configured authority gate.
```

### 5. Should auto-fix classification be visible during review discovery?

Candidate answer:

```text
No.

Record the finding and verdict first. Classify fixability afterward so ease of
automation cannot bias whether a defect is reported.

Prefer a separate classifier invocation from the reviewer for auto-fix
classification.
```

### 6. Should review quality be judged by number of findings?

Candidate answer:

```text
No.

Use seeded-defect recall, downstream escape rate, second-review disagreement,
false-positive rate, and receipt quality.

Track these metrics by risk tier and by review skill rather than only in
aggregate.
```

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-24 | Treat the no-finding pattern as a calibration signal, not proof by itself. | Clean work can legitimately produce clean reviews. | Require a finding in every review. |
| 2026-06-24 | Enforce fresh review context structurally. | Prompt-only independence is insufficient in automation. | Add only "be critical" wording. |
| 2026-06-24 | Use blind-first review before prior-finding reconciliation. | Prior findings anchor rereviews toward local confirmation. | Start rereview from the old finding list. |
| 2026-06-24 | Separate reviewer judgment from orchestrator continuation. | The reviewer should not optimize for autoprogression. | Tell reviewer to approve when safe to continue. |
| 2026-06-24 | Permit new findings in every round. | Suppressing discoveries reduces quality. | Apply no-new-finding as a reviewer constraint. |
| 2026-06-24 | Require clean-review sufficiency evidence. | Absence of findings needs affirmative review proof. | Treat no findings as self-explanatory. |
| 2026-06-24 | Pilot in code-review before expanding to the review family. | Code review has the clearest defect and calibration surface. | Modify every review skill at once. |
| 2026-06-24 | Measure recall and escapes, not finding volume. | Finding quotas create noise and false incentives. | Use clean-review percentage as quality target. |

## Next artifacts

```text
proposal-review
review-independence and criticality spec
workflow-stage-autoprogression spec amendment
formal review recording amendment
spec-review
architecture assessment
architecture-review when required
test-spec
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- [Review Independence and Criticality](../../specs/review-independence-and-criticality.md)

Planned follow-on directions include:

- Proposal for review-family rollout after the code-review pilot.
- Proposal for heterogeneous reviewer selection at elevated risk.
- Proposal for periodic human audit of automated clean reviews.
- Proposal for rotating review-calibration corpora.
- Proposal for review-quality dashboards only after the measurement contract is stable.

## Readiness

Ready for specification.

Proposal review approved this direction with no material findings. The downstream spec should define the normalized orchestration gate outcome, immutable initial-packet and phase-receipt evidence, exact L1/L2/L3 requirements, second-review disagreement behavior, rollout sampling floors, and adjustment rules.

No implementation or autoprogression behavior should change until those contracts and matching test specifications are approved.

## Core invariant

```text
Automation may invoke a review, but it must not author the reviewer's judgment.

The reviewer begins from a fresh context, forms independent risks before seeing
author conclusions or prior findings, challenges evidence rather than trusting
pass results, and remains free to report new findings in every round.

A clean review is acceptable only when the independent review process can show
what it tried to falsify and why no material defect was found.
```
