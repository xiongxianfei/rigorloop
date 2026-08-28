# Code Review M3 R2: Semantic Severity Correction Review

Review ID: code-review-m3-r2
Stage: code-review
Round: r2
Reviewer: fresh independent reviewer
Reviewer context ID: m3-ci-fix-review
Target: first M3 invocation-observability correction packet
Reviewed artifact: M3 implementation/test/evidence bundle `sha256:66b038f848fa1ae0b0912ee8a50d142da5530ee526309ae98a9cc1f40418282e`
Reviewed milestone: M3
Review date: 2026-08-28
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Context separation mechanism: distinct review-only context with exact three-file target and no write authority
Risk tier: elevated
Risk-tier triggers: user-visible diagnostics; lifecycle error classification; default console emission; CI-gating evidence
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`; `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`
Formal criteria: code-review-rereview-v1; requirement-fidelity-gate-v1; boundary-first-v1
Initial packet inventory: packages/rigorloop/dist/bin/rigorloop.js@working-tree#sha256:0faba4bfc7478c3575b560e2067794a25a4587039a3d31ab8b179ab16e557c7a; packages/rigorloop/dist/lib/lifecycle-cli.js@working-tree#sha256:3b06cb919d5c6ba3bacaadb85d7cd1608dc0eb0f1c908ba31907eec8e3b26e03; packages/rigorloop/test/cli-invocation-observability.test.js@working-tree#sha256:bc01cb6b39282fd9c8e3b13dee786d9d0eaa0b4c6d1115ada576e5591d1d2de0
Initial packet hash: sha256:66b038f848fa1ae0b0912ee8a50d142da5530ee526309ae98a9cc1f40418282e
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: lifecycle terminal severity and default console emission for expected, unsafe-recovery, and internal outcomes
Highest-impact failure modes: hiding an unsafe or internal failure; noisy expected rejection; semantic exit drift; unproved public composition
Changed boundaries: lifecycle semantic result to invocation diagnostic controller
Evidence expected: R4 and T06/T07 public, helper, mixed-diagnostic, stale, blocked, unsafe-recovery, and internal paths
Areas requiring direct inspection: `lifecycle-cli.js`; public CLI dispatch; invocation controller; focused tests
Areas intentionally out of scope: M4; milestone mutation; final verification; release readiness
Risk classes considered: requirement fidelity; failure precedence; public composition; compatibility; privacy; evidence adequacy
Falsifiable review questions: Can a later unsafe or internal error be hidden by an earlier expected error? Do public stale and recovery paths produce the required severity without changing semantic exits?
Automated review: yes
Material findings: CLIOBS-M3-R2-F1
Immediate next stage: review-resolution and M3 correction
Automatic downstream handoff: none
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `reviews/code-review-m3-r2.md`; `review-log.md`; `review-resolution.md`
- Open blockers: none after the subsequently recorded M3 R3 correction and resolution
- Next stage: implement next milestone after workflow consumes the clean rereview
- Review status: changes-requested
- Material findings: CLIOBS-M3-R2-F1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m3-r2.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4
- Required review-resolution: yes
- Finding IDs: CLIOBS-M3-R2-F1
- Verify readiness: not-claimed

## Finding CLIOBS-M3-R2-F1

Finding ID: CLIOBS-M3-R2-F1
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-cli.js`
Evidence: `lifecycleTerminalClass()` inspected only `errors[0]`; an expected rejection preceding `RL_RECOVERY_REQUIRED` or `RL_POST_VALIDATION_FAILED` downgraded the terminal severity.
Required outcome: every diagnostic participates in classification with precedence `internal or unknown` over `unsafe recovery` over `expected rejection`.
Safe resolution path: derive the expected set from the canonical closed lifecycle-code vocabulary, scan all errors, fail unknown codes closed, and add mixed-diagnostic regressions.
needs-decision rationale: none

## Checklist coverage

- Spec alignment: concern; R4 semantic precedence was incomplete.
- Test coverage: concern; the public lifecycle error paths were not exercised.
- Edge cases: concern; mixed diagnostics could downgrade the terminal result.
- Error handling: concern; unsafe and internal failures could become warning-only.
- Architecture boundaries: pass; semantic execution remained separate from diagnostic sinks.
- Compatibility: pass; semantic exit codes and result rendering were unchanged.
- Security/privacy: pass; no private diagnostic data was introduced.
- Derived artifact currency: pass for the reviewed M3 packet.
- Unrelated changes: pass; the correction was confined to lifecycle classification and proof.
- Validation evidence: concern; 70/70 focused tests passed but omitted the identified public and mixed partitions.

## Handoff

This review confirmed that prior finding `CLIOBS-M3-R1-F3` remained unresolved and added `CLIOBS-M3-R2-F1`. It was initially recording-blocked by its no-edit review instruction and is now reconstructed from the independent reviewer result before resolution. The subsequent M3 R3 rereview records the corrected packet; this record does not mutate lifecycle state or claim final verification.
