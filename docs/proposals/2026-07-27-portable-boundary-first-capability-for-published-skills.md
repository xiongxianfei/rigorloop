<!-- Template: proposal-skeleton-v1 -->
<!-- Skill: proposal -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/proposal/SKILL.md -->
<!-- Readability contract: use semantic source lines; keep stable IDs and tables for repeated proof or mapping structures. -->

# Portable Boundary-First Capability for Published Skills

## Status

accepted

## Problem

Published lifecycle skills can describe desired behavior through examples
without requiring the governing boundary model to be complete.
An example proves one outcome, but it does not by itself identify every
applicable valid, invalid, unknown, stale, interrupted, or adversarial state.

A prior unmerged candidate attempted to solve this by combining portable
boundary-first skill guidance with live certification of one exact Codex
runtime.
That candidate demonstrated an important distinction:

```text
portable published-skill capability
!=
repository-maintainer certification of one runtime
```

Published-skill users receive skill instructions and packaged references.
They do not receive or operate repository-local app-server probes, runtime
identity registries, immutable evidence publication, or recovery machinery.
Making those facilities part of the capability baseline would bind a portable
workflow product to a maintainer-only and vendor-specific execution system.

The project needs a smaller solution that helps published-skill users model
boundaries before implementation while keeping deterministic validation,
packaging proof, and semantic review with their proper owners.

## Goals

- Publish a portable boundary-first method through existing lifecycle skills.
- Preserve examples as explanation and discovery aids without treating them as
  the completeness owner.
- Give feature specs a reviewable way to identify applicable behavior
  dimensions, partitions, transitions, invariants, and outcomes.
- Give test specs a traceable way to map each applicable boundary to proof.
- Give plans a traceable way to turn applicable boundaries into isolated
  milestones, dependencies, rollback units, and proof timing.
- Require implementation and code review to inspect sibling, public, helper,
  failure, stale, and recovery paths when applicable.
- Keep semantic adequacy with independent review.
- Use deterministic repository validation only for structure, closed
  vocabularies, references, fixtures, packaging, and parity.
- Package the required boundary reference with every governed public skill.
- Define a small closed first-version boundary vocabulary and stable
  contract-to-proof identities before specification.
- Activate the contract prospectively without invalidating accepted historical
  artifacts or allowing mixed governed-skill behavior.
- Keep the capability independent of Codex, Claude Code, opencode, model
  identity, runtime version, network access, or workspace mutation behavior.
- Establish a portable baseline that later progressive-disclosure work can
  preserve without depending on one runtime.

## Non-goals

- Do not build or require a live agent-runtime certification harness.
- Do not bind the capability to Codex, a model ID, executable bytes, feature
  flags, app-server schemas, or permission profiles.
- Do not require published-skill users to clone this repository or run its
  validators.
- Do not claim that structural validation proves semantic completeness.
- Do not generate tests automatically from examples.
- Do not require a Cartesian product of every boundary dimension.
- Do not introduce a new lifecycle stage or standalone boundary-review skill.
- Do not require `proposal` or `proposal-review` to author the normative
  first-version boundary model.
- Do not add repository-local evidence publication, runtime attestation,
  transaction recovery, or file-change interception.
- Do not decide capability-preserving progressive disclosure in this proposal.
- Do not revive or merge the closed runtime-certification candidate.

## Vision fit

fits the current vision

