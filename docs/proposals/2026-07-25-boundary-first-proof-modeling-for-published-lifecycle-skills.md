# Boundary-First Proof Modeling for Published Lifecycle Skills

## Status

draft

## Problem

RigorLoop requires specifications, test specifications, implementation, and
independent review, but those stages can still translate behavior
example-by-example.

An example can demonstrate one desired outcome without exposing the dimensions
that determine all valid, invalid, stale, interrupted, or adversarial outcomes.
When an implementation follows examples instead of a complete boundary model,
the first exhaustive audit often happens during code review.

The merged single bounded review-fix automation initiative provides direct
evidence.
Its lifecycle recorded 104 material findings, including 82 implementation
code-review findings.
The recurring preventable pattern was not a rejected product direction.
It was incomplete translation of trust, state, authority, transaction,
recovery, compatibility, and composed-command boundaries into direct proof.

Repeated failure shapes included:

- accepting caller-provided evidence instead of deriving canonical truth;
- validating record shape without validating semantics or cross-record
  consistency;
- fixing one reported negative example while leaving a sibling bypass;
- proving a helper without proving the composed public path;
- proving mutation success without interruption, rollback, or reconciliation;
- using a narrow fixture as a substitute for a closed vocabulary or transition
  matrix.

The current workflow does not make the reusable transformation explicit enough:

```text
example
-> governing rule
-> boundary dimensions
-> valid and invalid partitions or transitions
-> important interactions
-> executable proof obligations
```

The result is avoidable review churn, failed remediation, and late discovery of
contract gaps.
The problem is not that RigorLoop uses examples.
The problem is allowing examples to become the implicit completeness model.

## Goals

- Make boundary modeling an explicit, reviewable part of behavior-changing
  work.
- Preserve examples as explanatory and discovery aids while preventing them
  from becoming the proof-coverage owner.
- Require each applicable behavior dimension to have explicit partitions,
  transitions, invariants, and failure behavior.
- Connect specification boundaries to test-spec proof and implementation
  handoff.
- Move the first exhaustive boundary audit before code-review handoff.
- Require sibling-boundary analysis after a material finding instead of only
  patching the reported example.
- Cover canonical truth, identity, authority, state, mutation, recovery,
  composition, compatibility, outcomes, and claims when applicable.
- Keep one standard workflow and use applicability with recorded rationale
  rather than creating lighter and stricter workflow lanes.
- Avoid an unbounded Cartesian-product test requirement by distinguishing
  exhaustive partition coverage from risk-selected interaction coverage.
- Improve published lifecycle skills through the existing workflow and skill
  contracts rather than creating a new one-off skill.
- Establish a reliable capability baseline before resuming capability-preserving
  progressive disclosure.

## Non-goals

- Do not remove examples, counterexamples, or scenario fixtures.
- Do not require every possible input combination to have an individual test.
- Do not make code review less independent or less adversarial.
- Do not treat a checklist alone as proof that boundaries were modeled.
- Do not create separate workflow routes based on change size, speed, or risk.
- Do not require a standalone boundary artifact for every change.
- Do not retroactively invalidate accepted historical artifacts.
- Do not reopen the accepted single bounded review-fix automation direction.
- Do not optimize published-skill context size in this proposal.
- Do not resume or implement the paused capability-preserving
  progressive-disclosure proposal.
- Do not create a new `boundary-review` skill or lifecycle stage.
- Do not encode product judgment in a validator when independent review is the
  appropriate owner.
- Do not use raw review-finding count as the sole quality metric.

## Vision fit

fits the current vision

RigorLoop exists to make AI-assisted changes traceable, reviewable, resumable,
and trustworthy.
Boundary-first proof modeling improves the traceability chain by making it
possible to reconstruct not only which examples were considered, but which
behavioral state space the contract and proof intentionally cover.

