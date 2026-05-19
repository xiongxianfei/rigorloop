# Code Review M2 R1: Assets-First Progressive Disclosure Pilot

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit 3b6e42964f817772e26033cf4abf1fb75ece9418
Status: clean-with-notes
Reviewed artifact: M2. Plan Skill Asset Split
Review date: 2026-05-19
Recording status: recorded

## Result

- Skill: code-review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/reviews/code-review-m2-r1.md
- Review log: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/review-log.md
- Review resolution: not-required
- Open blockers: none
- Immediate next stage: implement M3

## Review inputs

- Diff/review surface: M2 implementation commit `3b6e42964f817772e26033cf4abf1fb75ece9418`.
- Tracked governing branch state: approved spec amendment, approved test-spec amendment, active plan, M2 implementation, change metadata, and M2 validation evidence are tracked.
- Governing artifacts: `specs/skill-contract.md` R37-R44, `specs/skill-contract.test.md` T33-T36, and `docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md` M2.
- Validation evidence: active plan and change metadata record passing M2 commands, including `python scripts/validate-skills.py`, `python scripts/test-skill-validator.py`, `python scripts/measure-skill-tokens.py --skills-root skills`, `python scripts/build-skills.py --check`, change metadata validation, `git diff --check --`, artifact lifecycle validation, and selected CI for supported paths.

## Diff summary

M2 rewrites `skills/plan/SKILL.md` into a shorter common-path execution contract with a `Resource map`, then adds exactly four normative assets under `skills/plan/assets/`: `plan-skeleton.md`, `milestone.md`, `current-handoff-summary.md`, and `decision-log-row.md`. The commit also adds behavior-preservation and token-cost evidence and updates the active plan, plan index, and change metadata for M2 handoff.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | The diff modifies only `plan` for the asset slice, adds exactly the four approved normative assets, keeps `references/` and `scripts/` absent, and leaves proposal/proposal-review/spec/spec-review/code-review/verify/pr untouched. |
| Test coverage | pass | M1 validator coverage remains active, and M2 validation passed `validate-skills.py`, `test-skill-validator.py`, `build-skills.py --check`, change metadata validation, lifecycle validation, and selected CI for supported paths. |
| Edge cases | pass | Direct inspection confirms literal `COPY` resource-map entries for all four assets, `plan-skeleton.md` owns the full section layout, and `current-handoff-summary.md` contains labels/placeholders rather than lifecycle transition rules. |
| Error handling | pass | The split preserves `Stop conditions`, upstream settlement blockers, no-unfilled-placeholder guidance, and readiness-vs-Done boundaries in `SKILL.md`. |
| Architecture boundaries | pass | M2 stays within canonical skill text, skill-local assets, and change-local evidence; adapter packaging and broader parity proof remain M3 scope. |
| Compatibility | pass | `SKILL.md` retains project-local evidence wording, portable artifact-placement guidance, required core sections, and compact output expectations while moving the full plan layout to `assets/plan-skeleton.md`. |
| Security/privacy | pass | The assets contain placeholders and structural Markdown only; no secrets, credentials, machine-local paths, repository-root required dependencies, or private data were introduced. |
| Derived artifact currency | pass | `python scripts/build-skills.py --check` passed; no generated public adapter output was hand-edited. |
| Unrelated changes | pass | The reviewed commit is limited to `skills/plan`, M2 evidence, change metadata, active plan state, and the plan index. |
| Validation evidence | pass | Token evidence records `skills/plan/SKILL.md` decreasing from 3862 to 3282 estimated tokens, a 15.02 percent common-path reduction; total packaged content grows 7.04 percent, below the 10 percent hard cap with rationale. |

## No-finding rationale

The M2 diff satisfies the planned asset split without moving lifecycle rules into assets. `SKILL.md` still owns handoff consistency, milestone state, upstream settlement, readiness-vs-Done, validation, and claim-boundary rules. The assets are structural templates with metadata, normative status, fingerprints, and placeholders. The implementation records behavior-preservation evidence and passes the 15 percent common-path token reduction gate.

## Residual risks

M3 still owns generated adapter asset proof, behavior-parity evidence, historical coverage evidence, and milestone asset reuse evidence. Selected CI does not currently support `token-cost.md` as a deterministic v1 selector path; the M2 handoff records that limitation and passes selected CI on supported paths.

## Milestone handoff

- Reviewed milestone: M2. Plan Skill Asset Split
- Review status: clean-with-notes
- Milestone state after review: closed
- Required review-resolution: no
- Remaining in-scope implementation milestones: M3
- Next stage: implement M3
- Final closeout readiness: not ready; M3 remains unimplemented, and explain-change, verify, and PR handoff have not run.
