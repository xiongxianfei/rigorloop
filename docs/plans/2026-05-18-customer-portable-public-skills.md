# Customer-Portable Public Skills Execution Plan

- Status: done
- Owner: maintainers
- Start date: 2026-05-18
- Last updated: 2026-05-18
- Related issue or PR: this PR
- Supersedes: none

## Purpose / big picture

Implement the approved customer-portable public skill evidence contract in a small, reviewable first slice.

The goal is to make installed public skills operate safely in customer projects without requiring RigorLoop repository-internal docs, specs, reports, governance files, follow-up files, scripts, templates, generated mirrors, or adapter output as runtime evidence. The change must preserve rigor, keep public skill wording concise, and prove both static wording safety and runtime customer-fixture behavior.

## Source artifacts

- Proposal: [Customer-Portable Public Skills and Token-Friendly Local Guidance](../proposals/2026-05-18-customer-portable-public-skills-and-token-friendly-local-guidance.md)
- Spec: [Customer-Portable Public Skill Evidence](../../specs/customer-portable-public-skill-evidence.md)
- Architecture: not required; no runtime architecture change is expected.
- Test spec: [Customer-Portable Public Skill Evidence Test Spec](../../specs/customer-portable-public-skill-evidence.test.md)
- Review evidence: [customer-portable public skills review log](../changes/2026-05-18-customer-portable-public-skills/review-log.md)

## Context and orientation

Canonical authored public skill source lives under `skills/`. Generated public adapter skill bodies are release/generated output and must not be hand-edited. `docs/workflows.md` is the local artifact-location and workflow guide. This change affects public skill wording, workflow guidance, validation scripts, token reports, dynamic benchmark fixtures or reports, and generated-output validation evidence.

Likely touched surfaces:

- `docs/workflows.md`
- `skills/proposal/SKILL.md`
- `skills/proposal-review/SKILL.md`
- `skills/spec/SKILL.md`
- `skills/plan/SKILL.md`
- `skills/implement/SKILL.md`
- `skills/workflow/SKILL.md`
- `skills/verify/SKILL.md`
- `skills/pr/SKILL.md`
- `skills/project-map/SKILL.md`
- `scripts/test-skill-validator.py`
- `scripts/validate-skills.py`
- token-cost report under `docs/reports/token-cost/skills/`
- dynamic benchmark fixtures or reports
- temporary generated adapter output validation, not hand-edited generated bodies

`code-review` is a watchlist skill. It remains unchanged unless the audit finds a direct required RigorLoop-internal document dependency.

## Non-goals

- Do not copy full RigorLoop repository specs into customer projects.
- Do not make local `docs/workflows.md` mandatory for every skill invocation.
- Do not rewrite every public skill in one slice.
- Do not weaken safety-critical review, verification, material-finding, mutation-safety, or release-boundary rules.
- Do not implement `rigorloop status`, `rigorloop validate`, workflow YAML, generated workflow docs, or new CLI behavior.
- Do not introduce hard token gates.
- Do not run the full release benchmark suite unless a later approved artifact adds that scope.
- Do not hand-edit generated adapter skill bodies.

## Requirements covered

| Requirement IDs | Planned coverage |
|---|---|
| R1-R10 | Customer-project mode, local evidence use, portable defaults, ambiguity blocking, and no required local workflow guide in touched skills. |
| R11-R16 | `workflow` ownership of local `docs/workflows.md` guidance and concise customer-portability section in `docs/workflows.md`. |
| R17-R25 | Audit-scoped skill edits, `code-review` watchlist behavior, migration notes, and preservation of safety-critical boundaries. |
| R26-R28 | Focused static validation for required RigorLoop-internal dependency wording and allowed project-local references. |
| R29-R36 | Static token report and targeted customer-fixture dynamic benchmark evidence. |
| R37-R38 | Generated public adapter output validation from canonical skills without hand edits. |
| R39 | Out-of-scope CLI, workflow YAML, generated docs, hard token gates, release benchmark, and broad rewrite guardrails. |

