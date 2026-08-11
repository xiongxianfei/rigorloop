# Test-Spec-Review Skill Simplification Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: r1
Reviewer: Codex independent spec-review context

- Target: `specs/test-spec-review-skill-simplification.md`
- Reviewed artifact: `specs/test-spec-review-skill-simplification.md` at commit `aec6a9dd`

Review date: 2026-08-11
Status: changes-requested
Material findings: TSRSIM-SR1
Recording status: recorded

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: TSRSIM-SR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-11-test-spec-review-skill-simplification/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-08-11-test-spec-review-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-11-test-spec-review-skill-simplification/review-resolution.md`
- Open blockers: lifecycle and handoff validity lattice is incomplete
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: revise and rereview TSRSIM-SR1 before architecture assessment

## Findings

### Finding TSRSIM-SR1

Finding ID: TSRSIM-SR1
Severity: major
Location: R3-R5, R9, State and invariants, Error and boundary behavior
Evidence: The spec correctly classifies lifecycle mode and handoff mode independently and explicitly permits `formal + isolated`, but it neither permits nor rejects `advisory + workflow-managed`. R22 says advisory approval cannot satisfy formal implementation eligibility, while `workflow-managed` is the continuation-authority value. An implementation would therefore have to guess whether that combination stops, degrades to isolated, or may route downstream.
Required outcome: Close the lifecycle-by-handoff validity matrix. Preserve `formal + isolated` and `formal + workflow-managed`, preserve `advisory + isolated`, and reject `advisory + workflow-managed` before review or downstream routing because workflow-managed continuation requires formal review identity and settlement authority.
Safe resolution path: Add a normative validity requirement and table or equivalent examples; make invalid combination failure explicit in state invariants, error behavior, static fixtures, acceptance criteria, and boundary ownership. This is eligible for bounded authoring correction because the governing implementation-eligibility contract already determines the result and no product decision remains.
needs-decision rationale: none; existing `test-spec-review` and implementation-eligibility authority closes the outcome.

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | concern | Individual predicates are clear, but one composed validity state is unclosed. |
| normative language | pass | Requirements use stable IDs and testable normative behavior. |
| completeness | block | `advisory + workflow-managed` has no permitted outcome or stop rule. |
| testability | concern | The incomplete state lattice prevents one deterministic fixture. |
| examples | pass | Eight examples are requirement-owned and behaviorally distinct. |
| compatibility | pass | Existing statuses, paths, recording, staleness, and implementation eligibility are otherwise preserved. |
| observability | pass | Ledgers, fixtures, measurements, review fields, and package evidence are explicit. |
| security/privacy | pass | No secrets, network, external action, or target runtime is required. |
| non-goals | pass | Runtime machinery, schema changes, other skills, and permanent simplicity gates remain excluded. |
| acceptance criteria | concern | Add one criterion for the closed lifecycle-by-handoff matrix and invalid combination. |

## Boundary-first assessment

- Inputs and actors: lifecycle, handoff, boundary, recording, caller, reviewer, workflow, and implement authority are identified.
- State and timing: late recording, stale approval, pre-settlement review records, retry, missing resources, architecture assessment, and rollback are governed.
- Composition paths: four base assemblies, recording overlay, assets, boundary resources, and package-chain paths have explicit owners.
- Material gap: the composition of advisory lifecycle with workflow-managed handoff lacks a governed stop outcome.

## Recommendation

Revise the spec through the bounded correction above, record the disposition and validation evidence, then run independent spec-review R2.
No architecture assessment or downstream authoring is permitted from R1.
