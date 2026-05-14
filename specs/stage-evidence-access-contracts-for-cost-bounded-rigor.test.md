# Stage Evidence Access Contracts for Cost-Bounded Rigor Test Spec

## Status

active

## Approval

Maintainer-approved on 2026-05-14 by direct user request. Status remains `active` because this test spec is the relied-on proof-planning surface for M1 implementation and M2 execution/review evidence access.

M2 alignment approved on 2026-05-14 by direct user request after `M1: align stage evidence access M2 test spec`.

M3/M4 alignment drafted on 2026-05-15 for the plan-review-approved static validation and measurement follow-through. Maintainer approval remains the handoff before implementation relies on the M3/M4 alignment.

## Related spec and plan

- Spec: [Stage Evidence Access Contracts for Cost-Bounded Rigor](stage-evidence-access-contracts-for-cost-bounded-rigor.md)
- M1 plan: [Stage Evidence Access Contracts for Cost-Bounded Rigor](../docs/plans/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md)
- M2 plan: [Stage Evidence Access Contracts M2: Execution/Review Evidence Access](../docs/plans/2026-05-14-stage-evidence-access-contracts-m2-execution-review.md)
- M3/M4 plan: [Stage Evidence Access Contracts M3/M4: Static Validation And Measurement](../docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md)

## Testing strategy

Use focused static and lifecycle validation for this guidance-only change.

- Static/unit: `scripts/test-skill-validator.py` covers stable wording and scope-boundary assertions when implementation adds or updates concept checks.
- Contract/static: direct inspection of `docs/workflows.md` and selected skill text proves evidence-access sections, default/conditional guidance, bounded discovery, expansion reasons, full-file-read escape behavior, and M1/M2 validation separation.
- Integration/selector: `scripts/select-validation.py --mode explicit` proves M1 path selection excludes deferred M2 surfaces and M2 path selection includes `implement` and `code-review` without unrelated skill edits.
- Lifecycle: `scripts/validate-artifact-lifecycle.py`, `scripts/validate-change-metadata.py`, and `scripts/validate-review-artifacts.py` prove proposal/spec/plan/change-local state remains coherent.
- Measurement: `scripts/measure-skill-tokens.py` records diagnostic static token impact after canonical skill changes.
- Manual review: verifies migration rationale and optional `spec` no-change rationale when automation would require brittle semantic scoring.
- M3/M4 follow-through: implementation first audits existing concept checks before adding assertions, then records static skill token measurement and size delta as diagnostic evidence only.

No runtime, e2e, browser, release, adapter, migration-data, or hosted observability tests are required because the approved spec changes repository guidance and skill contracts only.

## Requirement coverage map

| Requirement | Tests |
|---|---|
| R1 | T1, T6 |
| R2 | T2, T6 |
| R3 | T3, T7 |
| R4 | T4, T7 |
| R5 | T1, T12, T13 |
| R6 | T1, T2, T12, T13 |
| R7 | T1, T2, T12, T13 |
| R8 | T1, T2, T5, T12, T13 |
| R9 | T1, T5, T12, T13 |
| R10 | T1, T5, T12, T13 |
| R10a | T1, T5, T12, T13 |
| R11 | T1, T5, T12, T13 |
| R12 | T1, T5, T12, T13 |
| R13 | T1, T2, T12, T13 |
| R14 | T1, T2, T12, T13 |
| R15 | T1, T2, T12, T13 |
| R16 | T8, T12, T13 |
| R17 | T8, T12, T13 |
| R18 | T8, T12, T13 |
| R19 | T2 |
| R20 | T2 |
| R21 | T2 |
| R22 | T2 |
| R23 | T3 |
| R24 | T3 |
| R25 | T4, T7 |
| R26 | T4, T7, T12, T13 |
| R27 | T7 |
| R28 | T7 |
| R29 | T7, T14 |
| R30 | T6, T12, T13, T15 |
| R31 | T6, T12, T13, T15 |
| R32 | T4, T9, T14, T15, T16 |
| R33 | T10, T14, T16 |
| R34 | T9, T11, T12, T13, T14, T15, T16 |

