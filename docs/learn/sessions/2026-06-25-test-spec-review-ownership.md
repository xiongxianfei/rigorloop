# Learn Session: Test Spec Review Ownership

## Frame

- Trigger: explicit maintainer invocation: "`$learn` test spec is still active. Who should own the duty to approve it? Should we consider add test-spec-review skill? What're the best practices?"
- Trigger type: maintainer request and workflow-process observation.
- Date: 2026-06-25
- Scope:
  - lifecycle ownership for top-level test specs;
  - whether a dedicated `test-spec-review` gate or skill should exist;
  - immediate guidance for the active independent adversarial review gates change.
- Evidence in scope:
  - `CONSTITUTION.md`
  - `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
  - `specs/review-independence-and-criticality.test.md`
  - `docs/learn/README.md`
  - `docs/learn/topics/workflow-stage-order.md`
  - `docs/learn/sessions/2026-05-25-plan-before-test-spec-public-framing.md`
  - `docs/learn/sessions/2026-05-08-spec-review-rounds-and-readiness.md`
- Explicit exclusions:
  - no workflow, spec, validator, or skill behavior change in this learn session;
  - no new `test-spec-review` skill created from learn alone;
  - no claim that the active M1 implementation review is complete;
  - no PR readiness or final verification claim.
- Prior learnings reviewed:
  - `docs/learn/topics/workflow-stage-order.md` records that `plan` comes before `test-spec`.
  - `docs/learn/sessions/2026-05-08-spec-review-rounds-and-readiness.md` records that test-spec readiness is downstream proof-design readiness, not the immediate next stage after spec-review.
- Session record path: `docs/learn/sessions/2026-06-25-test-spec-review-ownership.md`

## Observe

### O1. Test specs have a settled artifact state but no named formal review owner

Evidence:

- `specs/rigorloop-workflow.md` classifies `Test spec` as authored by `test-spec`, with review skill `repository-defined review surface`, settlement state `active`, and terminal states `abandoned`, `superseded`, or `archived`.
- `docs/workflows.md` mirrors the durable state rule: `Test spec` settlement state is `active`.
- `CONSTITUTION.md` says non-trivial work must read the matching test spec when one exists and that the test spec operationalizes, but does not override, the approved feature spec.
- The active `specs/review-independence-and-criticality.test.md` is marked `active` and is relied on before implementation.

Observation:

The current workflow distinguishes test-spec settlement from proposal/spec/architecture approval. That is coherent: a test spec is not a new product contract; it is the proof map for an already-approved contract and plan. But there is no named independent owner for judging whether that proof map is adequate before implementation begins.

### O2. Plan-review and code-review cannot fully own test-spec approval

Evidence:

- The canonical order is `plan-review -> test-spec -> implement -> code-review`.
- Prior learn guidance explains that test spec comes after plan so it can map milestone order, dependencies, rollback boundaries, and validation surfaces.
- Code-review happens after implementation has already used the test spec.

Observation:

`plan-review` can approve that the plan is test-spec-ready, but it cannot review the authored test spec because the test spec does not exist yet. `code-review` and `verify` can detect test adequacy defects later, but using them as the first quality gate means implementation may already be anchored on a weak proof map.

### O3. A dedicated test-spec review gate is plausible but should be scoped carefully

Evidence:

- `AGENTS.md` allows a new skill only when it owns a distinct artifact, gate, review responsibility, recurring action, or approved operational process.
- A `test-spec-review` skill would own a distinct artifact review responsibility: proof-map adequacy before implementation.
- Adding it would change standard workflow order, validators, lifecycle review stages, skill inventory, and possibly formal review-recording rules.

Observation:

A dedicated `test-spec-review` skill is justified if the project wants independent proof-map review before implementation. It should not be added as an incidental skill file. It should be introduced through proposal/spec/workflow amendments because it changes the lifecycle contract.

## Classify

| Observation ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | Session record only | Current workflow evidence | The current contract is coherent but leaves review ownership repository-defined. |
| O2 | observation | observation | Session record only | Current stage order and prior learn evidence | Existing adjacent gates can catch related defects, but they do not fully own pre-implementation test-spec adequacy. |
| O3 | direction | pending confirmation | Proposal/spec amendment for a dedicated `test-spec-review` gate or an explicit non-skill review surface | Not yet confirmed | Adding a new skill or formal gate changes workflow policy and needs an owning artifact. |

## Route

No routing performed.

Contributor confirmation is unavailable for derivative workflow/spec/skill changes. This session records the ownership gap and candidate direction, then stops before creating or editing a `test-spec-review` skill, workflow spec, validator, or topic file.

## Best-Practice Recommendation

Short-term:

- Treat the test spec authoring skill as responsible for setting the artifact to `active`.
- Treat `implement` as responsible for refusing to start when the active test spec is missing, stale, inconsistent with the approved spec or plan, or insufficiently mapped to the milestone.
- Treat `code-review` and `verify` as later backstops for test adequacy, not as the first owner of test-spec approval.

Best long-term shape:

- Add a dedicated `test-spec-review` gate if proof-map weakness is a recurring risk or if automated implementation will rely heavily on test specs.
- Keep the artifact settlement state as `active`; use the review record to say `approved`, `changes-requested`, `blocked`, or `inconclusive`.
- Place the gate between `test-spec` and `implement`.
- Make the reviewer inspect the approved spec, approved architecture when relevant, approved plan, and the test spec's requirement-to-test mapping.
- Keep review scope to proof adequacy: requirement coverage, negative and boundary cases, milestone mapping, validation command sufficiency, manual proof boundaries, fixtures, and non-goal preservation.
- Do not make `test-spec-review` re-approve product requirements or execution sequencing; those remain owned by `spec-review`, `architecture-review`, and `plan-review`.

## No Durable Lesson Rationale

No topic entry was created. The current question identifies a workflow design direction rather than a confirmed durable lesson. The durable workflow change, if accepted, belongs in a proposal/spec/workflow/skill update.

