# Review Resolution: Explain-Change Skill Simplification

## Summary

Closeout status: closed

Review closeout: proposal-review-r4

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `proposal-review-r4`
- Findings resolved: 6
- Unresolved findings: 0
- Current result: lifecycle-normalized proposal approved by same-stage rereview; no automatic downstream handoff.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| EXCSIM-PR1 | accepted | resolved | Four assemblies represent every governance/output combination. |
| EXCSIM-PR2 | accepted | resolved | Atomic replacement replaces unsupported partial recovery. |
| EXCSIM-PR3 | accepted | resolved | Every assembly must improve under one formula. |
| EXCSIM-PR4 | accepted | resolved | Every durable create and refresh composes from the current skeleton. |
| EXCSIM-PR5 | accepted | resolved | Reviewed subject and explanation evidence tail are separate identities. |
| EXCSIM-PR6 | accepted | resolved | `Workflow handback` replaces verification-readiness language. |

## Finding Details

### proposal-review-r4

No material findings. This clean rereview confirmed that the accepted status, follow-on artifacts, and readiness statement agree without changing the proposal direction.

### proposal-review-r3

No material findings. This clean rereview confirmed resolution of `EXCSIM-PR1` through `EXCSIM-PR6` against the revised proposal identity.

### proposal-review-r1

#### EXCSIM-PR1 - Governance and durable output are not represented as independent axes

Finding ID: EXCSIM-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal revision
Decision owner: proposal author
Decision needed: none; decision completed
Chosen action: Define portable-inline, portable-durable, governed-inline, and governed-durable assemblies.
Rationale: The independent axes require the complete four-way cross-product.
Validation target: proposal-review r3
Validation evidence: revised proposal `sha256:167a0affb94be03c43e4233d57a1263b3e46defd77d508158fd4e075224078f1`; proposal-review-r3 approved
Implementation evidence: not applicable at proposal stage

#### EXCSIM-PR2 - Retry claims lack a durable or atomic recovery basis

Finding ID: EXCSIM-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal revision
Decision owner: proposal author
Decision needed: none; decision completed
Chosen action: Use atomic whole-file replacement, fresh classification after uncertainty, and no resumable partial-write claim.
Rationale: A single-file artifact does not justify a new transaction owner when atomic replacement is available.
Validation target: proposal-review r3
Validation evidence: revised proposal `sha256:167a0affb94be03c43e4233d57a1263b3e46defd77d508158fd4e075224078f1`; proposal-review-r3 approved
Implementation evidence: not applicable at proposal stage

#### EXCSIM-PR3 - Acceptance does not require every declared profile to improve

Finding ID: EXCSIM-PR3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal revision
Decision owner: proposal author
Decision needed: none; decision completed
Chosen action: Count each loaded or copied file once and require word and byte reduction for all four assemblies.
Rationale: The central value claim must cover every supported runtime assembly.
Validation target: proposal-review r3
Validation evidence: revised proposal `sha256:167a0affb94be03c43e4233d57a1263b3e46defd77d508158fd4e075224078f1`; proposal-review-r3 approved
Implementation evidence: not applicable at proposal stage

### proposal-review-r2

#### EXCSIM-PR4 - Durable refresh contradicts the assembly and skeleton-loading model

Finding ID: EXCSIM-PR4
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal revision
Decision owner: proposal author
Decision needed: none; decision completed
Chosen action: Compose every durable create and refresh from the current skeleton and replace the complete file under exact authority.
Rationale: One structural rule makes resource loading, measurement, and mutation exhaustive.
Safe resolution path: Use current-skeleton whole-file composition; exclude section-level and historical-layout parsing.
Validation target: proposal-review r3
Validation evidence: revised proposal `sha256:167a0affb94be03c43e4233d57a1263b3e46defd77d508158fd4e075224078f1`; proposal-review-r3 approved
Implementation evidence: not applicable at proposal stage

#### EXCSIM-PR5 - Reviewed code state and later explanation evidence are conflated

Finding ID: EXCSIM-PR5
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal revision
Decision owner: proposal author
Decision needed: none; decision completed
Chosen action: Bind final review to the base-to-reviewed-subject diff and permit only one direct-child explanation-only evidence tail before verify.
Rationale: The explanation artifact must not make its own reviewed product diff stale.
Safe resolution path: Keep reviewed subject, recording revision, handoff revision, and permitted evidence-tail identities distinct.
Validation target: proposal-review r3
Validation evidence: revised proposal `sha256:167a0affb94be03c43e4233d57a1263b3e46defd77d508158fd4e075224078f1`; proposal-review-r3 approved
Implementation evidence: not applicable at proposal stage

#### EXCSIM-PR6 - `Verify readiness` exceeds explain-change claim authority

Finding ID: EXCSIM-PR6
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal revision
Decision owner: proposal author
Decision needed: none; decision completed
Chosen action: Use `Workflow handback` with explanation status, basis, cutoff, blockers, control return, and workflow ownership only.
Rationale: Workflow owns routing and verify owns readiness.
Safe resolution path: Forbid verification, branch, PR, release, deployment, and lifecycle readiness claims.
Validation target: proposal-review r3
Validation evidence: revised proposal `sha256:167a0affb94be03c43e4233d57a1263b3e46defd77d508158fd4e075224078f1`; proposal-review-r3 approved
Implementation evidence: not applicable at proposal stage
