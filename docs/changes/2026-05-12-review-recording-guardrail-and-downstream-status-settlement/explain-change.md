# Review Recording Guardrail and Downstream Status Settlement Explain Change

## Summary

This change makes formal lifecycle review findings harder to lose.

It adds a durable recording-output guardrail to the five formal review skills, keeps the full change-ID and `Location` rules in the formal review recording spec, moves examples out of active lifecycle-looking directories, and refreshes generated Codex, Claude, Codex-adapter, and opencode skill output.

The implementation intentionally does not add downstream upstream-status settlement behavior. That remains follow-up scope.

## Problem

The motivating failure was a `plan-review` result that reported material finding `PR-001` without creating the required change-local review record. A first correction then created the record but omitted `Location`, so the durable record still did not preserve the complete finding shape.

The existing policy already said material review findings must be recorded. The gap was operational: review skill output could finish after saying records should exist, without proving they were created or explicitly blocked.

## Decision Trail

| Decision point | Outcome | Source |
|---|---|---|
| Proposal direction | Keep review skills focused on recording evidence and defer downstream status settlement. | `docs/proposals/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md` |
| Spec contract | Add `Recording status`, required artifact path fields, complete material-finding shape, deterministic change-ID selection, and no standardized review-side status-sync fields. | `specs/formal-review-recording.md` `R24`-`R31m`, `R33` |
| Test plan | Prove recording output, `Location`, status-sync exclusion, examples routing, deterministic change-ID rules, and generated-output drift. | `specs/formal-review-recording.test.md` `T12`, `T21`-`T26` |
| Plan milestones | Split work into examples routing, review skill guardrail, and generated-output refresh. | `docs/plans/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md` M1-M3 |
| Review outcomes | M1, M2, and M3 code reviews returned `clean-with-notes` with no material findings. | Active plan validation notes and `change.yaml` |

No architecture or ADR artifact was required because this is a workflow/spec/skill contract change with no runtime architecture change.

## Diff Rationale By Area

| Files | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `docs/proposals/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md` | Accepted the narrowed proposal and recorded the split between review recording and downstream status settlement. | Preserve the chosen scope and avoid repeating the overbroad PR #44 direction. | Proposal review outcomes; spec `R33` | Proposal status is `accepted`; downstream settlement remains follow-up scope. |
| `specs/formal-review-recording.md` | Added normative rules for recording output, complete finding shape, `Location`, deterministic change-ID selection, generated-output refresh, and status-sync exclusion. | Give implementers and validators a testable contract instead of relying on skill prose alone. | `R15a`, `R24`-`R31m`, `R33` | `spec-review-r2` approved after `SR-001` was resolved. |
| `specs/formal-review-recording.test.md` | Added test coverage for recording status, artifact paths, `Location`, examples, status-sync exclusion, change-ID selection, and generated output. | Map every new `MUST` and named edge case to validation or manual proof. | `T12`, `T21`-`T26` | `python scripts/test-skill-validator.py` and adapter drift checks exercise these surfaces. |
| `docs/examples/**` | Added examples README, formal review recording examples, and moved the example plan to `docs/examples/plans/example-plan.md`. | Keep examples illustrative and prevent active selectors or lifecycle checks from treating them as current project state. | Spec `R31n`, `R32` series; test `T24` | `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-select-validation.py`; retained fixture rationale for `docs/changes/0001-skill-validator/`. |
| `AGENTS.md`, `CONSTITUTION.md`, `README.md`, `docs/workflows.md` | Updated references from the old example plan path and clarified examples/non-normative or recording behavior where needed. | Keep contributor-facing guidance aligned after the examples move and recording contract update. | Plan M1; test `T24` | Static validator and lifecycle/selector tests passed. |
| `scripts/test-artifact-lifecycle-validator.py`, `scripts/test-select-validation.py`, `scripts/validation_selection.py` | Taught validation/routing to treat `docs/examples/**` as examples, not active lifecycle state. | Make the examples move enforceable, not just documented. | Spec/test `T24` | `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-select-validation.py`. |
| `scripts/test-skill-validator.py` | Added static checks for formal review `Recording status` output, required fields, complete finding shape terms, short change-ID pointer, and exact forbidden status-sync fields. | Prevent review skills from dropping the guardrail or reintroducing status-sync output fields. | `R29a`, `R30`, `T23` | `python scripts/test-skill-validator.py` passed with 63 tests. |
| `templates/shared/review-isolation-and-recording.md` | Added the concise shared recording-status output block and complete material-finding shape. | Keep all five formal review skills aligned from one canonical shared source. | `R21`, `R24`-`R29`, `T19`, `T21`-`T23` | Shared-block byte-equality test passed. |
| `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md`, `skills/architecture-review/SKILL.md`, `skills/plan-review/SKILL.md`, `skills/code-review/SKILL.md` | Added recording-status guidance and result fields for review record, review log, review resolution, and blocker reporting. | Make material-finding recording operationally visible in formal review outputs. | `R24`-`R31m` | `python scripts/test-skill-validator.py`; M2 code-review clean. |
| `.codex/skills/**` and `dist/adapters/**` formal review skill outputs | Regenerated local Codex mirrors and public adapter packages from canonical skills. | Generated users must receive the same recording guardrail as canonical skill users. | `R15a`, `T12` | `python scripts/build-skills.py --check`; `python scripts/build-adapters.py --version 0.1.1 --check`; `python scripts/validate-adapters.py --version 0.1.1`. |
| `docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/**` | Added change metadata, spec-review records, review log, review resolution, and this explain-change. | Preserve durable review evidence, resolution evidence, validation evidence, and rationale. | Workflow baseline pack; formal review recording rules | `python scripts/validate-review-artifacts.py --mode closeout ...`; `python scripts/validate-change-metadata.py ...`. |
| `docs/plans/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md`, `docs/plan.md` | Added and maintained the active execution plan, milestone state, validation notes, and next-stage handoffs. | Keep workflow state explicit and avoid chat-only milestone state. | Plan workflow; implement/code-review handoff rules | M1-M3 closed after clean code reviews; current next stage is `explain-change` before this artifact, then `verify`. |

