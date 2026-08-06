# Code Review: M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: two independent L2 Codex reviewers
Target: 269351b5..7ef368b4
Reviewed artifact: M2 atomic-publication implementation
Reviewed milestone: M2
Review date: 2026-08-05
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m2-implementation
Reviewer context ID: m2-r1-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Risk tier: elevated
Risk-tier triggers: remote mutation; Git identity authority; diagnostics; privacy
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: spec; test spec; M2 plan; activation-publication ADR
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@7ef368b4#sha256:fa622a617f8af6f36a9b877338b97d4a4df25a493f385764c66feaad751b7918; specs/boundary-first-v1-v0-3-7-activation-release.test.md@7ef368b4#sha256:9d0d7c839c9c44d4c138fe22961b861a06c6520dc4d3dd9a1a648f0de8114186; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@7ef368b4#sha256:eaea12dafb3ee49d6ab284603566c8a9f190a92fbdcd4fe665ef70388ef07bde; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@7ef368b4#sha256:614c19fb59aae74205845024fa23993fed38e0b5dce2c65991a24909858b542a; range:269351b5..7ef368b4.diff@7ef368b4#sha256:19e9998612788eab361482d72a3bce4a769ca9d5037d7fe05932e2a922457a90
Initial packet hash: sha256:19e9998612788eab361482d72a3bce4a769ca9d5037d7fe05932e2a922457a90
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: atomic activation publication and bounded operator diagnostics
Highest-impact failure modes: stale remote authority, partial publication, and evidence-path indirection
Changed boundaries: BND-AUTH-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-ENV-001
Evidence expected: same-push advertised identities; real-Git atomicity; bounded private-safe failures
Areas requiring direct inspection: evidence path comparison; pre-push stdin; atomic command; error serializer
Areas intentionally out of scope: release payload; real activation transition; public release; final verify
Risk classes considered: identity; concurrency; remote mutation; recovery; privacy
Falsifiable review questions: can a symlink alias pass; can same-push stale identities pass; can a race be diagnosed safely
Material findings: BFA-M2-R1-001, BFA-M2-R1-002, BFA-M2-R1-003
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### BFA-M2-R1-001 — Symlink resolution defeats exact evidence-path authority

Finding ID: BFA-M2-R1-001
Severity: major
Location: `scripts/boundary_activation_release.py` candidate path validation
Evidence: supplied and canonical paths are resolved before the symlink check, so
a symlink alias to the canonical evidence file is accepted.
Required outcome: reject symlinks at both lexical paths and compare normalized
repository-relative paths without following symlinks.

### BFA-M2-R1-002 — Publication diagnostics lose safe required context

Finding ID: BFA-M2-R1-002
Severity: major
Location: `scripts/boundary_activation_release.py` push failure and error payload
Evidence: remote races collapse into generic atomic failures and the serialized
payload omits mode, release, available P/T/H, conflicting remote state,
expected invariant, and corrective action.
Required outcome: retain bounded failure classes and safe context without raw
provider output, private values, or temporary paths.

### BFA-M2-R1-003 — Same-push advertised identities and proof matrix are incomplete

Finding ID: BFA-M2-R1-003
Severity: major
Location: pre-push guard and `scripts/test-boundary-activation-release.py`
Evidence: the hook ignores Git pre-push stdin and trusts a separate `ls-remote`,
so an advertised main identity different from P can pass. The atomic-capability
test mocks all subprocess behavior and the suite omits required real-Git CAS,
non-fast-forward, evidence-drift, CLI-success, and privacy cases.
Required outcome: validate exactly one advertised mapping for both destinations
from hook stdin, keep a separate query only as defense in depth, add the approved
real-Git fixtures, and narrow implementation evidence to demonstrated claims.

## Validation evidence

The reviewed publication suite passed 7 tests and the selector suite passed 147
tests. Compilation, strict boundary validation, the explicit selector, and diff
checks passed. Review adversarial probes reproduced all three gaps while
confirming full-SHA refspecs, no force or sequential fallback, read-only check
mode, and all-or-neither behavior under receive rejection.
