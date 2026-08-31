## Result

Milestone: M1
Validation result: passed

## Core result

- Skill: implement
- Status: implemented
- Completed scope: Added the inactive lifecycle-contract activation model, deterministic v2/v1/legacy classification, exact prior-contract manifest matching, fail-closed vocabulary and ordering checks, reader diagnostics, and explicit v1 new-change scaffolding.
- Artifacts changed: `specs/lifecycle-contract-activation.yaml`; `schemas/lifecycle-contract-activation.schema.json`; `schemas/change.schema.json`; lifecycle contract, reader, and new-change modules; shared Node/Python fixtures and focused regressions.
- Tests added or updated: TS-001, TS-002, and TS-015 coverage for explicit v2, manifest-matched v1 and legacy-unversioned records, missing and mismatched membership, duplicate and raw-UTF-8-unsorted entries, unknown contract/class/activation-state values including explicit null, active test-spec state under v2, public repository-validator integration, invalid tracked manifests, heuristic-independence, reader diagnostics, and v1 scaffold preservation.
- Validation performed: CMD-01, CMD-03, CMD-04, and `git diff --check`.
- Validation result: after the R1 corrections, CMD-01 passed 173 Node tests with an isolated temporary root; CMD-03 passed 75 Python tests; CMD-04 passed 165 Python tests; whitespace validation passed.
- Open blockers: none.
- Next stage: code-review.
- Claim limitations: v2 routing, v2 package authority, lifecycle migration, activation, rollback, skill retirement, and adapter publication remain outside M1. The tracked manifest remains `preactivation`, has no activating revision or compatibility entries, and grants no v2 authority.

## Planned milestone

- Change ID: `2026-08-31-retire-standalone-test-spec-stage`
- Plan identity: `docs/plans/2026-08-31-retire-standalone-test-spec-stage.md`, sha256 `727b5a71f1d5ce001876cde59f195536c9671b4743e50a70ef95cf437ccc9938`.
- Milestone ID: M1.
- Milestone state: implementation complete; ready for the guarded `review-requested` transition.
- Baseline or change-pack status: Delivery Review package `delivery-review-r3` is current and granted; lifecycle initialization selected M1 and preserved the approved package identities.
- Milestone validation evidence: this file.
- Commit status: the M1 correction implementation commit is the Code Review R2 target; its exact identity is supplied by the tracked handoff and Git history rather than self-referenced from this evidence file.
- Code-review handoff: review schema closure, identical Node/Python classification, raw UTF-8 manifest determinism, bounded prior compatibility, inactive v2 behavior, and explicit v1 new-change output.

## Test-first record

The first focused run failed because the classifier exports and Python compatibility functions did not yet exist, the reader exposed no compatibility classification, and an active manifest did not constrain prior records. After those paths passed, the complete CMD-01 run exposed that `new-change` was still unversioned. The scaffold was corrected to emit a v1 draft at `proposal`, and CMD-01 then passed in full.

No in-place migration operation was added. Existing prior records keep their registered contract; the optional migration decision remains deferred by the approved architecture and plan.

## Code Review M1 R1 correction

- Findings addressed: `RTS-M1-CR1`, `RTS-M1-CR2`.
- Test-first evidence: the new Python explicit-null and public-validator tests failed before implementation because null fell through to legacy classification, `validate_file` accepted no activation-manifest input, and artifact lifecycle validation did not load or apply the tracked manifest. The matching Node explicit-null fixture already passed, demonstrating the cross-runtime divergence directly.
- Implementation: Python now distinguishes an absent lifecycle contract from an explicitly null or otherwise unknown value. Change-metadata validation loads the tracked activation manifest and invokes the shared classifier before v1 consistency checks. Artifact-lifecycle validation reads the manifest from the validated repository or tracked revision, validates it once, classifies every governed record, and blocks classifier failures before contract-specific state validation.
- Boundary preservation: a plain v2 record remains classified but inactive during preactivation; v2 routing and package semantics remain M2 work. Repositories without this repository-specific activation manifest retain their existing validation behavior. New-change continues to emit v1.
- Public-boundary proof: change-metadata validation rejects v2 active test-spec state; artifact-lifecycle validation rejects v2 active test-spec state, prior-contract records missing from an active manifest, and invalid activation-manifest vocabulary.
- Unaffected with rationale: Node classification logic required no production change because it already rejected explicit null and already powered runtime readers. Schemas, the preactivation manifest, new-change scaffolding, lifecycle routing, package authority, and generated adapters are unchanged because the corrections complete M1 classification integration without entering M2 or activation scope.
- Validation note: the first ordinary CMD-01 rerun encountered an ambient `/tmp/docs/changes/dead-end` directory through the test helper's parent-directory repository discovery. Repeating the exact command with `TMPDIR=/dev/shm` isolated the fixture root and passed all 173 selected tests; no implementation change was made for this unrelated environment dependency.
