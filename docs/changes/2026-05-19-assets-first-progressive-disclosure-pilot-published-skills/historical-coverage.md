# Historical Coverage: Plan Asset Pilot

## Scope

This record covers M3 historical coverage evidence for the assets-first `plan` pilot.

Historical plans predate the current published-skill design contract, so they are coverage evidence rather than strict structural parity references.

## Historical Corpus

| Plan | Era | Coverage purpose |
| --- | --- | --- |
| `docs/plans/2026-04-19-rigorloop-first-release-implementation.md` | pre-contract | Large multi-milestone first-release implementation with schema, skill, validator, CI, and traceability work. |
| `docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md` | pre-contract | Selector, CI wrapper, workflow guidance, generated-output, and final validation sequencing. |
| `docs/plans/2026-05-04-formal-review-recording.md` | pre-contract | Formal review recording, validator coverage, review skill guidance, generated output, and lifecycle closeout. |

## Coverage Parity

| Historical concern | Covered by current asset-based plan shape |
| --- | --- |
| Multi-milestone sequencing | `assets/plan-skeleton.md` Milestones section plus `assets/milestone.md` repeated once per milestone. |
| Cross-surface implementation context | Context and orientation, Source artifacts, Requirements covered, Dependencies, and Risks and recovery sections. |
| Validation-heavy changes | Validation plan, milestone Validation commands, and Validation notes sections. |
| Review and lifecycle handoff | Current Handoff Summary plus milestone states and `skills/plan/SKILL.md` handoff rules. |
| Decision traceability | Decision log table and reusable decision-log row asset. |
| Recovery and rollback | Risks and recovery section plus milestone Rollback/recovery field. |
| Completion evidence | Outcome and retrospective, Readiness, and validation notes. |

## Historical Gaps

| Gap | Treatment |
| --- | --- |
| Older plans do not consistently include Current Handoff Summary. | Expected historical drift; current plan contract keeps Current Handoff Summary required for live state. |
| Older plans use varied heading capitalization, such as `Purpose / Big Picture`. | Expected historical drift; current skeleton standardizes heading shape. |
| Older plans sometimes include bespoke handoff sections such as Immediate Test-Spec Handoff. | Covered by Source artifacts, Dependencies, Milestones, and Current Handoff Summary in the current structure. |

## Result

The asset-based `plan` skill can cover the same planning concerns represented by the historical corpus without requiring old plans to match the current section structure.