This also supports the vision's refusal to reward output volume without
evidence.
The change should reduce avoidable review cycles without weakening independent
review or turning the workflow into mechanical ceremony.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Solve example-driven implementation before progressive disclosure | in scope | Problem, Recommended Direction, Rollout and Rollback |
| Model behavior boundaries exhaustively | in scope | Boundary Completeness Model |
| Apply the solution to published lifecycle skills | in scope | Lifecycle Ownership, Scope Budget |
| Preserve examples where useful | in scope | Rule-to-Example Contract |
| Follow best practices and keep proof practical | in scope | Interaction Coverage, Testing and Verification Strategy |
| Pause capability-preserving progressive disclosure | in scope | Dependency and Sequencing |
| Implement the skill and validator changes immediately | out of scope | Non-goals, Next Artifacts |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Boundary-completeness vocabulary and applicability model | core to this proposal | All downstream ownership depends on a shared definition of completeness. |
| Rule-to-example traceability | core to this proposal | This directly prevents examples from becoming the contract. |
| Spec and test-spec boundary/proof ownership | core to this proposal | Normative behavior and executable proof need distinct owners. |
| Review-stage completeness and sibling-boundary audits | core to this proposal | Independent review must detect omissions and incomplete remediation. |
| Published lifecycle skill behavior updates | same-slice dependency | The policy has no effect unless the stage-owning skills consume it. |
| Workflow and skill-contract amendments | same-slice dependency | Existing canonical contracts should own the new behavior without a competing spec. |
| Deterministic structural validation | first-slice candidate | Stable fields and closed vocabularies can be checked mechanically after the spec settles their shape. |
| Qualitative boundary judgment | core to this proposal | Applicability, meaningful partitions, and interaction hazards require review judgment. |
| Retrospective automation corpus | same-slice dependency | The 104-finding initiative provides realistic positive and omission fixtures. |
| New standalone boundary artifact for every change | rejected option | It would add an owner and ceremony even when existing specs and test specs are sufficient. |
| Historical artifact retrofit | out of scope | Accepted artifacts remain historical evidence and evaluation inputs. |
| Capability-preserving progressive disclosure | separate proposal | It optimizes context only after this initiative establishes the capability baseline. |
| Review-efficiency metrics beyond this pilot | deferable follow-up | Root-cause clusters and failed-remediation rates need evidence before becoming policy. |

## Context

### Governing contracts

The Constitution already requires:

- approved specifications for observable behavior;
- test specifications that operationalize rather than override feature specs;
- concrete proof before behavior claims;
- formal independent reviews with durable material findings;
- exact source-of-truth precedence;
- fail-closed handling of unknown values in validator vocabularies.

The workflow specification owns lifecycle order, artifact handoff, formal
reviews, and implementation readiness.
The published-skill contract owns public skill structure, claim boundaries,
evidence access, progressive disclosure, and behavior-preservation proof.

This proposal keeps that ownership split:

```text
rigorloop workflow contract:
  lifecycle boundary-modeling and proof-handoff behavior

published-skill contract:
  how stage-owning public skills expose and execute that behavior

feature specification:
  normative boundary model for one behavior change

matching test specification:
  executable proof map for that boundary model
```

No new standalone normative boundary-modeling spec is recommended.
The two existing repository contracts should be amended with an exact
cross-spec ownership ledger so they do not duplicate rules.

### Evidence from the automation initiative

The tracked [Single Bounded Review-Fix Finding Volume learn
session](../learn/sessions/2026-07-25-single-bounded-review-fix-finding-volume.md)
found:

| Review family | Findings |
| --- | ---: |
| Proposal and spec review | 13 |
| All pre-implementation review | 22 |
| Implementation code review | 82 |
| Total | 104 |

The count is not a direct quality score.
It includes distinct residual findings and reflects a large state space plus
high-resolution review accounting.

The actionable evidence is the repeated root-cause cluster:
independent code review became the first exhaustive audit of boundary classes
that should already have been explicit in the spec, test spec, and
implementation proof.

### Dependency and sequencing

The separate capability-preserving progressive-disclosure proposal is paused
before proposal review by maintainer direction.

The sequencing invariant is:

```text
settle boundary-first behavior
-> implement and validate its published-skill contract
-> establish the new capability baseline
-> resume progressive-disclosure proposal review
-> evaluate context reduction against that baseline
```

This prevents behavior parity from canonizing a known omission.

## Options Considered

### Option 1: Keep examples and rely on independent code review

Pros:

- No workflow or skill changes.
- Independent review continues to catch real defects.

Cons:

- Code review remains the first exhaustive boundary audit.
- Review cycles stay expensive.
- Implementers can patch findings one example at a time.
- Contract omissions are discovered after code exists.

