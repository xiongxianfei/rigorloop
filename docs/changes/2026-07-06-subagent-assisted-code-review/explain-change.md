# Explain Change: Subagent-Assisted Code Review

Change ID: 2026-07-06-subagent-assisted-code-review
Explanation date: 2026-07-06
Explained diff: `52bdcbb329897225c22a593b8e04541409e2d315..4f413933`
Current workflow state: final holistic code-review closed; next stage is `explain-change` at the time this artifact is authored.
Verify readiness: not-claimed
PR readiness: not-claimed

## Summary

This change adds the first vendor-neutral contract for subagent-assisted code review.
The main `code-review` skill remains the reviewer of record.
Subagents are modeled as read-only specialist evidence collectors that return bounded packets.
Repository-owned validators and regression tests now enforce the role vocabulary, packet schema, aggregation boundary, coverage table shape, advisory import summaries, and required-coverage failure modes.

The implementation deliberately avoids runtime orchestration, persistent raw packet files, packaged Claude subagent configs, mandatory Codex review, parallel execution, and auto-fix behavior.
Generated-output proof was recorded through existing skill and adapter generation checks instead of hand-editing generated public adapter output.

## Problem

RigorLoop formal code review was already evidence-bound and lifecycle-aware, but broad changes can span validators, generated output, release packaging, security, compatibility, workflow state, and documentation.
One reviewer can miss specialized risks when the surface is broad.

The accepted direction was to widen specialist coverage without fragmenting review authority.
Subagents may inspect bounded surfaces and return advisory evidence.
Only the canonical `code-review` skill verifies evidence, promotes material findings, records review artifacts, and routes lifecycle state.

## Decision Trail