## Example coverage map

| Example | Tests |
|---|---|
| E1 | T2 |
| E2 | T5 |
| E3 | T5 |
| E4 | T8, T12, T13 |
| E5 | T7, T14 |

## Edge case coverage

| Edge case | Tests |
|---|---|
| 1. Line-number search is bounded discovery | T5 |
| 2. Out-of-set ADR content read is expansion | T5 |
| 3. `AGENTS.md` or `CONSTITUTION.md` input classification | T8, T12, T13 |
| 4. M1 tries to edit `implement` | T4, T7 |
| 5. M1 updates `spec` | T3, T7 |
| 6. M2 runs later | T7, T12, T13, T14 |
| 7. Static checks are concept-based | T6, T15 |
| 8. Token measurement increase is diagnostic | T10, T16 |
| 9. Contradictory bounded evidence expands | T1, T12, T13 |
| 10. Full file is review target | T1, T12, T13 |

## Test cases

### T1. Shared Workflow Evidence Model

- Covers: R1, R5-R15, edge cases 1, 2, 9, 10
- Level: static
- Fixture/setup: changed `docs/workflows.md`
- Steps:
  1. Inspect the new stage evidence access model in `docs/workflows.md`.
  2. Confirm it defines default evidence, conditional evidence, expansion evidence, and broad/full-file behavior.
  3. Confirm it distinguishes bounded discovery from substantive out-of-set reads.
  4. Confirm it preserves do-not-under-read and full-file-read escape behavior.
- Expected result: `docs/workflows.md` contains the shared model and does not make bounded evidence a reason to under-read.
- Failure proves: The central operational model is missing, incomplete, or unsafe.
- Automation location: `scripts/test-skill-validator.py` if stable static checks are added; otherwise manual review plus artifact lifecycle validation.

### T2. Proposal And Proposal-Review Local Evidence Guidance

- Covers: R2, R6-R9, R13-R15, R19-R22, E1
- Level: static
- Fixture/setup: changed `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md`
- Steps:
  1. Inspect `proposal` for default and conditional evidence guidance.
  2. Inspect `proposal-review` for default and conditional evidence guidance.
  3. Confirm both discourage broad authoritative-document searches for path/state discovery.
  4. Confirm both preserve expansion and full-file-read escape behavior without copying excessive shared wording.
- Expected result: both skills contain concise stage-local evidence-access guidance that matches their required default and conditional categories.
- Failure proves: M1 did not implement proposal-side evidence guidance or duplicated the shared model excessively.
- Automation location: `scripts/test-skill-validator.py` if stable concept checks are added; otherwise manual review.

### T3. Optional Spec Skill Boundary

- Covers: R3, R23, R24, edge case 5
- Level: static
- Fixture/setup: implementation decision on `skills/spec/SKILL.md`
- Steps:
  1. If `skills/spec/SKILL.md` changes, inspect it for accepted-proposal, latest proposal-review, review-resolution, and related-spec default evidence.
  2. Confirm conditional architecture/ADR, workflow-doc, code, and constitution reads are trigger-based.
  3. If `skills/spec/SKILL.md` does not change, inspect tracked implementation rationale for why immediate proposal-to-spec handoff did not need it.
- Expected result: `spec` is either updated with scoped evidence guidance or explicitly left unchanged with rationale.
- Failure proves: optional M1 `spec` scope was mishandled.
- Automation location: manual review; selected validation includes `skills/spec/SKILL.md` only if changed.

### T4. M1 Forbidden Surface Boundary

