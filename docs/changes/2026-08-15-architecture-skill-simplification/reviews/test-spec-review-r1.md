# Test-Spec Review R1: Architecture Skill Simplification

Review ID: test-spec-review-r1

Stage: test-spec-review

Round: r1

Reviewer: Codex independent test-spec-review context

Target: `specs/architecture-skill-simplification.test.md`

Reviewed artifact: commit `9be51238`

Review date: 2026-08-15

Status: changes-requested

Review status: changes-requested

Material findings: ARSIM-TSR1, ARSIM-TSR2

Recording status: recorded

Immediate next stage: test-spec revision

Implementation handoff: not-allowed

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: ARSIM-TSR1, ARSIM-TSR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-15-architecture-skill-simplification/reviews/test-spec-review-r1.md`
- Review log: `docs/changes/2026-08-15-architecture-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-15-architecture-skill-simplification/review-resolution.md`
- Open blockers: acceptance-criterion traceability and one executable command identity require test-spec revision
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: bounded automation target reached; no correction or implementation was started

## Findings

## Finding ARSIM-TSR1

Finding ID: ARSIM-TSR1
- Severity: major
- Location: `specs/architecture-skill-simplification.test.md`, Requirement coverage map, Test cases, and Readiness
- Evidence: The approved feature spec defines AC1 through AC10, and the review contract requires acceptance-criterion traceability. The proof map contains no AC identifier, no acceptance-criterion coverage table, and no test-case `Covers` field naming an acceptance criterion, so the asserted complete handoff cannot be audited from each accepted criterion to direct proof.
- Required outcome: Map AC1 through AC10 to stable test cases and commands, preserving their requirement and boundary basis without inventing new behavior.
- Safe resolution path: Add an acceptance-criterion coverage table or exact AC identifiers to the existing case mappings, verify every criterion has direct proof, rerun boundary and prose validation, and submit the revised test spec for independent rereview.
- needs-decision rationale: none; the accepted feature spec already supplies the complete criterion vocabulary.

## Finding ARSIM-TSR2

Finding ID: ARSIM-TSR2
- Severity: major
- Location: `specs/architecture-skill-simplification.test.md`, validation command `CMD1`
- Evidence: `CMD1` is `python -m unittest scripts.test_skill_validator.ArchitectureSkillSimplificationTests`, but the repository contains `scripts/test-skill-validator.py` and no importable `scripts/test_skill_validator.py` module. The approved plan names `python scripts/test-skill-validator.py ArchitectureSkillSimplificationTests` for focused validation, while the proposed `CMD1` cannot resolve even after the planned class is added to the existing hyphenated script.
- Required outcome: Replace `CMD1` with an executable, repository-owned command that matches the plan’s M1 ledger/fixture intent, or consolidate it with the valid focused runner while retaining explicit M1 ownership, failure behavior, and zero-test behavior.
- Safe resolution path: Use the existing `scripts/test-skill-validator.py` runner for the focused class or define the exact change-local standard-library command intended by M1, remove redundant command mappings, and verify resolution without running implementation validation during review.
- needs-decision rationale: none; the repository and approved plan already identify the supported test runner.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| governing-contract alignment | pass | The proof map consumes the approved spec, no-architecture assessment, active plan, and clean reviews without redefining behavior. |
| requirement coverage | pass | R1 through R54 map to stable cases and proof obligations. |
| acceptance-criterion coverage | block | AC1 through AC10 have no explicit traceability to test cases or commands. |
| example and edge coverage | pass | E1 through E10 and EC1 through EC6 map to deterministic cases with additional negative states. |
| boundary and interaction coverage | pass | All eight boundaries and INT-001 through INT-004 have exact covered proof obligations, and structural boundary validation passes. |
| negative and recovery coverage | pass | Invalid, missing, stale, conflicting, interrupted, concurrent, unrecorded, partial, dependency, and parity states are explicit. |
| proof-level adequacy | pass | Contract, integration, and smoke levels match the content, lifecycle, recovery, and distribution claims. |
| milestone mapping | pass | M1 freezes ownership, M2 changes the canonical package, M3 proves reduction and parity, and M4 owns closeout. |
| command ownership | block | CMD1 points to a nonexistent importable module and conflicts with the approved plan’s repository runner. |
| fixture and data design | pass | Temporary filesystems and change-local scenarios cover preparation, dependency order, retries, collisions, and derived packages. |
| manual-proof boundary | pass | No manual proof is necessary, and ordinary review is not converted into a new acceptance gate. |
| determinism and isolation | pass | The proof excludes network, publication, target-agent execution, transcript grading, and external state mutation. |
| implementation handoff | changes-requested | The two proof-map defects must be corrected and rereviewed before M1 begins. |

## Claim limitations

This review records proof-map defects only. It does not claim tests were implemented or run, permit implementation, approve validation, or establish verification, branch, PR, or lifecycle-closeout readiness.
