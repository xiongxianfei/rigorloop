# Boundary-First v1 v0.4.0 Activation Release

## Owning change record

`docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/change.yaml`

## Related proposal

`docs/proposals/2026-08-05-activate-boundary-first-v1-v0-3-7.md`

This specification narrows and composes the approved boundary-first proof,
progressive-guidance, release-process, and release-transaction contracts for
the `v0.4.0` activation. Non-conflicting requirements in those contracts remain
in force.

## Goal and context

Activate the complete `boundary-first-v1` package in stable release `v0.4.0`
without requiring an immutable public tag before the exact activation candidate
can be reviewed.

The release uses two reviewed commit identities on one first-parent chain:
remote `main` advances to the final reviewed evidence-bearing head, while
`v0.4.0` identifies the earlier pending-to-active transition commit. Candidate
validation is pre-tag proof only. Default and release-context validation remain
strict and require the real tag before publication.

## Glossary

- `candidate mode`: explicit pre-tag validation for a proposed active release;
  it does not claim publication or active public availability.
- `transition commit`: the unique first-parent commit that changes the activation
  record from `pending` to `active`.
- `reviewed head`: the final reviewed branch head containing required lifecycle
  evidence after the transition commit.
- `publication base`: the exact remote `main` commit `P` recorded when the
  candidate is created and used for publication compare-and-swap.
- `grandfathering baseline`: transition `T`'s exact first parent `B`, recorded
  by the activation manifest under the standing boundary-first contract.
- `strict mode`: the existing default validation that requires the immutable
  activating tag and its exact commit relationship.
- `tagged tree`: repository content reachable from the transition commit selected
  by `v0.4.0`.
- `atomic publication`: one remote transaction that fast-forwards `main` to the
  reviewed head and creates `v0.4.0` at the transition commit, or changes neither.

## Examples first

Example E1: candidate validation succeeds before the tag exists
Given remote `main` publication base `P` precedes or equals grandfathering
baseline `B`
And one active transition changes `B` to transition commit `T`
And reviewed head `H` contains `T` in its first-parent history
And `v0.4.0` does not exist locally or remotely
When candidate validation runs for `v0.4.0` at `H`
Then it validates `P`, `B`, `T`, `H`, rollback `v0.3.6`, the complete resource bundle,
and tag absence
And it reports candidate-ready without reporting an active published release.

Example E2: default validation remains strict
Given the same active tree but no `v0.4.0` tag
When ordinary boundary-first validation runs
Then it fails because the activating release tag does not exist.

Example E3: local tag enables strict release proof
Given candidate validation passed
And local immutable tag `v0.4.0` points to `T`
When strict boundary-first validation and the full release gate run from the
tagged tree
Then both require `v0.4.0` to resolve to `T` and `v0.3.6` to be its immediate
published predecessor.

Example E4: lifecycle evidence follows the transition
Given `T` contains every release and activation input
And commits after `T` change only the owning change's lifecycle evidence
When candidate validation runs at reviewed head `H`
Then it accepts the separate head and tag identities
And strict release proof remains reproducible from `T` without later evidence.

Example E5: base drift stops publication
Given candidate evidence was recorded against publication base `P`
And remote `main` advances to another commit before release
When atomic publication is attempted
Then the compare-and-swap fails, neither ref changes, and the candidate must be
rebased, regenerated, revalidated, and rereviewed.

Example E6: atomic ref update is unavailable
Given the remote cannot update the branch and tag atomically
When release publication is requested
Then publication stops before either ref changes
And no sequential branch-then-tag or tag-then-branch fallback is allowed.

Example E7: post-transition payload drift is detected
Given a commit after `T` changes a skill, resource, package, release profile, or
other release-gated input
When candidate validation runs at `H`
Then it fails, the invalid branch and PR are superseded without force-push,
And a replacement branch from the current authorized publication base creates
one new coherent transition and repeats full validation and review.

Example E8: publication partially fails outside the Git ref transaction
Given the atomic Git ref update succeeds and the tag workflow publishes one
public surface but another public surface fails
When release closeout runs
Then it records failed-during-publish or failed-after-publish evidence and uses
the standing fix-forward, dist-tag, deprecation, and rerunnable-closeout rules.

## Requirements

BFA-R001. The activating release MUST be stable release `v0.4.0`, npm package
version `0.4.0`, and npm dist-tag `latest`.

BFA-R002. The immutable rollback release MUST be `v0.3.6`, and strict release
validation MUST confirm it is the immediately preceding published semantic
version tag.

