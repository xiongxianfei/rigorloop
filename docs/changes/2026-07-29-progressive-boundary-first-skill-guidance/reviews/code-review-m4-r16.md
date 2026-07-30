# M4 Code Review R16

Review ID: code-review-m4-r16
Stage: code-review
Round: 16
Reviewer: two independent L2 Codex reviewers
Target: 24f2bcac..39af0da6
Reviewed artifact: commit 39af0da6
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r15-resolution
Reviewer context ID: m4-r16-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: narrow static scope; invocation vocabulary; path boundaries
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/skill-contract.md; specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:39af0da6.diff@39af0da6#sha256:c12d2e8c6b123e78932830413972164d787aaa1b80ed1cee9ba5f3bc0a32e950
Prompt template version: code-review-v1
Initial packet hash: sha256:c12d2e8c6b123e78932830413972164d787aaa1b80ed1cee9ba5f3bc0a32e950
Manifest owner: workflow-orchestrator
Affected behavior: published workflow portability classification
Highest-impact failure modes: missed case variants and false positives on variables or longer paths
Changed boundaries: dollar-token vocabulary; governed skill names; slash-command termination
Evidence expected: positive invocation controls and portable negative controls
Areas requiring direct inspection: portability trigger; residual checks; narrow-scope mutation matrix
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: portability; normalization; maintainability
Falsifiable review questions: Do outer and inner dollar checks use the same governed vocabulary; are shell variables, math notation, and longer workflow paths portable
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R16-001, CR-M4-R16-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M4-R16-001 — Dollar-token trigger and residual vocabulary differ

Finding ID: CR-M4-R16-001
Severity: blocker
Location: `scripts/adapter_distribution.py:68`; `scripts/adapter_distribution.py:368`; `scripts/adapter_distribution.py:429`
Evidence: Standalone uppercase governed-skill tokens bypass the outer lowercase trigger even though the residual check rejects them when another lowercase token activates the workflow checker.
Required outcome: The portability trigger and residual dollar-token check use one case-insensitive governed-skill vocabulary.
Safe resolution path: Compile one governed-skill invocation pattern, reuse it at both sites, and add standalone case-variant regressions.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R16-002 — Raw invocation patterns reject variables and longer paths

Finding ID: CR-M4-R16-002
Severity: blocker
Location: `scripts/adapter_distribution.py:68`; `scripts/adapter_distribution.py:429-436`
Evidence: `$project`, `$x$`, `/workflow-guide`, `/workflow.md`, and `/workflow/status` are classified as Codex-only despite being variables, math notation, or longer paths.
Required outcome: Reject actual governed `$skill` invocations and unqualified `/workflow` commands without rejecting unrelated variables, notation, or path suffixes.
Safe resolution path: Restrict dollar tokens to the closed governed-skill vocabulary and require slash-command termination or recognized whitespace-delimited arguments.
needs-decision rationale: none
Auto-fix class: declared-safe

## Requirement-fidelity receipt

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/adapter_distribution.py; scripts/test-adapter-distribution.py; skills/workflow/SKILL.md
Requirement-fidelity matched path triggers: skills/; scripts/*validator*
Requirement-fidelity matched category triggers: skill instructions derived from specs; spec-derived validators
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > feature spec > implementation diff > validator assertions > validation evidence
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: no
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: broad token patterns exceed R3l
Requirement-fidelity no-finding rationale: not-applicable because material findings exist

## Result

M4 remains open for a shared governed-skill pattern and command-boundary negative controls.
