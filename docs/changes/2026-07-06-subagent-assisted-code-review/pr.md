# PR Handoff

## Status

- Change ID: 2026-07-06-subagent-assisted-code-review
- Stage: pr
- PR status: opened
- PR URL: https://github.com/xiongxianfei/rigorloop/pull/123
- Last updated: 2026-07-06

## Title

feat: add subagent-assisted code review contract

## Body

### Summary

- Add the first vendor-neutral subagent-assisted `code-review` contract while keeping `code-review` as the reviewer of record.
- Add repository-owned validation and fixture coverage for specialist roles, packet schema, aggregation, coverage records, conflict/advisory sections, and required-coverage failure modes.
- Record generated-skill and adapter archive proof without hand-editing generated public adapter output.
- Close two material review findings and record final branch-ready verification evidence.

### Why

- Broad RigorLoop changes can span validators, generated output, release packaging, workflow state, docs, and security-sensitive surfaces.
- The accepted direction widens specialist review coverage with bounded read-only advisory packets while preserving one canonical review artifact and lifecycle authority.

### Spec / plan / architecture

- Proposal: `docs/proposals/2026-07-06-subagent-assisted-code-review.md`
- Spec: `specs/subagent-assisted-code-review.md`
- Test spec: `specs/subagent-assisted-code-review.test.md`
- Architecture / ADRs: `docs/changes/2026-07-06-subagent-assisted-code-review/architecture-assessment.md` records `architecture-not-required`
- Plan: `docs/plans/2026-07-06-subagent-assisted-code-review.md`
- Explain change: `docs/changes/2026-07-06-subagent-assisted-code-review/explain-change.md`
- Verify report: `docs/changes/2026-07-06-subagent-assisted-code-review/verify-report.md`

### What changed

- Updated `skills/code-review/SKILL.md` with subagent-assisted review mode, specialist selection, bounded input/output packet guidance, read-only boundaries, aggregation, conflict handling, advisory import behavior, and readiness boundaries.
- Added closed role/status constants, subagent selection helpers, packet validation, aggregation helpers, and advisory import validation in `scripts/skill_validation.py`.
- Added review-artifact validation for subagent coverage tables, required coverage, conflict decisions, and advisory import summaries in `scripts/review_artifact_validation.py`.
- Added focused regressions in `scripts/test-skill-validator.py` and `scripts/test-review-artifact-validator.py`, including the final required-vs-optional inconclusive coverage boundary.
- Added proposal/spec/test-spec/plan/review/explain/verify evidence under `docs/changes/2026-07-06-subagent-assisted-code-review/`.

### Tests and verification

- [x] `python scripts/test-skill-validator.py -k subagent_code_review` - 2 tests passed
- [x] `python scripts/test-review-artifact-validator.py` - 110 tests passed
- [x] `python scripts/validate-skills.py skills/code-review/SKILL.md` - 1 skill file validated
- [x] `python scripts/build-skills.py --check` - generated skills validated
- [x] `python scripts/test-build-skills.py` - 7 tests passed
- [x] `python scripts/test-adapter-distribution.py` - 131 tests passed
- [x] `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-06-subagent-assisted-code-review` - reviews=10, findings=2, log_entries=10, resolution_entries=2
- [x] `python scripts/validate-change-metadata.py docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml` - valid change metadata
- [x] `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` - validated 3 artifact files
- [x] `bash scripts/ci.sh --mode explicit --broad-smoke ...` - selected checks and `broad_smoke.repo` passed locally
- [x] `bash scripts/ci.sh --mode explicit --path docs/changes/2026-07-06-subagent-assisted-code-review/verify-report.md --path docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml --path docs/plans/2026-07-06-subagent-assisted-code-review.md --path docs/plan.md` - post-report focused CI passed
- [ ] Hosted CI - pending after PR opens

### Requirement coverage

- R1-R2 -> T1, T2, T13 -> reviewer-of-record and direct review preservation in `skills/code-review/SKILL.md` and skill validator tests
- R3-R5 -> T3, T4, T5 -> closed specialist roles and changed-surface selection in `scripts/skill_validation.py`
- R6-R8 -> T6, T7, T8 -> bounded read-only packets and schema validation in skill guidance and packet validators
- R9-R10 -> T9, T10, T11, T12 -> aggregation validation, dedupe, conflict handling, and malformed-packet rejection
- R11-R12 -> T8, T11, T12 -> coverage recording plus missing/required inconclusive coverage checks in review-artifact validation
- R13-R14 -> T13, T14 -> lifecycle boundaries and advisory external review behavior
- R15-R17 -> T15 -> deferred first-slice boundaries recorded in behavior-preservation and explain-change evidence
- R18 -> T16 -> generated skill and adapter proof through build and adapter tests

### Review resolution summary

- Accepted: 2
- Rejected: 0
- Deferred: 0
- Partially accepted: 0
- Needs decision: 0
- Review-resolution: `docs/changes/2026-07-06-subagent-assisted-code-review/review-resolution.md`

### Risks and rollback

- Risk: future target-native Claude or Codex integrations drift from the vendor-neutral packet contract. Mitigation: add matching validation before introducing those adapters.
- Risk: persistent packet storage or parallel execution expands the architecture boundary. Mitigation: route those follow-ups back through architecture/spec before implementation.
- Rollback: remove the code-review skill contract additions, subagent validation helpers, review-artifact validation, focused regressions, and change-local lifecycle artifacts together.

### Reviewer notes

- This is a contract and validation slice, not runtime subagent orchestration.
- No persistent raw packet files, packaged Claude subagent configs, mandatory Codex review, parallel execution, auto-fix behavior, new dependencies, or generated public adapter hand edits are introduced.
- Hosted CI was not observed before PR creation; local selected CI with broad smoke passed.

### Follow-ups

- Revisit architecture before persistent packet files, reusable orchestration, target-native config generation, external review-service integration, new dependencies, or parallel execution.
- Review hosted CI after the PR opens.
