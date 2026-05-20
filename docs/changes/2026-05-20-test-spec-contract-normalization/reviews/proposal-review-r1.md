# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Contributor proposal-review
Target: docs/proposals/2026-05-20-test-spec-contract-normalization.md
Status: changes-requested

## Review inputs

- Proposal: `docs/proposals/2026-05-20-test-spec-contract-normalization.md`
- Governance: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`
- Parent proposal: `docs/proposals/2026-05-19-rigorloop-published-skill-design-contract.md`
- Canonical skills: `skills/spec/SKILL.md`, `skills/spec-review/SKILL.md`, `skills/test-spec/SKILL.md`

## Findings

### TSCN-PR1 - Baseline audit evidence is not durable enough

Finding ID: TSCN-PR1
Severity: major
Evidence: The proposal says a prior workflow audit classified `test-spec` as behind the published-skill design contract and `spec` and `spec-review` as compliant, but it does not identify a durable audit table, artifact path, or exact evidence location.
Required outcome: Add a durable baseline compliance audit to the proposal or reference the artifact that already records it.
Safe resolution: Add a baseline compliance audit covering `spec`, `spec-review`, and `test-spec` against front matter, Workflow role, output skeleton, and stop-condition surfacing.

### TSCN-PR2 - Preservation proof is too general for stop-condition promotion and skeleton creation

Finding ID: TSCN-PR2
Severity: major
Evidence: The proposal says stop-condition preservation will be checked by diffing the surfaced conditions against the Rules they came from, and output-skeleton fidelity will be checked against existing required sections and coverage-map rules, but it does not require a concrete source-to-destination matrix.
Required outcome: Require a content-preservation matrix before implementation.
Safe resolution: Add a content-preservation proof section and acceptance criteria covering promoted stop conditions, required sections, test-case format, and coverage-map obligations.

### TSCN-PR3 - Amendment sequencing is ambiguous

Finding ID: TSCN-PR3
Severity: major
Evidence: The proposal says `specs/skill-contract.md` is amended only if a contract gap surfaces, validator adjustment is included only if needed, and generated adapter outputs are regenerated only if required. The Next artifacts list nevertheless includes conditional spec amendment and spec-review without a gate for deciding the route.
Required outcome: Add a sequencing rule that blocks implementation until the proof route is named.
Safe resolution: Add an amendment sequencing section requiring the plan to name one approved proof route before implementation begins.

### TSCN-PR4 - Generated adapter validation is too conditional

Finding ID: TSCN-PR4
Severity: major
Evidence: The proposal says adapter outputs are regenerated from canonical `skills/` only if required by the implementation workflow, and no generated archives are retroactively rewritten.
Required outcome: Require generated adapter output validation for current generated outputs, or require an explicit deferral rationale.
Safe resolution: Add a generated adapter output boundary that requires current generated output to be rebuilt or validated from canonical skills when `skills/test-spec/SKILL.md` changes, unless the plan records an explicit deferral.

## Checklist coverage

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | The compliance gap is concrete. |
| User value | pass | A self-contained `test-spec` skill improves adopter inspection and consistency. |
| Option diversity | pass | Options compare do-nothing, bundled readability, and normalization-only. |
| Decision rationale | pass | Option 3 follows from compliance-before-readability priority. |
| Scope control | revise | Amendment and adapter-validation gates need tightening. |
| Architecture awareness | revise | Canonical skill changes and generated adapter output need a clearer boundary. |
| Testability | revise | Preservation proof needs a matrix rather than generic diff discipline. |
| Risk honesty | pass | Stop-condition, skeleton, validator, and scope-creep risks are named. |
| Rollout realism | revise | Implementation gate must name the proof route before work begins. |
| Readiness for plan | changes-requested | Revise proof and sequencing controls first. |

## Recommended next stage

Revise the proposal to resolve TSCN-PR1, TSCN-PR2, TSCN-PR3, and TSCN-PR4, then rerun proposal-review before downstream plan reliance.