## Current Handoff Summary

- Current milestone: M3. Measurement, dynamic benchmark, adapters, and lifecycle evidence
- Current milestone state: closed
- Last reviewed milestone: M3 code-review R4 clean-with-notes
- Review status: clean-with-notes
- Remaining in-scope implementation milestones: none
- Next stage: none
- Final closeout readiness: completed
- Reason final closeout is or is not ready: M1, M2, M3, review-resolution, explain-change, verify, and PR handoff are complete for this branch. Hosted CI and human review remain external PR-review outcomes and are not claimed here.

## Milestones

### M1. Audit, workflow portability guidance, and baseline measurement

- Milestone state: closed
- Goal: Record the audit result, establish the local workflow-guide portability rule, and capture the static skill token baseline before any public skill wording changes.
- Requirements: R1-R16, R17-R20, R25, R29-R31
- Files/components likely touched:
  - `docs/workflows.md`
  - `skills/workflow/SKILL.md`
  - `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.md`
  - optional `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.yaml`
  - audit evidence in this plan, change metadata, or a change-local implementation note
- Dependencies:
  - Approved spec
  - Plan-review
  - Test spec
  - No first-slice public skill wording edits have started, except the short `workflow` caveat if required by the approved scope.
- Tests to add/update:
  - Static validator coverage for the `docs/workflows.md` customer-project portability section
  - Static validator coverage for the short `workflow` caveat if added
  - Static token baseline report structure if repo-owned report validation exists
- Implementation steps:
  - Add concise customer-project portability guidance to `docs/workflows.md`.
  - Add the short `workflow` skill caveat for creating or refreshing local `docs/workflows.md`.
  - Record first-slice audit evidence for touched skills and the `code-review` no-touch decision.
  - Confirm the audit does not expand the touched set merely for uniform wording.
  - Run baseline static skill token measurement before M2.
  - Record the baseline command, date, source revision, measured skill paths, and summary in `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.md`.
  - If baseline measurement was not captured before public skill wording changes, stop and revise the plan or reconstruct the baseline from a named tracked revision using a clean checkout or worktree before continuing.
- Validation commands:
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-18-customer-portable-public-skills/change.yaml`
  - `git diff --check -- docs/workflows.md skills/workflow/SKILL.md docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.md docs/plans/2026-05-18-customer-portable-public-skills.md docs/changes/2026-05-18-customer-portable-public-skills/change.yaml`
- Expected observable result:
  - `docs/workflows.md` tells customer projects that public skills operate in customer-project mode by default, use project-local artifacts when present, do not require RigorLoop internals, and fall back or block appropriately.
  - `workflow` owns creating or refreshing local `docs/workflows.md`.
  - Static token baseline exists before M2 skill wording changes.
- Commit message: `M1: audit customer-portable skills and capture baseline`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [ ] decision log updated if needed
  - [x] validation notes updated
  - [x] hand off to code-review for M1
  - [ ] milestone committed
  - [x] clean code-review recorded
- Risks:
  - Overloading `docs/workflows.md` with long duplicated policy.
  - Making `docs/workflows.md` appear mandatory for every skill.
  - Accidentally starting skill wording edits before baseline evidence is recorded.
- Rollback/recovery:
  - Revert only the workflow guidance and workflow skill caveat if wording overreaches.
  - If skill edits begin before baseline evidence exists, reconstruct the baseline from a named tracked revision in a clean checkout or worktree, record the revision and command, and rerun plan-review before proceeding.

### M2. Public skill wording and static validation

- Milestone state: closed
- Goal: Update only audited risky public skill wording and add focused static proof for required RigorLoop-internal dependency phrasing.
- Requirements: R1-R10, R17-R28, R37-R39
- Files/components likely touched:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/project-map/SKILL.md`
  - `scripts/test-skill-validator.py`
  - `scripts/validate-skills.py`
