# M2 Code Review R3

Review ID: code-review-m2-r3
Stage: code-review
Round: 3
Reviewer: two independent L2 Codex reviewers
Target: 4af4edd2..db77a533
Reviewed artifact: commit db77a533
Reviewed milestone: M2
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m2-r2-resolution
Reviewer context ID: m2-r3-primary-and-second-independent-agents
Context separation mechanism: separate-agents-remediation-review
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: semantic proof; closed vocabulary
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: commit:db77a533.diff@db77a533#sha256:395ff2c096f220ef2ce32aa4d292e677a5b66b0b5fd131becf16a56f672cca72; remediation:607de50f..db77a533.diff@db77a533#sha256:42108b259279140e86cfa7f2faa9a9b1ba40940fbc38bf675bf3cbf2dc40ef8c
Prompt template version: code-review-v1
Initial packet hash: sha256:395ff2c096f220ef2ce32aa4d292e677a5b66b0b5fd131becf16a56f672cca72
Manifest owner: workflow-orchestrator
Affected behavior: malformed-row and case-identity validation
Highest-impact failure modes: invalid rows reach the oracle; malformed rows crash coverage aggregation
Changed boundaries: row shape; case identity; skill identity; decision evaluation; coverage aggregation
Evidence expected: bounded diagnostics before dependent logic
Areas requiring direct inspection: semantic validator and mutation tests
Areas intentionally out of scope: M3, M4, final verification, PR
Risk classes considered: closed vocabulary; malformed input; semantic proof
Falsifiable review questions: Can an unknown case ID reach the oracle; can malformed rows raise
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Material findings: CR-M2-R3-001
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Reconciliation

`CR-M2-R1-001` is resolved. `CR-M2-R2-001` is substantially corrected, but its fail-closed boundary remains open through this narrower finding.

## Finding

### CR-M2-R3-001 — Case identity and malformed rows do not fail closed

Finding ID: CR-M2-R3-001
Severity: blocker
Location: `scripts/test-skill-validator.py`
Evidence: Unknown case IDs reach decision evaluation before the final set comparison. Missing row fields can later raise `KeyError` in coverage comprehensions. Case and skill types are not validated before set membership.
Required outcome: Validate row shape, case ID, skill ID, field types, and vocabularies before duplicate checks, oracle evaluation, guidance reads, or coverage aggregation; malformed rows return bounded errors.
Safe resolution path: Track only fully validated rows; add unknown/invalid case and skill mutations, missing/extra/non-dictionary row mutations, and a spy proving invalid rows never call the oracle.
needs-decision rationale: none
Auto-fix class: declared-safe

## Requirement-fidelity receipt

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/test-skill-validator.py
Requirement-fidelity matched path triggers: scripts/*validator*
Requirement-fidelity matched category triggers: spec-derived validators; closed enums
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > decomposition > implementation diff > validator assertions > validation evidence
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: no
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: malformed identity validation
Requirement-fidelity no-finding rationale: not-applicable because a material finding exists

## Result

- Review status: changes-requested
- Material findings: CR-M2-R3-001
- Required review-resolution: yes
- Reviewed milestone: M2
- Verify readiness: not-claimed
- Next stage: review-resolution