BFA-R003. The activation contract version MUST remain `boundary-first-v1` and
the governed skill inventory MUST remain exactly the ten skills named by the
approved progressive-guidance contract.

BFA-R004. Candidate validation MUST be opt-in through the exact command shape
`python scripts/validate-boundary-first.py --check --activation-candidate v0.4.0`.

BFA-R005. Without `--activation-candidate`, boundary-first validation MUST
retain the existing strict tag-existence, predecessor, tag-to-transition,
activation-immutability, baseline, resource, projection, and rollback checks.

BFA-R006. Candidate mode MUST require the activation record to be `active`, the
activating release to be `v0.4.0`, and the rollback release to be `v0.3.6`.

BFA-R007. Candidate mode MUST fail if `v0.4.0` already exists locally or is
observable on the configured remote. An unreachable remote tag check MUST be an
explicit blocking result, not a pass.

BFA-R008. Candidate mode MUST record the full publication-base identity `P`
from the exact remote `main` used to create the candidate and MUST require `P`
to equal or precede `B` in the candidate's first-parent history.

BFA-R009. Candidate mode MUST discover exactly one first-parent pending-to-active
transition `T` and MUST require the activation manifest's grandfathering
baseline to equal `T`'s full first-parent identity `B`.

BFA-R010. Candidate mode MUST identify the current full reviewed-head identity
`H` and require `T` to occur in `H`'s first-parent history.

BFA-R011. Candidate mode MUST validate every strict activation invariant that
does not logically require the absent `v0.4.0` tag, including exact resource,
manifest, projection, governed-skill, grandfathering, rollback-package, and
canonical-path identities.

BFA-R012. Candidate success MUST report `candidate_release`, `publication_base`,
`grandfathering_baseline`, `transition_commit`, `reviewed_head`,
`rollback_release`, and `tag_state` in a stable machine-readable result.

BFA-R013. Candidate output MUST use `tag_state: absent` and MUST NOT report
`activation: validated`, `published`, `active release`, or another strict-release
success claim.

BFA-R014. The transition commit's tagged tree MUST contain the release profile,
activation record, canonical resources, governed projections, package inputs,
release metadata, release notes, pending publication evidence, and every local
input required by strict boundary-first and full release verification.

BFA-R015. Commits after `T` and through `H` MUST change only lifecycle evidence
owned by this activation change and MUST NOT change activation, boundary,
skill, adapter, package, release-profile, release-metadata, release-note,
release-validation, generated-output, or other release-gated inputs.

BFA-R016. Candidate validation MUST fail with changed paths when BFA-R015 is
violated.

BFA-R017. Required proposal, spec, architecture, plan, test-spec, implementation,
code-review, rationale, and candidate-verification evidence MUST settle before
external ref publication. Evidence that follows `T` remains on `main` at `H`
and is not required inside the tagged tree unless another release contract
already requires it there.

BFA-R018. Before publication, the release operator MUST create local immutable
tag `v0.4.0` at `T` and MUST rerun ordinary strict boundary-first validation
from repository head `H` and full release verification from tagged tree `T`.

BFA-R019. Strict validation at `H` MUST require `v0.4.0` to resolve to `T`.
Full release verification at `T` MUST pass without reading later commits.

BFA-R020. External ref publication MUST use one atomic remote update that sets
`main` to `H` by fast-forward and creates `v0.4.0` at `T`.

BFA-R021. The atomic update MUST use compare-and-swap evidence that remote
`main` still equals publication base `P` immediately before the update.

BFA-R022. Base drift, a non-fast-forward result, an existing tag, an atomic
capability failure, or any ref rejection MUST leave both remote refs unchanged
and MUST stop publication.

BFA-R023. Sequential ref-update fallback MUST NOT be used. Base drift or an
atomic-ref failure MUST require candidate regeneration from the current
authorized publication base, followed by complete validation and rereview.

BFA-R024. Tag creation, remote ref mutation, GitHub release creation, npm
publication, and post-publication closeout MUST remain outside automatic
lifecycle continuation and require the explicit release action.

BFA-R025. The GitHub tag workflow MUST run the repository-owned full release
gate for `v0.4.0` before GitHub release or npm publication.

BFA-R026. Public publication MUST preserve trusted publishing, archive and
package integrity checks, packed non-dry-run smoke for Codex, Claude, and
opencode, registry verification, and live public `npx` smoke.

