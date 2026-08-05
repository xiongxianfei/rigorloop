# M4 Code Review R18

Review ID: code-review-m4-r18
Stage: code-review
Round: 18
Reviewer: two independent L2 Codex reviewers
Target: ea74c581..097d2af1
Reviewed artifact: commit 097d2af1
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r17-resolution
Reviewer context ID: m4-r18-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: Unicode identifiers; paired-dollar math; ASCII command identity; parent-path context
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/skill-contract.md; specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:097d2af1.diff@097d2af1#sha256:66fafcc3db140c1c94f86e0b1c85de4f60a1fc70c24f82215eab03a8ff055e7a
Prompt template version: code-review-v1
Initial packet hash: sha256:66fafcc3db140c1c94f86e0b1c85de4f60a1fc70c24f82215eab03a8ff055e7a
Manifest owner: workflow-orchestrator
Affected behavior: published workflow portability classification
Highest-impact failure modes: Unicode/math false positives and non-ASCII command aliases
Changed boundaries: identifier continuation; paired dollars; ASCII case identity; hyphenated parent paths
Evidence expected: direct positive and negative token-context controls
Areas requiring direct inspection: dollar candidate predicate; slash identity and left boundary; mutation matrix
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; maintainability
Falsifiable review questions: Are Unicode identifiers and paired-dollar math outside invocation scope; are command names ASCII-case-insensitive without Unicode case-fold aliases; are hyphenated parent paths outside slash-command scope
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R18-001, CR-M4-R18-002, CR-M4-R18-003
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M4-R18-001 — Unicode identifiers and paired math match governed prefixes

Finding ID: CR-M4-R18-001
Severity: blocker
Location: `scripts/adapter_distribution.py:94-101`
Evidence: Combining/variation continuations and paired expressions such as `$plań`, `$workflow️`, `$plan + 1$`, and `$plan^2$` are classified as invocations.
Required outcome: Complete-token detection leaves Unicode identifiers and paired-dollar math outside invocation scope.
Safe resolution path: Post-filter governed-name candidates with an explicit Unicode continuation predicate and a narrow same-line paired-dollar check.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R18-002 — Unicode case folding expands command vocabulary

Finding ID: CR-M4-R18-002
Severity: blocker
Location: `scripts/adapter_distribution.py:94-107`
Evidence: `$ſpec`, `$ımplement`, `$worKflow`, and `/worKflow` match unpublished Unicode case-fold aliases.
Required outcome: Command identities are ASCII-case-insensitive without expanding beyond the closed ASCII vocabulary.
Safe resolution path: Scope case-insensitive matching to ASCII and add Unicode case-fold negative controls.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R18-003 — Hyphenated parent paths match slash commands

Finding ID: CR-M4-R18-003
Severity: blocker
Location: `scripts/adapter_distribution.py:103-107`
Evidence: `docs-/workflow` matches an exact slash command even though it is a hyphenated path component.
Required outcome: Slash-command recognition excludes hyphenated parent route and file contexts.
Safe resolution path: Add hyphen to the left path-context boundary and retain exact-command positives.
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
Compressed requirement risk: regex-only token semantics exceed R3l
Requirement-fidelity no-finding rationale: not-applicable because material findings exist

## Result

M4 remains open for a narrow dollar-candidate predicate, ASCII command identity, and parent-path exclusion.
