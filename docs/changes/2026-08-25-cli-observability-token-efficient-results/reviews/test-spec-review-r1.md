# Test Specification Review R1: CLI Observability and Token-Efficient Results

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: r1
Target: `specs/cli-observability-and-token-efficient-results.test.md`
Reviewed artifact: `sha256:1d4d6dfb266b986ba9e66a0fa44816a77e26e02e5b721524737621c88f98e86a`
Reviewer: Codex independent test-spec-review context
Review date: 2026-08-25
Recording status: recorded
Status: changes-requested
Material findings: CLIOBS-TSR1, CLIOBS-TSR2

## Result

Skill: test-spec-review
Review status: changes-requested
Material findings: CLIOBS-TSR1, CLIOBS-TSR2
Recording status: recorded
Recording blocker: none
Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/test-spec-review-r1.md`
Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
Open blockers: direct external-path proof and executable M4 benchmark/package proof
Immediate next stage: test-spec revision
Implementation handoff: not-allowed
Stop condition: revise the proof map and submit the resulting identity for a fresh formal review

## Findings

## Finding CLIOBS-TSR1

Finding ID: CLIOBS-TSR1
Severity: major
Location: R34 coverage; PRF-008; T05; Performance checks
Evidence: R34 prohibits a daemon, database, network request, and unbounded directory traversal. T05 counts ordinary filesystem work and T08 bounds lookup names, but no case spies on network/process creation, detects database dependencies, or asserts that only the invocation process remains. The proof map therefore cannot directly establish the external-resource half of BND-ENV-001.
Required outcome: Add deterministic direct proof that ordinary logging and lookup open only the admitted filesystem resources and create no network connection, database, daemon, or background process.
Safe resolution path: Extend T05 with injected network/process guards and an open-handle assertion, and cite that proof from R34, PRF-008, and the performance section without changing feature behavior.
needs-decision rationale: none

## Finding CLIOBS-TSR2

Finding ID: CLIOBS-TSR2
Severity: major
Location: C06; M4 milestone proof row; T15; M4 plan alignment
Evidence: T15 names `scripts/test-cli-result-measurement.py`, but C06 invokes only the measurement program, so threshold, profile-drift, and aggregation regressions could be implemented without their test suite ever running. The approved M4 plan also requires packed-package smoke and operational documentation examples, while the M4 proof row assigns only T15 and contains no package-surface case.
Required outcome: Make the benchmark implementation's regression suite an explicit command and add direct packed-package and documented-command proof to M4 before its review gate.
Safe resolution path: Add a planned command for `scripts/test-cli-result-measurement.py`, map it to T15 and M4, add one automated T17 package/documentation contract case under the release command, and update the affected requirement, acceptance, command, and milestone rows.
needs-decision rationale: none

## Review rationale

The proof map otherwise traces all approved requirement, example, edge-case, boundary, interaction, acceptance, privacy, concurrency, recovery, compatibility, and authority partitions at an adequate level. Both findings are proof-only gaps inside the test specification; no feature-spec, architecture, or plan revision is required.
