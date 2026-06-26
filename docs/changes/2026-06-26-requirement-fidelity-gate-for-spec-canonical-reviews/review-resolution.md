# Requirement-Fidelity Gate Review Resolution

## Scope

This record tracks material review finding closeout for the requirement-fidelity gate change.

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: architecture-review-r1
Review closeout: plan-review-r1
Review closeout: test-spec-review-r1
Review closeout: test-spec-review-r2
Review closeout: code-review-r1
Review closeout: code-review-r2
Review closeout: code-review-r3
Review closeout: code-review-r4
Review closeout: code-review-r5
Review closeout: code-review-r6
Review closeout: code-review-r7

- Reviews covered: `proposal-review-r1`, `spec-review-r1`, `spec-review-r2`, `architecture-review-r1`, `plan-review-r1`, `test-spec-review-r1`, `test-spec-review-r2`, `code-review-r1`, `code-review-r2`, `code-review-r3`, `code-review-r4`, `code-review-r5`, `code-review-r6`, `code-review-r7`
- Findings resolved: 5
- Unresolved findings: 0
- Current result: `code-review-r7` returned clean-with-notes for M5; all implementation milestones are closed and the next stage is `explain-change`.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| SR1-F1 | accepted | resolved | Path B chosen: mandatory manual-review applicability is out of first-slice scope; manual reviews may voluntarily record fidelity receipts; follow-on manual applicability proposal is routed after at least 30 calibrated records. |
| SR1-F2 | accepted | resolved | Sampling and rotation obligations are quantified with Phase B sample floors, steady-state floors, corpus iteration size, rotation triggers, record fields, and planned test IDs. |
| TSR1-F1 | accepted | resolved | Added a manual proof case schema, three structured manual proofs, two automated replacements for machine-checkable obligations, coverage-map links, and new planned test IDs. |
| RFG-M2-CR1 | accepted | resolved | Workflow-managed clean review routing now requires a recorded requirement-fidelity applicability result; missing and unknown values fail closed, and clean-review fixtures are complete by default. |
| RFG-M4-CR1 | accepted | resolved | Requirement-compression calibration now rejects misclassified not-applicable audits that have missing or trivial corrective action. |

## Finding Details

### proposal-review-r1

No material findings; no resolution entry required. The review approved the proposal and directed downstream specification.

### spec-review-r1

#### SR1-F1 - Manual review applicability is undefined

Finding ID: SR1-F1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Chosen action: Revised `R1` into automated-review applicability plus `R1a` voluntary manual application and `R1b` first-slice exclusion for mandatory manual-review classification. Added voluntary manual example `E7`, an explicit non-goal, and a follow-on artifact for `Manual Review Applicability for the Requirement-Fidelity Gate` after Phase B produces at least 30 calibrated review records.
Rationale: The empirical miss motivating this change was automated autoprogression review compression, not a manual-review applicability failure. Defining manual risk classification now would expand first-slice authority and ownership without current calibration evidence.
Validation target: Rerun `spec-review-r2` after the spec revision.
Validation evidence: `specs/requirement-fidelity-gate.md` no longer requires mandatory manual-review applicability in the first slice and preserves voluntary manual receipt recording.

#### SR1-F2 - Calibration sampling obligations are not measurable

Finding ID: SR1-F2
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Chosen action: Replaced soft sampling language with quantified Phase B sample floors: 10 percent baseline applicable review sampling, 30 percent reviewer-authored decomposition sampling, 5 percent not-applicable receipt sampling per calibration cycle, and post-Phase-B floors of 5 percent and 15 percent without follow-on amendment. Added `Review-calibration-corpus maintainer`, sampling record fields, closed `sampling_reason`, not-applicable audit fields, closed `audit_outcome`, corpus iteration size, rotation triggers, rotation log fields, `iteration_id` evidence, and planned test IDs `RFG-T017` through `RFG-T022`.
Rationale: Calibration is a core compression-defense mechanism in the accepted proposal. The spec now gives tests and validators measurable rates, fields, owners, and closed vocabularies instead of relying on undefined terms.
Validation target: Rerun `spec-review-r2` after the spec revision.
Validation evidence: `specs/requirement-fidelity-gate.md` requirements `R17` through `R17d`, `R44` through `R44g`, and `R45` through `R45c` define measurable sampling and rotation obligations; `AC-RFG-014`, `AC-RFG-015`, and `RFG-T017` through `RFG-T022` define reviewable proof points.

