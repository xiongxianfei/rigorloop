# Usability-First Boundary-First v0.4.0 Release

## Owning change record

`docs/changes/2026-08-06-usability-first-boundary-release/change.yaml`

## Problem

Boundary-first behavior is implemented but still unavailable to published users.
The previous activation initiative coupled skill activation to public Git identities and introduced a candidate validator, hook protocol, and atomic publisher.
Eleven M2 review rounds showed that this release-specific machinery costs more complexity than it returns for a thin project, while the user-visible release remains blocked.

## Goals

- Make boundary-first behavior automatic in the published skills without requiring users to name the method.
- Keep default output concise and focused on the few boundaries that materially affect correctness.
- Publish one coherent v0.4.0 package through the existing routine release workflow.
- Preserve generated parity across Codex, Claude, opencode, and the npm package.
- Preserve v0.3.6 as the immutable rollback release.
- Remove one-off activation publication machinery from the release path.

## Non-goals

- Do not create a second release mode or a reduced-safety public workflow.
- Do not weaken package parity, installation, version, secret, rollback, or public-smoke checks.
- Do not model every possible Git race or provider failure inside RigorLoop.
- Do not redesign the boundary-first proof model in this release.
- Do not tag, publish, push, merge, or mutate public systems during lifecycle authoring and verification.
- Do not turn the release simplification into a broad rewrite of repository governance.

## Vision fit

fits the current vision

The direction preserves reviewable evidence while responding directly to the vision's failure condition: workflow artifacts are harmful when they slow delivery without improving review quality.
It keeps evidence attached to user-visible behavior and removes release-specific ceremony that users never consume.

## Context

The progressive boundary-first implementation already established canonical resources, stage-owned skill guidance, generated adapter parity, and activation metadata.
The remaining user value is straightforward: published skills should apply concise boundary awareness automatically.

The repository already has a routine release profile, deterministic package generation, release verification, trusted GitHub/npm publication, public smoke, and rerunnable closeout.
The cancelled initiative duplicated this boundary with custom pre-tag and atomic-ref mechanisms.

Replacement for: `docs/proposals/2026-08-05-activate-boundary-first-v1-v0-3-7.md`.
The older proposal and its downstream artifacts remain historical until their owning stages record formal supersession.

## Options Considered

### O0: Keep boundary-first pending

This avoids release work but withholds the completed user-facing behavior.

### O1: Finish the custom publisher

This preserves sunk work but retains a large release-specific state machine and its ongoing review burden.

### O2: Use the existing routine release workflow

Activation describes behavior in the checked tree.
Release metadata and the existing tag workflow independently prove public version and publication.
This is the recommended option.

### O3: Offer simple and hardened release modes

This increases choice but doubles concepts, documentation, tests, and maintenance for a thin project.

### O4: Redesign the complete workflow around usability

This may have long-term value but is too broad to block delivery of the already implemented capability.

## Recommended Direction

Choose O2.

Keep two concerns separate:

- The boundary-first activation record says whether the checked repository tree and generated packages use boundary-first behavior.
- The release profile, immutable tag, trusted publication workflow, and closeout evidence say whether a version is publicly released.

Prepare one normal v0.4.0 release commit that activates boundary-first, updates the routine release profile and generated surfaces, and passes ordinary repository and package validation.
After merge, a maintainer creates `v0.4.0` at the exact reviewed commit and uses the existing tag workflow.
No custom candidate mode, hook result protocol, first-parent identity chain, or atomic main/tag publisher is introduced.

Default skill behavior follows one concise rule:

> Cover the boundaries most likely to change correctness by default; expand only when the task, governing contract, or user explicitly calls for deeper analysis.

## Expected Behavior Changes

- Published related skills apply boundary-first guidance automatically.
- Users no longer need to request `boundary-first-method-v1` by name.
- Ordinary specifications, plans, implementations, and reviews cover material boundaries without enumerating remote scenarios.
- Users can explicitly request deeper boundary analysis when needed.
- Codex, Claude, opencode, and npm-delivered resources remain equivalent.
- The release follows the same maintainer workflow as other routine stable releases.

## Architecture Impact

The intended architecture is smaller than the cancelled design.
The activation manifest remains the authority for tree-local feature behavior, while existing release profiles and automation remain the authority for publication.

