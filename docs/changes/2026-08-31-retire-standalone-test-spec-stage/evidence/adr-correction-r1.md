# ADR correction evidence R1

Artifact path: docs/adr/ADR-20260831-verification-ownership-without-test-spec-stage.md
Artifact identity: sha256:fb9409e89524101cc54cb0af1ab9d7a22b6472a7a2cabe556ac9aaf3a91e795e
Authoring result: complete

Finding addressed: RTS-DR1

The ADR now makes the primary architecture's v2 discriminator durable: a frozen activation manifest binds pre-activation IDs to v1 or legacy-unversioned classes, v2 is emitted for new changes, classification fails closed without inference, optional migration is identity-bound and workflow-owned, and post-v2 recovery cannot silently impose the prior test-spec graph.

Validation performed:

- `git diff --check` passed.
- The ADR decision agrees with the registered primary architecture at `sha256:98023a64b3248bd4095a25242dd830b7f71bff280f050127a1390f623175129c`.
