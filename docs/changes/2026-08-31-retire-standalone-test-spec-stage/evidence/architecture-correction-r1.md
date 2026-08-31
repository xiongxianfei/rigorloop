# Architecture correction evidence R1

Artifact path: docs/architecture/2026-08-31-retire-standalone-test-spec-stage.md
Artifact identity: sha256:98023a64b3248bd4095a25242dd830b7f71bff280f050127a1390f623175129c
Authoring result: complete

Finding addressed: RTS-DR1

The revised architecture selects `stage-owned-change-local-v2` for the no-test-spec graph and one frozen activation manifest binding every pre-activation change ID to its observed v1 or legacy-unversioned class. It defines new-change behavior, exact record classification, completed-history interpretation, optional identity-bound migration, contradiction and unknown-value failures, and the different safe recovery boundaries before and after the first v2 record. No date, artifact-presence, Git-reachability, or network inference remains. The matching ADR correction follows through the second architecture-owned correction target before Design Review resumes.

Validation performed:

- `git diff --check` passed.
- The exact SHA-256 identity for the revised primary architecture is recorded above.
- The unchanged specification's RTS-R20 through RTS-R23, BND-STATE-001, BND-RECOVERY-001, BND-COMPAT-001, INT-001, and INT-005 now have an explicit architecture realization.
