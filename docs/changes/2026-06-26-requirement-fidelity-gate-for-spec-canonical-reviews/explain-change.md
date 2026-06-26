# Requirement-Fidelity Gate Explain Change

## Summary

This change adds a requirement-fidelity layer to automated reviews so reviewers and validators compare implementation surfaces against the complete normative spec, not merely against each other. It is an additive sibling to the independent adversarial review gates: independence protects against anchoring, while requirement fidelity protects against requirement compression.

The concrete trigger was the M2 review miss where `specs/test-spec-review-gate.md` R26 required `approved + current + recorded`, but the implementation, validator, and review only carried `approved + current`.

## Problem

The accepted proposal identifies a recurring failure mode:

```text
Spec says A + B + C.
Implementation or validator carries only A + B.
Review confirms implementation and validator agree.
The missing C is not rediscovered.
```

The independence gates remained valuable, but they did not force the review comparison point to be the full spec. This change makes the spec-canonical property list explicit in review records, validators, lifecycle gates, and calibration evidence.

## Decision Trail

| Decision source | Outcome |
| --- | --- |
| Proposal | Treat requirement compression as distinct from review anchoring; preserve independent-review gates; avoid finding quotas. |
| Spec | Requirements `R1`-`R50` define deterministic applicability, spec-first packet ordering, decomposition receipts, validator matrices, calibration sampling, generated-output proof, and compatibility preservation. |
| Architecture/ADR | Requirement-fidelity remains a repository-local workflow/validator layer; no new service, persistence engine, queue, or external API is introduced. |
| Plan | Five milestones: guidance, validator/lifecycle gates, R26 matrix pilot, compression calibration, and generated-output/behavior-preservation closeout. |
| Reviews | Five material findings were accepted and resolved; final `code-review-r7` closed all implementation milestones. |

## Diff Rationale By Area

| Area | Representative files | Why changed | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| Requirement-fidelity contract | `specs/requirement-fidelity-gate.md`, `specs/requirement-fidelity-gate.test.md` | Defines applicability, decomposition, receipt, validator, calibration, and preservation contracts. | Proposal; `R1`-`R50`; `AC-RFG-001`-`AC-RFG-020` | Spec-review R2; test-spec-review R2 |
| Review and workflow guidance | `skills/code-review/SKILL.md`, `skills/workflow/SKILL.md`, `skills/implement/SKILL.md`, adjacent review skills, `docs/workflows.md` | Teaches spec-first packet ordering, requirement-property decomposition, fidelity receipts, AND semantics with independence gates, and manual-review first-slice boundaries. | `R1`-`R3`, `R9`-`R23`, `R30`-`R40` | `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py` |
| Review-artifact validation | `scripts/review_artifact_validation.py`, `scripts/test-review-artifact-validator.py` | Enforces requirement-fidelity manifests, clean-review receipts, closed vocabularies, calibration records, seeded compression defects, and corrective-action semantics. | `R4`-`R13`, `R17`-`R17d`, `R30`-`R45c`, `R48` | `python scripts/test-review-artifact-validator.py` |
| Lifecycle and metadata gates | `scripts/lifecycle_state_sync.py`, `scripts/test-artifact-lifecycle-validator.py`, `scripts/change_metadata_semantics.py`, `scripts/validate-change-metadata.py`, `scripts/test-change-metadata-validator.py` | Prevents workflow-managed clean review continuation without fidelity applicability and receipt evidence; keeps lifecycle state synchronized. | `R3`-`R8`, `R30`-`R34`, `R46`, `R50` | lifecycle and change-metadata validator suites |
| R26 property matrix pilot | `scripts/test-skill-validator.py`, `tests/fixtures/requirement-fidelity-gate/representative-reviews/r26-matrix-pilot/spec-read-log.json` | Adds the canonical `approved/current/recorded` property-list by required-surface matrix and bounded spec-read proof. | `R24`-`R29`, `R43`, `AC-RFG-009`-`AC-RFG-012` | M3 code-review R4; skill-validator tests |
| Calibration fixtures | `tests/fixtures/review-artifacts/valid-requirement-compression-calibration/`, review-artifact validator tests | Adds requirement-compression seeded-defect family, sampling floors, rotation triggers, iteration IDs, and not-applicable audit evidence. | `R17`-`R17d`, `R41`-`R45c`, `AC-RFG-014`, `AC-RFG-015`, `AC-RFG-020` | M4 code-review R6 |
| Behavior preservation and generated-output proof | `docs/changes/.../behavior-preservation.md`, build/adapter validation evidence | Proves independent gates, historical reviews, manual scope, no finding quota, and generated output boundaries remain intact. | `R46`-`R50`, `T12`, `T14` | M5 code-review R7 |
| Change-local lifecycle evidence | `docs/changes/.../change.yaml`, `review-log.md`, `review-resolution.md`, `reviews/*.md`, active plan, `docs/plan.md` | Records proposal/spec/test/architecture/plan/review/implementation evidence and current workflow state. | Workflow contract; active plan | review-artifact, metadata, lifecycle validators |

