# Code Review M1 R1: Lifecycle Contracts and Conformance

Review ID: code-review-m1-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review context
Target: implementation milestone M1 range `b18fedac..d03fc845`
Reviewed milestone: M1
Reviewed artifact: commit `d03fc845`
Review date: 2026-08-24
Status: changes-requested
Review status: changes-requested
Material findings: RLCLI-CR-M1-1, RLCLI-CR-M1-2
Recording status: recorded
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L0
Author context ID: root-m1-implementation
Reviewer context ID: root-m1-review-r1-context-reset
Context separation mechanism: fresh-assumption-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: untrusted YAML parser; public request schema; lifecycle identity contract; runtime package dependency
Risk-tier classifier: deterministic changed-surface classification
Governing artifacts: `specs/governed-lifecycle-cli.md`; `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md`; `docs/plans/2026-08-24-governed-lifecycle-cli.md`; `specs/governed-lifecycle-cli.test.md`
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/governed-lifecycle-cli.md@d03fc845#sha256:f7d9984c6913f5326cce231874f57673835c25ed1d4c94a03bdf4437eba8e405; specs/governed-lifecycle-cli.test.md@d03fc845#sha256:67666e00f314a95058b1399ae723702257e3342781bb2b0acc4d7a81eeb48351; docs/plans/2026-08-24-governed-lifecycle-cli.md@d03fc845#sha256:3db2ac47143f4ad05e78eeeeea0edb8a0228d743319cce16199564f2d5bda485; docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md@d03fc845#sha256:9e2ed53a513fe7d1d04c69cfd5044a3aa4f2199e39695849ac7a5d638d6fb78e; commit:d03fc845.diff@d03fc845#sha256:9c769c775612fca93f29296bc0250088bb86506ff3d97c3db27242db98bc235d
Prompt template version: code-review-v1
Initial packet hash: sha256:9c769c775612fca93f29296bc0250088bb86506ff3d97c3db27242db98bc235d
Manifest owner: workflow-orchestrator
Affected behavior: lifecycle request and YAML contracts; deterministic revision identity; npm runtime dependency policy
Highest-impact failure modes: incomplete requests accepted; excluded provenance changes revision; unsafe YAML accepted; unreviewed dependency published
Changed boundaries: BND-INPUT-001; BND-TEMPORAL-001; BND-COMPAT-001; BND-ENV-001
Evidence expected: T01 and T22 request, parser, revision, package, and audit proof
Areas requiring direct inspection: lifecycle contract module; fixture; Node tests; package policy; publication test
Areas intentionally out of scope: M2 through M7 commands, transactions, semantic operations, skills, CI, and verification
Risk classes considered: input; identity; compatibility; dependency security; determinism
Falsifiable review questions: Can an incomplete operation pass; can excluded provenance alter revision; can unknown YAML or dependencies pass

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, invocation manifest, review log, and review resolution
- Open blockers: RLCLI-CR-M1-1 and RLCLI-CR-M1-2
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: RLCLI-CR-M1-1, RLCLI-CR-M1-2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-08-24-governed-lifecycle-cli/review-log.md`
- Review resolution: `docs/changes/2026-08-24-governed-lifecycle-cli/review-resolution.md`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4, M5, M6, M7
- Required review-resolution: yes
- Finding IDs: RLCLI-CR-M1-1, RLCLI-CR-M1-2
- Verify readiness: not-claimed

## Blind-first risk map

The highest-impact risks are accepting incomplete semantic requests, producing lifecycle revisions that change for explicitly excluded provenance, admitting unsafe YAML, weakening package publication controls, and freezing a contract that later mutation code cannot use deterministically. Direct inspection covered the M1 diff, R4, R18, R27, the lifecycle-revision ADR decision, T01, T22, package policy, and the shared fixtures. M2-M7 behavior remains outside this review.

## Findings

### Finding RLCLI-CR-M1-1

Finding ID: RLCLI-CR-M1-1
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-contract.js`; `validateLifecycleRequest`
Evidence: The validator requires only `change_id` and `expected_lifecycle_revision`. Requests such as `settle-artifact` without `artifact_id`, `record-review` without `evidence_path`, and `repair` without `condition` are accepted even though M1 owns complete operation schemas and R4 requires unknown and invalid requests to fail before mutation.
Required outcome: Define and enforce the required fields and closed operation-specific values for every first-release operation, including non-empty repository-relative evidence paths and structural stage-authority claims where applicable.
Safe resolution path: Add a closed per-operation field contract, reject missing or invalid fields before consistency, and add one missing-field plus one unknown-value regression for each operation.
needs-decision rationale: none
Auto-fix class: declared-safe

### Finding RLCLI-CR-M1-2

Finding ID: RLCLI-CR-M1-2
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-contract.js`; `lifecycleRevision`; shared conformance fixture
Evidence: The lifecycle revision hashes the complete change object and has no versioned provenance exclusion list. A documented actor or timestamp field therefore changes the revision, contrary to R27 and the ADR requirement that explicitly excluded provenance fields be omitted and frozen in fixtures.
Required outcome: Define the first versioned provenance exclusion set and prove that excluded provenance does not change the revision while every mutation-relevant field still does.
Safe resolution path: Strip only closed documented provenance keys during revision canonicalization, record that list in the shared fixture, and add positive and negative revision regressions.
needs-decision rationale: none
Auto-fix class: declared-safe

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | R4 and R27 are incomplete through the two findings. |
| Test coverage | block | Operation-specific missing fields and provenance exclusions lack direct proof. |
| Edge cases | block | Incomplete semantic requests currently pass. |
| Error handling | concern | Unknown operations and fields fail correctly, but required operation fields do not. |
| Architecture boundaries | block | The ADR-required exclusion list is absent. |
| Compatibility | concern | Parser and serializer fixtures are stable; revision semantics are not complete. |
| Security/privacy | pass | Unsafe YAML classes are rejected and the patched dependency audits clean. |
| Derived artifact currency | pass | Package policy and tarball inventory include the new runtime module. |
| Unrelated changes | pass | The implementation diff is confined to M1 contracts, tests, policy, and evidence. |
| Validation evidence | concern | Named commands pass, but direct review probes reveal missing assertions. |

## Requirement-fidelity receipt

Applicability: applicable. R4 decomposes into version, operation, allowed fields, required fields, and closed-value rejection; required-field coverage fails. R27 decomposes into deterministic serialization, revision, output, and documented provenance exclusion; the exclusion property fails. Other M1-owned parser, dependency, and deterministic ordering properties pass.

## Independent-review receipts

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Independence level: L0
Second review: not applicable because this result requests changes
Confidence: high

No clean-review sufficiency receipt is issued because material findings remain.
