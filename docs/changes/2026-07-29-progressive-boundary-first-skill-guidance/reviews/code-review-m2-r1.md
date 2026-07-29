# M2 Code Review R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: two independent L2 Codex reviewers
Target: 4af4edd2..28ca8cb7
Reviewed artifact: commit 28ca8cb7
Reviewed milestone: M2
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m2-implementation
Reviewer context ID: m2-primary-and-second-independent-agents
Context separation mechanism: separate-agents-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: public skill behavior; multi-surface guidance; compatibility state; semantic proof
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md@28ca8cb7#sha256:983a6cab29dd12ff18866f06a2a818ab9c198dd3a3ccddccc06c8e95516d2dd2; specs/progressive-boundary-first-skill-guidance.test.md@28ca8cb7#sha256:30595f49cb782e772588334dc9b6c31c728f5b6567892784d6fa27488e3f5257; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md@28ca8cb7#sha256:7aa4b69d2636eb0ff6bf6fb77bcf6835ad2dd5c889feaa8b786e1badce65d5c1; docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md@28ca8cb7#sha256:ad78a2f644679a6b0dbaaa6000c1c9b0a8751f9abeb238fcb74cee04e16181c9
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: governing artifacts plus commit:28ca8cb7.diff@28ca8cb7#sha256:b839825c76b9dc9672ddb4d183b4fb4ffb84d21cd20848878ff5daf4df8384a4
Prompt template version: code-review-v1
Initial packet hash: sha256:b839825c76b9dc9672ddb4d183b4fb4ffb84d21cd20848878ff5daf4df8384a4
Manifest owner: workflow-orchestrator
Affected behavior: automatic compact scanning, stage ownership, slice routing, scenario selection, and compatibility guidance
Highest-impact failure modes: prompt dependence; pending-active collapse; over-formalization; authority leakage; circular semantic proof
Changed boundaries: invocation; lifecycle state; stage authority; approved slices; sibling paths; recovery routing; compatibility
Evidence expected: exact scan, semantic matrix, authority isolation, slice expansion, scenario stop, generated parity
Areas requiring direct inspection: shared block; ten skills; fixture; test oracle; resources; generated output
Areas intentionally out of scope: M3, M4, final verification, and PR
Risk classes considered: contract fidelity; prompt independence; authority; progressive loading; compatibility; semantic proof; proportionality
Falsifiable review questions: Can contradictory fixture inputs pass; do equivalent named and unnamed requests differ; can invalid IDs or sibling paths evade routing
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Material findings: CR-M2-R1-001
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding

### CR-M2-R1-001 — Semantic scenario proof does not validate scenario decisions

Finding ID: CR-M2-R1-001
Severity: blocker
Location: `scripts/test-skill-validator.py`; `scripts/fixtures/boundary-first/semantic/progressive-cases.json`
Evidence: The scenario test checks shape, vocabularies, and selected fixture-authored values but does not derive expected action or route from the inputs. Both reviewers mutated inputs or expected actions into contradictory combinations and the focused test still passed. The fixture also omits named/unnamed equivalence, six invalid or insufficient identity partitions, substantive and undecidable revisions, sufficient-slice progress, owned sibling proof, recovery, ownerless discovery, and structural-pass/semantic-gap cases.
Required outcome: Semantic proof must fail when inputs contradict expected action or route and must cover the M2 state, identity, sibling-path, explanation, consent, recovery, and semantic-ownership distinctions required by the test spec and plan.
Safe resolution path: Add a deterministic test-owned oracle, bind cases to required and forbidden shipped guidance, complete the distinct scenario partitions, and add negative mutation and coverage tests.
needs-decision rationale: none
Auto-fix class: declared-safe

## Requirement-fidelity receipt

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: templates/shared/boundary-first-compact-scan.md; skills/workflow/SKILL.md; skills/spec/SKILL.md; skills/spec-review/SKILL.md; skills/plan/SKILL.md; skills/plan-review/SKILL.md; skills/test-spec/SKILL.md; skills/test-spec-review/SKILL.md; skills/implement/SKILL.md; skills/code-review/SKILL.md; skills/verify/SKILL.md; scripts/test-skill-validator.py; scripts/fixtures/boundary-first/semantic/progressive-cases.json
Requirement-fidelity matched path triggers: skills/; templates/; scripts/*validator*
Requirement-fidelity matched category triggers: skill instructions derived from specs; multi-surface public skill guidance; spec-derived validators
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > decomposition > expected surfaces > implementation diff > validator assertions > validation evidence
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: no
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: present in semantic scenario proof
Requirement-fidelity no-finding rationale: not-applicable because a material finding exists

## Result

- Skill: code-review
- Status: completed
- Review status: changes-requested
- Material findings: CR-M2-R1-001
- Recording status: recorded
- Required review-resolution: yes
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Verify readiness: not-claimed
- Next stage: review-resolution
