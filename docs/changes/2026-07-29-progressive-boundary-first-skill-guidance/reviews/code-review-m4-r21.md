# M4 Code Review R21

Review ID: code-review-m4-r21
Stage: code-review
Round: 21
Reviewer: two independent L2 Codex reviewers
Target: fa5a15e3..3d9c79dd
Reviewed artifact: commit 3d9c79dd
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r20-resolution
Reviewer context ID: m4-r21-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: closing-dollar boundary; invocation false negative
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/skill-contract.md; specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:3d9c79dd.diff@3d9c79dd#sha256:bb0b13419da27984bf1e72d179033d4be38e7df670100b6e6e5abbc1bd9e0af4
Prompt template version: code-review-v1
Initial packet hash: sha256:bb0b13419da27984bf1e72d179033d4be38e7df670100b6e6e5abbc1bd9e0af4
Manifest owner: workflow-orchestrator
Affected behavior: published workflow portability classification
Highest-impact failure modes: an opening variable dollar masquerades as a math closer
Changed boundaries: closer escaping and following identifier; digit; dollar; hyphen
Evidence expected: generic operator-led command positives plus paired-math negatives
Areas requiring direct inspection: closing-dollar plausibility and public evaluator
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; maintainability
Falsifiable review questions: Can an opening variable, currency, or escaped dollar close paired math
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R21-001
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding

### CR-M4-R21-001 — An opening dollar can masquerade as the math closer

Finding ID: CR-M4-R21-001
Severity: blocker
Location: `scripts/adapter_distribution.py:107-109`; `scripts/adapter_distribution.py:499-506`
Evidence: Operator-led command prose before `$HOME`, `$PATH`, `$5`, or escaped dollar text is accepted as paired math and hides the real governed invocation.
Required outcome: A paired-math closer is unescaped and cannot open an identifier, currency token, dollar token, or hyphen continuation.
Safe resolution path: Check the selected dollar's preceding escape and following token boundary before accepting the structural suffix.
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
Compressed requirement risk: closer identity is not checked
Requirement-fidelity no-finding rationale: not-applicable because a material finding exists

## Result

M4 remains open for a plausible closing-dollar boundary.