Implementation is expected to remove or retire the custom candidate-validation and activation-publication helpers added by the cancelled initiative.
No new service, persistence layer, inter-process protocol, or ref-publication component is expected.
Architecture assessment should determine whether retiring the activation-publication ADR is sufficient or whether a short replacement ADR is useful.

## Testing and Verification Strategy

- Prove automatic boundary-first behavior without a method-name prompt.
- Prove concise default output on representative spec, code-inspection, and code-review journeys.
- Prove explicit deeper analysis can expand coverage without changing the default.
- Prove canonical resource and generated package parity across all three adapters.
- Run packed installation and target initialization smoke.
- Validate v0.4.0 version, release profile, release notes, archives, and v0.3.6 rollback metadata.
- Run existing release preflight, repository-selected validation, and release verification.
- Keep external publication and public smoke as explicit post-merge maintainer actions.

## Rollout and Rollback

The implementation PR prepares and verifies the complete v0.4.0 tree through the normal workflow.
No local or remote release tag is required to prove that the PR's checked tree activates boundary-first behavior.

After merge, the maintainer tags the exact reviewed release commit and lets the existing trusted release workflow publish GitHub, npm, and adapter archives.
If pre-publication validation fails, no tag is published and the PR is corrected normally.
After publication, v0.3.6 remains the immutable rollback version and any v0.4.0 defect is corrected through a later patch rather than rewriting the tag or package.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Simplification removes a useful release guard | Retain existing release preflight, tagged-tree verification, trusted publication, and public closeout. |
| Activation and public publication are confused | Give activation metadata tree-local meaning and keep public version proof in release metadata and tag evidence. |
| Default boundary guidance becomes verbose | Test representative user journeys and treat concise output as an observable acceptance criterion. |
| Important boundaries are omitted | Require material correctness boundaries by default and allow governing contracts to demand deeper coverage. |
| Generated targets drift | Preserve deterministic generation, archive validation, and packed installation smoke. |
| Existing custom-publisher code remains accidentally authoritative | Remove its selector registration and implementation surfaces in the replacement implementation. |
| Standard release publication partially fails | Use existing rerunnable closeout and publish a corrective patch; never rewrite an immutable release. |

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Prioritize user usability over exceptional release robustness | in scope | Goals; recommended direction |
| Keep the solution concise | in scope | Goals; non-goals; expected behavior changes |
| Make boundary-first automatic | in scope | Goals; expected behavior changes |
| Publish v0.4.0 | in scope | Recommended direction; rollout and rollback |
| Preserve essential correctness | in scope | Testing and verification strategy |
| Remove the custom checker and publisher burden | in scope | Architecture impact; scope budget |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Automatic concise boundary-first behavior | core to this proposal | This is the user-visible value. |
| Routine v0.4.0 package preparation | core to this proposal | It delivers that value. |
| Three-adapter and npm parity | same-slice dependency | Published targets must stay coherent. |
| Remove custom candidate and publication helpers | same-slice dependency | Their continued presence preserves the rejected complexity. |
| Existing release verification and closeout | same-slice dependency | These are the retained essential release boundary. |
| General complexity-budget governance | deferable follow-up | It should be learned from this incident without delaying v0.4.0. |
| Whole-workflow usability redesign | separate proposal | It is broader than this release. |

## Open Questions

None blocks proposal review.
The downstream spec should name the representative user journeys used to judge concise output and identify the exact existing release checks retained after custom-helper removal.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-06 | Prioritize user-facing activation and concise output. | RigorLoop is thin and the previous release design delayed all user value. | Continue hardening the custom publisher. |
| 2026-08-06 | Separate tree-local activation from public release proof. | They have different owners and coupling them created the candidate/tag circularity. | Candidate mode and P/B/T/R/C/H identity choreography. |
| 2026-08-06 | Reuse the routine release workflow. | Existing generation, verification, trusted publication, and closeout already cover essential risks. | New atomic publication component; dual release modes. |
| 2026-08-06 | Preserve v0.3.6 rollback. | It is the current immutable public baseline. | Constructed rollback bundle or tag rewrite. |

## Next Artifacts

- Proposal review.
- A replacement activation/release spec and spec review.
- Architecture assessment, including retirement of the custom publication ADR.
- A small execution plan and plan review.
- A focused test specification and test-spec review.
- Implementation, independent review, explanation, verification, and PR handoff.
- Explicit post-merge release publication and public closeout.

## Follow-on Artifacts

None yet

## Readiness

Ready for `proposal-review`.
Implementation is not yet allowed.
