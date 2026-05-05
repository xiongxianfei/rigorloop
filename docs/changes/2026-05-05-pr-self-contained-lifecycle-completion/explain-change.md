# PR-Self-Contained Lifecycle Completion Change Explanation

## Summary

This change implements the approved PR-self-contained lifecycle completion workflow amendment. M1 aligns the governing and operational guidance so repo-local lifecycle state changes are recorded in the PR that performs the transition before review opens, while true downstream events keep a plan active until the event occurs.

The implementation is intentionally staged. M1 updates authoritative and operational prose plus the baseline change-local evidence. M2 adds validator behavior. M3 wires selector routing for warning-capable surfaces, updates canonical skill guidance, and refreshes generated outputs. M4 closes implementation evidence. Later code-review and verify completed cleanly; this explanation prepares the PR handoff while the plan remains active until PR handoff completes.

## Source Artifacts

- Proposal: `docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md`
- Spec: `specs/rigorloop-workflow.md`, especially `R6dc`, `R8h`-`R8hc`, `R8jb`, and `R8kh`-`R8kj`
- Test spec: `specs/rigorloop-workflow.test.md`, especially `T29`-`T32`
- Plan: `docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`

## Problem

The workflow allowed routine plan `Active` to `Done` closeout to wait until after PR merge. That made the closeout structurally easy to forget: once the PR merged, attention moved on and `docs/plan.md` plus the plan body could stay stale. This branch also carries the incident context that exposed the problem: learn sessions and the PR #29 plan closeout that corrected the stale state.

## Decision Trail

| Decision source | Outcome |
| --- | --- |
| Proposal | Adopt PR-self-contained lifecycle completion: the PR that performs the lifecycle transition records it before review opens. |
| Spec | `R6dc` requires constitution-level wording; `R8h`-`R8hc` require plan/index synchronization inside the PR and forbid merge as the routine downstream event; `R8jb` requires reviewer-visible merge-dependent language classification. |
| Test spec | `T29`-`T32` define proof for visible guidance, validator behavior, spec/test-spec lifecycle state, and selected validation routing. |
| Plan | M1 updates guidance, M2 adds lifecycle/review validation, M3 routes warnings through selector and skill surfaces, and M4 records final evidence. |
| Review | M2 material finding `CR-M2-R1-F1` was accepted, fixed, and clean on re-review; M3 and M4 direct reviews were clean with no detailed-record trigger. |

## M1 Diff Rationale

| Surface | M1 disposition | Rationale |
| --- | --- | --- |
| `CONSTITUTION.md` | updated | Adds the required governance wording from `R6dc`: synchronization happens in the PR that performs the lifecycle transition before review opens, and merge is not a trigger for further lifecycle changes. |
| `docs/workflows.md` | updated | Replaces routine merge-dependent plan closeout guidance with PR-contained closeout, true downstream event handling, broader lifecycle inconsistency, and tracked merge-dependent language warning guidance. |
| `AGENTS.md` | updated | Keeps concise agent-facing verification guidance aligned with the governing rule without duplicating the full workflow contract. |
| `docs/learn/topics/plan-lifecycle-closeout.md` | updated | Converts the durable lesson away from merge-dependent closeout and toward PR-contained lifecycle synchronization plus true downstream event handling. |
| `docs/plans/0000-00-00-example-plan.md` | unaffected with rationale | Existing wording already says to update the plan body and `docs/plan.md` in the same change when the lifecycle decision is known; it does not preserve the removed merge-dependent exception. |
| `README.md` | unaffected with rationale | Current README points to workflow docs and does not carry the stale merge-dependent plan-closeout rule. |
| Canonical stage skills and generated outputs | deferred to M3 | The active plan owns canonical skill updates and generated `.codex/skills/` plus `dist/adapters/` refresh in M3 so generated-output drift is handled in one coherent slice. |

## SR-1 Resolution

Spec-review SR-1 asked where merge-dependent language classification is recorded. The active test spec resolves this for the first slice: a warning is treated as addressed only when a contributor-visible tracked or review-visible surface classifies the wording as a true downstream completion event or stale lifecycle wording requiring correction. Automatic warning suppression after classification is not required in the first implementation slice.

## M1 Validation

M1 validation is recorded in `change.yaml` and the active plan.

