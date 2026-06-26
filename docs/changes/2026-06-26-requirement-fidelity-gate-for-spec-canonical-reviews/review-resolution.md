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

- Reviews covered: `proposal-review-r1`, `spec-review-r1`, `spec-review-r2`, `architecture-review-r1`, `plan-review-r1`, `test-spec-review-r1`, `test-spec-review-r2`
- Findings resolved: 3
- Unresolved findings: 0
- Current result: `test-spec-review-r2` approved the revised test spec with no material findings; implementation handoff is allowed.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| SR1-F1 | accepted | resolved | Path B chosen: mandatory manual-review applicability is out of first-slice scope; manual reviews may voluntarily record fidelity receipts; follow-on manual applicability proposal is routed after at least 30 calibrated records. |
| SR1-F2 | accepted | resolved | Sampling and rotation obligations are quantified with Phase B sample floors, steady-state floors, corpus iteration size, rotation triggers, record fields, and planned test IDs. |
| TSR1-F1 | accepted | resolved | Added a manual proof case schema, three structured manual proofs, two automated replacements for machine-checkable obligations, coverage-map links, and new planned test IDs. |

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
