# Activate Boundary-First v1 in RigorLoop v0.3.7

## Owning change record

`docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/change.yaml`

## Problem

The progressive boundary-first implementation is merged and validated, but the
tracked capability remains `pending`. Published users therefore cannot rely on
the active contract that makes concise boundary awareness automatic for new or
substantively revised behavior work.

## Goals

- Activate the complete `boundary-first-v1` bundle in one routine stable release.
- Publish matching Codex, Claude, and opencode adapter archives and the npm CLI package.
- Preserve `v0.3.6` as an immutable rollback release.
- Record pre-publication and post-publication evidence through the existing release transaction.
- Keep the release small: activation, versioned package preparation, and release evidence only.

## Non-goals

- Do not redesign the boundary-first model or add another activation mechanism.
- Do not change the governed skill set or resource vocabulary.
- Do not weaken release, package, archive, security, or public-smoke checks.
- Do not mutate an already published package or release in place.
- Do not include unrelated workflow, validator, or skill improvements.
- Do not publish, tag, or merge automatically as part of lifecycle authoring or verification.

## Vision fit

fits the current vision

The activation makes reviewed workflow behavior available through reproducible,
inspectable packages while retaining durable release and rollback evidence.

## Context

PR #129 merged the progressive compact scan, stage-owned resource slices,
deterministic projection, adapter parity, selector correction, and activation
proof. The live state intentionally remained `pending`.

Current GitHub, Git, and npm evidence identifies `v0.3.6`/`0.3.6` as the latest
public release. The repository already owns routine releases through
`docs/releases/profiles/<tag>.yaml`, generated preparation surfaces, cheap
preflight, the full release gate, trusted publishing, and rerunnable public
closeout. Detailed research is recorded in
`docs/research/2026-08-05-boundary-first-v1-activation-release.md`.

## Options considered

### O0: Keep the capability pending

This avoids release risk but leaves the user-requested automatic behavior
unavailable under the active contract.

### O1: Activate repository state without a public release

This creates a state/package mismatch and does not deliver the capability to
published users.

### O2: Activate and publish a routine stable patch release

This uses the existing transaction, delivers the complete bundle, and retains
an immutable rollback target. This is the recommended option.

### O3: Publish a release candidate first

This adds an observation phase but also adds another release identity and is
not justified by the already completed package and clean-install proof.

### O4: Introduce runtime or per-install activation

This adds a second state mechanism and contradicts the approved atomic release
model.

## Recommended direction

Choose O2. Prepare `v0.3.7` as the activating release and bind rollback to
`v0.3.6`. Use the existing routine release profile and generators. Treat the
activation state, canonical hashes, generated packages, release metadata, and
publication evidence as one coherent transaction.

Lifecycle automation may carry the change through verified PR readiness. Tag
creation and public GitHub/npm publication remain explicit external actions and
must stop for the release boundary even when every local gate passes.

## Expected behavior changes

- `boundary-first-v1` changes from `pending` to `active` in the activating release.
- New behavior-changing specifications automatically use the concise boundary scan and required formal authoring contract.
- Grandfathered non-substantive specifications retain their accepted status.
- Published installations for all supported targets contain the exact active resource bundle.
- Rollback selects the immutable `v0.3.6` release rather than constructing a mixed bundle.

## Architecture impact

No new container, service, persistence model, or release mechanism is expected.
The change exercises two approved architecture boundaries: the atomic
boundary-first activation state and the profile-driven routine release
transaction. Architecture assessment should confirm that the existing
architecture and ADRs fully cover the version-specific transition.

## Testing and verification strategy

- Prove the exact pending-to-active transition and closed activation fields.
- Prove canonical reference, manifest, and projection hashes match the release candidate.
- Prove all ten governed skills and three adapter targets have exact resource parity.
- Run boundary-first, skill, adapter, selector, release-transaction, package-publication, and release validation tests selected by the approved test specification.
- Run packed non-dry-run installation smoke for Codex, Claude, and opencode.
- Run the repository-owned `release-preflight`, full `release-verify`, PR CI, and required broad smoke.
- After publication, observe GitHub/npm identities and run live public `npx` smoke before closeout.

## Rollout and rollback

Prepare and review `v0.3.7` while the live capability remains pending. The
release transaction activates only the complete reviewed bundle. Trusted
publishing creates immutable GitHub and npm release identities after the final
external-action checkpoint.

Before publication, rollback discards the candidate and restores the coherent
pending bundle. After publication, rollback uses immutable `v0.3.6`; any defect
that requires changed code is corrected in a later patch release rather than
mutating `v0.3.7`.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Activation state and packages diverge | Generate and validate all versioned surfaces from one release profile and exact resource hashes. |
| A target receives an incomplete resource set | Require three-target archive generation, clean installation, and parity validation. |
| Rollback metadata points to an invalid release | Validate `v0.3.6` tag and adapter metadata as the exact immutable rollback target. |
| Release scripts omit the new version | Make version support profile-derived where already designed and fail cheap in release preflight. |
| Publication succeeds only partially | Preserve rerunnable public closeout and use a later corrective release; never rewrite published artifacts. |
| Scope expands into workflow redesign | Treat unrelated findings as separate follow-ups unless they block safe activation. |

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Proceed with the best next objective | in scope | Recommended direction |
| Make automatic boundary guidance available to users | in scope | Goals; expected behavior changes |
| Keep the solution concise | in scope | Goals; non-goals; scope budget |
| Publish the prepared capability | in scope | Rollout and rollback |
| Avoid further mechanism redesign | rejected option | O4; non-goals |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Boundary-first activation state | core to this proposal | It is the remaining user-visible transition. |
| `v0.3.7` routine release profile and generated preparation | core to this proposal | It is the existing source of truth and delivery path. |
| Three-adapter and npm package proof | same-slice dependency | Activation is incomplete without published package parity. |
| Pre-publication PR | separate implementation slice | Reviewable preparation must precede external publication. |
| Tag and public publication | separate implementation slice | External effects require an explicit release checkpoint. |
| Post-publication closeout | separate implementation slice | It depends on public GitHub/npm evidence. |
| Boundary model redesign | out of scope | The merged contract is already approved. |
| Release tooling redesign | out of scope | Existing profile-driven tooling owns routine releases. |

## Open questions

None blocks proposal review. The release remains stable `v0.3.7` unless review
finds evidence that a release candidate is required. Publication mode remains
the existing trusted-publishing path.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-05 | Use stable `v0.3.7`. | GitHub, Git, and npm agree that `v0.3.6` is current; a patch release is the smallest compatible successor. | Deferral, repository-only activation, release candidate. |
| 2026-08-05 | Use `v0.3.6` as rollback. | It is the latest immutable public release before activation. | Constructed rollback bundle. |
| 2026-08-05 | Reuse the routine release transaction. | Existing profile, preparation, verification, publication, and closeout boundaries already own this work. | New activation or release mechanism. |

## Next artifacts

- Proposal review.
- Version-specific activation/release specification and spec review.
- Architecture assessment against the existing activation and release architecture.
- Execution plan and plan review.
- Matching test specification and test-spec review.
- Implementation, independent code review, explanation, verification, and PR handoff.
- Explicit release publication and public-evidence closeout after the PR is merged.

## Follow-on artifacts

None yet

## Readiness

Ready for `proposal-review`. Implementation is not yet allowed.
