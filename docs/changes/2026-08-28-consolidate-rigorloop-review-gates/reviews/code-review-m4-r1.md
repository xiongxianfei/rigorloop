# Code Review M4 R1: Canonical Review Responsibilities

Review ID: code-review-m4-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review with fresh-assumption reset
Review date: 2026-08-30
Target: M4 implementation in commit `f8565829`
Reviewed milestone: M4
Recording status: recorded
Status: changes-requested
Material findings: CRG-M4-CR1, CRG-M4-CR2

## Result

- Skill: code-review
- Status: completed
- Open blockers: CRG-M4-CR1 and CRG-M4-CR2
- Next stage: review-resolution
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4, M5, M6
- Verify readiness: not-claimed

## Review inputs

- Actual diff: canonical review skills, workflow guidance, proposal template,
  governing text, and focused skill-contract tests in commit `f8565829`.
- Governing authority: CRG-R1 through CRG-R10, CRG-R31 through CRG-R40,
  CRG-R43 through CRG-R45, the approved package-topology ADR, and M4 of the
  approved plan.
- Validation evidence: M4 implementation evidence and the reported canonical
  skill, build, prose, and regression results.

## Findings

### Finding CRG-M4-CR1

Finding ID: CRG-M4-CR1
Severity: major
Location: `CONSTITUTION.md:150-158`
Evidence: The new unconditional `MUST` rules make Proposal Review, Design Review,
and Delivery Review authoritative immediately, while the atomic-cutover contract
requires this implementing change and all other legacy-dependent work to remain
under the pre-cutover workflow until one reviewed release revision. Only the
retirement sentence is qualified by "At consolidated cutover".
Required outcome: The constitution must state that the consolidated package-gate
rules take effect at cutover and that the implementing change remains governed by
the pre-cutover sequence.
Safe resolution path: Qualify the complete consolidated-gate block with the
cutover boundary and keep the existing atomic-retirement sentence.
needs-decision rationale: none

### Finding CRG-M4-CR2

Finding ID: CRG-M4-CR2
Severity: major
Location: `docs/workflows.md:431-437` and
`scripts/test-skill-validator.py:11692-11705`
Evidence: The operational workflow guide says its supported automation stages are
the legacy target set and provides no adjacent post-cutover target inventory.
The canonical workflow skill does provide that inventory. The new regression
only checks that the consolidated graph and a prose phrase exist, so the guide
can omit the actual new target list while tests pass.
Required outcome: The guide must explicitly distinguish the currently supported
pre-cutover targets from the post-cutover target set, and focused proof must fail
if the post-cutover inventory is absent or contains retired review targets.
Safe resolution path: Add one concise adjacent post-cutover target sentence and
strengthen the M4 regression around that exact sentence without activating the
new topology early.
needs-decision rationale: none

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Both findings violate the single atomic-cutover contract. |
| Test coverage | block | The workflow-guide regression does not prove its post-cutover target inventory. |
| Architecture boundaries | concern | Canonical surfaces disagree about when and where the new authority applies. |
| Compatibility | block | The highest-priority repository rule appears to switch authority before M6. |
| Unrelated changes | pass | Review is bounded to M4. |
| Validation evidence | concern | Commands pass, but the assertions permit the two publication defects. |

## Handoff

This review is recorded before correction. M4 remains review-requested. Resolve
CRG-M4-CR1 and CRG-M4-CR2 through the implementation owner, rerun the canonical
skill and prose checks, and return M4 for fresh code review.
