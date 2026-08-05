# ADR-20260805: Boundary-First Activation Candidate and Atomic Publication

## Owning change record

`docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/change.yaml`

## Context

Strict `boundary-first-v1` activation validation requires the immutable
activating tag to identify the unique pending-to-active transition. Creating
that public tag before review would make review follow publication, while
omitting strict proof would leave the release unverified. The final reviewed
branch also needs lifecycle evidence after the transition commit, so the
branch head and activation tag cannot be treated as one identity.

The approved release spec defines four identities on one first-parent chain:
publication base `P`, grandfathering baseline `B`, transition commit `T`, and
reviewed head `H`. It also requires exact compare-and-swap publication of
`main: P -> H` and `v0.4.0 -> T`, with both refs changing or neither.

## Decision

Add one release-specific, read-only candidate mode to the existing
boundary-first validator. The exact public command is:

```text
python scripts/validate-boundary-first.py --check --activation-candidate v0.4.0
```

Candidate mode obtains `P` from a fresh, successful remote query of
`refs/heads/main`; it does not fetch, mutate refs, or create evidence itself.
It derives `B` from `T`'s first parent, discovers the unique pending-to-active
`T`, and resolves `H` from `HEAD`. It accepts only the first-parent chain
`P ... B -> T ... H`, an absent local and remote `v0.4.0` tag, exact
`v0.3.6` rollback identity, complete activation/package identity, and no
release-gated path changes after `T`.

The command emits a stable machine-readable result containing `P`, `B`, `T`,
`H`, release, rollback, tag state, and bundle identity. Workflow-owned
candidate-verification evidence records that output; no new release profile,
activation-manifest field, transaction manifest, or mutable state store is
introduced.

Default validation remains strict. After candidate review, the release
operator creates local immutable tag `v0.4.0` at `T`, runs strict validation
from `H`, and runs the full release gate from a detached temporary worktree at
`T`. The tagged tree must contain every release input and must not read later
commits.

Publication uses one Git smart-protocol push with atomic capability:

```text
git push --atomic origin \
  <H>:refs/heads/main <T>:refs/tags/v0.4.0
```

The release command first proves `P` is an ancestor of `H`. It runs the plain
non-forced push with a temporary repository-owned pre-push guard that compares
the remote identities advertised for that same push with exact `P` for
`refs/heads/main` and the all-zero absent identity for `refs/tags/v0.4.0`.
The guard aborts before transfer on mismatch; Git's receive protocol rejects a
later race against the advertised old identities. An unexpected remote
identity, existing tag, non-fast-forward candidate, missing atomic capability,
or any ref rejection therefore fails the whole push. Force options and
sequential fallback are forbidden.

Only lifecycle evidence owned by this activation change may follow `T`.
Candidate validation compares `T..H`, reports every rejected path, and fails
on code, skill, resource, package, profile, release metadata, release note,
validator, generated-output, or other release-gated changes. If a payload fix
is needed after `T`, the branch and PR are superseded. A replacement branch is
created from the current authorized remote `main`, generates one new
transition, and repeats full validation and review without force-pushing the
invalid history.

## Alternatives considered

### Create the public activation tag before review

Rejected because immutable publication would precede the review and final
release gates that authorize it.

### Treat the reviewed head and transition tag as one commit

Rejected because code review, rationale, and verification evidence must be
recorded after the transition payload is complete, while the tag contract must
identify the unique pending-to-active commit.

### Add another activation or release transaction manifest

Rejected because the release profile and activation manifest already own
release state and activation identity. Candidate output plus existing
change-local verification evidence can record the four commit identities
without a competing state mechanism.

### Publish `main` and the tag sequentially

Rejected because either order can expose a mixed public state when the second
update fails.

### Repair an invalid transition with another payload commit

Rejected because release payload after `T` violates tagged-tree
self-containment and a second transition violates uniqueness. Replacement
history is the narrow non-destructive recovery.

## Consequences

- Pre-tag review can prove the exact activation bundle without weakening
  strict tag-context validation.
- Candidate evidence carries four explicit identities instead of overloading
  one base or head.
- Release publication depends on Git atomic-push support and exact lease
  behavior; unsupported remotes block rather than fall back.
- The tagged release remains reproducible even though later lifecycle evidence
  is present on `main`.
- Payload review findings after `T` are more expensive because they require a
  replacement branch and full rereview; this is the cost of immutable,
  single-transition publication.
- No new dependency, service, profile schema, activation-manifest field, or
  persistent state store is introduced.

## Follow-up

- Implement candidate validation, changed-path classification, strict split
  execution, and atomic publication support through the approved plan.
- Prove remote drift, unsupported atomic push, existing tag, tagged-tree
  self-containment, and replacement-candidate recovery in the matching test
  specification.
- Keep tag creation, remote mutation, GitHub release creation, and npm
  publication behind the explicit external-action checkpoint.