Rejected.

### Option 2: Add a longer implementation and code-review checklist

Pros:

- Small change.
- Easy to publish.
- Improves recall for known incident classes.

Cons:

- A checklist does not identify the feature-specific state space.
- It can become another list of examples.
- It does not bind spec rules to executable proof.
- Missing dimensions still have no accountable owner.

Rejected as the complete solution.
A compact checklist may be one projection of the accepted contract.

### Option 3: Require one standalone boundary matrix for every change

Pros:

- One visible artifact.
- Easy to review for presence.
- Could support deterministic validation.

Cons:

- Duplicates feature-spec and test-spec ownership.
- Adds ceremony to changes with few applicable dimensions.
- Risks divergence between the matrix, normative requirements, and tests.
- Artifact presence still does not prove semantic completeness.

Rejected as the default.
A project may use a separate artifact when its approved contract explicitly
needs one.

### Option 4: Boundary-first modeling embedded in existing lifecycle owners

The feature spec records applicable dimensions, partitions, transitions,
invariants, outcomes, and compatibility.
The test spec maps those boundaries to direct proof.
The stage-owning skills enforce explicit handoffs and independent completeness
checks.
Deterministic validation checks stable structure and closed vocabularies while
reviewers own semantic judgment.

Pros:

- Keeps normative behavior and proof with their existing owners.
- Creates traceability from rule to partition to test.
- Moves omission detection earlier without adding a workflow stage.
- Supports both simple and stateful changes through explicit applicability.
- Preserves independent review.

Cons:

- Requires coordinated changes to several lifecycle skills.
- Semantic completeness cannot be fully automated.
- Poorly designed applicability rules could create boilerplate.

Recommended.

### Option 5: Generate tests automatically from examples

Pros:

- Fast proof generation.
- Examples remain easy to author.

Cons:

- Automates the same incomplete model.
- Generated tests inherit example blind spots.
- Does not settle trust, state, recovery, or composition boundaries.

Rejected.

## Recommended Direction

Choose Option 4.

Amend the existing workflow and published-skill contracts so behavior-changing
work uses a boundary-first model before implementation handoff.

The method has six connected parts:

1. identify the governing rule behind each example;
2. classify applicable boundary dimensions;
3. enumerate valid, invalid, unknown, stale, and interrupted partitions or
   transitions as appropriate;
4. select important cross-dimension interactions by hazard rather than taking
   an unbounded Cartesian product;
5. map every modeled boundary to executable, deterministic, or explicitly
   manual proof;
6. require sibling-boundary analysis whenever review or validation finds one
   missed member of a boundary class.

### Boundary Completeness Model

The first contract should define a closed core inventory of boundary
dimensions.
Each behavior-changing specification should classify every core dimension as
applicable or not applicable with a concise rationale.

The initial inventory should cover:

| Boundary dimension | Questions the model answers | Representative partitions or proof |
| --- | --- | --- |
| Canonical ownership and trust | Which source owns truth, and which inputs are assertions? | canonical, caller-supplied, missing, contradictory |
| Identity and freshness | Which exact artifact or state does authority bind to? | exact, stale, substituted, changed-after-review |
| Closed vocabularies | Which values are accepted? | every known value plus unknown |
| State and lifecycle transitions | Which moves are legal from each state? | legal, illegal, terminal reopen, ambiguous current state |
| Authorization and scope | Who may perform which mutation against what basis? | absent, valid, revoked, invalidated, scope expansion |
| Mutation and atomicity | What becomes durable, and in which order? | precondition failure, complete write, partial write |
| Interruption and recovery | How does execution resume without repetition or loss? | retry, reconcile, cancel, stale prepared work |
| Concurrency and idempotency | What happens under repetition or competing work? | duplicate request, conflicting in-flight work, replay |
| Composition and bypass | Which public, helper, adapter, and sibling paths enforce the same rule? | direct path, composed path, alternate entry point |
| Compatibility and migration | How are old inputs read and new state written? | old, mixed, unsupported, one-way migration, rollback |
| Outcomes and stop behavior | Which outcomes continue, pause, block, or terminate? | success, changes requested, blocked, inconclusive, unknown |
| Evidence, observability, and claims | What proves completion and what may be reported? | current proof, missing proof, stale proof, overclaim |

