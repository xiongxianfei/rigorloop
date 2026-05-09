# Explain Change: Single Workflow Lane, Explain-Change Before Verify, and Public Skill Surface Boundary

## Summary

This change updates RigorLoop's workflow governance so the public workflow has one recommended standard path, focused manual skill invocations are isolated by default, `explain-change` runs before final `verify`, and shipped skill text stays project-portable.

The implementation changes governing workflow specs, test specs, contributor-facing guidance, canonical skills, generated Codex and adapter outputs, static wording checks, architecture documentation, active plan state, review records, change metadata, and learn session records. It does not change runtime services, package formats, release metadata format, repository deployment boundaries, or hosted workflow files.

This artifact is durable rationale before final `verify`. It summarizes validation already available, but it does not claim final `verify`, branch-ready status, PR-ready status, or hosted CI-final status.

## Problem

The accepted proposal identified three coupled workflow problems:

- public guidance still described fast-lane or lane-like routing, which made focused use look like a separate completed workflow;
- final `verify` was documented before `explain-change` even though final verification checks the complete change-local pack, including durable rationale;
- public skill text exposed RigorLoop repository internals such as internal spec paths, generated mirror paths, adapter paths, selector commands, and maintainer-only mechanics.

The result was confusing stage ownership: small or focused work could be read as bypassing the standard workflow, `verify` could block on an artifact that had not been created yet, and published skills were less portable for projects that do not share this repository layout.

## Decision Trail

| Decision source | Decision | Resulting implementation |
| --- | --- | --- |
| Proposal | Use one recommended standard workflow and isolated manual skill invocation instead of lane or trivial-work categories. | Removed public fast-lane and route-size vocabulary from specs, docs, skills, generated outputs, and static checks. |
| Proposal | Run `ci-maintenance` when triggered, then `explain-change`, then `verify`, then `pr`. | Updated workflow contract, autoprogression, milestone-aware closeout guidance, public summaries, stage skills, generated outputs, and plan handoff state. |
| Proposal | Published skills must be project-portable. | Added allow/block policy and static checks for public skill text while keeping repository-maintenance detail in internal specs, plans, tests, scripts, and maintainer docs. |
| Spec reviews SR1-SR9 | Remove proportional-evidence/tiny-work wording, replace stale direct-verify closeout wording, and strengthen static retired-term checks. | Updated `specs/rigorloop-workflow.md`, `specs/workflow-stage-autoprogression.md`, `specs/skill-contract.md`, matching test specs, and `scripts/test-skill-validator.py`. |
| Architecture review | Update the canonical architecture package directly rather than maintain a separate delta/merge-back cycle. | Updated `docs/architecture/system/architecture.md` and C4 diagrams to describe lowest-sufficient architecture surfaces and generated-output boundaries. |
| Plan reviews PLR1-PLR3 | Normalize architecture/readiness wording and model M6 as lifecycle closeout. | Updated the active plan so M1-M5 are implementation milestones and M6 is `Milestone type: lifecycle-closeout`. |
| Code reviews CR1-CR3 | Fix plan-state bookkeeping and stale `code-review`/`verify` final-closeout wording. | Closed CR1 as already fixed by bookkeeping, then updated canonical and generated `code-review` and `verify` skill text plus static checks. |
| CI-maintenance | No hosted CI edit is needed when current automation already covers the material risk. | Recorded that `.github/workflows/ci.yml` delegates all PR/main changes to `scripts/ci.sh` with no path filters, and branch-range selection covers the changed surfaces. |

## Requirements Trace

| Requirement area | Source IDs | Implementation evidence |
| --- | --- | --- |
| One standard workflow and isolated manual invocation | Workflow `R1`-`R5`; autoprogression `R1`-`R5` | `CONSTITUTION.md`, `AGENTS.md`, `README.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, `specs/workflow-stage-autoprogression.md`, canonical skills, generated skills, and adapter outputs. |
| Final closeout order | Workflow `R7x`-`R8j`, `R10`-`R10h`; milestone-aware review handoff requirements | Workflow specs, milestone-aware handoff spec/test, `skills/code-review/SKILL.md`, `skills/verify/SKILL.md`, plan handoff state, and generated public copies. |
| Public skill surface boundary | Workflow `R20`-`R20h`; skill contract `R3d`-`R3l`, `R12b`, `R20`-`R20b` | Canonical skill wording, generated skill mirrors, public adapter skill copies, and `scripts/test-skill-validator.py` portability checks. |
| Workflow guide responsibility | Workflow `R6d`-`R6n` | `docs/workflows.md` and `skills/workflow/SKILL.md` describe the guide as readable project workflow guidance, not the canonical spec. |
| CI-maintenance boundary | Workflow `R9`-`R9b`, `R18`, `R19`; skill contract `R6`-`R6c` | `skills/ci/SKILL.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, and CI-maintenance handoff evidence in the active plan. |
| Lowest sufficient architecture surface | Architecture package method and approved architecture review | `docs/architecture/system/architecture.md`, `docs/architecture/system/diagrams/context.mmd`, and `docs/architecture/system/diagrams/container.mmd`. |