The project vision requires RigorLoop to remain useful across sessions, agents,
and public adapters rather than becoming a vendor-specific control plane.
A portable boundary contract improves traceability and reviewability without
requiring a platform migration or hosted runtime.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Preserve portable boundary-first skill instructions | in scope | Goals, Recommended Direction |
| Preserve the packaged boundary reference | in scope | Recommended Direction, Architecture Impact |
| Preserve deterministic structural and fixture validation | in scope | Recommended Direction, Testing and Verification Strategy |
| Preserve packaging parity | in scope | Architecture Impact, Testing and Verification Strategy |
| Preserve independent semantic review | in scope | Goals, Recommended Direction |
| Remove Codex runtime certification from the required capability | in scope | Non-goals, Recommended Direction |
| Define the first-version boundary vocabulary and record relationships | in scope | First-version portable contract |
| Include planning and plan review in the governed lifecycle path | in scope | Scope budget, First-version portable contract |
| Select one-source deterministic reference projection | in scope | First-version portable contract, Architecture Impact |
| Define prospective activation and historical compatibility | in scope | First-version portable contract, Rollout and Rollback |
| Decide progressive disclosure | deferred follow-up | Non-goals, Next Artifacts |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Boundary vocabulary and record relationships | core to this proposal | Published skills need one shared language and stable contract-to-proof identities. |
| Spec and test-spec ownership | core to this proposal | Normative behavior and executable proof need distinct owners. |
| Plan and plan-review ownership | core to this proposal | Boundary dependencies, milestone isolation, rollback units, and proof timing need explicit owners. |
| Ten lifecycle skill projections | same-slice dependency | The governed path covers `workflow`, specification, planning, proof design, implementation, review, and verification. |
| Packaged shared reference | same-slice dependency | Users need the method without repository-only documentation. |
| One-source deterministic projection | same-slice dependency | Skill-local self-containment and parity require one canonical owner without hand-maintained copies. |
| Structural and fixture validation | same-slice dependency | Stable shapes and known omission classes can be checked deterministically. |
| Adapter resource and packaging parity | same-slice dependency | Every supported adapter must ship the same reference bytes and mappings. |
| Independent semantic review guidance | core to this proposal | Applicability and completeness require judgment rather than validator inference. |
| Prospective activation and compatibility | core to this proposal | Adoption must be deterministic without retroactively invalidating accepted artifacts. |
| Live runtime compatibility evaluation | separate proposal | It has different users, dependencies, claims, risks, and rollback behavior. |
| Runtime attestation and immutable behavior publication | out of scope | These do not create a capability available to published-skill users. |
| Progressive-disclosure optimization | separate proposal | It consumes the accepted portable baseline after this change settles. |

## Context

RigorLoop publishes canonical skills from `skills/` through adapter packages.
The repository supports Codex, Claude Code, and opencode and explicitly refuses
to become a vendor-specific control plane.

The useful part of the prior boundary-first candidate was the portable
contract:

```text
governing rule
-> applicable dimensions
-> partitions or transitions
-> important interactions
-> proof obligations
-> implementation and review handoff
```

The non-portable part attempted to establish the same capability by executing
skills through one exact runtime and publishing repository-local evidence.
That mechanism could provide maintainer evaluation for that runtime, but it
was neither necessary nor sufficient to make the capability available to
users of every published adapter.

This proposal treats published content as the capability and treats
repository validation as supporting release evidence.

## Options Considered

### Option 1: Continue with examples and ordinary independent review

This has the smallest implementation cost.
It leaves code review as the first likely exhaustive boundary audit and does
not connect examples to their governing rules or proof obligations.

Rejected because it preserves the observed example-first failure mode.

### Option 2: Adopt the full runtime-certification candidate

This can observe one configured runtime executing selected scenarios.
It adds runtime identity, process isolation, transport, file-change control,
publication, recovery, and vendor-specific compatibility obligations.

Rejected because published users cannot use the mechanism and its result
cannot establish portability across other runtimes or adapters.

### Option 3: Publish a portable boundary contract with deterministic support

Existing lifecycle owners receive stage-appropriate boundary responsibilities.
A packaged reference carries the shared method.
Repository validators check only deterministic structure, references,
fixtures, resource packaging, and parity.
Independent reviews decide semantic completeness.

Recommended because it directly improves the user-visible skill capability
with the smallest complete cross-stage change.

### Option 4: Publish the portable contract and require live evaluation for every adapter

This could provide additional compatibility observations.
It would require comparable runtime APIs, isolation, evidence, and model
behavior across adapters that do not expose identical control surfaces.

Rejected as a baseline requirement.
A later proposal may define optional adapter-specific evaluation with narrow
claims after the portable capability is established.

## Recommended Direction

Choose Option 3.

