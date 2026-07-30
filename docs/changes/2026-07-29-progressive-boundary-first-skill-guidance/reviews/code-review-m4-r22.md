# M4 Code Review R22

Review ID: code-review-m4-r22
Stage: code-review
Round: 22
Reviewer: two independent L2 Codex reviewers
Target: d8635d32..ed2a2140
Reviewed artifact: commit ed2a2140
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r21-resolution
Reviewer context ID: m4-r22-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: dollar opener boundaries; escaped interior dollar
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/skill-contract.md; specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:ed2a2140.diff@ed2a2140#sha256:30f0e56395daab3ef19f03568678a8e9ec062d860d4b434202775d89741cf98c
Prompt template version: code-review-v1
Initial packet hash: sha256:30f0e56395daab3ef19f03568678a8e9ec062d860d4b434202775d89741cf98c
Manifest owner: workflow-orchestrator
Affected behavior: published workflow portability classification
Highest-impact failure modes: opener dollars close math; escaped interior dollars hide the real closer
Changed boundaries: braced variables; command substitutions; escape parity; same-line closer search
Evidence expected: plain command positives and escaped-interior math negatives
Areas requiring direct inspection: closer scan; opener boundary; public evaluator
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; maintainability
Falsifiable review questions: Can braced-variable or command-substitution dollars close math; can an escaped interior dollar prevent discovery of a later closer
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R22-001, CR-M4-R22-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M4-R22-001 — Braced and subshell openers masquerade as closers

Finding ID: CR-M4-R22-001
Severity: blocker
Location: `scripts/adapter_distribution.py:512-525`
Evidence: Plain `$plan` commands followed by `${HOME}` or `$(pwd)` remain portable because `{` and `(` are accepted after the alleged closer.
Required outcome: Braced-variable and command-substitution opening dollars cannot close paired math.
Safe resolution path: Reject `{` and `(` after a closer and add plain public-evaluator controls.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R22-002 — Escaped interior dollar prevents discovery of the closer

Finding ID: CR-M4-R22-002
Severity: blocker
Location: `scripts/adapter_distribution.py:499-511`
Evidence: `$plan + \$5$` is classified as an invocation because only the first subsequent dollar is inspected.
Required outcome: Skip escaped interior dollars while scanning for a plausible same-line closer; retain odd sole-closer and opening-token rejection.
Safe resolution path: Scan later dollar candidates, allow escaped-dollar literals inside the bounded suffix, and add escape-parity controls.
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
Compressed requirement risk: one-shot closer inspection is incomplete
Requirement-fidelity no-finding rationale: not-applicable because material findings exist

## Result

M4 remains open for a bounded closer scan and opener exclusions.
