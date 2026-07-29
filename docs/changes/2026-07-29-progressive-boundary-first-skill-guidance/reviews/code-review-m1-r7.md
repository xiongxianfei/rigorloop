# M1 Code Review R7

Review ID: code-review-m1-r7
Stage: code-review
Round: 7
Reviewer: two independent L2 Codex reviewers
Target: 9d16bbe2..328e31d3
Reviewed artifact: commit 328e31d3
Reviewed milestone: M1
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m1-r6-resolution
Reviewer context ID: m1-r7-primary-and-second-fresh-agents
Context separation mechanism: fresh-separate-agents-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: validator behavior; projection transaction; filesystem containment; multi-component change
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md@328e31d3#sha256:983a6cab29dd12ff18866f06a2a818ab9c198dd3a3ccddccc06c8e95516d2dd2; specs/progressive-boundary-first-skill-guidance.test.md@328e31d3#sha256:30595f49cb782e772588334dc9b6c31c728f5b6567892784d6fa27488e3f5257; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md@328e31d3#sha256:7aa4b69d2636eb0ff6bf6fb77bcf6835ad2dd5c889feaa8b786e1badce65d5c1; docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md@328e31d3#sha256:ad78a2f644679a6b0dbaaa6000c1c9b0a8751f9abeb238fcb74cee04e16181c9
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/progressive-boundary-first-skill-guidance.md@328e31d3#sha256:983a6cab29dd12ff18866f06a2a818ab9c198dd3a3ccddccc06c8e95516d2dd2; specs/progressive-boundary-first-skill-guidance.test.md@328e31d3#sha256:30595f49cb782e772588334dc9b6c31c728f5b6567892784d6fa27488e3f5257; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md@328e31d3#sha256:7aa4b69d2636eb0ff6bf6fb77bcf6835ad2dd5c889feaa8b786e1badce65d5c1; docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md@328e31d3#sha256:ad78a2f644679a6b0dbaaa6000c1c9b0a8751f9abeb238fcb74cee04e16181c9; commit:328e31d3.diff@328e31d3#sha256:1d9c833f61fbaa7b224e5e5dcde7d2efb22de84345eed8760aad9f3599f2c48b
Prompt template version: code-review-v1
Initial packet hash: sha256:1d9c833f61fbaa7b224e5e5dcde7d2efb22de84345eed8760aad9f3599f2c48b
Manifest owner: workflow-orchestrator
Affected behavior: input snapshot identity, target containment and recovery, manifest diagnostics
Highest-impact failure modes: unbounded concurrency claim, outside write by parent swap, recovery abort, opaque resource layer
Changed boundaries: temporal scope; filesystem containment; recovery; diagnostics
Evidence expected: contract interpretation, no-follow writes, recovery aggregation, layer diagnostics
Areas requiring direct inspection: specification concurrency scope, write primitive, restoration boundary, identity error
Areas intentionally out of scope: M2, M3, M4, PR, and final verification
Risk classes considered: temporal retry; recovery; containment; diagnostics; authority
Falsifiable review questions: Does the contract require hostile post-read exclusion; can topology swap write outside; do identity errors name layers
Material findings: CR-M1-R7-001, CR-M1-R7-002, CR-M1-R7-003
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M1-R7-001 — Final-read race is treated as an unbounded concurrency guarantee

Finding ID: CR-M1-R7-001
Severity: blocker
Location: `scripts/boundary_first_reference.py`
Evidence: A non-cooperative writer can change an input immediately after its final read and before return.
Required outcome: Either enforce a global linearization boundary or define success against the named immutable input snapshot.
Safe resolution path: Follow the governing contract: return the named snapshot identities; subsequent drift is a new state and must fail activation or the next check.
needs-decision rationale: The spec requires interrupted or drifted bundles to block activation, not exclusion of hostile writes after the projector's linearization read.
Auto-fix class: none

### CR-M1-R7-002 — Target topology drift can escape containment or abort recovery

Finding ID: CR-M1-R7-002
Severity: blocker
Location: `scripts/boundary_first_reference.py`
Evidence: Swapping a target parent for an outside symlink between validation and write can mutate outside; `_restore_targets` resolves before its catch and can abort recovery.
Required outcome: Writes never follow target symlinks, and recovery continues across unsafe targets while reporting incomplete restoration.
Safe resolution path: Use descriptor-relative no-follow operations and catch path-contract failures inside each restore iteration.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M1-R7-003 — Exact-manifest diagnostics omit the affected resource layer

Finding ID: CR-M1-R7-003
Severity: blocker
Location: `scripts/boundary_first_reference.py`
Evidence: A known-value tuple drift reports only whole-manifest identity and an opaque digest.
Required outcome: Identity failures name the affected stable resource layer without disclosing the untrusted value.
Safe resolution path: Compare opaque per-layer identities for diagnostics only and list the affected stable IDs.
needs-decision rationale: none
Auto-fix class: declared-safe

## Requirement-fidelity receipt

Applicability: applicable
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: present for containment and layer diagnostics; concurrency scope disputed
No-finding rationale: not-applicable because material findings exist

## Independent-review receipts

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Independence level: L2
Second review: satisfied; both reviewers requested changes
Confidence: high

No clean-review sufficiency receipt is issued because the review is not clean.