- `rg -n 'Only merge-dependent ...' CONSTITUTION.md AGENTS.md docs/workflows.md docs/learn/topics/plan-lifecycle-closeout.md docs/plans/0000-00-00-example-plan.md README.md` produced no matches after M1 edits.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml` passed.
- `python scripts/select-validation.py --mode explicit <M1 surface>` passed and selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `readme.validate`, `readme.vision_markers`, and `selector.regression`.
- `bash scripts/ci.sh --mode explicit <M1 surface>` passed with the same selected check IDs.
- `git diff --check -- <M1 edited surface>` produced no whitespace diagnostics.

The first stale-wording scan intentionally failed before M1 edits because stale merge-dependent closeout wording still existed in workflow docs and canonical skills. Skill wording remains deferred to M3 with tracked rationale.

## M2 Diff Rationale

| Surface | M2 disposition | Rationale |
| --- | --- | --- |
| `scripts/artifact_lifecycle_validation.py` | updated | Adds plan index/body lifecycle agreement checks, terminal plan readiness checks, and non-blocking tracked merge-dependent lifecycle-language warnings. |
| `scripts/test-artifact-lifecycle-validator.py` | updated | Adds failing-first coverage for completed plans under Active, duplicate Active/Done index entries, index-only plan changes, index/body disagreement, terminal stale readiness, true downstream active plans, and warning behavior. |
| `tests/fixtures/artifact-lifecycle/**` | updated | Adds focused fixture repositories for the new lifecycle validator cases. |
| `scripts/test-review-artifact-validator.py` | updated | Adds direct closeout-mode proof that `Closeout status: open` remains blocking even after material findings are resolved. |
| `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/reviews/**` | added | Records the M2 code-review finding, accepted resolution, and clean re-review. |

## M2 Validation

- `python scripts/test-artifact-lifecycle-validator.py` failed before implementation with the expected new M2 failures.
- A follow-up M2 self-check added and first observed a failing duplicate Active/Done index fixture before tightening the parser.
- M2 code-review added and first observed a failing index-only `docs/plan.md` fixture before expanding plan-index-only scope to linked plan bodies.
- `python scripts/test-artifact-lifecycle-validator.py` passed after implementation.
- `python scripts/test-review-artifact-validator.py` passed.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-05-pr-self-contained-lifecycle-completion` passed.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-05-pr-self-contained-lifecycle-completion` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths <proposal/spec/test-spec/plan-index/plan>` passed with expected non-blocking lifecycle-language warnings.
- `bash scripts/ci.sh --mode explicit <M2 surface>` passed selected checks `review_artifacts.regression`, `review_artifacts.validate`, `artifact_lifecycle.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml` passed.
- `git diff --check -- <M2 edited surface>` produced no whitespace diagnostics.
- `bash scripts/ci.sh --mode broad-smoke` passed after M2 review-resolution and clean re-review.

## M3 Diff Rationale

| Surface | M3 disposition | Rationale |
| --- | --- | --- |
| `scripts/validation_selection.py` | updated | Routes governance, workflow guidance, canonical skills, change metadata, and review artifacts through `artifact_lifecycle.validate` so tracked lifecycle-language warnings run where stale policy can be introduced. |
| `scripts/test-select-validation.py` | updated | Adds failing-first selector coverage for PR-contained lifecycle warning surfaces and adjusts CI wrapper expectations for multi-path lifecycle validation commands. |
| `skills/workflow/SKILL.md`, `skills/plan/SKILL.md`, `skills/implement/SKILL.md`, `skills/verify/SKILL.md`, `skills/explain-change/SKILL.md`, `skills/pr/SKILL.md` | updated | Replaces stale merge-dependent closeout guidance with the approved rule: lifecycle transitions are synchronized before review opens, true downstream completion events keep plans active, and merge itself is not the event. |
| `scripts/test-skill-validator.py` | updated | Adds stable phrase coverage for the affected stage skills and guards against reintroducing the removed merge-dependent closeout wording. |
| `.codex/skills/**`, `dist/adapters/**` | regenerated | Keeps generated Codex skill output and public adapter packages in sync with canonical skill guidance. |
| `scripts/ci.sh` | unaffected with rationale | Existing per-check output buffering already preserves warning output from selected validation; selector routing was sufficient. |

## M3 Validation

- `python scripts/test-select-validation.py` failed before implementation with the expected new selector test failure.
- `python scripts/test-skill-validator.py` failed before implementation with the expected new skill guidance failures.
- `python scripts/test-select-validation.py` passed after implementation.
- `python scripts/test-skill-validator.py` passed after implementation.
- `python scripts/validate-skills.py` passed.
- `python scripts/build-skills.py` regenerated `.codex/skills/`.
- `python scripts/build-skills.py --check` passed.
- `python scripts/build-adapters.py --version 0.1.1` regenerated public adapter output.
- `python scripts/build-adapters.py --version 0.1.1 --check` passed.
- `python scripts/validate-adapters.py --version 0.1.1` passed.
- `python scripts/test-adapter-distribution.py` passed.
- `python scripts/select-validation.py --mode explicit --path <M3 touched paths>` passed and selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- `bash scripts/ci.sh --mode explicit --path <M3 touched paths>` passed with the same selected check IDs.

## M4 Diff Rationale

| Surface | M4 disposition | Rationale |
| --- | --- | --- |
| `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml` | updated | Records M3/M4 clean reviews, M4 and verify validation, branch-scope changed files, and current handoff status. |
| `docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md` | updated | Marks M4, code-review, and verify complete; records validation and lifecycle decisions; keeps the plan Active until PR handoff completes. |
| `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/explain-change.md` | updated | Adds the M4 rationale and readiness state so PR handoff can use tracked evidence instead of chat memory. |
| `docs/plan.md` | unaffected with rationale | The implementation, code-review, and verify stages are complete, but the initiative is not Done until explain-change and PR handoff are complete in the PR tree. |

## M4 Validation

- M3 direct `code-review` of commit `2dab908` returned `clean-with-notes` with no material findings.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml` passed before M4 evidence edits.
- `python scripts/test-artifact-lifecycle-validator.py` passed.
- `python scripts/test-review-artifact-validator.py` passed.
- `python scripts/test-select-validation.py` passed.
- `python scripts/test-skill-validator.py` passed.
- `python scripts/validate-skills.py` passed.
- `python scripts/build-skills.py --check` passed.
- `python scripts/build-adapters.py --version 0.1.1 --check` passed.
- `python scripts/validate-adapters.py --version 0.1.1` passed.
- `python scripts/test-adapter-distribution.py` passed.
- `python scripts/select-validation.py --mode explicit --path <all touched paths>` passed and selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.regression`, `review_artifacts.validate`, `artifact_lifecycle.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- `bash scripts/ci.sh --mode explicit --path <all touched paths>` passed with the same selected check IDs.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml` passed after M4 evidence edits.
- `git diff --check -- <all touched paths>` produced no whitespace diagnostics after M4 evidence edits.
- M4 direct `code-review` of commit `e518725` returned `clean-with-notes` with no material findings.
- Verify passed after branch-scope PR-mode selector, PR-mode CI with broad smoke, review closeout validation, metadata validation, and whitespace cleanup for two precursor learn session files in the PR diff.

## Tests Added or Changed

| Test surface | What it proves |
| --- | --- |
| `scripts/test-artifact-lifecycle-validator.py` | Plan/index lifecycle disagreement, terminal stale readiness, duplicate Active/Done entries, true downstream Active plans, and merge-dependent language warnings. |
| `scripts/test-review-artifact-validator.py` | `Closeout status: open` remains blocking even after material findings are otherwise resolved. |
| `scripts/test-select-validation.py` | Selector routes tracked lifecycle-warning surfaces through `artifact_lifecycle.validate`, and CI command expectations match multi-path lifecycle validation. |
| `scripts/test-skill-validator.py` | Affected canonical stage skills carry PR-contained lifecycle guidance and do not reintroduce removed merge-dependent closeout wording. |
| Generated-output checks | `build-skills.py --check`, `build-adapters.py --version 0.1.1 --check`, adapter validation, and adapter distribution tests prove canonical and generated guidance stay synchronized. |

## Review Resolution Summary

Material findings: 1 accepted and closed (`CR-M2-R1-F1`). Rejected: 0. Deferred: 0. Partially accepted: 0. Needs decision: 0.

Review-resolution record: `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/review-resolution.md`.

M3 and M4 direct code-reviews were clean with no material findings, so their results are recorded artifact-locally in the plan, `change.yaml`, and this explanation rather than as empty detailed review records.

## Verification Evidence

- `python scripts/select-validation.py --mode pr --base origin/main --head HEAD` passed and selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.regression`, `review_artifacts.validate`, `artifact_lifecycle.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
- `bash scripts/ci.sh --mode pr --base origin/main --head HEAD` passed with the same selected check IDs, including broad smoke.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-05-pr-self-contained-lifecycle-completion` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml` passed.
- `git diff --check origin/main...HEAD` passed after removing EOF-only blank lines from two precursor learn session files.

## Alternatives Rejected

- Keep merge-dependent Done with reminders: rejected because the recurring stale-state issue is caused by relying on memory after merge.
- Build post-merge automation first: rejected for this slice because PR-contained state removes the routine need for post-merge cleanup.
- Suppress merge-dependent language warnings automatically after classification: rejected for the first slice; contributor-visible classification is enough.
- Add caching, distributed execution, or broader workflow automation: out of scope for this lifecycle rule.

## Scope Control

This change does not create a new lifecycle stage, does not change generated output by hand, does not require every historical artifact to be migrated, and does not treat release, deploy, package publication, external migration, or unobserved hosted checks as PR-local completion events.

## Risks and Follow-Ups

- The branch includes precursor learn/closeout commits that motivated the change; verification therefore used the full `origin/main...HEAD` PR diff rather than only the M1-M4 commit range.
- Generated skill and adapter output is intentionally included because canonical stage skill guidance changed.
- No deferred product or spec decision remains. The remaining workflow step is PR handoff.

## PR Handoff Summary

- The implementation and internal review/verify gates are complete.
- `docs/plan.md` and the plan body intentionally remain Active until PR handoff records the final pre-review lifecycle state.
- The PR body should call out that broad smoke was required by the touched CI-speed plan and passed in PR-mode CI.

## Current Readiness

M1 is implemented, code-reviewed with no required changes, and verified. M2 is implemented, CR-M2-R1-F1 is accepted and resolved, and M2 re-review is clean. M3 direct code-review is clean. M4 direct code-review is clean. Verify passed. Explain-change is complete.

`docs/plan.md` remains Active by design: PR handoff is not yet complete, so the plan is not Done under the PR-self-contained lifecycle rule.