BFA-R027. Before the atomic remote update, rollback MUST delete or ignore only
the local candidate tag and leave remote `main`, public tags, GitHub Releases,
npm, and the pending public capability unchanged.

BFA-R028. After the remote update, Git ref rollback MUST NOT rewrite or delete
`v0.4.0`. Package recovery MUST use standing failed-release evidence,
fix-forward, dist-tag correction, deprecation, or later patch release rules.

BFA-R029. Runtime behavior rollback MUST select immutable `v0.3.6` packages and
MUST NOT construct a mixed resource bundle or overwrite `v0.4.0`.

BFA-R030. If GitHub/npm publication is partial or public evidence is delayed,
release evidence MUST remain open with the exact failed phase and rerunnable
closeout; it MUST NOT report successful publication.

BFA-R031. Candidate and strict validation diagnostics MUST identify the mode,
release, publication base, grandfathering baseline, transition commit,
reviewed head when available,
conflicting tag or drifted path, expected invariant, and corrective action.

BFA-R032. Candidate validation MUST be deterministic and side-effect free: it
MUST NOT create tags, commits, branches, archives, packages, release artifacts,
GitHub releases, npm publications, or remote mutations.

BFA-R033. Candidate validation MUST NOT weaken or bypass artifact-lifecycle,
skill, adapter, package, release, security, or selected CI checks owned by
changed paths.

BFA-R034. Release preparation and validation MUST suppress credentials, tokens,
OTPs, private environment values, usernames, hostnames, and machine-local
temporary paths from committed evidence and normal diagnostics.

BFA-R035. If any release-gated payload or transition input changes after `T`,
the unpublished candidate MUST be rejected. Recovery MUST create a replacement
branch from the current authorized publication base, generate exactly one new
pending-to-active transition, rerun all validation and review, and supersede the
invalid branch and PR without force-push or retaining the invalid transition in
the replacement branch's first-parent history.

## Inputs and outputs

Inputs:

- exact candidate release `v0.4.0`;
- activation record and its Git first-parent history;
- current `HEAD`, publication base `P`, grandfathering baseline `B`, and
  local/remote tag namespaces;
- canonical resource and projection identities;
- `v0.3.6` rollback tag and adapter artifact metadata;
- routine release profile, generated release surfaces, packages, and notes;
- review, rationale, verification, and release evidence;
- remote atomic-ref and compare-and-swap results;
- public GitHub/npm metadata after publication.

Outputs:

- machine-readable candidate validation result or bounded diagnostic;
- strict boundary-first and release-gate results;
- versioned release profile and generated release artifacts;
- atomic ref-update result;
- GitHub/npm publication and public-smoke evidence;
- failed-release and recovery evidence when applicable.

## State and invariants

- Public capability state is `pending` until remote `v0.4.0` exists and strict
  tag-context release validation succeeds.
- Candidate-ready is not published, active-public, tag-ready, or release-ready.
- `P` equals or precedes `B`; `B` is the first parent of `T`; `T` is in the
  first-parent history of `H`.
- Remote publication maps `main: P -> H` and creates `v0.4.0 -> T` atomically.
- The tagged tree `T` is self-contained for strict release validation.
- Later lifecycle evidence at `H` cannot change release-gated payload.
- `v0.3.6` remains the only rollback release for this activation.
- Published Git tags and npm versions are immutable.

## Error and boundary behavior

- Unknown or malformed candidate release values fail closed.
- Candidate mode with a pending manifest fails closed.
- Candidate mode with a pre-existing local or reachable remote tag fails closed.
- Multiple or absent activation transitions fail closed.
- Transition-parent, baseline, first-parent, resource, projection, package, or
  rollback mismatch fails closed.
- Release-gated changes after `T` fail closed with path evidence.
- Unreachable remote tag state blocks candidate success.
- Publication-base drift or ref conflict blocks both remote updates.
- Unsupported atomic ref updates block publication without sequential fallback.
- Strict gate failure after local tag creation deletes or abandons only the
  local tag and records failed-before-publish evidence.
- Partial public publication follows the standing release recovery contract.

## Compatibility and migration

Default boundary-first validation retains strict behavior. Existing pending
validation, active fixtures, historical releases, release profiles, and public
adapter installation remain compatible.

The new candidate flag is additive and valid only for the named `v0.4.0`
activation. It does not create a general way to validate arbitrary missing tags
or future releases. Generalization requires a later approved contract.

Grandfathered specifications are computed from baseline `B` under the
existing boundary-first rules. New specifications introduced after `B` are not
grandfathered.

## Observability

