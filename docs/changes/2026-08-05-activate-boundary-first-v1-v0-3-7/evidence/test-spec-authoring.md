# Test-Spec Authoring Evidence

- Artifact ID: `test-spec`
- Test spec: `specs/boundary-first-v1-v0-3-7-activation-release.test.md`
- Completion status: complete
- Next review: `test-spec-review-r2`

The proof map covers all 35 requirements, 15 acceptance criteria, eight
examples, 12 edge cases, eight boundaries, and seven selected interactions.
Sixteen outcome-focused test cases separate repository-local implementation
proof from the two explicit release-owned manual procedures.
The command ledger binds focused M1/M2 tests, release-mode M3/M4 validation,
strict-H and detached-T proof, atomic publication, and public closeout without
authorizing external mutation during implementation.

The R2 revision resolves the four first-pass findings: proof obligations use
the closed execution-level vocabulary; BFA-R017 has an M1 missing-evidence
regression plus M4 and release-checkpoint actual-state proof; atomic Git,
tag-workflow, and public closeout paths map to distinct commands and evidence;
and MP1/MP2 now define bounded, executable, auditable external procedures.
