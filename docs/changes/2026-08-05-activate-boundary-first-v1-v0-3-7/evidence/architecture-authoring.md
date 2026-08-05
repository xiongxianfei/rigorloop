# Architecture Authoring Evidence

- Architecture surface: canonical-update and ADR
- Canonical package: `docs/architecture/system/architecture.md`
- Diagram: `docs/architecture/system/diagrams/component-boundary-guidance.mmd`
- ADR: `docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md`
- Completion status: complete
- Next review: `architecture-review-r1`

## Design result

The design reuses the existing routine release profile, activation manifest,
boundary validator, full release gate, and Git transport. It adds no manifest,
service, dependency, or persistent state owner.

Candidate validation reads a fresh remote advertisement and emits exact
publication base `P`, grandfathering baseline `B`, transition `T`, and reviewed
head `H` evidence. Default validation remains strict. The full release gate
runs from a detached worktree at `T`, while strict boundary validation runs
from `H` with local tag `v0.4.0 -> T`.

Publication uses a plain non-forced `git push --atomic`. A temporary pre-push
guard compares the identities advertised for that same push with `main == P`
and an absent tag; Git's receive-side old-identity check rejects a later race.
Sequential fallback is forbidden. Release-gated drift after `T` requires a
replacement branch and review rather than another transition or history
rewrite.

## Requirement mapping

| Spec requirements | Architecture ownership |
| --- | --- |
| BFA-R004-R013, BFA-R031-R034 | Existing boundary validator gains one explicit read-only candidate entry point and stable JSON result. |
| BFA-R008-R012 | Candidate validator derives and reports `P ... B -> T ... H`. |
| BFA-R014-R019 | Path classifier freezes release payload at `T`; strict validation runs at `H`; full release verification runs at `T`. |
| BFA-R020-R023 | Guarded non-forced atomic push owns exact CAS and all-or-neither ref mutation. |
| BFA-R024-R030 | Existing explicit release operator, tag workflow, trusted publication, closeout, and immutable rollback boundaries remain authoritative. |
| BFA-R035 | Invalid unpublished history is superseded and regenerated once from current authorized remote main. |

## Alternatives and consequences

Rejected alternatives are public tag creation before review, conflating `H`
with `T`, another candidate manifest, sequential ref publication, and in-place
repair after `T`. The chosen design makes post-transition payload fixes more
expensive, but preserves one immutable transition, exact tagged-tree proof, and
atomic publication without a competing state model.

## Validation target

Architecture review should challenge same-push remote identity authority,
plain atomic Git behavior without force options, the `T..H` permitted-path
boundary, detached tagged-tree verification, absence of new mutable state, and
replacement-candidate recovery.
