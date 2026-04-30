# Code Review R1

Review ID: code-review-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M1-M3 range `28f1736..3327901`
Status: changes-requested
Review date: 2026-04-30

## Scope

Reviewed the completed M1-M3 implementation for the vision skill quality refinement against the approved proposal, spec, test spec, active plan, change-local evidence, generated output, and selected validation evidence.

## Review inputs

- Diff range: `28f1736..3327901`
- Review surface: canonical `vision` skill, focused skill-validator assertions, generated Codex and public adapter skill output, spec/test-spec handoff updates, active plan, change metadata, and explain-change evidence.
- Tracked governing branch state: proposal, spec, test spec, plan, change metadata, and explain-change were tracked at `3327901`.
- Spec: `specs/vision-skill.md` R18, R19, R81-R94, and AC13-AC19.
- Test spec: `specs/vision-skill.test.md` T2, T3, T4, T8, T9, T10, and T11.
- Plan milestone: `docs/plans/2026-04-30-vision-skill-quality-refinement.md` M1-M3.
- Architecture / ADR: not required by the approved plan because the refinement changes skill guidance, tests, generated output, and lifecycle artifacts without adding a runtime boundary or architecture package change.
- Validation evidence: M1-M3 skill, generator, adapter, selector, lifecycle, metadata, README marker, explicit CI, and whitespace evidence recorded in the active plan and change metadata.

## Diff summary

The implementation adds the accepted proposal, active plan, change-local evidence, spec/test-spec updates, focused skill-validator assertions, the canonical `vision` skill refinement, and regenerated Codex and adapter skill outputs. It leaves unrelated root `README.md` and `vision.md` changes outside the reviewed range.

## Findings

### CR1-F1: Revise mode does not require the approved ask-or-confirm gate

Finding ID: CR1-F1

Evidence: `specs/vision-skill.md` R18 requires a substantive revise-mode invocation to ask or confirm whether the revision is substantive or editorial before finalizing. `specs/vision-skill.test.md` T2 requires an assertion that revise mode asks or confirms substantive versus editorial classification before finalizing. The implemented `skills/vision/SKILL.md` only says to classify the revision as substantive or editorial before finalizing, and `scripts/test-skill-validator.py` checks related traceability terms without asserting the ask-or-confirm gate.

Required outcome: Revise-mode guidance must explicitly ask or confirm substantive/editorial classification before finalizing, and the focused skill-validator assertion must prove that wording.

Safe resolution: Update `skills/vision/SKILL.md`, add focused assertion coverage in `scripts/test-skill-validator.py`, regenerate `.codex/skills/` and `dist/adapters/` through repository generators, then rerun the selected skill and generated-output checks.

## Checklist coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | concern | CR1-F1 violates R18 despite satisfying the R81-R94 structural changes. |
| Test coverage | concern | Focused assertions cover heuristics, mode-table shape, edit authorization, and traceability wording, but not the R18 ask-or-confirm wording. |
| Edge cases | concern | The scope-change-labeled-editorial edge case depends on a stronger classification gate. |
| Error handling | pass | Stop and clarification paths remain present in the mode table and README marker rules. |
| Architecture boundaries | pass | No architecture boundary or dependency changed. |
| Compatibility | pass | `vision` remains upstream and outside the normal lifecycle. |
| Security/privacy | pass | Skill privacy and external research boundaries remain present. |
| Generated output drift | pass | Recorded generator and adapter validation shows generated output synchronized after M2/M3. |
| Unrelated changes | pass | The reviewed range excludes the unrelated uncommitted root `README.md` and untracked `vision.md`. |
| Validation evidence | concern | Selected CI passed, but it did not catch CR1-F1. |

## Recommended next stage

Enter review-resolution for CR1-F1, then rerun `code-review`.