| Decision source | Decision | Result in this diff |
|---|---|---|
| Accepted proposal | Use subagents as specialist evidence collectors, not final approvers. | `skills/code-review/SKILL.md` now documents reviewer-of-record invariants, advisory packets, and aggregation. |
| Accepted proposal | Do not initially store separate packet files, package every Claude subagent, require Codex review, require one model, or run parallel specialists. | Spec, plan, and implementation keep those surfaces optional or deferred. |
| Spec R1-R2 | Canonical `code-review` remains reviewer of record and direct review still works. | Skill guidance preserves direct review and forbids subagents from approving, closing, or claiming readiness. |
| Spec R3-R8 | Role vocabulary and packet status/schema are closed and fail closed. | `scripts/skill_validation.py`, `scripts/review_artifact_validation.py`, and tests enforce closed roles, statuses, schema version, and required fields. |
| Spec R9-R10 | Aggregator verifies evidence, deduplicates, resolves conflicts, and rejects malformed packets. | Aggregation helpers validate packets before promotion and record accepted, rejected, duplicate, and conflict outcomes. |
| Spec R11-R14 | Canonical review records coverage and preserve lifecycle boundaries; external reviews remain advisory. | Review-artifact validation covers subagent coverage, conflict decisions, and advisory import summaries. |
| Spec R15-R18 | Target-native configs, persistent packet files, parallel execution, and new dependencies are optional or out of first slice. | No new orchestrator, storage layer, vendor-specific config generator, dependency, or publication behavior was introduced. |
| Architecture assessment | Architecture not required for the first slice unless storage, orchestration, target-native generation, dependencies, or external integrations are added. | Implementation stayed within skills, scripts, tests, and change-local evidence. |
| Plan M1 | Update code-review contract and assets. | M1 updated the canonical skill and static skill validator tests. |
| Plan M2 | Add validation and fixtures. | M2 added helper validation, review-artifact validation, and focused regression tests. |
| Plan M3 | Prove generated-output and adapter alignment. | M3 added `behavior-preservation.md` and ran existing generated skill and adapter archive checks. |
| Final holistic review | Fix optional inconclusive coverage being treated as required. | `SUBCR-FINAL-CR1` was accepted and resolved by scoping the inconclusive clean-status block to required roles. |

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `docs/proposals/2026-07-06-subagent-assisted-code-review.md` | Recorded and accepted the proposal. | Preserve the user-selected direction and scope before spec work. | Proposal goals, non-goals, open questions. | `proposal-review-r1` approved with no material findings. |
| `specs/subagent-assisted-code-review.md` | Added the contract for roles, selection, packets, aggregation, coverage records, advisory imports, lifecycle boundaries, and deferred surfaces. | Convert the proposal into normative requirements. | R1-R18, AC1-AC14. | `spec-review-r1` approved with no material findings. |
| `specs/subagent-assisted-code-review.test.md` | Added a proof map from requirements to validator, skill, review-artifact, generated-output, and adapter checks. | Make implementation testable before code changes. | T1-T16. | `test-spec-review-r1` approved with no material findings. |
| `docs/changes/2026-07-06-subagent-assisted-code-review/architecture-assessment.md` | Recorded `architecture-not-required`. | The first slice did not introduce storage, orchestration, target-native config generation, dependencies, or external service boundaries. | Architecture assessment routing. | Plan proceeded without architecture doc. |
| `docs/plans/2026-07-06-subagent-assisted-code-review.md` | Added and maintained the active milestone plan, validation notes, handoffs, decisions, and final review state. | Keep workflow state single-owned by the plan body. | Plan policy and milestone workflow. | Lifecycle validation passed. |
| `docs/plan.md` | Added the plan index entry and advanced its next stage as milestones closed. | Keep the active lifecycle index in sync with the plan body. | Plan file policy. | Lifecycle validation passed. |
| `skills/code-review/SKILL.md` | Added subagent-assisted review mode, specialist selection, read-only boundaries, packet and aggregation contracts, conflict rules, advisory import guidance, and no-readiness-claim rules. | M1 needed the canonical review skill to own the reviewer-of-record behavior. | R1-R18, AC1-AC14. | `python scripts/test-skill-validator.py -k subagent_code_review`; `python scripts/validate-skills.py skills/code-review/SKILL.md`. |
| `scripts/skill_validation.py` | Added closed role/status constants, subagent selection helpers, packet validation, aggregation helpers, and advisory import validation. | M2 needed repository-owned validation for packet shape and aggregation semantics. | R3-R10, R14. | `python scripts/test-skill-validator.py -k subagent_code_review`. |
| `scripts/test-skill-validator.py` | Added focused regressions for skill guidance, role selection, packet validation, malformed packet rejection, aggregation dedupe/conflict behavior, low-evidence non-promotion, and advisory imports. | Prove validator behavior directly and catch closed-vocabulary regressions. | T1-T7, T9-T12, T14. | Targeted test command passed after M1, M2, and review-resolution fixes. |
| `scripts/review_artifact_validation.py` | Added validation for subagent coverage tables, missing required coverage, required inconclusive coverage, conflict decisions, and advisory imports. | M2 needed review records to fail closed when required specialist coverage is missing or malformed. | R11-R14, AC7, AC12, AC14. | `python scripts/test-review-artifact-validator.py -k subagent_code_review_record`; full validator test file. |
| `scripts/test-review-artifact-validator.py` | Added review-record fixtures for valid coverage, unknown roles, unknown statuses, missing required coverage, inconclusive required coverage, optional inconclusive coverage, malformed conflict decisions, and advisory summaries. | Prove parser-owned review artifact behavior without persistent packet files. | T8, T12, T14. | Full test file passed: 110 tests. |
| `docs/changes/2026-07-06-subagent-assisted-code-review/behavior-preservation.md` | Recorded generated skill mirror and adapter archive proof. | M3 needed durable evidence that canonical skill changes remain source-derived and adapter-compatible. | R13-R18, T13, T15, T16. | `build-skills`, `test-build-skills`, and adapter archive tests passed. |
| `docs/changes/2026-07-06-subagent-assisted-code-review/review-log.md` | Indexed all formal reviews and current open-finding state. | Formal lifecycle reviews require durable evidence and traceable open/closed finding state. | Review rules and review-resolution contract. | `validate-review-artifacts` passed. |
| `docs/changes/2026-07-06-subagent-assisted-code-review/review-resolution.md` | Recorded accepted dispositions for `SUBCR-M2-CR1` and `SUBCR-FINAL-CR1`, plus no-finding sections for clean reviews. | Material findings must be resolved before downstream explain-change, verify, or PR. | Review finding resolution contract. | Closeout status is closed; no open findings remain. |
| `docs/changes/2026-07-06-subagent-assisted-code-review/reviews/*.md` | Recorded proposal, spec, plan, test-spec, milestone code reviews, final holistic review, and rerun review evidence. | Formal reviews must be durable and auditable. | Workflow review requirements. | Review artifact validation passed with 10 review entries. |
| `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml` | Recorded artifacts, changed files, review state, and validation evidence. | Keep compact change metadata aligned with the lifecycle and review artifacts. | Change metadata contract. | `validate-change-metadata` passed. |

## Tests Added Or Changed

| Test area | Test IDs or functions | What it proves | Why this level is appropriate |
|---|---|---|---|
| Skill guidance and helper validation | `python scripts/test-skill-validator.py -k subagent_code_review` | The skill text exposes the required contract and helper APIs enforce closed roles, schema version, packet fields, aggregation behavior, advisory imports, and malformed packet rejection. | Unit-style tests are the right level for parser/helper behavior and skill-text contract checks. |
| Review artifact validation | `python scripts/test-review-artifact-validator.py -k subagent_code_review_record` | Review records validate coverage rows, unknown roles/statuses, missing required coverage, required inconclusive coverage, optional inconclusive coverage, conflict decisions, and advisory sections. | Review-record behavior is parser-owned, so direct fixture tests are more precise than broad workflow tests. |
| Final regression for `SUBCR-FINAL-CR1` | `test_subagent_code_review_record_optional_inconclusive_coverage_allows_clean_status` plus the existing required-inconclusive regression | Optional inconclusive subagent coverage no longer blocks a clean review when required coverage is satisfied, while required inconclusive coverage still blocks. | A paired positive/negative fixture proves the exact boundary from R11b and R12b. |
| Generated skill proof | `python scripts/build-skills.py --check`; `python scripts/test-build-skills.py` | Canonical skill changes remain source-derived and generated skill output stays current. | Existing generation tests own generated-skill parity. |
| Adapter package proof | `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives` | Adapter release archive generation still includes required release archives from canonical sources. | Existing adapter distribution tests own release archive behavior. |
| Lifecycle and metadata proof | `validate-review-artifacts`, `validate-change-metadata`, `validate-artifact-lifecycle` | Review records, change metadata, and plan/index lifecycle state are structurally coherent. | Repository-owned validators are the correct proof for workflow artifacts. |

