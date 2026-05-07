# Explain Change: Review Skill Material Finding Recording

## Summary

This change closes the isolated-review material-finding recording gap across the formal review skills.

The core behavior is now explicit: isolation controls downstream handoff only; every material finding requires durable change-local review files. The change also makes new `review-resolution.md` records easier for humans to scan while preserving the field labels required by structural validation.

Implementation landed as one aggregate milestone commit for the former M1/M2/M3 scope because the proof assertions, shared guidance, and generated outputs are mutually dependent.

## Problem

Prior guidance let agents confuse two separate ideas:

- a direct or review-only request does not automatically continue downstream;
- a material review finding still needs durable evidence when it affects tracked work.

That ambiguity recurred in the learn session `docs/learn/sessions/2026-05-06-isolated-review-material-finding-records.md`, where an isolated material finding drove a tracked artifact edit but was not recorded until later reconstruction.

## Decision Trail

| Source | Decision |
|---|---|
| Proposal | Adopt the broad rule: material finding recording follows the finding, not workflow context. |
| Owner decision | Simplify the trigger: every material finding is recorded, all material findings require change-local review files, and isolation stops handoff, not recording. |
| Formal review spec | Add stage-neutral detailed-record triggers, isolated material output requirements, broad tracked-artifact definition, and shared review-skill block requirements. |
| Review-resolution spec | Require scan-first `review-resolution.md` records with summary, overview, compact details, shared validation evidence, and parseable labels. |
| Workflow spec | Preserve milestone commit requirements, review closeout blockers, and branch readiness gates. |
| Plan | Replan former M1/M2/M3 as one aggregate implementation slice because the static proof, canonical guidance, and generated outputs become green together. |

No separate architecture artifact was needed. The change reuses the existing review artifact model, skill validation, generated Codex skill mirror, and public adapter generation.

## Diff Rationale By Area

| Area | Files | Why they changed | Source artifact | Test/evidence |
|---|---|---|---|---|
| Governance and workflow summaries | `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md` | Align operational guidance with the broad material-finding rule and no-material clean-review lightweight path. | Proposal; `formal-review-recording` `R2c`, `R2d`, `R5a`; workflow `R12ana`, `R12anb` | `skills.regression`, `artifact_lifecycle.validate`, selected CI |
| Formal review recording specs | `specs/formal-review-recording.md`, `specs/rigorloop-workflow.md`, `specs/review-finding-resolution-contract.md` | Encode material finding recording, isolated output obligations, review closeout gates, no-material detailed-record boundaries, and scan-first review-resolution requirements. | Accepted proposal and review findings `RSV*`, `SR*`, `CR*` | review artifact tests, lifecycle validation |
| Test specs | `specs/*.test.md` for the three governing specs | Map each new `MUST` to proof surfaces, including shared block byte-equality, isolated material output fields, broad material trigger, generated drift, and scan-first closeout. | Plan M1 proof map | `test-skill-validator.py`, `test-review-artifact-validator.py` |
| Canonical shared block | `templates/shared/review-isolation-and-recording.md` | Provide one copy-paste source for the formal review skills without adding a generation step. | Proposal option and plan M2 | byte-equality assertions in `test-skill-validator.py` |
| Review-resolution template | `templates/review-resolution.md` | Give authors a scan-first structure that is useful to reviewers and still validator-readable. | `review-finding-resolution-contract` `R15`-`R15i` | scan-first fixture and negative table-only tests |
| Canonical skills | `skills/proposal-review`, `spec-review`, `architecture-review`, `plan-review`, `code-review`, plus downstream `verify`, `explain-change`, `pr` | Copy the shared block into formal review skills and align downstream closeout guidance with scan-first review-resolution summaries. | Plan M2 | `validate-skills.py`, `test-skill-validator.py` |
| Generated skill mirrors | `.codex/skills/**` | Refresh local Codex runtime output from canonical skill sources. | Plan M3 | `build-skills.py --check` |
| Public adapters | `dist/adapters/**` | Refresh Codex, Claude, and opencode adapter packages so shipped skill guidance matches canonical skills. | Plan M3 | `test-adapter-distribution.py`, `build-adapters.py --check`, `validate-adapters.py` |
| Review artifact validator tests | `scripts/test-review-artifact-validator.py` | Add proof for scan-first closeout, parseable per-finding labels, table-only rejection, no-material review boundaries, and closeout blockers. | Test spec `T18`; review-resolution spec | `python scripts/test-review-artifact-validator.py` |
| Skill validator tests | `scripts/test-skill-validator.py` | Add proof for shared block source, byte-equality copies, broad material rule wording, final output fields, and governance wording. | Test spec `T19`, `T20` | `python scripts/test-skill-validator.py` |
| Change-local evidence | `docs/changes/2026-05-07-review-skill-material-finding-recording/**` | Preserve proposal/spec/code review findings, dispositions, validation evidence, code-review reruns, and lifecycle metadata. | Review recording contract and workflow plan | review artifact closeout validation |
| Plan and learn artifacts | `docs/plan.md`, `docs/plans/...`, `docs/learn/**` | Record aggregate closeout, milestone-boundary lessons, plan-readiness lessons, validation, verify result, and current handoff state. | Workflow `R8a`-`R8c`; learn sessions | lifecycle validation |