## Tests Added Or Changed

| Test area | What it proves | Why this level is appropriate |
| --- | --- | --- |
| Skill validator tests | Public skills teach the gate, no finding quota is introduced, and R26 uses a property-list by surface-list matrix. | Static skill guidance is the user-facing contract for reviewers and implementers. |
| Review-artifact validator tests | Requirement-fidelity manifests, receipts, closed enums, calibration records, seeded defects, and corrective-action conditions fail closed. | Review artifacts are structured evidence; validator tests prevent silent schema drift. |
| Lifecycle validator tests | Workflow-managed clean reviews cannot advance without fidelity applicability and receipt evidence; direct/profile-off behavior remains compatible. | The bug class affects automated continuation, so lifecycle routing needs direct coverage. |
| Change-metadata tests | Metadata status and finding counts stay synchronized with review evidence. | Change metadata drives workflow state and must not drift from review records. |
| Selector tests and selected CI | Touched surfaces route to the correct focused checks. | Prevents new validator/evidence paths from being omitted by local or CI validation. |
| Build-skill and adapter checks | Generated skill and adapter surfaces remain current through normal generation. | R49 is about generated output parity, so proof must come from generation commands, not manual edits. |
| Bounded spec-read proof | Requirement-fidelity review can inspect relevant clauses without broad full-spec reads. | This protects the proposal non-goal of avoiding broad full-spec reads for every small change. |

## Validation Evidence Before Final Verify

Representative validation recorded during implementation and review includes:

- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/test-build-skills.py`
- `python scripts/build-skills.py --check`
- `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`
- `python scripts/test-review-artifact-validator.py`
- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/test-change-metadata-validator.py`
- `python scripts/test-select-validation.py`
- `bash scripts/ci.sh --mode explicit --path docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md --path docs/plan.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/behavior-preservation.md`
- change-local `validate-review-artifacts`, `validate-change-metadata`, `validate-artifact-lifecycle`, and `git diff --check`

Final verify has not run yet.

## Review Resolution Summary

See `docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-resolution.md`.

Resolution summary:

| Count | Meaning |
| ---: | --- |
| 5 | accepted and resolved findings |
| 0 | unresolved findings |
| 0 | `needs-decision` findings |

Resolved findings:

- `SR1-F1`: mandatory manual-review applicability is out of first-slice scope.
- `SR1-F2`: calibration sampling and rotation obligations are quantified.
- `TSR1-F1`: manual proof obligations are structured and machine-checkable obligations were moved to automated tests.
- `RFG-M2-CR1`: workflow-managed clean handoff now requires requirement-fidelity applicability and receipt evidence.
- `RFG-M4-CR1`: misclassified not-applicable audits now require non-trivial corrective action.

## Alternatives Rejected

- Replace independent-review gates: rejected because requirement fidelity is an additive sibling layer, not a replacement for independence.
- Finding quotas or forced-failure reviews: rejected because calibration should measure recall, not incentivize noisy findings.
- Mandatory first-slice manual-review applicability classification: rejected until automated calibration data exists.
- Full automated prose property extraction: deferred as too broad for the first slice.
- Rewrite all historical reviews, all validators, or all specs: rejected by `R47` and `R50`; the slice updates selected high-value surfaces.
- Hand-edit generated adapter output: rejected by `R49`; M5 uses build and validation commands against generated output.

## Scope Control

Preserved non-goals:

- no hosted service, queue, database, deployment boundary, or external API;
- no private chain-of-thought exposure;
- no broad full-spec-read requirement for every review;
- no historical review migration;
- no change to workflow stage order;
- no automatic repair policy for requirement-compression findings beyond reviewer-declared safe fixes.

## Risks And Follow-Ups

Remaining downstream work:

- run final `verify`;
- prepare PR handoff after verify;
- hosted CI and human review remain external PR outcomes.

Known follow-ups from the proposal remain future work, not part of this slice:

- automatic spec-property extraction;
- immutable review packet manifests;
- all-review-family requirement-fidelity rollout;
- validator-generation helpers from property/surface matrices;
- review-quality reporting for compression-defect recall.

Current lifecycle state: all implementation milestones are closed after `code-review-r7`; next stage is `verify` after this explanation is recorded and validated.