- Covers: R4, R25, R26, R32, edge case 4
- Level: integration
- Fixture/setup: implementation diff
- Steps:
  1. Inspect changed paths.
  2. Confirm M1 does not edit `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, or `skills/plan/SKILL.md`.
  3. Confirm no runtime enforcement, semantic read auditing, hard token gates, lifecycle token summaries, release validation changes, adapter packaging changes, or generated-output source model changes appear in the diff.
- Expected result: M1 changed paths stay within approved M1 scope.
- Failure proves: M1 absorbed deferred or out-of-scope work.
- Automation location: `git diff --name-only`, `scripts/select-validation.py --mode explicit`, and code-review.

### T5. Evidence Expansion Boundary

- Covers: R8-R12, E2, E3, edge cases 1, 2
- Level: static
- Fixture/setup: changed `docs/workflows.md` and selected skill text
- Steps:
  1. Confirm bounded discovery examples include path inventory, heading scan, line-number search, count query, targeted diff summary, and metadata lookup.
  2. Confirm bounded discovery does not require an evidence-expansion record.
  3. Confirm substantive out-of-set reads require a compact reason.
  4. Confirm `Evidence expansion` output appears only when expansion occurred.
- Expected result: the boundary is explicit and lightweight.
- Failure proves: the model either under-records substantive expansion or over-logs harmless discovery.
- Automation location: `scripts/test-skill-validator.py` if stable concept checks are added; otherwise manual review.

### T6. Concept-Based Static Proof

- Covers: R30, R31
- Level: unit
- Fixture/setup: `scripts/test-skill-validator.py`, if updated
- Steps:
  1. Inspect any new static checks.
  2. Confirm checks use stable sections, concepts, or short phrases.
  3. Confirm checks do not require exact long paragraphs or broad natural-language scoring.
- Expected result: static proof is narrow and reviewable.
- Failure proves: validation became brittle or semantic-scoring-based.
- Automation location: `scripts/test-skill-validator.py`.

### T7. M1 And M2 Validation Separation

- Covers: R27-R29, E5, edge cases 4, 5, 6
- Level: integration
- Fixture/setup: changed M1 paths
- Steps:
  1. Run `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md`.
  2. If `skills/spec/SKILL.md` changes, rerun with `--path skills/spec/SKILL.md` included.
  3. Confirm M1 selected validation does not require `skills/implement/SKILL.md` or `skills/code-review/SKILL.md`.
  4. Confirm the plan/test spec keep M2 validation separate for later `implement` and `code-review` paths.
- Expected result: selected validation is scoped to M1 and excludes M2 skill paths.
- Failure proves: validation scope reintroduces workflow amplification.
- Automation location: `scripts/select-validation.py --mode explicit`.

### T8. Input Contract Preservation

- Covers: R16-R18, E4, edge case 3
- Level: manual
- Fixture/setup: changed skill inputs
- Steps:
  1. For each touched skill with input guidance removed, downgraded, or reclassified, inspect the migration table or equivalent review-visible note.
  2. Confirm each changed input is classified as standing operating instructions, default task evidence, conditional task evidence, expansion evidence, or obsolete/duplicated guidance.
  3. Confirm any removal or downgrade has rationale.
- Expected result: no existing mandatory operating input is silently weakened.
- Failure proves: cost reduction introduced unsafe under-reading.
- Automation location: manual review in plan/code-review/explain-change evidence.

### T9. Safety-Critical And Out-Of-Scope Behavior Preservation

- Covers: R32, R34
- Level: manual
- Fixture/setup: implementation diff and changed artifacts
- Steps:
  1. Inspect changed artifacts for review, verify, PR, material-finding, source-of-truth, release, and adapter guidance changes.
  2. Confirm any touched safety-critical guidance is preserved or explicitly outside the diff.
  3. Confirm no release or generated-output source model changes are introduced.
- Expected result: safety-critical workflow behavior remains intact.
- Failure proves: M1 weakened or broadened protected workflow behavior.
- Automation location: code-review and final verify.

### T10. Static Token Measurement Is Diagnostic

- Covers: R33, edge case 8
- Level: smoke
- Fixture/setup: canonical skill changes
- Steps:
  1. Run `python scripts/measure-skill-tokens.py` after canonical skill edits.
  2. Record the result in validation notes or explain-change.
  3. Confirm no hard token gate is introduced.
- Expected result: token measurement evidence exists and remains warning-only.
- Failure proves: token impact was not measured or became an unintended hard gate.
- Automation location: `scripts/measure-skill-tokens.py`.

### T11. Lifecycle And Review Evidence Coherence

- Covers: R34 and artifact lifecycle requirements
- Level: integration
- Fixture/setup: lifecycle and change-local artifacts
- Steps:
  1. Run review-artifact validation for the change root.
  2. Run change-metadata validation.
  3. Run artifact lifecycle validation for proposal, spec, test spec, plan, plan index, and change metadata.
  4. Run `git diff --check -- <changed paths>`.
- Expected result: lifecycle artifacts remain coherent and review evidence remains closed.
- Failure proves: implementation evidence cannot be trusted for downstream handoff.
- Automation location:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
  - `git diff --check -- <changed paths>`

### T12. Implement Local Evidence Guidance

- Covers: R5-R18, R26, R30-R34, E4, edge cases 3, 6, 9, 10
- Level: static
- Fixture/setup: changed `skills/implement/SKILL.md` and M2 input-classification notes
- Steps:
  1. Inspect `implement` for a concise `Evidence access` section.
  2. Confirm default evidence includes active plan `Current Handoff Summary`, current milestone section, approved spec, test spec, code/tests named by the milestone, and milestone validation commands.
  3. Confirm conditional evidence includes architecture/ADR when architecture boundaries are touched, review-resolution when accepted findings are being implemented, `docs/workflows.md` when routing or artifact placement is ambiguous, `CONSTITUTION.md` when governance/source-of-truth/safety constraints matter, and neighboring files when existing patterns are needed.
  4. Confirm it records a compact reason only for substantive out-of-set reads and does not require evidence-expansion output for default evidence, triggered conditional evidence, or bounded discovery.
  5. Confirm the section preserves full-file-read escape behavior and the do-not-under-read invariant.
  6. Inspect M2 input-classification notes for standing operating instructions, default task evidence, conditional task evidence, expansion evidence, or obsolete/duplicated guidance.
- Expected result: `implement` has stage-local evidence guidance without weakening handoff inspection, first-pass completeness, validation layering, plan-update ownership, or milestone handoff behavior.
- Failure proves: M2 weakened implementation safety, over-logged bounded discovery, or omitted required implementation-stage evidence categories.
- Automation location: `scripts/test-skill-validator.py` if stable concept checks are added; otherwise manual review plus lifecycle/change metadata validation.

### T13. Code-Review Local Evidence Guidance

- Covers: R5-R18, R26, R30-R34, E4, edge cases 3, 6, 9, 10
- Level: static
- Fixture/setup: changed `skills/code-review/SKILL.md` and M2 input-classification notes
- Steps:
  1. Inspect `code-review` for a concise `Evidence access` section.
  2. Confirm default evidence includes actual diff or changed files, approved spec, test spec, current plan milestone, validation evidence, and relevant tests.
  3. Confirm conditional evidence includes architecture/ADR when architecture is touched, review-resolution when reviewing fixes, change metadata when lifecycle state or review closeout matters, `CONSTITUTION.md` when source-of-truth/governance/safety boundaries matter, and related code paths when the diff depends on them.
  4. Confirm it records a compact reason only for substantive out-of-set reads and does not require evidence-expansion output for default evidence, triggered conditional evidence, or bounded discovery.
  5. Confirm the section preserves full-file-read escape behavior and the do-not-under-read invariant.
  6. Inspect M2 input-classification notes for standing operating instructions, default task evidence, conditional task evidence, expansion evidence, or obsolete/duplicated guidance.
- Expected result: `code-review` has stage-local evidence guidance without weakening independent-review mode, actual-diff grounding, material-finding requirements, review-resolution handoff, first-pass checklist coverage, or milestone-aware routing.
- Failure proves: M2 weakened review rigor, over-logged bounded discovery, or omitted required review-stage evidence categories.
- Automation location: `scripts/test-skill-validator.py` if stable concept checks are added; otherwise manual review plus lifecycle/change metadata validation.

### T14. M2 Selected Validation And Lifecycle Coherence

- Covers: R29, R32-R34, E5, edge case 6
- Level: integration
- Fixture/setup: changed M2 paths
- Steps:
  1. Run `python scripts/select-validation.py --mode explicit --path skills/implement/SKILL.md --path skills/code-review/SKILL.md`.
  2. Confirm M2 selected validation covers the execution/review skill paths and does not require unrelated `skills/plan/SKILL.md` or `skills/spec/SKILL.md` edits.
  3. Run concept checks, skill validation, generated-skill mirror checks, adapter archive smoke checks when selected, change metadata validation, artifact lifecycle validation, and `git diff --check -- <changed paths>`.
  4. Run `python scripts/measure-skill-tokens.py` and record the result as diagnostic only.
- Expected result: M2 validation proves the touched execution/review skill guidance, lifecycle artifacts, and token measurement without introducing runtime enforcement, release behavior changes, adapter packaging changes, generated-output source changes, or hard token gates.
- Failure proves: M2 validation is too broad, too narrow, missing lifecycle proof, or turned token measurement into a hard gate.
- Automation location:
  - `python scripts/select-validation.py --mode explicit --path skills/implement/SKILL.md --path skills/code-review/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-build-skills.py`
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`
  - `python scripts/measure-skill-tokens.py`
  - lifecycle, review-artifact, change-metadata, and diff checks named by the active plan

