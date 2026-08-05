# M4 Code Review R23

Review ID: code-review-m4-r23
Stage: code-review
Round: 23
Reviewer: two independent L2 Codex reviewers
Target: 3a57a6b7..f573e592
Reviewed artifact: commit f573e592
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r22-resolution
Reviewer context ID: m4-r23-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: candidate-dollar escape parity
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/skill-contract.md; specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:f573e592.diff@f573e592#sha256:7411fe4ae0f2bbba9cde1c2cda237f8ac215253827695d8d94cd8fc5ea46047d
Prompt template version: code-review-v1
Initial packet hash: sha256:7411fe4ae0f2bbba9cde1c2cda237f8ac215253827695d8d94cd8fc5ea46047d
Manifest owner: workflow-orchestrator
Affected behavior: published workflow portability classification
Highest-impact failure modes: escaped governed-name literals are treated as commands
Changed boundaries: odd and even backslash parity at the candidate dollar
Evidence expected: public evaluator parity controls
Areas requiring direct inspection: candidate match boundary and shared escape helper
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; maintainability
Falsifiable review questions: Do odd-escaped candidates remain portable while even and unescaped candidates fail
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R23-001
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding

### CR-M4-R23-001 — Escape parity is not applied to candidate dollars

Finding ID: CR-M4-R23-001
Severity: blocker
Location: `scripts/adapter_distribution.py:489-495`
Evidence: Odd-escaped `\$plan` and `\\\$plan` literals are classified as Codex invocations; the second reviewer did not reproduce a material issue, so the conservative material verdict governs.
Required outcome: Odd-escaped governed-name literals remain portable while unescaped and even-backslash tokens remain commands.
Safe resolution path: Apply the shared escape-parity helper at each candidate match and add public controls.
needs-decision rationale: none
Auto-fix class: declared-safe

## Requirement-fidelity receipt

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/adapter_distribution.py; scripts/test-adapter-distribution.py
Requirement-fidelity matched path triggers: scripts/*validator*
Requirement-fidelity matched category triggers: spec-derived validators
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > feature spec > implementation diff > validator assertions > validation evidence
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: no
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: shared parity is not applied at both dollar boundaries
Requirement-fidelity no-finding rationale: not-applicable because a material finding exists

## Result

M4 remains open for candidate-dollar escape parity.
