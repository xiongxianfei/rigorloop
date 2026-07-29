# M4 Code Review R7

Review ID: code-review-m4-r7
Stage: code-review
Round: 7
Reviewer: two independent L2 Codex reviewers
Target: 1dd4136b..0ef98a01
Reviewed artifact: commit 0ef98a01
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r6-resolution
Reviewer context ID: m4-r7-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: HTML visible-text normalization; exact command boundaries; fail-closed parsing
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:0ef98a01.diff@0ef98a01#sha256:0f5a915ea1ec26b427c7995b8e51a6309a135a9b729fa022b1db628c85b7b963
Prompt template version: code-review-v1
Initial packet hash: sha256:0f5a915ea1ec26b427c7995b8e51a6309a135a9b729fa022b1db628c85b7b963
Manifest owner: workflow-orchestrator
Affected behavior: cross-adapter workflow invocation portability
Highest-impact failure modes: markup hides adapter labels or approved commands are accepted as invalid prefixes
Changed boundaries: inline HTML; code spans; command prefixes, suffixes, and trailing arguments
Evidence expected: normalized visible-text closure and exact approved command records
Areas requiring direct inspection: portability parser and mutation matrix
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; fail-closed input
Falsifiable review questions: Can inline HTML split a residual adapter label; can an approved Codex command survive inside an invalid command
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R7-001, CR-M4-R7-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M4-R7-001 — Inline HTML hides residual adapter labels

Finding ID: CR-M4-R7-001
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: Normalization removes only `code` tags, so `Co<em>dex</em>`, `Cla<strong>ude</strong>`, and `Open<span>Code</span>` residual labels remain portable.
Required outcome: Residual-label closure operates on normalized visible text after ordinary inline HTML markup is removed.
Safe resolution path: Use bounded HTML-to-visible-text normalization and add split-tag mutations for every supported adapter label.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R7-002 — Approved Codex commands are accepted as invalid prefixes

Finding ID: CR-M4-R7-002
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`
Evidence: Unrestricted substring removal accepts malformed forms including `status-now`, `status extra`, `office`, `<target-stage>-extra`, and a prefixed `x$workflow auto: status`.
Required outcome: The approved Codex invocations match complete exact command records rather than substrings.
Safe resolution path: Compare the exact multiset of dollar-command code spans before residual-label checks and add prefix, suffix, and trailing-argument mutations.
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
Compressed requirement risk: present in HTML normalization and exact command records
Requirement-fidelity no-finding rationale: not-applicable because material findings exist

## Result

M4 remains open for generic inline-markup normalization and exact Codex command-record validation.
