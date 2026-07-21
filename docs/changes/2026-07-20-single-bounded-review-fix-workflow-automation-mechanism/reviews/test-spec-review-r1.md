# Test Spec Review R1

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: 1
Reviewer: Codex test-spec-review
Target: specs/single-bounded-review-fix-workflow-automation.test.md
Reviewed artifact: specs/single-bounded-review-fix-workflow-automation.test.md
Review date: 2026-07-21
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: BRF-TSR1, BRF-TSR2, BRF-TSR3
Immediate next stage: review-resolution
Implementation handoff: not-allowed
Automatic downstream handoff: none

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: BRF-TSR1, BRF-TSR2, BRF-TSR3
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/test-spec-review-r1.md
- Review log: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md
- Review resolution: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md
- Open blockers: manual proof contracts are incomplete; CMD30 is not shell-executable as stored; deterministic time, randomness, environment, and order controls are not defined
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Stop condition: revise and rereview the active test spec before M1 implementation

## Review inputs

| Artifact | SHA-256 |
| --- | --- |
| `specs/single-bounded-review-fix-workflow-automation.test.md` | `5952b951d04da54d4aaa7f97f3f7b89af6afa87cfd7ef79468eade4f55ae4a41` |
| `specs/single-bounded-review-fix-workflow-automation.md` | `59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070` |
| `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md` | `d2ad212fb0a729f80c52d7ddd24cef68b01915688a0d1759c4e441d6a47c7fa2` |
| `docs/architecture/system/architecture.md` | `3ad5871a99f96f86e7beed58137a6eab7fdf235a0a36dd5c25f3ea6899e9dca8` |
| `docs/adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md` | `72f84faada32301b58221e008f7bd90d198bc002e51ffa868e5210b1299bd538` |

The feature spec is approved, architecture and ADR are settled, plan-review R2 is approved, and no upstream review finding remains open.
The proof map is therefore reviewable; all findings are local to the test specification.

## Findings

### BRF-TSR1

Finding ID: BRF-TSR1
Severity: major
Location: `specs/single-bounded-review-fix-workflow-automation.test.md:149` and `specs/single-bounded-review-fix-workflow-automation.test.md:578`
Evidence: M4-M6 rely on `MP1` through `MP3`, but each manual proof is only a one-sentence confirmation. The records do not name an automation-impracticality rationale, exact procedure, required environment, durable evidence artifact, explicit pass condition, explicit failure condition, or owning stage. The two additional manual QA checks at lines 583-584 have no stable IDs or milestone ownership.
Required outcome: Every manual proof used by a milestone must be an executable review contract with a stable ID, automation rationale, exact steps, required environment, evidence artifact, pass condition, failure condition, owning stage, and required gate. Additional manual checks must either receive the same contract or map to automated test IDs.
Safe resolution path: Replace the three one-line entries with a structured manual-proof table or subsections containing every required field; bind MP1 to M4/M5/M6 code-review as applicable, MP2 to M5/M6 code-review and final verify, and MP3 to M6 code-review. Give the public-output and diagnostic checks stable IDs or absorb them into T22/T25 assertions.
needs-decision rationale: none

### BRF-TSR2

Finding ID: BRF-TSR2
Severity: major
Location: `specs/single-bounded-review-fix-workflow-automation.test.md:145` and `specs/single-bounded-review-fix-workflow-automation.test.md:134`
Evidence: CMD30 stores the manifest-version pipeline as `\|` inside inline code so the Markdown table remains parseable. In raw shell execution, the backslash suppresses pipeline syntax and passes a literal `|` argument to `sed`, so the command marked `existing/configured` is not executable as stored. CMD18 also uses `M4 and M5 code-review` in the singular `First required milestone` field instead of identifying M4 as the first gate.
Required outcome: Every validation command must be directly executable from its canonical stored form, and every ledger row must identify exactly one first required milestone or gate.
Safe resolution path: Replace CMD30 with a shell-equivalent command that avoids a raw table pipe, such as an `awk` first-match expression, or move the pipeline into a repository-owned executable wrapper and reference that wrapper. Confirm it remains equivalent to the approved plan's manifest-derived temporary adapter validation. Normalize CMD18's first required milestone to M4 and retain M5 reuse in failure behavior or notes.
needs-decision rationale: none

### BRF-TSR3

Finding ID: BRF-TSR3
Severity: major
Location: `specs/single-bounded-review-fix-workflow-automation.test.md:532` through `specs/single-bounded-review-fix-workflow-automation.test.md:547`, with affected cases T14, T15, T16, T19, T22, and T28
Evidence: The fixture policy provides temporary repositories, stable IDs, relative paths, and no-network doubles, but it does not control clock/timestamps, timezone/locale, randomness, process environment, fixture order, or repeated-run isolation. Those inputs affect authorization times, target binding times, migration times, deterministic transition keys, status output, and recovery/idempotency assertions.
Required outcome: The proof map must define deterministic controls for every nondeterministic input used by transactional, migration, status, and end-to-end tests and must require order-independent repeated execution.
Safe resolution path: Add a fixture determinism contract using an injected fixed UTC clock, explicit stable ID/key inputs, fixed locale/timezone, sanitized environment, seeded or prohibited randomness, fresh temporary roots per case, and teardown assertions. Add a direct repeat/reordered-run assertion to the state or end-to-end suite so leaked global state and order dependence fail visibly.
needs-decision rationale: none

## Review dimensions

| Dimension | Verdict | Notes |
| --- | --- | --- |
| Governing-contract alignment | pass | The proof map operationalizes the approved target, authority, recovery, migration, review, and external-action contracts without changing them. |
| Requirement coverage | pass | All 139 BRF requirements and every acceptance family map to stable tests or bounded manual proof. |
| Example coverage | pass | E1-E12 map to stable test IDs. |
| Negative and boundary coverage | pass | Unknown values, invalid transitions, missing authority, stale evidence, partial output, cancellation, migration, rollback, and external-action traps are covered. |
| Proof-level adequacy | concern | Automated levels are appropriate, but manual proof is not yet contract-complete. |
| Milestone mapping | pass | M1-M6 have distinct proof gates aligned with the reviewed plan. |
| Command validity | block | CMD30 is not executable as stored, and CMD18's first-required field is not normalized. |
| Fixture and data design | concern | Fixture families and temporary repositories are appropriate, but nondeterministic inputs remain unspecified. |
| Manual-proof boundary | block | MP1-MP3 lack mandatory ownership, environment, evidence, and pass/fail fields. |
| Observability | pass | Test cases and result contracts identify failure meaning and durable evidence surfaces. |
| Determinism and isolation | block | Clock, timezone, locale, randomness, environment, and order independence are not controlled. |
| Scope and non-goals | pass | Alias removal, background execution, external actions, second registries, and hosted-CI claims remain excluded. |
| Execution economics | pass | Focused milestone commands precede M6 selected CI and required broad smoke. |
| Traceability | pass | Requirement, example, edge-case, milestone, test, command, and evidence IDs are consistently linked. |
| Implementation handoff | block | Implementation would need to invent manual-proof and deterministic-fixture contracts and repair a required M6 command. |

## Recommendation

Revise only the active test specification and its lifecycle references.
No spec, architecture, ADR, or plan redesign is required.
After the three findings are incorporated, rerun `test-spec-review` before M1 implementation.

This direct formal review is isolated and does not automatically revise the test spec or start implementation.
