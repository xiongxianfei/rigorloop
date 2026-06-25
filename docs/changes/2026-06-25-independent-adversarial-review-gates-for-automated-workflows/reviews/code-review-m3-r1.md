# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M3 code-review pilot and review-family guidance implementation diff at commit `a249c968`
Reviewed artifact: M3 implementation diff at commit `a249c968`
Review date: 2026-06-25
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/code-review-m3-r1.md`, `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md`, `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md`, `docs/plans/2026-06-25-independent-adversarial-review-gates.md`, `docs/plan.md`, `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml`
- Open blockers: CR4-F1, CR4-F2
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CR4-F1, CR4-F2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/code-review-m3-r1.md
- Review log: docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md
- Review resolution: docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md
- Reviewed milestone: M3. Code-review pilot and review-family guidance
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3 resolution, M4, M5
- Required review-resolution: yes
- Finding IDs: CR4-F1, CR4-F2
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: `6863b89b..a249c968`, especially `skills/code-review/SKILL.md`, `skills/implement/SKILL.md`, `skills/workflow/SKILL.md`, `skills/spec-review/SKILL.md`, `skills/plan-review/SKILL.md`, `scripts/test-skill-validator.py`, active plan state, plan index, and change metadata updates.
- Tracked governing branch state: branch `proposal/independent-adversarial-review-gates`; M3 implementation commit is tracked at `a249c968`. One unrelated untracked learn-session file exists and was excluded from the implementation review surface.
- Governing artifacts: `specs/review-independence-and-criticality.md` R6, R8, R9, R18-R20; `specs/review-independence-and-criticality.test.md` T5, T6, T14, T15, T18; `docs/plans/2026-06-25-independent-adversarial-review-gates.md` M3.
- Validation evidence reviewed: M3 recorded focused `python scripts/test-skill-validator.py -k review_independence_m3`, full `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/test-build-skills.py`, `python scripts/build-skills.py --check`, adapter archive build and validation for `v0.1.5`, change metadata validation, explicit-path lifecycle validation, review artifact structure validation, `git diff --check`, and whitespace scan.

## Diff summary

M3 adds canonical skill guidance for the automated `code-review` independent adversarial review pilot, workflow and implement handoff routing, Phase 1 manifest-only guidance for automated `spec-review` and `plan-review`, skill-validator assertions for those phrases, and lifecycle state updates handing M3 to code-review.

## Findings

### CR4-F1 - `failed-remediation` is named but not operationally defined in code-review guidance

Finding ID: CR4-F1
Severity: major
Location: `skills/code-review/SKILL.md:349`; `scripts/test-skill-validator.py:4997`-`4999`
Evidence: `specs/review-independence-and-criticality.md:231`-`233` requires prior finding reconciliation to include `failed-remediation`, and specifically requires `failed-remediation` when a prior finding was claimed or expected to be fixed but is independently rediscovered during the blind-first pass. The M3 skill text only says to reconcile prior findings as ``resolved`, `still-present`, `failed-remediation`, `reopened`, `superseded`, or `new-finding``. It does not state the required condition for `failed-remediation`. The M3 skill-validator assertion likewise checks only that the category list appears, not that the required rediscovery condition is present.
Required outcome: The canonical `code-review` guidance must tell reviewers when `failed-remediation` is required, and the M3 skill-validator coverage must fail if that condition is removed.
Safe resolution path: Add a sentence to `skills/code-review/SKILL.md` in the prior-finding reconciliation paragraph: "`failed-remediation` is required when a prior finding was claimed or expected to be fixed but is independently rediscovered during the blind-first pass." Add the same required phrase to `test_review_independence_m3_code_review_pilot_guidance`. Rerun `python scripts/test-skill-validator.py -k review_independence_m3`, full `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, and the M3 generated skill/adapter proof commands.
needs-decision rationale: none
auto_fix_class: declared-safe

### CR4-F2 - Implement handoff guidance still permits `auto-fix eligibility` in the initial packet

Finding ID: CR4-F2
Severity: major
Location: `skills/implement/SKILL.md:247`; `scripts/test-skill-validator.py:5022`-`5024`
Evidence: `specs/review-independence-and-criticality.md:183`-`193` lists prohibited initial context before review hypotheses are formed, including `auto-fix eligibility`. The new `code-review` guidance correctly excludes `auto-fix eligibility` at `skills/code-review/SKILL.md:343`, but the `implement` handoff guidance excludes only `auto-fix budget` and omits `auto-fix eligibility`. Because `implement` owns the workflow-managed handoff to automated `code-review`, this omission leaves the authoring side free to leak the fixability signal that R9d is trying to keep out of review discovery. The M3 test assertion mirrors the omission by requiring `auto-fix budget` but not `auto-fix eligibility`.
Required outcome: The `implement` skill's initial packet exclusion list must include `auto-fix eligibility`, and the skill-validator assertion must require that phrase.
Safe resolution path: Add `auto-fix eligibility` to the forbidden initial packet list in `skills/implement/SKILL.md`, update `test_review_independence_m3_workflow_and_implement_route_automated_gate` to assert it, and rerun the M3 skill validation and generated adapter proof commands.
needs-decision rationale: none
auto_fix_class: declared-safe

## Checklist coverage

1. Spec alignment: block. CR4-F1 under-specifies R8d in the reviewer-facing skill; CR4-F2 omits an R5 prohibited initial-context item from the implement handoff skill.
2. Test coverage: block. The new M3 assertions prove category presence and most forbidden packet items, but they do not prove the `failed-remediation` condition or `auto-fix eligibility` exclusion.
3. Edge cases: block. The named rereview edge case where a claimed fix is rediscovered lacks operational guidance, and the auto-fix eligibility anchoring case is not blocked at the implement handoff surface.
4. Error handling: concern. This is guidance-level behavior rather than exception handling, but both omissions create fail-open review-process behavior.
5. Architecture boundaries: pass. The implementation stays in canonical skill guidance, skill-validator tests, and required lifecycle metadata; no service, persistence, or external dependency was added.
6. Compatibility: pass. Direct isolated `spec-review`, `plan-review`, and profile-off code-review behavior remains explicitly preserved.
7. Security/privacy: pass. The diff does not introduce secret handling, credential exposure, network calls, or private reasoning recording.
8. Derived artifact currency: pass. M3 ran local skill validation, generated local skill checks, and public adapter archive build/validation for `v0.1.5`.
9. Unrelated changes: pass. The reviewed commit contains expected M3 skill, test, plan, index, and change metadata updates. The unrelated untracked learn file is excluded.
10. Validation evidence: concern. The recorded commands are relevant and passed, but the targeted M3 tests are too narrow to catch CR4-F1 and CR4-F2.

## No-finding rationale

Not applicable. Material findings were found.

## Residual risks

M4-M5 remain planned future milestones. This review covers the M3 guidance slice, not calibration fixture implementation, final generated guidance alignment, behavior-preservation evidence, explain-change, verify, or PR readiness.

## Milestone handoff state

- Reviewed milestone: M3. Code-review pilot and review-family guidance
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining implementation milestones: M3 resolution, M4, M5
- Next stage: review-resolution M3
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation-milestones-open, review-resolution-open, explain-change-pending, verify-pending, pr-handoff-pending — M3 has material code-review findings requiring review-resolution; M4-M5 remain incomplete.