### spec-review-r2

No material findings. `spec-review-r2` approved the revised spec and confirmed `SR1-F1` and `SR1-F2` are closed.

### architecture-review-r1

No material findings. `architecture-review-r1` approved the canonical architecture update and ADR for downstream planning.

### plan-review-r1

No material findings. `plan-review-r1` approved the execution plan for downstream test-spec authoring.

### test-spec-review-r1

#### TSR1-F1 - Manual proof obligations are not auditable enough for implementation handoff

Finding ID: TSR1-F1
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec revision
Chosen action: Added `Manual proof case schema` with required stable ID, automation rationale, owning stage, required environment, exact steps, evidence artifact, pass condition, failure condition, owner role, and cadence fields. Added `MP-RFG-001` for private rotating corpus custody, `MP-RFG-002` for receipt-prose quality, and `MP-RFG-003` for public skill scan-first usability. Converted broad-read/performance confirmation to automated `T-RFG-PERF-001` and no-implementation-before-review gating to automated `T-RFG-GATE-001`. Updated the requirement coverage map, milestone coverage map, affected test cases, fixtures, performance checks, and manual QA checklist, and added planned proof IDs `RFG-022`, `RFG-023`, and `RFG-024`.
Rationale: Three obligations require human judgment and now have bounded manual proof cases. The broad-read and lifecycle-gating obligations are machine-checkable and are now specified as automated tests rather than manual confirmation.
Validation target: Rerun `test-spec-review-r2` after the test spec revision.
Validation evidence: `specs/requirement-fidelity-gate.test.md` contains the manual proof schema, structured proof cases `MP-RFG-001` through `MP-RFG-003`, automated test cases `T-RFG-PERF-001` and `T-RFG-GATE-001`, updated coverage-map links, and the new planned test IDs.

### test-spec-review-r2

No material findings. `test-spec-review-r2` approved the revised test spec, confirmed `TSR1-F1` is closed, and allowed implementation handoff.

### code-review-r1

No material findings. `code-review-r1` reviewed the M1 implementation diff, confirmed the requirement-fidelity guidance surfaces and skill-validator coverage align with the approved first-slice contract, closed M1, and handed off to M2 implementation.

### code-review-r2

#### RFG-M2-CR1 - Clean automated handoff can omit the fidelity applicability result entirely

Finding ID: RFG-M2-CR1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Stop state: review-requested
Rationale: `code-review-r2` found that the M2 lifecycle route advances workflow-managed clean reviews when requirement-fidelity applicability is absent, so independent-review evidence alone can still advance the profile.
Chosen action: Introduced `WORKFLOW_MANAGED_CLEAN_REVIEW_GATES` in `scripts/lifecycle_state_sync.py` with spec-cited independent-review, fidelity-applicability, and fidelity-receipt checks. Missing requirement-fidelity applicability now fails closed with `fidelity-applicability-missing`; unknown applicability fails closed with `fidelity-applicability-unknown`; applicable reviews with invalid receipts fail with `fidelity-receipt-invalid`; and not-applicable reviews without a closed reason fail with `fidelity-not-applicable-reason-invalid`.
Resolution: Canonicalized the lifecycle clean-review fixture through `make_workflow_managed_clean_review_fixture`, populated every R4-R8 and R30-R34 fidelity field by default, and made omission/invalid-value cases explicit per test. Added lifecycle regressions for missing applicability, unknown applicability, invalid applicable receipts, invalid/missing not-applicable reasons, complete default clean-review advancement, and direct-review compatibility. Added a review-artifact validator gate marker, a negative test for gate-in-force records missing applicability, and the durable `invalid-workflow-managed-missing-fidelity-applicability` fixture.
Required outcome: Workflow-managed clean handoff cannot advance without a recorded fidelity applicability result, and the review-artifact validator exposes the same missing-applicability invariant when the requirement-fidelity gate is in force.
Validation target: Rerun `code-review-r3` after the M2 resolution implementation.
Validation evidence: `python scripts/test-artifact-lifecycle-validator.py -k requirement_fidelity` passed; `python scripts/test-review-artifact-validator.py -k requirement_fidelity` passed; `python scripts/test-artifact-lifecycle-validator.py` passed; `python scripts/test-review-artifact-validator.py` passed; `python scripts/test-change-metadata-validator.py` passed; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews` passed; `python scripts/validate-change-metadata.py docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml` passed; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md --path docs/plan.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-log.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-resolution.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/code-review-r2.md` passed; `python scripts/validate-review-artifacts.py --mode structure tests/fixtures/review-artifacts/invalid-workflow-managed-missing-fidelity-applicability` failed as expected with `fidelity-applicability-missing`; `git diff --check -- scripts/lifecycle_state_sync.py scripts/test-artifact-lifecycle-validator.py scripts/review_artifact_validation.py scripts/test-review-artifact-validator.py tests/fixtures/review-artifacts/invalid-workflow-managed-missing-fidelity-applicability docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md docs/plan.md` passed.

