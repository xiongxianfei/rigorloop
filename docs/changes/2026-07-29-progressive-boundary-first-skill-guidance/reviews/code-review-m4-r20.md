# M4 Code Review R20

Review ID: code-review-m4-r20
Stage: code-review
Round: 20
Reviewer: two independent L2 Codex reviewers
Target: 3717578b..ee739c06
Reviewed artifact: commit ee739c06
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r19-resolution
Reviewer context ID: m4-r20-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: paired-dollar structure; arithmetic false positive
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/skill-contract.md; specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:ee739c06.diff@ee739c06#sha256:4cf73926c22139a677f91cee61b0e2cbe59397215d65dcf6208594590af51ca8
Prompt template version: code-review-v1
Initial packet hash: sha256:4cf73926c22139a677f91cee61b0e2cbe59397215d65dcf6208594590af51ca8
Manifest owner: workflow-orchestrator
Affected behavior: published workflow portability classification
Highest-impact failure modes: ordinary paired arithmetic is mistaken for an invocation
Changed boundaries: multi-operator; grouped; Unicode; comparison expressions
Evidence expected: structural math negatives plus retained real-invocation positives
Areas requiring direct inspection: paired-dollar suffix predicate and public evaluator
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; maintainability
Falsifiable review questions: Does candidate-local math require an unnecessary arithmetic grammar; can unrelated later dollars still hide a real invocation
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R20-001
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding

### CR-M4-R20-001 — Paired-dollar arithmetic is compressed to one ASCII atom

Finding ID: CR-M4-R20-001
Severity: blocker
Location: `scripts/adapter_distribution.py:107-109`; `scripts/adapter_distribution.py:499-506`
Evidence: Multi-operator, grouped, Unicode, exponent, and comparison expressions inside candidate-local paired dollars are classified as invocations.
Required outcome: Candidate-local arithmetic remains outside invocation scope without restoring unrelated-later-dollar false negatives.
Safe resolution path: Use an operator-led bounded structural suffix that excludes newline, dollar, code, and prose separators; retain generic real-invocation positives.
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
Compressed requirement risk: an arithmetic grammar exceeds R3l
Requirement-fidelity no-finding rationale: not-applicable because a material finding exists

## Result

M4 remains open for a structural candidate-local paired-dollar boundary.
