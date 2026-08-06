# Code Review: M1 R3

Review ID: code-review-m1-r3
Stage: code-review
Round: 3
Reviewer: two independent L2 Codex reviewers
Target: 3852a010..e418519c
Reviewed artifact: corrected M1 implementation range
Reviewed milestone: M1
Review date: 2026-08-05
Recording status: recorded
Status: blocked
Review status: blocked
Automated review: yes
Native review status: blocked
Review gate outcome: blocked
Independence level: L2
Author context ID: root-m1-review-resolution-r2
Reviewer context ID: m1-r3-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@e418519c#sha256:48a42eb23156330bc7a60a869c93ec512e3c0b8e79b29587ccfbd94eebab8db9; specs/boundary-first-v1-v0-3-7-activation-release.test.md@e418519c#sha256:41db52a5c323377576cfd44bfe55a929126ad7654197e0c079349f5591f2f898; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@e418519c#sha256:e940e7d27ad26287f33bb65a2616e096d6b5ed805b6aa95346ea4a4c5370af91; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@e418519c#sha256:911b77ee4384c8576269a04233e7581865075bda3a78277f67371b3afca2d2e5; range:3852a010..e418519c.diff@e418519c#sha256:aca05bdfab93e82a34b031ad5002d986fadb0c7a1f9c118976bc576a564a5e4b
Initial packet hash: sha256:db8be39cd73715a7f5c6376868bf8e6551c0d4b57def545bede4ec89549aa811
Risk tier: elevated
Risk-tier triggers: validator behavior; remote authority read; release boundary; lifecycle gate
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: spec, test spec, M1 plan, activation-publication ADR
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Affected behavior: candidate evidence identity; merged ancestry; invocation authority; privacy serialization; sibling composition
Highest-impact failure modes: self-referential final H; shallow manifest acceptance; short private-value disclosure; omitted sibling failure
Changed boundaries: BND-AUTH-001; BND-STATE-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-ENV-001
Evidence expected: producing-head graph; complete ancestry; canonical invocation shape; privacy probes; every selected sibling failure
Areas requiring direct inspection: candidate evidence helper; Git traversal; invocation validation; privacy bounds; selected execution
Areas intentionally out of scope: publication mutation; release payload; real transition; public release; final verify
Risk classes considered: identity authority; lifecycle; temporal recovery; composition; privacy; compatibility
Falsifiable review questions: can final H be represented; can shallow payloads, short private values, or omitted sibling failures pass
Material findings: BFA-M1-R3-001
Immediate next stage: review-resolution
Milestone closeout: blocked
Required review-resolution: yes
Verify readiness: not-claimed
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Second review: satisfied; both reviewers stopped on the upstream identity conflict

## Result

- Skill: code-review
- Status: blocked
- Review status: blocked
- Reviewed target: `3852a010..e418519c`
- Reviewed milestone: M1
- New material findings: BFA-M1-R3-001
- Recording status: recorded
- Review resolution: required
- Milestone closeout: blocked
- Remaining implementation milestones: M1, M2, M3, M4
- Next stage: upstream spec/architecture decision, then M1 resolution and R4
- Verify readiness: not-claimed

## Independent review gate

A fresh L2 reviewer and the prior primary reviewer recorded risk maps before R3
evidence was released. Both independently identified the same unrepresentable
final-head self-reference and stopped downstream handoff.

## Finding

### BFA-M1-R3-001 — Final evidence-bearing H is self-referential

Finding ID: BFA-M1-R3-001
Severity: blocker
Location: feature spec glossary, BFA-R010/R012/R017, M4 plan, ADR, and candidate evidence binding
Evidence: candidate validation at R reports R; committing that JSON creates C, so the final evidence-bearing head cannot be R. The implementation accepts R as the producer parent and a later current H, silently introducing a two-head model absent from the approved contract.
Required outcome: define a realizable identity model distinguishing candidate-producing head from final evidence-bearing publication head, or choose a different non-self-referential evidence mechanism.
Safe resolution path: amend and review spec, architecture/ADR, plan, and test spec, then align implementation and rerun M1 review.
needs-decision rationale: a tracked file committed at final H cannot contain the hash of its containing commit, so implementation cannot satisfy the literal approved contract.

## Open-finding reconciliation

| Finding | R3 status | Basis |
| --- | --- | --- |
| BFA-M1-CR1-003 | needs-decision | Forgery binding works technically but depends on the unapproved producer-parent interpretation. |
| BFA-M1-CR1-005 | still open | One reviewer reproduced omitted `rigorloop_cli.test` failure injection and missing short private-environment proof. |
| BFA-M1-CR1-007 | still open | One reviewer reproduced acceptance of a four-field invocation plus arbitrary extra payload. |
| BFA-M1-CR1-008 | still open | One reviewer reproduced a four-character private environment value in a drift path. |
| BFA-M1-R2-001 | resolved | Complete T..H traversal rejects merged side-branch change/revert history. |

## Evidence challenge

Both suites were rerun independently: CMD1 passed 82 tests and the selector
suite passed 146. CMD2, CMD3, exact CMD4, canonical lifecycle checks, and
`git diff --check` are credible. The gate remains blocked by the identity-model
conflict and the three narrower reproduced gaps above.
