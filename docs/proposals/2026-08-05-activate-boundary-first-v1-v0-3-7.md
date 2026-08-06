# Activate Boundary-First v1 in RigorLoop v0.4.0

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
- Add one explicit candidate-validation mode so the reviewed activation commit can be proven before its immutable tag exists.
- Keep the release small: activation, versioned package preparation, and release evidence only.

## Non-goals

- Do not redesign the boundary-first model or add another activation mechanism.
- Do not change the governed skill set or resource vocabulary.
- Do not weaken release, package, archive, security, or public-smoke checks.
- Do not mutate an already published package or release in place.
- Do not include unrelated workflow, validator, or skill improvements; the only
  validator change is the pre-tag candidate mode required to break the
  review-before-tag circularity.
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

### O2: Activate and publish a routine stable minor release

This uses the existing transaction, delivers the complete bundle, and retains
an immutable rollback target. This is the recommended option.

### O3: Publish a release candidate first

This adds an observation phase but also adds another release identity and is
not justified by the already completed package and clean-install proof.

### O4: Introduce runtime or per-install activation

This adds a second state mechanism and contradicts the approved atomic release
model.

## Recommended direction

Choose O2. Prepare `v0.4.0` as the activating release and bind rollback to
`v0.3.6`. Use the existing routine release profile and generators. Treat the
activation state, canonical hashes, generated packages, release metadata, and
publication evidence as one coherent transaction.

Add one narrowly scoped candidate-validation mode. In candidate mode, the
validator checks the proposed active tree, expected `v0.4.0` identity,
immediate `v0.3.6` predecessor, transition parent, grandfathering baseline,
resource hashes, projections, packages, and rollback metadata without claiming
that the absent tag is already published. Default and release-context
validation remain strict: `v0.4.0` must exist and resolve to the exact reviewed
pending-to-active transition commit.

Lifecycle automation may carry one first-parent candidate branch through
verified PR readiness. The branch has two distinct reviewed identities: the
pending-to-active transition commit and the later final branch head containing
required review, rationale, and verification evidence. Candidate validation
discovers and records both.

Because normal merge commits would change the activation transition identity,
release execution must fast-forward `main` to the exact final reviewed branch
head with an unchanged-parent compare-and-swap, create `v0.4.0` at the exact
earlier transition commit in that head's first-parent history, and push both
refs atomically. Any base drift invalidates candidate evidence and returns the
change to regeneration and review. Tag creation and public GitHub/npm
publication remain explicit external actions and must stop for the release
boundary even when every local gate passes.

## Expected behavior changes

- `boundary-first-v1` changes from `pending` to `active` in the activating release.
- New behavior-changing specifications automatically use the concise boundary scan and required formal authoring contract.
- Grandfathered non-substantive specifications retain their accepted status.
- Published installations for all supported targets contain the exact active resource bundle.
- Rollback selects the immutable `v0.3.6` release rather than constructing a mixed bundle.
- Candidate validation proves the proposed transition without treating an absent tag as active-release evidence; strict release validation still requires the immutable tag.

## Architecture impact

No new container, service, or persistence model is expected. The change
exercises two approved architecture boundaries—the atomic boundary-first
activation state and the profile-driven routine release transaction—and adds a
narrow validation phase between them. Architecture assessment must cover
candidate-versus-release authority, separate reviewed-head and transition-tag
identities, fast-forward and base-drift behavior, atomic ref publication, tagged
tree self-containment, and strict tag-context revalidation.

## Testing and verification strategy

- Prove the exact pending-to-active transition and closed activation fields.
- Prove candidate mode accepts only an absent expected tag with the exact
  candidate transition, immediate predecessor, baseline, and complete bundle;
  default mode must continue to reject the absent tag.
- Prove candidate mode rejects an existing conflicting tag, base drift, wrong
  predecessor, non-fast-forward transition, mixed bundle, or mismatched commit.
- Prove candidate evidence distinguishes the final reviewed branch head from
  the earlier transition commit and that both belong to one first-parent chain.
- Prove canonical reference, manifest, and projection hashes match the release candidate.
- Prove all ten governed skills and three adapter targets have exact resource parity.
- Run boundary-first, skill, adapter, selector, release-transaction, package-publication, and release validation tests selected by the approved test specification.
- Run packed non-dry-run installation smoke for Codex, Claude, and opencode.
- Run candidate-mode validation, repository-owned `release-preflight`, PR CI,
  and required broad smoke before the external checkpoint; after creating the
  local immutable tag, run default strict validation and full `release-verify`
  before the atomic push.
- Run strict release verification from the tagged transition tree and prove it
  needs no lifecycle artifact committed only after that transition.