- Dependencies:
  - M1 closed or no longer blocking
  - M1 baseline static token measurement recorded
  - Test spec with requirement-to-test mapping
- Tests to add/update:
  - Static checks for forbidden required RigorLoop-internal dependency wording
  - Static checks allowing project-local or conditional docs/spec references
  - Static checks for migration/audit evidence expectations where practical
- Implementation steps:
  - Rewrite risky references in touched skills as project-local, conditional, direct-target, or repository-mode references.
  - Preserve each touched skill's claim boundaries, stop conditions, output shape, and safety-critical obligations.
  - Leave `code-review` unchanged unless audit evidence shows direct required internal-doc dependency wording.
  - Add focused static validator coverage for forbidden and allowed wording.
  - Run canonical skill validation.
  - Stop if the M1 baseline is missing; do not continue skill wording edits until baseline evidence exists or a named tracked-ref reconstruction method is recorded.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-18-customer-portable-public-skills/change.yaml`
  - `git diff --check -- skills scripts docs/changes/2026-05-18-customer-portable-public-skills/change.yaml`
- Expected observable result:
  - Touched public skills no longer require RigorLoop repository-internal docs as customer-project evidence.
  - Legitimate project-local docs/spec references remain allowed.
- Commit message: `M2: make audited public skills customer-portable`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [ ] decision log updated if needed
  - [x] validation notes updated
  - [x] hand off to code-review for M2
  - [ ] milestone committed
  - [x] clean code-review recorded
- Risks:
  - Removing safety-critical behavior while simplifying wording.
  - Static checks becoming too broad and blocking legitimate project-local references.
- Rollback/recovery:
  - Revert the specific skill wording or static check that overreaches, preserving unrelated milestone changes.

### M3. Measurement, dynamic benchmark, adapters, and lifecycle evidence

- Milestone state: closed
- Goal: Record after-change static proof, compare it with the M1 baseline, run targeted dynamic proof, validate generated public adapter output from canonical skills, and prepare lifecycle evidence for downstream gates.
- Requirements: R29-R39
- Files/components likely touched:
  - `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.md`
  - optional `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.yaml`
  - dynamic benchmark fixtures or report files
  - change-local explain-change and validation evidence
  - temporary generated adapter output outside tracked source, if supported by scripts
- Dependencies:
  - M2 skill wording and static validation complete
  - M1 baseline static token measurement recorded
  - Dynamic benchmark mechanism selected in test spec or implementation notes
- Tests to add/update:
  - Report validation for the static token report if repo-owned report validation exists
  - Dynamic benchmark result-quality checks or recorded manual acceptance criteria
  - Adapter validation from temporary generated output
- Implementation steps:
  - Run after-change static skill token measurement.
  - Compare the after-change measurement against the M1 baseline and record the before/after report.
  - Run targeted customer-fixture dynamic benchmark scenarios:
    - `proposal-customer-no-internal-docs`
    - `proposal-review-customer-local-artifacts`
    - `spec-customer-local-workflow-guide`
    - `plan-customer-local-spec-and-code`
    - `implement-customer-plan-handoff`
    - `workflow-customer-route-no-internal-docs`
    - `project-map-customer-repo-orientation`
    - `verify-customer-final-pack`
    - `pr-customer-ready-handoff`
    - `code-review-customer-diff-small` only if `code-review` changes
  - Record broad searches, full-file reads, largest command output, input tokens, result-quality status, local guide use, portable-default behavior, ambiguity blocking, and attempted reliance on absent RigorLoop internals.
  - Validate generated public adapter output from canonical `skills/` using temporary or release-output generation.
  - Update change-local metadata and durable reasoning evidence.
- Validation commands:
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version <current-or-next-version> --output-dir <tmp-output>`
  - `python scripts/validate-adapters.py --root <tmp-output> --version <current-or-next-version>`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-18-customer-portable-public-skills/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-18-customer-portable-public-skills`
  - `git diff --check --`
- Expected observable result:
  - Static comparison evidence uses the M1 baseline and the M3 after-change measurement.
  - Dynamic measurement evidence shows public skills do not require RigorLoop repository-internal docs in customer projects.
  - Generated public adapter output validates from canonical skills without hand-editing generated bodies.
- Commit message: `M3: record customer-portable skill measurement evidence`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [ ] decision log updated if needed
  - [x] validation notes updated
  - [x] hand off to code-review for M3
  - [ ] milestone committed
  - [x] clean code-review recorded
- Risks:
  - Dynamic benchmark output becomes too broad or expensive.
  - Adapter generation tooling may need a current-or-next version value.
- Rollback/recovery:
  - Preserve static validation and skill wording; if dynamic benchmark tooling is unavailable, record the blocker and keep generated adapter validation gap explicit for review.

## Validation plan

Run the smallest relevant validation after each milestone, then expand before final verify:

- M1: workflow/static skill validator checks, baseline static token measurement, metadata, and diff checks for touched docs/skill/report surfaces.
- M2: full skill validator, skill validation, generated skill check, metadata, and diff checks for touched skill/script surfaces.
- M3: after-change static token measurement and comparison against the M1 baseline, dynamic benchmark evidence, adapter temp-output generation/validation, review artifact validation, metadata validation, and broad diff check.

Before PR readiness, expected verification includes:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/measure-skill-tokens.py
python scripts/build-skills.py --check
python scripts/validate-change-metadata.py docs/changes/2026-05-18-customer-portable-public-skills/change.yaml
python scripts/validate-review-artifacts.py docs/changes/2026-05-18-customer-portable-public-skills
git diff --check --
```

