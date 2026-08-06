# Usability-First Boundary-First v0.4.0 Test-Spec Review R1

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: 1
Reviewer: Codex independent test-spec-review peer
Target: specs/usability-first-boundary-release.test.md
Review date: 2026-08-06
Status: changes-requested
Review status: changes-requested
Material findings: UBR-TSR1-001
Immediate next stage: test-spec revision
Implementation handoff: not-allowed
Automatic downstream handoff: none

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: `UBR-TSR1-001`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/test-spec-review-r1.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md#test-spec-review-r1`
- Open blockers: `UBR-TSR1-001`
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: M1 proof currently depends on an M2-owned command.

## Review inputs

- Test spec: `specs/usability-first-boundary-release.test.md`
- Authoring evidence: `docs/changes/2026-08-06-usability-first-boundary-release/evidence/test-spec-authoring.md`
- Approved feature spec: `specs/usability-first-boundary-release.md`
- Approved spec review: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/spec-review-r3.md`
- Approved plan: `docs/plans/2026-08-06-usability-first-boundary-release.md`
- Approved plan review: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/plan-review-r2.md`
- Approved architecture and ADR review: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/architecture-review-r2.md`
- Boundary-first review method: `.agents/skills/test-spec-review/references/boundary-first-method-v1.md`

The review confirmed 20 requirement rows, 12 acceptance-criterion rows, six example rows, ten edge-case rows, 11 boundary or interaction obligations, 23 test cases, 18 command entries, and four milestone proof rows. All 18 command paths exist; `v0.4.0` support is correctly implementation-owned rather than claimed as already passing.

## Findings

## Finding UBR-TSR1-001

Finding ID: UBR-TSR1-001
Severity: major
Location: `specs/usability-first-boundary-release.test.md`, T23, CMD06, and the M1 milestone proof row
Evidence: T23 is marked `Required by milestone: M1`, and M1 lists T23 as required before code-review M1. T23 names only CMD06, `python scripts/test-boundary-first-validation.py`. The command ledger assigns CMD06 to M2 and makes it first required at code-review M2; the approved plan likewise lists that command under M2, not M1. M1 therefore cannot execute all required proof using commands owned and available at its own closeout boundary.
Required outcome: Make every M1-required test executable through M1-owned commands while preserving direct proof for UBR-R005 and AC-UBR-012. No M1 closeout obligation may depend on a command whose ownership begins in M2.
Safe resolution path: Keep T4 as M1's direct UBR-R005 ownership proof. Move T23 and AC-UBR-012's fail-closed proof-map mutation coverage to M2, add T23 to the M2 milestone row, and remove T23 from M1. If M1 still needs a current-artifact structural check, cite existing M1-owned CMD05 without moving CMD06 or changing the approved plan.
needs-decision rationale: none; the approved plan and command ledger already determine the milestone owners.

## Review dimensions

| Dimension | Verdict | Evidence |
| --- | --- | --- |
| Governing-contract alignment | pass | The proof map operationalizes all UBR requirements, accepted boundaries, interactions, release separation, and non-goals without adding a mechanism. |
| Requirement coverage | pass | UBR-R001 through UBR-R020 each map to concrete automated tests with assertions matching the contract. |
| Example coverage | pass | E1 through E6 have stable semantic, activation, release, or recovery tests. |
| Negative and boundary coverage | pass | Missing, additional, stale, malformed, unknown, mixed, divergent, unavailable, mismatched, partial, and privacy-sensitive states are covered. |
| Proof-level adequacy | pass | Unit proof owns closed tuples; integration owns wiring and failure behavior; end-to-end owns package parity; smoke owns the M3/M4 release boundaries. |
| Milestone mapping | block | T23 is M1-required but depends only on CMD06, which begins in M2. |
| Command validity | pass | All 18 command paths and interfaces exist or are planned version extensions; classifications, owners, failure behavior, zero-test behavior, and side-effect boundaries are explicit. |
| Fixture and data design | pass | Fixtures are repository-local, temporary, deterministic, cleanup-owned, immutable-source preserving, and closed-vocabulary aware. |
| Manual-proof boundary | pass | No local outcome needs manual proof; external publication remains a separately authorized operational event. |
| Observability | pass | Assertions bind stable semantic categories and repository-relative identities without exact prose. |
| Determinism and isolation | pass | History, network, remote, registry, publication, user installation, randomness, and private state are isolated or stubbed. |
| Scope and non-goals | pass | The proof map does not add a runtime checker, writer, CLI, candidate protocol, publisher, release mode, or historical migration. |
| Execution economics | pass | Focused M1/M2 checks precede M3's expensive gates; M4 reruns them only because activation changes the checked state. |
| Traceability | pass | Requirement, acceptance, example, boundary, interaction, test, command, and milestone IDs are consistently linked apart from the timing defect. |
| Implementation handoff | block | M1 cannot close independently until UBR-TSR1-001 is corrected and the revised test spec is reviewed. |

## Exact proof-map gap

No requirement, boundary, interaction, fixture family, or validation command is missing. The defect is the timing link among an existing test, command, and milestone.

## Recommendation

Revise the test spec using the safe resolution path and request test-spec-review R2.
This direct review is isolated and does not revise the test spec, start implementation, modify workflow routing, or claim that any test command passed.
