# Verify Skill Simplification Test-Spec Review R1

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: r1
Reviewer: Codex independent test-spec-review context
Target: `specs/verify-skill-simplification.test.md`
Review date: 2026-08-11
Status: changes-requested
Review status: changes-requested
Material findings: VFSIM-TSR1
Immediate next stage: test-spec revision
Implementation handoff: not-allowed

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: VFSIM-TSR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-11-verify-skill-simplification/reviews/test-spec-review-r1.md`
- Review log: `docs/changes/2026-08-11-verify-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-11-verify-skill-simplification/review-resolution.md`
- Open blockers: VFSIM-TSR1
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: formal test-spec review recorded; implementation remains blocked pending revision and rereview

## Finding VFSIM-TSR1

Finding ID: VFSIM-TSR1
Severity: major
Location: `specs/verify-skill-simplification.test.md` proof rows `PRF-002`, `PRF-005`, and `PRF-006`; test `T13`
Evidence: `PRF-002` and `PRF-005` include R33 and T13 but declare M2 as their required milestone even though the approved plan assigns rollout, rollback, mixed-package, and installed-package proof to M3. `PRF-005` and `PRF-006` cite T13 without citing the M3 adapter commands that can exercise package failure and recovery. T13 itself cites only CMD7, which validates a complete generated package, and CMD9, which validates change metadata; neither command exercises its stated incomplete-package and prior-package rollback fixtures. CMD6 is the approved M3 owner for adapter-distribution failure fixtures.
Required outcome: Align every affected proof row with M3 and the commands and evidence that directly establish rollout, rollback, mixed-package failure, and recovery. Make T13 cite the adapter-distribution proof owner, or narrow T13 so its commands establish every claimed outcome.
Safe resolution path: Revise `PRF-002`, `PRF-005`, and `PRF-006` to use the correct required milestone, command set, and M3 evidence; add CMD6 to T13 and its direct proof rows for incomplete/mixed/rollback fixtures while retaining CMD7 for the selected valid package path and CMD9 for lifecycle metadata. Re-run boundary and lifecycle validation, then request a new test-spec review.
needs-decision rationale: none

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Governing-contract alignment | pass | The test spec operationalizes the approved spec and plan without changing product behavior. |
| Requirement coverage | concern | All R1-R33 are mapped, but R33 proof timing and commands are inconsistent. |
| Example coverage | pass | E1-E8 map to stable tests. |
| Negative and boundary coverage | pass | Failure, stale, ambiguous, cross-target, missing-resource, and mixed-package cases are represented. |
| Proof-level adequacy | concern | Rollback proof names an end-to-end package outcome without a command that exercises its failure fixture. |
| Milestone mapping | block | M3 rollback work is claimed complete by M2 proof rows. |
| Command validity | block | T13's CMD7 and CMD9 cannot establish its incomplete/mixed-package rollback outcome; CMD6 is the approved fixture owner. |
| Fixture and data design | pass | Static records and temporary package roots are deterministic and bounded. |
| Manual-proof boundary | pass | MP0 and MP1 are exact, justified, owned, and evidenced. |
| Observability | pass | Tests and commands identify IDs, evidence artifacts, and failure meaning. |
| Determinism and isolation | pass | Proof excludes network, publication, credentials, and target-agent execution. |
| Scope and non-goals | pass | No runtime journey, tokenizer gate, or new permanent validator is introduced. |
| Execution economics | pass | Focused M1/M2 proof is separated from broader M3 package proof. |
| Traceability | concern | Coverage is complete by ID, but the affected proof rows do not trace to the actual producing commands and milestone. |
| Implementation handoff | block | M3 rollback behavior would require implementation-time guessing. |

## No-finding areas

- All 33 requirements, 8 examples, 8 boundary IDs, and 6 selected interaction IDs have explicit proof-map rows.
- CMD1 matches the approved plan and rejects unknown closed values before dependent consistency checks.
- CMD7 uses the trusted immutable `v0.3.6` fixture, checked subprocesses, and an automatically cleaned temporary directory.
- Static scenarios, package validation, and manual semantic review explicitly exclude Codex, Claude Code, opencode, or another target-agent runtime.