## Tests Added Or Changed

| Test surface | What it proves |
|---|---|
| `scripts/test-skill-validator.py` | Formal review skills share the same `## Isolation and Recording` block from `templates/shared/review-isolation-and-recording.md`; the block contains the broad material-finding rule and isolated output obligations. |
| `scripts/test-review-artifact-validator.py` | `review-resolution.md` can be scan-first and still close out findings; table-only finding details without parseable labels fail; the reusable template preserves required fields. |
| `specs/formal-review-recording.test.md` | Requirements for isolated material output, tracked artifact definition, shared block placement, and structural-only first-slice validation have mapped proof. |
| `specs/review-finding-resolution-contract.test.md` | New `review-resolution.md` readability requirements are mapped to validator and fixture proof. |
| `specs/rigorloop-workflow.test.md` | Workflow closeout, review blockers, and validation layering remain aligned with the broader review recording contract. |

The tests are static or structural because the change updates workflow contracts, skills, templates, and generated documentation rather than runtime behavior.

## Verification Evidence

The aggregate implementation and later lifecycle updates passed:

- `python scripts/test-skill-validator.py`
- `python scripts/test-review-artifact-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/test-select-validation.py`
- `python scripts/test-adapter-distribution.py`
- `python scripts/build-skills.py --check`
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/validate-adapters.py --version 0.1.1`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-07-review-skill-material-finding-recording`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`
- `bash scripts/ci.sh --mode local`
- `bash scripts/ci.sh --mode explicit ...`
- `git diff --check 6f03c4e..HEAD -- .`

Selector-selected CI passed the stable checks `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.regression`, `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.

Broad smoke was not run. The plan records `broad_smoke_required: false` because this change affects workflow-governance artifacts, skills, templates, static validation, and generated packages without runtime data flow, deployment, storage, network, release packaging, schema, or external integration risk.

## Review Resolution Summary

Detailed review resolution is recorded in `docs/changes/2026-05-07-review-skill-material-finding-recording/review-resolution.md`.

Summary:

- Reviews covered: 7
- Material findings resolved: 13
- Unresolved findings: 0
- Dispositions: 13 accepted, 0 rejected, 0 deferred, 0 partially accepted, 0 needs-decision
- Closeout status: closed

The final code-review rerun, `code-review-r3`, found no blocking or required-change issues.

## Alternatives Rejected

| Alternative | Why rejected |
|---|---|
| Clarify only `proposal-review` | The same isolation-versus-recording ambiguity existed across all formal review skills. |
| Require detailed records for every isolated review | Too heavy for clean no-material reviews and contrary to the existing proportional record model. |
| Add validator-only enforcement | Would catch some omissions late but would not fix the skill wording that caused agents to skip recording. |
| Add semantic edit-reference validation in this slice | Deferred deliberately; the first slice stays structural/static to avoid overbuilding review-quality inference. |
| Generate the shared block into skills | Rejected by owner decision; the chosen mechanism is copy-paste with byte-equality assertion. |

## Scope Control

This change does not add a new review stage, does not introduce `pr-review`, does not make isolated reviews auto-continue downstream, does not require empty `review-resolution.md` for no-material detailed records, and does not change runtime product behavior.

Historical review records were not migrated except where this change needed current reconstructed or closeout evidence.

## Risks And Follow-Ups

Remaining risks:

- Manual copy-paste shared blocks can drift if future edits bypass the canonical source. Static byte-equality assertions are the guardrail.
- The current validator remains structural. Semantic detection of unrecorded review-driven edits is intentionally deferred.
- The plan remains Active until PR handoff and final lifecycle Done transition complete.

Follow-ups:

- Run PR handoff after this explanation is committed.
- Move the plan to Done in the PR tree if the PR claims this initiative complete.

## PR Handoff Summary

- Implements broad material-finding recording across formal review skills.
- Adds the canonical shared review block and scan-first review-resolution template.
- Adds validator coverage for shared block equality and review-resolution readability.
- Refreshes generated Codex skill mirrors and public adapters.
- Records closed review-resolution evidence and passing verify.

Readiness: ready for PR handoff after this explanation artifact and lifecycle bookkeeping are validated and committed.