### T15. M3 Static Validation Audit And Gap Fill

- Covers: R30-R32, R34, edge case 7
- Level: unit
- Fixture/setup: current `scripts/test-skill-validator.py`, existing stage evidence access checks, and M3 plan/change-local evidence
- Steps:
  1. Inspect `test_stage_evidence_access_contract_guidance`, `test_stage_evidence_access_proposal_side_skills`, and `test_stage_evidence_access_m2_execution_review_skills`.
  2. Map existing coverage against the M3 concept list: `Evidence access`, default evidence, conditional evidence, reason recording, bounded evidence before broad reads, and full-file-read escape behavior.
  3. If a concept is missing, add the smallest stable assertion needed to protect it.
  4. If coverage is already sufficient, record a no-change rationale in the active plan and change metadata instead of adding duplicate checks.
  5. Run `python scripts/test-skill-validator.py` and selected lifecycle validation for touched surfaces.
- Expected result: M3 either adds focused concept-level static checks or records a reviewed no-change rationale that existing checks already protect the guidance.
- Failure proves: static validation is missing required concept protection, became brittle, or added unnecessary duplicate checks.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/select-validation.py --mode explicit --path scripts/test-skill-validator.py --path docs/plans/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement.md --path docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/change.yaml`
  - lifecycle, change-metadata, and diff checks named by the active M3/M4 plan

### T16. M4 Static Measurement And Size-Delta Recording

- Covers: R32-R34, edge case 8
- Level: smoke
- Fixture/setup: M2 merged baseline of 23 skills, 235521 bytes, and 58868 estimated tokens; current canonical skill set after M3
- Steps:
  1. Run `python scripts/measure-skill-tokens.py`.
  2. Compare the result against the M2 merged baseline.
  3. If M3 changed canonical skill text, record per-skill deltas for touched skills.
  4. If M3 changed only validator or lifecycle artifacts, record that static skill size is expected to remain unchanged and verify the measurement result.
  5. Record the measurement and increase/decrease/unchanged statement in plan validation notes and change metadata; summarize it later in explain-change.
  6. Confirm no hard token threshold, runtime enforcement, dynamic benchmark requirement, release validation change, adapter packaging change, or generated-output source-model change was introduced.
- Expected result: M4 records diagnostic static skill size evidence and size-delta interpretation without turning token totals into a release or implementation gate.
- Failure proves: measurement was skipped, stale, misinterpreted as a hard gate, or broadened into excluded dynamic/release/adapter work.
- Automation location:
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - lifecycle, change-metadata, and diff checks named by the active M3/M4 plan

## Fixtures and data

- Existing `docs/workflows.md`.
- Existing canonical skills under `skills/proposal/`, `skills/proposal-review/`, optionally `skills/spec/`, and M2 skills under `skills/implement/` and `skills/code-review/`.
- Existing validation scripts:
  - `scripts/test-skill-validator.py`
  - `scripts/validate-skills.py`
  - `scripts/select-validation.py`
  - `scripts/measure-skill-tokens.py`
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/validate-review-artifacts.py`
  - `scripts/validate-change-metadata.py`
