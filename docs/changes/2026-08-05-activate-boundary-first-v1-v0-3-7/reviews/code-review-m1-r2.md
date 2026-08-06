# Code Review: M1 R2

Review ID: code-review-m1-r2
Stage: code-review
Round: 2
Reviewer: two independent L2 Codex reviewers
Target: 3852a010..d1dc3328
Reviewed artifact: corrected M1 implementation range
Reviewed milestone: M1
Review date: 2026-08-05
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m1-review-resolution
Reviewer context ID: m1-r2-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: validator behavior; remote authority read; release boundary; lifecycle gate
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: specs/boundary-first-v1-v0-3-7-activation-release.md@d1dc3328; specs/boundary-first-v1-v0-3-7-activation-release.test.md@d1dc3328; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@d1dc3328; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@d1dc3328
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@d1dc3328#sha256:48a42eb23156330bc7a60a869c93ec512e3c0b8e79b29587ccfbd94eebab8db9; specs/boundary-first-v1-v0-3-7-activation-release.test.md@d1dc3328#sha256:41db52a5c323377576cfd44bfe55a929126ad7654197e0c079349f5591f2f898; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@d1dc3328#sha256:e940e7d27ad26287f33bb65a2616e096d6b5ed805b6aa95346ea4a4c5370af91; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@d1dc3328#sha256:911b77ee4384c8576269a04233e7581865075bda3a78277f67371b3afca2d2e5; range:3852a010..d1dc3328.diff@d1dc3328#sha256:1af17aa9bd17d7e2a63e22557f9177ebf5f8fc54b2c0ba9561f728a237d48449
Initial packet hash: sha256:8cfda74b5a6dcdc05fb808a8600a5377fc192944aa624f443ac85aca0d7b63a9
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Affected behavior: candidate CLI; remote and Git topology authority; post-T drift; lifecycle readiness; failure serialization; selector composition
Highest-impact failure modes: merged drift bypass; forged candidate authority; arbitrary lifecycle payload; private-value disclosure; sibling-check bypass
Changed boundaries: BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001
Evidence expected: direct T1-T6, T12, and T16 adversarial Git, lifecycle, privacy, and sibling-failure proof
Areas requiring direct inspection: CLI dispatch; Git range traversal; lifecycle classifier; readiness authority; failure context; directory preflight; selector execution
Areas intentionally out of scope: M2 publication mutation; M3 payload; M4 real transition; public release; final verify
Risk classes considered: correctness; identity; lifecycle; temporal recovery; compatibility; filesystem/Git; privacy; side effects; selector composition
Falsifiable review questions: can merged drift, forged evidence, arbitrary invocation payloads, private values, or failed siblings pass
Material findings: BFA-M1-R2-001
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Second review: satisfied; both reviewers requested changes

## Result

- Skill: code-review
- Status: completed
- Review status: changes-requested
- Reviewed target: `3852a010..d1dc3328`
- Reviewed milestone: M1
- New material findings: one; four R1 findings remain open after failed remediation
- Recording status: recorded
- Review resolution: required
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4
- Next stage: review-resolution M1
- Verify readiness: not-claimed

## Independent review gate

Both L2 reviewers recorded blind-first risk maps before implementation evidence,
prior findings, resolution claims, or command results were released. They then
challenged the evidence independently and reproduced the remaining failures.

## Prior-finding reconciliation

| Finding | R2 status | Basis |
| --- | --- | --- |
| BFA-M1-CR1-001 | resolved | Presence-sensitive dispatch rejects an empty supplied value. |
| BFA-M1-CR1-002 | resolved | Parent-relative first-parent scanning catches direct change/revert, rename, deletion, and union cases. |
| BFA-M1-CR1-003 | failed-remediation | Candidate evidence identities remain format-only and can be forged or stale. |
| BFA-M1-CR1-004 | resolved | Failure output includes available context and corrective action. |
| BFA-M1-CR1-005 | failed-remediation | T16 and the reproduced R2 cases lack direct proof. |
| BFA-M1-CR1-006 | resolved | Empty, mixed, untracked, and top-level symlink directories fail preflight. |
| BFA-M1-CR1-007 | failed-remediation | The review-invocation namespace remains open-ended and shape-blind. |
| BFA-M1-CR1-008 | failed-remediation | Real runtime identities and raw non-path fields can still disclose private values. |

## Findings

### BFA-M1-R2-001 — Merged side-branch history bypasses drift detection

Finding ID: BFA-M1-R2-001
Severity: blocker
Location: `scripts/boundary_first_validation.py` post-transition traversal
Evidence: a side branch added and reverted `skills/payload/SKILL.md`, then merged after T; both forbidden commits remained reachable from H, but first-parent-only traversal returned success.
Required outcome: inspect every commit newly reachable in T..H, including non-first-parent merge ancestry, and reject the deterministic union of forbidden parent-relative paths.
Safe resolution path: traverse the complete commit range and add side-branch change/revert/merge regressions.
needs-decision rationale: none

## Evidence challenge

CMD1 passed 77 tests, CMD2 and CMD3 passed, amended CMD4 selected all
declared M1 checks without debt, the selector suite passed 144 tests, and
metadata/lifecycle checks passed. Those results are credible for their direct
assertions but do not exercise the reproduced bypasses above.
