# M1 Code Review R5

Review ID: code-review-m1-r5
Stage: code-review
Round: 5
Reviewer: two independent L2 Codex reviewers
Target: 9d16bbe2..e26ff0c9
Reviewed artifact: commit e26ff0c9
Reviewed milestone: M1
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m1-r4-resolution
Reviewer context ID: m1-r5-primary-and-second-fresh-agents
Context separation mechanism: fresh-separate-agents-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: validator behavior; generated-output machinery; compatibility identity; multi-component change
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md; docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/progressive-boundary-first-skill-guidance.md@e26ff0c9#sha256:983a6cab29dd12ff18866f06a2a818ab9c198dd3a3ccddccc06c8e95516d2dd2; specs/progressive-boundary-first-skill-guidance.test.md@e26ff0c9#sha256:30595f49cb782e772588334dc9b6c31c728f5b6567892784d6fa27488e3f5257; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md@e26ff0c9#sha256:7aa4b69d2636eb0ff6bf6fb77bcf6835ad2dd5c889feaa8b786e1badce65d5c1; docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md@e26ff0c9#sha256:ad78a2f644679a6b0dbaaa6000c1c9b0a8751f9abeb238fcb74cee04e16181c9; commit:e26ff0c9.diff@e26ff0c9#sha256:d4e81185f10b2dd94cb9cbbcea22e5b5aeb7a90ae5531acf79622fdab400195d
Prompt template version: code-review-v1
Initial packet hash: sha256:d4e81185f10b2dd94cb9cbbcea22e5b5aeb7a90ae5531acf79622fdab400195d
Manifest owner: workflow-orchestrator
Affected behavior: resource diagnostics and unexpected-resource inventory
Highest-impact failure modes: canonical scalar disclosure and unrelated symlink rejection
Changed boundaries: diagnostic privacy and namespace ownership
Evidence expected: public and sibling secret probes; related and unrelated symlink fixtures
Areas requiring direct inspection: version diagnostics and recursive inventory filters
Areas intentionally out of scope: M2, M3, M4, PR, and final verification
Risk classes considered: privacy; authority; composition; filesystem containment
Falsifiable review questions: Can canonical content leak; can unrelated symlinks block projection
Material findings: CR-M1-R5-001, CR-M1-R5-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M1-R5-001 — Canonical resource diagnostics disclose untrusted version scalars

Finding ID: CR-M1-R5-001
Severity: blocker
Location: `scripts/boundary_first_reference.py`
Evidence: A secret-like version scalar appears verbatim in the public projection diagnostic.
Required outcome: No untrusted canonical-resource content appears in projection, activation, or skill-validation diagnostics.
Safe resolution path: Hash the offending version value and add public and sibling regressions.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M1-R5-002 — Projection inventory rejects unrelated symlinked resources

Finding ID: CR-M1-R5-002
Severity: major
Location: `scripts/boundary_first_reference.py`
Evidence: `other-guidance.md` as a symlink under a skill reference tree triggers a boundary projection failure.
Required outcome: Fail closed on governed target topology and additional boundary resources without claiming unrelated references.
Safe resolution path: Scope recursive symlink inventory to `boundary-first-*.md` while retaining exact ancestor checks for governed paths.
needs-decision rationale: none
Auto-fix class: declared-safe

## Requirement-fidelity receipt

Applicability: applicable
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: present for diagnostic privacy and inventory ownership
No-finding rationale: not-applicable because material findings exist

## Independent-review receipts

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Independence level: L2
Second review: satisfied; one reviewer requested changes and one returned clean-with-notes
Confidence: high
Unreviewed surfaces: M2, M3, M4, and final verification

No clean-review sufficiency receipt is issued because the review is not clean.