Candidate success emits one concise JSON result with mode, release, publication
base, grandfathering baseline, transition, head, rollback, tag state, and
validated bundle identity.

Failures emit stable issue codes and bounded expected/actual values. Remote
commands, release gates, and publication evidence record commit and tag
identities without secrets or machine-local paths.

Release evidence distinguishes candidate-ready, failed-before-publish,
failed-during-publish, failed-after-publish, published-with-closeout-pending,
and closed outcomes according to standing release contracts.

## Security and privacy

Candidate validation is read-only and requires no publishing credentials.
Remote publication uses the existing authenticated Git boundary and trusted
npm publishing workflow. No credential value is written to repository evidence
or normal output.

Atomic publication must reject unexpected remote identities and must not use
force push, tag overwrite, sequential fallback, or mutable published artifacts.

## Accessibility and UX

No graphical UI is introduced. CLI success remains concise and machine-readable;
failure output names the blocked phase and corrective action without requiring
maintainers to infer whether candidate or strict mode ran.

## Performance expectations

Candidate validation SHOULD finish within the existing focused
boundary-first-validation budget and MUST NOT run full adapter archive or public
network smoke itself. Release preflight and full release verification retain
their existing performance and timing-evidence contracts.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: BFA-R001 through BFA-R035

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | BFA-R004, BFA-R006, BFA-R007, BFA-R031 | BND-INPUT-001 | - |
| state-lifecycle | applicable | BFA-R005, BFA-R006, BFA-R013, BFA-R017, BFA-R024 | BND-STATE-001 | - |
| identity-authority | applicable | BFA-R008, BFA-R009, BFA-R010, BFA-R012, BFA-R014, BFA-R018, BFA-R019, BFA-R020, BFA-R021 | BND-AUTH-001 | - |
| composition-path | applicable | BFA-R005, BFA-R014, BFA-R018, BFA-R019, BFA-R025, BFA-R026, BFA-R033 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | BFA-R015, BFA-R016, BFA-R021, BFA-R022, BFA-R023, BFA-R035 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | BFA-R022, BFA-R023, BFA-R027, BFA-R028, BFA-R030, BFA-R035 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | BFA-R002, BFA-R003, BFA-R005, BFA-R029 | BND-COMPAT-001 | - |
| external-environment | applicable | BFA-R007, BFA-R020, BFA-R022, BFA-R025, BFA-R030 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | BFA-R004, BFA-R006, BFA-R007, BFA-R031 | absent flag; exact v0.4.0 flag; malformed or other release; local tag absent/present; remote reachable/unreachable | Candidate mode is explicit, named, and tag-absent only. | Exact input validates; unknown, conflicting, or unreachable input stops with bounded diagnostics. | BFA-R004 |
| BND-STATE-001 | state-lifecycle | BFA-R005, BFA-R006, BFA-R013, BFA-R017, BFA-R024 | pending; candidate-active/unpublished; locally tagged/strictly verified; remotely tagged/publishing; published/closeout pending; closed | Candidate state never claims public activation; external transitions require explicit action and strict gates. | Legal transitions advance with evidence; premature or mixed state stops. | BFA-R013 |
| BND-AUTH-001 | identity-authority | BFA-R008, BFA-R009, BFA-R010, BFA-R012, BFA-R014, BFA-R018, BFA-R019, BFA-R020, BFA-R021 | publication base P; grandfathering baseline B; transition T; reviewed head H; rollback tag; activating tag; remote main | P equals or precedes B, B is T's first parent, T is in H's first-parent history, main advances P to H, and tag maps to T; T is release-self-contained. | Exact identities and tagged-tree proof pass; drift, ambiguity, mismatch, stale authority, or missing self-containment stops. | BFA-R020 |
| BND-COMPOSE-001 | composition-path | BFA-R005, BFA-R014, BFA-R018, BFA-R019, BFA-R025, BFA-R026, BFA-R033 | candidate CLI; default validator; strict validation at H; full release verification at T; tag workflow; package/archive checks; public closeout | Candidate mode changes only absent-tag authority; the tagged tree is self-contained; every sibling gate retains ownership. | Complete composed path publishes; bypass, post-T dependency, or omitted gate blocks. | BFA-R033 |
| BND-TEMPORAL-001 | temporal-retry | BFA-R015, BFA-R016, BFA-R021, BFA-R022, BFA-R023, BFA-R035 | transition before evidence; repeated candidate check; payload drift after T; publication-base drift; local tag retry; atomic push retry; replacement candidate | Release-gated payload is fixed at T; changed paths fail; retry never overwrites refs, retains an invalid transition, or reuses stale evidence. | Idempotent read checks pass; drift or failed atomic update requires a fresh candidate and rereview. | BFA-R023 |
| BND-RECOVERY-001 | failure-recovery | BFA-R022, BFA-R023, BFA-R027, BFA-R028, BFA-R030, BFA-R035 | invalid unpublished transition; pre-push failure; atomic-ref rejection; failed-during-publish; failed-after-publish; delayed public evidence | Invalid unpublished history is superseded by a replacement branch from current P; pre-push leaves remote unchanged; post-push never rewrites immutable artifacts. | Replace and rereview before publication, abandon local state, or use standing fix-forward/closeout recovery after publication. | BFA-R035 |
| BND-COMPAT-001 | compatibility-migration | BFA-R002, BFA-R003, BFA-R005, BFA-R029 | pending/default strict; active v0.4.0; v0.3.6 rollback; historical fixtures | boundary-first-v1 and default strict behavior remain stable; rollback is one immutable release. | Compatible paths remain valid; mixed or older rollback fails. | BFA-R005 |
| BND-ENV-001 | external-environment | BFA-R007, BFA-R020, BFA-R022, BFA-R025, BFA-R030 | local Git; reachable/unreachable remote; atomic-capable/incapable remote; GitHub workflow; npm/public network | External uncertainty never becomes success; atomic refs precede public package claims. | Available exact dependencies advance; unavailable, partial, or uncertain dependencies block or remain open. | BFA-R022 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | BFA-R005, BFA-R007, BFA-R013 | BND-INPUT-001, BND-STATE-001 | Candidate flag or absent tag is mistaken for public activation. | Candidate output is explicitly non-public; default strict mode still fails without the tag. |
| INT-002 | BFA-R008, BFA-R009, BFA-R010, BFA-R012, BFA-R014, BFA-R015, BFA-R016, BFA-R019, BFA-R020 | BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001 | P, B, T, and H are conflated; the tagged tree depends on later content; or later evidence mutates release payload. | Candidate records all four identities, proves T is self-contained, and rejects post-transition release-gated drift with changed paths. |
| INT-003 | BFA-R020, BFA-R021, BFA-R022 | BND-AUTH-001, BND-ENV-001 | Remote main changes or atomic ref capability is absent. | Compare-and-swap and atomic update change both refs or neither. |
| INT-004 | BFA-R018, BFA-R019, BFA-R025, BFA-R033 | BND-COMPOSE-001, BND-AUTH-001 | Candidate validation substitutes for strict release verification. | Local tag and strict full release gates run before remote publication. |
| INT-005 | BFA-R027, BFA-R028, BFA-R030 | BND-RECOVERY-001, BND-STATE-001, BND-ENV-001 | Failure crosses from reversible local state into immutable partial publication. | Pre-push abandons locally; post-push records exact state and fixes forward without overwrite. |
| INT-006 | BFA-R002, BFA-R029 | BND-COMPAT-001, BND-RECOVERY-001 | Recovery selects mixed or non-predecessor packages. | Rollback selects exact immutable v0.3.6 artifacts or fails closed. |
| INT-007 | BFA-R016, BFA-R023, BFA-R035 | BND-TEMPORAL-001, BND-RECOVERY-001 | A payload correction is appended after T or a second transition is added to the same candidate history. | Supersede the invalid branch and PR; rebuild one transition from current authorized P; repeat validation and review without force-push. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | BFA-R004, BFA-R006, BFA-R008, BFA-R009, BFA-R010, BFA-R012 | BND-INPUT-001, BND-AUTH-001 | - | - |
| E2 | regression | BFA-R005 | BND-INPUT-001, BND-COMPAT-001 | REG-BFA-001 | - |
| E3 | illustration | BFA-R018, BFA-R019 | BND-AUTH-001, BND-COMPOSE-001 | - | - |
| E4 | regression | BFA-R014, BFA-R015, BFA-R016 | BND-AUTH-001, BND-TEMPORAL-001 | REG-BFA-002 | - |
| E5 | regression | BFA-R021, BFA-R022, BFA-R023 | BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001 | REG-BFA-003 | - |
| E6 | regression | BFA-R020, BFA-R022 | BND-COMPOSE-001, BND-ENV-001 | REG-BFA-004 | - |
| E7 | regression | BFA-R015, BFA-R016, BFA-R023, BFA-R035 | BND-TEMPORAL-001, BND-COMPOSE-001, BND-RECOVERY-001 | REG-BFA-005 | - |
| E8 | illustration | BFA-R028, BFA-R030 | BND-STATE-001, BND-RECOVERY-001, BND-ENV-001 | - | - |