Publish one shared boundary-first reference and project only the
stage-appropriate responsibilities into ten existing lifecycle skills.

The portable method is:

1. connect every behavioral example to a governing rule;
2. classify a closed core of boundary dimensions as applicable or
   not applicable with rationale;
3. define the relevant partitions, transitions, invariants, failure outcomes,
   and compatibility behavior;
4. select cross-boundary interactions based on actual hazards rather than a
   Cartesian product;
5. map every applicable boundary and selected interaction to automated,
   manual, or hybrid proof;
6. implement against that proof map;
7. independently review completeness and sweep sibling boundaries after an
   escape.

The ownership split is:

| Owner | Responsibility |
| --- | --- |
| Feature spec | Normative dimensions, boundaries, interactions, and outcomes |
| Test spec | Proof obligations and test or manual-evidence mapping |
| Published skills | Stage-local authoring, review, handoff, and stop behavior |
| Shared packaged reference | Portable vocabulary, record shapes, and method |
| Repository validators | Deterministic shape, closed-set, reference, fixture, and packaging checks |
| Independent reviewers | Applicability, completeness, risk selection, and evidence adequacy |

No runtime execution, model compliance, or repository-local behavior report is
part of the portable capability predicate.

## First-version portable contract

### Core dimensions

The first version uses this closed applicability inventory:

| Dimension ID | Dimension | Typical questions |
| --- | --- | --- |
| `input-domain` | Inputs and value partitions | absent, empty, malformed, minimum, maximum, unknown |
| `state-lifecycle` | Valid state and transitions | initial, active, stale, terminal, invalid transition |
| `identity-authority` | Identity, ownership, and permission | wrong owner, missing authority, stale identity, privilege boundary |
| `composition-path` | Public, helper, sibling, and composed paths | public API, helper, alternate entry point, bypass route |
| `temporal-retry` | Ordering, duplication, retry, and concurrency | duplicate, reordering, retry, race, idempotency |
| `failure-recovery` | Failure, interruption, and recovery | partial work, timeout, rollback, resume, failed dependency |
| `compatibility-migration` | Version and historical compatibility | old client, old data, mixed version, migration, rollback |
| `external-environment` | External systems and operating environment | unavailable dependency, resource limit, filesystem, network, platform |

Each dimension is classified as exactly `applicable` or `not-applicable`.
A `not-applicable` result carries a concise rationale.
If applicability cannot be decided from the governing contract, spec review
blocks rather than recording a durable third applicability state.
The inventory does not require every possible partition or a Cartesian product
of interactions.

### Feature-spec boundary records

Each feature-spec boundary record relates:

| Field | Purpose |
| --- | --- |
| `Boundary ID` | Stable identity such as `BND-STATE-001` |
| `Dimension` | One closed first-version dimension |
| `Governing requirements` | Existing normative requirement IDs |
| `Applicability` | `applicable` or `not-applicable` |
| `Rationale` | Why the dimension or boundary applies or does not apply |
| `Partitions / transitions` | Relevant members only |
| `Invariants` | Properties preserved across the boundary |
| `Outcomes` | Success, failure, stale, interrupted, and recovery behavior when relevant |
| `Selected interactions` | Hazard-driven cross-boundary cases |
| `Owner` | Owning requirement or upstream decision |

### Test-spec proof records

Each test-spec proof record relates:

| Field | Purpose |
| --- | --- |
| `Boundary ID` | An identity already present in the approved feature spec |
| `Proof IDs` | Automated test IDs or manual-proof IDs |
| `Proof level` | Unit, integration, contract, end-to-end, smoke, or manual |
| `Command IDs` | Validation commands when command-owned |
| `Evidence artifact` | Required durable evidence location |
| `Required milestone` | Point at which proof becomes mandatory |
| `Uncovered gap` | Upstream route when proof cannot satisfy the governing boundary |

Test specs do not invent boundary IDs or normative outcomes.
An uncovered gap returns to the governing feature spec or upstream decision.

### Example ownership

Every behavioral example is classified as exactly one of:

```text
illustrates an existing governed boundary
regresses a previously observed defect
exposes a contract gap that must return upstream
```