The specification stage should be exhaustive at the declared boundary:

- every applicable dimension is represented;
- every closed value and transition class is accounted for;
- invalid and unknown behavior is explicit;
- non-applicability has a reviewable rationale;
- important dimension interactions are selected from concrete hazards.

It should not require exhaustive enumeration of all possible combinations.

### Rule-to-Example Contract

Examples remain useful for communication, regression reproduction, and
evaluation.
They should never be the only owner of behavior.

Every behavior-significant example should resolve to one of:

```text
illustrates a named rule and partition
reproduces a named regression
discovers a missing rule or partition
is non-normative explanatory material
```

An example that discovers a missing rule should cause the owning artifact to be
revised or the work to pause.
It should not be implemented as an isolated special case.

### Interaction Coverage

Exhaustive partition modeling and exhaustive Cartesian testing are different.

The test-spec should cover every partition or transition directly, then select
cross-dimension interactions where failure would be consequential or where
evidence shows coupling.
Typical interactions include:

```text
stale identity + otherwise valid authorization
partial write + retry
cancel + prepared transition
legacy input + new writer
unknown outcome + downstream routing
helper success + composed public-path failure
```

The spec should define a small closed vocabulary for interaction-selection
rationale so omitted combinations are deliberate rather than invisible.

### Lifecycle Ownership

| Stage | Boundary-first responsibility |
| --- | --- |
| `proposal` | Identify boundary-bearing product decisions, trust assumptions, compatibility direction, and unresolved risks without pretending to be the detailed contract. |
| `proposal-review` | Challenge whether the direction leaves architecture or policy decisions for the spec author to invent. |
| `spec` | Own the normative dimensions, partitions, transitions, invariants, outcomes, and non-applicability rationale. |
| `spec-review` | Audit the boundary model for missing dimensions, implicit closed contracts, contradictions, and example-only behavior. |
| `architecture` | Map trust sources, mutation boundaries, persistence, recovery, concurrency, and component ownership when applicable. |
| `architecture-review` | Challenge cross-component bypasses and recovery assumptions. |
| `plan` | Sequence work so boundary proof can be established before dependent implementation. |
| `plan-review` | Reject sequencing that defers foundational negative or recovery proof until after implementation. |
| `test-spec` | Map every modeled boundary to direct positive, negative, stale, tamper, transition, interruption, composition, or manual proof. |
| `test-spec-review` | Independently audit dimension, partition, interaction, fixture, selector, and milestone coverage. |
| `implement` | Establish the planned proof before or with code, derive trusted evidence from canonical owners, and perform a sibling-boundary sweep before handoff. |
| `code-review` | Review the actual diff for omitted dimensions, sibling bypasses, unproved composed paths, and incomplete remediation. |
| `verify` | Confirm spec, test-spec, implementation, review resolution, and final evidence remain coherent. |
| `workflow` | Route and stop on missing required boundary or proof evidence without creating a new stage. |

### Review-Finding Resolution

When a material finding exposes one missed member of a boundary class, the
resolution should include:

```text
reported example
root boundary class
sibling inputs, transitions, or paths inspected
governing artifact updated when the contract was incomplete
direct regression proof
broader proof or rationale for unaffected siblings
```

This does not allow implementation to broaden accepted product scope.
If the sibling sweep discovers a new product decision or incompatible behavior,
the run should pause for the owning artifact or maintainer decision.

### Mechanical and Judgment Boundaries

Repository-owned validators may check:

- required stable fields and IDs;
- closed vocabulary values;
- trace links from requirements to boundary entries and proof cases;
- missing classifications or non-applicability rationales;
- duplicate or orphan entries;
- unknown values before consistency checks;
- selected fixture and validation registration.

Validators should not claim to determine:

- whether all domain-specific dimensions were discovered;
- whether a partition is semantically meaningful;
- whether interaction coverage matches product risk;
- whether a reviewer's adversarial reasoning is sufficient.

Those remain explicit review responsibilities.

## Expected Behavior Changes

After adoption:

- behavior-changing specs expose applicable boundary dimensions instead of
  relying on examples and edge-case prose alone;
- examples identify the rule or partition they illustrate;
- spec review can request changes for an implicit closed contract even when all
  listed examples are internally consistent;