## Edge cases

EC1. `--activation-candidate` is present without `--check`; argument validation
fails without mutating state.

EC2. Candidate release is `v0.4.1`, a prerelease, malformed, or not equal to the
manifest release; validation fails closed.

EC3. `v0.4.0` exists locally but not remotely, or remotely but not locally;
candidate mode reports the conflicting namespace and stops.

EC4. Remote tag lookup is unavailable; candidate mode blocks rather than
assuming absence.

EC5. The branch has zero or multiple pending-to-active transitions; validation
fails.

EC6. `T` is reachable from `H` only through a non-first-parent path; validation
fails.

EC7. A documentation-only lifecycle receipt follows `T`; candidate validation
accepts it when no release-gated input changes.

EC8. A review fix changes code, a skill, release notes, or release metadata after
`T`; the candidate is invalid. Its branch and PR are superseded, and a new branch
from the current authorized `P` generates one replacement transition before full
validation and rereview.

EC9. Remote `main` changes after candidate verification; compare-and-swap blocks
both ref updates.

EC10. The remote rejects atomic pushes; no sequential fallback occurs.

EC11. Strict validation passes at `H` but full release verification fails at
tagged tree `T`; publication stops and the local tag is abandoned.

EC12. Git refs publish atomically but npm trusted publication fails; release
evidence records the partial public state and applies standing recovery.

