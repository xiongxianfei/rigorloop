# M1 Code Review R6

Review ID: code-review-m1-r6
Stage: code-review
Round: 6
Reviewer: two independent L2 Codex reviewers
Target: 9d16bbe2..e9fba6f7
Reviewed artifact: commit e9fba6f7
Reviewed milestone: M1
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m1-r5-resolution
Reviewer context ID: m1-r6-primary-and-second-fresh-agents
Context separation mechanism: fresh-separate-agents-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: validator behavior; projection transaction; compatibility identity; multi-component change
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md@e9fba6f7#sha256:983a6cab29dd12ff18866f06a2a818ab9c198dd3a3ccddccc06c8e95516d2dd2; specs/progressive-boundary-first-skill-guidance.test.md@e9fba6f7#sha256:30595f49cb782e772588334dc9b6c31c728f5b6567892784d6fa27488e3f5257; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md@e9fba6f7#sha256:7aa4b69d2636eb0ff6bf6fb77bcf6835ad2dd5c889feaa8b786e1badce65d5c1; docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md@e9fba6f7#sha256:ad78a2f644679a6b0dbaaa6000c1c9b0a8751f9abeb238fcb74cee04e16181c9
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/progressive-boundary-first-skill-guidance.md@e9fba6f7#sha256:983a6cab29dd12ff18866f06a2a818ab9c198dd3a3ccddccc06c8e95516d2dd2; specs/progressive-boundary-first-skill-guidance.test.md@e9fba6f7#sha256:30595f49cb782e772588334dc9b6c31c728f5b6567892784d6fa27488e3f5257; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md@e9fba6f7#sha256:7aa4b69d2636eb0ff6bf6fb77bcf6835ad2dd5c889feaa8b786e1badce65d5c1; docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md@e9fba6f7#sha256:ad78a2f644679a6b0dbaaa6000c1c9b0a8751f9abeb238fcb74cee04e16181c9; commit:e9fba6f7.diff@e9fba6f7#sha256:afff8b4d4cf3c0913b2fef69e1504fded3d40e8ed7d332b97264540a7f6949fd
Prompt template version: code-review-v1
Initial packet hash: sha256:afff8b4d4cf3c0913b2fef69e1504fded3d40e8ed7d332b97264540a7f6949fd
Manifest owner: workflow-orchestrator
Affected behavior: projection transaction input stability
Highest-impact failure modes: success returned after canonical input mutation
Changed boundaries: temporal retry; composition identity; recovery
Evidence expected: manifest and source mutation at early, middle, and late writes with restoration and retry
Areas requiring direct inspection: input snapshots, final stability barrier, restoration, diagnostics
Areas intentionally out of scope: M2, M3, M4, PR, and final verification
Risk classes considered: temporal retry; recovery; identity authority; composition
Falsifiable review questions: Can source or manifest mutation during projection return success
Material findings: CR-M1-R6-001
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding

### CR-M1-R6-001 — Projection can return success for an already-stale transaction

Finding ID: CR-M1-R6-001
Severity: blocker
Location: `scripts/boundary_first_reference.py`
Evidence: Mutating the compact source after the first target write allowed `ok=True` even though a returned projection differed from the current canonical source.
Required outcome: Projection never reports success when the manifest or a canonical resource changes during the operation; write mode restores prior targets and retry remains deterministic.
Safe resolution path: Re-read all canonical inputs before success, compare with preflight snapshots, restore write targets on drift, and add early/middle/late source and manifest mutation tests.
needs-decision rationale: none
Auto-fix class: declared-safe

## Requirement-fidelity receipt

Applicability: applicable
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: present for in-operation input stability
No-finding rationale: not-applicable because a material finding exists

## Independent-review receipts

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Independence level: L2
Second review: satisfied; one reviewer requested changes and one returned clean-with-notes
Confidence: high

No clean-review sufficiency receipt is issued because the review is not clean.
