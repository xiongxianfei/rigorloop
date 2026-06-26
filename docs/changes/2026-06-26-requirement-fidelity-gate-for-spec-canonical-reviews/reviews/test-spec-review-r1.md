# Test Spec Review R1: Requirement-Fidelity Gate

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: 1
Reviewer: Codex test-spec-review skill
Target: specs/requirement-fidelity-gate.test.md
Reviewed artifact: specs/requirement-fidelity-gate.test.md
Review date: 2026-06-26
Recording status: recorded
Status: changes-requested
Material findings: TSR1-F1
Review status: changes-requested
Immediate next stage: review-resolution
Implementation handoff: not-allowed

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: TSR1-F1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/test-spec-review-r1.md
- Review log: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-log.md
- Review resolution: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-resolution.md#test-spec-review-r1
- Open blockers: TSR1-F1
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Stop condition: material proof-map finding requires review-resolution before implementation

## Review Inputs

- Test spec: specs/requirement-fidelity-gate.test.md
- Approved feature spec: specs/requirement-fidelity-gate.md
- Spec-review evidence: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/spec-review-r2.md
- Approved plan: docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md
- Plan-review evidence: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/plan-review-r1.md
- Architecture: docs/architecture/system/architecture.md
- ADR: docs/adr/ADR-20260626-requirement-fidelity-gate.md
- Architecture-review evidence: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/architecture-review-r1.md
- Review skill rule: .agents/skills/test-spec-review/SKILL.md

## Findings

## Finding TSR1-F1

Finding ID: TSR1-F1
Severity: major
Location: specs/requirement-fidelity-gate.test.md:27, specs/requirement-fidelity-gate.test.md:260, specs/requirement-fidelity-gate.test.md:343, specs/requirement-fidelity-gate.test.md:349
Evidence: The test spec relies on manual proof for private corpus custody, receipt-prose quality, scan-first skill usability, broad-read performance behavior, and milestone-start gating. The manual checks are recorded only as broad bullets such as "manual contract review", "Manually review public skill text", and "Confirm..." checklist items. The test-spec-review contract requires manual proof to name a stable ID, automation rationale, exact steps, required environment, evidence artifact, pass condition, failure condition, and owning stage.
Required outcome: Every manual proof that remains in the test spec must be represented by an auditable manual proof case with a stable ID, automation rationale, exact steps, required environment, evidence artifact, pass condition, failure condition, and owning stage, or it must be converted into automated/fixture-backed proof.
Safe resolution path: Revise `specs/requirement-fidelity-gate.test.md` to add a `Manual proof cases` section or convert the affected manual bullets into test cases with manual level. Cover at least public skill scan-first review, private rotating corpus custody, receipt-boilerplate quality sampling, broad-read/performance confirmation, and no-implementation-before-review gating. Link those manual proof IDs from the requirement coverage map, affected test cases, and manual QA checklist, then rerun `test-spec-review`.
needs-decision rationale: none

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Governing-contract alignment | pass | The test spec operationalizes the approved requirement-fidelity spec, architecture, ADR, and plan without changing product direction. |
| Requirement coverage | concern | All requirement IDs are mapped, but manual proof obligations are not yet auditable enough for the requirements they cover. |
| Example coverage | pass | Examples E1-E7 map to stable test IDs. |
| Negative and boundary coverage | pass | The proof map includes missing manifests, bad ordering, missing decomposition, matrix failures, unknown values, vague specs, missing receipts, historical reviews, and generated-output drift. |
| Proof-level adequacy | concern | Unit and integration coverage is well-scoped, but the manual-proof level lacks required procedure and evidence details. |
| Milestone mapping | pass | Test cases map to M1-M5 and align with the approved plan sequence. |
| Command validity | concern | Commands are existing repository commands or implementation-owned fixture tests, but manual-proof ownership must be made explicit with the manual proof cases. |
| Fixture and data design | pass | Fixture locations and isolation policy are appropriate and avoid external services. |
| Manual-proof boundary | block | Manual checks are justified at a high level but not exact, owned, evidenced, or bounded as required by the review contract. |
| Observability | pass | Review and calibration evidence fields are named and routed to validator fixtures. |
| Determinism and isolation | pass | Tests use filesystem fixtures, temporary directories, no network, and real validator paths. |
| Scope and non-goals | pass | The test spec avoids automatic prose extraction, historical migration, all-validator rewrite, and hosted services. |
| Execution economics | pass | Focused checks are distinguished from generated adapter and selected CI proof. |
| Traceability | pass | Requirements, examples, edge cases, milestones, and tests are linked consistently except for missing manual proof IDs. |
| Implementation handoff | block | Implementation would have to guess how to satisfy the manual proof obligations. |

## Exact Proof-Map Gaps

- Manual contract review for private rotating corpus custody needs a stable manual proof ID, exact inspection steps, required evidence artifact, pass/fail criteria, and owning stage.
- Manual review for sample receipt prose quality needs a stable manual proof ID, sampling input, pass/fail criteria, evidence artifact, and owning stage.
- Manual review for public skill scan-first usability needs exact review steps, evidence artifact, and pass/fail criteria.
- Manual performance confirmation that implementation avoids broad full-spec reads needs exact steps and pass/fail criteria.
- Manual confirmation that no implementation milestone begins before test-spec-review needs an owning stage and evidence artifact.

## Handoff

No automatic downstream handoff is performed. `TSR1-F1` must be dispositioned in review-resolution and the test spec must be revised or explicitly dispositioned before implementation can rely on this proof map.