## Non-goals

- No new boundary vocabulary, governed skill, runtime flag, or per-install activation.
- No generalized missing-tag candidate mode for releases after `v0.4.0`.
- No weakening of default strict activation or release verification.
- No normal merge commit, force push, tag overwrite, or sequential ref fallback.
- No redesign of release profiles, package contents, adapters, trusted publishing, or public closeout.
- No automatic authorization for merge, tag, push, GitHub release, npm publish, or rollback.
- No historical release or accepted-spec rewrite.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC-BFA-001 | Exact candidate command validates a complete active v0.4.0 tree without requiring the absent tag and emits non-public candidate status. |
| AC-BFA-002 | Default validation still fails an active tree whose activating tag is absent. |
| AC-BFA-003 | Candidate validation records exact P, B, T, and H identities and requires the first-parent chain `P ... B -> T ... H`. |
| AC-BFA-004 | Candidate validation proves v0.3.6 is the rollback predecessor and validates exact resource/package identities. |
| AC-BFA-005 | Post-transition release-gated drift fails with changed-path evidence. |
| AC-BFA-006 | The tagged transition tree contains every input needed by strict validation and full release verification. |
| AC-BFA-007 | Local v0.4.0 at T makes strict validation pass at H and the full release gate pass at T before remote mutation. |
| AC-BFA-008 | Base drift, tag conflict, non-fast-forward, or missing atomic capability changes neither remote ref. |
| AC-BFA-009 | Authorized publication atomically advances main from P to H and maps v0.4.0 to T. |
| AC-BFA-010 | Tag workflow preserves full GitHub/npm/archive/package/smoke gates and trusted publication. |
| AC-BFA-011 | Pre-push failure abandons only local candidate state; post-push failure records immutable recovery evidence. |
| AC-BFA-012 | v0.3.6 rollback packages remain exact and mixed rollback fails closed. |
| AC-BFA-013 | Candidate validation is deterministic, side-effect free, bounded, and credential-free. |
| AC-BFA-014 | Every BFA-R001 through BFA-R035 requirement has direct automated or explicitly release-owned proof in the matching test specification. |
| AC-BFA-015 | A post-T release-gated change rejects the unpublished candidate and requires a replacement branch from current authorized P, one new transition, complete validation, and rereview without force-push. |

## Open questions

None. Exact internal function boundaries and stable issue-code names may be
selected in architecture and planning without changing observable behavior.

## Next artifacts

- Spec review.
- Architecture assessment and, because ref authority and validation phases are
  affected, architecture plus architecture review.
- Execution plan and plan review.
- Matching test specification and test-spec review.
- Implementation and independent code review.
- Explanation, verification, and PR handoff.
- Explicit atomic release publication and public closeout after the external
  action checkpoint.

## Follow-on artifacts

None yet

## Readiness

Ready for `spec-review`. Implementation is not yet allowed.