An example does not create a normative boundary implicitly.

### Governed lifecycle skills

The first version governs:

```text
workflow
spec
spec-review
plan
plan-review
test-spec
test-spec-review
implement
code-review
verify
```

The normative boundary model begins at feature-spec authoring.
`proposal` and `proposal-review` remain outside the first-version authoring
contract, although proposals may identify boundary risks as decision input.

| Skill | Boundary-first responsibility |
| --- | --- |
| `workflow` | Route the method, locate governing artifacts, and block on missing applicable ownership. |
| `spec` | Author the normative boundary model. |
| `spec-review` | Judge applicability, partition completeness, selected interactions, invariants, outcomes, and example ownership. |
| `plan` | Convert applicable boundaries into isolated milestones, dependencies, rollback units, affected surfaces, and proof timing. |
| `plan-review` | Reject coupled trust boundaries, omitted dependencies, and proof sequencing that cannot close independently. |
| `test-spec` | Map every applicable boundary and selected interaction to proof. |
| `test-spec-review` | Judge proof adequacy, negative coverage, fixtures, command ownership, and manual-proof boundaries. |
| `implement` | Stop on missing boundary or proof ownership and implement against the approved model. |
| `code-review` | Check composed public, helper, sibling, failure, stale, recovery, and escaped-boundary paths. |
| `verify` | Confirm contract-to-proof-to-implementation coherence and unresolved-gap closure. |

Deterministic validators verify shape, IDs, closed values, references,
fixtures, and packaging.
`spec-review` approves semantic boundary completeness.
`plan-review` approves sequencing and milestone isolation.
`test-spec-review` approves proof adequacy.
`code-review` approves implementation fidelity.
`verify` confirms final evidence coherence without replacing those judgments.

### Shared reference

The portable method is a versioned `READ` reference named
`boundary-first-method-v1.md`, not a copy-and-fill asset.

One canonical source projects deterministically into each governed skill at:

```text
references/boundary-first-method-v1.md
```

Projected copies are not hand-edited.
Every governed `SKILL.md` declares a stage-specific `READ` resource-map entry.
Canonical, projected, generated, packed, and installed copies retain byte
parity.
The exact canonical repository path remains an architecture decision, but the
one-source, deterministic-projection model is settled here.

The shared reference owns the dimension vocabulary, boundary and proof record
fields, interaction-selection method, example classifications, and portable
worked examples.
Stage-specific stop conditions, review approval semantics, artifact placement,
lifecycle routing, and readiness claims remain in governing specs and skills.

### Activation

Feature specs identify adoption with:

```yaml
boundary_contract: boundary-first-v1
```

After repository activation, the marker applies to new behavior-changing
feature specs and existing specs receiving a substantive normative revision.
An in-flight change may opt in before test-spec approval.

A substantive revision changes at least one of:

```text
public or internal behavior
state transitions
input or error behavior
identity, ownership, permission, or security rules
persistence or data shape
compatibility or migration behavior
external integration
concurrency, retry, or idempotency behavior
failure, interruption, rollback, or recovery behavior
```

Spelling, formatting, links, status settlement, review-record references, and
non-normative example clarification do not activate the contract by
themselves.

Activation does not occur until the shared method, all ten governed skill
projections, validators, review fixtures, generated output, adapter parity,
and installed-skill cold-read proof are current together.
A feature spec does not claim `boundary-first-v1` while governed skills have
mixed behavior.
Accepted historical artifacts remain valid until substantively revised.

## Expected Behavior Changes

- A behavior-changing spec records an explicit boundary model or a bounded
  non-applicability rationale under the approved contract.
- Examples identify whether they illustrate a governed boundary, regress a
  known failure, or expose a contract gap.
- A test spec maps every applicable boundary and selected interaction to
  concrete proof.
- A plan maps applicable boundaries to closeable milestones, dependencies,
  rollback units, affected surfaces, and proof timing.
- Implementation stops when a required boundary lacks an approved owner or
  proof obligation.
- Code review checks the composed public path and sibling members of any
  escaped boundary class.