- After publication, observe GitHub/npm identities and run live public `npx` smoke before closeout.

## Rollout and rollback

Prepare and review one first-parent `v0.4.0` candidate branch while the public
capability remains pending. The transition commit contains every release input
needed by the tag workflow. Later commits add lifecycle review, rationale, and
verification evidence without changing the release payload or activation
record. Candidate validation proves the complete proposed bundle and both
commit identities but never claims a published active release.

At the external-action checkpoint, confirm `origin/main` still equals the
candidate branch's reviewed base. Create local `v0.4.0` at the transition
commit, run strict validation and full release verification from that tagged
tree, then atomically fast-forward remote `main` to the final reviewed branch
head and publish the tag at the transition commit. The tag workflow performs
trusted GitHub/npm publication from that exact transition tree.

Before the atomic push, rollback deletes only the local candidate tag and leaves
remote `main`, public packages, and the coherent pending bundle unchanged. A
failed compare-and-swap or any base drift stops publication and requires a
rebased, regenerated, and rereviewed candidate. After publication, rollback
uses immutable `v0.3.6`; any defect that requires changed code is corrected in
a later patch release rather than mutating `v0.4.0`.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Activation state and packages diverge | Generate and validate all versioned surfaces from one release profile and exact resource hashes. |
| A target receives an incomplete resource set | Require three-target archive generation, clean installation, and parity validation. |
| Rollback metadata points to an invalid release | Validate `v0.3.6` tag and adapter metadata as the exact immutable rollback target. |
| Release scripts omit the new version | Make version support profile-derived where already designed and fail cheap in release preflight. |
| Candidate validation is mistaken for active-release proof | Give it an explicit mode and result; keep default and release gates strict and tag-bound. |
| Merge or base drift changes the reviewed transition identity | Require unchanged-parent compare-and-swap and atomic fast-forward/tag publication; regenerate and rereview on drift. |
| Review evidence after activation changes final branch HEAD | Track branch-head and transition-tag identities separately; require one first-parent chain and a self-contained tagged release tree. |
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
| `v0.4.0` routine release profile and generated preparation | core to this proposal | It is the existing source of truth and delivery path. |
| Three-adapter and npm package proof | same-slice dependency | Activation is incomplete without published package parity. |
| Candidate-validation bridge | same-slice dependency | Current strict validation cannot prove an active PR before its tag exists. |
| Pre-publication PR | separate implementation slice | It reviews the transition commit plus later lifecycle evidence on one first-parent branch. |
| Atomic fast-forward and tag publication | separate implementation slice | It publishes final `main` and the earlier transition tag as two explicit reviewed identities. |
| Post-publication closeout | separate implementation slice | It depends on public GitHub/npm evidence. |
| Boundary model redesign | out of scope | The merged contract is already approved. |
| Broad release tooling redesign | out of scope | Only the candidate-validation bridge is required; existing profile-driven tooling remains authoritative. |

## Open questions

None blocks proposal review. The release is stable `v0.4.0` because REL-R10
requires a minor version for backward-compatible public skill behavior.
Publication mode remains the existing trusted-publishing path.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-05 | Use stable `v0.4.0`. | GitHub, Git, and npm agree that `v0.3.6` is current, and REL-R10 requires a minor release for new backward-compatible public skill behavior. | Contract-invalid patch release, deferral, repository-only activation, release candidate. |
| 2026-08-05 | Use `v0.3.6` as rollback. | It is the latest immutable public release before activation. | Constructed rollback bundle. |
| 2026-08-05 | Reuse the routine release transaction. | Existing profile, preparation, verification, publication, and closeout boundaries already own this work. | New activation or release mechanism. |
| 2026-08-05 | Separate candidate and strict tag-context validation. | Strict validation requires a tag that cannot safely exist before review; candidate mode proves the exact proposed transition without weakening release proof. | Publish-before-review; omit activation validation from PR. |
| 2026-08-05 | Atomically publish two reviewed commit identities. | `main` owns the final reviewed head, while the tag contract binds the earlier first-parent pending-to-active transition; compare-and-swap prevents stale-base publication. | Same-commit conflation; normal merge commit; force push; mutable tag. |

## Next artifacts

- Proposal review.
- Version-specific activation/release specification, including candidate versus strict validation, and spec review.
- Architecture assessment of validation authority, transition identity, and atomic ref publication.
- Execution plan and plan review.
- Matching test specification and test-spec review.
- Implementation, independent code review, explanation, verification, and PR handoff.
- Explicit release publication and public-evidence closeout after the PR is merged.

## Follow-on artifacts

None yet

## Readiness

Ready for `proposal-review`. Implementation is not yet allowed.