- test specs map each modeled partition and transition to concrete proof;
- implementation handoff pauses when required boundary proof is missing or
  stale;
- implementers resolve a finding by inspecting its sibling boundary class;
- code review still performs an independent adversarial audit and records any
  residual omission;
- unknown closed-vocabulary values fail closed before consistency behavior;
- simple behavior changes use the same workflow and record non-applicable
  dimensions rather than entering a reduced workflow lane;
- progressive-disclosure work remains paused until this capability baseline is
  accepted and implemented.

## Architecture Impact

The proposal primarily changes workflow and public skill contracts.
An architecture assessment is still required because deterministic validation
may touch:

```text
feature-spec and test-spec templates or assets
published lifecycle skill bodies or packaged references
traceability and artifact validators
validation selectors and fixtures
generated public adapter packages
```

The architecture assessment should decide whether a typed intermediate model is
useful for validation.
It should preserve these ownership boundaries:

```text
feature spec:
  normative behavior

test spec:
  proof operationalization

published skills:
  stage procedure and handoff

validators:
  structural and closed-vocabulary checks

reviewers:
  semantic completeness and judgment
```

No new durable artifact type or lifecycle stage is assumed.

## Testing and Verification Strategy

The downstream test strategy should combine structural, behavioral, and
incident-replay proof.

### Contract and traceability proof

- Every core boundary dimension has a closed identity.
- Every applicable dimension maps to a feature-spec rule.
- Every modeled partition or transition maps to one or more test-spec cases.
- Every non-applicable dimension carries a rationale.
- Every example maps to a rule, regression, discovery gap, or explicit
  non-normative role.
- Unknown enum and illegal transition cases are present where closed contracts
  apply.

### Published-skill behavior proof

- `spec` produces boundary-complete requirements rather than only examples.
- `spec-review` finds an intentionally omitted trust or transition dimension.
- `test-spec` maps positive, negative, stale, tamper, interruption, and
  composition cases when triggered.
- `test-spec-review` rejects a proof map that covers examples but omits a
  declared partition.
- `implement` stops on a contract gap instead of inventing behavior.
- `code-review` expands a seeded example defect into its sibling boundary
  class.
- `verify` detects contract–proof–implementation drift.
- Manual isolated skill invocations retain their existing claim boundaries.

### Incident replay

Use representative findings from the merged automation initiative as an
evaluation corpus:

- caller-supplied versus canonical evidence;
- known versus unknown enum values;
- legal versus illegal state transitions;
- exact versus stale or substituted identity;
- complete versus partial writes;
- fresh execution versus retry or reconciliation;
- helper versus composed public-command path;
- one bypass versus a sibling bypass.

The corpus should prove that the new process surfaces the missing class before
code-review handoff where the governing evidence is available.
It should not rewrite the historical review record.

### Validation layering

Run the repository selector for touched paths, execute selected focused checks,
then run broader smoke only when the accepted test spec or another authoritative
trigger requires it.
Final evidence should name the commands actually run.

## Rollout and Rollback

Roll out in this order:

1. settle the proposal through independent proposal review;
2. amend the workflow and published-skill contracts with an exact ownership
   ledger;
3. review the specification before changing public skills;
4. assess architecture for validator, resource, adapter, and template impact;
5. create and independently review the proof map;
6. update the affected lifecycle skills and deterministic checks in reviewable
   slices;
7. replay representative automation boundary failures;
8. establish the accepted boundary capability baseline;
9. decide whether to resume the paused progressive-disclosure proposal.

Compatibility behavior:

- accepted historical artifacts remain valid;
- new behavior-changing work uses the contract after its adoption point;
- active work at adoption records whether it adopts the new proof model or
  finishes under its already approved contract;
- published adapters remain generated from canonical `skills/` sources;
- no user is required to add a new artifact merely because this proposal
  exists.

Rollback:

- revert skill, validator, template, and adapter changes together;
- keep historical proposal, review, and learning evidence;
- return to existing workflow behavior without interpreting partial boundary
  records as approved proof;
- keep progressive disclosure paused until the capability baseline is again
  settled.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Boundary modeling becomes a long generic checklist. | Require feature-specific partitions, transitions, and trace links; presence alone is not approval. |
