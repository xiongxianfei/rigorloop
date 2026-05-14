# Explain Change: Stage Evidence Access Contracts for Cost-Bounded Rigor

## Summary

M1 adds a stage evidence access model for proposal-side workflow work. The change makes `docs/workflows.md` the shared operating guide for default evidence, conditional evidence, expansion evidence, bounded discovery, and full-file-read escape behavior.

It also updates `proposal` and `proposal-review` with concise stage-local evidence-access sections and adds concept-level static proof. `spec` was intentionally left unchanged because its existing upstream-status and bounded-evidence behavior is sufficient for immediate proposal-to-spec handoff.

## Problem

RigorLoop skills had broad lists of possibly relevant artifacts but did not consistently tell agents which smallest evidence set to read first. That created token waste and workflow amplification from broad searches, repeated artifact reads, and early over-collection before a stage knew what it needed to prove.

## Decision Trail

| Source | Decision |
|---|---|
| Proposal | Adopt the default evidence + conditional evidence + justified expansion + bounded-read model instead of a hard allow-list. |
| Proposal review | Split validation guidance into M1 and M2 command groups so M1 does not select deferred `implement` and `code-review` paths. |
| Spec | M1 must update `docs/workflows.md`, `proposal`, and `proposal-review`; `spec` is optional only if immediate handoff needs it; `implement`, `code-review`, and `plan` are out of M1. |
| Plan | Implement the shared model, proposal-side local guidance, optional `spec` no-change rationale, input classification, concept checks when stable, and scoped validation. |
| Test spec | Prove shared model, proposal/proposal-review local guidance, bounded discovery boundary, optional `spec` boundary, M1/M2 validation separation, input preservation, and diagnostic token measurement. |
| Review resolution | `SEA-PR-1` split M1/M2 validation guidance; `SEA-M1-CR1-1` removed an unrelated M5 plan-index transition from the M1 diff. |

Architecture was not required because the approved spec changes workflow and skill guidance only, with no runtime architecture, persistence, API, data, release, or adapter boundary change.

## Diff Rationale by Area

| File | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `docs/workflows.md` | Added `Stage Evidence Access`. | Centralizes the shared model: default evidence, conditional evidence, expansion evidence, bounded discovery, reason recording, full-file escape, and M1/M2 validation split. | Spec `R1`, `R5`-`R15`, `R27`-`R29`. | `test_stage_evidence_access_contract_guidance`; T1, T5, T7. |
| `skills/proposal/SKILL.md` | Added concise `Evidence access` guidance and reclassified inputs as standing instructions or task evidence. | Gives proposal authors a smallest sufficient starting set while preserving governance, vision, related proposal, workflow, code, and orientation triggers. | Spec `R2`, `R6`-`R9`, `R16`-`R20`. | `test_stage_evidence_access_proposal_side_skills`; T2, T8. |
| `skills/proposal-review/SKILL.md` | Added concise `Evidence access` guidance and reclassified inputs. | Gives proposal reviewers a bounded default set and trigger-based expansion without weakening standing gates or review rigor. | Spec `R2`, `R6`-`R9`, `R16`-`R18`, `R21`-`R22`. | `test_stage_evidence_access_proposal_side_skills`; T2, T8. |
| `scripts/test-skill-validator.py` | Added concept checks for the shared workflow model and proposal-side skill sections. | Provides stable static proof without exact long paragraph locks or broad semantic scoring. | Spec `R30`-`R31`. | `python scripts/test-skill-validator.py`. |
| `docs/proposals/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md` | Added and revised the accepted proposal. | Preserves the direction, scope split, and proposal-review resolution trail. | Proposal-review `SEA-PR-1`. | Proposal-review records and lifecycle validation. |
| `specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md` | Added approved behavior contract. | Defines the M1/M2 boundary, requirements, edge cases, compatibility, and non-goals. | Accepted proposal and clean spec-review. | `spec-review-r1`; lifecycle validation. |
| `specs/stage-evidence-access-contracts-for-cost-bounded-rigor.test.md` | Added active test spec. | Maps requirements and edge cases to static, lifecycle, selected-validation, and manual proof. | Approved spec and reviewed plan. | Test-spec approval and lifecycle validation. |
| `docs/plans/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md` | Added and updated active plan state through M1 closeout. | Keeps current milestone state, input classification, no-`spec` rationale, validation notes, and review status reconstructable. | Plan-review and implement/code-review stages. | Artifact lifecycle validation. |
| `docs/plan.md` | Indexed the active stage evidence plan and updated its current summary. | Keeps the plan index synchronized with the active plan body. | Workflow state ownership rules. | Artifact lifecycle validation. |
| `docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/**` | Added change metadata, review log, review-resolution, proposal/spec/plan/code-review records. | Records formal review evidence, material findings, accepted dispositions, validation evidence, and clean review receipts. | Formal review recording rules; spec `R34`. | Review-artifact and change-metadata validation. |

