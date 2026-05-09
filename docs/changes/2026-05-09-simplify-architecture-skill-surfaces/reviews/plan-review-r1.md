# Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review
Target: docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md
Status: changes-requested

## Review inputs

- Plan: `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`
- Plan index: `docs/plan.md`
- Accepted proposal: `docs/proposals/2026-05-09-simplify-architecture-skill-surfaces.md`
- Approved spec: `specs/architecture-package-method.md`
- Test spec: `specs/architecture-package-method.test.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260509-architecture-skill-surface-simplification.md`
- Architecture-review record: `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/architecture-review-r1.md`

## Verdict

changes-requested

## Findings

### PR-F1 - Implementation milestones bypass per-milestone code-review

Finding ID: PR-F1
Severity: material
Dimension: Sequencing

Evidence: `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md` defines M1 through M4 as implementation milestones with `Milestone state: planned` and milestone closeout checklists at lines 88-276. Those closeout checklists require targeted validation, progress updates, validation notes, and milestone commits, but none require handing the milestone to `code-review` before closure. The plan instead defers code-review until M5 at lines 278-304, after "M1 through M4 are closed" and "the completed implementation" exists.

Problem: Repository workflow guidance for milestone-based plans expects each in-scope implementation milestone to follow the implementation and code-review loop before the next implementation milestone closes or final closeout begins. Deferring code-review until after all implementation milestones collapses four reviewable slices into one late review and weakens the plan's reviewability claim.

Required outcome: The plan must make per-milestone review sequencing explicit for M1 through M4, or intentionally reclassify any non-implementation milestone so final closeout readiness cannot depend on unreviewed implementation work.

Safe resolution: Add code-review handoff and review closeout requirements to each in-scope implementation milestone, for example:

```text
- Implementation handoff:
  - targeted validation passed
  - hand off to code-review for this milestone
- Review closeout:
  - code-review completed
  - material findings resolved or explicitly dispositioned
  - milestone state updated before starting the next implementation milestone
```

Then update the Current Handoff Summary, Dependencies, and M5 so M5 performs final lifecycle closeout only after M1-M4 have each passed their milestone review loop.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Self-contained context | pass | The plan includes source artifacts, no-map rationale, current skill/source orientation, generated-output boundaries, and downstream gates. |
| Source alignment | pass | Milestones trace to the accepted proposal, approved spec requirements, architecture-review note, ADR, and adapter validation requirement. |
| Milestone size | concern | M1-M4 are reviewable slices, but the review loop is not attached to each slice. See PR-F1. |
| Sequencing | block | M1-M4 close before code-review, then M5 reviews the completed implementation. See PR-F1. |
| Scope discipline | pass | Non-goals protect C4/arc42/ADR retention, historical deltas, generated-output boundaries, and governance churn. |
| Validation quality | pass | Commands are explicit and include lifecycle, skill, generated-output, adapter drift, adapter validation, selected CI, and diff checks. |
| TDD readiness | pass | The plan identifies test-spec and static test updates before canonical skill implementation. |
| Risk coverage | pass | Risks cover stale wording, public skill leakage, generated drift, weakened review quality, and plan/index lifecycle drift. |
| Architecture alignment | pass | The plan follows the approved simplification and keeps the 2026-04-28 C4 plus arc42 plus ADR method intact. |
| Operational readiness | pass | Generated outputs, adapter validation, selected CI, final verify, and PR handoff are covered. |
| Plan maintainability | concern | Progress and closeout surfaces exist, but they need per-milestone review status before implementation starts. |

## Missing milestones or dependencies

- Missing per-implementation-milestone code-review dependency for M1, M2, M3, and M4.
- M5 should remain lifecycle closeout only after each implementation milestone has completed its own code-review loop.

## Exact suggested edits

- Add `code-review M1` through `code-review M4` handoff and closeout requirements to the corresponding milestones.
- Update `Current Handoff Summary` so `Last reviewed milestone` and `Review status` will be maintained per milestone.
- Update M5 dependencies to require M1-M4 review closeout, not only M1-M4 closure.
- Keep immediate next stage as `test-spec` only after plan-review R2 approves the revised plan.

## Readiness

- Immediate next stage: plan revision, then plan-review rerun.
- `test-spec` readiness: blocked until PR-F1 is resolved and plan-review approves the revised plan.
- Implementation readiness: blocked.
- No automatic downstream handoff is performed because this was a direct `plan-review` request.