- Verify checks contract-to-proof-to-implementation coherence without claiming
  that deterministic structure validation proves semantic adequacy.
- Installed adapter skills include the same mapped boundary reference as their
  canonical source.
- Activated feature specs identify `boundary-first-v1`; historical accepted
  contracts remain valid until substantively revised.
- Users can apply the complete method using only the published skill package
  and their project artifacts.

## Architecture Impact

The expected architecture impact is limited to authored skill content,
packaged references, deterministic validation, fixtures, and adapter packaging.

Likely touched surfaces are:

- `skills/<skill>/SKILL.md` for the ten governed skills;
- one canonical versioned boundary reference projected deterministically into
  each governed skill's `references/` directory;
- `specs/rigorloop-workflow.md` and `specs/skill-contract.md`;
- matching test specs;
- existing skill and adapter validators;
- deterministic omission fixtures and validation selection.

The architecture assessment should confirm:

- one canonical shared reference owner;
- deterministic projection and byte parity for skill-local, generated, packed,
  and installed copies;
- no repository-root resource dependency in installed skills;
- no live runtime, network, sandbox, process-isolation, or model dependency;
- no new durable behavior-evidence store;
- no claim that a maintainer check is user-executable capability.

## Testing and Verification Strategy

The test strategy should prove:

- every governed skill maps the required shared reference;
- canonical, generated, packed, and installed adapter resources remain
  byte-identical where the adapter contract requires parity;
- required structural fields and closed vocabularies reject missing,
  duplicate, unknown, stale, and conflicting references;
- deterministic fixtures cover representative structural omissions from
  specification, planning, test-spec, implementation, and review handoffs;
- simple changes can classify dimensions as not applicable without false
  blocking or universal artifact creation;
- boundary examples cannot become normative owners;
- test specs cannot invent boundary IDs absent from the governing spec;
- code-review guidance requires public-path and sibling-boundary checks;
- bounded independent review exercises use structurally valid but
  substantively incomplete fixtures to confirm that `spec-review`,
  `plan-review`, and `test-spec-review` report the expected omission classes.

Validation should use existing repository-owned skill, adapter, fixture, and
selector test surfaces.
It should not invoke an agent runtime to establish pass or fail.
Semantic-review exercises produce durable review evidence with named fixture
inputs and expected findings.
They demonstrate the reviewed guidance against those cases only; they do not
certify a model, runtime, or universal semantic completeness.

## Rollout and Rollback

Roll out prospectively after the portable contract, all ten skills, packaged
reference, fixtures, validators, generated output, adapter parity, and
installed-skill cold-read proof are reviewed together.

Existing accepted historical artifacts remain valid.
New or substantively revised behavior contracts adopt the portable boundary
model after the repository activation point.
In-flight changes may opt in before test-spec approval.
Partial activation across the governed skill set is not supported.

Rollback stops new activation and removes the active published projections as
one coherent compatibility change.
Artifacts already accepted under `boundary-first-v1` remain valid historical
contracts; rollback does not delete their boundary models or proof mappings.
Because the baseline introduces no runtime service, evidence database, or
published transaction format, rollback remains a content and packaging change.

The closed runtime-certification candidate is not a migration source and does
not require compatibility support from `main`.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Boundary records become boilerplate | Require concise applicability rationale and avoid standalone artifacts by default. |
| Teams enumerate dimensions mechanically | Keep semantic completeness with independent review and include structurally valid but incomplete fixtures. |
| Proof requirements become a Cartesian product | Select interactions by documented hazards and require exhaustive partitions only within applicable dimensions. |
| Published references drift across adapters | Extend existing canonical-to-package resource and parity checks. |
| Validators overclaim correctness | Limit validator outcomes to structural and referential properties; reserve semantic claims for review evidence. |
| Simple changes are falsely blocked | Include small-change fixtures with justified non-applicability and no extra universal artifact. |
| Runtime evaluation is reintroduced implicitly | Keep runtime certification explicitly outside the capability predicate and require a separate proposal for it. |
| Planning recreates a coupled trust-boundary milestone | Make plan-review reject milestones that cannot close one primary boundary and its proof independently. |
| Activation leaves mixed skill behavior | Gate the marker on all ten projections, validators, packages, and installed-skill proof becoming current together. |

