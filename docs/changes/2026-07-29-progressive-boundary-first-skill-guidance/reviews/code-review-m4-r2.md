# M4 Code Review R2

Review ID: code-review-m4-r2
Stage: code-review
Round: 2
Reviewer: two independent L2 Codex reviewers
Target: 7e8f5d5b..f0dd6fff
Reviewed artifact: commit f0dd6fff
Reviewed milestone: M4
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m4-r1-resolution
Reviewer context ID: m4-r2-primary-and-second-independent-agents
Context separation mechanism: separate-agents
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: package parity; evidence integrity; cross-adapter composition
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md; specs/progressive-boundary-first-skill-guidance.test.md; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:f0dd6fff.diff@f0dd6fff#sha256:333168068c8262f792a769e2b19f784df1c3800996568a08fbfcf12097a83e38
Prompt template version: code-review-v1
Initial packet hash: sha256:333168068c8262f792a769e2b19f784df1c3800996568a08fbfcf12097a83e38
Manifest owner: workflow-orchestrator
Affected behavior: historical loading comparison and supported-adapter package completeness
Highest-impact failure modes: inaccurate baseline or silently omitted governed skill resources
Changed boundaries: historical measurement; portability classification; generated output; archives; clean installs
Evidence expected: source-derived loading counts and exact governed-skill adapter matrix
Areas requiring direct inspection: M4 evidence; workflow portability; clean-install completeness oracle
Areas intentionally out of scope: final holistic review, final verification, and PR
Risk classes considered: evidence integrity; package parity; cross-adapter composition
Falsifiable review questions: Does old governed downstream work load the full reference; does every adapter contain every requested governed resource
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M4-R2-001; CR-M4-R2-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### CR-M4-R2-001 — Pre-split downstream initial-load baseline contradicts its source

Finding ID: CR-M4-R2-001
Severity: major
Location: `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/evidence/m4-package-readiness.md`
Evidence: At baseline commit `9d16bbe2`, each routing or downstream skill reads the full reference for the comparable governed operation, but the evidence records zero initially loaded resources.
Required outcome: Use one comparable governed-work scenario and record one 8,318-byte initial resource for the pre-split routing/downstream family.
Safe resolution path: Correct the row and state how each family count follows from the historical and current load conditions.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M4-R2-002 — Adapter proof silently excludes workflow from Claude and opencode

Finding ID: CR-M4-R2-002
Severity: blocker
Location: `scripts/adapter_distribution.py`; `scripts/test-adapter-distribution.py`; `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/evidence/m4-package-readiness.md`
Evidence: Portability classification excludes `workflow` from Claude and opencode because its shipped body contains `$workflow`; report-derived filtering then reduces those archives and installs to 13 governed resources while the command and evidence claim 14.
Required outcome: Make workflow portable under the approved adapter contract, require the full requested governed-skill by supported-adapter matrix, assert 14-resource identity independently for every layer, and correct the evidence.
Safe resolution path: Replace Codex-only invocation prose with adapter-neutral wording, remove report-derived completeness filtering for selected governed skills, and add missing-skill and exact-identity regressions.
needs-decision rationale: none
Auto-fix class: declared-safe

## Requirement-fidelity receipt

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/adapter_distribution.py; scripts/test-adapter-distribution.py; skills/workflow/SKILL.md; docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/evidence/m4-package-readiness.md
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
Compressed requirement risk: present in cross-adapter completeness
Requirement-fidelity no-finding rationale: not-applicable because material findings exist

## Result

Both R1 implementation fixes are effective within included packages. M4 remains
open because its historical loading baseline and full supported-adapter package
matrix are not yet correct.
