# Review Resolution: Governed Lifecycle CLI

## Summary

Closeout status: closed

Review closeout: spec-review-r1
Review closeout: architecture-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2

- Reviews covered: `spec-review-r1`, `architecture-review-r1`, `code-review-m1-r1`, `code-review-m1-r2`
- Findings resolved: 9
- Unresolved findings: 0
- Current result: All accepted findings are resolved; M1 received a direct same-context clean review and user-directed continuation.

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| RLCLI-SR1 | accepted | resolved | Added the normative evidence-invalidation matrix and architecture constraint. |
| RLCLI-SR2 | accepted | resolved | Defined recovery-bundle, restoration, blocking, and repair outcomes. |
| RLCLI-SR3 | accepted | resolved | Separated stale-envelope failure from current-revision already-recorded success. |
| RLCLI-AR1 | accepted | resolved | Reconciled canonical hash-policy statements with activated freshness identity. |
| RLCLI-AR2 | accepted | resolved | Selected pinned `yaml`, closed input domain, and deterministic serialization. |
| RLCLI-AR3 | accepted | resolved | Defined fixed lock/recovery paths, phases, ordering, refusal, and repair. |
| RLCLI-CR-M1-1 | accepted | resolved | Enforced complete operation-specific request contracts and closed values. |
| RLCLI-CR-M1-2 | accepted | resolved | Added and proved the closed version-one provenance exclusion set. |
| RLCLI-CR-M1-3 | accepted | resolved | Admitted and validated only the documented request-provenance vocabulary. |

### code-review-m1-r2

#### RLCLI-CR-M1-3

Finding ID: RLCLI-CR-M1-3
Disposition: accepted
Rationale: Every approved request shape must be representable while unknown provenance continues to fail closed.
Status: resolved
Owner: implement
Owning stage: implement
Final action: Admitted only `actor` and `recorded_at`, validated non-empty actor and calendrically valid RFC 3339 timestamp values, and added accepted, malformed, and unknown-field regressions.
Validation target: `packages/rigorloop/test/lifecycle-contract.test.js`
Validation evidence: `evidence/m1-correction-r2.md`; formal rereview pending

### code-review-m1-r1

#### RLCLI-CR-M1-1

Finding ID: RLCLI-CR-M1-1
Disposition: accepted
Rationale: Incomplete requests must fail before transition consistency or mutation.
Status: resolved
Owner: implement
Owning stage: implement
Final action: Added closed per-operation required fields and validators for identifiers, paths, review authority, migration source version, repair conditions, and repair acknowledgment.
Validation target: `packages/rigorloop/test/lifecycle-contract.test.js`
Validation evidence: `evidence/m1-correction-r1.md`; formal rereview pending

#### RLCLI-CR-M1-2

Finding ID: RLCLI-CR-M1-2
Disposition: accepted
Rationale: The versioned lifecycle identity contract must exclude only documented provenance.
Status: resolved
Owner: implement
Owning stage: implement
Final action: Added the version-one `actor` and `recorded_at` exclusion set to code and the shared fixture, with regressions proving excluded provenance is stable and workflow state remains identity-relevant.
Validation target: `packages/rigorloop/test/lifecycle-contract.test.js`; shared conformance fixture
Validation evidence: `evidence/m1-correction-r1.md`; formal rereview pending

### spec-review-r1

#### RLCLI-SR1

Finding ID: RLCLI-SR1
Disposition: accepted
Rationale: Evidence freshness is a product contract and cannot be delegated to architecture.
Status: resolved
Owner: spec
Owning stage: spec
Final action: Added the closed first-release evidence-invalidation matrix and made architecture subordinate to its outcomes.
Validation target: `specs/governed-lifecycle-cli.md` at `sha256:f7d9984c6913f5326cce231874f57673835c25ed1d4c94a03bdf4437eba8e405`
Validation evidence: `evidence/spec-revision-r1.md`; `reviews/spec-review-r2.md`

### architecture-review-r1

#### RLCLI-AR1

Finding ID: RLCLI-AR1
Disposition: accepted
Rationale: Current canonical architecture must not contain both hash-based freshness and an unconditional no-hash rule.
Status: resolved
Owner: architecture
Owning stage: architecture
Final action: Qualified every legacy no-hash statement and made ADR-20260824 the scoped successor for activated freshness identities.
Validation target: canonical architecture at `sha256:911aafdbec7f124d92705dd0364183c7a4a805f8963a359553e17d343d2b3c95`
Validation evidence: `evidence/architecture-revision-r1.md`; `reviews/architecture-review-r2.md`

#### RLCLI-AR2

Finding ID: RLCLI-AR2
Disposition: accepted
Rationale: YAML parsing is a security, compatibility, dependency, and deterministic-output architecture choice.
Status: resolved
Owner: architecture
Owning stage: architecture
Final action: Selected the pinned `yaml` dependency, rejected unsafe YAML constructs, and defined normalized schema-ordered UTF-8/LF serialization.
Validation target: revised architecture and ADR identities from architecture-review r2
Validation evidence: `evidence/architecture-revision-r1.md`; `reviews/architecture-review-r2.md`

#### RLCLI-AR3

Finding ID: RLCLI-AR3
Disposition: accepted
Rationale: Same-worktree serialization and recovery must have one fault-injectable protocol before planning.
Status: resolved
Owner: architecture
Owning stage: architecture
Final action: Fixed sibling paths, exclusive-create semantics, modes, phases, recovery ordering, refusal behavior, cleanup, and orphan-lock repair.
Validation target: revised architecture and ADR identities from architecture-review r2
Validation evidence: `evidence/architecture-revision-r1.md`; `reviews/architecture-review-r2.md`

#### RLCLI-SR2

Finding ID: RLCLI-SR2
Disposition: accepted
Rationale: Atomicity and recovery require one observable outcome across crashes and post-validation failure.
Status: resolved
Owner: spec
Owning stage: spec
Final action: Added a verified recovery bundle, automatic restore, recovery-blocked state, and named reconciliation repair contract.
Validation target: `specs/governed-lifecycle-cli.md` at `sha256:f7d9984c6913f5326cce231874f57673835c25ed1d4c94a03bdf4437eba8e405`
Validation evidence: `evidence/spec-revision-r1.md`; `reviews/spec-review-r2.md`

#### RLCLI-SR3

Finding ID: RLCLI-SR3
Disposition: accepted
Rationale: The stale-revision invariant and idempotent result must be simultaneously testable.
Status: resolved
Owner: spec
Owning stage: spec
Final action: Preserved fail-closed stale revisions and defined current-revision equivalent operations as already recorded only when durable facts are identical.
Validation target: `specs/governed-lifecycle-cli.md` at `sha256:f7d9984c6913f5326cce231874f57673835c25ed1d4c94a03bdf4437eba8e405`
Validation evidence: `evidence/spec-revision-r1.md`; `reviews/spec-review-r2.md`
