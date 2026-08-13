# Test-Spec Review R1: Test-Spec Skill Simplification

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: r1
Reviewer: Codex independent test-spec-review context
Target: `specs/test-spec-skill-simplification.test.md`
Reviewed artifact: commit `786fa626`
Review date: 2026-08-13
Status: changes-requested
Review status: changes-requested
Material findings: TSSIM-TSR1
Recording status: recorded
Immediate next stage: review-resolution
Implementation handoff: not-allowed

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: TSSIM-TSR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-13-test-spec-skill-simplification/reviews/test-spec-review-r1.md`
- Review log: `docs/changes/2026-08-13-test-spec-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-13-test-spec-skill-simplification/review-resolution.md`
- Open blockers: TSSIM-TSR1
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Stop condition: bounded automation target reached at the first formal test-spec-review result; implementation remains blocked pending disposition, test-spec revision, and rereview

## Findings

## Finding TSSIM-TSR1

Finding ID: TSSIM-TSR1
Severity: major
Location: `specs/test-spec-skill-simplification.test.md`, Validation commands, CMD1; T13; M1 proof row
Evidence: CMD1 only checks that the three documents are non-empty, disposition and classification values are members of closed sets, and IDs are unique. It does not validate the required semantic-rule or literal fields, non-empty values, the exact scenario inventory, per-scenario required and forbidden outcomes, explicit invalid-disposition and invalid-classification fixtures, or that unknown values are rejected before consistency checks. T13, the M1 row, and CMD1's failure behavior nevertheless claim those properties, while the approved plan requires them before canonical package edits.
Required outcome: Replace CMD1 with an exact deterministic command that validates the closed required-field sets, non-empty fields, unique IDs, the approved exact scenario inventory, required and forbidden outcome data, explicit invalid fixtures, and unknown-value-first results, then update any coupled fixture description without weakening M1.
Safe resolution path: Revise only the test-spec command and coupled proof wording, retain the plan's M1 ownership and no-target-runtime boundary, validate boundary coverage, record disposition, and submit the revised proof map for a new formal test-spec review.
needs-decision rationale: none

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| governing-contract alignment | pass | The proof map consumes the approved specification, architecture assessment, and reviewed plan without redefining product behavior. |
| requirement coverage | pass | R1 through R62 map to stable test cases or manual semantic procedures. |
| example coverage | pass | E1 through E12 map to deterministic public-path cases. |
| boundary and interaction coverage | pass | All 12 approved boundaries and five selected interactions have direct proof obligations with exact owner sets; repository boundary validation passes. |
| negative and failure coverage | pass | Missing, stale, mismatched, conflicting, duplicate, interrupted, mixed-package, reliance, resource, and forbidden-write states are explicit. |
| transaction coverage | pass | Creation, exact retry, stale stop, same-entry restart, revision, fresh review, settlement isolation, and active reliance have distinct outcomes. |
| structural composition | pass | Full and bounded composition, five asset owners, placeholders, missing assets, and policy boundaries are explicit. |
| optional manual verification | pass | MP0 and MP1 are justified semantic reviews, and automated/manual/hybrid proof preserves existing structures without a new manual-proof contract or asset. |
| proof-level adequacy | pass | Contract, integration, automated, hybrid, and manual evidence match the claims they support. |
| milestone mapping | pass | M1 freezes ownership and baseline evidence, M2 performs the canonical refactor, M3 proves final semantics and package parity, and M4 is lifecycle-only closeout. |
| command validity | block | CMD1 does not execute several properties that its failure behavior, T13, and the M1 gate claim. |
| fixture and data design | concern | The prose names the right fixture classes, but CMD1 does not validate their exact inventory or invalid-fixture outcomes. |
| observability | pass | Evidence paths, stable IDs, command failures, profile inputs, and package targets are explicit. |
| determinism and isolation | pass | Acceptance excludes network services, publication, target-agent execution, prompt journeys, and transcript grading. |
| implementation handoff | block | M1 could pass without complete ledgers or fail-closed unknown-value proof. |

## No-finding areas

- The feature and proof records pass deterministic boundary validation.
- Every normative requirement and approved example has mapped proof.
- Creation, retry, same-entry restart, revision, peer settlement, and workflow isolation are directly covered.
- The existing five assets remain the only structural owners, and optional manual verification adds no new contract or asset.
- Package proof selects `test-spec` directly across generated, archived, and clean-installed targets.
- No acceptance command executes or grades Codex, Claude Code, opencode, or another target-agent runtime.
- The review did not execute implementation or final validation commands.

## Claim limitations

This review records a proof-map defect and blocks implementation handoff. It does not claim implemented tests, completed milestones, validation success, verification, branch readiness, or PR readiness.
