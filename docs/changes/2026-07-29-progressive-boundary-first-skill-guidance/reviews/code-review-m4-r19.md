# M4 Code Review R19

Review ID: code-review-m4-r19
Stage: code-review
Round: 19
Reviewer: two independent L2 Codex reviewers
Target: e31cd971..f40a3b93
Reviewed artifact: commit f40a3b93
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r18-resolution
Reviewer context ID: m4-r19-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: join controls; paired-dollar locality; invocation false negative
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/skill-contract.md; specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:f40a3b93.diff@f40a3b93#sha256:7d843cd4b4fc930dba3bfff8f242fa5ad69124866fc9e01fcf30d8c87e88d51e
Prompt template version: code-review-v1
Initial packet hash: sha256:7d843cd4b4fc930dba3bfff8f242fa5ad69124866fc9e01fcf30d8c87e88d51e
Manifest owner: workflow-orchestrator
Affected behavior: published workflow portability classification
Highest-impact failure modes: join-control false positives and unrelated-dollar false negatives
Changed boundaries: ZWNJ; ZWJ; candidate-local paired math; later variables and currency
Evidence expected: generic-skill positive controls plus math-only negatives
Areas requiring direct inspection: continuation predicate; paired-dollar exemption; public evaluator
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; maintainability
Falsifiable review questions: Do ZWNJ and ZWJ identifier continuations remain portable; can an unrelated later dollar hide a real governed invocation
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R19-001, CR-M4-R19-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M4-R19-001 — Join-control identifiers match governed prefixes

Finding ID: CR-M4-R19-001
Severity: blocker
Location: `scripts/adapter_distribution.py:474-490`
Evidence: ZWNJ and ZWJ continuations after `$plan` are classified as invocations although they participate in portable identifier syntax.
Required outcome: Standard join controls count as narrow identifier continuation.
Safe resolution path: Add U+200C and U+200D to the continuation predicate and public-evaluator negatives.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R19-002 — Any later dollar suppresses a real invocation

Finding ID: CR-M4-R19-002
Severity: blocker
Location: `scripts/adapter_distribution.py:492-496`
Evidence: A real `$plan` or `$workflow` invocation followed by `$PATH`, later paired math, escaped dollar text, or currency is treated as paired math and remains portable.
Required outcome: Only a plausible candidate-local closing dollar suppresses the candidate.
Safe resolution path: Recognize the approved empty or arithmetic suffix before the closing dollar and add generic-skill failures for unrelated later dollars.
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
Compressed requirement risk: nonlocal dollar scanning exceeds R3l
Requirement-fidelity no-finding rationale: not-applicable because material findings exist

## Result

M4 remains open for join-control continuation and candidate-local paired-math recognition.