| Teams interpret “exhaustive” as every input combination. | Define exhaustive dimension and partition coverage separately from hazard-selected interaction coverage. |
| Simple changes accumulate boilerplate. | Use the same workflow with concise non-applicability rationales and no new universal artifact. |
| Specs become test implementations. | Keep normative behavior in the spec and concrete fixtures or commands in the test spec. |
| Test specs override product behavior. | Require every proof entry to trace to an approved rule and pause on gaps. |
| Validators make false semantic claims. | Limit automation to stable structure, closed vocabularies, and traceability; leave completeness judgment to review. |
| Review loses independence because authors self-certify completeness. | Preserve independent spec, test-spec, and code-review audits. |
| Finding remediation expands scope. | Pause when sibling analysis discovers a new product decision or incompatible behavior. |
| The workflow overfits one automation incident. | Use the incident as a corpus while defining model-neutral dimensions applicable to other stateful behavior. |
| Historical work appears invalid. | Apply the contract prospectively and preserve historical artifacts as evidence. |
| Multiple specs become contradictory. | Keep workflow behavior and public-skill projection with their existing owners and add an exact cross-spec ownership ledger. |
| Progressive disclosure resumes too early. | Require an explicit resume decision after the boundary capability baseline is accepted and implemented. |

## Open Questions

None block proposal review.

The specification should settle:

1. the exact closed IDs and required fields for the core boundary dimensions;
2. the closed vocabulary for applicability and interaction-selection rationale;
3. which behavior changes trigger a detailed boundary table versus a concise
   embedded classification;
4. the exact trace-link shape among requirements, boundary entries, examples,
   and test cases;
5. which structural checks are deterministic enough for repository validators;
6. the minimum incident-replay corpus for behavior-preservation evidence;
7. the exact cross-spec ownership ledger between
   `specs/rigorloop-workflow.md` and `specs/skill-contract.md`;
8. the adoption rule for active initiatives at the implementation boundary.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-25 | Solve boundary-first proof modeling before progressive disclosure. | Context optimization should preserve a complete capability baseline, not a known omission. | Run both proposals concurrently; optimize first and repair later. |
| 2026-07-25 | Preserve examples as subordinate evidence. | Examples are valuable for explanation and regression but cannot establish completeness. | Remove examples; generate behavior only from examples. |
| 2026-07-25 | Embed boundary ownership in existing specs and test specs. | These artifacts already own normative behavior and executable proof. | Require a new standalone boundary artifact for every change. |
| 2026-07-25 | Amend existing workflow and skill contracts. | The behavior crosses lifecycle handoff and published-skill execution but does not justify another competing contract. | Create a standalone boundary-modeling spec; put all rules in skill prose. |
| 2026-07-25 | Require closed core dimensions with explicit applicability. | Silent omissions need a visible review surface without creating separate workflow lanes. | Use an optional checklist; apply only to high-risk work. |
| 2026-07-25 | Separate partition completeness from interaction selection. | Full Cartesian testing is usually infeasible, while omitted partitions remain unsafe. | Require every combination; sample examples only. |
| 2026-07-25 | Preserve independent review. | Earlier self-audit reduces churn but cannot replace adversarial review. | Treat a completed author checklist as approval. |
| 2026-07-25 | Use automation findings as an evaluation corpus, not a quality oracle. | Root-cause classes are reusable; raw counts are not directly comparable. | Set a finding-count target. |
| 2026-07-25 | Avoid a new lifecycle skill or stage. | Existing stages already have the necessary artifact and review owners. | Add `boundary-review`. |

## Next Artifacts

```text
proposal-review
spec amendments:
  specs/rigorloop-workflow.md
  specs/skill-contract.md
spec-review
architecture assessment
architecture and ADR updates when required
architecture-review when required
plan
plan-review
test-spec amendments:
  specs/rigorloop-workflow.test.md
  specs/skill-contract.test.md
test-spec-review
implementation
code-review
explain-change
verify
pr
resume decision:
  capability-preserving progressive disclosure
```

## Follow-on Artifacts

None yet

## Readiness

Ready for `proposal-review`.

The proposal does not claim acceptance, specification readiness,
implementation readiness, review efficiency improvement, or progressive-
disclosure readiness.
