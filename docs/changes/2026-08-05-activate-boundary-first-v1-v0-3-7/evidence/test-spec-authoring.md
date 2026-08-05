# Test-Spec Authoring Evidence

- Artifact ID: `test-spec`
- Test spec: `specs/boundary-first-v1-v0-3-7-activation-release.test.md`
- Completion status: complete
- Next review: `test-spec-review-r3`

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

The R3 correction links MP1 and its producing checkpoint/publication commands
directly from both recovery and external-environment proof obligations, so no
row claims atomic evidence without its actual authority-crossing procedure.

The M1 code-review amendment resolves `BFA-M1-CR1-005` by adding
`scripts/validation_selection.py` and `scripts/test-select-validation.py` to
CMD4's literal path set. Those are the selector implementation and regression
surfaces necessarily touched to support CMD4's tracked fixture directory. The
command remains read-only and retains the same owner, milestone, and failure
boundary.
