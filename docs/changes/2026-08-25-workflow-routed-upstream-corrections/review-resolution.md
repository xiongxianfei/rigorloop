# Review Resolution: Workflow-Routed Upstream Corrections

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: spec-review-r2

- Reviews covered: proposal-review-r1, spec-review-r1, spec-review-r2
- Findings resolved: 5
- Unresolved findings: 0
- Current result: The spec-review r2 boundary correction is implemented; independent spec-review r3 is required.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| WRUC-PR1 | accepted | resolved | Guarded duplicate-registration withdrawal is now a same-slice dependency and rollout commits prevention and recovery together. |
| WRUC-SR1 | accepted | resolved | The source blocker moves into the immutable snapshot and is non-fatal during the exact route. |
| WRUC-SR2 | accepted | resolved | Return evidence binds the exact route, revised artifact, and approving review occurrence. |
| WRUC-SR3 | accepted | resolved | The receipt stores the prior lifecycle revision while the result reports the resulting revision. |
| WRUC-SR4 | accepted | resolved | State and authority behavior now each have one truthful complete boundary. |

## Resolution Entries

### proposal-review-r1

#### WRUC-PR1

Finding ID: WRUC-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Decision owner: none
Decision needed: none
Chosen action: Change guarded duplicate-registration withdrawal to a same-slice dependency and keep active-branch consumption separate.
Rationale: The proposal cannot promise to remove the current blocker while treating the only recovery operation as optional.
Required outcome: The scope budget and rollout make collision prevention and guarded withdrawal one committed capability.
Validation target: revised proposal and proposal-review-r2
Final action: Updated the scope-budget treatment and rollout commitment without changing the selected authority boundary.
Validation evidence: docs/changes/2026-08-25-workflow-routed-upstream-corrections/evidence/proposal-revision-r1.md; revised proposal sha256:51b5ced0eb33970c8fa01a01a0b8ff49af256e47bcf70a930e985673f8c82959

### spec-review-r1

#### WRUC-SR1

Finding ID: WRUC-SR1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Decision owner: none
Decision needed: none
Chosen action: Specify a suspended source snapshot and a non-fatal active-route blocker projection.
Rationale: The route must make the exact destination revision executable while preserving the original downstream blocker for return.
Required outcome: Only the routed destination operation is admitted, and return restores the original blocker exactly.
Validation target: revised spec and spec-review-r2
Validation evidence: `docs/changes/2026-08-25-workflow-routed-upstream-corrections/evidence/spec-revision-r1.md`; revised spec `sha256:66f22be6e1d6cfe51cb9bf77913a165cbb63d87729529b54138519246e142dc8`

### spec-review-r2

#### WRUC-SR4

Finding ID: WRUC-SR4
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Decision owner: none
Decision needed: none
Chosen action: Consolidate each affected core dimension into one complete boundary and update downstream references.
Rationale: A structurally valid record must also state complete partitions, invariants, and outcomes for every requirement it claims.
Required outcome: No partial boundary row overclaims full-dimension ownership.
Validation target: revised spec and spec-review-r3
Validation evidence: `docs/changes/2026-08-25-workflow-routed-upstream-corrections/evidence/spec-revision-r2.md`; revised spec `sha256:1a3bc2c06cc7e30f4f9feac9d53448c0d344d0fdc0ff10f7a28520bda1bb7100`

### spec-review-r1

#### WRUC-SR2

Finding ID: WRUC-SR2
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Decision owner: none
Decision needed: none
Chosen action: Define exact return-evidence and approving-review identity fields.
Rationale: A contained file alone cannot prove that the revised destination passed its required current review.
Required outcome: Return is tied to the exact route, artifact revision, review occurrence, authority, outcome, and lifecycle revision.
Validation target: revised spec and spec-review-r2
Validation evidence: `docs/changes/2026-08-25-workflow-routed-upstream-corrections/evidence/spec-revision-r1.md`; revised spec `sha256:66f22be6e1d6cfe51cb9bf77913a165cbb63d87729529b54138519246e142dc8`

#### WRUC-SR3

Finding ID: WRUC-SR3
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Decision owner: none
Decision needed: none
Chosen action: Persist only `prior_lifecycle_revision` in a withdrawal receipt and expose the resulting revision in the operation result.
Rationale: A receipt cannot contain the hash of the bytes that include that same hash without a special fixed-point protocol.
Required outcome: Receipt construction and replay identity are deterministic and non-circular.
Validation target: revised spec and spec-review-r2
Validation evidence: `docs/changes/2026-08-25-workflow-routed-upstream-corrections/evidence/spec-revision-r1.md`; revised spec `sha256:66f22be6e1d6cfe51cb9bf77913a165cbb63d87729529b54138519246e142dc8`

### proposal-review-r2

Review closeout: proposal-review-r2

No material findings; no resolution entry required.

### spec-review-r3

Review closeout: spec-review-r3

No material findings; no resolution entry required.
