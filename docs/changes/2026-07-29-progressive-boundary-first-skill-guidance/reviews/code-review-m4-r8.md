# M4 Code Review R8

Review ID: code-review-m4-r8
Stage: code-review
Round: 8
Reviewer: two independent L2 Codex reviewers
Target: 7bcf48bd..b5b9ca72
Reviewed artifact: commit b5b9ca72
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r7-resolution
Reviewer context ID: m4-r8-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: rendered-text normalization; command-record boundaries; fail-closed parsing
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:b5b9ca72.diff@b5b9ca72#sha256:cc1f99666d11eb7fde21d3857c3e581fc37d1f8ab71e69e8a0c10bf415d15309
Prompt template version: code-review-v1
Initial packet hash: sha256:cc1f99666d11eb7fde21d3857c3e581fc37d1f8ab71e69e8a0c10bf415d15309
Manifest owner: workflow-orchestrator
Affected behavior: cross-adapter workflow invocation portability
Highest-impact failure modes: rendered formatting hides adapter labels or adjacent text extends an approved command
Changed boundaries: HTML comments and attributes; Markdown inline formatting; adjacent code-span text
Evidence expected: parser-derived visible text and complete command-owning records
Areas requiring direct inspection: portability parser and mutation matrix
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; fail-closed input
Falsifiable review questions: Can supported rendered formatting hide an adapter label; can adjacent text extend an approved command code span
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R8-001, CR-M4-R8-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M4-R8-001 — Rendered formatting still hides adapter labels

Finding ID: CR-M4-R8-001
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: HTML comments, quoted `>` attributes, non-allowlisted elements, and Markdown emphasis or links can split a rendered Codex, Claude, or OpenCode label while preserving portability.
Required outcome: Residual-label closure operates on normalized rendered visible text for supported HTML and Markdown inline constructs.
Safe resolution path: Use a bounded HTML parser, normalize Markdown inline constructs, and add cross-adapter mutations for comments, quoted attributes, emphasis, and links.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R8-002 — Adjacent text extends exact command code spans

Finding ID: CR-M4-R8-002
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: Appending `-now` or `-extra` directly after an approved command code span preserves the exact span multiset and leaves no residual dollar invocation.
Required outcome: Approved commands match complete owning records, including boundaries immediately outside code spans.
Safe resolution path: Validate the exact Markdown list items that own the three approved command forms and add adjacent prefix and suffix mutations.
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
Compressed requirement risk: present in rendered-text and owning-record closure
Requirement-fidelity no-finding rationale: not-applicable because material findings exist

## Result

M4 remains open for parser-derived visible text and exact command-owning list items.