### code-review-r3

No material findings. `code-review-r3` reviewed the M2 resolution diff at commit `75635fca`, confirmed `RFG-M2-CR1` is resolved across lifecycle routing, fixture defaults, review-artifact validation, and compatibility coverage, closed M2, and handed off to M3 implementation.

### code-review-r4

No material findings. `code-review-r4` reviewed the M3 implementation diff at commit `32e1b372`, confirmed the R26 property-list by surface-list matrix, missing-`recorded` negative proof, and bounded spec-read fixture align with the approved M3 contract, closed M3, and handed off to M4 implementation.

### code-review-r5

#### RFG-M4-CR1 - Misclassified not-applicable audits can omit corrective action

Finding ID: RFG-M4-CR1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Stop state: review-requested
Rationale: `code-review-r5` found that M4 validates the closed `Audit outcome` enum but does not enforce `R45b`'s conditional corrective-action requirement when the audit outcome is `misclassified-should-have-applied`.
Required outcome: Requirement-compression calibration validation must fail when a misclassified not-applicable audit records no corrective action.
Safe resolution path: Add a review-artifact validator regression where `Audit outcome: misclassified-should-have-applied` and `Corrective action: none` fails, then update `scripts/review_artifact_validation.py` to reject missing, empty, or `none` corrective action for that audit outcome. Keep the existing valid requirement-compression calibration fixture passing.
Chosen action: Added `REQUIREMENT_COMPRESSION_REQUIRES_CORRECTIVE_ACTION_OUTCOMES` citing `R45b` and `TRIVIAL_CORRECTIVE_ACTION_VALUES` covering empty, `none`, `n/a`, and `na` values after whitespace and case normalization. Added `_validate_requirement_compression_corrective_action` at the existing requirement-compression parse site.
Resolution: Added regressions for the exact `misclassified-should-have-applied` plus `Corrective action: none` probe, empty action, missing action, whitespace/case variants, `N/A`, a real corrective-action pass case, and the compatibility guard that `Audit outcome: correct` with `Corrective action: none` remains valid. The existing valid requirement-compression calibration fixture remains valid and the approved spec was not changed.
Validation target: Rerun `code-review-r6` after the M4 resolution implementation.
Validation evidence: `python scripts/test-review-artifact-validator.py -k requirement_compression_misclassified_audit` passed after first failing for the expected reason before the validator fix; `python scripts/test-review-artifact-validator.py -k requirement_compression` passed; `python scripts/validate-review-artifacts.py --mode structure tests/fixtures/review-artifacts/valid-requirement-compression-calibration` passed; `python scripts/test-review-artifact-validator.py` passed; `python scripts/test-select-validation.py` passed with `102 passed in 134.70s`.

### code-review-r6

No material findings. `code-review-r6` reviewed the M4 resolution diff at commit `83156ff4`, confirmed `RFG-M4-CR1` is resolved across the validator constant, conditional corrective-action check, exact negative regression, trivial-value normalization, real-action pass case, and `correct`-outcome compatibility guard, closed M4, and handed off to M5 implementation.

### code-review-r7

No material findings. `code-review-r7` reviewed the final M5 implementation and requirement-fidelity change surface at commit `54311aff`, confirmed behavior-preservation evidence, generated-output validation through normal build commands, selected CI, and lifecycle state synchronization, closed M5, and handed off to `explain-change`.