## Diff Rationale By Area

| Area / files | Change | Reason | Source artifact | Test or evidence |
| --- | --- | --- | --- | --- |
| `docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md` | Recorded the accepted direction, including manual skill isolation, explain-before-verify, CI-maintenance boundary, workflow guide responsibility, and public skill boundary. | The change needed a reviewed decision record before spec and implementation work. | Proposal-review R1/R2 and `review-resolution.md`. | Proposal lifecycle validation and selected CI in `change.yaml`. |
| `specs/rigorloop-workflow.md` | Updated the canonical workflow contract to one standard workflow, manual invocation isolation, stage obligation metadata, final closeout order, active-plan transition rules, and public-surface static expectations. | This is the authoritative workflow-routing contract. | Workflow spec-review R1-R5. | `specs/rigorloop-workflow.test.md`, retired-wording scans, selected CI, lifecycle validation. |
| `specs/workflow-stage-autoprogression.md` | Replaced stale "default" downstream language with mandatory-or-triggered continuation and aligned final closeout routing through `ci-maintenance`, `explain-change`, `verify`, and `pr`. | Autoprogression must not turn isolated skill use into workflow completion or skip triggered stages. | Spec-review SR6/SR7 and autoprogression requirements. | `specs/workflow-stage-autoprogression.test.md`, `scripts/test-skill-validator.py`, selected CI. |
| `specs/milestone-aware-review-handoff.md` | Aligned clean final milestone review behavior with final closeout rather than direct `verify`. | Planned milestone routing must close implementation milestones before downstream lifecycle gates. | Spec-review SR8 and plan-review PLR3. | `specs/milestone-aware-review-handoff.test.md`, code-review R7. |
| `specs/skill-contract.md` | Added exact public-skill portability allow/block policy and clarified `ci` as the current `ci-maintenance` skill entrypoint. | Published skills are a user-facing interface and should not leak RigorLoop maintainer internals. | Skill contract amendment and spec-review R5. | `specs/skill-contract.test.md`, `scripts/test-skill-validator.py`, generated-output checks. |
| `CONSTITUTION.md`, `AGENTS.md`, `README.md`, `docs/workflows.md` | Replaced lane-like route guidance with one standard workflow and isolated manual skill use; reordered final closeout; updated generated-output and public-surface guidance. | Contributor-facing guidance must summarize the governing contract without competing with it. | Workflow spec, Constitution rules, proposal decisions. | Retired-term scans, README validation, selected CI. |
| `skills/workflow/SKILL.md` | Removed lane selection language, added standard workflow routing and `docs/workflows.md` refresh responsibility. | The workflow skill should route work and maintain the readable guide, not author a competing spec. | Proposal workflow guide decision and workflow `R6d`-`R6n`. | Skill validation, skill-validator regression, generated-output drift checks. |
| `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, `skills/plan/SKILL.md` | Updated milestone handoff and final closeout readiness language; removed direct final-milestone-to-`verify` phrasing. | Implementation and review stages must not overclaim final lifecycle readiness or skip closeout gates. | Milestone-aware handoff amendment and CR2. | Code-review R5/R7, stale direct-verify scans, selected CI. |
| `skills/explain-change/SKILL.md`, `skills/verify/SKILL.md`, `skills/pr/SKILL.md` | Moved durable rationale before final verify, kept final validation under `verify`, preserved isolated direct `verify`, and kept PR readiness under `pr`. | Stage ownership needed a clean claim boundary after the order change. | Proposal SWF2, CR3, workflow `R10`-`R10h`. | `scripts/test-skill-validator.py`, stale verify-before-explanation scans, selected CI. |
| Other canonical skills under `skills/` | Replaced stale lane wording and public internal-detail language where the skills participate in workflow routing or published guidance. | Public shipped skills need consistent portable wording across supported stages. | Skill contract `R3d`-`R3l`. | Skill validation and public-surface scans. |
| `.codex/skills/**` | Refreshed generated local Codex runtime mirrors from canonical skills. | Generated runtime guidance must match canonical skill sources. | Generated-output policy in Constitution, workflow spec, and skill contract. | `python scripts/build-skills.py`, `python scripts/build-skills.py --check`. |
| `dist/adapters/**` | Refreshed public Codex, Claude, and opencode adapter packages from canonical skills and adapter templates. | Public adapter packages carry shipped skill text and must match canonical source while staying project-portable. | Skill contract public-surface boundary and adapter-generation policy. | `python scripts/build-adapters.py --version 0.1.1`, drift checks, adapter validation, adapter distribution tests. |
| `scripts/adapter_templates/**` | Aligned adapter entrypoint guidance with the standard workflow and public-skill portability policy. | Adapter package guidance is public and should not preserve stale lane routing. | Skill contract and workflow specs. | Adapter generation and validation checks. |
| `scripts/test-skill-validator.py` | Added static checks for retired route vocabulary, stale final-closeout phrases, verify-before-explanation phrases, and public skill internal-path leakage. | The review found stale phrases that existing checks missed; validation needed narrow phrase coverage. | SWF5, SR8, SR9, CR2, CR3. | `python scripts/test-skill-validator.py` and selected CI. |
| `scripts/test-select-validation.py` | Updated expectations for project-portable validation-selector wording in public skill text. | Selector-related examples in public skills should not expose repository-internal commands as user-facing requirements. | Public skill surface boundary. | `python scripts/test-select-validation.py`. |
| `docs/architecture/system/architecture.md` and C4 diagrams | Added direct canonical architecture update guidance, lowest-sufficient architecture surface, generated-output flow, validation/generation responsibilities, and final closeout flow. | The architecture package must describe current repository boundaries after the workflow/governance change. | Architecture-review R1. | Architecture lifecycle validation, C4 diagram selected CI, code-review R7. |
| `docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md` and `docs/plan.md` | Created and maintained the active execution plan, milestone state, validation notes, decision log, current handoff, and plan index synchronization. | Planned initiative state must be durable and synchronized before downstream claims. | Plan-review R2 and milestone commit policy. | Plan lifecycle validation, selected CI, code-review R7, ci-maintenance checks. |
| `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/**` review artifacts | Added `change.yaml`, `review-log.md`, `review-resolution.md`, and detailed proposal/spec/architecture/plan/code review records. | Material findings needed durable records and dispositions before downstream closeout. | Formal review recording contract and review-resolution contract. | `python scripts/validate-review-artifacts.py --mode closeout ...` passed with 17 reviews, 23 findings, 0 unresolved. |
| `docs/learn/sessions/2026-05-08-*.md` | Recorded explicit learn sessions for process questions surfaced during this change. | The user asked for learn captures around spec-review rounds, architecture update overhead, code-review evidence timing, and milestone commit policy mismatch. | Learn skill invocations and workflow learn model. | Learn artifacts are tracked; selected branch-range inspection classified them as learn artifacts. |

## Tests Added Or Changed

| Test surface | What changed | What it proves |
| --- | --- | --- |
| `specs/rigorloop-workflow.test.md` | Added/updated coverage for one standard workflow, isolated manual skill invocation, final closeout order, `ci-maintenance` boundary, and public workflow-surface assertions. | The canonical workflow spec can be reviewed against concrete manual and integration checks. |
| `specs/workflow-stage-autoprogression.test.md` | Updated v1 autoprogression coverage for mandatory or triggered downstream stages, isolated manual skill invocation, and final `ci-maintenance -> explain-change -> verify -> pr` ordering. | Workflow-managed continuation does not bypass triggers or turn manual skill runs into workflow completion. |
| `specs/milestone-aware-review-handoff.test.md` | Replaced direct-verify closeout assertions with final-closeout readiness and lifecycle-closeout milestone checks. | Clean final implementation milestone review routes to final closeout, while non-final or ambiguous milestones do not. |
| `specs/skill-contract.test.md` | Added published-skill portability and `ci`/`ci-maintenance` entrypoint coverage. | Shipped skills omit maintainer-only details while internal repository surfaces may still mention them. |
| `scripts/test-skill-validator.py` | Added phrase-based retired-term, stale closeout, verify-before-explanation, and public internal-path checks over canonical and generated public skill surfaces. | Historical wording regressions are blocked without broad semantic prose scoring. |
| `scripts/test-select-validation.py` | Updated selector and skill wording expectations to use project-portable language. | Validation routing remains deterministic while published skills avoid internal command/path leakage. |
| Generated-output drift and adapter tests | Regenerated and checked `.codex/skills/**` and `dist/adapters/**`. | Derived skill and adapter packages stay reproducible from canonical sources. |

The test level is mostly static and artifact-focused because this change changes workflow contracts, documentation, skills, generated guidance, and validation text rather than runtime application behavior.

## Validation Evidence Available Before Final Verify

Validation already run and recorded includes:

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/test-select-validation.py`
- `python scripts/build-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/build-adapters.py --version 0.1.1`
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/test-adapter-distribution.py`
- `python scripts/validate-adapters.py --version 0.1.1`
- `python scripts/validate-readme.py README.md`
- `python scripts/validate-readme.py README.md --vision-markers`
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-08-single-workflow-lane-explain-before-verify`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-single-workflow-lane-explain-before-verify`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`
- `python scripts/select-validation.py --mode pr --base origin/proposal/2026-05-08-skill-optimization --head HEAD`
- selected `bash scripts/ci.sh --mode explicit ...` runs over proposal/spec/review artifacts, canonical skills, generated output, adapter templates, architecture package, active plan state, and the full initiative changed path set;
- `git diff --check -- ...` and whitespace scans over touched milestone surfaces.

The latest ci-maintenance pass inspected `.github/workflows/ci.yml`, `.github/workflows/release.yml`, `scripts/ci.sh`, and `scripts/validation_selection.py`. It found no hosted workflow edit was needed because the CI workflow runs on pull requests and `main` pushes without path filters and delegates validation routing to the repo-owned selector-backed wrapper.

Known validation notes before final `verify`:

- Hosted CI status has not been observed in this local stage and is not claimed here.
- Final `verify` still needs to validate this `explain-change.md` artifact, the updated `change.yaml`, plan/index synchronization, generated-output drift, review closeout, and current branch state.
- Lifecycle validation has previously reported existing nonblocking reviewer-attention warnings in `docs/plan.md` and `specs/rigorloop-workflow.md`; final `verify` owns deciding whether any warning is blocking for PR readiness.

## Review Resolution Summary

Review closeout is recorded in `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md`.

- Reviews covered: 17
- Material findings resolved: 23
- Unresolved findings: 0
- Dispositions: all material findings are accepted and resolved.

The major review-driven changes were:

- proposal-review SWF1-SWF8 tightened the problem framing, public-skill boundary, `docs/workflows.md` guide shape, static validation expectations, active-plan transition note, and `ci-maintenance` boundary;
- spec-review SR1-SR9 removed alternate lane/size/risk vocabulary, fixed direct-verify closeout wording, aligned autoprogression vocabulary, and strengthened static checks;
- plan-review PLR1-PLR3 normalized architecture/readiness state and converted M6 to lifecycle-closeout;
- code-review CR1-CR3 fixed milestone bookkeeping and stale `code-review`/`verify` final-closeout wording.

## Alternatives Rejected

| Alternative | Why rejected |
| --- | --- |
| Keep fast-lane/full-lifecycle or replace it with a small-change lane | It preserves the same public routing split and keeps completion evidence ambiguous. |
| Use "proportional evidence" as a contract term | Spec review found it still invited size/risk classification and made tests ambiguous. |
| Move only `explain-change` before `verify` | It fixes the circular dependency but leaves public lane guidance and public-skill internal leakage unresolved. |
| Put CI-maintenance after `verify` | That would let final explanation and verification ignore CI infrastructure changes in the final diff. |
| Create a separate `skills/ci-maintenance/` path | The approved contract keeps `skills/ci/` as the entrypoint while using `ci-maintenance` as the visible stage label. |
| Add a deterministic `docs/workflows.md` generator now | The proposal and plan chose skill-owned guide refresh because the content is still stabilizing and no repeated drift required a new generator. |
| Hand-edit generated `.codex/skills/` or `dist/adapters/` output | Generated surfaces are derived and must be refreshed from canonical skills and adapter templates. |
| Use a change-local architecture delta and merge-back loop for this architecture update | The user explicitly asked to update architecture directly, and architecture review accepted the direct canonical package update as the lowest sufficient surface. |

## Scope Control

The change preserved these non-goals:

- no separate fast, full, small-change, low-risk, high-risk, or mini-spec route was introduced;
- no workflow-guide generator was added;
- no `skills/ci-maintenance/` directory was created;
- no generated output was made canonical;
- no runtime service, database, deployment infrastructure, package format, or release metadata format changed;
- no broad natural-language scoring validator was added;
- `learn` remains periodic, triggered, or explicitly invoked rather than a default final per-change stage.

## Risks And Follow-Ups

- Final `verify` must run after this artifact exists and must treat this file as part of the final change pack.
- PR handoff is not ready until `verify` validates branch-ready evidence and PR readiness remains owned by `pr`.
- Hosted CI is not claimed as passed because no hosted run was observed during this stage.
- The active plan remains `Active` until final `verify` and PR handoff complete; when lifecycle completion becomes true in this PR, `docs/plan.md` and the plan body must be synchronized in the same PR state transition.
- If final `verify` identifies stale generated output, stale lifecycle state, or an outdated rationale after further edits, rerun the appropriate generator or update this artifact before PR handoff.

## Readiness For Verify

`explain-change` is complete enough to hand off to final `verify` once this artifact and its metadata/index updates are validated and committed.

This is not a final verification result. Final `verify` still owns validation evidence, branch-ready proof, and the decision on whether a standalone `verify-report.md` is required.
