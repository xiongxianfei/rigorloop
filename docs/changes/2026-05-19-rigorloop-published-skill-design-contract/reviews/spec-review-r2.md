# Spec Review R2: RigorLoop Published Skill Design Contract

Review ID: spec-review-r2
Stage: spec-review
Round: 2
Reviewer: external review result provided in chat
Target: specs/skill-contract.md
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: SKC-PR1, SKC-PR2, SKC-PR3, SKC-PR4
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/spec-review-r2.md
- Review log: docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-log.md
- Review resolution: docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-resolution.md#spec-review-r2
- Open blockers: first-slice scope conflict, routing/body duplication risk, routing-test oracle precision, behavior-preservation proof
- Immediate next stage: spec revision
- No automatic downstream handoff: this review does not start spec, plan, implementation, or code-review work.

## Overall Verdict

Good direction, changes requested.

The amendment correctly keeps `specs/skill-contract.md` as the normative source, distinguishes skill-contract behavior from workflow-routing behavior, separates repository-root internals from packaged skill-local resources, and adds a bounded routing-test rule. The remaining issue is internal consistency: older baseline requirements and the new published-skill design amendment both used the phrase "first implementation slice" for different scopes.

## Material Findings

### SKC-PR1 - `first implementation slice` refers to two incompatible scopes

Finding ID: SKC-PR1
Severity: major
Location: Examples, requirements, state and invariants, and R36 in `specs/skill-contract.md`
Evidence: The historical baseline says the first implementation slice normalizes `workflow`, `plan`, `implement`, `code-review`, `verify`, `pr`, and `learn`, while the new amendment limits the new pilot to `proposal`, `proposal-review`, validator changes, and generated adapter validation.
Required outcome: Disambiguate the historical baseline slice from the new published-skill design pilot.
Safe resolution path: Add explicit slice terminology and update examples, requirements, state and invariants, and acceptance criteria to use the distinct labels.

### SKC-PR2 - Mandatory body sections risk duplicating routing logic

Finding ID: SKC-PR2
Severity: major
Location: R3, R29, and R31 in `specs/skill-contract.md`
Evidence: The spec requires every normalized skill to include `When to use` and `When not to use` body sections, while also making frontmatter `description` the portable routing source.
Required outcome: Clarify what body `When to use` and `When not to use` sections may contain without replacing or duplicating full routing logic.
Safe resolution path: Add requirements stating body routing sections must not replace `description`, may summarize invocation scope, local stop conditions, or competing skills after load, and validators should treat `description` as independently sufficient.

### SKC-PR3 - Routing coverage validation is under-specified

Finding ID: SKC-PR3
Severity: major
Location: R29, R35, observability, and performance expectations in `specs/skill-contract.md`
Evidence: The spec says validators must evaluate routing coverage against `description`, but it does not define the deterministic data to evaluate.
Required outcome: Define deterministic routing-coverage evidence for the pilot.
Safe resolution path: Require a routing coverage table for each changed pilot skill, covering positive triggers, near misses, competing skills, and should-not-trigger prompt classes; allow static table and bounded phrase checks while prohibiting broad semantic scoring without an approved harness.

### SKC-PR4 - Behavior-preservation proof is not explicit enough for skill rewrites

Finding ID: SKC-PR4
Severity: major
Location: R3b, acceptance criteria, and testing or validation expectations in `specs/skill-contract.md`
Evidence: The spec requires preserving behavior-significant guidance but does not require a concrete migration note or behavior-parity proof for each touched pilot skill.
Required outcome: Require preservation notes and behavior-parity evidence for each changed pilot skill.
Safe resolution path: Add requirements for behavior-preservation notes and behavior-parity evidence showing material review status, finding format, recording obligations, stop conditions, validation obligations, and claim boundaries were not weakened.

## Readiness

Not ready for approval as written. Resolve `SKC-PR1` through `SKC-PR4`, then rerun spec review.
