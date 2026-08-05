# M4 Code Review R13

Review ID: code-review-m4-r13
Stage: code-review
Round: 13
Reviewer: two independent L2 Codex reviewers
Target: 3171fee9..e50f8830
Reviewed artifact: commit e50f8830
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r12-resolution
Reviewer context ID: m4-r13-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: nested Markdown; default-ignorable ranges; normalization precision
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:e50f8830.diff@e50f8830#sha256:5eefc25948d5159a07e64c7a4f979a3f2b9e736f987efcf6d50a7da67eb0a3f4
Prompt template version: code-review-v1
Initial packet hash: sha256:5eefc25948d5159a07e64c7a4f979a3f2b9e736f987efcf6d50a7da67eb0a3f4
Manifest owner: workflow-orchestrator
Affected behavior: cross-adapter workflow invocation portability
Highest-impact failure modes: nested formatting hides labels or omitted default-ignorables split tokens
Changed boundaries: nested Markdown; Unicode variation controls
Evidence expected: bounded recursive delimiter parsing and completed governed ranges
Areas requiring direct inspection: portability parser and mutation matrix
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; false-positive input
Falsifiable review questions: Can nested supported Markdown hide an adapter label; can an omitted variation control split a label or invocation
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R13-001, CR-M4-R13-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M4-R13-001 — Markdown normalization is not recursively delimiter-aware

Finding ID: CR-M4-R13-001
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: Nested triple emphasis, mixed emphasis, strikethrough, and link-label formatting hide rendered labels, while intraword underscore keys can be misclassified.
Required outcome: Supported nested formatting normalizes to a fixed point without removing literal intraword punctuation.
Safe resolution path: Recursively normalize bounded paired delimiters and add nested positives plus intraword-underscore negatives.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R13-002 — Default-ignorable variation ranges remain incomplete

Finding ID: CR-M4-R13-002
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: Mongolian variation selectors and Khmer inherent-vowel controls, including entity forms, split labels and slash invocations.
Required outcome: The governed default-ignorable ranges include these variation controls.
Safe resolution path: Add U+180B–U+180F and U+17B4–U+17B5 with label, entity, and slash-command regressions.
needs-decision rationale: none
Auto-fix class: declared-safe

## Requirement-fidelity receipt

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/adapter_distribution.py; scripts/test-adapter-distribution.py; skills/workflow/SKILL.md
Requirement-fidelity matched path triggers: skills/; scripts/*validator*
Requirement-fidelity matched category triggers: skill instructions derived from specs; spec-derived validators
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > decomposition > implementation diff > validator assertions > validation evidence
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: no
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: present in recursive rendering and variation controls
Requirement-fidelity no-finding rationale: not-applicable because material findings exist

## Result

M4 remains open for recursive delimiter-aware Markdown normalization and the omitted variation-control ranges.
