# Explain Change: Stage Evidence Access Contracts M2 Execution/Review

## Summary

This change completes M2 for stage evidence access contracts by adding concise evidence-access guidance to `implement` and `code-review`, adding concept-level static proof for those two skills, and recording the lifecycle evidence needed for downstream verification.

The reason for the change is to make high-cost execution and review stages start from the smallest sufficient evidence set without weakening implementation safety, independent review rigor, validation, material-finding, or source-of-truth behavior.

## Problem

M1 covered proposal-side evidence control. The accepted proposal and approved spec intentionally deferred execution/review stage guidance to M2 because `implement` and `code-review` are high-cost, high-risk evidence consumers.

The M2 problem was narrower than the original initiative:

- add local evidence-access guidance for `implement` and `code-review`;
- preserve their existing mandatory operating inputs and safety obligations;
- prove the guidance with concept-level checks;
- keep `plan`, `spec`, runtime enforcement, hard token gates, release behavior, adapter packaging, and generated-output source changes out of scope.

## Decision Trail

| Source | Decision or requirement | Effect on this change |
|---|---|---|
| Accepted proposal | Split execution/review evidence access into M2 after proposal-side M1. | Created a separate M2 plan instead of reopening M1. |
| Spec `R5`-`R15` | Define default, conditional, expansion, bounded discovery, full-file, and do-not-under-read behavior. | Added stage-local evidence-access sections to both touched skills. |
| Spec `R16`-`R18` | Preserve mandatory operating inputs and record input classification/migration notes. | Kept existing `Inputs to read` sections and recorded the migration table in the active plan. |
| Spec `R26`, `R29` | Keep `implement`/`code-review` as M2 scope and validate them separately when M2 runs. | Selected M2 validation targets only `skills/implement/SKILL.md` and `skills/code-review/SKILL.md`. |
| Spec `R30`-`R31` | Static checks should be concept-based, not exact long prose. | Added focused string checks for stable concepts in `scripts/test-skill-validator.py`. |
| Spec `R32`-`R34` | Do not add runtime enforcement or weaken safety-critical workflow behavior. | Kept this as a documentation/static validation change only. |
| Test spec `T12` | Prove `implement` local evidence guidance and input preservation. | Guided the `implement` skill update and validator terms. |
| Test spec `T13` | Prove `code-review` local evidence guidance and input preservation. | Guided the `code-review` skill update and validator terms. |
| Test spec `T14` | Prove M2 selected validation and lifecycle coherence. | Drove selected validation, lifecycle validation, token measurement, and change-local recording. |
| Plan M1 | Align the active test spec before skill implementation. | Added M2-specific test cases before editing skill guidance. |
| Plan M2 | Implement execution/review guidance with concept proof. | Added the two skill sections, validator checks, migration notes, and validation evidence. |

