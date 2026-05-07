# Milestone-Aware Review Handoff Explain Change

## Summary

This change makes clean code review of a milestone aware of whether more in-scope implementation milestones remain. A clean non-final milestone review closes that milestone and routes to the next implementation milestone; only a clean final implementation milestone can route to `verify`.

Status: implementation evidence is current through M4, final verification has passed, and this explanation closes the explain-change gate. The next workflow stage is `pr`.

## Problem

The old workflow guidance treated a clean `code-review` result as a direct handoff to `verify`. That was correct for single-slice or final-milestone work, but it could skip planned implementation milestones in a milestone-based full-feature plan.

## Decision Trail

| Source | Decision |
| --- | --- |
| Proposal | Use a milestone loop and reserve `verify` for after all implementation milestones are closed. |
| Spec | Requirements `R1`-`R11b` define milestone-aware routing, one milestone state field, same-milestone review-resolution, lifecycle-closeout handling, and a static-only first slice. |
| Test spec | Tests `T1`-`T14` map the requirements, examples, edge cases, selector proof, generated-output proof, and compatibility checks. |
| Plan | M1 added static proof, M2 aligned authoritative workflow specs, M3 aligned operating docs and authored skills, and M4 refreshed generated outputs. |
| Architecture | Not required because no runtime boundary, storage, parser, API, or deployment behavior changed. |
| Verification | Final `verify` passed selected CI, broad smoke, review-artifact closeout, generated drift checks, diff hygiene, and whitespace checks. |

## Diff Rationale By Area

| Files | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `docs/proposals/2026-05-07-milestone-aware-review-handoff.md` | Accepted the milestone-aware policy direction and rejected a `code-review`-only patch. | Establishes why the workflow contract, docs, skills, and plan evidence all had to change together. | Proposal goals and recommended direction | Plan-review and lifecycle validation |
| `specs/milestone-aware-review-handoff.md` | Added the governing contract for milestone states, transitions, handoff summaries, same-milestone review-resolution, no milestone postponement, and lifecycle-closeout distinction. | Defines the behavior that fixes premature `verify` routing. | `R1`-`R11b`, `AC1`-`AC8` | `specs/milestone-aware-review-handoff.test.md`; artifact lifecycle validation |
| `specs/milestone-aware-review-handoff.test.md` | Added a traceable proof map for requirements, examples, edge cases, compatibility, selector proof, and generated-output proof. | Keeps the guidance-only slice testable without adding an executable plan-state validator. | Test cases `T1`-`T14` | Artifact lifecycle validation and selected CI |
| `specs/workflow-stage-autoprogression.md`, `specs/rigorloop-workflow.md` | Replaced the unconditional clean-review-to-verify shortcut with milestone-aware final/non-final routing and same-milestone findings handling. | Makes the authoritative workflow contracts match the approved policy. | Spec `R4`-`R10a` | `scripts/test-skill-validator.py` milestone-aware workflow-spec assertions |
| `specs/workflow-stage-autoprogression.test.md`, `specs/rigorloop-workflow.test.md` | Added corresponding examples and edge-case proof expectations. | Keeps overlap workflow test specs aligned with the amended contract. | Test spec `T2`, `T3`, `T9`, `T10` | Selected CI |
| `scripts/test-skill-validator.py` | Added static assertions for the single milestone-state vocabulary, stale shortcut removal, skill guidance, and static-only boundary. | Gives repository-owned proof for guidance text without parsing live plan state. | Test spec `T2`-`T7`, `T9`-`T11` | `python scripts/test-skill-validator.py` passed with 33 tests |
| `docs/workflows.md`, `AGENTS.md` | Added contributor-facing milestone-aware loop guidance while preserving existing lifecycle stages. | Prevents the short operating summary from continuing to imply `code-review -> verify` for every clean milestone. | Spec `R1`, `R8`, `R10` | `scripts/test-skill-validator.py`; selected CI |
| `skills/implement/SKILL.md` | Clarified `planned -> implementing -> review-requested`, targeted validation evidence, and no implement-owned `Ready for verify`. | Keeps implementation completion distinct from review closeout. | Spec `R3`-`R3b` | Skill-validator state and handoff assertions |
| `skills/code-review/SKILL.md` | Added milestone-aware review handoff and plan closeout checks. | Makes clean non-final reviews close the milestone and route to the next implementation milestone; findings move to `resolution-needed`. | Spec `R4`-`R6b`, `R8` | Skill-validator stale-shortcut and handoff assertions |
| `skills/plan/SKILL.md` | Added one `Milestone state` vocabulary, the milestone review loop, current handoff summary fields, and `lifecycle-closeout` guidance. | Gives plans the evidence surface needed for later stages to decide readiness. | Spec `R2`, `R7`-`R9b` | Skill-validator plan guidance assertions |
| `skills/workflow/SKILL.md` | Updated orchestration guidance for milestone-based plans and lifecycle-closeout work. | Keeps workflow-managed handoff decisions consistent across stages. | Spec `R1`, `R10` | Skill-validator workflow guidance assertions |
| `.codex/skills/*`, `dist/adapters/*` for `implement`, `code-review`, `plan`, and `workflow` | Regenerated derived skill mirrors and public adapter package copies. | Keeps Codex, Claude, and opencode users on the same milestone-aware guidance. | Plan M4 | `build-skills.py --check`, `build-adapters.py --check`, adapter validation |
| `docs/changes/2026-05-07-milestone-aware-review-handoff/*` | Added change metadata, review log, review resolution, plan-review record, and this explanation. | Provides durable traceability for requirements, material plan-review closeout, validation, and final rationale. | Workflow baseline change-local pack | Change metadata, review artifact, and lifecycle validation |
| `docs/plan.md`, `docs/plans/2026-05-07-milestone-aware-review-handoff.md` | Added and maintained the active plan, milestone state, handoff summary, validation notes, and lifecycle progress. | Keeps plan index and body coherent through implementation, review, and verify. | Plan policy and verify lifecycle rules | Artifact lifecycle validation and selected CI |

