# Boundary-First v1 Activation Release Research

## Decision to support

Choose the release identity, rollback target, and release path for activating
the merged `boundary-first-v1` capability.

## Questions answered

1. What is the current public RigorLoop release?
2. What is the smallest compatible release target?
3. Does the repository already provide a routine release transaction path?
4. Which state and external boundaries must remain explicit?

## Summary conclusion

GitHub Releases, Git tags, and the npm registry all identify `v0.3.6` as the
current public release. The next semantic version depends on the standing
release-classification contract, while `v0.3.6` is the immutable rollback
candidate.

The repository already provides profile-driven release preparation, preflight,
verification, trusted publication, and rerunnable public closeout. The change
should use those surfaces and should not introduce another activation or
release mechanism.

## Evidence table

| Source | Finding | Confidence | Relevance |
| --- | --- | --- | --- |
| `gh release list --limit 5` on 2026-08-05 | `v0.3.6` is marked Latest. | high | Establishes the current GitHub release. |
| `npm view @xiongxianfei/rigorloop version --json` on 2026-08-05 | npm reports `0.3.6`. | high | Establishes the current public package version. |
| Local Git tags after `git fetch origin` | `v0.3.6` is the highest version tag. | high | Confirms repository release history agrees with public surfaces. |
| `docs/releases/profiles/v0.3.6.yaml` | Routine releases use a typed profile with three targets and required publication evidence. | high | Defines the reusable release path. |
| `scripts/prepare-release.py`, `scripts/release-preflight.py`, `scripts/release-verify.sh`, and `scripts/close-release-publication.py` | Existing tooling owns preparation, cheap failure detection, the full gate, and public closeout. | high | Avoids a second mechanism. |
| `specs/boundary-first-activation.yaml` | The capability remains `pending` with no activating or rollback release. | high | Identifies the remaining activation transition. |

## Implications for proposal, specification, architecture, and tests

- The proposal should apply REL-R9 through REL-R10: activation adds public skill
  behavior and therefore uses the next stable minor release, `v0.4.0`.
- The approved progressive boundary-first specification remains the normative
  activation contract; any version-specific contract should amend only the
  release transaction and activation identities.
- Existing release and boundary-first architecture is sufficient unless review
  discovers a conflicting state transition.
- Tests must prove the `pending` to `active` transition, exact resource hashes,
  adapter parity, `v0.3.6` rollback selection, package installation, release
  preflight, and full release verification.
- Tag creation and publication remain explicit external actions after reviewed
  and verified release preparation.

## Remaining uncertainty

The trusted-publishing workflow and registry credentials cannot be proven by
local preparation alone. Hosted release execution and post-publication evidence
must be observed when publication is explicitly authorized.

## Recommendation

Proceed with a routine stable `v0.4.0` activation release, use `v0.3.6` as the
rollback release, reuse the profile-driven release transaction, and keep tag
publication outside automatic workflow continuation.