No architecture or ADR decision was needed because the change does not alter runtime architecture, data flow, persistence, APIs, release packaging, or adapter packaging.

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md` | Added M2 approval note, M2 plan reference, M2 coverage mappings, and test cases `T12`-`T14`. | The active test spec was M1-centered and needed direct proof requirements before execution/review skill edits. | Plan M1, spec `R5`-`R18`, `R26`, `R29`-`R34` | Test-spec alignment validation and maintainer approval recorded in the active plan and change metadata. |
| `skills/implement/SKILL.md` | Added an `Evidence access` section with default evidence, conditional evidence, bounded discovery boundary, expansion reason rule, do-not-under-read rule, and full-file escape conditions. | Gives implementation agents a smallest-sufficient-evidence starting point while preserving implementation safety. | Test spec `T12`; spec `R5`-`R18`, `R26`, `R30`-`R34` | `test_stage_evidence_access_m2_execution_review_skills`; code-review M2 R1. |
| `skills/code-review/SKILL.md` | Added an `Evidence access` section with default evidence, conditional evidence, bounded discovery boundary, expansion reason rule, do-not-under-read rule, and full-file escape conditions. | Gives reviewers a bounded evidence model without weakening actual-diff grounding, validation review, material findings, or milestone handoff. | Test spec `T13`; spec `R5`-`R18`, `R26`, `R30`-`R34` | `test_stage_evidence_access_m2_execution_review_skills`; code-review M2 R1. |
| `scripts/test-skill-validator.py` | Added `test_stage_evidence_access_m2_execution_review_skills`. | Provides stable concept-level proof for the two M2 skills without brittle paragraph matching. | Test spec `T12`-`T14`; spec `R30`-`R31` | `python scripts/test-skill-validator.py` failed before skill edits and passed after implementation. |
| `docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md` | Created and maintained the active M2 plan, current handoff, migration notes, validation notes, and review status. | The plan owns workflow state, milestone sequencing, input classification, and next-stage handoff. | AGENTS plan policy; plan-review R1; code-review M2 R1 | Plan lifecycle validation; review artifact validation; code-review clean result. |
| `docs/plan.md` | Added/updated the active plan index entry as M2 moved through planning, implementation, review, and now explanation. | Keeps the lifecycle index synchronized with the active plan. | AGENTS plan file policy | Artifact lifecycle validation. |
| `docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml` | Recorded changed files, requirements, tests, review status, and validation evidence. | Provides change-local lifecycle metadata for verification and PR handoff. | Workflow baseline change-local pack | Change metadata validation. |
| `docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/review-log.md` | Recorded formal reviews for plan-review and code-review. | Formal lifecycle reviews require durable recording. | Repository review-recording rules | Review artifact validation. |
| `docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/reviews/plan-review-r1.md` | Recorded clean plan review. | Proves the M2 plan was approved before test-spec alignment and implementation. | Plan-review stage | Review artifact validation. |
| `docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/reviews/code-review-m2-r1.md` | Recorded clean-with-notes code review with no material findings. | Closes M2 implementation review and confirms no review-resolution is required. | Code-review stage | Review artifact validation; plan handoff now routes to `explain-change`. |
| `docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/explain-change.md` | Added this durable rationale. | Ordinary non-trivial workflow changes need durable reasoning before final verify and PR. | Explain-change skill and active plan lifecycle closeout | To be validated after this artifact is recorded. |

## Tests Added Or Changed

| Test ID or command | What it proves | Why this level is appropriate |
|---|---|---|
| Test spec `T12` | `implement` has local evidence guidance, preserves input obligations, avoids logging bounded discovery, and keeps full-file/do-not-under-read escape behavior. | Static guidance change; direct text inspection and concept checks are enough. |
| Test spec `T13` | `code-review` has local evidence guidance and preserves independent-review obligations. | Static guidance change; direct text inspection and concept checks are enough. |
| Test spec `T14` | M2 selected validation covers `implement` and `code-review` without unrelated skill edits or hard token gates. | Integration-level selector and lifecycle proof match the risk. |
| `test_stage_evidence_access_m2_execution_review_skills` | The two M2 skills include required default evidence, conditional evidence, reason-recording, bounded discovery, and full-file concepts. | Concept-level unit/static proof avoids brittle paragraph locks. |

## Validation Evidence Available Before Final Verify

Recorded validation so far:

- `python scripts/select-validation.py --mode explicit --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/plan.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/plan.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
- `python scripts/test-change-metadata-validator.py`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
- `git diff --check -- specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md docs/plan.md docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review`
- `python scripts/test-skill-validator.py`
- `python scripts/select-validation.py --mode explicit --path skills/implement/SKILL.md --path skills/code-review/SKILL.md`
- `python scripts/validate-skills.py`
- `python scripts/test-build-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path scripts/test-skill-validator.py --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md --path specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/plan.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml`
- `python scripts/measure-skill-tokens.py`
- `git diff --check -- skills/implement/SKILL.md skills/code-review/SKILL.md scripts/test-skill-validator.py specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md docs/plan.md docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review`
- `python scripts/validate-review-artifacts.py docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/change.yaml --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/review-log.md --path docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/reviews/code-review-m2-r1.md`
- `git diff --check -- docs/plan.md docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review`

Static token measurement result was diagnostic only: 23 skills, 235521 bytes, and 58868 estimated tokens; `implement` measured 4268 estimated tokens and `code-review` measured 5054 estimated tokens.

Hosted CI has not been observed yet in this lifecycle. Final `verify` still owns the final readiness decision.

## Review Resolution Summary

No material findings were recorded.

- `plan-review-r1`: approved with 0 material findings.
- `code-review-m2-r1`: clean-with-notes with 0 material findings.

No `review-resolution.md` is required for this change.

## Alternatives Rejected

| Alternative | Why rejected |
|---|---|
| Reopen the completed M1 plan for execution/review guidance. | M1 intentionally closed proposal-side scope and deferred execution/review guidance to M2. |
| Update `plan` evidence guidance in M2. | The approved spec keeps `plan` as future-slice design context unless later promoted. |
| Add runtime enforcement or semantic read auditing. | Spec `R32` keeps those out of scope. |
| Add hard token gates. | Spec `R33` keeps static token measurement diagnostic and warning-only. |
| Phrase-lock long evidence-access paragraphs in the validator. | Spec `R30` requires concept-based checks rather than exact long wording. |
| Run release validation as part of M2. | The change does not alter release behavior; release validation was not selected by the active plan or test spec. |

## Scope Control

Preserved non-goals:

- no `plan` or `spec` skill update in M2;
- no runtime enforcement;
- no semantic read auditing;
- no hard token gates;
- no lifecycle token-cost summary implementation;
- no release behavior change;
- no adapter packaging change;
- no generated-output source model change;
- no weakening of code-review, validation, material-finding, source-of-truth, verify, PR, or release rules.

## Risks And Follow-Ups

Remaining risks:

- Final verification has not run yet.
- Hosted CI has not been observed yet.
- The plan remains active until `verify` and PR handoff complete.

Current readiness:

- M2 implementation is closed.
- Code-review is clean with no material findings.
- This explanation records the rationale for final verification.
- Next stage after this artifact is recorded and validated: `verify`.
