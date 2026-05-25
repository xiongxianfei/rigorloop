# Learn Session: Plan Before Test Spec Public Framing

## Frame

- Trigger: explicit maintainer invocation: "`$learn` What's the best practices? It always confuses reader about generate plan after spec and before test spec."
- Trigger type: maintainer request and contributor observation.
- Date: 2026-05-25
- Scope: public and contributor-facing descriptions of the RigorLoop traceability chain, especially `README.md`, `VISION.md`, and change-local proof for `2026-05-25-adopter-facing-vision-and-readme-principle-rewrite`.
- Evidence in scope:
  - `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
  - `README.md`
  - `VISION.md`
  - `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/vision-readme-sync-proof.md`
  - `docs/plans/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md`
  - prior session `docs/learn/sessions/2026-05-08-spec-review-rounds-and-readiness.md`
- Explicit exclusions:
  - no workflow stage-order change;
  - no skill behavior change;
  - no new validator or spec amendment;
  - no claim that this learn session changes the authoritative workflow contract.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-08-spec-review-rounds-and-readiness.md` recorded that `spec-review` may report eventual `test-spec` readiness while the immediate next repository stage remains `architecture` or `plan`.
- Session record path: `docs/learn/sessions/2026-05-25-plan-before-test-spec-public-framing.md`

## Observe

### O1. Public traceability copy can easily put test spec before plan

Evidence:

- The active README/VISION rewrite initially described the chain as proposal to spec, tests, plan, implementation, review, verification, and PR handoff.
- The maintainer caught the issue and stated that RigorLoop generates spec, then plan, then test spec.
- `docs/workflows.md` and `specs/rigorloop-workflow.md` name the standard order as `proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review -> plan -> plan-review -> test-spec -> implement`.
- `docs/learn/sessions/2026-05-08-spec-review-rounds-and-readiness.md` already identified a related confusion: eventual `test-spec` readiness is not the same thing as the immediate next stage after spec review.

Observation:

The phrase "tests trace to the contract" is true, but public chain copy should
not collapse proof design into a generic "tests" stage before planning. In
RigorLoop, planning comes before test-spec so the proof map can account for the
approved execution sequence, milestones, dependencies, rollback boundaries, and
validation surfaces.

## Classify

| Observation ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | durable-lesson | durable-lesson | topic update: `docs/learn/topics/workflow-stage-order.md` | maintainer request and repeated evidence from 2026-05-08 plus current README/VISION correction | The confusion recurred across prior workflow-readiness discussion and the current public framing rewrite, and the maintainer explicitly asked for best practices. |

## Route

- Added topic guidance: `docs/learn/topics/workflow-stage-order.md`.
- No authoritative workflow artifact was changed because the canonical order is already stated in `docs/workflows.md` and `specs/rigorloop-workflow.md`.
- No proposal, ADR, spec, skill, or validator follow-up is required from this session.

## Best Practice

When describing RigorLoop's traceability chain for readers, use the canonical
order and name why plan comes before test spec:

```text
proposal -> proposal-review -> spec -> spec-review -> plan -> plan-review ->
test-spec -> implement -> code-review -> explain-change -> verify -> PR
```

Include architecture stages only when the context needs the full conditional
chain:

```text
proposal -> proposal-review -> spec -> spec-review -> architecture ->
architecture-review -> plan -> plan-review -> test-spec -> implement ->
code-review -> review-resolution when triggered -> ci-maintenance when triggered
-> explain-change -> verify -> PR
```

Reader-facing explanation:

```text
The plan comes before the test spec because the proof map depends on the chosen
implementation sequence, milestones, dependencies, and validation surfaces.
Spec-review may say the spec is eventually test-spec ready, but planning still
comes first when it is required.
```

## Validation

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/learn/sessions/2026-05-25-plan-before-test-spec-public-framing.md --path docs/learn/topics/workflow-stage-order.md` passed; the lifecycle validator reported 0 lifecycle-managed artifact files for these learn surfaces.
- `git diff --check --` passed.
- `rg -n "proposal -> spec -> tests -> plan|spec, tests, plan|test spec.*plan|Test spec.*Plan|tests, plan" README.md VISION.md docs/learn/sessions/2026-05-25-plan-before-test-spec-public-framing.md docs/learn/topics/workflow-stage-order.md docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/vision-readme-sync-proof.md` found only intentional historical/anti-pattern mentions in this session and topic file.