## Validation Evidence Available Before Final Verify

Commands recorded during implementation and review:

```text
python scripts/test-skill-validator.py -k subagent_code_review
python scripts/validate-skills.py skills/code-review/SKILL.md
python scripts/test-review-artifact-validator.py -k subagent_code_review
python scripts/test-review-artifact-validator.py -k subagent_code_review_record
python scripts/test-review-artifact-validator.py
python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-06-subagent-assisted-code-review
python scripts/validate-change-metadata.py docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-07-06-subagent-assisted-code-review/behavior-preservation.md --path docs/proposals/2026-07-06-subagent-assisted-code-review.md --path specs/subagent-assisted-code-review.md --path specs/subagent-assisted-code-review.test.md --path docs/plans/2026-07-06-subagent-assisted-code-review.md --path docs/plan.md --path docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml
python scripts/build-skills.py --check
python scripts/test-build-skills.py
python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives
bash scripts/ci.sh --mode explicit --path skills/code-review/SKILL.md --path docs/changes/2026-07-06-subagent-assisted-code-review/behavior-preservation.md --path docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml --path docs/plans/2026-07-06-subagent-assisted-code-review.md --path docs/plan.md
```

Hosted CI status is not claimed.
Final `verify` has not run yet.

## Review Resolution Summary

Review-resolution artifact: `docs/changes/2026-07-06-subagent-assisted-code-review/review-resolution.md`.

| Finding | Disposition | Status | Summary |
|---|---|---|---|
| `SUBCR-M2-CR1` | accepted | resolved | Aggregation now validates each subagent packet before processing so malformed or unknown-role packets cannot produce accepted findings. |
| `SUBCR-FINAL-CR1` | accepted | resolved | Review-artifact validation now scopes inconclusive clean-status blocking to roles listed in `Required subagent coverage`. |

Counts:

- Accepted and resolved material findings: 2.
- Rejected, deferred, partially accepted, or needs-decision findings: 0.
- Open findings in `review-log.md`: 0.
- Final holistic code-review rerun: `code-review-final-r2`, clean-with-notes.

## Alternatives Rejected

| Alternative | Why rejected |
|---|---|
| Keep a monolithic reviewer-only model. | It preserves simplicity but does not improve specialist coverage for broad generated-output, security, release, compatibility, and workflow-state changes. |
| Let subagents directly write canonical findings or approve milestones. | This fragments lifecycle authority and weakens the reviewer-of-record model. |
| Require subagent consensus before a material finding can block. | A specialist finding can be material even when other reviewers are silent. Evidence, not vote count, must decide. |
| Store raw packet files in the first implementation. | The accepted first slice records summarized coverage in the canonical review artifact and defers packet storage until audit volume justifies it. |
| Package Claude custom subagents for every role immediately. | Vendor-neutral packet and aggregation behavior needed to stabilize first. |
| Require Codex/GitHub review for every PR. | External review output remains optional advisory evidence and does not replace local lifecycle review. |
| Add parallel specialist execution now. | Parallelism is an execution optimization after schema, read-only boundaries, and aggregation behavior are stable. |
| Hand-edit generated adapter output. | Generated public adapter output must remain source-derived through repository-owned generation checks. |

## Scope Control

The change preserves these non-goals:

- No subagent can approve, block, close, or mark milestones directly.
- No subagent edits code, documentation, generated output, review logs, or review-resolution records.
- No live GitHub PR review is required for local closeout.
- No single vendor output is authoritative.
- No persistent raw packet storage is required.
- No background asynchronous review or parallel execution is introduced.
- No generated public adapter package output is hand-edited.
- No verify, PR-body, PR-open, or branch readiness is inferred from subagent output.

## Risks And Follow-Ups

Residual risks:

- Future target-native Claude or Codex integrations can drift from the vendor-neutral packet contract if added without matching validation.
- Persistent packet storage and parallel execution remain unimplemented; introducing either later should trigger architecture review.
- Review-artifact validation now covers the first packet and coverage shapes, but future packet formats need explicit schema-version handling rather than ad hoc extension.

Follow-ups:

- Run final `verify` next.
- Revisit architecture before adding persistent packet files, reusable orchestration, target-native config generation, new dependencies, external review-service integration, or parallel execution.
- Keep future generated-output proof source-derived through repository-owned build and adapter validation commands.

## Readiness Statement

This explanation satisfies the `explain-change` stage for the current reviewed diff.
The active plan can move to `verify`.
This artifact does not claim final verification, branch readiness, PR-body readiness, PR-open readiness, hosted CI status, or merge readiness.