Adapter validation is required if canonical public skills change:

```bash
python scripts/build-adapters.py --version <current-or-next-version> --output-dir <tmp-output>
python scripts/validate-adapters.py --root <tmp-output> --version <current-or-next-version>
```

## Risks and recovery

- Risk: skill wording becomes vague.
  - Recovery: restore essential contract wording and cite the preserved rule in migration evidence.
- Risk: static checks block legitimate project-local docs/spec references.
  - Recovery: narrow forbidden phrases to required RigorLoop-internal dependency wording and add allowed examples.
- Risk: dynamic benchmark creates excessive output.
  - Recovery: cap routine output, summarize broad searches, and record only required metrics.
- Risk: generated adapter validation cannot run locally.
  - Recovery: record the command, failure, and smallest next action; do not hand-edit generated bodies.
- Risk: `code-review` is touched without proven need.
  - Recovery: revert `code-review` changes unless audit evidence identifies a direct required RigorLoop-internal dependency.

## Dependencies

- Spec is approved.
- Plan-review is required before implementation.
- Test spec is required before implementation.
- Adapter validation depends on available repository-owned adapter generation/validation scripts and a chosen version value.
- Dynamic benchmark implementation depends on existing benchmark harness or a focused first-slice fixture/report pattern defined during test-spec or implementation.

## Progress

- [x] 2026-05-18: proposal accepted after proposal-review R2.
- [x] 2026-05-18: spec created and approved by spec-review R1.
- [x] 2026-05-18: execution plan created.
- [x] 2026-05-18: plan-review R2 approved the revised plan and closed `CPS-PLAN-1`.
- [x] 2026-05-18: test spec created.
- [x] 2026-05-18: M1 implemented and handed off for code-review.
- [x] 2026-05-18: M1 reviewed cleanly and closed by code-review R1.
- [x] 2026-05-18: M2 implementation started after confirming the M1 baseline static token measurement exists.
- [x] 2026-05-18: M2 implemented and handed off for code-review.
- [x] 2026-05-18: M2 reviewed cleanly and closed by code-review R2.
- [x] 2026-05-18: M3 implementation started after M2 clean code-review R2.
- [x] 2026-05-18: M3 implemented and handed off for code-review.
- [x] 2026-05-18: M3 code-review R3 requested changes for `CPS-M3-CR1`.
- [x] 2026-05-18: M3 reviewed cleanly by code-review R4.
- [x] 2026-05-18: explain-change recorded.
- [x] 2026-05-18: verify passed locally with explicit selected CI proof; legacy no-argument broad smoke exposed unrelated baseline lifecycle debt and is recorded as a warning.
- [x] 2026-05-18: PR handoff prepared.