## Tests Added or Changed

| Test/proof | What it proves | Why this level fits |
|---|---|---|
| `test_stage_evidence_access_contract_guidance` | `docs/workflows.md` contains the shared model, bounded discovery boundary, expansion reason rule, full-file escape, and M1/M2 validation split. | Static concept proof is appropriate because M1 changes guidance text, not runtime behavior. |
| `test_stage_evidence_access_proposal_side_skills` | `proposal` and `proposal-review` contain concise local default/conditional evidence guidance and expansion/full-file behavior. | Static concept proof avoids brittle exact paragraph locks while proving required guidance is present. |
| Manual no-`spec` rationale in the active plan | `skills/spec/SKILL.md` was intentionally not updated in M1. | The test spec allows manual review because semantic handoff sufficiency would be brittle to automate. |
| Review-artifact and lifecycle validators | Review records, material finding dispositions, active plan state, and change metadata are coherent. | Lifecycle integrity is part of the workflow contract for non-trivial changes. |
| Static token measurement | Canonical skill size impact was measured as diagnostic evidence. | The approved spec requires measurement to remain warning-only, not a hard gate. |

## Validation Evidence Available Before Final Verify

- `python scripts/test-skill-validator.py` failed before guidance edits for the new checks, then passed after implementation.
- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md`
- `python scripts/build-skills.py --check`
- `python scripts/test-build-skills.py`
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md`
- `python scripts/test-select-validation.py`
- `python scripts/measure-skill-tokens.py`
- Review-resolution fix validation for `SEA-M1-CR1-1`: change metadata validation, artifact lifecycle validation, and scoped `git diff --check --`.
- `code-review-m1-r3` clean-with-notes for the current tracked M1 branch state.

Static token measurement reported 23 skills, 233054 bytes, and 58252 estimated tokens. `proposal` measured 3047 estimated tokens and `proposal-review` measured 3110 estimated tokens. This is diagnostic only.

Hosted CI has not been observed for this branch.

## Review Resolution Summary

Review resolution: [review-resolution.md](review-resolution.md)

Material findings:

| Finding | Disposition | Result |
|---|---|---|
| `SEA-PR-1` | accepted | Proposal validation guidance was split into scoped M1 and M2 command groups. |
| `SEA-M1-CR1-1` | accepted | An unrelated M5 plan-index transition was removed from the M1 diff; clean code-review reruns followed. |

No `needs-decision` findings remain. `review-log.md` records no open findings.

## Alternatives Rejected

- Hard allow-lists were rejected because `implement` and `code-review` need richer evidence in normal work.
- Updating `implement`, `code-review`, or `plan` in M1 was rejected because the approved scope defers execution/review evidence access to M2.
- Updating `skills/spec/SKILL.md` was rejected for M1 because the existing `spec` skill already requires accepted proposal input, upstream status settlement, review-resolution handling, bounded evidence, and full-file-read escape behavior.
- Runtime enforcement, semantic read auditing, hard token gates, dynamic benchmarks, release validation changes, adapter packaging changes, generated-output source changes, and lifecycle token-cost summary work were rejected as out of scope.
- Exact long prose checks were rejected in favor of concept-based static proof.

## Scope Control

M1 changed only the shared workflow guide, proposal-side skills, stable static proof, and lifecycle/review artifacts. It did not modify `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, `skills/plan/SKILL.md`, or `skills/spec/SKILL.md`.

The separate M5 plan closeout commit is not part of this stage evidence access rationale.

## Risks and Follow-Ups

- Final `verify` still needs to run before PR handoff.
- Hosted CI is not yet observed for this branch.
- M2 execution/review evidence access remains future work for `implement` and `code-review`.
- The guidance relies on agents following the evidence expansion rule; semantic runtime read auditing remains intentionally out of scope.
