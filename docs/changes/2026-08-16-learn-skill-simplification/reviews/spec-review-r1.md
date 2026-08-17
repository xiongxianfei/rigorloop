# Spec Review R1: Learn Skill Simplification

Review ID: spec-review-r1
Stage: spec-review
Round: r1
Reviewer: Codex independent spec-review context
Target: `specs/learn-skill-simplification.md`

Reviewed artifact: commit `6c7b276e`
Review date: 2026-08-17
Recording status: recorded
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: LRNSIM-SR1, LRNSIM-SR2, LRNSIM-SR3
- Open blockers: exact cross-spec precedence, complete loaded-profile acceptance, and schedulable-route completion ownership
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: specification must close LRNSIM-SR1 through LRNSIM-SR3 before architecture assessment or planning

## Recording

- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-16-learn-skill-simplification/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-08-16-learn-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-16-learn-skill-simplification/review-resolution.md`

## Governed settlement

- Settlement mode: governed-spec-entry
- Settlement status: revision-required
- Governed change identity: `2026-08-16-learn-skill-simplification`

## Boundary review

- Boundary applicability: `boundary-first-v1` applicable; structure is complete, but authority and completion outcomes need the revisions below
- Boundary resources: `boundary-first-method-v1.md`, `boundary-first-feature-authoring-v1.md`
- Boundary blocker: BND-AUTH-001 and BND-COMPAT-001 do not yet resolve exact legacy-clause precedence; BND-INPUT-001 does not yet own the schedulable completion discriminator

## Automated review

- Automation mode: workflow-managed-automated
- Automation evidence: `review-invocation-spec-review-r1.yaml`
- Automation result: bounded spec correction permitted; no downstream promotion until approving rereview

## Findings

## Finding LRNSIM-SR1

Finding ID: LRNSIM-SR1
Severity: major
Location: `Goal and context`, R20, R23, R32, R35, and `Compatibility and migration`; `specs/learn-artifact-model.md` R21-R24, R33, inputs/outputs, and Example E3
Evidence: The new spec says destination owners retain mutation authority, while the approved older contract still normatively says the learn Route phase updates authoritative artifacts and lists those updates as learn outputs. A general statement that the focused amendment is “more specific” does not give each conflicting legacy clause one exact disposition, so two approved requirements can instruct opposite writers.
Required outcome: Add an exact cross-spec disposition table for every conflicting legacy requirement, example, output, invariant, and acceptance surface, preserving the obligation to produce authoritative updates while transferring mutation to the destination owner and limiting learn to route and backlink writes.
Safe resolution path: Add a closed amendment section that names `learn-artifact-model.md` R21-R24 and R33 plus affected non-requirement surfaces, states their prospective replacement or reinterpretation, and requires companion contract/test alignment in the implementation slice.
needs-decision rationale: none

## Finding LRNSIM-SR2

Finding ID: LRNSIM-SR2
Severity: major
Location: R42, Performance expectations, and AC10
Evidence: The accepted proposal requires both real procedural profiles, `LR0-route-result` and `LR1-learn-session`, to decrease from the 1,712-word and 12,375-byte flat baseline. R42 and AC10 require strict reduction only for LR1 and merely report LR0, so implementation could enlarge the route-result common path and still satisfy the specification.
Required outcome: Require strict word and byte reduction for both LR0 and LR1 against the recorded baseline while continuing to report each resource and total package separately.
Safe resolution path: Amend R42, Performance expectations, and AC10 with the same deterministic assembly and baseline for both profiles.
needs-decision rationale: none

## Finding LRNSIM-SR3

Finding ID: LRNSIM-SR3
Severity: major
Location: R26, R29, R31, R34, and BND-INPUT-001
Evidence: R34 permits a durable scheduled follow-up only when the route “explicitly permits that completion kind,” but R26 does not require a completion-kind field or define which classifications permit it. Result recording therefore cannot deterministically distinguish an acceptable scheduled follow-up from one that must remain pending.
Required outcome: Give every route one closed expected completion kind, or define an exhaustive classification-to-completion mapping, and require `record-learn-route-result` to validate the supplied owner-result kind against it.
Safe resolution path: Add a route field such as `required completion kind: authoritative-artifact | durable-scheduled-follow-up`, define its owner and immutability, update result-recording validation, and add the field to input and boundary coverage.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | concern |
| normative language | pass |
| completeness | block |
| testability | block |
| examples | pass |
| compatibility | block |
| observability | pass |
| security/privacy | pass |
| non-goals | pass |
| acceptance criteria | block |

## Boundary assessment

All eight dimensions are present and structurally valid, and the selected interactions are proportionate. The exact authority transition from the older learn contract is not closed, and the scheduled-follow-up discriminator is missing from the route input model. Those are normative boundary gaps rather than proof-only omissions.

## Required wording direction

The revision should add an exact legacy-disposition table, make both loaded profiles strictly smaller, and record one immutable completion-kind expectation on each route. It should not add a route registry, workflow coordinator, polling operation, transaction schema, template, or target-runtime acceptance path.

## Claim limitations

This review settles only the current specification as `revision-required`. It does not claim architecture completion, plan readiness, test-spec readiness, implementation readiness, verification, branch readiness, or PR readiness.
