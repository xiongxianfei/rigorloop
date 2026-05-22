# Code Review M4 R1 - Plan Archive Guidance Alignment

Review ID: code-review-m4-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M4. Contributor guidance and skill alignment
Reviewed artifact: commit `2d7dd3c`
Review date: 2026-05-22
Status: changes-requested
Recording status: recorded

## Review inputs

- Diff/review surface: `2d7dd3c M4: document plan archive maintenance`
- Plan: `docs/plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md`
- Spec: `specs/plan-index-lifecycle-ownership.md`
- Test spec: `specs/plan-index-lifecycle-ownership.test.md`
- Touched guidance: `docs/workflows.md`, `AGENTS.md`, `docs/examples/plans/example-plan.md`, `skills/plan/SKILL.md`
- Validation evidence recorded in the plan and change metadata

## Diff summary

M4 adds bounded-plan-index and archive guidance to the workflow guide, root agent guidance, the example plan, and the canonical `plan` skill. It also records M4 validation evidence and moves the active plan/index to `review-requested` for M4.

## Findings

### BPIX-M4-CR1 - Plan guidance does not cover all R8a ownership bullets

Finding ID: BPIX-M4-CR1
Severity: major
Location: `skills/plan/SKILL.md`
Evidence: `R8a` requires the repository's workflow summary and plan guidance to describe, at minimum, that `implement` owns ongoing plan-body updates, final lifecycle closeout owns state transitions in the plan index surfaces and plan body, and `verify` challenges stale lifecycle state before `branch-ready`. The M4 diff adds archive, lifecycle marker, and active supersession wording to `skills/plan/SKILL.md`, but the touched `Plan authoring rules` still do not explicitly describe those three ownership points. `docs/workflows.md` covers them, but the requirement names both workflow summary and plan guidance.
Required outcome: Plan guidance must explicitly include the missing R8a ownership points or record a spec-backed rationale for why another plan-guidance surface satisfies `R8a`.
Safe resolution path: Add concise wording to `skills/plan/SKILL.md` near the existing plan authoring rules that says `implement` owns ongoing plan-body progress/decision/validation updates, final lifecycle closeout owns lifecycle state transitions across the plan index surfaces and plan body, and `verify` challenges stale lifecycle state before `branch-ready`. Rerun `python scripts/validate-skills.py skills/plan/SKILL.md`, `python scripts/validate-skills.py`, `python scripts/build-skills.py --check`, adapter archive validation if required by the plan, artifact lifecycle checks for touched guidance/plan state, change metadata validation, and `git diff --check --`.

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | block | `R8a` requires both workflow summary and plan guidance to describe lifecycle ownership; `skills/plan/SKILL.md` misses three ownership bullets. |
| Test coverage | concern | T14 requires review of touched guidance for plan/index/archive ownership; the guidance audit checked marker presence but did not prove all R8a ownership bullets in plan guidance. |
| Edge cases | pass | Guidance does cover archive placement, explicit lifecycle markers, and active supersession marker structure. |
| Error handling | pass | No runtime error handling is touched. |
| Architecture boundaries | pass | No architecture or ADR boundary is touched. |
| Compatibility | concern | Contributor-facing plan guidance remains partially incomplete for the newly enforced archive/lifecycle ownership contract. |
| Security/privacy | pass | The diff adds tracked Markdown guidance and no secrets, credentials, private paths, or unsafe logging. |
| Derived artifact currency | pass | Canonical skill validation, generated skill check, and temporary adapter archive validation are recorded. |
| Unrelated changes | pass | The diff is scoped to guidance surfaces, active plan/index state, and change-local evidence. |
| Validation evidence | concern | Commands passed, but the manual guidance audit was too narrow to catch the missing R8a ownership bullets. |

## No-finding rationale

Not applicable; one required-change finding is recorded.

## Residual risks

After the finding is fixed, code-review should re-check `R8a` directly rather than relying only on keyword presence.

## Handoff

Route to review-resolution for `BPIX-M4-CR1`. Keep M4 on the same milestone with state `resolution-needed`. This review does not claim branch readiness, PR readiness, final verification, or CI status.