- M1 change root: `docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/`
- M2 change root: `docs/changes/2026-05-14-stage-evidence-access-contracts-m2-execution-review/`
- M3/M4 change root: `docs/changes/2026-05-15-stage-evidence-access-contracts-m3-m4-validation-measurement/`
- M3/M4 static measurement baseline: M2 merged result of 23 skills, 235521 bytes, and 58868 estimated tokens.

No generated adapter fixtures, release archives, runtime data, or external services are required.

## Mocking/stubbing policy

No mocks or stubs are required. This is a static repository-guidance change.

## Migration or Compatibility Tests

- Covered by T4, T8, T9, and T11.
- No historical artifact backfill or data migration tests are required.

## Observability verification

- Covered by T11 and validation-note review.
- No runtime logs, metrics, traces, or audit events are required.

## Security/privacy verification

- Covered by T9.
- Review should confirm guidance prefers targeted excerpts and does not encourage dumping secrets, private logs, credentials, or irrelevant large excerpts.

## Performance checks

- Covered by T10.
- Static token measurement is diagnostic only; no hard threshold is introduced.
- M4 size-delta recording is covered by T16 and remains diagnostic only.

## Manual QA checklist

- [ ] Confirm `docs/workflows.md` owns the shared model.
- [ ] Confirm `proposal` and `proposal-review` guidance is concise and stage-local.
- [ ] Confirm `spec` is updated only if needed, or has no-change rationale.
- [ ] Confirm no M1 edits to `implement`, `code-review`, or `plan`.
- [ ] Confirm input migration rationale exists for any removed, downgraded, or reclassified input guidance.
- [ ] Confirm selected validation excludes M2 paths.
- [ ] Confirm token measurement was run after canonical skill edits.
- [ ] Confirm `implement` includes M2 evidence guidance and preserves handoff inspection, first-pass completeness, validation layering, plan-update ownership, and milestone handoff behavior.
- [ ] Confirm `code-review` includes M2 evidence guidance and preserves independent-review mode, actual-diff grounding, material-finding requirements, review-resolution handoff, checklist coverage, and milestone-aware routing.
- [ ] Confirm M2 selected validation covers `skills/implement/SKILL.md` and `skills/code-review/SKILL.md` without requiring unrelated `plan` or `spec` skill edits.
- [ ] Confirm M3 audits existing static concept coverage before adding checks.
- [ ] Confirm any M3 no-change rationale is recorded in the active plan and change metadata.
- [ ] Confirm M4 static measurement compares against the M2 merged baseline and records increase/decrease/unchanged.
- [ ] Confirm M4 measurement remains diagnostic and does not introduce hard token gates or dynamic benchmarks.

## What not to test

- Do not run release or adapter validation unless implementation touches release or adapter surfaces.
- Do not run dynamic token benchmarks unless a later approved plan or test-spec revision requires them.
- Do not test runtime enforcement or semantic read auditing; those are out of scope.
- Do not test M2 `implement` or `code-review` evidence guidance in M1.
- Do not test or require `plan` evidence guidance in M2.
- Do not add new skill evidence guidance solely for M3/M4.
- Do not run release validation, adapter validation, or dynamic token benchmarks for M3/M4 unless later selected validation requires them because touched paths changed.
- Do not require exact long wording matches across skills.

## Uncovered gaps

None.

## Next artifacts

```text
maintainer approval for M3/M4 test-spec alignment
implement M3. Static Validation Audit And Gap Fill
implement M4. Measurement And Size-Delta Recording
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet.

## Readiness

Active proof surface for M3/M4 implementation after maintainer approval. The active plan `Current Handoff Summary` owns the next workflow action.