## Decision log

- 2026-05-18: no architecture stage planned -> this is a public skill/documentation/validation/reporting change with no runtime architecture change.
- 2026-05-18: use three implementation milestones -> separates workflow/audit anchoring, skill/static validation changes, and measurement/adapter proof.
- 2026-05-18: keep `code-review` watchlist-only -> safety-critical review wording should not change without direct dependency evidence.

## Surprises and discoveries

- M1 baseline static token measurement was captured before this implementation turn changed canonical public skill text.
- `code-review` remains unchanged for M1. The first-slice audit records it as watchlist-only unless M2 audit evidence finds a direct required RigorLoop-internal document dependency.
- Initial M3 targeted dynamic benchmark evidence used a synthetic customer fixture and manual result-quality record. Live model scenario execution was not run, so live input-token counters were recorded as not measured.
- code-review R3 found that the M3 dynamic benchmark evidence does not yet prove dynamic runtime behavior because required runtime fields are recorded as `not-measured` while scenario quality is marked `pass`.
- CPS-M3-CR1 fix replaced the static-only benchmark evidence with live `codex exec` JSONL and analyzer summaries for the required customer-fixture scenarios.

## Validation notes

- 2026-05-18: plan creation and plan-review recording validation passed before test-spec authoring.
- 2026-05-18: test spec authoring validation passed.
- 2026-05-18: M1 red proof: `python scripts/test-skill-validator.py` failed before implementation with missing `## Customer-project portability` in `docs/workflows.md` and missing `## Customer-project workflow guide` in `skills/workflow/SKILL.md`.
- 2026-05-18: M1 baseline proof: `python scripts/measure-skill-tokens.py` measured 23 canonical skills at 58,868 estimated tokens before this implementation turn changed public skill text. Baseline recorded in `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.md`.
- 2026-05-18: M1 green proof: `python scripts/test-skill-validator.py` passed after adding focused customer-project portability checks and M1 wording.
- 2026-05-18: M1 skill validation: `python scripts/validate-skills.py` passed for 23 canonical skill files.
- 2026-05-18: M1 generated skill check: `python scripts/build-skills.py --check` passed using temporary generated output.
- 2026-05-18: M1 change metadata validation passed.
- 2026-05-18: M1 review artifact validation passed.
- 2026-05-18: M1 artifact lifecycle validation passed for proposal, spec, test spec, plan, plan index, change metadata, review log, review resolution, and formal review records.
- 2026-05-18: M1 diff whitespace check passed for touched M1 surfaces.
- 2026-05-18: code-review R1 for M1 recorded `clean-with-notes` with no material findings.
- 2026-05-18: M2 red proof: `python scripts/test-skill-validator.py` failed before M2 skill wording because audited skills were missing `## Project-local evidence` and `project-map` was missing `## Customer-project orientation`.
- 2026-05-18: M2 green proof: `python scripts/test-skill-validator.py` passed after adding M2 skill wording and focused required-RigorLoop-internal dependency checks.
- 2026-05-18: M2 skill validation: `python scripts/validate-skills.py` passed for 23 canonical skill files.
- 2026-05-18: M2 generated skill check: `python scripts/build-skills.py --check` passed using temporary generated output.
- 2026-05-18: M2 code-review no-touch proof: `git diff -- skills/code-review/SKILL.md` produced no diff.
- 2026-05-18: M2 change metadata validation passed.
- 2026-05-18: M2 review artifact validation passed.
- 2026-05-18: M2 artifact lifecycle validation passed for proposal, spec, test spec, plan, plan index, change metadata, review log, review resolution, and formal review records.
- 2026-05-18: M2 diff whitespace check passed for touched skill, script, report, plan, and change-local surfaces.
- 2026-05-18: code-review R2 for M2 recorded `clean-with-notes` with no material findings.
- 2026-05-18: M3 after-change static proof: `python scripts/measure-skill-tokens.py` measured 23 canonical skills at 60,235 estimated tokens after M2 skill wording changes. The token report compares this with the M1 baseline of 58,868 estimated tokens.
- 2026-05-18: M3 customer fixture exclusion proof passed: the targeted fixture has no root `AGENTS.md`, no root `CONSTITUTION.md`, no `docs/follow-ups.md`, and no `docs/project-map.md`.
- 2026-05-18: M3 targeted dynamic benchmark record created at `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills-dynamic-benchmark.md` for proposal, proposal-review, spec, plan, implement, workflow, project-map, verify, and pr. `code-review` was not included because its skill wording did not change.
- 2026-05-18: M3 generated adapter build passed: `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-adapters-m3-BxELAV`.
- 2026-05-18: M3 generated adapter validation passed: `python scripts/validate-adapters.py --root /tmp/rigorloop-adapters-m3-BxELAV --version v0.1.5`.
- 2026-05-18: M3 final skill validator passed.
- 2026-05-18: M3 final canonical skill validation passed.
- 2026-05-18: M3 final generated skill check passed using temporary generated output.
- 2026-05-18: M3 final change metadata validation passed.
- 2026-05-18: M3 final review artifact validation passed.
- 2026-05-18: M3 final artifact lifecycle validation passed for proposal, spec, test spec, plan, plan index, change metadata, review log, review resolution, and formal review records.
- 2026-05-18: M3 final diff whitespace check passed.
- 2026-05-18: code-review R3 for M3 recorded `changes-requested` with material finding `CPS-M3-CR1`.
- 2026-05-18: CPS-M3-CR1 accepted. Live benchmark prompts, JSONL, and analyzer summaries were recorded under `docs/reports/token-cost/skills/runs/2026-05-18-customer-portable-public-skills/`.
- 2026-05-18: CPS-M3-CR1 live fixture exclusion proof passed after installing generated `.agents/skills/` and removing generated root `AGENTS.md` from the temporary fixture.
- 2026-05-18: CPS-M3-CR1 live dynamic benchmark evidence recorded measured runtime fields for proposal, proposal-review, spec, plan, implement, workflow, project-map, verify, and pr.
- 2026-05-18: CPS-M3-CR1 post-fix validation passed for change metadata, review artifacts, artifact lifecycle, diff whitespace, skill validator, canonical skill validation, and generated skill check.
- 2026-05-18: code-review R4 for M3 recorded `clean-with-notes` with no material findings and closed `CPS-M3-CR1`.
- 2026-05-18: explain-change recorded the problem-to-diff rationale, review-resolution summary, validation evidence, alternatives rejected, and remaining verify-stage risks.
- 2026-05-18: final verify passed targeted repository-owned validation: skill validator, canonical skill validation, static token measurement, generated skill check, adapter archive build/validation, fixture exclusion check, change metadata validation, review artifact validation, explicit lifecycle validation, diff whitespace check, and `bash scripts/ci.sh --mode explicit ...` selected checks.
- 2026-05-18: final verify broad-smoke warning: legacy no-argument `bash scripts/ci.sh` exited 1 because diff-scoped broad smoke expanded through `docs/plan.md` into unrelated historical lifecycle debt. The changed-surface explicit CI wrapper passed.
- 2026-05-18: PR handoff prepared after moving this plan from `Active` to `Done` in `docs/plan.md`.

## Outcome and retrospective

- Complete. Implementation milestones, review-resolution, explain-change, final local verify, and PR handoff are closed for this branch.

## Readiness

- See `Current Handoff Summary`.
- Ready for human PR review. Hosted CI and reviewer decisions are not claimed until observed on the opened PR.

## Risks and follow-ups

- Follow-up only if dynamic benchmark results show broad-search behavior outside the first-slice skill set.
