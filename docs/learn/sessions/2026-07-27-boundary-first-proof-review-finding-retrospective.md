# Learn Session: Boundary-First Proof Review-Finding Retrospective

## Status

- captured
- candidate classifications awaiting contributor confirmation
- no derivative routing performed

## Frame

- Trigger: explicit maintainer questions asking why the boundary-first proof modeling initiative accumulated 185 material findings, whether weak proposal, specification, or planning caused the volume, and why a repository-only Codex runtime-certification mechanism entered a proposal intended to improve portable published-skill behavior.
- Trigger type: explicit maintainer request / repeated review findings / workflow-process retrospective.
- Date: 2026-07-27
- Scope:
  - change `2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills`;
  - review activity from proposal review through final holistic code review;
  - upstream artifact quality, runtime feasibility, scope growth, implementation proof, and finding-accounting behavior.
- Evidence in scope:
  - the accepted proposal, approved specifications, accepted architecture and ADRs, approved plan, and approved test specification;
  - the change-local review log, review resolution, validation records, and verify report;
  - M1 code-review R1 and spec-review R9 through R13, where executable evidence became a standalone Codex behavior harness;
  - branch commit history and current diff statistics;
  - the prior single bounded review-fix finding-volume retrospective.
- Explicit exclusions:
  - no reopening of resolved findings;
  - no claim that raw finding count is a direct quality score;
  - no attribution to an individual reviewer, contributor, or model;
  - no workflow, skill, proposal, specification, architecture, plan, or topic update without contributor confirmation.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-07-25-single-bounded-review-fix-finding-volume.md`
- Session record path: `docs/learn/sessions/2026-07-27-boundary-first-proof-review-finding-retrospective.md`

## Observe

### O1 - The direction was sound, but the first-release solution was not bounded tightly enough

The accepted proposal correctly identified example-first implementation as the problem and explicitly rejected raw finding count as a sole quality metric. It also selected an end-to-end first release spanning eight public skills, workflow and skill contracts, deterministic validation, and a retrospective automation corpus.

The resulting branch contains 699 changed files and about 95,638 added lines.
The largest implementation files are the behavior harness, its tests, the typed model, and its validator. The implementation therefore became a cross-cutting trusted execution and evidence system, not merely a small published-skill guidance correction.

The proposal was not strategically wrong. Its first-release surface combined too many independently risky concerns:

- boundary vocabulary and proof semantics;
- published-skill behavior;
- executable conformance validation;
- isolated stage execution;
- runtime capability detection;
- file-change control;
- evidence publication and recovery;
- adapter, selector, and release integration.

### O2 - The primary architectural assumption was disproved too late

The active plan records that live M2 generation proved the pinned app-server could return schema-constrained stage messages but did not expose the assumed stage-agent workspace-write surface or file-change operation.

That discovery happened after proposal, specification, architecture, plan, and test-spec approval and after M1 implementation. It forced a new design based on read-only children, parent-only materialization, an exact-runtime capability projection, a deny-only dispatcher, integrity observations, and additional ADRs.

This is the strongest causal signal in the record. The initiative committed to a runtime-dependent architecture before running a small executable feasibility probe against the pinned runtime.

### O3 - Upstream artifacts were repeatedly reopened because feasibility and contract were coupled

The change recorded:

| Review family | Review records |
| --- | ---: |
| Proposal review | 2 |
| Spec review | 58 |
| Architecture review | 30 |
| Plan review | 23 |
| Test-spec review | 27 |
| Code review, including preflight and final review | 27 |
| **Total** | **167** |

The verify report records 185 resolved material findings.

Only two proposal reviews were needed. Most churn occurred after the direction was accepted, while runtime transport, authority, evidence, recovery, and proof contracts were being discovered and projected across specifications, architecture, plans, tests, and implementation.

This does not mean the later artifacts were generally poor. It means their approval gates operated on assumptions that had not yet been empirically settled, so each runtime discovery invalidated several downstream projections.

### O4 - The initiative reproduced the pattern it was designed to prevent

The prior retrospective concluded that independent review had become the first exhaustive boundary audit and recommended complete boundary inventories before code-review handoff.

The new proposal adopted that lesson, but its own enforcement mechanism created new boundaries faster than the artifacts closed them:

- process isolation and credential exposure;
- app-server request and response schemas;
- capability and version projection;
- file-change policy and handler conformance;
- envelope transport and materialization;
- publication transactions and recovery;
- review correction authority;
- adapter and selector behavior.

Boundary-first modeling was applied inside each correction, but the system boundary kept expanding. Exhaustiveness cannot converge while the subject being modeled is still changing materially.

### O5 - Milestone and PR size amplified defect discovery and correction cost

The branch has 354 commits. M2 owns the hermetic harness, upstream skill behavior, runtime feasibility, transport, publication, correction behavior, and fresh evidence. Keeping those concerns inside one milestone made each review correction capable of changing the inputs of several other proofs.

The final diff is dominated by durable evidence and review records, which is appropriate for auditability but poor for human reviewability. Every new review round also created identities and lifecycle surfaces that later corrections had to keep synchronized.

### O6 - Stable finding identities amplify the count but are not the root cause

The repository preserves each material residual or sibling-boundary escape under a new stable finding ID. That is better audit evidence than rewriting one broad comment, but 185 findings are not 185 independent first-draft defects.

The count includes:

- first-pass design or implementation gaps;
- newly exposed sibling cases;
- incomplete remediation;
- stale cross-artifact projections;
- lifecycle and evidence-consistency findings;
- findings introduced by later architecture changes.

Raw count therefore measures both defect volume and review resolution granularity. It should be paired with root-cause clusters, failed-remediation rate, review rounds, and final holistic escapes.

### O7 - Review resolution crossed the accepted proposal boundary without reopening proposal choice

The accepted proposal selected boundary-first modeling embedded in existing lifecycle owners. It described deterministic validation of stable structure and closed vocabularies, while independent review retained semantic judgment.
It did not select live certification of one Codex runtime as the published capability.

M1 code-review R1 correctly found that executable seeded-omission and simple-change evidence lacked an owner. Findings `BFP-M1-CR6` and `BFP-M1-CR7` were marked as requiring owner decisions. The subsequent resolution treated them as contract-completeness gaps and routed through spec revision.

That route progressively changed the solution:

```text
deterministic fixture and trace evidence
-> one immutable nondeterministic behavior run
-> complete harness dependency identity
-> runtime/model/instruction/tool invocation profile
-> standalone hermetic harness
-> canonical `codex` runtime
```

The proposal remained accepted and unchanged while the mechanism changed materially. A new runtime, process-isolation boundary, transport protocol, publication transaction, and compatibility commitment are proposal-level solution choices, not merely missing fields in a specification.

The repository already instructed code review to stop when a finding requires a product, specification, architecture, ADR, or scope decision. The failure was therefore not absence of a general stop rule. It was failure to classify the proposed correction at the correct decision level.

### O8 - Portable user capability and maintainer-only certification were conflated

Published users receive skill instructions and the packaged boundary-proof reference. They do not receive or operate the repository's behavior harness, immutable evidence runs, capability registry, app-server probes, or recovery transaction.

The portable capability is:

```text
skill instructions
+ packaged boundary reference
+ artifact contract
+ proof and review handoffs
```

The Codex mechanism is:

```text
repository-maintainer evaluation
+ one exact runtime and model substrate
+ repository-local evidence publication
```

Maintainer evaluation may test a published capability, but it is not itself a capability available to published-skill users. Making the second mechanism a mandatory capability-baseline component caused the project to optimize and certify a repository-only implementation instead of the portable user contract.

## Root Cause

The immediate technical root cause was:

> A broad, runtime-dependent trust and proof mechanism entered the normal
> lifecycle before its minimum runtime capabilities and end-to-end enforcement
> boundary were proven by a small executable feasibility slice.

The deeper governance root cause was:

> A review finding about missing evidence was classified as a specification
> completeness problem even after its proposed resolution introduced a new
> mechanism, trust boundary, runtime dependency, and compatibility commitment.
> Because the correction was not classified as a proposal-level scope and
> solution decision, review-resolution authority expanded the initiative
> without a renewed comparison of alternatives.

The conceptual root cause was:

> Proof of a portable published-skill contract was conflated with live
> certification of one repository-controlled Codex runtime.

That produced the following causal chain:

```text
sound boundary-first direction
-> over-broad first-release enforcement scope
-> unproven runtime assumption
-> late live-runtime contradiction
-> repeated spec, architecture, plan, and test-spec redesign
-> expanding trust and recovery boundaries
-> large coupled implementation milestone
-> adversarial review becomes the integration boundary audit
-> many distinct findings and synchronization corrections
```

The proposal, specification, and plan each contributed differently:

| Artifact | Assessment | Contribution |
| --- | --- | --- |
| Proposal | good problem framing and direction; over-broad first release | Combined guidance, validation, runtime isolation, evidence, and rollout into one initiative. |
| Specification | increasingly rigorous; stabilized reactively | Closed many contracts only after implementation or runtime review exposed them. |
| Architecture | ultimately robust; initial feasibility assumption was wrong | Assumed a child write/file-change surface that the pinned runtime did not expose. |
| Plan | detailed and traceable; milestones remained too coupled | Allowed a very large M2 and did not put a mandatory runtime feasibility gate before architecture commitment. |
| Test spec | comprehensive at closeout; repeatedly reprojected | Followed the changing contract instead of preventing the initial capability assumption. |

The concise answer is therefore:

```text
not bad direction
+ insufficient initial scope control
+ wrong decision-level classification during review resolution
+ portable capability conflated with maintainer certification
+ feasibility proven too late
+ changing boundary during exhaustive modeling
+ oversized coupled milestones
+ high-resolution finding accounting
```

## Classify

| Observation ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | process-follow-up | pending confirmation | Possible proposal scope-budget and split-delivery guidance | Not yet confirmed | A single first release combined several distinct trust boundaries. |
| O2 | process-follow-up | pending confirmation | Possible research/spike and architecture-feasibility gate | Not yet confirmed | The decisive runtime capability was tested after downstream approval. |
| O3 | observation | observation | Session record only | Review inventory and plan history | Review distribution locates churn after proposal direction was settled. |
| O4 | durable-lesson | pending confirmation | Possible boundary-first guidance clarification | Not yet confirmed | Boundary completeness requires a stable subject and cannot compensate for continuing scope expansion. |
| O5 | process-follow-up | pending confirmation | Possible milestone and PR size-budget proposal | Not yet confirmed | Coupled milestone scope increased review and synchronization cost. |
| O6 | observation | observation | Possible future review-metrics proposal | Review artifact contract | Stable identities aid auditability but make raw count an incomplete metric. |
| O7 | durable-lesson | pending confirmation | Proposal, code-review, review-resolution, and workflow escalation guidance | Not yet confirmed | A finding correction that introduces a new mechanism or trust boundary must return to proposal choice rather than enter ordinary contract correction. |
| O8 | direction | pending confirmation | Separate corrective proposal for portable published capability versus optional maintainer compatibility evaluation | Not yet confirmed | Changing the accepted capability baseline and superseding runtime ADRs requires an owning proposal, not a learn-session rule. |

## Candidate Best Practices

These are candidates only until contributor confirmation:

1. Run a disposable, pinned-runtime feasibility probe before approving any architecture whose trust model depends on runtime tools, permissions, isolation, transport, or mutation behavior.
2. Split the work into independently reviewable deliveries: boundary vocabulary and skill guidance; runtime feasibility; enforcement harness; publication/recovery; adapter and rollout integration.
3. Freeze the enforcement boundary before requiring exhaustive proof. If a discovery adds a new trusted component or protocol, route upstream and re-scope rather than absorbing it into the same milestone.
4. Limit each implementation milestone to one primary trust boundary and one rollback unit.
5. Test the smallest composed public path early, before building exhaustive internal matrices around an assumed transport.
6. Track root-cause clusters, failed-remediation rate, review rounds, and final escapes alongside unique material-finding count.
7. Keep durable audit records, but avoid treating their file count as the implementation size or asking reviewers to review generated evidence as if it were authored product logic.
8. Classify the decision level before accepting a review-resolution path: implementation detail, specification completion, architecture choice, or proposal-level direction and scope.
9. Require proposal amendment or a separate proposal when a correction adds a new runtime dependency, process or trust boundary, persistence protocol, compatibility commitment, public capability claim, or independently deployable workstream.
10. Do not let a generic owner approval such as "use the best solution" select a new mechanism implicitly. Present the minimal portable option, maintainer-evaluation option, and runtime-specific option with scope and cost before requesting the decision.
11. Treat the accepted proposal's scope budget as a live invariant. A work item that cannot map to an existing budget row must stop before spec or implementation correction and be explicitly added or separated.
12. Keep published capability and maintainer validation as separate layers.
    Repository-only evaluation may support release confidence, but it cannot be the user-facing capability or a universal portability claim.
13. Limit automatic review-fix authority to corrections inside the already selected mechanism. Discovery of a new mechanism invalidates that bounded correction path and pauses for proposal-level decision.
14. Ask the first question at every rereview: "Does this remain the solution selected by the accepted proposal?" Completeness review follows only after that alignment passes.

## Candidate Project Resolution

The smallest project correction is two separately reviewable decisions.

### 1. Correct the shipped capability

Open a focused proposal that:

- keeps the portable boundary-first skill instructions and packaged reference;
- defines deterministic structural, fixture, packaging, and semantic-review proof as the published capability baseline;
- removes Codex runtime certification from the mandatory portable baseline;
- classifies the existing Codex harness as optional maintainer compatibility evaluation, or retires it if its continuing cost is not justified; and
- explicitly supersedes or narrows affected runtime-specific specification clauses and ADRs rather than deleting implementation first.

### 2. Correct lifecycle escalation

Open a separate small process proposal that:

- defines the proposal-boundary escalation triggers in candidate practice 9;
- requires review findings and owner decisions to name their decision-owning stage;
- prevents bounded review-fix automation from materializing a new mechanism;
- requires proposal intent and scope-budget alignment before every specification, architecture, or implementation rereview; and
- adds regression scenarios for this initiative's exact failure: an implementation finding proposes a runtime-specific harness for a portable skill goal, and the workflow must pause at proposal decision instead of silently revising the spec.

These should remain separate because correcting the current product scope and improving future lifecycle governance have different owners, risks, and rollback paths.

## Route

No derivative routing performed.

Contributor confirmation is required before these candidate classifications may update workflow policy, skills, proposals, specifications, plans, learn topics, or validation behavior.