## Tests Added Or Changed

- `scripts/test-skill-validator.py` added milestone-aware static checks for:
  - approved `Milestone state` values and evidence-only use of `implementation-complete` and `review-clean`;
  - required `implement`, `code-review`, `plan`, and `workflow` guidance;
  - removal of stale unconditional clean-review-to-verify wording from workflow specs, docs, and skills.
- `specs/milestone-aware-review-handoff.test.md` added `T1`-`T14`, covering scope boundaries, final/non-final clean review routing, same-milestone findings, ambiguous plans, no milestone postponement, lifecycle-closeout distinction, generated output, selector paths, security/privacy, and compatibility.
- `specs/workflow-stage-autoprogression.test.md` and `specs/rigorloop-workflow.test.md` were updated so the existing workflow proof surfaces include the milestone-aware amendment.
- Existing adapter and generated-output checks prove generated mirrors match canonical skill sources.
- No executable plan-state validator, workflow simulator, or standalone `review-resolution` skill was added.

## Verification Evidence

Implementation and final verification evidence are recorded in the active plan and `change.yaml`.

Key commands:

- `python scripts/build-skills.py --check`
- `python scripts/test-adapter-distribution.py`
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/validate-adapters.py --version 0.1.1`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-07-milestone-aware-review-handoff`
- `bash scripts/ci.sh --mode explicit ...` with every active changed authored, generated, change-local, review-artifact, plan, workflow, and adapter skill path
- `bash scripts/ci.sh --mode broad-smoke`
- `git diff --check origin/main..HEAD`
- whitespace scan over active changed files from `origin/main..HEAD`

Final lifecycle `verify` passed after M4 was reviewed and closed. The active plan records selected CI, broad smoke, review-artifact closeout, generated-output drift, diff hygiene, and whitespace evidence.

Hosted CI was not observed during local verification, so this explanation does not claim hosted CI passed.

## Review Resolution Summary

The plan-review finding `PLR1-F1` was recorded in [review-log.md](review-log.md) and resolved in [review-resolution.md](review-resolution.md).

Counts:

- Findings resolved: 1
- Accepted: 1
- Unresolved findings: 0
- Closeout status: closed

The accepted finding replaced an unclassified `dist/adapters` selector path with concrete generated adapter skill file paths. M1, M2, M3, and M4 implementation reviews were clean with no material findings and did not require detailed review files.

## Alternatives Rejected

- Keeping `implementation-complete` or `review-clean` as milestone states was rejected because it creates a parallel or ambiguous state model.
- Adding executable plan-state validation was rejected for this first slice because the approved scope is guidance and static wording checks.
- Adding a standalone `review-resolution` skill was rejected; same-milestone resolution guidance is local to the existing workflow and stage skills.
- Requiring a plan-template or historical-plan migration was rejected for this slice because the approved scope is forward-compatible guidance for touched or relied-on milestone plans.

## Scope Control

This change does not alter fast-lane, bugfix, isolated review, direct `pr`, merge, release, deploy, destructive Git, runtime data flow, persistence, APIs, schemas, or hosted automation behavior.

Existing untouched historical plans are not migrated solely because they lack the new handoff summary or state vocabulary.

## Risks And Follow-Ups

- Generated outputs must remain in sync with canonical `skills/`; M4 drift checks and final verify cover the current branch.
- PR preparation confirmed branch base hygiene: the branch is restacked on `origin/main` at `f8162780ea535c412bb5d7cf69fd303c61af0656875c04491` with active scope `origin/main..HEAD`, so no stacked-branch caveat remains.
- The plan remains `Active` because PR handoff is a true downstream completion event. Merge is not being used as a deferred lifecycle-closeout trigger.

## PR Handoff Summary

- Branch-ready for the active milestone-aware change scope: yes.
- Next stage: `pr`.
- PR-stage caveat: none for branch base; the branch has been restacked for a standalone PR.
- PR body should cite the approved spec, test spec, active plan, review-resolution closeout, selected CI, broad smoke, and this explanation.