## Open Questions

None block proposal review.

The specification should formalize field syntax, ID grammar, validation error
behavior, and activation enforcement for the selected model.
Architecture should select the exact canonical reference path and projection
mechanism while preserving the settled one-source and byte-parity contract.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-27 | Define the capability by portable published content and project artifacts. | Users must be able to apply the method without repository-local runtime infrastructure. | Full runtime certification; examples alone |
| 2026-07-27 | Keep semantic completeness under independent review. | Applicability and missing-boundary judgment cannot be established by structural validation. | Validator-owned semantic approval |
| 2026-07-27 | Limit deterministic validation to structure, fixtures, packaging, and parity. | These properties are reproducible and portable across supported adapters. | Live agent execution as the capability gate |
| 2026-07-27 | Keep runtime compatibility evaluation separate. | It has different users, claims, dependencies, and rollback behavior. | Bundling it into the portable baseline |
| 2026-07-27 | Use eight closed first-version dimensions and two applicability states. | The proposal must bound user burden and cross-stage identity before specification. | Letting the specification choose the model |
| 2026-07-27 | Govern ten lifecycle skills, including plan and plan-review. | Planning owns boundary isolation, dependencies, rollback units, and proof timing. | Calling an eight-skill path end-to-end |
| 2026-07-27 | Package a versioned `READ` reference through one-source deterministic projection. | Installed skills need self-contained guidance without hand-maintained copies. | Repository-root dependency; copied template; manual duplicates |
| 2026-07-27 | Activate through `boundary_contract: boundary-first-v1` prospectively and atomically. | Compatibility needs deterministic adoption and historical grandfathering. | Retroactive migration; partial activation |

## Acceptance Criteria

| ID | Criterion |
| --- | --- |
| `AC-PBF-001` | A closed first-version dimension vocabulary exists. |
| `AC-PBF-002` | Feature-spec and test-spec record relationships are defined. |
| `AC-PBF-003` | Every example links to a governed boundary, known-defect regression, or explicit contract gap. |
| `AC-PBF-004` | `plan` and `plan-review` are included in the governed skill set. |
| `AC-PBF-005` | Every governed stage has one named semantic or deterministic responsibility. |
| `AC-PBF-006` | The shared method is a versioned `READ` reference rather than a copied template. |
| `AC-PBF-007` | One canonical source deterministically projects skill-local copies. |
| `AC-PBF-008` | Canonical, projected, generated, packed, and installed reference bytes match. |
| `AC-PBF-009` | Validators do not claim semantic completeness. |
| `AC-PBF-010` | Spec-review, plan-review, and test-spec-review own their distinct semantic judgments. |
| `AC-PBF-011` | The prospective activation marker and substantive-revision rule are closed. |
| `AC-PBF-012` | Existing accepted historical artifacts are not retroactively invalidated. |
| `AC-PBF-013` | No runtime, model, network, sandbox, or workspace-mutation dependency is introduced. |
| `AC-PBF-014` | Simple changes can use concise non-applicability rationales without a standalone boundary artifact. |

## Next Artifacts

If accepted:

1. amend the workflow and published-skill contracts;
2. perform `spec-review` on the amended contracts;
3. perform an architecture assessment limited to reference ownership,
   validation, fixtures, and adapter packaging;
4. perform `architecture-review`;
5. create an execution plan with small skill, validation, and packaging slices;
6. perform `plan-review`;
7. create matching test-spec proof maps;
8. perform `test-spec-review`;
9. begin implementation only after those gates pass.

The separate capability-preserving progressive-disclosure proposal remains
paused until this portable baseline is accepted and implemented.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent `proposal-review`.
The proposal now selects the first-version vocabulary, governed lifecycle
owners, shared-reference projection model, and prospective activation policy.
It preserves every requested capability component, excludes runtime
certification, and leaves only field syntax and architecture mechanism details
to downstream artifacts.