## Tests Added Or Changed

| Test or proof surface | What it proves | Why this level is appropriate |
|---|---|---|
| `python scripts/test-artifact-lifecycle-validator.py` | `docs/examples/plans/example-plan.md` is not treated as active lifecycle state. | The behavior is selector/lifecycle classification, so validator tests are direct. |
| `python scripts/test-select-validation.py` | `docs/examples/**` routes as examples rather than active lifecycle artifacts. | Prevents future routing regressions for examples. |
| `python scripts/test-change-metadata-validator.py` | Retaining `docs/changes/0001-skill-validator/` as a fixture remains valid. | The retained fixture is validator-owned and intentionally not moved in this slice. |
| `python scripts/test-skill-validator.py` | Formal review skills contain the recording-status contract and exclude exact status-sync result fields. | Static skill text is the changed behavior surface. |
| `python scripts/build-skills.py --check` | `.codex/skills/**` mirrors match canonical skills. | Generated local runtime output must not drift. |
| `python scripts/build-adapters.py --version 0.1.1 --check` | Public adapter output matches canonical sources for version `0.1.1`. | Adapter output is generated and must be reproducible. |
| `python scripts/validate-adapters.py --version 0.1.1` and `python scripts/test-adapter-distribution.py` | Adapter package structure, manifests, aliases, and release metadata behavior remain valid. | Adapter distribution behavior is broader than file drift. |
| Manual generated-output `rg` proof | Generated review skills contain recording guidance and omit exact forbidden status-sync fields. | Complements drift checks with direct evidence for the central user-facing behavior. |

## Validation Evidence Available Before Final Verify

Validation recorded in the active plan and change metadata includes:

- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/test-select-validation.py`
- `python scripts/test-change-metadata-validator.py`
- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/build-adapters.py --version 0.1.1`
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/validate-adapters.py --version 0.1.1`
- `python scripts/test-adapter-distribution.py`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/change.yaml`
- scoped `git diff --check -- ...` commands for changed surfaces.

Notable expected failures were also recorded before M3 generation:

- `python scripts/build-skills.py --check` failed because five generated Codex review skill mirrors were stale.
- `python scripts/build-adapters.py --version 0.1.1 --check` failed because 15 adapter review skill files were stale.

Both failures were resolved by running the repository-owned generators.

Hosted CI and final `verify` have not run in this stage.

## Review Resolution Summary

Review-resolution surface: `docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/review-resolution.md`.

- Material findings: 1 total.
- Accepted: 1 (`SR-001` from `spec-review-r1`).
- Rejected: 0.
- Deferred: 0.
- Needs decision: 0.
- Closeout status: closed.

`SR-001` required the normative change-ID selection rule to live in `specs/formal-review-recording.md`. The spec and test spec were updated, and `spec-review-r2` approved the result with no material findings.

## Alternatives Rejected

- Review-side artifact-status sync was rejected for this slice because it made review skills responsible for lifecycle settlement. The approved split keeps review skills focused on evidence recording and leaves downstream settlement for follow-up design.
- Duplicating the full change-ID algorithm and long `Location` examples into every review skill was rejected. The spec owns the normative rule, examples live under `docs/examples/formal-review-recording/`, and skills carry only a concise pointer.
- Moving `docs/changes/0001-skill-validator/` was rejected for this slice because it remains a repo-owned validator fixture and historical proof pack with existing compatibility references.
- Hand-editing generated `.codex/skills` or `dist/adapters` output was rejected. Generated output was refreshed through `scripts/build-skills.py` and `scripts/build-adapters.py --version 0.1.1`.

## Scope Control

Preserved non-goals:

- No downstream upstream-status settlement was implemented.
- No standardized review-side `Status sync`, `Status artifact`, `Status sync blocker`, or `Status settlement recommendation` fields were added to formal review skills.
- No new review stage was created.
- Clean reviews with no material findings remain lightweight.
- Long examples were kept out of public skill bodies.
- Generated output was regenerated from canonical sources rather than hand-edited.

## Risks And Follow-Ups

- Public review skills are longer because they now include recording-status output obligations. The shared block keeps the growth consistent and testable.
- Static checks prove the skill wording is present; they do not guarantee a future agent will always create the artifacts at runtime. The spec keeps runtime/output validation as a possible later escalation if the lapse recurs.
- Downstream upstream-status settlement remains follow-up scope. A future proposal should define which downstream skills participate, what evidence is sufficient, and which lifecycle fields may be minimally edited.

## Readiness

This explanation completes the durable rationale surface for the change-local pack.

Next stage: `verify`.
